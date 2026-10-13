---
name: aws-well-architected-review
description: Assess an AWS workload, architecture design, or infrastructure-as-code (CloudFormation, CDK, Terraform) against the AWS Well-Architected Framework's six pillars and produce a prioritized, evidence-based findings report, using read-only evidence from AWS Config, Security Hub, Trusted Advisor, IAM Access Analyzer and Compute Optimizer. Use when the user says "review my AWS architecture", "do a Well-Architected review", "is this CloudFormation production-ready", "what are the risks in this AWS account", or "prepare for a Well-Architected Tool review". Read-only.
license: MIT
metadata:
  provider: aws
  framework: AWS Well-Architected Framework
  pillars: operational-excellence, security, reliability, performance-efficiency, cost-optimization, sustainability
  category: assessment
  status: draft
  last-reviewed: 2026-10-12
  version: 0.1.0
---

# AWS Well-Architected Review

Run a structured, evidence-based review of an AWS workload against the six pillars of the AWS Well-Architected Framework. Each finding is tied to a framework best practice (for example `SEC02-BP02`), with evidence, severity, a fix and the trade-off.

## When to use

- Reviewing a deployed workload (one or more accounts and regions).
- Reviewing IaC or a design before go-live.
- Preparing input for a formal review in the AWS Well-Architected Tool.

## When not to use

- Designing a multi-account foundation: use `aws-landing-zone`.
- Making changes: this skill is **read-only**.

## Inputs to gather

| Input | Why it matters | Default |
|---|---|---|
| Scope: accounts, regions, IaC, or design description | Evidence approach | Ask (required) |
| Workload criticality and RTO/RPO | Reliability bar | Business-important; targets flagged as a gap if missing |
| Environment | Severity calibration | prod |
| Compliance (PCI DSS, HIPAA, SOC 2…) | Extra controls | None |
| Lenses to apply (Serverless, SaaS, Container Build, etc.) | Specialized questions | None |

## Workflow

1. **Confirm access.** `aws sts get-caller-identity`. The role should have read-only permissions (for example the AWS-managed `ReadOnlyAccess` or `SecurityAudit` + `ViewOnlyAccess`). Never ask for access keys in chat.
2. **Gather evidence (read-only).** Use only `describe-*`, `list-*` and `get-*` calls. Pull from:
   - **Security Hub** findings for the *AWS Foundational Security Best Practices* standard (`aws securityhub get-findings`).
   - **AWS Config** non-compliant rules (`aws configservice describe-compliance-by-config-rule`).
   - **Trusted Advisor** checks (needs Business support or higher for the full set).
   - **IAM Access Analyzer** external and unused-access findings.
   - **Compute Optimizer** right-sizing recommendations.
   - **Cost Explorer** for cost trends and anomalies.
   - For IaC: run `cfn-lint`, `cfn_nag` or Checkov if available, and inspect the resource properties.
3. **Assess each pillar** against the framework's questions and best practices, plus any selected lenses. See [references/pillar-checks.md](references/pillar-checks.md). Mark missing evidence as **Unable to verify**.
4. **Rate risk** using Well-Architected terminology: **High risk issue (HRI)**, **Medium risk issue (MRI)**, or no issue. Calibrate for non-prod and say so.
5. **State the trade-offs** for each recommendation (for example multi-region improves reliability but increases cost and the sustainability footprint).
6. **Write the report**: a summary by pillar, the top 5 actions, the findings (pillar, best practice ID, risk, evidence, recommendation, trade-off, source), the unable-to-verify items, and next steps. Suggest recording the review in the AWS Well-Architected Tool and creating a milestone.

## Well-Architected alignment

| Pillar | What this skill checks (summary) | Source |
|---|---|---|
| Operational Excellence | IaC and CI/CD, observability, runbooks, deployment safety, operational readiness reviews | https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html |
| Security | Identity (no long-term keys, Identity Center), detective controls (CloudTrail, GuardDuty, Security Hub), data protection (KMS, TLS), network exposure | https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html |
| Reliability | Multi-AZ, quotas, backups with tested restore, scaling, failure handling, DR strategy vs. RTO/RPO | https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html |
| Performance Efficiency | Right resource types (e.g. Graviton), scaling, caching, performance testing | https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/welcome.html |
| Cost Optimization | Tagging/cost allocation, budgets, right-sizing, Savings Plans/RIs, idle resources, storage lifecycle | https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html |
| Sustainability | Utilization, managed services, efficient instance types, data lifecycle, region choice | https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sustainability-pillar.html |

**Trade-offs:** Match recommendations to criticality. A single-AZ dev environment is a valid choice. Present the cost and sustainability impact of reliability improvements together.

## Guardrails

- **Read-only.** No `create-*`, `put-*`, `update-*`, `delete-*`, `attach-*` or `modify-*` calls.
- Redact account IDs, ARNs with account numbers, and any secrets from the report unless the user asks otherwise. Report exposed secrets as HRIs.
- Respect scope: only the accounts and regions the user named.
- Every finding needs evidence and a source link.

## Validation

- Every pillar appears in the report.
- Each HRI has been re-checked against the raw evidence.
- Best practice IDs match the current framework version.

## Common mistakes

- Treating Trusted Advisor or Security Hub scores as the whole review. Process-level questions (runbooks, game days) need interviews or documents.
- Checking only `us-east-1`. Enumerate the regions in use (`aws ec2 describe-regions` + Cost Explorer by region).
- Ignoring global services (IAM, CloudFront, Route 53).

## Related skills

- `aws-landing-zone`, `aws-iam-least-privilege`, `aws-network-hub`, `aws-observability-baseline`

## References

- AWS Well-Architected Framework: https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html
- AWS Well-Architected Tool: https://docs.aws.amazon.com/wellarchitected/latest/userguide/intro.html
- Security Hub Foundational Security Best Practices: https://docs.aws.amazon.com/securityhub/latest/userguide/fsbp-standard.html
- Trusted Advisor: https://docs.aws.amazon.com/awssupport/latest/user/trusted-advisor.html
- IAM Access Analyzer: https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html
- Compute Optimizer: https://docs.aws.amazon.com/compute-optimizer/latest/ug/what-is-compute-optimizer.html
