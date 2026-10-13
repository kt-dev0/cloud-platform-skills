# Baseline checks per pillar (Google Cloud)

## Operational Excellence
- Infrastructure is defined in Terraform (or Config Connector) and deployed via a pipeline.
- SLOs are defined in Cloud Monitoring, and alerting policies have notification channels and owners.
- Incident and postmortem process is documented.

## Security, Privacy and Compliance
- Projects live under folders with org policies inherited. No projects sit directly under "No organization".
- No basic roles (`roles/owner`, `roles/editor`) granted to humans in prod. Access is granted to groups.
- Service account key creation is disabled (`iam.disableServiceAccountKeyCreation`), and workloads use attached service accounts or Workload Identity Federation.
- Domain restricted sharing is on (`iam.allowedPolicyMemberDomains`) and the resource locations constraint is set where needed.
- Public exposure is controlled: no external IPs on VMs unless they're needed (`compute.vmExternalIpAccess`), uniform bucket-level access is on, and public access prevention is enforced.
- Data Access audit logs are enabled for sensitive services, and VPC Service Controls protect sensitive data perimeters.

## Reliability
- Production uses regional or multi-zonal resources (regional MIGs, regional GKE, Cloud SQL HA).
- Backups exist and restores have been tested. Quotas are monitored.
- The DR plan matches the RTO/RPO.

## Cost Optimization
- Labels are applied for cost allocation, budgets and alerts are configured, and billing export to BigQuery is on.
- Recommender idle-resource and right-sizing findings have been reviewed.
- Committed use discounts cover steady usage.
- Storage classes and lifecycle rules are in place.

## Performance Optimization
- Autoscaling is configured, and machine families fit the workload.
- Cloud CDN or caching is used where appropriate.
- Load tests are part of releases.

## Sustainability
- Region choice considers the carbon-free energy data, as long as it doesn't break latency or residency requirements.
- Idle resources are removed, and non-prod is scheduled off.
