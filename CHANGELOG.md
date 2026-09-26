# Changelog

## 0.2.0 - 2026-09-26

- Renamed the skill `claude-stack` -> `ecosystem-guide`: Agent Skills names may not contain `claude`/`anthropic`, so the old name could not be uploaded to claude.ai or the API.
- Packaged the repository root as a Claude plugin with a GitHub marketplace (`.claude-plugin/`), so one install reaches claude.ai chat, Cowork and Claude Code.
- Rewrote `SKILL.md`: narrower third-person trigger description with explicit "not for" cases, an answer-from-memory path for stable concepts, surface-first routing table, and a freshness protocol with official entry points. Dated facts moved out of `SKILL.md`.
- Re-verified and expanded `surfaces.md`, `claude-code.md`, `agent-skills.md`, `source-policy.md`, `cross-agent-collaboration.md` (Codex/Gemini skill paths) against current docs; corrected the stale claim that claude.ai Skills never reach Claude Code.
- Evals: `questions.json` schema v2 (`should_trigger`, `reads`), 22 new cases (10 held out, 10 should-not-trigger in total), and a generated `claude plugin eval` suite with trigger, routing and rubric graders; `scripts/summarize_evals.py` reports recall, false-trigger rate and routing accuracy. Measured on held-out cases: trigger recall 33% -> 100%, routing 33% -> 100%, answer pass 42% -> 83%, no false triggers (`evals/RESULTS.md`).
- Validator now enforces spec constraints (reserved words, portable frontmatter, sizes, one-level links, dated references), manifest/version consistency, eval drift and secret patterns. Added unit tests.
- Source watch hashes clean Markdown (`.md`) or tag-stripped HTML, tracks 8 more official pages, and names the references to review for each change.
- `CLAUDE.md` and `GEMINI.md` now import `AGENTS.md` instead of duplicating it. Bootstrap links `~/.agents/skills` by default; the Claude Code personal link is opt-in (`--claude-code`) to avoid duplicating the plugin.

## 0.1.1 - 2026-09-23

- Renamed the cross-agent skill from `sonnet-stack` to `claude-stack` to reflect that it covers the full Claude ecosystem, not only Sonnet models.
- Updated local install paths, validation, and freshness cache naming accordingly.

## 0.1.0 - 2026-09-23

- Initial cross-agent `sonnet-stack` skill.
- Added Academy curriculum map and note-ingestion policy.
- Added Claude / Codex / Gemini local bootstrap and sync design.
- Added monthly first-party source watcher and repository validation workflow.
- Added initial eval set for routing, freshness, surface distinctions, and cross-agent collaboration.
