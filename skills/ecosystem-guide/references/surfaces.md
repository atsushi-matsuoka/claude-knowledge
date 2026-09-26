# Claude product surfaces

Last verified: 2026-09-26

## Surfaces

- **claude.ai chat**: web, desktop and mobile conversations.
- **Cowork**: agentic tasks in the Claude desktop app; runs in an isolated environment and can write to the user's files.
- **Claude Code**: terminal, IDE extensions, the desktop app's Code tab, and cloud sessions (claude.ai/code, routines).
- **Claude API / Claude Platform**: programmatic access, including the Skills API and managed agents.
- **Agent SDK**: Claude Code's agent loop as a library.

## Where Skills come from, per surface

| Skill source | chat | Cowork | Claude Code (local) | Claude Code cloud | API |
|---|---|---|---|---|---|
| Enabled on the claude.ai account (uploaded or from a plugin) | yes | yes, synced at session start | yes when signed in with that account; downloaded to `~/.claude/skills/synced/` | yes | no |
| `~/.claude/skills/` (personal) | no | no | yes | no | no |
| Repository `.claude/skills/` | no | no | yes | yes | no |
| Plugin installed with `/plugin` or `claude plugin install` | no | no | yes, on that machine | no | no |
| Uploaded through the Skills API | no | no | no | no | yes |

Consequences:

- A skill uploaded on claude.ai is not "chat only" anymore: signed-in Claude Code, Cowork and cloud sessions receive it. Synced copies are download-only and never run `` !`command` `` injections.
- A personal `~/.claude/skills/` skill does not reach Cowork or cloud sessions. To cover them, enable it on the claude.ai account (or commit it to the repo for cloud sessions).
- The API has its own upload lifecycle; nothing syncs into or out of it.
- Older Platform pages still say custom Skills never sync across surfaces. The Claude Code skills page is newer and more specific for the account-sync case; re-check both when this matters.

## Plugins, per surface

A plugin folder installs everywhere, but each surface loads a subset:

- **Skills**: chat, Cowork and Claude Code.
- **Agents (subagents) and hooks**: Cowork and Claude Code; ignored in chat.
- **Remote MCP (http/sse)**: all three (connect it from the plugin's Connectors tab in chat/Cowork).
- **Local MCP (command)**: Cowork on the user's computer and Claude Code; ignored in chat.
- **Top-level `bin/`**: Claude Code only; makes chat and Cowork refuse the whole plugin.
- **Where to add**: chat/Cowork use Customize > Plugins (account-level; a GitHub repo can be added as a marketplace). Claude Code uses `/plugin` or `claude plugin` (machine-level). Account installs appear in Claude Code as synced plugins; CLI installs do not go back to the account.

## Rules

- Never assume something installed on one surface exists on another. Name the surface for each instruction.
- Distinguish "the model can do it" from "this plan, surface, or organization has it enabled".

## Sources

- https://code.claude.com/docs/en/skills (where skills live; Cowork and cloud; synced skills)
- https://claude.com/docs/plugins/platform-support (component support by app)
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview (API and upload constraints)
