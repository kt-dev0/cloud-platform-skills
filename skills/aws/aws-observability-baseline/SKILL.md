---
name: aws-observability-baseline
description: Establish organization-wide logging, detection and monitoring on AWS — organization CloudTrail to a Log Archive account, AWS Config with an aggregator, GuardDuty and Security Hub with delegated administration, VPC Flow Logs, CloudWatch cross-account observability, log retention, alarms and AWS Health notifications. Use when the user says "centralize logging in AWS", "set up CloudTrail for the organization", "enable GuardDuty everywhere", "cross-account CloudWatch dashboards", "baseline alarms for AWS", or "our CloudWatch Logs bill is too high".
license: MIT
metadata:
  provider: aws
  framework: AWS Well-Architected Framework
  pillars: operational-excellence, security, reliability, performance-efficiency, cost-optimization, sustainability
  category: observability
  status: draft
  last-reviewed: 2026-10-12
  version: 0.1.0
---

# AWS Observability Baseline

Give every account consistent audit logging, threat detection, configuration history and operational monitoring, all centralized and protected and at a sustainable cost.

## When to use

- After the landing zone is created, or when auditing gaps in logging and detection.
- Centralizing CloudWatch across accounts.
- Reducing logging costs.

## When not to use

- Instrumenting application code (tracing and metrics in the app). That belongs to the workload team, though this skill points to the standards.

## Inputs to gather

| Input | Why it matters | Default |
|---|---|---|
| Log retention requirements (audit vs. operational) | S3 lifecycle / Object Lock, CloudWatch retention | Audit 1 year+; operational 30–90 days |
| Governed regions | Where to enable regional services | Same as landing zone |
| SIEM in use? | Export path (S3, Security Lake, Firehose) | None |
| Alert destinations | SNS topics, chat, paging integration | Email + chat |
| Control Tower in place? | It already configures org CloudTrail and Config | Ask |

## Workflow

1. **Assess (read-only).** `aws cloudtrail describe-trails`, `aws configservice describe-configuration-recorders`, `aws guardduty list-detectors`, `aws securityhub describe-hub`, per governed region. Flag gaps.
2. **Audit logging.**
   - Create an **organization trail** (multi-region, including global events) to an S3 bucket in the **Log Archive** account, with SSE-KMS, log file validation enabled, and a bucket policy restricted to CloudTrail and the organization. Consider S3 Object Lock for immutability.
   - Enable data events (S3, Lambda) only where they're needed, because they're priced per event.
3. **Configuration history.** Turn on the **AWS Config** recorder in every account and governed region, with an organization aggregator in the Audit account. Consider periodic recording frequency for high-churn resource types to control cost.
4. **Threat detection and posture.** Use **GuardDuty** and **Security Hub** with **delegated admin** in the Audit or Security Tooling account and auto-enable for new accounts. Enable the Foundational Security Best Practices standard, and use cross-region aggregation in Security Hub.
5. **Network logs.** Send VPC Flow Logs (at least for prod VPCs and the network hub) to S3 in Log Archive, or to CloudWatch Logs with set retention.
6. **Operational monitoring.**
   - Use **CloudWatch cross-account observability** (a monitoring account linked to source accounts through OAM).
   - **Set a retention period on every CloudWatch log group.** The default is never expire.
   - Create alarms on user-facing symptoms (error rates, latency, saturation) with owners and runbooks, and route them through SNS.
   - Send **AWS Health** events to EventBridge rules, then to SNS or chat.
7. **Security alerting.** Use EventBridge rules for high-severity GuardDuty findings and for critical CloudTrail events (root sign-in, CloudTrail stop/delete, SCP changes, IAM policy changes), routed to the security team.
8. **Generate IaC.** Preview it, show the cost drivers (CloudTrail data events, Config items recorded, GuardDuty volume, log ingestion and storage), and **confirm before deploying**.

## Well-Architected alignment

| Pillar | Recommendation | Rationale | Source |
|---|---|---|---|
| Operational Excellence | Cross-account CloudWatch; alarms with runbooks; Health events routed | Teams see and act on issues quickly | https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Unified-Cross-Account.html |
| Security | Org trail to locked-down Log Archive; GuardDuty + Security Hub org-wide; Config history | Complete, tamper-resistant audit and detection | https://docs.aws.amazon.com/awscloudtrail/latest/userguide/creating-trail-organization.html |
| Reliability | Alarms on symptoms; AWS Health notifications; Config for change correlation | Faster detection and diagnosis | https://docs.aws.amazon.com/health/latest/ug/cloudwatch-events-health.html |
| Performance Efficiency | Metrics and Container/Lambda Insights where needed; dashboards per workload | Spot saturation before users do | https://aws-observability.github.io/observability-best-practices/ |
| Cost Optimization | Log retention on every group; S3 lifecycle to cheaper tiers; selective data events; Config recording frequency | Logging cost grows silently | https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html |
| Sustainability | Store only needed logs; tier and expire data | Less stored data, less energy | https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sustainability-pillar.html |

**Trade-offs:** Full data events and continuous Config recording give maximum visibility at a significant cost. Enable them for sensitive workloads first. Long immutable retention helps compliance but makes mistaken data impossible to delete.

## Guardrails

- Never disable, delete or shorten the retention of audit trails or Config recorders without explicit confirmation.
- Don't enable S3 Object Lock in compliance mode without explicit approval, because it can't be undone during the retention period.
- Log Archive bucket access is read-only for security, with no write or delete for humans.
- Don't route security findings to public or unsecured channels.

## Validation

- `aws cloudtrail get-trail-status --name <org-trail>` shows `IsLogging: true`. Logs appear in Log Archive for a test account.
- `aws guardduty list-members` from the delegated admin includes all accounts.
- `aws logs describe-log-groups --query "logGroups[?retentionInDays==null].logGroupName"` returns nothing.
- Trigger a test alarm and a GuardDuty sample finding (`create-sample-findings`) in a test account, **with confirmation**, to verify routing.

## Common mistakes

- Log groups with no retention ("never expire").
- Enabling GuardDuty or Config only in the home region.
- Letting workload accounts' admins modify the org trail or the Log Archive bucket.

## Related skills

- `aws-landing-zone`, `aws-network-hub`, `aws-well-architected-review`

## References

- Creating a trail for an organization: https://docs.aws.amazon.com/awscloudtrail/latest/userguide/creating-trail-organization.html
- AWS Config multi-account aggregation: https://docs.aws.amazon.com/config/latest/developerguide/aggregate-data.html
- GuardDuty with Organizations: https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_organizations.html
- CloudWatch cross-account observability: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Unified-Cross-Account.html
- VPC Flow Logs: https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html
- AWS Observability Best Practices: https://aws-observability.github.io/observability-best-practices/
