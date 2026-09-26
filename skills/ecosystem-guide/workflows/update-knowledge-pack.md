# Workflow: update the knowledge pack

1. Identify the trigger: Academy learning, source-watch issue, user correction, or a newly released Claude capability.
2. Locate the smallest affected reference or workflow. Keep `SKILL.md` free of dated facts.
3. Check `sources/manifest.json` for the canonical page; add it if missing.
4. Read the current first-party page (append `.md` for clean Markdown when available).
5. Write concise original guidance; do not paste source text wholesale. Keep the `## Sources` list.
6. Update that file's `Last verified` date only for content you actually re-checked.
7. If behavior could regress, add or edit a case in `evals/questions.json` (`should_trigger`, `expect`, optional `reads`), then run `python scripts/build_evals.py`.
8. Run `python scripts/validate_repository.py` and `python -m unittest discover -s tests`.
9. For description or routing changes, run the Claude Code suite: `claude plugin eval . --trust-plugin --no-publish` (see README for a cheaper smoke run).
10. Review the diff for lost negations, limits, surface distinctions, or uncertainty. Bump `version` in `.claude-plugin/plugin.json` and add a `CHANGELOG.md` entry.
11. Open a reviewable PR; do not auto-merge knowledge changes.
