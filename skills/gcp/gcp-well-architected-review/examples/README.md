# Examples

> These are starting scenarios. Contributors: after you run one with an agent, add notes on what actually happened.

## 1. Project review

**Prompt:** "Review our prod GCP project for Well-Architected gaps."

**Expected behaviour:** Checks inherited org policies, IAM, SCC findings and Recommender data read-only; reports across all pillars.

## 2. Terraform review

**Prompt:** "Is this Terraform for GKE production-ready?"

**Expected behaviour:** Reviews regional cluster, Workload Identity, private nodes, release channel, and autoscaling.
