# Baseline checks per pillar

These are the checks the review **always** runs. Add service-specific checks from the matching WAF service guide (https://learn.microsoft.com/azure/well-architected/service-guides/).

## Reliability (RE)

- Reliability targets (SLO, RTO, RPO) are defined and documented.
- Production compute and data services use availability zones where the region and SKU support them.
- Stateful data has backups, and restores have been **tested**.
- Health probes and endpoints exist for load-balanced or front-door-routed services.
- No single points of failure: single-instance VMs, a single gateway, a non-redundant SKU in prod.
- Multi-region or DR design matches the RTO/RPO; it isn't required by default.
- Retry and timeout patterns exist for dependencies (check in app or design).

## Security (SE)

- Microsoft Entra ID authentication is used. Local auth and shared keys are disabled where the service supports it.
- Managed identities are used for service-to-service access.
- RBAC follows least privilege. Flag Owner or Contributor assignments at subscription scope and direct user assignments instead of groups.
- Public network access is disabled, or justified and restricted (private endpoints, firewalls, NSGs).
- Storage blocks anonymous or public blob access, and TLS 1.2 or later is enforced.
- Secrets live in Key Vault, with soft delete and purge protection enabled. No secrets in IaC or app settings.
- Microsoft Defender for Cloud plans are enabled for the workload's resource types.
- Diagnostic and audit logs go to a central Log Analytics workspace.

## Cost Optimization (CO)

- Resources are tagged for cost allocation (for example owner, environment, cost-center).
- Budgets and alerts are configured.
- No orphaned resources: unattached disks, unassociated public IPs, empty App Service plans, idle gateways.
- SKUs are right-sized against utilization, and dev/test uses lower tiers or auto-shutdown.
- Reservations or savings plans are evaluated for steady-state usage.

## Operational Excellence (OE)

- Infrastructure is defined in IaC and deployed through a pipeline, with no ClickOps drift.
- Safe deployment practices are in place: staged rollout, slots or blue-green, and rollback.
- Monitoring covers metrics, logs and actionable alerts with owners.
- Diagnostic settings are enabled on key resources.
- Runbooks or playbooks exist for common incidents.

## Performance Efficiency (PE)

- Performance targets are defined (latency, throughput).
- Autoscale is configured for variable load.
- Caching or a CDN is used where it fits.
- Load or performance testing is part of the release process.
- Data store tier and partitioning fit the access patterns.
