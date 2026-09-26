---
type: llm
---

The user asked:

> My CLAUDE.md is 900 lines and Claude seems to ignore half of it. How should I restructure it?

PASS only if the final response satisfies every point below (wording may differ; judge substance, not formatting). Product facts the response verified from a cited source may be newer than your own knowledge: do not fail it because a model name, price or date is unfamiliar to you; judge only the listed behaviors.

- recommend a much shorter CLAUDE.md (official target is under ~200 lines)
- move procedures/reference material into Skills and file-specific rules into path-scoped .claude/rules
- note that @imports still load at launch and do not reduce context

FAIL if any point is missing, contradicted, or if the response states a changing product fact (price, limit, model detail, availability) as certain without a source or date caveat.
