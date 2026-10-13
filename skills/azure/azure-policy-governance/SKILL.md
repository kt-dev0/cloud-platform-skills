---
name: azure-policy-governance
description: Design, author, and safely roll out Azure Policy as code — choosing built-in vs. custom definitions, grouping into initiatives, assigning at management group scope, staged enforcement (audit → deny), remediation of DeployIfNotExists/Modify policies, and exemptions. Use when the user says "enforce tagging in Azure", "write an Azure Policy", "deny public IPs", "set up policy as code", "remediate non-compliant resources", "create a policy exemption", or "why is my deployment blocked by policy".
license: MIT
metadata:
  provider: azure
  framework: Azure Well-Architected Framework
  pillars: reliability, security, cost-optimization, operational-excellence, performance-efficiency
  category: governance
  status: draft
  last-reviewed: 2026-10-12
  version: 0.1.0
---

# Azure Policy Governance

Turn governance requirements into Azure Policy that is managed as code, assigned at the right scope, rolled out without breaking teams, and kept compliant through remediation.

## When to use

- Enforcing standards (tags, allowed regions or SKUs, no public access, diagnostic settings).
- Moving from portal-managed policy to policy as code.
- Investigating a policy denial or non-compliance, or handling an exemption request.

## When not to use

- Initial landing zone setup, where the ALZ default policies already apply: use `azure-landing-zone` first.
- RBAC and access control: use `azure-identity-rbac`.

## Inputs to gather

| Input | Why it matters | Default |
|---|---|---|
| The requirement in plain words (e.g. "all resources need an owner tag") | Drives definition choice | Ask (required) |
| Scope (management group / subscription) | Assignment location | Lowest MG that covers all targets |
| Desired effect (audit / deny / auto-fix) | Determines user impact | Audit first |
| Compliance framework (e.g. CIS, NIST, ISO 27001) | Built-in regulatory initiatives may already cover it | None |
| Policy-as-code tooling (Bicep/Terraform/EPAC) | Repo layout and pipeline | Same as existing IaC |

## Workflow

1. **Search built-ins first.** Look for a built-in definition or initiative before writing a custom one: `az policy definition list --query "[?contains(displayName, '<keyword>')]"`. Built-ins are maintained by Microsoft.
2. **Choose the effect.**
   - Use `Deny` to prevent new non-compliance at deployment time.
   - Use `Audit` / `AuditIfNotExists` for visibility only.
   - Use `Modify` to add or replace tags and some properties automatically. It needs a managed identity.
   - Use `DeployIfNotExists` to deploy companion resources such as diagnostic settings or private DNS records. It needs a managed identity.
   - Parameterize the effect (`effect` parameter) so the same definition can be audited first and enforced later.
3. **Author custom definitions** only when no built-in fits. Use the narrowest `if` conditions, aliases from `az provider show --namespace <ns> --expand "resourceTypes/aliases"`, and `mode: Indexed` for resources that support tags and location.
4. **Group into initiatives** by intent (for example "Security baseline", "Tagging"), not one assignment per policy.
5. **Assign at management group scope** where possible. Grant DINE/Modify assignment identities the minimum role at that scope (for example Contributor only where it's required, or a narrower built-in role).
6. **Roll out safely** (follow the safe deployment practices for policy):
   1. Assign with `enforcementMode: DoNotEnforce`, or with the `Audit` effect, to a test or canary scope.
   2. Review compliance results and the impacted teams.
   3. Widen the scope ring by ring (sandbox → non-prod → prod).
   4. Switch to `Deny` or enforced mode, and communicate the change ahead of time.
7. **Remediate** existing resources for DINE/Modify policies with remediation tasks (`az policy remediation create`). **Confirm with the user first**, because remediation changes live resources.
8. **Exemptions.** Use `Waiver` or `Mitigated` categories with an `expiresOn` date and a documented justification. Never disable an assignment just to unblock one team.
9. **Store everything as code** in a repo with PR review. Deploy through a pipeline using a workload-identity-federated identity.

## Well-Architected alignment

| Pillar | Recommendation | Rationale | Source |
|---|---|---|---|
| Reliability | Enforce zone-redundant SKUs / backup policies for prod scopes via audit or DINE | Prevents fragile deployments at scale | https://learn.microsoft.com/azure/governance/policy/overview |
| Security | Deny public network access, enforce encryption/TLS, deploy Defender and diagnostics via DINE; align to Microsoft Cloud Security Benchmark | Guardrails apply regardless of who deploys | https://learn.microsoft.com/security/benchmark/azure/ |
| Cost Optimization | Allowed SKUs/regions; required cost tags with Modify-based inheritance | Prevents expensive surprises; enables cost allocation | https://learn.microsoft.com/azure/governance/policy/tutorials/govern-tags |
| Operational Excellence | Policy as code, staged rollout, exemptions with expiry | Predictable, auditable governance changes | https://learn.microsoft.com/azure/governance/policy/how-to/policy-safe-deployment-practices |
| Performance Efficiency | Keep policy count manageable (initiatives, built-ins); avoid overly broad DINE that slows deployments | Evaluation overhead and deployment friction | https://learn.microsoft.com/azure/governance/policy/concepts/effect-basics |

**Trade-offs:** A `Deny` policy gives the strongest guarantee but blocks teams at deploy time, so pair it with clear error messages (`nonComplianceMessages`) and an exemption process. DINE automation reduces toil but needs privileged managed identities, which widen the blast radius. Scope those roles narrowly.

## Guardrails

- Never assign `Deny` straight to production scopes without an audit phase, unless the user explicitly accepts the risk.
- Never run remediation tasks without explicit confirmation and a list of the affected resources.
- Don't grant `Owner` to policy assignment identities.
- Exemptions must have an expiry date and a justification.

## Validation

- Validate definitions with a test deployment against a sandbox scope, using compliant and non-compliant cases.
- `az policy state summarize --management-group <mg>` before and after.
- `az policy state trigger-scan` to force evaluation in test scopes.
- For Deny, show that a non-compliant `what-if` deployment fails with the expected `nonComplianceMessage`.

## Common mistakes

- Writing custom policies that duplicate built-ins.
- Using `mode: All` for tag policies, which flags resources that don't support tags.
- Forgetting that DINE/Modify policies don't fix existing resources without a remediation task.
- Assigning at subscription level everywhere instead of at the management group.

## Related skills

- `azure-landing-zone`: ALZ default policy assignments
- `azure-monitoring-baseline`: DINE policies for diagnostic settings
- `azure-hub-spoke-network`: private DNS zone policies

## References

- Azure Policy overview: https://learn.microsoft.com/azure/governance/policy/overview
- Policy effects: https://learn.microsoft.com/azure/governance/policy/concepts/effect-basics
- Safe deployment practices for policy: https://learn.microsoft.com/azure/governance/policy/how-to/policy-safe-deployment-practices
- Remediate non-compliant resources: https://learn.microsoft.com/azure/governance/policy/how-to/remediate-resources
- Exemption structure: https://learn.microsoft.com/azure/governance/policy/concepts/exemption-structure
- Enterprise Policy as Code (EPAC): https://azure.github.io/enterprise-azure-policy-as-code/
