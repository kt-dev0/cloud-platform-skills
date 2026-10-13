---
name: aws-landing-zone
description: Design and deploy a multi-account AWS landing zone with AWS Organizations and AWS Control Tower (or Landing Zone Accelerator on AWS) — OU structure per AWS multi-account guidance, Log Archive and Audit accounts, service control policies, Control Tower controls, IAM Identity Center, and account vending (Account Factory / AFT). Use when the user says "set up an AWS landing zone", "design our AWS OUs", "Control Tower vs Landing Zone Accelerator", "multi-account strategy", "account vending", or "write SCPs for our organization".
license: MIT
metadata:
  provider: aws
  framework: AWS Well-Architected Framework
  pillars: operational-excellence, security, reliability, performance-efficiency, cost-optimization, sustainability
  category: foundation
  status: draft
  last-reviewed: 2026-10-12
  version: 0.1.0
---

# AWS Landing Zone

Build a secure, scalable multi-account AWS environment based on the AWS guidance *Organizing Your AWS Environment Using Multiple Accounts* and the AWS Security Reference Architecture (SRA). Prefer **AWS Control Tower** as the managed baseline, and extend it rather than replace it.

## When to use

- A new AWS organization, or an existing one without a clear OU or guardrail structure.
- Choosing between Control Tower, Landing Zone Accelerator (LZA) on AWS, and custom tooling.
- Designing account vending, and service control policies (SCPs) or resource control policies (RCPs).

## When not to use

- Transit networking design: use `aws-network-hub`.
- Detailed permission sets and IAM roles: use `aws-iam-least-privilege`.
- Reviewing a workload: use `aws-well-architected-review`.

## Inputs to gather

| Input | Why it matters | Default |
|---|---|---|
| Greenfield or existing organization | Enrollment vs. new setup | Ask |
| Home region and governed regions | Control Tower home region can't be changed easily; region deny SCP | Ask (required) |
| Compliance needs (e.g. FedRAMP, PCI) | LZA has compliance-oriented configurations | None |
| Identity source (Identity Center directory / external IdP such as Entra ID, Okta) | Identity Center configuration | External IdP |
| IaC for account customization (Terraform / CloudFormation / CDK) | AFT vs. Customizations for Control Tower vs. LZA | Ask |
| Expected number of workloads/teams | OU and account granularity | Ask |

## Workflow

1. **Assess (read-only).** `aws organizations describe-organization`, `list-roots`, `list-organizational-units-for-parent`, `list-accounts`, `list-policies --filter SERVICE_CONTROL_POLICY`. Flag workloads running in the **management account**.
2. **Choose the implementation.**
   - Use **Control Tower** by default: managed landing zone, controls library, Account Factory.
   - Add **Account Factory for Terraform (AFT)** when the organization standardizes on Terraform for account customization.
   - Use **Landing Zone Accelerator on AWS** (deployed alongside Control Tower) for regulated environments that need broad, configuration-driven security baselines.
3. **Design the OU structure** (adapt it to need, but keep these foundational OUs):
   ```
   Root
   ├── Security            (Log Archive, Audit/Security Tooling accounts)
   ├── Infrastructure      (Network, Shared Services)
   ├── Workloads
   │   ├── Prod
   │   └── NonProd
   ├── Sandbox             (isolated, budget-capped experimentation)
   ├── Policy Staging      (test SCPs/controls before broad rollout)
   └── Suspended           (closed/quarantined accounts, deny-all SCP)
   ```
   Use **one account per workload per environment**. Organise OUs by **security and control needs**, not by the org chart.
4. **Management account hygiene.** Keep it to billing, Organizations and Control Tower only, with no workloads. Delegate administration of security services (GuardDuty, Security Hub, Config, IAM Access Analyzer, Firewall Manager) to the Audit or Security Tooling account.
5. **Preventive guardrails.**
   - Enable the mandatory and strongly recommended Control Tower controls.
   - Write SCPs for: a region deny (excluding global services), preventing anyone from disabling CloudTrail, Config or GuardDuty, preventing accounts from leaving the organization, and protecting the Control Tower roles. Test them in **Policy Staging** first.
   - Consider resource control policies to enforce a data perimeter (for example restricting S3 access to organization principals).
6. **Identity.** Use IAM Identity Center federated with the corporate IdP, with group-based permission sets. Detail lives in `aws-iam-least-privilege`.
7. **Account vending.** Define what each new account gets: baseline roles, budget, tags, default VPC removal, a network attachment request, and security service enrollment.
8. **Generate the configuration** (Control Tower manifest or settings, AFT repos, or the LZA config files). Use placeholders for account emails and IDs. Present the plan and the cost drivers (Config recording, CloudTrail data events, GuardDuty, Security Hub), and **confirm before deploying**.

## Well-Architected alignment

| Pillar | Recommendation | Rationale | Source |
|---|---|---|---|
| Operational Excellence | Control Tower + IaC-driven account vending; Policy Staging OU for testing guardrails | Consistent, automated account baselines | https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html |
| Security | Org-wide CloudTrail to Log Archive; delegated admin security tooling; SCPs; no workloads in management account | Strong isolation and centralized detection | https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html |
| Reliability | Account-level isolation limits blast radius and quota contention | Failures and limits don't spread across workloads | https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.html |
| Performance Efficiency | Per-account service quotas; governed regions close to users | Scale independently per workload | https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html |
| Cost Optimization | Consolidated billing, mandatory tags, budgets per account, sandbox spend limits | Clear cost ownership | https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.html |
| Sustainability | Region deny for unused regions; sandbox cleanup automation | Avoid idle, forgotten resources | https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sustainability-pillar.html |

**Trade-offs:** More accounts improve isolation but add per-account baseline costs (Config, GuardDuty) and operational overhead. Strict SCPs block risky actions but can break service integrations, which is why the Policy Staging OU exists. LZA offers broad compliance coverage at the price of more complexity than Control Tower alone.

## Guardrails

- Never attach new SCPs to Root or production OUs without testing them in Policy Staging and getting explicit confirmation.
- Never deploy workloads into the management account.
- Don't modify or delete the Control Tower-managed resources or roles (`AWSControlTower*`) directly.
- Never close or move accounts without confirmation and an impact summary.
- Keep root user credentials for member accounts locked down (centralized root access management where available).

## Validation

- Control Tower dashboard shows no drift. `aws controltower list-enabled-controls --target-identifier <ou-arn>` shows the expected controls.
- Test SCPs with IAM policy simulation or a test action in a Policy Staging account (expect `AccessDenied`).
- An org trail exists: `aws cloudtrail describe-trails` from the management account shows `IsOrganizationTrail: true`.

## Common mistakes

- Running workloads in the management account.
- Designing OUs after the org chart, which forces reorganization later.
- A region deny SCP that blocks global services (IAM, CloudFront, Route 53, Support).
- Skipping the Suspended OU, so closed accounts keep their permissions.

## Related skills

- `aws-iam-least-privilege`, `aws-network-hub`, `aws-observability-baseline`, `aws-well-architected-review`

## References

- Organizing your AWS environment using multiple accounts: https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.html
- AWS Control Tower: https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html
- Account Factory for Terraform: https://docs.aws.amazon.com/controltower/latest/userguide/aft-overview.html
- Landing Zone Accelerator on AWS: https://aws.amazon.com/solutions/implementations/landing-zone-accelerator-on-aws/
- Service control policies: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html
- AWS Security Reference Architecture: https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html
