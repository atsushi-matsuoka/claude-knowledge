---
type: llm
---

The user asked:

> Claude Code keeps forgetting to run our linter after editing files, even though CLAUDE.md says to. What's the right fix?

PASS only if the final response satisfies every point below (wording may differ; judge substance, not formatting). Product facts the response verified from a cited source may be newer than your own knowledge: do not fail it because a model name, price or date is unfamiliar to you; judge only the listed behaviors.

- explain CLAUDE.md is advisory context
- recommend a hook (e.g. PostToolUse on edits) for something that must run every time

FAIL if any point is missing, contradicted, or if the response states a changing product fact (price, limit, model detail, availability) as certain without a source or date caveat.
