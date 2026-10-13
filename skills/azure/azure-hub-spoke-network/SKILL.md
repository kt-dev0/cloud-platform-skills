---
name: azure-hub-spoke-network
description: Design and build Azure hub-and-spoke networking (or decide on Virtual WAN instead) — IP address planning, hub VNet with Azure Firewall, VPN/ExpressRoute gateways and Bastion, spoke peering, user-defined routes, and centralized Private DNS for private endpoints — with Bicep or Terraform using Azure Verified Modules. Use when the user says "set up hub and spoke in Azure", "design our Azure network", "connect on-prem to Azure", "plan VNet address space", "private endpoint DNS isn't resolving", or "hub-spoke vs Virtual WAN".
license: MIT
metadata:
  provider: azure
  framework: Azure Well-Architected Framework
  pillars: reliability, security, cost-optimization, operational-excellence, performance-efficiency
  category: networking
  status: draft
  last-reviewed: 2026-10-12
  version: 0.1.0
---

# Azure Hub-and-Spoke Network

Design a hub-and-spoke network in the Connectivity subscription that centralizes shared services (firewall, gateways, DNS, Bastion) and isolates workloads in peered spoke VNets. Follows the Azure Architecture Center reference architecture.

## When to use

- Designing or extending the network for an Azure landing zone.
- Connecting on-premises to Azure, or centralizing egress inspection.
- Fixing private endpoint DNS resolution across VNets.

## When not to use

- Management group or subscription design: use `azure-landing-zone`.
- Workload-internal subnet design for one app only: handle that in the workload's own IaC.

## Inputs to gather

| Input | Why it matters | Default |
|---|---|---|
| Regions | One hub per region | Ask (required) |
| On-prem connectivity: none / site-to-site VPN / ExpressRoute | Gateway type and SKU | None |
| Existing on-prem and cloud CIDR ranges | Avoid overlaps (peering requires non-overlapping space) | Ask (required if hybrid) |
| Expected number of spokes in 3 years | Address space sizing; Virtual WAN vs. hub-spoke | ≤ 50 |
| Egress inspection required? | Azure Firewall SKU (Standard vs. Premium) | Yes, Standard |
| Environment criticality | Zone redundancy, DDoS Network Protection | prod |

## Workflow

1. **Choose the topology.**
   - Choose **customer-managed hub-and-spoke** when you need full control of routing and NVAs, or when the estate has one or two regions.
   - Choose **Azure Virtual WAN** when there are many regions or branches, large-scale any-to-any connectivity, or SD-WAN integration. Explain the trade-off and stop here if Virtual WAN is chosen; this skill covers hub-and-spoke.
2. **Plan IP addressing.** Allocate a summarizable block per region (for example a /16), carve a /22–/23 hub and /24-sized or larger spokes. Reserve space for growth. Never overlap with on-premises ranges. Produce an IP plan table.
3. **Design the hub VNet subnets** (the names are mandatory where noted):
   - `AzureFirewallSubnet`: /26
   - `GatewaySubnet`: /27 or larger (use /26 if ExpressRoute and VPN coexist)
   - `AzureBastionSubnet`: /26 or larger
   - An optional DNS Private Resolver inbound/outbound subnets (/28 each, delegated)
4. **Hub services.**
   - Azure Firewall (zone-redundant) with a Firewall Policy. Use Premium if TLS inspection or IDPS is required.
   - VPN or ExpressRoute gateway using an availability-zone SKU, if hybrid connectivity is needed.
   - Azure Bastion for administrative access. Don't put public IPs on VMs.
   - DDoS Network Protection for production public endpoints. State the cost.
5. **Spokes.** Peer each spoke to the hub. Enable *use remote gateways* on the spoke and *allow gateway transit* on the hub when gateways exist. Peering is **not transitive**, so spoke-to-spoke traffic goes through the firewall using UDRs.
6. **Routing.** Add a route table on each spoke subnet with `0.0.0.0/0 → firewall private IP`, and routes for other spokes' prefixes through the firewall. Disable gateway route propagation on spoke route tables so traffic is forced through the firewall when hybrid exists.
7. **DNS.** Centralize the `privatelink.*` Private DNS zones in the Connectivity subscription and link them to the hub (and to the spokes, or resolve through the DNS Private Resolver). For hybrid, set up conditional forwarders on-prem → resolver inbound endpoint. Use Azure Policy (DeployIfNotExists) to auto-register private endpoint DNS records.
8. **Network security.** Put NSGs on every spoke subnet (except where they aren't supported) with a deny-by-default posture, and enable VNet flow logs to the central workspace.
9. **Generate IaC** with Azure Verified Modules (hub networking and virtual network modules), parameterized per region. Run a preview, then present the resources and their monthly cost drivers (firewall, gateways, Bastion, DDoS) and **get confirmation before deploying**.

## Well-Architected alignment

| Pillar | Recommendation | Rationale | Source |
|---|---|---|---|
| Reliability | Zone-redundant firewall and gateways; active-active VPN gateways for critical hybrid links | Hub is a shared dependency for all spokes | https://learn.microsoft.com/azure/well-architected/service-guides/azure-firewall |
| Security | Default route through Azure Firewall; NSGs on spokes; no public IPs on VMs; Bastion for admin; private endpoints + central DNS | Centralized inspection, minimal exposure | https://learn.microsoft.com/azure/architecture/networking/architecture/hub-spoke |
| Cost Optimization | Share firewall/gateways across spokes; right-size firewall SKU; evaluate Basic SKUs for small/non-prod hubs; note peering data-transfer charges | Hub cost is fixed per region | https://learn.microsoft.com/azure/virtual-network/virtual-network-peering-overview |
| Operational Excellence | IP plan as code; firewall policy as code; flow logs + firewall logs to Log Analytics | Traceable network changes, faster troubleshooting | https://learn.microsoft.com/azure/cloud-adoption-framework/ready/azure-best-practices/define-an-azure-network-topology |
| Performance Efficiency | Place hubs in the same region as spokes; choose gateway SKU by throughput; consider Virtual WAN at large scale | Avoid cross-region hairpinning and gateway bottlenecks | https://learn.microsoft.com/azure/virtual-wan/virtual-wan-about |

**Trade-offs:** Forcing all traffic through the firewall improves security and visibility but adds latency, cost and a scaling dependency. Premium firewall features (TLS inspection) carry a cost and add certificate operations. A single shared hub is cheaper than a hub per environment but couples prod and non-prod routing. Decide this explicitly.

## Guardrails

- Never overlap address spaces. Validate the IP plan against the on-prem ranges before generating IaC.
- Don't open inbound management ports (22, 3389) from the internet. Use Bastion or just-in-time access.
- Changing route tables or peering on live networks can cause outages. Present the impact and **require confirmation**, ideally inside a change window.
- No shared keys in IaC for VPN connections. Reference Key Vault secrets.

## Validation

- `az deployment group what-if` / `terraform plan` reviewed.
- After deployment: `az network watcher show-next-hop` from a spoke VM confirms the firewall is the next hop, and `nslookup <resource>.privatelink...` from a spoke returns a private IP.
- Firewall logs show the expected allowed and denied flows.

## Common mistakes

- Sizing the address space too small. Re-addressing later is very disruptive.
- Creating Private DNS zones per spoke, which breaks resolution across spokes. Centralize them.
- Forgetting to disable gateway route propagation on spokes, which lets traffic bypass the firewall to on-prem.
- Expecting transitive peering between spokes.

## Related skills

- `azure-landing-zone`: Connectivity subscription placement
- `azure-policy-governance`: policies for private DNS zone registration and denying public IPs
- `azure-monitoring-baseline`: network logs and alerts

## References

- Hub-spoke network topology in Azure: https://learn.microsoft.com/azure/architecture/networking/architecture/hub-spoke
- Define an Azure network topology: https://learn.microsoft.com/azure/cloud-adoption-framework/ready/azure-best-practices/define-an-azure-network-topology
- Private endpoint DNS: https://learn.microsoft.com/azure/private-link/private-endpoint-dns
- Private Link and DNS integration at scale: https://learn.microsoft.com/azure/cloud-adoption-framework/ready/azure-best-practices/private-link-and-dns-integration-at-scale
- Azure Firewall service guide: https://learn.microsoft.com/azure/well-architected/service-guides/azure-firewall
- Azure Virtual WAN: https://learn.microsoft.com/azure/virtual-wan/virtual-wan-about
