# Contributing

Thanks for helping build a shared library of cloud platform engineering skills. This guide covers what makes a good skill and how to submit one.

## The community-usefulness bar

A skill is accepted when it meets **all** of these:

- [ ] **Solves a recurring, real task** that many platform engineers face (not a one-off or a narrow internal process).
- [ ] **Org-agnostic.** No company names, tenant IDs, subscription IDs, internal URLs, or hard-coded naming schemes. Anything org-specific is a parameter or a clarifying question.
- [ ] **Aligned to the provider's framework.** It maps to the pillars in [docs/frameworks.md](docs/frameworks.md) and states the trade-offs.
- [ ] **Cites official sources** (provider docs and architecture centers) for every non-obvious recommendation.
- [ ] **Secure and safe by default.** Least privilege and no secrets in code. It plans or runs what-if before applying, and it asks for confirmation before destructive or costly actions.
- [ ] **Tested.** You ran it with an agent on at least one realistic scenario and recorded the prompt and the outcome in `examples/`.
- [ ] **Focused and composable.** It does one job well and links to sibling skills instead of duplicating them.
- [ ] **Passes `python3 scripts/validate_skills.py`.**

## Naming and placement

- Path: `skills/<provider>/<provider>-<topic>/`, where provider is one of `azure`, `aws`, `gcp`, `oci`, or `multi-cloud`.
- The folder name and the `name` in the frontmatter must match exactly. Use lowercase kebab-case, at most 64 characters.
- Use the provider's own vocabulary (for example *subscription* on Azure, *account* on AWS, *project* on GCP, *compartment* on OCI).

## Skill anatomy

Start from [templates/SKILL_TEMPLATE.md](templates/SKILL_TEMPLATE.md). Required sections:

1. **When to use / When not to use**
2. **Inputs to gather**: the clarifying questions the agent asks first
3. **Workflow**: numbered and decision-oriented ("if X, then Y")
4. **Well-Architected alignment**: a pillar table plus trade-offs
5. **Guardrails**
6. **Validation**: how the agent proves the output is correct
7. **References**: official links only

Keep `SKILL.md` under ~400 lines. Put deeper material in `references/` and link to it so the agent loads it only when needed.

### Writing the `description`

The description decides when an agent uses the skill, so make it count:
- Say **what** the skill does and **when** to use it.
- Include the phrases users actually type ("review my Azure architecture", "is this Bicep well-architected").
- Stay under 1024 characters.

## Workflow for contributors

1. Open a **Skill request** issue (or comment on an existing one) so nobody duplicates work.
2. Draft the skill with [prompts/create-skill.md](prompts/create-skill.md).
3. Test it with an agent and save the results to `examples/`. Keep raw output from real accounts in `test-runs/`, which git ignores. Before you copy anything into `examples/`, remove account, tenant and subscription IDs, hostnames and any secrets.
4. Self-review with [prompts/review-skill.md](prompts/review-skill.md).
5. Run `python3 scripts/validate_skills.py`.
6. Add the skill to the catalog table in `README.md` and to `.claude-plugin/marketplace.json`.
7. Open a PR. The PR template walks you through the checklist.

## Keeping skills current

Cloud guidance changes often. Each quarter, maintainers run [prompts/refresh-skill.md](prompts/refresh-skill.md) on skills whose `last-reviewed` date is more than 6 months old. If you spot something outdated, open an issue with the official source that shows the change.

## Adding a new provider

1. Add the provider's framework and pillars to [docs/frameworks.md](docs/frameworks.md).
2. Add the provider's terms and sources to the *Provider profiles* section of [prompts/create-skill.md](prompts/create-skill.md).
3. Add the provider to `PROVIDERS` in `scripts/validate_skills.py`.
4. Add a plugin entry (for example `aws-platform-skills`) to `.claude-plugin/marketplace.json`.

## Code of conduct

Be respectful and constructive. We follow the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).
