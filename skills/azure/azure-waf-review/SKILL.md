---
name: azure-waf-review
description: Assess an Azure workload, architecture design, or infrastructure-as-code (Bicep, Terraform, ARM) against the Microsoft Azure Well-Architected Framework and produce a prioritized findings report covering Reliability, Security, Cost Optimization, Operational Excellence and Performance Efficiency. Use when the user asks things like "review my Azure architecture", "is this Bicep well-architected", "do a WAF assessment", "what are the risks in this subscription", or "how do I make this workload production-ready on Azure". Read-only; it never changes resources.
license: MIT
metadata:
  provider: azure
  framework: Azure Well-Architected Framework
  pillars: reliability, security, cost-optimization, operational-excellence, performance-efficiency
  category: assessment
  status: draft
  last-reviewed: 2026-10-12
  version: 0.1.0
---

# Azure Well-Architected Review

Run a structured, evidence-based review of an Azure workload against the five pillars of the Azure Well-Architected Framework (WAF). The output is a prioritized report that ties each finding to a WAF design-review checklist item, the evidence for it, a concrete fix, and the trade-off involved.

## When to use

- Reviewing an existing workload deployed in Azure (one or more subscriptions or resource groups).
- Reviewing IaC (Bicep, Terraform, ARM) or an architecture diagram or description before deployment.
- Preparing a workload for production, an audit, or a cost or reliability improvement effort.

## When not to use

- Designing a landing zone from scratch: use `azure-landing-zone`.
- A pure cost deep dive: use `azure-finops-cost-review`.
- Making changes: this skill is **read-only**. Hand fixes to the relevant skill or to the user.

## Inputs to gather

Ask these first. If the user skips a question, use the default and record it as an assumption in the report.

| Input | Why it matters | Default |
|---|---|---|
| Scope: live subscription/RG, IaC files, or a design description | Determines how evidence is gathered | Ask; required |
| Workload purpose and criticality (e.g. internal tool vs. revenue-critical) | Sets the reliability and security bar | Business-important |
| Environment (dev/test/prod) | Production gets a stricter bar | prod |
| Availability / recovery targets (SLO, RTO, RPO) | Needed to judge reliability findings | None stated; flag as a gap |
| Compliance needs (e.g. PCI DSS, HIPAA, ISO 27001) | Adds mandatory controls | None |
| Pillar focus, if any | Lets the review go deeper on one area | All five, equally |

## Workflow

1. **Confirm scope and access.**
   - For a live environment, confirm the user is signed in (`az account show`) with at least **Reader** on the scope. Never ask for or accept credentials in chat.
   - For IaC or a design, read every provided file before you assess anything.
2. **Gather evidence (read-only).**
   - Live environment: run the Azure Resource Graph queries in [references/resource-graph-queries.md](references/resource-graph-queries.md) and pull Azure Advisor recommendations. Use only `list`, `show` and `graph query` commands; never `create`, `update`, `delete` or `set`.
   - IaC: if PSRule for Azure is available, run it (`Invoke-PSRule -Module PSRule.Rules.Azure`). Otherwise inspect resource properties by hand against the checklists.
   - Build a resource inventory: types, SKUs, regions, zone configuration, networking exposure, identity model.
3. **Assess each pillar** against the WAF design-review checklist for that pillar (codes `RE:`, `SE:`, `CO:`, `OE:`, `PE:`) and against the WAF **service guide** for each major service in the workload. See [references/pillar-checks.md](references/pillar-checks.md) for the checks this skill always runs.
   - If evidence is missing, report it as **"Unable to verify"**. Don't assume a pass or a fail.
   - If the user's SLO/RTO/RPO targets aren't stated, record that as an Operational Excellence and Reliability finding in its own right.
4. **Rate each finding.**
   - **High:** a likely outage, data loss, security breach or major waste. Fix now.
   - **Medium:** a significant gap against the WAF recommendation. Plan a fix.
   - **Low:** a hardening or optimization opportunity.
   - Lower the severity for dev/test environments where that's appropriate, and say that you did.
5. **State the trade-offs.** For each recommendation, name the pillar it may cost (for example, zone redundancy improves Reliability but raises Cost).
6. **Write the report** in the format in [references/report-template.md](references/report-template.md). Lead with the top 5 actions.
7. **Offer next steps.** Suggest the official Azure Well-Architected Review assessment for a formal score, and the related skills that could implement fixes. Make no changes.

## Well-Architected alignment

| Pillar | What this skill checks (summary) | Source |
|---|---|---|
| Reliability | Defined targets, zone/region redundancy, health probes, backup and restore testing, failure-mode analysis | https://learn.microsoft.com/azure/well-architected/reliability/checklist |
| Security | Identity (Microsoft Entra ID, managed identity), least-privilege RBAC, network exposure, encryption, secrets in Key Vault, Defender for Cloud | https://learn.microsoft.com/azure/well-architected/security/checklist |
| Cost Optimization | Right-sizing, idle or orphaned resources, reservations and savings plans, budgets and tagging for cost allocation | https://learn.microsoft.com/azure/well-architected/cost-optimization/checklist |
| Operational Excellence | IaC coverage, safe deployment practices, monitoring and alerting, diagnostic settings, runbooks | https://learn.microsoft.com/azure/well-architected/operational-excellence/checklist |
| Performance Efficiency | Performance targets, autoscaling, capacity planning, caching, load testing | https://learn.microsoft.com/azure/well-architected/performance-efficiency/checklist |

**Trade-offs:** The pillars pull against each other. Always present recommendations against the workload's stated criticality. A dev environment that is cheap and single-zone is a valid design choice, not a defect. See https://learn.microsoft.com/azure/well-architected/pillars for the official trade-off guidance.

## Guardrails

- **Read-only.** Never run commands that create, modify or delete resources, role assignments or policies.
- Never request, display or store secrets, keys, connection strings or tokens. If evidence contains a secret, redact it and raise a High security finding.
- Don't put tenant IDs, subscription IDs or internal hostnames in the report unless the user asks for them.
- Base each finding on evidence and give a source link. Never present an assumption as a fact.
- Respect scope: only query the subscriptions or resource groups the user named.

## Validation

- Each finding has a pillar, a checklist code, evidence, a severity, a recommendation and a source link.
- All five pillars appear in the report, even if a pillar's only entry is "no issues found" or "unable to verify".
- Spot-check a sample of High findings against the raw evidence before you present the report.

## Common mistakes

- Treating Advisor output as the whole review. Advisor is one input; the WAF checklists cover design and process gaps that Advisor can't see.
- Holding dev/test to production standards without saying so.
- Recommending multi-region for every workload. Match the recommendation to the stated RTO/RPO and criticality.
- Giving generic advice ("improve security"). Every recommendation must name a resource or pattern and a concrete change.

## Related skills

- `azure-landing-zone`: platform foundation gaps found during review
- `azure-policy-governance`: enforce fixes at scale with Azure Policy
- `azure-monitoring-baseline`: Operational Excellence gaps
- `azure-finops-cost-review`: deep cost analysis

## References

- Azure Well-Architected Framework: https://learn.microsoft.com/azure/well-architected/
- Azure Well-Architected Review assessment: https://learn.microsoft.com/assessments/azure-architecture-review/
- WAF service guides: https://learn.microsoft.com/azure/well-architected/service-guides/
- Azure Advisor: https://learn.microsoft.com/azure/advisor/advisor-overview
- Azure Resource Graph: https://learn.microsoft.com/azure/governance/resource-graph/overview
- PSRule for Azure: https://azure.github.io/PSRule.Rules.Azure/
- Microsoft Cloud Security Benchmark: https://learn.microsoft.com/security/benchmark/azure/
