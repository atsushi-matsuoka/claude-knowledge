# Quality-first model and effort selection

Last verified: 2026-09-28

The roles below are this pack's proposed policy, based on first-party model positioning and reasoning guidance. They are not measured optimal thresholds. Current IDs belong in the separate model register, not in permanent instructions.

| Task evidence | Initial policy | Acceptance / escalation |
|---|---|---|
| Bounded extraction, formatting, routine transformations; low failure cost | Efficient candidate, low effort | Exact checks on missing fields, types and preserved meaning |
| Ordinary development or several dependent steps | Balanced candidate, medium effort | Run affected tests; inspect the result, not only tool exit codes |
| Complex design, scientific synthesis, security-sensitive review or high failure cost | High-capability candidate, high effort | Ground claims; use independent verification where worthwhile |
| A short edit requiring strict preservation of meaning | Treat precision as consequential; high-capability candidate | Explicit original/final comparison of quantities, negation and certainty |

Choose a surface with the necessary tools first. Restrict choices to recently confirmed runtime availability and compatible input/tool requirements. If the required quality tier is unavailable, explain the limitation; do not silently select a cheaper model. When a cheaper tier has no verified candidate, an available stronger one is an acceptable bounded fallback.

Effort and model are different controls. Start with a reasonable supported effort; consider xhigh/max or pro execution only when the expected quality value or actual evaluation justifies the latency and spend. Do not select maximum effort by default. Do not infer that a stronger model will fix a permission error, an absent file or an impossible output contract: repair the evidence/tool path first.

For ambiguous tasks, prioritize a usable reversible first artifact over asking the user to select technical components. When tests expose a reasoning failure, raise effort or model for that step; for missing context, retrieve the necessary evidence instead. Keep candidate, selected, invoked and validated as separate recorded states.

## Sources

- https://developers.openai.com/api/docs/models
- https://developers.openai.com/api/docs/guides/reasoning
- https://developers.openai.com/api/docs/guides/evaluation-best-practices
