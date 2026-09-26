# Claude Code: where guidance belongs

Last verified: 2026-09-26

## Placement

| Need | Put it in | Context cost |
|---|---|---|
| Facts/rules needed every session (build commands, conventions) | `CLAUDE.md` | every request |
| Rules only for some files | `.claude/rules/*.md` with `paths:` globs | only when matching files are touched |
| Reference material or a repeatable procedure | a Skill | description every request; body when used |
| Noisy side task, parallel research | a subagent (`.claude/agents/`) | isolated; only the summary returns |
| Something that must happen every time, deterministically | a hook | zero unless it returns context |
| Live external data or actions | an MCP server | tool names at start; schemas on demand |
| The same setup across repos or people | a plugin | its skills/agents descriptions every request |

Guidance in `CLAUDE.md` is advisory context. To block an action regardless of what the model decides, use a `PreToolUse` hook.

## Sizes and limits worth checking before advising

- `CLAUDE.md`: target under 200 lines per file. `@path` imports still load at launch, so they organize but do not save context.
- Skill listing: `description` + `when_to_use` truncated at 1,536 characters combined; keep the key use case first.
- `SKILL.md`: keep under 500 lines; move detail into files it links to.
- Once invoked, a skill's content stays in context for the session (re-attached, with a budget, after compaction).

## AGENTS.md interoperability

- Claude Code reads `AGENTS.md` only when no `CLAUDE.md`/`.claude/CLAUDE.md`/`CLAUDE.local.md` exists in the working directory or above (default setting; needs a recent version).
- To share one file across agents, put `@AGENTS.md` at the top of `CLAUDE.md` and add Claude-only notes below it. A symlink also works but breaks on Windows clones.

## Skill frontmatter that only Claude Code understands

`when_to_use`, `disable-model-invocation`, `user-invocable`, `paths`, `context: fork`, `agent`, `model`, `effort`, `hooks`, `arguments`, `allowed-tools` pre-approval, `` !`cmd` `` injection, `${CLAUDE_SKILL_DIR}`. Skills that must also upload to claude.ai or the API should use only the Agent Skills spec fields (`name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`); other fields fail packaging.

## Sources

- https://code.claude.com/docs/en/features-overview
- https://code.claude.com/docs/en/memory
- https://code.claude.com/docs/en/skills
