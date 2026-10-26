# Repository instructions (shared by Claude Code, Codex, Gemini CLI)

This repository is a knowledge-and-workflow pack about the Claude ecosystem, not an application. The **merged `main`** is the source of truth; PR branches and installed account copies are not.

- Two focused skills share this pack: `skills/ecosystem-guide/` for product facts/routing, and `skills/task-craft/` for applying prompting, specification and evaluation methods. Follow ecosystem-guide's `workflows/update-knowledge-pack.md` when maintaining either.
- Keep `SKILL.md` short and free of dated facts. Put detail and anything volatile in `references/`, each with `Last verified:` and a `## Sources` list.
- Current first-party Anthropic documentation beats saved notes and Academy material for product facts. Verify model names, pricing, limits, availability, beta status, commands and config paths before changing a claim.
- Do not copy Academy lessons or official docs wholesale; write short original summaries with source URLs.
- Do not mirror the Claude API reference; Anthropic's `claude-api` skill and the Platform docs cover it.
- Eval cases live in `evals/questions.json`. After editing them run `python scripts/build_evals.py`.
- After any change run `python scripts/validate_repository.py`, `python -m unittest discover -s tests` and `python scripts/check_sources.py --no-network` where executable; report failures and unrun checks honestly.
- Never add patient-identifiable data, credentials, secrets, or organization-restricted material.

- Preserve skill boundaries: simple direct tasks should not become prompt-design projects. Do not load product documentation for stable method application alone.
- Keep the existing ecosystem-guide cases and holdouts unchanged when extending task-craft. New cases select `skill` explicitly; generated suites remain generated.
- Distinguish Academy outlines, read lesson text, exercised notebooks and measured outcomes. Use `academy-notes/2026-09-27-practice-intake.md` and `evals/TASK_CRAFT.md`; do not claim Academy completion or model-quality gains without evidence.

## Authorized maintenance delivery

- The repository owner has authorized the biweekly maintainer to create, verify and **merge** bounded knowledge-pack maintenance PRs without asking again (2026-10-13). Use a branch and PR; do not push directly to `main`.
- Merge **only** if the exact PR head passed required CI, the diff and primary-source evidence were checked, there is no unresolved critical issue or conflicting work, and GitHub's required reviews/branch protections are satisfied. Do not self-approve, bypass protections or silently relax checks. Leave blocked/high-risk changes open and report why.
- After merging, re-fetch `main` and the PR to verify merge commit/actual content. A successful merge updates the GitHub source/marketplace, **not** an installed Claude/Cowork/Claude Code or other account: verify distribution/installation separately and never claim unobserved rollout.
- Do not initiate paid API/model evals, new authentications, account/plugin installation or deletion, or modifications outside this repository without separate explicit authorization.

## Atomic changes and CI notifications

- Prepare related files locally, run the required offline checks, then publish one coherent commit. In particular, update all version metadata and CHANGELOG entries together; do not publish them one file at a time.
- When using the GitHub API, create all blobs and a single tree/commit before moving the feature-branch ref once. Avoid sequential Contents API writes for a multi-file change.
- Validation runs for pull requests (including drafts) and pushes to `main`, not every unpublished feature-branch push. Open a PR only after the complete change passes local checks; batch follow-up fixes before each push. Do not use `[skip ci]` or weaken tests to suppress alerts.
- A new commit supersedes an older validation run for the same PR/ref. Real failures on the current PR head and merged `main` still fail normally. Source-watch scheduling and failure reporting remain enabled.
- Check CI for the exact final PR head before any separately authorized merge. GitHub notification subscriptions are not changed by this policy.
