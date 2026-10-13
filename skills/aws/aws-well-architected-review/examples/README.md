# Examples

> These are starting scenarios. Contributors: after you run one with an agent, add notes on what actually happened.

## 1. Live account review

**Prompt:** "Do a Well-Architected review of our prod account for the payments service."

**Expected behaviour:** Confirms read-only role, pulls Security Hub, Config, Trusted Advisor, Access Analyzer and Compute Optimizer data, and produces an HRI/MRI report across all six pillars.

## 2. IaC review

**Prompt:** "Is this CDK app production-ready?"

**Expected behaviour:** Reviews the synthesized templates, runs cfn-lint/Checkov if available, and reports findings with best-practice IDs.
