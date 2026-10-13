---
name: aws-iam-least-privilege
description: Design and review least-privilege access on AWS — IAM Identity Center permission sets for humans, IAM roles for workloads (instance profiles, Lambda execution roles, EKS Pod Identity/IRSA), OIDC federation for CI/CD with no long-term keys, permissions boundaries, SCP/RCP guardrails, and IAM Access Analyzer for policy validation and unused-access cleanup. Use when the user says "write a least-privilege IAM policy", "remove AWS access keys", "GitHub Actions OIDC to AWS", "set up IAM Identity Center permission sets", "review our IAM users", or "find unused AWS permissions".
license: MIT
metadata:
  provider: aws
  framework: AWS Well-Architected Framework
  pillars: operational-excellence, security, reliability, performance-efficiency, cost-optimization, sustainability
  category: identity
  status: draft
  last-reviewed: 2026-10-12
  version: 0.1.0
---

# AWS IAM Least Privilege

Give humans temporary, federated, group-based access, give workloads roles instead of keys, and continuously shrink permissions toward what's actually used.

## When to use

- Designing permission sets and roles for a new organization or workload.
- Eliminating IAM users and long-term access keys.
- Writing or reviewing IAM policies.

## When not to use

- Organization-wide SCP strategy: use `aws-landing-zone` (this skill covers SCPs only as they relate to permissions).

## Inputs to gather

| Input | Why it matters | Default |
|---|---|---|
| Personas and the accounts they need | Permission set → account assignments | Ask |
| Identity source (external IdP / Identity Center directory) | SCIM provisioning, MFA source | External IdP |
| Workload compute types (EC2, Lambda, ECS, EKS) | Role delivery mechanism | Ask |
| CI/CD platform | OIDC provider configuration | GitHub Actions |
| Existing IAM users / keys to migrate? | Cleanup scope | Ask |

## Workflow

1. **Inventory (read-only).**
   - `aws iam generate-credential-report` then `get-credential-report`, to find IAM users, key age, key last-used date and MFA status.
   - IAM Access Analyzer: external-access findings and **unused access** findings (unused roles, keys, permissions).
   - `aws iam list-roles`. Flag roles with `AdministratorAccess` or `*:*`, and trust policies that allow broad principals.
2. **Humans → IAM Identity Center.**
   - Use permission sets per persona (for example `PlatformAdmin`, `Developer`, `ReadOnly`, `SecurityAudit`), assigned to **IdP groups**, not users.
   - Use AWS managed job-function policies as a starting point, and add inline or customer-managed policies to narrow them.
   - Set session duration as short as is practical. Keep privileged sets for break-glass or approval-based temporary elevation.
3. **Workloads → roles, never keys.**
   - EC2: instance profiles. Lambda: execution roles. ECS: task roles.
   - EKS: **EKS Pod Identity** (or IRSA).
   - CI/CD: an **OIDC identity provider** with trust conditions on `sub` scoped to the repo, branch or environment. Never use wildcard repos.
   - On-prem: IAM Roles Anywhere instead of access keys.
4. **Write policies with least privilege.**
   - Grant specific actions and resource ARNs, and use conditions (`aws:PrincipalOrgID`, `aws:SourceArn`, `aws:SourceAccount`, `aws:RequestedRegion`, tags for ABAC).
   - Generate a starting policy from CloudTrail activity using Access Analyzer **policy generation**, then refine it.
   - Validate every policy with `aws accessanalyzer validate-policy` and fix all security warnings.
5. **Delegation safety.** When teams create their own roles, require a **permissions boundary** and enforce it with an SCP condition.
6. **Root user.** Turn on MFA, remove access keys, and use centralized root access management for member accounts where it's available.
7. **Continuous cleanup.** Review Access Analyzer unused-access findings regularly, and remove unused roles, keys and permissions **after confirmation**.
8. **Output** the persona matrix (persona → group → permission set → accounts), the policies and roles as IaC, and a migration plan for existing keys.

## Well-Architected alignment

| Pillar | Recommendation | Rationale | Source |
|---|---|---|---|
| Operational Excellence | IAM as code; policy validation in CI; scheduled access reviews | Predictable, reviewable permission changes | https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html |
| Security | Federation for humans, roles for workloads, no long-term keys, least privilege, boundaries | Credentials are the top breach vector | https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html |
| Reliability | OIDC/roles avoid key rotation outages; break-glass access documented | Access continuity during incidents | https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/sec_permissions_emergency_process.html |
| Performance Efficiency | ABAC (tag-based) policies scale without per-resource policy edits | Fewer policies to manage as estate grows | https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_attribute-based-access-control.html |
| Cost Optimization | IAM is free, but Access Analyzer unused-access analysis is priced per analyzed IAM role/user—scope it intentionally | Avoid surprise analyzer charges | https://aws.amazon.com/iam/access-analyzer/pricing/ |
| Sustainability | Remove unused roles/users to reduce operational sprawl | Smaller, simpler footprint | https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sustainability-pillar.html |

**Trade-offs:** Very tight policies can break legitimate future actions. Use policy generation from real activity plus a feedback loop instead of guessing. Short sessions improve security but annoy users, so tune them per persona.

## Guardrails

- Never ask for, print or store access keys or secrets. If you find keys in code, report them as critical and recommend immediate rotation.
- Never delete users, keys or roles, or detach policies, without explicit confirmation and an impact list.
- Never produce `"Action": "*"` with `"Resource": "*"` except for documented break-glass roles.
- OIDC trust policies must restrict `sub` (and `aud`). Never allow any repository.

## Validation

- `aws accessanalyzer validate-policy --policy-type IDENTITY_POLICY --policy-document file://policy.json` returns no security warnings.
- `aws iam simulate-principal-policy` confirms intended allows and denies.
- Pipeline runs authenticate with `aws-actions/configure-aws-credentials` using `role-to-assume` and no stored secrets.
- Credential report shows no active keys older than policy allows.

## Common mistakes

- Wildcard `sub` claims in GitHub OIDC trust policies.
- Giving CI/CD `AdministratorAccess` "temporarily".
- Using IAM users for humans in member accounts alongside Identity Center.

## Related skills

- `aws-landing-zone`, `aws-well-architected-review`, `aws-observability-baseline`

## References

- IAM security best practices: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html
- IAM Identity Center: https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html
- IAM Access Analyzer: https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html
- Permissions boundaries: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html
- EKS Pod Identity: https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html
- GitHub Actions OIDC with AWS: https://docs.github.com/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services
