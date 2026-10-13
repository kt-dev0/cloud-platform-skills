---
name: oci-well-architected-review
description: Assess an Oracle Cloud Infrastructure (OCI) workload, tenancy, design, or Terraform/Resource Manager stack against Oracle's Well-Architected Framework for OCI and the CIS OCI Foundations Benchmark, producing a prioritized, evidence-based findings report using read-only evidence from Cloud Guard, Cloud Advisor, OCI Search and the CIS compliance script. Use when the user says "review my OCI architecture", "is our Oracle Cloud tenancy secure", "run a CIS check on OCI", "OCI best practices review", or "is this OCI Terraform production-ready". Read-only.
license: MIT
metadata:
  provider: oci
  framework: Well-Architected Framework for OCI
  pillars: security-compliance, reliability-resilience, performance-cost, operational-efficiency
  category: assessment
  status: draft
  last-reviewed: 2026-10-12
  version: 0.1.0
---

# OCI Well-Architected Review

Run a structured, evidence-based review of an OCI tenancy or workload against the four areas of Oracle's Well-Architected Framework for OCI, with CIS Benchmark evidence where it applies.

## When to use

- Reviewing a deployed tenancy or workload compartment.
- Reviewing Terraform or Resource Manager stacks, or a design, before go-live.

## When not to use

- Designing the tenancy foundation: use `oci-landing-zone`.
- Making changes: this skill is **read-only**.

## Inputs to gather

| Input | Why it matters | Default |
|---|---|---|
| Scope: tenancy, compartments, regions, IaC or design | Evidence approach | Ask (required) |
| Workload criticality and RTO/RPO | Reliability bar | Flag missing targets |
| Environment | Severity calibration | prod |
| Compliance needs | Extra controls | None |

## Workflow

1. **Confirm access.** `oci iam region list` and `oci iam compartment list`. The reviewer group needs read-only policies, for example `Allow group <domain>/<Auditors> to inspect all-resources in tenancy` and `Allow group <domain>/<Auditors> to read all-resources in tenancy`. Never ask for API private keys in chat.
2. **Gather evidence (read-only).** Use only `list`, `get` and `search` commands.
   - Inventory: `oci search resource structured-search --query-text "query all resources"` per subscribed region.
   - **Cloud Guard** problems and recommendations (`oci cloud-guard problem list --compartment-id <tenancy-ocid> --compartment-id-in-subtree true`).
   - **Cloud Advisor** recommendations (cost, performance, high availability, security).
   - **CIS compliance script** from the OCI Landing Zones project, which runs read-only and produces CIS Benchmark reports.
   - IAM policies: `oci iam policy list --compartment-id <ocid>`. Flag `manage all-resources in tenancy` outside Administrators.
   - IaC: `terraform validate`, plus Checkov if available.
3. **Assess each area.** See [references/pillar-checks.md](references/pillar-checks.md). Mark missing evidence as **Unable to verify**.
4. **Rate findings** High / Medium / Low, calibrated to the environment.
5. **State the trade-offs** for each recommendation.
6. **Write the report**: a summary by area, the top 5 actions, the findings (area, CIS control if applicable, evidence, severity, recommendation, trade-off, source), the unable-to-verify items, and next steps.

## Well-Architected alignment

| Area | What this skill checks (summary) | Source |
|---|---|---|
| Security and Compliance | IAM policy scope, MFA, compartments, Cloud Guard, Security Zones, Vault keys, public exposure, CIS controls | https://docs.oracle.com/en/solutions/oci-best-practices/ |
| Reliability and Resilience | Availability domain / fault domain distribution, backups and tested restore, cross-region DR vs. RTO/RPO, service limits | https://docs.oracle.com/en/solutions/oci-best-practices/ |
| Performance and Cost Optimization | Right-sizing (flexible shapes), autoscaling, budgets, tagging, idle resources, storage tiers | https://docs.oracle.com/en/solutions/oci-best-practices/ |
| Operational Efficiency | IaC (Terraform/Resource Manager), monitoring and alarms, logging, events/notifications, runbooks | https://docs.oracle.com/en/solutions/oci-best-practices/ |

**Trade-offs:** Match recommendations to criticality. Cross-region DR raises cost; Security Zones restrict some configurations. Present both sides.

## Guardrails

- **Read-only.** No `create`, `update` or `delete` commands, and no policy changes.
- Redact OCIDs and user names from the report unless the user asks otherwise. Report exposed key material as High.
- Stay within the given scope and regions.

## Validation

- Every area appears in the report.
- Each High finding has been re-checked against the raw evidence.

## Common mistakes

- Reviewing only the home region.
- Missing policies defined in parent compartments or at the root.

## Related skills

- `oci-landing-zone`, `oci-iam-policies`, `oci-hub-spoke-network`, `oci-observability-baseline`

## References

- Well-Architected Framework for OCI: https://docs.oracle.com/en/solutions/oci-best-practices/
- Cloud Guard: https://docs.oracle.com/en-us/iaas/Content/cloud-guard/home.htm
- Cloud Advisor: https://docs.oracle.com/en-us/iaas/Content/CloudAdvisor/home.htm
- OCI Search: https://docs.oracle.com/en-us/iaas/Content/Search/home.htm
- OCI Landing Zones (incl. CIS compliance script): https://github.com/oci-landing-zones
- CIS Oracle Cloud Infrastructure Foundations Benchmark: https://www.cisecurity.org/benchmark/oracle_cloud
