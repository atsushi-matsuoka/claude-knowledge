---
name: claude-stack
description: Use for tasks involving Anthropic Claude, claude.ai, Claude Code, Claude API, Anthropic models, Agent Skills, MCP with Claude, Claude prompting practices, or workflows coordinating Claude with Codex/ChatGPT or Gemini. Use it to distinguish product surfaces, choose the right Claude workflow, consult current official Anthropic sources for volatile facts, and apply this repository's Academy-derived practices. Do not use it for general coding or unrelated AI questions.
---

# Claude Stack

Treat this skill as a routing and workflow layer for Claude-related work.

## Core behavior

1. Identify the **surface** first: claude.ai, Claude Code, Claude API/Platform, or a cross-agent workflow.
2. Read only the reference files needed for the task. Do not load every file by default.
3. For volatile claims (models, pricing, limits, plan availability, beta status, commands, feature availability), verify the current first-party Anthropic source when network/web access is available.
4. Prefer official Anthropic docs and release information over Academy notes or saved summaries when they conflict.
5. Treat Academy material as a curriculum and set of learned practices, not as a frozen product specification.
6. For detailed Claude API/SDK implementation in Claude Code, prefer Anthropic's bundled `claude-api` skill when available; use `references/api-routing.md` to decide.
7. When coordinating multiple AI systems, pass a **specification and acceptance criteria**, not a giant vendor-specific prompt.
8. Do not claim a local or remote action completed unless it was actually executed and verified.
9. Do not put patient-identifiable information, credentials, or restricted clinical data into prompts, repositories, or shared notes unless the user's organization explicitly permits that workflow.

## Freshness

If this is a local CLI session and the repository checkout may be stale, you may run:

```bash
python scripts/ensure_fresh.py --max-age-hours 24
```

Run it only when the script exists and the repository is clean enough for a fast-forward update. Do not discard local changes.

## Routing

- Product/surface distinctions → `references/surfaces.md`
- Claude Code setup and context → `references/claude-code.md`
- Agent Skills → `references/agent-skills.md`
- MCP → `references/mcp.md`
- Prompting → `references/prompting.md`
- API / SDK → `references/api-routing.md`
- Model choice / volatile capability → `references/model-selection.md`
- Claude ↔ Codex/Gemini collaboration → `references/cross-agent-collaboration.md`
- Privacy / clinical context → `references/data-safety.md`
- Updating this pack → `workflows/update-knowledge-pack.md`

## Default output standard

State what is verified versus inferred. When current documentation matters, include the source or say that live verification was unavailable. Prefer short, actionable guidance over exhaustive restatement of documentation.
