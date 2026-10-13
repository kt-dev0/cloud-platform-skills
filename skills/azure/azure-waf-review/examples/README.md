# Examples

## 1. Review IaC before deployment

**Prompt:** "Here's the Bicep for our new web app (App Service, Azure SQL, Storage). Is it well-architected for production?"

**Expected behaviour:** the agent asks about criticality and RTO/RPO, reads every Bicep file, and runs PSRule if it's available. It reports findings such as SQL public network access being enabled, a missing zone-redundant App Service plan, or no diagnostic settings, each with a checklist code and a Learn link. It makes no changes.

## 2. Review a live subscription

**Prompt:** "Do a WAF assessment of resource group rg-payments-prod."

**Expected behaviour:** the agent confirms `az account show` and Reader access, runs the Resource Graph queries scoped to that RG, and pulls Advisor recommendations. It produces the report with a top-5 action list. It only runs `list`, `show` and `graph query` commands.

## 3. Design-only review

**Prompt:** "We're planning AKS + Cosmos DB in one region with a VPN back to on-prem. What would the Well-Architected Framework say?"

**Expected behaviour:** the agent runs a design review using the AKS and Cosmos DB service guides. It flags the single-region choice against the stated RTO, and it marks implementation details as "Unable to verify" rather than guessing.
