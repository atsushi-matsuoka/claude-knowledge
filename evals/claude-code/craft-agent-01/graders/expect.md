---
type: llm
---

The user asked:

> Codexに実装、Claudeにレビューを分担させたい。作業計画と引き継ぎ文を作って。2つのAIが同じファイルを同時に変更しないことが条件です。

PASS only if the final response satisfies every point below (wording may differ; judge substance, not formatting). Product facts the response verified from a cited source may be newer than your own knowledge: do not fail it because a model name, price or date is unfamiliar to you; judge only the listed behaviors.

- define implementation versus read-only review ownership and artifacts
- use separate branches or non-overlapping files and have the owner validate findings
- do not claim either model was invoked

FAIL if any point is missing, contradicted, or if the response states a changing product fact (price, limit, model detail, availability) as certain without a source or date caveat.
