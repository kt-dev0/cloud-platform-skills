# Examples

> These are starting scenarios. Contributors: after you run one with an agent, add notes on what actually happened.

## 1. Centralized egress

**Prompt:** "We have 40 VPCs each with NAT gateways. Can we centralize?"

**Expected behaviour:** Designs a TGW + egress VPC with per-AZ NAT, compares TGW processing cost vs. per-VPC NAT, and plans a phased migration with confirmation.

## 2. Hybrid DNS

**Prompt:** "On-prem can't resolve our private hosted zones."

**Expected behaviour:** Designs Route 53 Resolver inbound endpoints and on-prem conditional forwarders, shared via RAM.
