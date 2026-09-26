---
name: ecosystem-guide
description: Claude/Anthropic ecosystem guide with dated, source-linked notes. Use when an answer depends on facts that change or differ by surface - whether a Skill, plugin, connector, setting or feature works in claude.ai chat, Cowork, Claude Code or the Claude API, and whether it syncs between them; where guidance belongs (CLAUDE.md, AGENTS.md, rules, Skills, subagents, hooks, MCP, plugins); current models, pricing, limits, plan availability or beta status; handing work between Claude and Codex/ChatGPT or Gemini; or updating the claude-knowledge pack. Not for general coding, stable concepts answerable from memory, other vendors' tools alone, or writing Claude API/SDK code (use the claude-api skill).
metadata:
  version: 0.2.0
  source: https://github.com/atsushi-matsuoka/claude-knowledge
---

# Claude ecosystem guide

Saved notes help with routing and design judgment. Current first-party Anthropic docs are the authority for product facts.

## 1. Decide how much to load

- **Stable concept** (what a context window is, how tool use works in general, prompt basics): answer from knowledge. Read nothing here.
- **Surface or placement question**: read the one matching reference below.
- **Volatile fact** (see §3): read the matching reference for context, then verify live before stating it as current.

Read at most the references the question needs. Never load the whole folder.

## 2. Pin the surface first

"Claude" can mean claude.ai chat, Cowork, Claude Code (terminal, IDE, desktop, cloud/web), the Claude API/Platform, or the Agent SDK. The same feature often differs between them. If the user's surface is unclear and the answer depends on it, say which surface each part applies to.

| Question is about | Read |
|---|---|
| Which surface supports or syncs what (Skills, plugins, connectors, sessions) | [references/surfaces.md](references/surfaces.md) |
| Where guidance belongs in Claude Code: CLAUDE.md, AGENTS.md, rules, Skills, subagents, hooks, MCP, plugins | [references/claude-code.md](references/claude-code.md) |
| Writing, naming, packaging, distributing or evaluating a Skill | [references/agent-skills.md](references/agent-skills.md) |
| MCP servers and connectors | [references/mcp.md](references/mcp.md) |
| Claude API / SDK work | [references/api-routing.md](references/api-routing.md) |
| Model choice, pricing, limits, availability | [references/model-selection.md](references/model-selection.md) |
| Prompting practice | [references/prompting.md](references/prompting.md) |
| Claude working with Codex/ChatGPT or Gemini | [references/cross-agent-collaboration.md](references/cross-agent-collaboration.md) |
| Clinical, patient or restricted data | [references/data-safety.md](references/data-safety.md) |
| Which source wins; official doc entry points | [references/source-policy.md](references/source-policy.md) |
| Updating this knowledge pack | [workflows/update-knowledge-pack.md](workflows/update-knowledge-pack.md) |

## 3. Freshness protocol

Volatile: model names/IDs, pricing, context windows, usage or rate limits, plan and region availability, beta/GA status, CLI commands and flags, config file names/paths/fields, per-surface support, data-retention settings.

For a volatile claim:

1. Note the `Last verified` date of the reference you read.
2. If web access exists, check the official page (entry points in `references/source-policy.md`) and answer from it, citing the URL.
3. If web access is unavailable, say so, give the saved claim with its `Last verified` date, and do not present it as guaranteed current.
4. If the official page contradicts the saved note, follow the official page and tell the user the pack's note looks stale (in this repository, propose the fix via `workflows/update-knowledge-pack.md`).

Official pages can lag each other. Prefer the most specific, most recently updated page for the exact surface.

## 4. Answer standard

- Label what was verified now, what comes from a dated note, and what is inference.
- Give short, actionable guidance; link the official page instead of restating it.
- Do not claim an install, sync, upload, or command succeeded unless it was run and checked.
- Never put patient-identifiable data, credentials, or organization-restricted material into prompts, Skills, repositories, or shared notes.
