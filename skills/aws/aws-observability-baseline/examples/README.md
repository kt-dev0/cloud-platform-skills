# Examples

> These are starting scenarios. Contributors: after you run one with an agent, add notes on what actually happened.

## 1. Gap audit

**Prompt:** "Check whether CloudTrail, Config and GuardDuty are enabled everywhere."

**Expected behaviour:** Enumerates governed regions and accounts read-only, reports gaps, and proposes delegated-admin enablement.

## 2. Cost

**Prompt:** "CloudWatch Logs is our third-largest bill line."

**Expected behaviour:** Finds log groups with no retention and high ingestion, and recommends retention, filtering, and S3 export.
