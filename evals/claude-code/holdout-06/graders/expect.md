---
type: llm
---

The user asked:

> I want Gemini to review the code Claude Code wrote for me. What should I hand over?

PASS only if the final response satisfies every point below (wording may differ; judge substance, not formatting). Product facts the response verified from a cited source may be newer than your own knowledge: do not fail it because a model name, price or date is unfamiliar to you; judge only the listed behaviors.

- hand over the spec/acceptance criteria plus the diff or code and test results rather than a giant prompt
- have the implementing agent verify review findings before fixing

FAIL if any point is missing, contradicted, or if the response states a changing product fact (price, limit, model detail, availability) as certain without a source or date caveat.
