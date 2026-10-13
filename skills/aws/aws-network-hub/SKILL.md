---
name: aws-network-hub
description: Design centralized multi-VPC networking on AWS — IP planning with VPC IPAM, AWS Transit Gateway hub (or Cloud WAN for global networks), centralized egress via NAT gateways, centralized inspection with AWS Network Firewall, shared interface VPC endpoints, Route 53 Resolver for hybrid DNS, and Direct Connect/Site-to-Site VPN — shared to workload accounts with AWS RAM. Use when the user says "set up Transit Gateway", "design our AWS network", "centralize egress in AWS", "connect on-prem to AWS", "share VPC endpoints across accounts", or "Transit Gateway vs Cloud WAN".
license: MIT
metadata:
  provider: aws
  framework: AWS Well-Architected Framework
  pillars: operational-excellence, security, reliability, performance-efficiency, cost-optimization, sustainability
  category: networking
  status: draft
  last-reviewed: 2026-10-12
  version: 0.1.0
---

# AWS Network Hub

Design a scalable, secure multi-VPC network owned by a central **Network account**, following the AWS whitepaper *Building a Scalable and Secure Multi-VPC AWS Network Infrastructure*.

## When to use

- A multi-account organization needs VPC-to-VPC, hybrid or centralized egress connectivity.
- Adding inspection, shared endpoints or hybrid DNS.

## When not to use

- A single VPC for a single workload. Use the workload's own IaC with Multi-AZ subnets; this hub pattern is overkill.
- Organization and account design: use `aws-landing-zone`.

## Inputs to gather

| Input | Why it matters | Default |
|---|---|---|
| Regions in use | One Transit Gateway per region; peering or Cloud WAN across regions | Ask (required) |
| On-prem connectivity (Direct Connect / VPN / none) and on-prem CIDRs | Attachment type, non-overlapping IP plan | None |
| Number of VPCs expected | TGW vs. Cloud WAN; route table design | ≤ 50 per region |
| Inspection needs (egress only / east-west / ingress) | Network Firewall placement | Egress + east-west for prod |
| Environment segmentation (prod / non-prod isolated?) | TGW route table segmentation | Isolated |

## Workflow

1. **Choose the topology.**
   - Use **Transit Gateway** for hub-and-spoke within a region, with TGW peering for a few regions.
   - Use **AWS Cloud WAN** for many regions or a global network with central policy-based segmentation.
   - Use plain **VPC peering** only for a few VPCs with no transitive needs.
2. **Plan IP addressing with VPC IPAM.** Create pools per region and environment, with non-overlapping and summarizable CIDRs. Exclude on-prem ranges. Share the pools via RAM so workload accounts allocate from them.
3. **Transit Gateway.** Create it in the Network account and share it to the organization or specific OUs through **AWS RAM**. Disable default route table association and propagation. Create segmented route tables (for example `prod`, `nonprod`, `shared`, `inspection`) so prod and non-prod can't route to each other unless that's intended.
4. **Centralized egress.** Create an egress VPC with NAT gateways in **each AZ**. Spoke default routes go to the TGW, which sends them to the egress VPC. This removes NAT gateways from every spoke. Note the TGW data-processing cost trade-off.
5. **Inspection.** Create an inspection VPC with **AWS Network Firewall** endpoints per AZ. **Enable appliance mode** on the inspection VPC's TGW attachment for symmetric routing. Route east-west and egress traffic through it as required.
6. **Shared endpoints.** Put centralized interface VPC endpoints (for example for SSM, STS, ECR, Logs) in a shared-services VPC, with Route 53 private hosted zones associated to the spokes. Use **gateway endpoints** for S3 and DynamoDB in each VPC, because they're free.
7. **Hybrid DNS.** Create Route 53 Resolver inbound and outbound endpoints in the shared VPC, with forwarding rules shared via RAM.
8. **Hybrid connectivity.** Attach Direct Connect (via a DX gateway) or Site-to-Site VPN to the TGW. For critical links, use redundant connections or locations, or VPN as a backup to DX.
9. **Spoke VPC baseline.** Use private subnets across at least two AZs (three for prod), with no internet gateway unless the VPC is an ingress VPC. Enable VPC Flow Logs to the central logging destination.
10. **Generate IaC.** Preview it with a plan or change set, present the resources and cost drivers (TGW attachment hours and data processing, NAT, Network Firewall endpoints, interface endpoints), and **confirm before deploying**.

## Well-Architected alignment

| Pillar | Recommendation | Rationale | Source |
|---|---|---|---|
| Operational Excellence | Network account owns shared networking; IPAM; everything as IaC; flow logs centralized | Consistent, auditable network changes | https://docs.aws.amazon.com/whitepapers/latest/building-scalable-secure-multi-vpc-network-infrastructure/welcome.html |
| Security | Segmented TGW route tables; centralized inspection; no IGW in spokes; private endpoints | Limit lateral movement and exposure | https://docs.aws.amazon.com/network-firewall/latest/developerguide/what-is-aws-network-firewall.html |
| Reliability | Per-AZ NAT and firewall endpoints; appliance mode; redundant DX/VPN | Avoid AZ-level single points of failure and asymmetric routing | https://docs.aws.amazon.com/vpc/latest/tgw/tgw-best-design-practices.html |
| Performance Efficiency | Keep traffic in-region and in-AZ where possible; Cloud WAN for global scale | Reduce latency and cross-AZ hops | https://docs.aws.amazon.com/network-manager/latest/cloudwan/what-is-cloudwan.html |
| Cost Optimization | Centralize NAT/endpoints where TGW processing costs < per-VPC duplication; use free gateway endpoints for S3/DynamoDB | Network data charges add up quietly | https://docs.aws.amazon.com/whitepapers/latest/building-scalable-secure-multi-vpc-network-infrastructure/centralized-egress-to-internet.html |
| Sustainability | Share network appliances across workloads rather than duplicating | Fewer idle resources | https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sustainability-pillar.html |

**Trade-offs:** Centralized egress and inspection improve control but add TGW data-processing charges and a shared dependency. For very high-throughput workloads, local NAT can be cheaper. Fine-grained segmentation improves security but makes routing more complex to operate.

## Guardrails

- Never overlap CIDRs. Validate against IPAM and on-prem ranges first.
- Changing TGW route tables, associations or propagation on live networks can black-hole traffic. Present the impact and **require confirmation**.
- Don't add `0.0.0.0/0` inbound security group rules. Use SSM Session Manager for administrative access.
- Only share resources through RAM with the intended OUs or accounts, never publicly.

## Validation

- `aws ec2 search-transit-gateway-routes` confirms the expected routes per route table.
- VPC Reachability Analyzer path from a spoke to the internet and to on-prem passes through the intended firewall.
- DNS from a spoke resolves shared endpoint names to private IPs.

## Common mistakes

- Leaving the TGW default route table association on, which joins everything into one flat network.
- Forgetting appliance mode on the inspection VPC attachment, which causes asymmetric flows and dropped traffic.
- Running a NAT gateway in only one AZ for prod.
- Paying for interface endpoints for S3 traffic that a free gateway endpoint could carry.

## Related skills

- `aws-landing-zone`, `aws-observability-baseline`, `aws-well-architected-review`

## References

- Building a scalable and secure multi-VPC AWS network infrastructure: https://docs.aws.amazon.com/whitepapers/latest/building-scalable-secure-multi-vpc-network-infrastructure/welcome.html
- Transit Gateway: https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html
- Transit Gateway design best practices: https://docs.aws.amazon.com/vpc/latest/tgw/tgw-best-design-practices.html
- VPC IPAM: https://docs.aws.amazon.com/vpc/latest/ipam/what-it-is-ipam.html
- AWS Network Firewall: https://docs.aws.amazon.com/network-firewall/latest/developerguide/what-is-aws-network-firewall.html
- Route 53 Resolver: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver.html
- AWS Cloud WAN: https://docs.aws.amazon.com/network-manager/latest/cloudwan/what-is-cloudwan.html
