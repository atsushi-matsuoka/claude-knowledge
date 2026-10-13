# Workflow: update the knowledge pack

1. Identify the trigger: Academy learning, source-watch issue, user correction, or a newly released Claude capability.
2. Locate the smallest affected reference or workflow. Keep `SKILL.md` free of dated facts.
3. Check `sources/manifest.json` for the canonical page; add it if missing.
4. Read the current first-party page (append `.md` for clean Markdown when available).
5. Write concise original guidance; do not paste source text wholesale. Keep the `## Sources` list.
6. Update that file's `Last verified` date only for content you actually re-checked.
7. If behavior could regress, add or edit a case in `evals/questions.json` (`should_trigger`, `expect`, optional `reads`), then run `python scripts/build_evals.py`.
8. Run `python scripts/validate_repository.py`, `python -m unittest discover -s tests`, and `python scripts/check_sources.py --no-network`. Record each result and warning; never report an unrun command as passed.
9. For description or routing changes, propose a Claude Code suite (`claude plugin eval . --trust-plugin --no-publish`); run paid model calls only with explicit approval. Otherwise record real-model effects as unmeasured.
10. Review the diff for lost negations, limits, surface distinctions, or uncertainty. Bump `version` in `.claude-plugin/plugin.json` and add a `CHANGELOG.md` entry when appropriate.
11. Before opening a PR, inspect existing open PRs for the same purpose. Reuse/update a matching PR rather than duplicate it, and never push to `main`.
12. **Complete the GitHub handoff in this run:** use an authenticated GitHub PR creation/update operation, with `main` as base and the change branch as head. Include the official source URLs, file scope, observed test results, warnings, and unmeasured/uninstalled status. A pushed branch, compare URL, or suggested manual PR is **not** a completed PR. If creation fails, inspect the error and retry through another supported, authorized GitHub operation; never bypass permissions or claim success without a PR URL.
13. **Check the exact PR head:** read back the PR number/URL, open state, base/head, head SHA, diff, required reviews and CI for that SHA. Fix failed checks within scope and rerun them. Do not confuse a pending check, unchecked claim or an informational warning with success.
14. **Complete the owner-authorized merge:** the biweekly maintainer has standing approval (2026-10-13) to merge its reviewed maintenance PR after required CI and GitHub reviews pass, with no critical unresolved findings or conflicting PRs. Merge using the observed head SHA as an optimistic lock; never bypass required approvals, force a merge, write directly to `main`, or auto-merge an unverified/high-risk change. If blocked, leave the PR open and explain exactly why.
15. **Verify publication separately from installation:** re-fetch the merged PR and `main` commit/content to prove the knowledge-pack and GitHub marketplace source are updated. Do not claim Claude chat/Cowork/Claude Code account installs, version sync, API availability or measured quality without actual checks. This automation does not change account installations, login credentials, billing or paid evals. If there is no substantive diff, finish without a PR or success notification.

## Practice-layer additions

- For task-craft, start from an actual failure or a retrieved educational section. Record source coverage and whether it was only an outline, read text, exercised material or a measured behavior.
- Convert a learned principle into an original procedure, example and acceptance check. Do not add prose merely to enlarge the knowledge base.
- Put dated practical guidance in task-craft references. Stable method application does not require a live fetch on every user task; version-specific product claims still do.
- New task-craft cases in questions.json use `skill: task-craft`. Preserve the existing ecosystem-guide cases and untouched holdouts. Rebuild generated cases.
- Separate activation/artifact grading from downstream task results. Follow evals/TASK_CRAFT.md; without a real model run report effect unmeasured. Never run paid evaluation automatically.
- Keep every skill metadata.version, plugin.json version and top CHANGELOG entry aligned. New fetch_url entries require an actual baseline refresh; keep failed retrievals visible.
- Do not edit historical handoffs. Merge only under the owner's bounded authorization and mandatory checks/reviews; do not claim that a PR or merged repo change is installed on the user's accounts.
