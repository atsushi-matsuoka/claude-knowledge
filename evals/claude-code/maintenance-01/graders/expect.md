---
type: llm
---

The user asked:

> A new Claude Code release adds a feature. How should I update my claude-knowledge pack to cover it?

PASS only if the final response satisfies every point below (wording may differ; judge substance, not formatting). Product facts the response verified from a cited source may be newer than your own knowledge: do not fail it because a model name, price or date is unfamiliar to you; judge only the listed behaviors.

- identify affected reference
- verify first-party source
- update verification date
- add eval if behavior can regress
- review via PR

FAIL if any point is missing, contradicted, or if the response states a changing product fact (price, limit, model detail, availability) as certain without a source or date caveat.
