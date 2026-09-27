---
type: llm
---

The user asked:

> 要約プロンプトを改善する実験計画を立てたい。テストの正解を見せてからプロンプトを作れば公平ですか？それも含めて手順を決めて。

PASS only if the final response satisfies every point below (wording may differ; judge substance, not formatting). Product facts the response verified from a cited source may be newer than your own knowledge: do not fail it because a model name, price or date is unfamiliar to you; judge only the listed behaviors.

- explain that revealing final test answers to the designer contaminates the comparison
- separate development inputs from untouched final tests
- propose matched baseline and candidate runs without fabricated results

FAIL if any point is missing, contradicted, or if the response states a changing product fact (price, limit, model detail, availability) as certain without a source or date caveat.
