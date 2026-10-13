---
name: azure-landing-zone
description: Design and deploy an Azure landing zone following the Cloud Adoption Framework (CAF) — management group hierarchy, platform subscriptions (management, connectivity, identity), policy baseline, and subscription vending — using the official Azure Landing Zones accelerator with Bicep or Terraform (Azure Verified Modules). Use when the user says "set up an Azure landing zone", "design our management groups", "enterprise-scale Azure foundation", "how should we organize Azure subscriptions", or "ALZ accelerator".
license: MIT
metadata:
  provider: azure
  framework: Azure Well-Architected Framework
  pillars: reliability, security, cost-optimization, operational-excellence, performance-efficiency
  category: foundation
  status: draft
  last-reviewed: 2026-10-12
  version: 0.1.0
---

# Azure Landing Zone

Guide the user to a CAF-aligned Azure landing zone: a scalable platform foundation that application teams deploy into. Prefer the **official Azure Landing Zones (ALZ) implementation** over hand-built foundations. This skill decides the design, generates configuration for the accelerator, and runs a preview before anything is deployed.

## When to use

- A new Azure estate, or an existing one without a management group hierarchy or policy baseline.
- Restructuring subscriptions and management groups to align with CAF.
- Choosing between ALZ Bicep, ALZ Terraform, or the portal accelerator.

## When not to use

- Designing hub-and-spoke or Virtual WAN networking in depth: use `azure-hub-spoke-network`.
- Authoring custom policies or exemptions: use `azure-policy-governance`.
- Reviewing an existing workload: use `azure-waf-review`.

## Inputs to gather

| Input | Why it matters | Default |
|---|---|---|
| Org size and number of expected workloads | Determines whether full ALZ or a simplified start is appropriate | Ask |
| IaC preference (Bicep / Terraform) and CI/CD platform (GitHub / Azure DevOps) | Selects the accelerator flavour | Ask |
| Primary and secondary regions | Platform resource placement, data residency | Ask (required) |
| Network topology (hub-and-spoke / Virtual WAN / none yet) | Connectivity subscription design | Hub-and-spoke |
| Hybrid connectivity (VPN / ExpressRoute / none) | Gateways and IP planning | None |
| Compliance requirements | Additional policy initiatives (regulatory compliance built-ins) | None |
| Existing tenant state (greenfield / brownfield) | Brownfield requires migration planning | Ask |
| Management group prefix | Naming of the intermediate root | `alz` |

## Workflow

1. **Assess current state (read-only).** If brownfield, list management groups, subscriptions and policy assignments (`az account management-group list`, `az account list`, `az policy assignment list`). Flag workloads deployed in the tenant root or with Owner at root.
2. **Choose the implementation path.**
   - If the user has a CI/CD platform and IaC skills → recommend the **ALZ IaC accelerator** (Bicep or Terraform), which bootstraps the pipeline, identities and state.
   - If the organization is small, has fewer than ~5 workloads, and has no platform team → recommend starting with the ALZ design but a reduced scope (management + one landing zone MG). Explain that it can grow into the full design.
   - Use the portal accelerator only for evaluation or demo tenants.
3. **Design the management group hierarchy** using the CAF reference unless there is a strong reason to deviate:
   ```
   Tenant Root Group
   └── <prefix> (intermediate root)
       ├── Platform
       │   ├── Management     (Log Analytics, automation)
       │   ├── Connectivity   (hub networking, DNS, firewall)
       │   └── Identity       (domain controllers if required)
       ├── Landing zones
       │   ├── Corp           (internal, private connectivity)
       │   └── Online         (internet-facing)
       ├── Sandbox
       └── Decommissioned
   ```
   Organise by **governance need, not org chart**. Keep the hierarchy shallow (three to four levels below the root).
4. **Plan platform subscriptions**: Management, Connectivity and Identity, each with a clear owner. Small estates may consolidate them into one platform subscription. Record that as a trade-off.
5. **Select the policy baseline.** Use the ALZ default policy assignments. Enable the deny assignments in `DoNotEnforce` mode first, then enforce. Hand custom needs to `azure-policy-governance`.
6. **Define subscription vending**: how application teams request subscriptions (one subscription per workload per environment), what each subscription gets (budget, tags, RBAC groups, spoke VNet peering), and who approves.
7. **Generate the configuration** for the chosen accelerator: the input parameters file, the management group names, the regions, and the platform subscription IDs (supplied by the user). Never invent subscription or tenant IDs; use placeholders.
8. **Validate** (see below), then present the plan: the resources, the policy impact, the estimated platform cost (firewall, gateways, Log Analytics ingestion), and the next steps. **Get explicit confirmation before any deployment.**

## Well-Architected alignment

| Pillar | Recommendation | Rationale | Source |
|---|---|---|---|
| Reliability | Deploy platform services (gateways, firewall) zone-redundant in the primary region; document the DR region | Platform outages affect every workload | https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/design-areas |
| Security | Policy-driven guardrails at MG scope; no workloads at tenant root; PIM for platform roles; centralized logging | Consistent controls at scale | https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/design-area/security |
| Cost Optimization | Budgets and mandatory cost tags via subscription vending; size platform SKUs to the actual need | Platform cost is shared and often overlooked | https://learn.microsoft.com/azure/cloud-adoption-framework/govern/cost-management/ |
| Operational Excellence | Deploy only via IaC and pipelines (ALZ accelerator); subscription vending automated | Repeatable, auditable changes | https://learn.microsoft.com/azure/architecture/landing-zones/subscription-vending |
| Performance Efficiency | Subscription-per-workload avoids hitting subscription limits; regional placement near users | Scale units and quota isolation | https://learn.microsoft.com/azure/azure-resource-manager/management/azure-subscription-service-limits |

**Trade-offs:** The full ALZ design adds platform cost (firewall, gateways, logging) and operational overhead that a small organization may not need on day one. Consolidating platform subscriptions saves cost and effort but reduces isolation. Enforcing deny policies early improves security but can block teams. Roll them out in audit mode first.

## Guardrails

- Never create resources or assign roles at the **Tenant Root Group**. Use the intermediate root.
- Never deploy without a `what-if` or `terraform plan` that the user has reviewed and confirmed.
- Don't move subscriptions between management groups in a brownfield tenant without listing the policy changes that will apply to them.
- The deployment identity uses workload identity federation (OIDC), not client secrets, and is scoped to the intermediate root only.
- Keep at least two emergency access (break-glass) accounts excluded from Conditional Access lockouts. Refer to `azure-identity-rbac`.

## Validation

- Bicep: `az deployment mg what-if --management-group-id <intermediate-root> ...`
- Terraform: `terraform validate` and `terraform plan`, reviewed in a pull request.
- After deployment: `az account management-group show --name <prefix> --expand --recurse` matches the design, and the policy compliance state is visible in the portal or through `az policy state summarize`.

## Common mistakes

- Mirroring the org chart in management groups, which makes the hierarchy deep and brittle.
- Building a custom foundation instead of using the maintained ALZ implementation.
- Putting multiple unrelated workloads in one subscription, which blurs RBAC, cost and quota boundaries.
- Leaving Sandbox subscriptions connected to the corporate network.

## Related skills

- `azure-hub-spoke-network`: connectivity subscription design
- `azure-policy-governance`: custom policy and exemptions
- `azure-identity-rbac`: platform roles, PIM, break-glass accounts
- `azure-monitoring-baseline`: management subscription and logging

## References

- Azure landing zone overview: https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/
- Implementation options: https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/implementation-options
- Management groups design area: https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org-management-groups
- Azure Landing Zones documentation and accelerator: https://azure.github.io/Azure-Landing-Zones/
- Subscription vending: https://learn.microsoft.com/azure/architecture/landing-zones/subscription-vending
- Resource naming: https://learn.microsoft.com/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming
