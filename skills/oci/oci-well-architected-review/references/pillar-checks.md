# Baseline checks per area (OCI)

## Security and Compliance
- No workloads in the root compartment. Compartments separate network, security, app and database.
- Only the tenancy Administrators group has `manage all-resources in tenancy`. Every other policy is compartment-scoped with the least verb (inspect < read < use < manage).
- MFA is enforced for all console users. API keys and auth tokens are rotated, and the tenancy admin isn't used day to day.
- Workloads use instance, resource or workload principals (dynamic groups), not user API keys.
- Cloud Guard is enabled with detector and responder recipes, and Security Zones protect sensitive compartments.
- Vault customer-managed keys are used where required.
- Object Storage buckets aren't public. No security list or NSG allows `0.0.0.0/0` on 22 or 3389.

## Reliability and Resilience
- Production spans fault domains, and availability domains where the region has more than one.
- Backups exist for block volumes, databases and object storage (replication or versioning), and restores have been tested.
- Cross-region DR (Full Stack DR, Data Guard) matches the RTO/RPO.
- Service limits are monitored.

## Performance and Cost Optimization
- Flexible shapes are right-sized, and autoscaling is configured.
- Budgets and alerts are set per compartment, and cost-tracking tags are defined.
- No idle or unattached resources. Object Storage uses the right tier and lifecycle policies.

## Operational Efficiency
- Infrastructure is defined in Terraform or Resource Manager.
- Monitoring alarms go to Notifications topics with owners.
- Service logs are enabled and routed with Connector Hub.
- Events rules cover critical IAM and network changes, as the CIS Benchmark recommends.
