---
name: oci-hub-spoke-network
description: Design OCI hub-and-spoke networking with a Dynamic Routing Gateway (DRG) — VCN CIDR planning, hub VCN with OCI Network Firewall, DRG route tables and import distributions, spoke VCN attachments, NAT and Service Gateways, Network Security Groups, private DNS, and hybrid connectivity via FastConnect or Site-to-Site VPN, plus remote peering across regions. Use when the user says "set up hub and spoke in OCI", "design our Oracle Cloud network", "DRG routing", "connect on-prem to OCI with FastConnect", "centralize firewall in OCI", or "plan VCN CIDRs".
license: MIT
metadata:
  provider: oci
  framework: Well-Architected Framework for OCI
  pillars: security-compliance, reliability-resilience, performance-cost, operational-efficiency
  category: networking
  status: draft
  last-reviewed: 2026-10-12
  version: 0.1.0
---

# OCI Hub-and-Spoke Network

Use the DRG as the central router, with a hub VCN for shared inspection and connectivity and spoke VCNs for workloads. This follows OCI Architecture Center hub-and-spoke reference architectures.

## When to use

- Several VCNs need shared hybrid connectivity, inspection or egress.
- Connecting on-premises networks or other regions to OCI.

## When not to use

- A single VCN for a single workload.
- Compartment and tenancy design: use `oci-landing-zone`.

## Inputs to gather

| Input | Why it matters | Default |
|---|---|---|
| Regions | DRG per region; remote peering across regions | Ask (required) |
| On-prem connectivity (none / Site-to-Site VPN / FastConnect) and on-prem CIDRs | Non-overlapping plan, redundancy | None |
| Number of spoke VCNs | CIDR plan and DRG route table design | ≤ 20 |
| Inspection needs (north-south, east-west) | Network Firewall placement and routing | Both for prod |
| Internet-facing workloads? | DMZ/ingress design | Ask |

## Workflow

1. **IP plan.** Use non-overlapping VCN CIDRs per region and environment, excluding on-prem ranges, with room for growth. Use regional subnets (rather than AD-specific ones) unless there's a specific need. Produce an IP plan table.
2. **DRG.** Create one DRG per region in the network compartment, and attach the hub VCN and each spoke VCN (DRG v2 attachments).
3. **Hub VCN.**
   - **OCI Network Firewall** in a dedicated subnet, with a firewall policy managed as code.
   - **NAT Gateway** for private egress.
   - **Service Gateway** for private access to the Oracle Services Network (Object Storage and similar).
   - An Internet Gateway only in a dedicated ingress or DMZ subnet, if public ingress is needed.
4. **Routing for inspection.**
   - Add a DRG route table for spoke attachments that sends `0.0.0.0/0` and the other spokes' prefixes to the hub VCN attachment.
   - On the hub VCN attachment, use a VCN route table (ingress routing) that steers traffic to the firewall's private IP.
   - Use a separate DRG route table for the hub attachment, with import distributions that learn the spoke routes.
   - Document every route table. Asymmetric routing is the most common failure.
5. **Spokes.** Use private subnets only, with route rules sending everything to the DRG. Use **NSGs** (preferred over security lists) per application tier, with least-privilege rules between NSGs.
6. **Hybrid.** Use **FastConnect** (redundant virtual circuits across locations for prod) and/or **Site-to-Site VPN** as backup, attached to the DRG. Use BGP where possible.
7. **Cross-region.** Use **remote peering connections** between DRGs for DR or multi-region designs.
8. **DNS.** Use the VCN resolver with private views, and forwarding and listening endpoints for hybrid resolution.
9. **Logging.** Enable VCN Flow Logs on the hub and the critical spokes, and route the firewall logs to the logging compartment.
10. **Generate Terraform** (OCI Landing Zones networking modules, or the official provider resources). Run `terraform plan`, present the resources and cost drivers (Network Firewall, FastConnect ports, outbound data transfer), and **confirm before applying**.

## Well-Architected alignment

| Area | Recommendation | Rationale | Source |
|---|---|---|---|
| Security and Compliance | Central Network Firewall; private spokes; NSGs with least privilege; Bastion service for admin; flow logs | Controlled, inspected traffic and minimal exposure | https://docs.oracle.com/en-us/iaas/Content/network-firewall/home.htm |
| Reliability and Resilience | Redundant FastConnect/VPN; regional subnets; remote peering for DR | No single connectivity failure point | https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/fastconnect.htm |
| Performance and Cost Optimization | Service Gateway for OSN traffic; size firewall to throughput; review outbound transfer | Avoid unnecessary internet egress and bottlenecks | https://docs.oracle.com/en-us/iaas/Content/Network/Tasks/servicegateway.htm |
| Operational Efficiency | DRG route tables and firewall policy as code; documented IP plan | Predictable routing changes | https://docs.oracle.com/en-us/iaas/Content/Network/Tasks/managingDRGs.htm |

**Trade-offs:** Routing all east-west traffic through the firewall improves inspection but adds latency, cost and a dependency. Allow direct spoke-to-spoke traffic only where the risk is accepted. Security lists are simpler, but NSGs give finer per-resource control.

## Guardrails

- Never overlap CIDRs.
- Changing DRG or VCN route tables or firewall policies on live networks can black-hole traffic. Present the impact and **require confirmation**.
- Don't allow `0.0.0.0/0` ingress on administrative ports. Use the Bastion service.
- Don't store VPN shared secrets in Terraform plain text. Use Vault secrets or sensitive variables.

## Validation

- `terraform plan` reviewed.
- Network Path Analyzer confirms that spoke → internet, spoke → on-prem and spoke → spoke paths traverse the firewall as intended.
- Flow logs show traffic hitting the expected firewall subnet.

## Common mistakes

- Missing ingress route table on the hub VCN attachment, so traffic bypasses the firewall.
- Using the Internet Gateway in spokes for convenience.
- Single FastConnect virtual circuit for production.

## Related skills

- `oci-landing-zone`, `oci-observability-baseline`, `oci-well-architected-review`

## References

- Networking overview: https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/overview.htm
- Dynamic Routing Gateways: https://docs.oracle.com/en-us/iaas/Content/Network/Tasks/managingDRGs.htm
- OCI Network Firewall: https://docs.oracle.com/en-us/iaas/Content/network-firewall/home.htm
- Network Security Groups: https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/networksecuritygroups.htm
- Service Gateway: https://docs.oracle.com/en-us/iaas/Content/Network/Tasks/servicegateway.htm
- OCI Architecture Center: https://docs.oracle.com/solutions/
