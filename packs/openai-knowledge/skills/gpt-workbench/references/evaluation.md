# Demonstrate benefit instead of claiming it

Last verified: 2026-09-28

Measure three distinct outcomes: selecting the right guidance/model, producing a correct artifact, and improving the result when that artifact is used. A successful Skill activation or a longer prompt establishes none of the downstream benefit.

Before optimizing, define the task-specific target and critical failures. Keep baseline/candidate trials matched for inputs, tools, budget and downstream execution conditions. For a Skill ablation use the same model/settings; for model selection change the model deliberately and label it as a different experiment. Record all attempts, including errors and incomplete outputs, plus observed latency and total cost. Never fill unobserved usage fields with zero.

Use deterministic exact checks for structured outputs. For specifications and reviews, a fixed rubric should separately assess requirement preservation, evidence, usability and safety; calibrate model judging with human review and conceal candidate labels where possible. Keep final test answers out of prompt design. The initial cases in this pack are developer-visible smoke cases; obtain independently prepared held-out cases before claiming general improvement.

Reject a critical constraint or privacy regression even if an average score rises. Reuse frozen baselines for unchanged behavior, rerun affected tests during development, and run an appropriate complete comparison at release. A small synthetic set supports only a narrow observed result, not increased general intelligence. Unexecuted model experiments remain unmeasured.

## Sources

- https://developers.openai.com/api/docs/guides/evaluation-best-practices
- https://developers.openai.com/api/docs/guides/structured-outputs
