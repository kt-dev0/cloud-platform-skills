# Examples

> These are starting scenarios. Contributors: after you run one with an agent, add notes on what actually happened.

## 1. Greenfield enterprise

**Prompt:** "We're a 2,000-person company starting on Azure with GitHub Actions and Terraform. Set up our landing zone."

**Expected behaviour:** Asks for regions, connectivity and compliance; recommends the ALZ IaC accelerator (Terraform); proposes the CAF management group hierarchy and platform subscriptions; generates accelerator inputs with placeholder IDs; shows `terraform plan` and cost drivers; waits for confirmation.

## 2. Small org

**Prompt:** "We're a 15-person startup with 3 apps. Do we need a full landing zone?"

**Expected behaviour:** Recommends the ALZ design with reduced scope (consolidated platform subscription, one landing-zone MG), explains the trade-offs, and shows how it can grow.
