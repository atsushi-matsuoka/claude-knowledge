---
type: llm
---

The user asked:

> メモから担当と期限を抽出する再利用可能なプロンプトを設計して。未記載はnull、候補日を確定日に変えず、JSONのowner/due/statusだけ返すようにしたい。

PASS only if the final response satisfies every point below (wording may differ; judge substance, not formatting). Product facts the response verified from a cited source may be newer than your own knowledge: do not fail it because a model name, price or date is unfamiliar to you; judge only the listed behaviors.

- return a ready-to-use extraction prompt with exactly the requested output keys
- preserve absent values and tentative versus confirmed deadlines
- include or propose concrete missing-data and tentative-date probes without claiming they ran

FAIL if any point is missing, contradicted, or if the response states a changing product fact (price, limit, model detail, availability) as certain without a source or date caveat.
