# Repository instructions for Codex

This repository is a knowledge-and-workflow pack, not an application.

- Use the `claude-stack` skill when editing Claude/Anthropic knowledge or workflows.
- Keep `SKILL.md` concise. Put detailed or volatile material in `references/`.
- Prefer current first-party Anthropic documentation over saved summaries when they conflict.
- Do not duplicate the full Anthropic API reference; Claude Code already bundles Anthropic's `claude-api` skill.
- Treat Academy notes as learning input, not canonical product documentation.
- Do not copy course lessons or official docs wholesale. Write concise original summaries and retain source URLs.
- For model names, pricing, rate/usage limits, feature availability, and beta status, verify the current official source before changing a factual claim.
- Run `python scripts/validate_repository.py` after structural changes.
- When source monitoring reports a change, update only claims that can be tied to current first-party evidence.
- Never add patient-identifiable data, credentials, secrets, or organization-restricted clinical data.
