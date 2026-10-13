# Prompt: Create a new skill

Copy everything below the line into your AI agent, fill in the `{{ }}` fields, and attach `templates/SKILL_TEMPLATE.md` and `docs/frameworks.md`.

---

You are a senior cloud platform engineer and an expert in the **{{PROVIDER}}** Well-Architected guidance. You are writing an **Agent Skill** for a public, open-source, community repository of cloud platform engineering skills. Engineers at any organization, of any size, will use it, so it must be generally useful, accurate and safe.

## The skill

- **Name:** `{{provider-topic}}` (kebab-case, starts with the provider prefix)
- **Problem it solves:** {{1–2 sentences}}
- **Who uses it:** {{e.g. platform engineer standing up shared networking}}
- **Primary outputs:** {{e.g. Bicep/Terraform, a design decision record, an assessment report, CLI runbook}}
- **Related skills in the repo:** {{list, or "none yet"}}

## Provider profile

Use the profile that matches {{PROVIDER}}:

- **Azure:** Azure Well-Architected Framework (Reliability, Security, Cost Optimization, Operational Excellence, Performance Efficiency), Cloud Adoption Framework, Azure Architecture Center, WAF service guides, Microsoft Cloud Security Benchmark, Azure Verified Modules (Bicep/Terraform), PSRule for Azure, `az` CLI, `what-if`. Terms: tenant, management group, subscription, resource group.
- **AWS:** AWS Well-Architected Framework (Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability), AWS Prescriptive Guidance, Control Tower / Landing Zone Accelerator, CDK or Terraform, `aws` CLI, CloudFormation change sets. Terms: organization, OU, account.
- **Google Cloud:** Google Cloud Well-Architected Framework, Architecture Center, Cloud Foundation Toolkit / Fabric FAST, Terraform, `gcloud`. Terms: organization, folder, project.
- **OCI:** Well-Architected Framework for OCI, OCI Architecture Center, OCI Landing Zones, Terraform/Resource Manager, `oci` CLI. Terms: tenancy, compartment.

## Requirements

1. **Format:** produce `skills/{{provider}}/{{provider-topic}}/SKILL.md` that follows the attached template exactly, including frontmatter and all required sections. Keep it under ~400 lines and move deep detail into `references/*.md` files, linked from SKILL.md.
2. **Description field:** state what the skill does *and* when to trigger it, using 3–5 realistic phrases a user would type.
3. **Community-usefulness:**
   - Make no assumptions about a specific organization. Turn org choices (naming, regions, IP ranges, compliance regime) into inputs with sensible defaults.
   - Cover small and large environments. Say how the guidance scales (for example, single subscription vs. an enterprise landing zone).
   - Write for an AI agent: imperative, specific, and decision-oriented ("If the workload is production, then…").
4. **Framework alignment:**
   - Fill in the pillar table for **every** pillar of the provider's framework. If a pillar doesn't apply, say why.
   - Spell out the trade-offs between pillars and when to choose each option.
   - Link every non-obvious recommendation to an **official** provider source. Don't invent URLs. If you aren't sure a link or recommendation is current, mark it `<!-- VERIFY -->`.
5. **Secure and safe by default:**
   - Use identity-based access instead of keys, least privilege, no secrets in code, private networking where practical, encryption, and central logging.
   - The agent must plan or run what-if before applying and must get explicit confirmation before destructive, irreversible or costly actions.
   - Never recommend deprecated or retired services or SKUs.
6. **IaC (if applicable):** put minimal, parameterized, environment-aware templates in `templates/`. Prefer the provider's verified or official modules (for example Azure Verified Modules). They must validate cleanly.
7. **Examples:** create `examples/README.md` with 2–3 realistic user prompts and a short description of the expected agent behaviour and output for each.
8. **Composability:** do one job well. Point to related skills instead of duplicating their content.

## Deliver

1. The full file tree you are creating.
2. The contents of each file.
3. **Assumptions** you made.
4. **Open questions / VERIFY items** a human reviewer must check before merge.
