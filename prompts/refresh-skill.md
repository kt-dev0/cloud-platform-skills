# Prompt: Refresh an existing skill

Run this quarterly on skills whose `last-reviewed` date is more than 6 months old. Use an agent that has web access.

---

You are maintaining a community Agent Skill for cloud platform engineering. Bring the attached skill up to date with the provider's **current** official guidance.

1. Open every link in **References** and in the alignment table. Report broken or redirected links and replace them with the current official URL.
2. Check the provider's Well-Architected framework, the relevant service guides, and the release notes and deprecation announcements for the services this skill covers. List every change since the skill's `last-reviewed` date that affects its recommendations.
3. Check the IaC templates against the latest verified or official module versions and API versions.
4. Propose minimal, specific edits. Don't rewrite sections that are still correct.
5. Update `last-reviewed` to today and bump `version`: patch for link and wording fixes, minor for changed recommendations, major for a changed workflow or outputs.

Output: a change summary table (what changed, why, source URL), followed by the updated files.
