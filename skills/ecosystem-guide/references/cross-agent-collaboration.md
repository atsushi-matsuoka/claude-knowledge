# Claude ↔ Codex ↔ Gemini collaboration

Last verified: 2026-09-26

## Default pattern

Use a shared artifact as the handoff boundary:

1. Discovery / requirement shaping.
2. `SPEC.md` with goal, scope, constraints, non-goals, acceptance criteria, and tests.
3. Implementation by the execution agent.
4. Independent review by a different model when failure cost justifies it.
5. The implementation agent verifies review findings and fixes only valid issues.

Avoid asking one model to generate a huge "perfect prompt" for another when a stable specification would work better.

## Suggested roles for a non-engineer

- Conversational model: clarify the rough idea and expose decisions.
- Codex / coding agent: implement, run tests, inspect failures, and produce a concrete result.
- Claude or another independent model: review design, UX, edge cases, or code when independent critique is valuable.

The roles are not fixed by brand. Re-evaluate them on real tasks and eval results.

## Sharing one skill with other agents

The same Agent Skills folder works across hosts; only discovery paths differ.

| Host | User-level path | Repo-level path | Notes |
|---|---|---|---|
| Codex | `$HOME/.agents/skills/<name>` | `.agents/skills/` from cwd up to repo root | symlinked skill folders are followed |
| Gemini CLI | `~/.gemini/skills/` or the `~/.agents/skills/` alias | `.gemini/skills/` or `.agents/skills/` | asks for consent before activating a skill; `gemini skills link` / `install` also exist |
| Claude | plugin marketplace or claude.ai account (see `surfaces.md`) | `.claude/skills/` | `~/.claude/skills/` reaches local Claude Code only |

For this pack, `scripts/bootstrap.py` clones or fast-forwards the GitHub repo and links `~/.agents/skills/ecosystem-guide`, which serves Codex and Gemini CLI together. It never resets or discards local changes; a dirty checkout is left alone and reported.

Being signed in to the same account does not give a local agent your private repositories. Discovery uses local paths: the repo must be cloned (with Git credentials) or reached through a configured connector.

## Shared knowledge

Use GitHub as the reviewed source of truth. Local agent skill installations should point to or sync from that repository. Use Google Drive as a learning inbox and human-readable archive, not a competing canonical copy.

## Sources

- https://learn.chatgpt.com/docs/build-skills (Codex skill locations)
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md (Gemini CLI skills)
