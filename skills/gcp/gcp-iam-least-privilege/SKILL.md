---
name: gcp-iam-least-privilege
description: Design and review least-privilege access in Google Cloud — group-based IAM with predefined roles instead of basic roles, dedicated service accounts per workload, no service account keys (Workload Identity Federation for CI/CD and external workloads, Workload Identity for GKE), IAM Conditions, deny policies, Privileged Access Manager for just-in-time elevation, and IAM recommender cleanup. Use when the user says "remove Editor role", "GitHub Actions to GCP without keys", "set up Workload Identity Federation", "review GCP IAM", "least privilege service account", or "just-in-time access in Google Cloud".
license: MIT
metadata:
  provider: gcp
  framework: Google Cloud Well-Architected Framework
  pillars: operational-excellence, security, reliability, cost-optimization, performance-optimization, sustainability
  category: identity
  status: draft
  last-reviewed: 2026-10-12
  version: 0.1.0
---

# Google Cloud IAM Least Privilege

Grant access to groups through predefined roles at the narrowest resource level, run workloads as dedicated service accounts without keys, and shrink permissions continuously using recommender data.

## When to use

- Designing IAM for a new foundation or workload.
- Eliminating service account keys and basic roles.
- Reviewing IAM after an audit or SCC finding.

## When not to use

- Org policy baseline: use `gcp-landing-zone`.

## Inputs to gather

| Input | Why it matters | Default |
|---|---|---|
| Personas and the resources they need | Role and scope mapping | Ask |
| Identity source (Cloud Identity / federated IdP) | Group management | Federated |
| Workload runtimes (Compute Engine, Cloud Run, GKE, Cloud Functions, external) | Identity delivery mechanism | Ask |
| CI/CD platform | Workload Identity Federation provider config | GitHub Actions |
| Existing SA keys to migrate? | Cleanup scope | Ask |

## Workflow

1. **Inventory (read-only).**
   - `gcloud asset search-all-iam-policies --scope=organizations/<ID>`. Flag `roles/owner` and `roles/editor`, `allUsers` / `allAuthenticatedUsers`, individual user bindings, and external domains.
   - `gcloud iam service-accounts keys list --iam-account=<sa> --managed-by=user` for each service account, to find user-managed keys.
   - IAM recommender (role recommendations) and Policy Analyzer for who has access to what.
2. **Humans.** Bind Google groups to **predefined roles** at the lowest practical level (project, folder or resource). Avoid basic roles in production. Use custom roles only when predefined roles are too broad.
3. **Just-in-time elevation.** Use **Privileged Access Manager (PAM)** entitlements for admin roles, with justification, approval and a time limit, instead of standing grants.
4. **Workloads.**
   - Use one **dedicated service account per workload**. Don't use the default compute service account; disable automatic Editor grants through org policy.
   - GKE: **Workload Identity Federation for GKE**.
   - CI/CD and external clouds: **Workload Identity Federation** with attribute conditions (for example restrict `assertion.repository` and `assertion.ref`). **No SA keys.**
   - Use service account impersonation (`roles/iam.serviceAccountTokenCreator`, granted narrowly) instead of distributing keys.
5. **Conditions and deny.** Use **IAM Conditions** for time-bound access or resource-name or tag-based scoping. Use **IAM deny policies** to block high-risk permissions organization-wide (for example keep SA key creation denied for everyone except a break-glass group).
6. **Cleanup.** Apply IAM recommender suggestions **after confirmation**. Delete user-managed keys after migration, and disable them first to detect breakage.
7. **Output** the persona matrix (persona → group → role → scope → PAM yes/no), the service account inventory, the Terraform for bindings, and the key migration plan.

## Well-Architected alignment

| Pillar | Recommendation | Rationale | Source |
|---|---|---|---|
| Operational Excellence | IAM as Terraform; recommender-driven reviews; PAM audit trail | Auditable and repeatable access management | https://cloud.google.com/policy-intelligence/docs/role-recommendations-overview |
| Security, Privacy and Compliance | Groups + predefined roles; no basic roles; no SA keys; WIF; deny policies | Reduces credential theft and privilege abuse | https://cloud.google.com/iam/docs/using-iam-securely |
| Reliability | Keyless auth avoids key expiry/rotation incidents; break-glass group documented | Access continuity | https://cloud.google.com/iam/docs/best-practices-service-accounts |
| Cost Optimization | IAM itself is free; use PAM instead of third-party JIT tooling where sufficient | Avoid redundant tooling spend | https://cloud.google.com/iam/docs/pam-overview |
| Performance Optimization | Bind at folder level for groups shared across many projects to stay within policy size limits | IAM policy size and management scale | https://cloud.google.com/iam/quotas |
| Sustainability | Remove unused service accounts and bindings | Less sprawl to operate | https://cloud.google.com/architecture/framework/sustainability |

**Trade-offs:** Fine-grained custom roles maximize least privilege but need maintenance when Google adds permissions. Prefer predefined roles at a narrower scope. PAM approvals add incident friction; use pre-approved entitlements for on-call.

## Guardrails

- Never request, output or store service account keys. If you find keys in code, report them as critical and recommend disabling and rotating them immediately.
- Never remove bindings, disable or delete service accounts or keys without explicit confirmation and an impact list.
- Never grant `roles/iam.serviceAccountTokenCreator` or `roles/iam.serviceAccountUser` at project level when the service-account level is enough.
- WIF providers must have an attribute condition. Never trust an entire identity provider issuer.

## Validation

- `gcloud projects get-iam-policy <ID>` shows no basic roles for humans in prod.
- Policy Troubleshooter (`gcloud policy-intelligence troubleshoot-policy iam`) confirms the intended allow or deny.
- Pipeline authenticates with `google-github-actions/auth` using `workload_identity_provider` and no key file.

## Common mistakes

- Workloads running as the default compute service account with Editor.
- Granting `serviceAccountUser` project-wide, which lets the grantee act as every service account in the project.
- WIF provider without an attribute condition.

## Related skills

- `gcp-landing-zone`, `gcp-well-architected-review`, `gcp-observability-baseline`

## References

- Use IAM securely: https://cloud.google.com/iam/docs/using-iam-securely
- Best practices for service accounts: https://cloud.google.com/iam/docs/best-practices-service-accounts
- Workload Identity Federation: https://cloud.google.com/iam/docs/workload-identity-federation
- Workload Identity Federation for GKE: https://cloud.google.com/kubernetes-engine/docs/concepts/workload-identity
- Privileged Access Manager: https://cloud.google.com/iam/docs/pam-overview
- Deny policies: https://cloud.google.com/iam/docs/deny-overview
- Role recommendations: https://cloud.google.com/policy-intelligence/docs/role-recommendations-overview
