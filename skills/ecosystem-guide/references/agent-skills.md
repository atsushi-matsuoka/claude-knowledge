# Agent Skills: authoring, packaging, evaluating

Last verified: 2026-09-26

A Skill is a folder with `SKILL.md` plus optional scripts, references and assets. The host shows only `name` + `description` until the skill is relevant, then loads the body, then linked files on demand (progressive disclosure).

## Hard constraints (Agent Skills spec / Claude Platform)

- `name`: max 64 chars, lowercase letters, digits, hyphens; no XML tags; must not contain the reserved words `anthropic` or `claude`. Hosts that only read files (Claude Code, Codex, Gemini CLI) may accept such names, but claude.ai and API uploads reject them.
- `description`: non-empty, max 1,024 chars, no XML tags, third person, states what it does and when to use it.
- Portable frontmatter: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. Anything else is host-specific.
- Host listing budgets are separate from the spec limit: Claude Code truncates `description` + `when_to_use` at 1,536 characters combined in its skill listing. Other hosts may truncate differently.

## Writing guidance

- The description is the trigger. Put concrete trigger situations first; add explicit "not for" cases to stop over-triggering.
- Body under 500 lines. Link references one level deep from `SKILL.md`; add a table of contents to references over 100 lines.
- Write for a capable model: state decisions and constraints, not tutorials. Keep dated facts in references with a `Last verified` line, not in the body.
- Scripts for fragile, deterministic steps; prose for judgment.

## Distribution options

- **Claude, everywhere at once**: package as a plugin in a GitHub marketplace and add it in claude.ai Customize > Plugins; it reaches chat, Cowork and (synced) Claude Code.
- **Claude Code only**: `~/.claude/skills/<name>/`, repo `.claude/skills/`, or a plugin via `/plugin marketplace add owner/repo`.
- **Other agents**: Codex and Gemini CLI read `~/.agents/skills/<name>/` (check their current docs).
- **API**: upload through the Skills API separately.

## Evaluating

- Build a few realistic prompts first, including prompts that should *not* trigger the skill, and measure without the skill as a baseline.
- Claude Code ships `claude plugin eval`: per-case `prompt.md` plus graders (`tool_used` with `tool: Skill` to check triggering, `llm` rubrics for answer quality). It runs with and without the plugin and reports the delta. Check `claude plugin eval --help` for current flags.
- Test with every model you expect to use; smaller models need more explicit guidance.

## Sources

- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/plugin-evals
