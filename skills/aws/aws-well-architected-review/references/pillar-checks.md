# Baseline checks per pillar (AWS)

Always run these. Add lens- and service-specific checks as needed.

## Operational Excellence
- Infrastructure is defined in IaC (CloudFormation, CDK or Terraform) and deployed via a pipeline.
- Deployments are safe: canary or blue-green with automatic rollback.
- Runbooks and playbooks exist, and dashboards and alarms have owners.

## Security
- The root user has MFA and no access keys. Use centralized root access management in Organizations where it's available.
- Humans sign in through IAM Identity Center. There are no IAM users with long-term access keys.
- CloudTrail is enabled organization-wide. GuardDuty, Security Hub and Config are enabled in all used regions.
- S3 Block Public Access is on at account level, and storage and databases are encrypted with KMS.
- Security groups allow no `0.0.0.0/0` inbound on admin ports. Use SSM Session Manager instead of SSH bastions.
- Secrets live in Secrets Manager or Parameter Store (SecureString), not in code or environment files.

## Reliability
- Production uses Multi-AZ for databases, load-balanced compute and NAT gateways.
- AWS Backup plans exist and restores have been tested.
- Service quotas are monitored.
- The DR strategy (backup/restore, pilot light, warm standby, multi-site) matches the RTO/RPO.

## Performance Efficiency
- Auto Scaling is configured. Instance families are current-generation, and Graviton is evaluated.
- Caching (CloudFront, ElastiCache) is used where it fits.
- Load tests are part of releases.

## Cost Optimization
- Cost allocation tags are activated, AWS Budgets and Cost Anomaly Detection are configured.
- No idle resources: unattached EBS volumes, idle load balancers, unused Elastic IPs, old snapshots.
- Savings Plans or Reserved Instances cover steady usage, and S3 lifecycle or Intelligent-Tiering is in place.

## Sustainability
- Utilization targets are defined, and managed or serverless services are preferred where they fit.
- Data has lifecycle and retention policies, and non-prod is scheduled off outside working hours.
