# Examples

> These are starting scenarios. Contributors: after you run one with an agent, add notes on what actually happened.

## 1. App team access

**Prompt:** "Let the app team manage compute in the app compartment but only use the network."

**Expected behaviour:** Writes compartment-scoped policies with `manage instance-family` and `use virtual-network-family`, attached at the parent compartment.

## 2. Remove API keys

**Prompt:** "Our VMs use a user's API key to read Object Storage."

**Expected behaviour:** Creates a dynamic group and instance principal policy, and plans key removal after confirmation.
