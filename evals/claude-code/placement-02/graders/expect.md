---
type: llm
---

The user asked:

> Our repo already has an AGENTS.md for Codex. Do I also need a CLAUDE.md for Claude Code, and how do I avoid duplicating instructions?

PASS only if the final response satisfies every point below (wording may differ; judge substance, not formatting):

- say Claude Code can read AGENTS.md when there is no CLAUDE.md
- recommend a CLAUDE.md that imports @AGENTS.md if Claude-specific notes are needed
- warn that adding a CLAUDE.md stops AGENTS.md being read unless imported

FAIL if any point is missing, contradicted, or if the response states a changing product fact (price, limit, model detail, availability) as certain without a source or date caveat.
