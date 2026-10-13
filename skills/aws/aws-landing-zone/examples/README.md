# Examples

> These are starting scenarios. Contributors: after you run one with an agent, add notes on what actually happened.

## 1. New org

**Prompt:** "Set up our AWS organization for 30 product teams using Terraform."

**Expected behaviour:** Recommends Control Tower + AFT, proposes the OU structure, SCPs tested in Policy Staging, Identity Center, and account vending baseline; confirms before deploying.

## 2. Regulated

**Prompt:** "We need FedRAMP-aligned controls across accounts."

**Expected behaviour:** Recommends Landing Zone Accelerator alongside Control Tower and explains the complexity trade-off.
