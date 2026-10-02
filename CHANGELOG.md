# Changelog

## 0.3.1 - 2026-10-02

- Reviewed the 2026-10-01 source-watch signals against current first-party documentation rather than treating fingerprint changes as behavior changes.
- Refreshed the dated model-selection snapshot for the current Claude Platform lineup.
- Clarified claude.ai account Skill synchronization into Cowork, cloud and signed-in Claude Code, including the terminal version/background-sync boundary and the documented Platform-vs-Code wording conflict.
- Recorded the bundled official `/claude-api` Skill as the preferred route for volatile Claude API/SDK reference material instead of duplicating it here.
- Rechecked current prompting guidance; no task-craft procedure, canonical eval case, generated eval, bootstrap, marketplace structure or source fetch URL changed.
- No new Claude Academy lesson body or exercise was promoted, and no Claude plugin eval or downstream model-effect comparison was run. task-craft effectiveness remains unmeasured.

## 0.3.0 - 2026-09-27

- Added `task-craft`: practical prompt/spec/workflow design, failure diagnosis, original examples and outcome evaluation, separate from product knowledge.
- Recorded exactly which public educational text and official docs were reviewed; Academy lesson completion and real-model effectiveness remain unclaimed.
- Added 24 task-craft routing/artifact cases and nine synthetic downstream fixtures with a strict offline scorer.
- Generalized validation, generated evals and bootstrap to multiple skills while preserving the existing ecosystem-guide cases and description.
- Registered the new method sources for monthly monitoring and refreshed fetch baselines.
- Existing historical handoffs and v0.2.0 measurement records remain unchanged below their new status notes. No automatic merge or paid evaluation.

- PR #2 review fixes: placeholder result rows and empty error messages are missing evidence, never completed comparisons; recorded execution failures remain distinct.
- Removed the version-pinned regression test, split version/frontmatter checks and added a coherent next-patch full-suite probe.
- Made the deadline example explicitly confirmed-only, with four static contract probes; no real-model effectiveness claim.

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
