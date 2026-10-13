# Examples

> These are starting scenarios. Contributors: after you run one with an agent, add notes on what actually happened.

## 1. Tagging

**Prompt:** "Require an owner and cost-center tag on all resource groups and inherit them to resources."

**Expected behaviour:** Finds built-in tag definitions, proposes an initiative with Deny on RGs and Modify inheritance, rolls out in DoNotEnforce first, plans remediation with confirmation.

## 2. Blocked deployment

**Prompt:** "My deployment failed with RequestDisallowedByPolicy."

**Expected behaviour:** Identifies the assignment and definition, explains why, and suggests compliant changes or a time-bound exemption with justification.
