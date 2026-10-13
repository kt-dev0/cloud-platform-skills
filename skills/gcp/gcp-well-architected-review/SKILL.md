---
name: gcp-well-architected-review
description: Assess a Google Cloud workload, architecture design, or infrastructure-as-code (Terraform, Config Connector) against the Google Cloud Well-Architected Framework and produce a prioritized, evidence-based findings report, using read-only evidence from Security Command Center, Recommender (Active Assist), Cloud Asset Inventory and Policy Intelligence. Use when the user says "review my GCP architecture", "is this Google Cloud setup production-ready", "do a Well-Architected review on GCP", "what are the risks in this GCP project", or "review this Terraform for Google Cloud". Read-only.
license: MIT
metadata:
  provider: gcp
  framework: Google Cloud Well-Architected Framework
  pillars: operational-excellence, security, reliability, cost-optimization, performance-optimization, sustainability
  category: assessment
  status: draft
  last-reviewed: 2026-10-12
  version: 0.1.0
---

# Google Cloud Well-Architected Review

Run a structured, evidence-based review of a Google Cloud workload against the pillars of the Google Cloud Well-Architected Framework, with prioritized and sourced recommendations.

## When to use

- Reviewing a deployed workload (projects, folders or the whole organization).
- Reviewing Terraform or a design before go-live.

## When not to use

- Designing the organization foundation: use `gcp-landing-zone`.
- Making changes: this skill is **read-only**.

## Inputs to gather

| Input | Why it matters | Default |
|---|---|---|
| Scope: organization / folder / project IDs, IaC, or design | Evidence approach | Ask (required) |
| Workload criticality and SLOs / RTO / RPO | Reliability bar | Flag missing targets as a gap |
| Environment | Severity calibration | prod |
| Compliance needs (e.g. PCI DSS, HIPAA, Assured Workloads regimes) | Extra controls | None |
| Security Command Center tier | Which findings are available | Standard |

## Workflow

1. **Confirm access.** `gcloud auth list` and `gcloud config list`. The reviewer needs read-only roles such as `roles/viewer`, `roles/iam.securityReviewer` and `roles/cloudasset.viewer`, plus `roles/securitycenter.findingsViewer` if SCC is used. Never ask for service account keys.
2. **Gather evidence (read-only).** Use only `list`, `describe`, `get-iam-policy` and `search-*` commands.
   - Inventory: `gcloud asset search-all-resources --scope=<projects/ID|folders/ID|organizations/ID>`
   - IAM: `gcloud asset search-all-iam-policies --scope=...`. Flag basic roles (Owner, Editor) and external members.
   - **Security Command Center** findings (misconfigurations, vulnerabilities, threats).
   - **Recommender**: IAM role recommendations, idle VMs and disks, VM right-sizing, committed use discount recommendations.
   - Org policies in effect: `gcloud org-policies list --project=<ID>` (or `--folder`/`--organization`).
   - IaC: run `terraform validate`, plus Checkov or `gcloud beta terraform vet` if available.
3. **Assess each pillar** against the framework's principles and recommendations. See [references/pillar-checks.md](references/pillar-checks.md). Mark missing evidence as **Unable to verify**.
4. **Rate findings** High / Medium / Low, calibrated to the environment.
5. **State the trade-offs** for each recommendation.
6. **Write the report**: a summary by pillar, the top 5 actions, the findings (pillar, evidence, severity, recommendation, trade-off, source), the unable-to-verify items, and next steps.

## Well-Architected alignment

| Pillar | What this skill checks (summary) | Source |
|---|---|---|
| Operational Excellence | IaC, CI/CD, Cloud Monitoring/Logging coverage, SLOs, incident process | https://cloud.google.com/architecture/framework/operational-excellence |
| Security, Privacy and Compliance | Resource hierarchy + org policies, IAM least privilege, no SA keys, VPC Service Controls where needed, CMEK needs, SCC findings | https://cloud.google.com/architecture/framework/security |
| Reliability | Regional/multi-zonal resources, SLOs, backups and tested restore, quotas, DR vs. RTO/RPO | https://cloud.google.com/architecture/framework/reliability |
| Cost Optimization | Labels, budgets, CUDs, idle resources, right-sizing, storage classes and lifecycle | https://cloud.google.com/architecture/framework/cost-optimization |
| Performance Optimization | Autoscaling, machine families, caching/CDN, load testing | https://cloud.google.com/architecture/framework/performance-optimization |
| Sustainability | Region carbon data, utilization, managed services, data lifecycle | https://cloud.google.com/architecture/framework/sustainability |

**Trade-offs:** Match recommendations to criticality. Multi-region raises cost; low-carbon regions may add latency. Make these choices explicit for the user.

## Guardrails

- **Read-only.** No `create`, `update`, `delete`, `set-iam-policy` or `add-iam-policy-binding`.
- Redact project numbers and member emails from the report unless the user asks otherwise. Report any exposed key material as High.
- Stay within the given scope.

## Validation

- Every pillar appears in the report.
- Each High finding has been re-checked against the raw evidence.

## Common mistakes

- Reviewing a single project and missing the policies inherited from folders or the organization.
- Treating the SCC score as the whole review.

## Related skills

- `gcp-landing-zone`, `gcp-iam-least-privilege`, `gcp-shared-vpc-network`, `gcp-observability-baseline`

## References

- Google Cloud Well-Architected Framework: https://cloud.google.com/architecture/framework
- Security Command Center: https://cloud.google.com/security-command-center/docs/security-command-center-overview
- Recommender: https://cloud.google.com/recommender/docs/overview
- Cloud Asset Inventory: https://cloud.google.com/asset-inventory/docs/overview
