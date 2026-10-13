---
name: oci-observability-baseline
description: Establish tenancy-wide logging, monitoring and alerting in Oracle Cloud Infrastructure — Audit log retention, service logs (VCN Flow Logs, Object Storage, Load Balancer), Connector Hub routing to Object Storage / Logging Analytics / SIEM, Monitoring alarms, Notifications topics, Events rules for critical IAM and network changes (CIS), and Cloud Guard integration. Use when the user says "centralize logs in OCI", "set up OCI alarms", "CIS event notifications", "send OCI logs to our SIEM", "Connector Hub setup", or "monitoring baseline for Oracle Cloud".
license: MIT
metadata:
  provider: oci
  framework: Well-Architected Framework for OCI
  pillars: security-compliance, reliability-resilience, performance-cost, operational-efficiency
  category: observability
  status: draft
  last-reviewed: 2026-10-12
  version: 0.1.0
---

# OCI Observability Baseline

Make sure every compartment has audit coverage, the critical service logs, alarms with owners, and notifications for security-relevant changes, all centralized and retained appropriately.

## When to use

- After landing zone setup, or when CIS checks show logging and notification gaps.
- Integrating OCI with a SIEM or central log platform.

## When not to use

- Application-level APM instrumentation details. They belong to the workload team.

## Inputs to gather

| Input | Why it matters | Default |
|---|---|---|
| Audit retention requirement | Tenancy Audit retention setting; archive to Object Storage for longer | 365 days |
| SIEM / log platform | Connector Hub target (Streaming, Object Storage, Logging Analytics) | Object Storage archive |
| Subscribed regions | Logging and Events are regional | Ask |
| Alert destinations | Notifications subscriptions (email, PagerDuty, Slack via HTTPS, Functions) | Email |

## Workflow

1. **Assess (read-only).** Check the tenancy Audit retention (`oci audit config get --compartment-id <tenancy-ocid>`), `oci logging log-group list`, `oci events rule list` and `oci ons topic list` per compartment and region.
2. **Audit.** Audit is always on. Set retention to meet the requirement, and archive to Object Storage through Connector Hub if you need longer than the maximum.
3. **Service logs.** In a log group in the security or logging compartment, enable:
   - VCN Flow Logs (at least for the hub and prod subnets)
   - Object Storage write (and read, for sensitive buckets) logs
   - Load balancer access and error logs
   - Network Firewall logs
4. **Connector Hub.** Route Audit and service logs to the destination: an Object Storage bucket with lifecycle and retention rules, Logging Analytics, or Streaming for a SIEM. Grant the connector only the policies it needs.
5. **Events and Notifications (CIS-aligned).** Create Notifications topics for security and operations, and Events rules that notify on:
   - IAM changes: identity providers, IdP group mappings, groups, policies, users
   - Network changes: VCNs, route tables, security lists, NSGs, network gateways
   - Cloud Guard problems detected
6. **Monitoring.** Create alarms on user-impacting symptoms (compute and LB health, database availability, error rates), and route them to Notifications topics with severity, owners and runbook links in the alarm body.
7. **Agents.** Enable the Oracle Cloud Agent monitoring plugin on compute instances. Use the Management Agent and Logging Analytics for OS and application logs where needed.
8. **Generate Terraform.** Run `terraform plan`, present the cost drivers (Logging Analytics ingestion, storage, Streaming), and **confirm before applying**.

## Well-Architected alignment

| Area | Recommendation | Rationale | Source |
|---|---|---|---|
| Security and Compliance | Audit retention; CIS event notifications; flow logs; centralized, access-controlled log storage | Detect and investigate security events | https://docs.oracle.com/en-us/iaas/Content/Audit/home.htm |
| Reliability and Resilience | Health and availability alarms with owners; notifications to on-call | Faster detection and recovery | https://docs.oracle.com/en-us/iaas/Content/Monitoring/home.htm |
| Performance and Cost Optimization | Object Storage lifecycle tiers for archives; collect only needed logs; right-size Logging Analytics ingestion | Logging cost control | https://docs.oracle.com/en-us/iaas/Content/connector-hub/home.htm |
| Operational Efficiency | Observability as Terraform; standardized topics, rules and alarms per compartment | Consistent coverage | https://docs.oracle.com/en-us/iaas/Content/Logging/home.htm |

**Trade-offs:** Enabling read logs on all buckets and flow logs on every subnet maximizes visibility at a storage and analysis cost; prioritize sensitive and production resources. Retention locks on archive buckets support compliance but make deletion impossible during the retention period.

## Guardrails

- Never shorten Audit retention, or delete log groups, rules or connectors, without explicit confirmation.
- Don't apply Object Storage retention rules that lock data without explicit approval.
- Don't send security notifications to unauthenticated public endpoints.
- Use least-privilege policies for Connector Hub service principals.

## Validation

- `terraform plan` reviewed.
- A test IAM change (in a sandbox, **with confirmation**) triggers the expected notification.
- Logs appear at the Connector Hub destination. The CIS compliance script's logging and monitoring section improves.

## Common mistakes

- Creating Events rules in only one region, even though IAM events are delivered in the home region and network events are regional.
- Topics without confirmed subscriptions.
- Leaving Audit at the default retention when compliance needs longer.

## Related skills

- `oci-landing-zone`, `oci-hub-spoke-network`, `oci-well-architected-review`

## References

- Audit: https://docs.oracle.com/en-us/iaas/Content/Audit/home.htm
- Logging: https://docs.oracle.com/en-us/iaas/Content/Logging/home.htm
- Connector Hub: https://docs.oracle.com/en-us/iaas/Content/connector-hub/home.htm
- Monitoring: https://docs.oracle.com/en-us/iaas/Content/Monitoring/home.htm
- Events: https://docs.oracle.com/en-us/iaas/Content/Events/home.htm
- Logging Analytics: https://docs.oracle.com/en-us/iaas/logging-analytics/home.htm
