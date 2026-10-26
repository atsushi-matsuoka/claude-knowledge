# Changelog

## Unreleased — CI maintenance

- Validate PR updates and pushes to main rather than every feature-branch push; cancel superseded validation runs while preserving current-head failures.
- Document atomic multi-file commits to avoid incomplete version updates and duplicate CI notifications. Plugin/Skill content and versions are unchanged.

## 0.3.4 - 2026-10-26

- Added guarded migration routing for Claude API version `2026-10-21` (October 21), including new SDK/`ant` CLI defaults, request validation and Bedrock compatibility cautions; no production migration or API test was performed.
- Distinguished October 22's Anthropic-managed Claude Models on Google Cloud from Google-managed Claude, including IAM/OAuth versus API-key authentication, billing, client routing and account-access caveats.
- Re-checked the official October 26 model lineup, base/cache pricing and Sonnet 4.5 retirement schedule; no model replacements or pricing changes were made. Source-watch fingerprints remain review signals, not proof of changed behavior.
- No `sources/manifest.json` fetch_url, eval-case, marketplace name, Skill name or bootstrap change; plugin/Skill versions aligned. No paid model calls, account plugin installation/sync, or task-craft effectiveness evaluation.

## 0.3.3 - 2026-10-12

- Clarified Anthropic's staged chat/Cowork integration versus per-surface plugin and execution support; user/account rollout must be verified.
- Routed the October 9 Claude Managed Agents dynamic workflow beta to its separate Platform surface with budget/run-state cautions; did not duplicate API docs or authorize model calls.
- Clarified marketplace account-update controls versus the one-time manual plugin-name migration. No account update or plugin installation was attempted.
- Kept current model IDs and 2026-10-11 model guidance, Skill routing, eval cases, marketplace/plugin names and repository visibility unchanged. No real-model evaluation was run.

## 0.3.2 - 2026-10-11

- Re-verified Claude Fable 5.1, Opus 5.5, Sonnet 5.5 and Haiku 5.5 against official model IDs, availability caveats, context/output limits, thinking modes and API pricing, including Haiku's 100K-token pricing boundary and model-specific cache-read rates.
- Documented Claude Sonnet 4.5 deprecation (2026-09-30), planned retirement (2026-11-30 on Anthropic-operated platforms), and the need to check provider-specific schedules and migration/Claude Code compatibility.
- Updated the README's illustrative Claude plugin eval model from Sonnet 5 to Sonnet 5.5; the example does not assert a successful paid model evaluation.
- No model benchmark, account activation, plugin installation, or automatic merge was performed.

## 0.3.1 - 2026-10-10

- Moved the Anthropic official-source fingerprint watcher from monthly to weekly (Sunday 09:30 JST), ahead of the separately scheduled biweekly full knowledge review.
- Kept source changes as review signals, with no automatic knowledge rewrite, PR merge or installed-plugin update.
- Renamed the third-party plugin package from `claude-knowledge` to `matsuoka-knowledge-pack` to satisfy current Claude Code reserved-name rules; existing installations need a one-time migration (README). Marketplace name, repository URL and Skill names remain unchanged.

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
