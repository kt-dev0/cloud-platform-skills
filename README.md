# Cloud Platform Skills

Community-maintained **AI agent skills for cloud platform engineering**. Each skill teaches an AI agent (Claude Code, Claude.ai, or any tool that supports the open [Agent Skills](https://agentskills.io) format) how to do a real platform engineering task the way the cloud provider recommends: aligned to its Well-Architected Framework, secure by default, and backed by official documentation.

It covers **Azure**, **AWS**, **Google Cloud** and **Oracle Cloud (OCI)**, with more to come.

## Why this exists

General-purpose AI models know a lot about the cloud, but they often:
- suggest outdated services, SKUs or patterns
- skip security defaults (public endpoints, keys instead of managed identity)
- ignore cost, reliability and operational trade-offs
- produce infrastructure as code (IaC) that can't be repeated or that won't pass policy

A skill fixes this by giving the agent a tested, opinionated workflow, guardrails, and links to the authoritative sources.

## Catalog

Every cloud has the same core set of skills: **review → landing zone → network hub → identity → observability**. Azure adds policy and governance. All skills are `draft` until the community has tested them; see [CONTRIBUTING.md](CONTRIBUTING.md).

| Area | Azure | AWS | Google Cloud | Oracle Cloud (OCI) |
|---|---|---|---|---|
| Well-Architected review | [azure-waf-review](skills/azure/azure-waf-review/) | [aws-well-architected-review](skills/aws/aws-well-architected-review/) | [gcp-well-architected-review](skills/gcp/gcp-well-architected-review/) | [oci-well-architected-review](skills/oci/oci-well-architected-review/) |
| Landing zone / foundation | [azure-landing-zone](skills/azure/azure-landing-zone/) | [aws-landing-zone](skills/aws/aws-landing-zone/) | [gcp-landing-zone](skills/gcp/gcp-landing-zone/) | [oci-landing-zone](skills/oci/oci-landing-zone/) |
| Network hub | [azure-hub-spoke-network](skills/azure/azure-hub-spoke-network/) | [aws-network-hub](skills/aws/aws-network-hub/) | [gcp-shared-vpc-network](skills/gcp/gcp-shared-vpc-network/) | [oci-hub-spoke-network](skills/oci/oci-hub-spoke-network/) |
| Identity & least privilege | [azure-identity-rbac](skills/azure/azure-identity-rbac/) | [aws-iam-least-privilege](skills/aws/aws-iam-least-privilege/) | [gcp-iam-least-privilege](skills/gcp/gcp-iam-least-privilege/) | [oci-iam-policies](skills/oci/oci-iam-policies/) |
| Observability baseline | [azure-monitoring-baseline](skills/azure/azure-monitoring-baseline/) | [aws-observability-baseline](skills/aws/aws-observability-baseline/) | [gcp-observability-baseline](skills/gcp/gcp-observability-baseline/) | [oci-observability-baseline](skills/oci/oci-observability-baseline/) |
| Policy & governance | [azure-policy-governance](skills/azure/azure-policy-governance/) | — | — | — |

See [docs/roadmap.md](docs/roadmap.md) for planned skills. Requests are welcome; open a *Skill request* issue.

## Install

**Claude Code** (plugin marketplace):
```
/plugin marketplace add kt-dev0/cloud-platform-skills
/plugin install azure-platform-skills@cloud-platform-skills   # or aws-, gcp-, oci-platform-skills
```

**Any Agent Skills–compatible tool:** copy a skill folder (for example `skills/azure/azure-waf-review/`) into your tool's skills directory, such as `~/.claude/skills/` or `.claude/skills/` in a project.

**Claude.ai:** zip a skill folder and upload it under *Settings → Capabilities → Skills*.

## Repository layout

```
skills/
  <provider>/                 # azure, aws, gcp, oci, multi-cloud
    <provider>-<topic>/
      SKILL.md                # required: frontmatter + agent instructions
      references/             # deeper docs the agent loads on demand
      templates/              # IaC starters (Bicep/Terraform/CDK/...)
      scripts/                # deterministic helpers (validation, discovery)
      examples/               # sample prompts + expected outcomes
docs/frameworks.md            # pillar definitions for every provider's framework
prompts/                      # prompts for creating, reviewing and refreshing skills
templates/SKILL_TEMPLATE.md   # start every new skill from this
scripts/validate_skills.py    # CI linter for skill structure
```

## Principles every skill follows

1. **Useful to anyone.** No org-specific names, tenants or assumptions. Org choices become parameters or clarifying questions.
2. **The provider's own guidance first.** Each skill aligns to the Well-Architected Framework of its provider (see [docs/frameworks.md](docs/frameworks.md)) and cites official docs.
3. **Secure by default.** Least privilege, no secrets in code, private networking where practical, encryption and diagnostics on.
4. **Safe to run.** Plan or what-if before apply. Nothing destructive or costly happens without the user's explicit confirmation.
5. **Trade-offs made explicit.** Every recommendation says which pillar it favours and what it costs elsewhere.
6. **Kept current.** Every skill records a `last-reviewed` date and is re-checked regularly.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). The short version: copy `templates/SKILL_TEMPLATE.md`, use [prompts/create-skill.md](prompts/create-skill.md) to draft it, test it on a real scenario, and run `python3 scripts/validate_skills.py` before opening a PR.

## Disclaimer

This is a community project. It is not affiliated with or endorsed by Microsoft, Amazon, Google or Oracle. Always review generated plans and code before you deploy them.

## License

[MIT](LICENSE)
