# Model candidates, not account entitlements

Last verified: 2026-09-28

The companion models.json is a small dated candidate register, not a complete catalogue or benchmark. GPT-6 Astra is the first-party high-capability candidate, Sol the balanced coding/workflow candidate, and Luna the focused-volume candidate. Their API IDs and supported efforts come from the specific model cards. No account invocation or task-quality comparison was performed.

## Retrieval limitation

Current first-party search-index extracts exposed these three cards. Direct page opens in this session returned 404/cache misses; the generic latest-model page also served an older GPT-5.6 body while its search extract described GPT-6. Preserve that discrepancy. Treat entries as candidates pending a live check at use time, not as evidence that the API or a user-facing selector currently exposes them.

Astra does not support effort none. Sol/Luna support none as well as reasoning efforts. Responses API is the conservative tool-using target; do not transplant a Responses request to Chat Completions. The reasoning guide says Astra has no Chat Completions function calling; Sol/Luna cards limit that endpoint's function calling to effort none. Inspect current endpoint-specific docs before constructing requests.

Standard text token input/output prices per million from the indexed cards are 10/50 USD, 2/10 USD and 0.10/0.50 USD respectively. These are not complete job costs: reasoning output, cache writes, long inputs, tools and retry counts can alter totals. No currency conversion or user's remaining quota is assumed.

## Sources

- https://developers.openai.com/api/docs/models
- https://developers.openai.com/api/docs/models/gpt-6-astra
- https://developers.openai.com/api/docs/models/gpt-6-sol
- https://developers.openai.com/api/docs/models/gpt-6-luna
- https://developers.openai.com/api/docs/guides/reasoning
- https://developers.openai.com/api/docs/guides/latest-model
