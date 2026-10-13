---
name: azure-monitoring-baseline
description: Establish a platform monitoring baseline in Azure — Log Analytics workspace design, diagnostic settings at scale via Azure Policy, Azure Monitor Agent with data collection rules, activity log and Service Health alerts, Azure Monitor Baseline Alerts (AMBA), action groups, and log cost controls. Use when the user says "set up monitoring for Azure", "centralize logs", "how many Log Analytics workspaces", "enable diagnostic settings everywhere", "baseline alerts for Azure", or "our Log Analytics bill is too high".
license: MIT
metadata:
  provider: azure
  framework: Azure Well-Architected Framework
  pillars: reliability, security, cost-optimization, operational-excellence, performance-efficiency
  category: observability
  status: draft
  last-reviewed: 2026-10-12
  version: 0.1.0
---

# Azure Monitoring Baseline

Give every Azure subscription consistent, centrally managed observability — logs, metrics, alerts and health notifications — at a cost the organization can sustain.

## When to use

- Setting up the Management subscription of a landing zone.
- Standardizing diagnostic settings, agents and alerts across subscriptions.
- Reducing Log Analytics cost or consolidating sprawling workspaces.

## When not to use

- Application performance tuning inside a single app (Application Insights instrumentation details belong to the app team).
- SIEM content engineering in Microsoft Sentinel. This skill only prepares the workspace.

## Inputs to gather

| Input | Why it matters | Default |
|---|---|---|
| Data residency / sovereignty requirements | Workspace region(s) | Ask |
| Log retention needs (operational vs. compliance) | Interactive vs. long-term retention | 30–90 days interactive; archive for compliance |
| Who responds to alerts (on-call tool, email, ITSM) | Action group design | Email + on-call webhook |
| Microsoft Sentinel planned? | Workspace topology | No |
| Expected daily ingestion (GB) | Commitment tier decision | Estimate from a pilot |

## Workflow

1. **Workspace design.** Start with **as few workspaces as possible**: typically one central platform workspace per region or sovereignty boundary. Add separate workspaces only for data-residency, billing-separation or access-separation needs that table-level or resource-context RBAC can't meet.
2. **Platform logs.**
   - Send the Activity Log of every subscription to the central workspace, through policy.
   - Assign the built-in initiative that enables resource logs (category group `allLogs` or `audit`) to Log Analytics at the management group scope, using `DeployIfNotExists`. Remediate existing resources **after confirmation**.
3. **VM and Arc telemetry.** Use **Azure Monitor Agent (AMA)** with data collection rules (DCRs) deployed through policy. The legacy Log Analytics (MMA) agent is retired. Collect only the needed events and counters.
4. **Application telemetry.** Use workspace-based Application Insights resources only (classic is retired).
5. **Alerts.**
   - Deploy **Azure Monitor Baseline Alerts (AMBA)** for platform and landing zone resources as a starting set.
   - Add **Service Health** and **Resource Health** alerts per subscription.
   - Route through a small set of standard **action groups** (for example critical → on-call; warning → email or ITSM).
   - Alert on symptoms that affect users, not on every metric. Every alert needs an owner and a runbook link.
6. **Cost controls.**
   - Set table plans: use Basic or Auxiliary logs for high-volume, low-query data where that fits.
   - Set retention per table, and use long-term retention for compliance instead of keeping data interactive.
   - Use a commitment tier when steady ingestion justifies it.
   - Add a daily cap only for non-prod. **Never cap a security or production workspace.**
   - Use DCR transformations to filter noisy data at ingestion.
7. **Access.** Use resource-context access so app teams see their own resources' logs without workspace-wide rights.
8. **Generate IaC and policy assignments**, preview them, show the estimated ingestion cost, and **confirm before deploying**.

## Well-Architected alignment

| Pillar | Recommendation | Rationale | Source |
|---|---|---|---|
| Reliability | Service Health/Resource Health alerts; AMBA baseline; health models for critical workloads | Detect platform and resource failures fast | https://azure.github.io/azure-monitor-baseline-alerts/ |
| Security | Activity log + audit logs centralized; workspace RBAC; immutable/long-term retention for compliance; Sentinel-ready | Investigations need complete, protected logs | https://learn.microsoft.com/azure/azure-monitor/logs/workspace-design |
| Cost Optimization | Minimize workspaces, table plans, per-table retention, DCR filtering, commitment tiers | Log ingestion is often the largest monitoring cost | https://learn.microsoft.com/azure/azure-monitor/best-practices-cost |
| Operational Excellence | Diagnostics and agents via policy; alerts with owners and runbooks; dashboards/workbooks | Consistent coverage without manual effort | https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/design-area/management |
| Performance Efficiency | Collect only needed counters/frequency; use metrics (not logs) for near-real-time alerting | Lower latency alerts, less query load | https://learn.microsoft.com/azure/azure-monitor/alerts/alerts-types |

**Trade-offs:** Collecting `allLogs` everywhere maximizes visibility but can multiply cost. Start with `audit` plus targeted categories and expand on demand. A single workspace simplifies querying but may conflict with data residency or chargeback requirements.

## Guardrails

- Never set a daily cap on a workspace used for security or production incident response.
- Running DINE remediation and changing table plans or retention can cause data loss or cost changes. **Confirm first.**
- Don't send logs across sovereignty boundaries without explicit approval.
- Don't put secrets in action group webhooks. Use secure webhooks or Key Vault-backed configuration.

## Validation

- `az monitor diagnostic-settings list --resource <id>` on sample resources shows the central workspace.
- KQL in the workspace: `AzureActivity | summarize count() by SubscriptionId` shows every subscription.
- `Usage | where TimeGenerated > ago(7d) | summarize GB = sum(Quantity)/1024 by DataType | top 10 by GB` identifies cost drivers.
- Fire a test alert through each action group.

## Common mistakes

- Creating one workspace per application or per resource group.
- Enabling every log category without a consumer for the data.
- Keeping the retired MMA agent or classic Application Insights resources.
- Alert storms with no owner, which train teams to ignore alerts.

## Related skills

- `azure-landing-zone`: Management subscription
- `azure-policy-governance`: DINE policy rollout and remediation
- `azure-waf-review`: Operational Excellence findings

## References

- Log Analytics workspace design: https://learn.microsoft.com/azure/azure-monitor/logs/workspace-design
- Create diagnostic settings at scale with policy: https://learn.microsoft.com/azure/azure-monitor/essentials/diagnostics-settings-policies-deployifnotexists
- Azure Monitor Agent overview: https://learn.microsoft.com/azure/azure-monitor/agents/azure-monitor-agent-overview
- Azure Monitor Baseline Alerts: https://azure.github.io/azure-monitor-baseline-alerts/
- Cost optimization in Azure Monitor: https://learn.microsoft.com/azure/azure-monitor/best-practices-cost
- Management design area: https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/design-area/management
