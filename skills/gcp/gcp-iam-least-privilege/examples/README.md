# Examples

> These are starting scenarios. Contributors: after you run one with an agent, add notes on what actually happened.

## 1. Keyless CI

**Prompt:** "Deploy from GitHub Actions to GCP without a JSON key."

**Expected behaviour:** Creates a WIF pool/provider with attribute condition on repository, a dedicated SA, and narrow roles.

## 2. Editor cleanup

**Prompt:** "Too many people have Editor. Fix it."

**Expected behaviour:** Inventories bindings, uses IAM recommender to propose predefined roles to groups, and plans removal with confirmation.
