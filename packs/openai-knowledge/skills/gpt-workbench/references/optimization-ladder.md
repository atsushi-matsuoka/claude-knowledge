# Optimize measured work under constraints

Last verified: 2026-09-28

This is a proposed decision procedure, not an empirically optimal routing policy. It supplements API Bootcamp sessions whose lesson bodies remain unavailable.

1. Define mandatory quality, meaning-preservation and authorization checks. Choose a representative development set and reserve independently prepared final cases. Record the baseline before tuning.
2. Classify the failure: unavailable evidence/tool access; irrelevant context; ambiguous instructions; reasoning error; malformed output; latency/cost. Repair the cause rather than reflexively changing models.
3. Change the smallest relevant factor. Compare prompt/context/tool changes at fixed model/settings. Compare model or reasoning effort as a separate experiment with the same accepted contract. Choose only supported, actually accessible candidates; no claimed switch without execution evidence.
4. Measure correct usable outputs plus critical failures, total observed cost including retries/tools, and end-to-end completion time. Time to first token is a different metric. Unknown measurements stay unknown, not zero.
5. After quality passes, consider shorter unnecessary output, fewer round trips, caching of eligible stable input, deterministic code, or independent parallel work. Check current compatibility before implementation. Cost savings cannot authorize a quality or privacy regression.
6. Consider fine-tuning/distillation only for persistent behavioral failures with representative lawful data, a valid evaluation and explicit budget. First check current platform/model support; do not promise it changes a consumer ChatGPT account or replaces missing evidence. Do not run paid training/evals automatically.

## Original probe

Candidate B is faster and has a better mean rubric score, but sends a draft without approval. Reject promotion. A candidate that only emits the first character faster has not demonstrated lower total completion latency. Report measured tradeoffs with sample sizes, not general capability gains.

## Sources

- https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy
- https://developers.openai.com/api/docs/guides/latency-optimization
- https://developers.openai.com/api/docs/guides/evaluation-best-practices
