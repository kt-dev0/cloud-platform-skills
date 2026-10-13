---
name: oci-landing-zone
description: Design and deploy an Oracle Cloud Infrastructure (OCI) landing zone using the official OCI Landing Zones (Core Landing Zone, CIS-aligned) — compartment hierarchy, identity domains and groups, compartment-scoped IAM policies, Cloud Guard, Security Zones, Vault, budgets, tagging, and centralized logging — deployed via Terraform or Resource Manager. Use when the user says "set up an OCI landing zone", "design OCI compartments", "CIS landing zone for Oracle Cloud", "organize our OCI tenancy", or "OCI tenancy best practices".
license: MIT
metadata:
  provider: oci
  framework: Well-Architected Framework for OCI
  pillars: security-compliance, reliability-resilience, performance-cost, operational-efficiency
  category: foundation
  status: draft
  last-reviewed: 2026-10-12
  version: 0.1.0
---

# OCI Landing Zone

Build a secure, CIS-aligned OCI tenancy foundation. Prefer the **official OCI Landing Zones** Terraform (Core Landing Zone, or the Operating Entities Landing Zone for multi-entity organizations) over a hand-built one.

## When to use

- A new OCI tenancy, or one where resources sit in the root compartment.
- Aligning a tenancy to the CIS OCI Foundations Benchmark.

## When not to use

- Detailed network design: use `oci-hub-spoke-network`.
- Detailed IAM policy authoring: use `oci-iam-policies`.

## Inputs to gather

| Input | Why it matters | Default |
|---|---|---|
| Greenfield or existing tenancy | Deploy alongside vs. migrate | Ask |
| Home region and other subscribed regions | Home region hosts IAM; multi-region DR | Ask (required) |
| Single org vs. multiple operating entities / business units | Core vs. Operating Entities Landing Zone | Single |
| Identity source (identity domain / federated IdP) | Groups and SSO | Federated |
| Environments | Compartment layout per environment | prod, nonprod |
| CIS profile level (1 or 2) | Strictness of controls | Level 1 |

## Workflow

1. **Assess (read-only).** `oci iam compartment list --compartment-id-in-subtree true --all`, `oci iam policy list`, `oci cloud-guard configuration get`. Flag resources in the root compartment and broad policies.
2. **Choose the implementation.** Use the **OCI Core Landing Zone** for most organizations, and the **Operating Entities Landing Zone** for multiple business units that need delegated administration. Deploy with Terraform or as an OCI Resource Manager stack.
3. **Compartment design** (adapt it to need):
   ```
   Root (tenancy) — no workloads
   └── <prefix>-top (enclosing compartment)
       ├── <prefix>-network       (VCNs, DRG, firewalls)
       ├── <prefix>-security      (Vault, Cloud Guard targets, logging, bastion)
       ├── <prefix>-app           (application tier)
       ├── <prefix>-database      (database tier)
       └── <prefix>-exainfra      (optional, Exadata)
   ```
   Repeat per environment, or add environment subcompartments, depending on the isolation needed.
4. **Identity.** Create groups per function (network admins, security admins, app admins, database admins, auditors, cost admins) in the identity domain, federated with the corporate IdP. Write compartment-scoped policies (details in `oci-iam-policies`). Enforce MFA and keep a break-glass admin.
5. **Security services.**
   - **Cloud Guard**: enabled at tenancy level, with reporting in the home region and detector and responder recipes (responders in notify mode first).
   - **Security Zones**: on sensitive compartments.
   - **Vault**: for customer-managed keys.
   - **Bastion service**: for administrative access, with no public SSH.
   - Vulnerability Scanning on compute.
6. **Governance.** Create tag namespaces and defined tags (cost center, environment, owner), tag defaults per compartment, budgets with alerts per compartment, and quotas to limit sprawl.
7. **Logging and notifications.** Set Audit retention as required. Create Events rules and Notifications topics for IAM, network and Cloud Guard changes, and use Connector Hub to archive logs (details in `oci-observability-baseline`).
8. **Generate the configuration** (the landing zone Terraform variables file or Resource Manager stack inputs) with placeholders for OCIDs. Run `terraform plan` (or the Resource Manager *Plan* job), present the plan, and **confirm before apply**.

## Well-Architected alignment

| Area | Recommendation | Rationale | Source |
|---|---|---|---|
| Security and Compliance | CIS-aligned landing zone; no root-compartment workloads; Cloud Guard + Security Zones; MFA; Vault | Preventive and detective guardrails from day one | https://github.com/oci-landing-zones |
| Reliability and Resilience | Plan multi-AD/fault-domain placement and DR region during foundation design; protect Terraform state | Foundations are hard to change later | https://docs.oracle.com/en/solutions/oci-best-practices/ |
| Performance and Cost Optimization | Budgets, quotas and cost-tracking tags per compartment | Cost ownership and sprawl control | https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/budgetsoverview.htm |
| Operational Efficiency | Landing zone as Terraform/Resource Manager; standardized compartments and tags | Repeatable, auditable tenancy changes | https://docs.oracle.com/en-us/iaas/Content/ResourceManager/home.htm |

**Trade-offs:** CIS Level 2 and Security Zones add strong protection but restrict some configurations, such as public buckets and some unencrypted options. Apply them to sensitive compartments first. Finer compartment separation improves least privilege but means more policies to maintain.

## Guardrails

- Never deploy workloads into the root compartment.
- Never apply landing zone changes to an existing tenancy without a reviewed plan and explicit confirmation.
- Moving or deleting compartments changes the policies that apply to them and can break access. Confirm first.
- Cloud Guard responders that change resources stay in notify-only mode until the user approves auto-remediation.

## Validation

- `terraform plan` or the Resource Manager plan job reviewed.
- `oci iam compartment list` matches the design.
- Cloud Guard reports targets for the enclosing compartment. A CIS compliance script run shows improved results.

## Common mistakes

- Using the tenancy admin user for daily operations.
- Tenancy-wide `manage all-resources` policies for non-admin groups.
- Skipping tag defaults, which makes cost allocation impossible later.

## Related skills

- `oci-iam-policies`, `oci-hub-spoke-network`, `oci-observability-baseline`, `oci-well-architected-review`

## References

- OCI Landing Zones: https://github.com/oci-landing-zones
- OCI Core Landing Zone: https://github.com/oci-landing-zones/terraform-oci-core-landingzone
- Well-Architected Framework for OCI: https://docs.oracle.com/en/solutions/oci-best-practices/
- Cloud Guard: https://docs.oracle.com/en-us/iaas/Content/cloud-guard/home.htm
- Security Zones: https://docs.oracle.com/en-us/iaas/Content/security-zone/home.htm
- OCI security best practices: https://docs.oracle.com/en-us/iaas/Content/Security/Concepts/security_guide.htm
