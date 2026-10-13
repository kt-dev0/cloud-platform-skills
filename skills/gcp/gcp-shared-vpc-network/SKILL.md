---
name: gcp-shared-vpc-network
description: Design Google Cloud networking with Shared VPC — host and service projects per environment, custom-mode VPCs and subnet IP planning (including GKE secondary ranges), hierarchical and network firewall policies, Cloud NAT, Private Google Access and Private Service Connect, Cloud DNS, and hybrid connectivity via HA VPN or Cloud Interconnect, optionally connected with Network Connectivity Center. Use when the user says "set up Shared VPC", "design our GCP network", "connect on-prem to Google Cloud", "plan GKE IP ranges", "centralize firewall rules in GCP", or "private access to Google APIs".
license: MIT
metadata:
  provider: gcp
  framework: Google Cloud Well-Architected Framework
  pillars: operational-excellence, security, reliability, cost-optimization, performance-optimization, sustainability
  category: networking
  status: draft
  last-reviewed: 2026-10-12
  version: 0.1.0
---

# Google Cloud Shared VPC Network

Centralize network administration in host projects while workload teams deploy into service projects. This follows Google's VPC design best practices and the landing zone network design guidance.

## When to use

- Designing the network for a Google Cloud landing zone.
- Adding hybrid connectivity, private service access, or centralized firewalling.

## When not to use

- A single standalone project with no shared-network needs.
- Organization and folder design: use `gcp-landing-zone`.

## Inputs to gather

| Input | Why it matters | Default |
|---|---|---|
| Environments to isolate | One host project (Shared VPC) per environment | prod, nonprod |
| Regions | Subnets are regional; Cloud Router/NAT per region | Ask (required) |
| On-prem connectivity (none / HA VPN / Dedicated or Partner Interconnect) and on-prem CIDRs | Non-overlapping plan, redundancy | None |
| GKE usage and expected scale | Secondary ranges for pods/services | Ask |
| Need for central inspection (NVA) | Hub-and-spoke with NCC or NVAs vs. simple Shared VPC | No |
| Sensitive data perimeters | VPC Service Controls | Ask |

## Workflow

1. **Choose the topology.**
   - **Shared VPC per environment** (recommended baseline): simple and centrally governed.
   - **Hub-and-spoke**: a hub VPC for hybrid and shared services, with spoke Shared VPCs connected using **Network Connectivity Center** VPC spokes or VPC Network Peering. Choose it when many VPCs need shared hybrid access or central NVAs.
2. **IP plan.** Use custom-mode VPCs only (no auto-mode). Allocate non-overlapping regional subnets, and size secondary ranges for GKE pods and services generously. Exclude on-prem ranges. Produce an IP plan table.
3. **Host and service projects.** Enable Shared VPC on the host project, attach service projects, and grant `roles/compute.networkUser` **at subnet level** to the service project's groups and service accounts (not at host-project level).
4. **Firewalling.**
   - Use **hierarchical firewall policies** at organization or folder level for org-wide rules (for example allow IAP ranges for admin access, deny known-bad traffic).
   - Use **global network firewall policies** in host projects for VPC rules, targeting secure tags or service accounts rather than network tags.
   - Default to denying ingress. Log firewall rules on sensitive paths.
5. **Egress and private access.**
   - Use **Cloud NAT** per region (with Cloud Router) for private VMs that need internet egress.
   - Turn on **Private Google Access** on subnets.
   - Use **Private Service Connect** for Google APIs and published services where it fits, with the matching Cloud DNS zones.
6. **Admin access.** Use Identity-Aware Proxy TCP forwarding instead of public IPs or bastions with external IPs.
7. **DNS.** Use Cloud DNS private zones in the host project, DNS peering or forwarding for hybrid, and inbound server policies for on-prem → GCP resolution.
8. **Hybrid connectivity.** Use **HA VPN** (99.99% SLA configuration needs two tunnels to a properly configured peer) or redundant **Interconnect** VLAN attachments across edge availability domains. Advertise routes with Cloud Router.
9. **Data perimeters.** For sensitive data, add **VPC Service Controls** perimeters around projects with sensitive APIs, starting in dry-run mode.
10. **Generate Terraform.** Use the Google-maintained network modules or the networks stage of the foundation blueprint. Run `terraform plan`, present the resources and cost drivers (NAT, Interconnect, VPN, egress, NVAs), and **confirm before applying**.

## Well-Architected alignment

| Pillar | Recommendation | Rationale | Source |
|---|---|---|---|
| Operational Excellence | Centralized network admin in host projects; network as Terraform; subnet-level IAM | Clear ownership, fewer misconfigurations | https://cloud.google.com/vpc/docs/shared-vpc |
| Security, Privacy and Compliance | Hierarchical firewall policies; no external IPs; IAP for admin; VPC Service Controls for sensitive data | Defense in depth, exfiltration protection | https://cloud.google.com/firewall/docs/firewall-policies-overview |
| Reliability | HA VPN / redundant Interconnect; regional NAT per region; multi-zone workloads | Avoid single points of failure in connectivity | https://cloud.google.com/network-connectivity/docs/vpn/concepts/topologies |
| Cost Optimization | Minimize cross-region and internet egress; right-size Interconnect; avoid unnecessary NVAs | Network egress is a top cost driver | https://cloud.google.com/vpc/network-pricing |
| Performance Optimization | Regional placement; Premium vs. Standard network tier decision; sufficient GKE ranges | Latency and scale headroom | https://cloud.google.com/architecture/best-practices-vpc-design |
| Sustainability | Share network infrastructure across teams; avoid idle NVAs/VPN tunnels | Less duplicated, idle infrastructure | https://cloud.google.com/architecture/framework/sustainability |

**Trade-offs:** A Shared VPC per environment is simple, but very large organizations may hit per-VPC limits and need hub-and-spoke. Central NVAs add inspection at the cost of complexity and throughput limits. VPC Service Controls are powerful, but they break access patterns that haven't been mapped, so always use dry-run first.

## Guardrails

- Never overlap CIDRs, and never use auto-mode VPCs in production.
- Changing firewall policies, routes or Cloud Router advertisements on live networks can cause outages. Present the impact and **require confirmation**.
- Enforcing a VPC Service Controls perimeter (moving it out of dry-run) needs explicit confirmation after reviewing the dry-run violations.
- Don't grant `compute.networkUser` at host-project level when subnet level is enough.

## Validation

- `terraform plan` reviewed.
- Connectivity Tests (Network Intelligence Center) confirm the intended paths from service-project VMs to on-prem, the internet (through NAT) and Google APIs.
- `gcloud compute networks subnets list-usable --project=<service-project>` shows only the intended subnets.

## Common mistakes

- Undersized GKE secondary ranges.
- Granting network admin to app teams instead of `networkUser` on specific subnets.
- Leaving the default network in host or service projects.

## Related skills

- `gcp-landing-zone`, `gcp-iam-least-privilege`, `gcp-observability-baseline`

## References

- Best practices for VPC design: https://cloud.google.com/architecture/best-practices-vpc-design
- Decide the network design for your landing zone: https://cloud.google.com/architecture/landing-zones/decide-network-design
- Shared VPC: https://cloud.google.com/vpc/docs/shared-vpc
- Firewall policies: https://cloud.google.com/firewall/docs/firewall-policies-overview
- Network Connectivity Center: https://cloud.google.com/network-connectivity/docs/network-connectivity-center/concepts/overview
- Private Service Connect: https://cloud.google.com/vpc/docs/private-service-connect
- Cloud NAT: https://cloud.google.com/nat/docs/overview
