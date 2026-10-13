---
name: gcp-landing-zone
description: Design and deploy a Google Cloud landing zone — organization resource hierarchy (folders, projects), organization policy constraints, Cloud Identity groups, billing and budgets, centralized logging, and project vending — following Google's enterprise foundations blueprint (terraform-example-foundation) or Cloud Foundation Fabric FAST. Use when the user says "set up a GCP landing zone", "design our Google Cloud folder structure", "which org policies should we enable", "enterprise foundations blueprint", "project factory", or "how to organize GCP projects".
license: MIT
metadata:
  provider: gcp
  framework: Google Cloud Well-Architected Framework
  pillars: operational-excellence, security, reliability, cost-optimization, performance-optimization, sustainability
  category: foundation
  status: draft
  last-reviewed: 2026-10-12
  version: 0.1.0
---

# Google Cloud Landing Zone

Establish a secure, scalable Google Cloud foundation using Google's landing zone design guidance. Prefer a **maintained, Google-published Terraform foundation** (the enterprise foundations blueprint or Fabric FAST) over a hand-built one.

## When to use

- A new Google Cloud organization, or one where projects grew without structure.
- Choosing the resource hierarchy and the org policy baseline.
- Setting up project vending.

## When not to use

- Network design in depth: use `gcp-shared-vpc-network`.
- IAM role design: use `gcp-iam-least-privilege`.

## Inputs to gather

| Input | Why it matters | Default |
|---|---|---|
| Organization exists (Cloud Identity / Workspace domain)? | Prerequisite for folders and org policies | Ask |
| Identity source (Cloud Identity, or federated from Entra ID / Okta) | Groups and SSO | Federated |
| Regions and data residency | `gcp.resourceLocations` constraint | Ask (required) |
| Environments | Folder structure | production, nonproduction, development |
| Foundation tooling: enterprise foundations blueprint vs. Fabric FAST | Repo structure and pipeline | Enterprise foundations blueprint |
| Compliance regime (Assured Workloads needed?) | Folder-level controls | None |

## Workflow

1. **Assess (read-only).** `gcloud organizations list`, `gcloud resource-manager folders list --organization=<ID>`, `gcloud projects list`, `gcloud org-policies list --organization=<ID>`. Flag projects outside the organization and basic-role grants at org level.
2. **Set up the prerequisites (done by the user, with super admin or org admin).** Create the admin groups (for example `gcp-organization-admins`, `gcp-billing-admins`, `gcp-security-admins`, `gcp-network-admins`), keep super admin accounts separate and MFA-protected, and use them only for break-glass.
3. **Choose the foundation.**
   - The **enterprise foundations blueprint** (`terraform-example-foundation`) is staged (bootstrap → org → environments → networks → projects), well documented, and fits most organizations.
   - **Cloud Foundation Fabric FAST** is more modular and suits teams comfortable with composing Terraform.
4. **Design the hierarchy** (adapt it to need):
   ```
   Organization
   ├── fldr-bootstrap        (seed/CI-CD projects for the foundation)
   ├── fldr-common           (logging, monitoring, shared networking hosts, security tooling)
   ├── fldr-production
   ├── fldr-nonproduction
   ├── fldr-development
   └── fldr-sandbox          (optional, restricted, budget-capped)
   ```
   Use folders for policy inheritance by **environment and control need**. Use one project per workload per environment.
5. **Org policy baseline.** Apply at the organization and override at folders only with justification. Typical constraints:
   - `iam.disableServiceAccountKeyCreation`
   - `iam.allowedPolicyMemberDomains` (domain restricted sharing)
   - `iam.automaticIamGrantsForDefaultServiceAccounts` (disable)
   - `compute.skipDefaultNetworkCreation`
   - `compute.vmExternalIpAccess` (deny by default)
   - `compute.requireOsLogin`
   - `storage.uniformBucketLevelAccess`
   - `storage.publicAccessPrevention`
   - `sql.restrictPublicIp`
   - `gcp.resourceLocations` (if residency applies)

   Use dry-run mode for org policies where supported, and run Policy Simulator before enforcing on existing estates.
6. **Central logging.** Create an organization-level aggregated log sink to a central log bucket (and/or BigQuery). Details are in `gcp-observability-baseline`.
7. **Billing.** Link the billing account, set budgets with alerts per project or folder, and turn on billing export to BigQuery.
8. **Project vending.** Use a project factory that creates projects with labels, budget, Shared VPC attachment, required APIs only, and group-based IAM.
9. **Generate the Terraform inputs** with placeholders for the org ID, billing account and domain. Run `terraform plan`, present the plan and the cost drivers, and **confirm before applying**.

## Well-Architected alignment

| Pillar | Recommendation | Rationale | Source |
|---|---|---|---|
| Operational Excellence | Foundation as Terraform with staged pipelines; project factory | Repeatable, reviewable foundation changes | https://cloud.google.com/architecture/security-foundations |
| Security, Privacy and Compliance | Org policy baseline; group-based admin roles; separate super admins; central audit logs | Preventive guardrails inherited by every project | https://cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints |
| Reliability | Project-per-workload isolates quotas and failures; foundation state stored safely in seed project | Limits blast radius | https://cloud.google.com/architecture/landing-zones/decide-resource-hierarchy |
| Cost Optimization | Budgets, labels and billing export from day one | Clear cost ownership | https://cloud.google.com/billing/docs/how-to/budgets |
| Performance Optimization | Region selection near users within residency limits; quota planning per project | Latency and scale | https://cloud.google.com/architecture/landing-zones |
| Sustainability | Consider low-carbon regions in `gcp.resourceLocations` choices; sandbox cleanup | Lower footprint, fewer idle resources | https://cloud.google.com/sustainability/region-carbon |

**Trade-offs:** Strict org policies (no external IPs, no SA keys) break some third-party tools. Use targeted, documented folder or project exceptions rather than weakening the organization-wide baseline. The full blueprint is comprehensive but heavy for very small organizations, so a reduced scope is acceptable.

## Guardrails

- Never apply org policies at organization level on an existing estate without dry-run or simulation and explicit confirmation.
- Never grant `roles/owner` or `roles/resourcemanager.organizationAdmin` to individual users permanently. Use groups and keep super admins for break-glass.
- Don't delete or move projects without confirmation. Moving projects changes the policies they inherit.
- Store Terraform state in a protected bucket in the seed project, with versioning on.

## Validation

- `terraform plan` reviewed for each stage.
- `gcloud resource-manager folders list` matches the design.
- `gcloud org-policies describe <constraint> --organization=<ID>` shows the expected enforcement.
- A test project created by the factory has the expected labels, budget, IAM and network attachment.

## Common mistakes

- Projects created outside the organization (no hierarchy, no policies).
- Default VPCs left in projects.
- Granting Editor broadly because "it's easier".

## Related skills

- `gcp-shared-vpc-network`, `gcp-iam-least-privilege`, `gcp-observability-baseline`, `gcp-well-architected-review`

## References

- Landing zone design in Google Cloud: https://cloud.google.com/architecture/landing-zones
- Enterprise foundations blueprint: https://cloud.google.com/architecture/security-foundations
- terraform-example-foundation: https://github.com/terraform-google-modules/terraform-example-foundation
- Cloud Foundation Fabric FAST: https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/fast
- Decide a resource hierarchy: https://cloud.google.com/architecture/landing-zones/decide-resource-hierarchy
- Organization policy constraints: https://cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints
