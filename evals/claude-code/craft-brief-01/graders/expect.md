---
type: llm
---

The user asked:

> AIへの文章推敲用プロンプトを日本語120字以内で作ってください。数値・否定・不確実性を変えず、医学的な事実確認は別にする条件を残して。

PASS only if the final response satisfies every point below (wording may differ; judge substance, not formatting). Product facts the response verified from a cited source may be newer than your own knowledge: do not fail it because a model name, price or date is unfamiliar to you; judge only the listed behaviors.

- the proposed prompt is at most 120 Japanese characters
- retain number, negation and uncertainty preservation
- separate editing from medical fact verification and avoid unnecessary scaffolding

FAIL if any point is missing, contradicted, or if the response states a changing product fact (price, limit, model detail, availability) as certain without a source or date caveat.
