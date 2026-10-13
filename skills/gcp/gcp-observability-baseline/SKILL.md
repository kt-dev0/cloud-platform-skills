---
name: gcp-observability-baseline
description: Establish organization-wide logging and monitoring in Google Cloud — Cloud Audit Logs configuration (including Data Access logs), aggregated organization log sinks to a central log bucket or BigQuery, log retention and Log Analytics, Cloud Monitoring metrics scopes, alerting policies and notification channels, SLO monitoring, Ops Agent for VMs, and log cost controls. Use when the user says "centralize logs in GCP", "set up an org log sink", "enable data access audit logs", "monitor multiple GCP projects", "baseline alerts for Google Cloud", or "reduce Cloud Logging cost".
license: MIT
metadata:
  provider: gcp
  framework: Google Cloud Well-Architected Framework
  pillars: operational-excellence, security, reliability, cost-optimization, performance-optimization, sustainability
  category: observability
  status: draft
  last-reviewed: 2026-10-12
  version: 0.1.0
---

# Google Cloud Observability Baseline

Give every project complete audit logging, centralized log storage, and actionable monitoring, with costs kept under control.

## When to use

- After the landing zone is created, or when auditing logging and monitoring gaps.
- Building cross-project dashboards and alerting.
- Reducing Cloud Logging spend.

## When not to use

- Application instrumentation details (OpenTelemetry in app code). That belongs to the workload team.

## Inputs to gather

| Input | Why it matters | Default |
|---|---|---|
| Retention requirements (audit vs. operational) | Log bucket retention, locked buckets, BigQuery/Cloud Storage export | Audit 1 year+; operational 30 days |
| Data residency | Log bucket region | Ask |
| Sensitive services needing Data Access logs | Cost vs. visibility | Ask |
| SIEM in use? | Pub/Sub or BigQuery export | None |
| Alert destinations | Notification channels | Email + chat/paging |

## Workflow

1. **Assess (read-only).** `gcloud logging sinks list --organization=<ID>`, `gcloud logging buckets list --project=<logging-project>`, and the org and project IAM audit configs (`auditConfigs` in `get-iam-policy`).
2. **Audit logs.** Admin Activity and System Event logs are always on. **Data Access logs are off by default for most services.** Enable them at organization or folder level for sensitive services (for example Cloud Storage, Secret Manager, BigQuery, Cloud SQL). Explain the cost impact first.
3. **Aggregated sinks.** Create an **organization-level aggregated sink** (with `--include-children`) routing audit logs, and other required logs, to a **central log bucket** in a dedicated logging project in the common folder. Optionally add BigQuery for analytics or Pub/Sub for a SIEM. Grant the sink's writer identity only the destination permission it needs.
4. **Log storage.** Set retention on the central bucket. Use **bucket locking** only when compliance requires immutability. Upgrade the bucket to **Log Analytics** for SQL queries. Create log views to restrict access per team.
5. **Cost controls.** Add exclusion filters on the `_Default` sink for noisy, low-value logs (for example debug-level logs or some load balancer request logs), and use sampling in VPC Flow Logs. Never exclude audit logs that compliance requires. Note that `_Required` logs can't be excluded.
6. **Monitoring.**
   - Create a **metrics scope** in a central monitoring project that includes the workload projects (per environment).
   - Define **SLOs** for key services, and alert on SLO burn rate rather than raw metrics where possible.
   - Create alerting policies with documentation (runbook links), routed to notification channels.
   - Install the **Ops Agent** on VMs through policy or an agent policy.
7. **Security signals.** Use Security Command Center for findings, and log-based alerts for critical events (for example IAM policy changes at org level, org policy changes, or sink deletion).
8. **Generate Terraform.** Run `terraform plan`, show the cost estimate (log ingestion and storage beyond the free allotment, Data Access log volume), and **confirm before applying**.

## Well-Architected alignment

| Pillar | Recommendation | Rationale | Source |
|---|---|---|---|
| Operational Excellence | Central metrics scopes; SLO-based alerting with runbooks; Ops Agent | Actionable, low-noise operations | https://cloud.google.com/monitoring/settings |
| Security, Privacy and Compliance | Org aggregated sink; Data Access logs for sensitive services; restricted log views; optional bucket lock | Complete, protected audit trail | https://cloud.google.com/logging/docs/export/aggregated_sinks |
| Reliability | SLOs and burn-rate alerts; uptime checks | Detect user-impacting issues early | https://cloud.google.com/monitoring/slo-monitoring |
| Cost Optimization | Exclusion filters, retention tuning, flow log sampling, selective Data Access logs | Logging cost grows with volume | https://cloud.google.com/logging/docs/routing/overview |
| Performance Optimization | Log Analytics for fast cross-project queries; metrics for real-time alerting | Faster investigation | https://cloud.google.com/logging/docs/log-analytics |
| Sustainability | Store only useful logs; expire data appropriately | Less stored data | https://cloud.google.com/architecture/framework/sustainability |

**Trade-offs:** Enabling Data Access logs broadly gives maximum audit coverage at a high cost; target sensitive services first. Locked buckets meet compliance needs but can't be shortened or deleted. Confirm the requirement before locking.

## Guardrails

- Never delete or modify org-level sinks, or exclude audit logs, without explicit confirmation.
- Never lock a log bucket without explicit approval, because it's irreversible.
- Don't route logs outside the approved residency region.
- Give the sink writer identity least privilege on the destination only.

## Validation

- `gcloud logging sinks describe <sink> --organization=<ID>` shows `includeChildren: true` and the correct destination.
- A test admin action in a workload project appears in the central bucket within minutes.
- A test incident fires an alert to the notification channel.

## Common mistakes

- Assuming Data Access logs are on by default.
- A project-level sink instead of an org-level aggregated sink, which leaves new projects uncovered.
- Alerting on every metric with no SLO context.

## Related skills

- `gcp-landing-zone`, `gcp-iam-least-privilege`, `gcp-well-architected-review`

## References

- Cloud Audit Logs: https://cloud.google.com/logging/docs/audit
- Aggregated sinks: https://cloud.google.com/logging/docs/export/aggregated_sinks
- Log Analytics: https://cloud.google.com/logging/docs/log-analytics
- Metrics scopes: https://cloud.google.com/monitoring/settings
- SLO monitoring: https://cloud.google.com/monitoring/slo-monitoring
- Ops Agent: https://cloud.google.com/monitoring/agent/ops-agent
