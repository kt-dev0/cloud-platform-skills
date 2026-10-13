# Report template

Write the report in Markdown using this structure.

```markdown
# Azure Well-Architected Review: <workload name>

**Scope:** <subscriptions/RGs/IaC files reviewed>  
**Environment / criticality:** <prod, business-critical>  
**Date:** <YYYY-MM-DD>  
**Assumptions:** <defaults used for unanswered inputs>

## Summary

| Pillar | High | Medium | Low | Unable to verify |
|---|---|---|---|---|
| Reliability | | | | |
| Security | | | | |
| Cost Optimization | | | | |
| Operational Excellence | | | | |
| Performance Efficiency | | | | |

### Top 5 actions
1. <action> (<pillar>, <severity>)
...

## Findings

### <ID e.g. SEC-01>: <short title>
- **Pillar / checklist:** Security / SE:05
- **Severity:** High
- **Affected:** <resource(s) or IaC file:line>
- **Evidence:** <what was observed>
- **Recommendation:** <concrete change>
- **Trade-off:** <impact on other pillars, if any>
- **Source:** <Microsoft Learn URL>

## Unable to verify
<items lacking evidence, and what's needed to verify them>

## Next steps
- Run the official Azure Well-Architected Review assessment for a formal score.
- <related skills to implement fixes>
```
