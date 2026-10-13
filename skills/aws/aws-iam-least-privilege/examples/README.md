# Examples

> These are starting scenarios. Contributors: after you run one with an agent, add notes on what actually happened.

## 1. Remove keys

**Prompt:** "Replace the AWS access keys in our GitHub Actions secrets."

**Expected behaviour:** Creates an OIDC provider and role with `sub` restricted to the repo/branch, least-privilege policy validated with Access Analyzer, and a key retirement plan.

## 2. Policy authoring

**Prompt:** "Write a policy that lets a Lambda read one S3 prefix and one DynamoDB table."

**Expected behaviour:** Produces a scoped policy with resource ARNs and conditions, validated with validate-policy.
