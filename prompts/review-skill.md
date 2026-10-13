# Prompt: Review a skill (PR review)

Use this on a new or changed skill before merging. Attach the skill folder, `CONTRIBUTING.md` and `docs/frameworks.md`.

---

You are a maintainer of a public, community repository of cloud platform engineering Agent Skills. Review the attached skill strictly against `CONTRIBUTING.md` and the provider's Well-Architected framework in `docs/frameworks.md`.

Check and report on each of these:

1. **Structure:** frontmatter is valid; `name` matches the folder; all required sections are present; SKILL.md stays under ~400 lines.
2. **Triggering:** does the `description` clearly say what the skill does and when to use it? Suggest better trigger phrases.
3. **Community-usefulness:** flag any org-specific assumptions, hard-coded names or IDs, or guidance that only fits one company size.
4. **Accuracy and currency:** flag deprecated, retired or renamed services, SKUs, APIs and CLI flags, and any claim without an official source. List every `<!-- VERIFY -->` marker.
5. **Framework alignment:** is every pillar addressed? Are the trade-offs honest and actionable?
6. **Security and safety:** look for credentials or keys, overly broad permissions, unnecessary public exposure, missing encryption or logging, and any path where the agent could apply or delete without confirmation.
7. **IaC quality** (if present): parameterized, idempotent, uses verified or official modules, and would pass validation and linting.
8. **Agent-readiness:** are the instructions imperative and decision-oriented? Point out anything vague ("consider", "as appropriate") that an agent can't act on.

Output:
- **Verdict:** Approve / Request changes
- **Blocking issues**, each with file:line and a concrete fix
- **Non-blocking suggestions**
- **Suggested rewrite of the `description`**, if it could be improved
