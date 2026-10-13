#!/usr/bin/env python3
"""Validate skill structure for the cloud-platform-skills repo.

Checks every skills/<provider>/<skill>/SKILL.md for:
  - frontmatter with name, description, and required metadata keys
  - name matching the folder and the provider prefix
  - required sections
  - a reasonable length
Also checks that every skill is listed in .claude-plugin/marketplace.json.

Standard library only so it runs anywhere: python3 scripts/validate_skills.py
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"

PROVIDERS = {"azure", "aws", "gcp", "oci", "multi-cloud"}
# Pillar keys per provider; keep in sync with docs/frameworks.md
PILLARS = {
    "azure": {"reliability", "security", "cost-optimization", "operational-excellence", "performance-efficiency"},
    "aws": {"operational-excellence", "security", "reliability", "performance-efficiency", "cost-optimization", "sustainability"},
    "gcp": {"operational-excellence", "security", "reliability", "cost-optimization", "performance-optimization", "sustainability"},
    "oci": {"security-compliance", "reliability-resilience", "performance-cost", "operational-efficiency", "distributed-cloud"},
}
STATUSES = {"draft", "stable", "deprecated"}
REQUIRED_METADATA = ["provider", "framework", "pillars", "category", "last-reviewed", "version"]
REQUIRED_SECTIONS = [
    "When to use",
    "When not to use",
    "Inputs to gather",
    "Workflow",
    "Well-Architected alignment",
    "Guardrails",
    "Validation",
    "References",
]
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_LINES = 500
STALE_DAYS = 365


def parse_frontmatter(text):
    """Parse the simple two-level YAML frontmatter used by SKILL.md files."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    data, parent = {}, None
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indented = line.startswith((" ", "\t"))
        key, _, value = line.strip().partition(":")
        value = value.strip().strip('"').strip("'")
        if indented and parent is not None:
            data[parent][key] = value
        elif value:
            data[key], parent = value, None
        else:
            data[key], parent = {}, key
    return data, text[end + 4:]


def validate_skill(skill_dir, provider):
    errors, warnings = [], []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return ["missing SKILL.md"], warnings

    text = skill_md.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    if fm is None:
        return ["missing or malformed YAML frontmatter"], warnings

    name = fm.get("name", "")
    if name != skill_dir.name:
        errors.append(f"name '{name}' does not match folder '{skill_dir.name}'")
    if not NAME_RE.match(name) or len(name) > 64:
        errors.append("name must be lowercase kebab-case, max 64 chars")
    if not name.startswith(provider + "-"):
        errors.append(f"name must start with provider prefix '{provider}-'")

    desc = fm.get("description", "")
    if not desc:
        errors.append("missing description")
    elif len(desc) > 1024:
        errors.append(f"description is {len(desc)} chars (max 1024)")

    meta = fm.get("metadata")
    if not isinstance(meta, dict):
        errors.append("missing metadata block")
        meta = {}
    for key in REQUIRED_METADATA:
        if not meta.get(key):
            errors.append(f"missing metadata.{key}")
    if meta.get("provider") and meta["provider"] != provider:
        errors.append(f"metadata.provider '{meta['provider']}' does not match folder '{provider}'")
    allowed = PILLARS.get(provider)
    if allowed and meta.get("pillars"):
        unknown = {p.strip() for p in meta["pillars"].split(",")} - allowed
        if unknown:
            errors.append(f"unknown pillar key(s) for {provider}: {', '.join(sorted(unknown))}")
    if meta.get("status") and meta["status"] not in STATUSES:
        errors.append(f"metadata.status must be one of {', '.join(sorted(STATUSES))}")
    reviewed = meta.get("last-reviewed")
    if reviewed:
        try:
            age = (date.today() - date.fromisoformat(reviewed)).days
            if age > STALE_DAYS:
                warnings.append(f"last-reviewed is {age} days old; run prompts/refresh-skill.md")
        except ValueError:
            errors.append("metadata.last-reviewed must be YYYY-MM-DD")

    headings = {h.strip() for h in re.findall(r"^##\s+(.+)$", body, re.MULTILINE)}
    for section in REQUIRED_SECTIONS:
        if section not in headings:
            errors.append(f"missing section '## {section}'")

    lines = text.count("\n") + 1
    if lines > MAX_LINES:
        warnings.append(f"SKILL.md is {lines} lines; move detail into references/")
    if "<!-- VERIFY -->" in text:
        warnings.append("contains unresolved <!-- VERIFY --> markers")

    return errors, warnings


def marketplace_skills():
    if not MARKETPLACE.exists():
        return set()
    data = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    paths = set()
    for plugin in data.get("plugins", []):
        for p in plugin.get("skills", []):
            paths.add(Path(p).as_posix().lstrip("./"))
    return paths


def main():
    listed = marketplace_skills()
    failed = False
    count = 0
    for provider_dir in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        provider = provider_dir.name
        if provider not in PROVIDERS:
            print(f"✗ skills/{provider}: unknown provider (add it to PROVIDERS)")
            failed = True
            continue
        for skill_dir in sorted(p for p in provider_dir.iterdir() if p.is_dir()):
            count += 1
            rel = skill_dir.relative_to(ROOT).as_posix()
            errors, warnings = validate_skill(skill_dir, provider)
            if rel not in listed:
                errors.append("not listed in .claude-plugin/marketplace.json")
            status = "✗" if errors else "✓"
            print(f"{status} {rel}")
            for e in errors:
                print(f"    error: {e}")
            for w in warnings:
                print(f"    warning: {w}")
            failed = failed or bool(errors)
    print(f"\n{count} skill(s) checked.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
