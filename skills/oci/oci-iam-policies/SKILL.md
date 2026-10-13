---
name: oci-iam-policies
description: Design and review least-privilege OCI IAM — identity domains and groups, compartment-scoped policy statements using the least verb (inspect, read, use, manage), conditions, dynamic groups with instance/resource principals and OKE workload identity instead of API keys, MFA, and break-glass administration. Use when the user says "write an OCI IAM policy", "least privilege in Oracle Cloud", "review OCI policies", "remove API keys from OCI workloads", "dynamic group for instance principal", or "who can manage what in our tenancy".
license: MIT
metadata:
  provider: oci
  framework: Well-Architected Framework for OCI
  pillars: security-compliance, reliability-resilience, performance-cost, operational-efficiency
  category: identity
  status: draft
  last-reviewed: 2026-10-12
  version: 0.1.0
---

# OCI IAM Policies

Write OCI policies that grant groups the least verb on the narrowest resource type and compartment, and give workloads principals instead of keys.

## When to use

- Authoring policies for a landing zone or a new workload.
- Reviewing existing policies for over-privilege.
- Moving workloads off user API keys.

## When not to use

- Compartment structure design: use `oci-landing-zone`.

## Inputs to gather

| Input | Why it matters | Default |
|---|---|---|
| Personas and the compartments they work in | Group → policy mapping | Ask |
| Identity domain(s) and IdP federation | Group naming in policy statements (`'<domain>'/'<group>'`) | Default domain, federated |
| Workload runtimes (Compute, Functions, OKE, external) | Principal type | Ask |
| Existing API keys / auth tokens to migrate? | Cleanup scope | Ask |

## Workflow

1. **Inventory (read-only).**
   - `oci iam policy list --compartment-id <ocid>` for each compartment, including the root.
   - Flag statements that use `manage all-resources` outside Administrators, `any-user`, policies at tenancy level that could be compartment-scoped, and users with API keys (`oci iam user api-key list`).
2. **Map personas to policies** using the verb hierarchy **inspect < read < use < manage**. Grant the lowest verb that works, on specific resource families or types rather than `all-resources`:
   ```
   Allow group 'Default'/'NetworkAdmins' to manage virtual-network-family in compartment <prefix>-top:<prefix>-network
   Allow group 'Default'/'AppAdmins' to use virtual-network-family in compartment <prefix>-top:<prefix>-network
   Allow group 'Default'/'AppAdmins' to manage instance-family in compartment <prefix>-top:<prefix>-app
   Allow group 'Default'/'Auditors' to read all-resources in tenancy
   ```
3. **Attach policies at the right level.** Attach a policy to the compartment it governs, or to its parent, so compartment admins can't edit their own permissions. Keep tenancy-level policies for tenancy-wide needs only.
4. **Conditions.** Use `where` clauses to narrow further, for example `where target.resource.tag.<ns>.<key> = '<value>'`, `request.permission`, or limiting which groups a delegated admin can manage.
5. **Workloads.**
   - Compute and Functions: **dynamic groups** with matching rules (for example `ALL {instance.compartment.id = '<ocid>'}`) and **instance or resource principals**.
   - OKE: **workload identity** for pods.
   - **No user API keys on servers or in pipelines.** For CI/CD outside OCI, use identity federation where it's supported. Otherwise use a dedicated, tightly scoped service user with keys stored in a secrets manager and rotated.
6. **Human access hygiene.** Enforce MFA through identity domain sign-on policies, and federate with the corporate IdP. Keep a break-glass local admin with MFA, and monitor its use. Don't use the tenancy admin for daily work.
7. **Output** the persona matrix (persona → group → statements → compartment), the policies as Terraform, and the migration plan for keys. **Confirm before applying any changes or removals.**

## Well-Architected alignment

| Area | Recommendation | Rationale | Source |
|---|---|---|---|
| Security and Compliance | Least verb, compartment-scoped, groups not users, principals not keys, MFA | Limits blast radius and credential exposure | https://docs.oracle.com/en-us/iaas/Content/Identity/policieshow/how-policies-work.htm |
| Reliability and Resilience | Break-glass admin; principals avoid key expiry issues | Access continuity | https://docs.oracle.com/en-us/iaas/Content/Security/Concepts/security_guide.htm |
| Performance and Cost Optimization | Grant cost admins `read usage-reports`/budgets; keep policy count within service limits via families | Cost visibility; manageable policy set | https://docs.oracle.com/en-us/iaas/Content/Identity/policiescommon/commonpolicies.htm |
| Operational Efficiency | Policies as Terraform; naming conventions; periodic review | Auditable, repeatable access | https://docs.oracle.com/en-us/iaas/Content/Identity/home.htm |

**Trade-offs:** Very granular policies (individual resource types) are more secure but harder to maintain than resource families. Start with families at compartment scope and narrow them where there's risk.

## Guardrails

- Never request, print or store API private keys, auth tokens or customer secret keys. If you find exposed keys, report them as critical and recommend immediate deletion and rotation.
- Never delete policies, users or keys without explicit confirmation and an impact list.
- Never write `Allow any-user to ...` without a restrictive `where` clause and an explicit justification.
- Never grant `manage policies` in a compartment to the same group whose access those policies control, unless that is intended delegated administration.

## Validation

- Terraform plan reviewed.
- Test with a member of each group: allowed actions succeed and the boundary actions fail with authorization errors.
- Re-run the CIS compliance script; IAM controls improve.

## Common mistakes

- Attaching a compartment's policies inside that compartment, which lets its admins escalate their own privileges.
- Dynamic group matching rules that are too broad (for example the whole tenancy).
- Using `manage` where `use` is enough (for example app teams on network resources).

## Related skills

- `oci-landing-zone`, `oci-well-architected-review`, `oci-observability-baseline`

## References

- How policies work: https://docs.oracle.com/en-us/iaas/Content/Identity/policieshow/how-policies-work.htm
- Common policies: https://docs.oracle.com/en-us/iaas/Content/Identity/policiescommon/commonpolicies.htm
- Calling services from an instance (instance principals): https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/callingservicesfrominstances.htm
- OCI IAM overview: https://docs.oracle.com/en-us/iaas/Content/Identity/home.htm
- OCI security best practices: https://docs.oracle.com/en-us/iaas/Content/Security/Concepts/security_guide.htm
