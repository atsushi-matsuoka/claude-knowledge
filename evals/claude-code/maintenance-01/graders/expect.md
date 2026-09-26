---
type: llm
---

The user asked:

> A new Claude Code release adds a feature. How should this repo change?

PASS only if the final response satisfies every point below (wording may differ; judge substance, not formatting):

- identify affected reference
- verify first-party source
- update verification date
- add eval if behavior can regress
- review via PR

FAIL if any point is missing, contradicted, or if the response states a changing product fact (price, limit, model detail, availability) as certain without a source or date caveat.
