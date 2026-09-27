# From data to a verified artifact

Last verified: 2026-09-28

Before analysis, record the unit of observation, inclusion rules, metric denominator, date coverage, missing-value policy and expected output. Inspect schemas and samples. For joins, check key uniqueness, relationship cardinality, row counts and unmatched keys before interpreting a total. Do not silently deduplicate without a justified rule.

Compare like periods and populations. Label incomplete periods and uncertain definitions; avoid causal or medical conclusions from descriptive counts. Use code or formulas for arithmetic, retaining source locations and transformations needed to reproduce it.

Produce the requested file, then reopen that exact saved artifact. Reconcile totals across tables/charts/text, inspect relevant formulas and missing cells, and verify readability or rendering when visual layout matters. Refine the same artifact rather than replacing evidence with an attractive narrative. Convert a repeated successful method into a Skill only after the contract is clear.

## Original probe

The input says March: 100 orders; April days 1-10: 60. Both counts can be reported with their windows. A claim that April's monthly total fell 40% is unsupported. For a join with two detail rows per order, distinct-order count and detail-row count must remain separate. These are synthetic contract examples, not Academy demo execution.

## Sources

- https://academy.openai.com/public/clubs/work-users-ynjqu/resources/how-data-science-teams-use-codex-webinar-resource-guide-2026-05-28
- https://academy.openai.com/public/clubs/work-users-ynjqu/resources/data-analysis
