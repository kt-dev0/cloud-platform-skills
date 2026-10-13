# Examples

> These are starting scenarios. Contributors: after you run one with an agent, add notes on what actually happened.

## 1. Hybrid hub

**Prompt:** "Design a hub-spoke network in East US 2 connecting to on-prem 10.0.0.0/8 via ExpressRoute."

**Expected behaviour:** Flags the on-prem /8 overlap risk and asks for free ranges; produces an IP plan, hub subnets, firewall/gateway SKUs, spoke UDRs and central private DNS; previews the IaC and confirms.

## 2. DNS issue

**Prompt:** "My private endpoint resolves to a public IP from another VNet."

**Expected behaviour:** Diagnoses missing VNet links or per-spoke Private DNS zones; recommends centralized privatelink zones with policy-based registration.
