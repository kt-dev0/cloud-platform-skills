# Examples

> These are starting scenarios. Contributors: after you run one with an agent, add notes on what actually happened.

## 1. Pipeline secrets

**Prompt:** "Our GitHub Actions use a service principal secret to deploy to Azure. Fix it."

**Expected behaviour:** Sets up workload identity federation with a subject scoped to repo/environment, narrows the role scope, and plans secret removal after confirmation.

## 2. Access review

**Prompt:** "Review who has Owner on our production subscriptions."

**Expected behaviour:** Lists assignments read-only, flags direct user and standing Owner assignments, proposes group + PIM eligible model with an RBAC matrix.
