---
type: llm
---

The user asked:

> 200ページの資料を扱うAIワークフローを設計して。毎回全部を入れず、質問に必要な根拠だけを渡し、回答の出典を追えるようにしたい。

PASS only if the final response satisfies every point below (wording may differ; judge substance, not formatting). Product facts the response verified from a cited source may be newer than your own knowledge: do not fail it because a model name, price or date is unfamiliar to you; judge only the listed behaviors.

- propose retrieving relevant evidence with source locations rather than loading all pages
- keep source facts and unresolved gaps separate
- provide a small workflow with evidence and output checks, not invented retrieval results

FAIL if any point is missing, contradicted, or if the response states a changing product fact (price, limit, model detail, availability) as certain without a source or date caveat.
