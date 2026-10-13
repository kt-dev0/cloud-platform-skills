---
name: <provider>-<topic>
description: <What this skill does AND when to use it. Include the phrases users actually type, e.g. "set up a hub-spoke network in Azure", "review my VNet design". Max 1024 chars.>
license: MIT
metadata:
  provider: <azure | aws | gcp | oci | multi-cloud>
  framework: <e.g. Azure Well-Architected Framework>
  pillars: <comma-separated keys from docs/frameworks.md, e.g. "security, reliability">
  category: <foundation | networking | identity | governance | compute | data | observability | cost | devops | assessment>
  status: draft            # draft -> stable once community-tested
  last-reviewed: <YYYY-MM-DD>
  version: 0.1.0
---

# <Skill title>

<One paragraph: the outcome this skill produces and for whom.>

## When to use

- <trigger scenario>
- <trigger scenario>

## When not to use

- <out-of-scope scenario>: use `<sibling-skill>` instead.

## Inputs to gather

Ask for these before you act. If the user doesn't know an answer, use the default and say that you did.

| Input | Why it matters | Default |
|---|---|---|
| Environment (dev/test/prod) | Drives SKU, redundancy and cost choices | dev |
| Region(s) | Availability zones, data residency, service availability | — (must ask) |
| Compliance requirements | Policy, encryption and logging requirements | none |
| Budget sensitivity | Cost-optimization vs. reliability trade-offs | balanced |

## Workflow

1. **Discover**: <how to inspect the current state or inputs, read-only>.
2. **Decide**: <decision points written as "If X, then Y; otherwise Z">.
3. **Generate**: <what to produce: IaC, plan, report>. Start from `templates/` and Azure Verified Modules (or the provider's equivalent).
4. **Validate**: run the checks in [Validation](#validation).
5. **Present**: summarise what will change, the cost impact, and the trade-offs. **Get explicit confirmation before any apply or destructive action.**

## Well-Architected alignment

| Pillar | Recommendation | Rationale | Source |
|---|---|---|---|
| Reliability | | | |
| Security | | | |
| Cost Optimization | | | |
| Operational Excellence | | | |
| Performance Efficiency | | | |

**Trade-offs:** <for example, zone redundancy improves reliability but raises cost; explain when each choice is right.>

## Guardrails

- Use managed identities or workload identity, never stored credentials. Keep secrets in a vault.
- Grant least-privilege RBAC at the narrowest scope.
- Disable public network access unless it is required and justified.
- Enable encryption at rest and in transit, and send diagnostic logs to central monitoring.
- Follow the provider's naming and tagging guidance; ask for the org's conventions.
- Never run destructive, irreversible or costly operations without explicit user confirmation.

## Validation

- <e.g. `az bicep build`, `az deployment group what-if`, `terraform validate && terraform plan`>
- <e.g. PSRule for Azure, Checkov, policy compliance checks>
- <how to confirm the outcome after deployment>

## Common mistakes

- <mistake> → <correct approach>

## Related skills

- `<sibling-skill>`: <relationship>

## References

- <Official doc title>: <URL>
