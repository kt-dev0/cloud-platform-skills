---
name: azure-identity-rbac
description: Design least-privilege access for Azure — Azure RBAC role assignments at the right scope, Microsoft Entra groups, Privileged Identity Management (PIM) for just-in-time admin access, managed identities for workloads, workload identity federation for CI/CD (no secrets), and emergency access accounts. Use when the user says "who should have Owner", "set up RBAC for our subscriptions", "remove secrets from our pipeline", "use managed identity", "set up PIM", "GitHub Actions OIDC to Azure", or "review Azure role assignments".
license: MIT
metadata:
  provider: azure
  framework: Azure Well-Architected Framework
  pillars: reliability, security, cost-optimization, operational-excellence, performance-efficiency
  category: identity
  status: draft
  last-reviewed: 2026-10-12
  version: 0.1.0
---

# Azure Identity and RBAC

Design and review who and what can access Azure resources, so that humans get just-in-time, group-based, least-privilege access, and workloads authenticate without secrets.

## When to use

- Designing the RBAC model for a landing zone or a new workload.
- Reviewing existing role assignments for excessive privilege.
- Removing client secrets and keys from apps and pipelines.

## When not to use

- Entra ID tenant-wide configuration such as Conditional Access policy authoring in depth. This skill flags the need; tenant identity is usually owned by a separate identity team.
- Policy-based governance: use `azure-policy-governance`.

## Inputs to gather

| Input | Why it matters | Default |
|---|---|---|
| Personas (platform admins, app teams, readers, auditors, pipelines) | Map personas to roles | Ask |
| Scopes (MG / subscription / RG) | Where assignments live | Use the management group hierarchy from `azure-landing-zone` |
| Entra ID P2 / Governance licensing available? | PIM requires it | Ask |
| CI/CD platform | Federated credential setup | GitHub Actions |
| Existing assignments to review? | Brownfield cleanup | Ask |

## Workflow

1. **Inventory (read-only, if brownfield).** `az role assignment list --all --include-inherited --output table` per scope. Flag:
   - `Owner`, `Contributor` or `User Access Administrator` assigned to **users** rather than groups.
   - Assignments at subscription or MG scope that could be narrower.
   - Assignments to deleted principals ("Unknown" identities).
   - Service principals that hold client secrets.
2. **Map personas to built-in roles.** Prefer built-in roles over custom ones. Use custom roles only when no built-in fits, and keep their `actions` explicit (no `*`).
   - Platform admins: `Owner` at the intermediate-root MG, **eligible through PIM only**.
   - App teams: `Contributor` (or narrower) on their own subscription or RG. Delegate role assignment through **Role Based Access Control Administrator with conditions** that restrict which roles they can assign.
   - Auditors: `Reader` (plus `Security Reader` where needed).
3. **Assign to Entra groups, not users.** Use role-assignable groups for privileged roles.
4. **Privileged Identity Management.** Make privileged roles eligible (not active) and require MFA, a justification, an approval for Owner or User Access Administrator, and a time limit. Schedule access reviews.
5. **Workload identities.**
   - Azure-hosted apps: use **managed identities**. Choose user-assigned when several resources share an identity or its lifecycle must be independent; otherwise use system-assigned.
   - CI/CD and external workloads: use **workload identity federation** (OIDC) on an app registration or a user-assigned managed identity. **No client secrets.**
   - AKS: Microsoft Entra Workload ID.
   - Disable local or key-based auth on data services where it's supported (Storage shared keys, Cosmos DB local auth, Service Bus SAS). Use data-plane RBAC instead.
6. **Emergency access.** Keep at least two cloud-only break-glass accounts with strong phishing-resistant credentials, excluded from Conditional Access policies that could lock everyone out, and alert on every sign-in.
7. **Produce the RBAC matrix** (persona → group → role → scope → PIM yes/no) and the IaC for the role assignments. Present any removals or changes and **confirm before applying**.

## Well-Architected alignment

| Pillar | Recommendation | Rationale | Source |
|---|---|---|---|
| Reliability | Break-glass accounts; avoid secret expiry outages by using managed identity / federation | Expired secrets are a common outage cause | https://learn.microsoft.com/entra/identity/role-based-access-control/security-emergency-access |
| Security | Least privilege, group-based, PIM for privileged roles, no standing Owner, no secrets | Identity is the primary security perimeter | https://learn.microsoft.com/azure/role-based-access-control/best-practices |
| Cost Optimization | PIM and access reviews need Entra ID P2/Governance licenses—license only privileged users | Avoid over-licensing | https://learn.microsoft.com/entra/id-governance/licensing-fundamentals |
| Operational Excellence | Role assignments as code; periodic access reviews; RBAC matrix documented | Auditable, repeatable access | https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/design-area/identity-access |
| Performance Efficiency | Stay within role-assignment limits per subscription by assigning to groups at higher scopes | Large estates hit assignment limits | https://learn.microsoft.com/azure/role-based-access-control/troubleshoot-limits |

**Trade-offs:** PIM approvals add friction during incidents, so balance this with eligible roles that don't need approval for on-call engineers. Very granular custom roles maximize least privilege but are costly to maintain. Prefer built-ins at a narrower scope.

## Guardrails

- Never remove role assignments, disable accounts or rotate credentials without explicit confirmation and an impact list.
- Never output, log or store secrets. When you find existing secrets, recommend migrating to federation or managed identity and rotating them.
- Never assign `Owner` or `User Access Administrator` as a permanent (active) assignment to an individual user, except for the documented break-glass accounts.
- Don't exclude regular admin accounts from Conditional Access.

## Validation

- `az role assignment list --assignee <principal> --all` shows only the intended roles and scopes.
- The pipeline signs in through OIDC (`azure/login` with `client-id`/`tenant-id`/`subscription-id` and no secret) and succeeds.
- PIM: the role shows as *Eligible* and activation requires MFA and justification.
- Entra sign-in logs alert fires on a test break-glass sign-in (coordinate with the identity team).

## Common mistakes

- Using `Contributor` for pipelines at subscription scope when RG-scoped or narrower roles suffice.
- Creating a service principal with a secret for an Azure-hosted app that could use managed identity.
- Assigning roles directly to users, which leads to orphaned access when people change teams.

## Related skills

- `azure-landing-zone`: management group scopes
- `azure-policy-governance`: deny local auth via policy
- `azure-waf-review`: Security pillar findings

## References

- Azure RBAC best practices: https://learn.microsoft.com/azure/role-based-access-control/best-practices
- Privileged Identity Management: https://learn.microsoft.com/entra/id-governance/privileged-identity-management/pim-configure
- Managed identities overview: https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/overview
- Workload identity federation: https://learn.microsoft.com/entra/workload-id/workload-identity-federation
- Delegate role assignments with conditions: https://learn.microsoft.com/azure/role-based-access-control/delegate-role-assignments-overview
- Emergency access accounts: https://learn.microsoft.com/entra/identity/role-based-access-control/security-emergency-access
- Identity and access management design area: https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/design-area/identity-access
