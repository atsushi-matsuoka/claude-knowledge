# Repository instructions (shared by Claude Code, Codex, Gemini CLI)

This repository is a knowledge-and-workflow pack about the Claude ecosystem, not an application. GitHub is the reviewed source of truth.

- Two focused skills share this pack: `skills/ecosystem-guide/` for product facts/routing, and `skills/task-craft/` for applying prompting, specification and evaluation methods. Follow ecosystem-guide's `workflows/update-knowledge-pack.md` when maintaining either.
- Keep `SKILL.md` short and free of dated facts. Put detail and anything volatile in `references/`, each with `Last verified:` and a `## Sources` list.
- Current first-party Anthropic documentation beats saved notes and Academy material for product facts. Verify model names, pricing, limits, availability, beta status, commands and config paths before changing a claim.
- Do not copy Academy lessons or official docs wholesale; write short original summaries with source URLs.
- Do not mirror the Claude API reference; Anthropic's `claude-api` skill and the Platform docs cover it.
- Eval cases live in `evals/questions.json`. After editing them run `python scripts/build_evals.py`.
- After any change run `python scripts/validate_repository.py` and `python -m unittest discover -s tests`.
- Never add patient-identifiable data, credentials, secrets, or organization-restricted material.

- Preserve skill boundaries: simple direct tasks should not become prompt-design projects. Do not load product documentation for stable method application alone.
- Keep the existing ecosystem-guide cases and holdouts unchanged when extending task-craft. New cases select `skill` explicitly; generated suites remain generated.
- Distinguish Academy outlines, read lesson text, exercised notebooks and measured outcomes. Use `academy-notes/2026-09-27-practice-intake.md` and `evals/TASK_CRAFT.md`; do not claim Academy completion or model-quality gains without evidence.
