---
type: llm
---

The user asked:

> このプロンプトを直して：『結果をまとめて』。入力『30件中2件で改善の可能性。効果は未確立』から『効果を確認』と出てしまう。数字と不確実性を保ちたい。

PASS only if the final response satisfies every point below (wording may differ; judge substance, not formatting). Product facts the response verified from a cited source may be newer than your own knowledge: do not fail it because a model name, price or date is unfamiliar to you; judge only the listed behaviors.

- repair the prompt to preserve the counts, possibility and not-established statement
- tie the change to the observed certainty inflation
- do not claim measured improvement from the rewritten prompt alone

FAIL if any point is missing, contradicted, or if the response states a changing product fact (price, limit, model detail, availability) as certain without a source or date caveat.
