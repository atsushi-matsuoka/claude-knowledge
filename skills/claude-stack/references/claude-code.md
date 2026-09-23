# Claude Code practices

Last verified: 2026-09-23

- Keep `CLAUDE.md` focused on rules and context that should be present every session.
- Put occasional reference material and repeatable workflows in Skills so they load on demand.
- Prefer project-local configuration when behavior is project-specific; use user-level skills for durable expertise that should follow the user across projects.
- Do not overfill persistent instructions. Long always-on context can reduce adherence and waste tokens.
- Before recommending exact paths, commands, or configuration fields, check current Claude Code docs if network access is available.
- For Claude API coding, use the official bundled `claude-api` skill where available rather than maintaining a second API manual here.
