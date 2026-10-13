# Examples

> These are starting scenarios. Contributors: after you run one with an agent, add notes on what actually happened.

## 1. New platform

**Prompt:** "Set up central monitoring for our 20 Azure subscriptions."

**Expected behaviour:** Recommends one workspace per region, diagnostic settings and AMA via policy, AMBA alerts, Service Health alerts and action groups; shows ingestion cost estimate.

## 2. Cost

**Prompt:** "Our Log Analytics bill doubled. Why?"

**Expected behaviour:** Runs the Usage query, identifies top tables, and recommends table plans, retention, and DCR filtering.
