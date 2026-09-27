---
type: llm
---

The user asked:

> レビュー用のAI指示を設計して。修正はせず、元の仕様と差分を見て、問題の場所・影響・根拠だけ返してほしい。根拠が弱い指摘は断定しないで。

PASS only if the final response satisfies every point below (wording may differ; judge substance, not formatting). Product facts the response verified from a cited source may be newer than your own knowledge: do not fail it because a model name, price or date is unfamiliar to you; judge only the listed behaviors.

- produce a review prompt with an explicit read-only boundary
- require locations, impact and evidence tied to the original specification and diff
- preserve uncertainty and do not automatically implement findings

FAIL if any point is missing, contradicted, or if the response states a changing product fact (price, limit, model detail, availability) as certain without a source or date caveat.
