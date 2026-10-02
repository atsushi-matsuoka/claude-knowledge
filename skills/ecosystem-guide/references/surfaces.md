# Claude product surfaces

Last verified: 2026-10-02

## Surfaces

- **claude.ai chat**: web, desktop and mobile conversations.
- **Cowork**: agentic tasks in the Claude desktop app; runs in an isolated environment and can write to the user's files.
- **Claude Code**: terminal, IDE extensions, the desktop app's Code tab, and cloud sessions (claude.ai/code, routines).
- **Claude API / Claude Platform**: programmatic access, including the Skills API and managed agents.
- **Agent SDK**: Claude Code's agent loop as a library.

## Where Skills come from, per surface

| Skill source | chat | Cowork | Claude Code (local) | Claude Code cloud | API |
|---|---|---|---|---|---|
| Enabled on the claude.ai account (uploaded or from a plugin) | yes | yes, loaded for the session | yes when signed in with that account; recent versions sync to `~/.claude/skills/synced/` | yes | no |
| `~/.claude/skills/` (personal) | no | no | yes | no | no |
| Repository `.claude/skills/` | no | no | yes | yes | no |
| Plugin installed with `/plugin` or `claude plugin install` | no | no | yes, on that machine | no | no |
| Uploaded through the Skills API | no | no | no | no | yes |

Consequences:

- Cowork and Claude Code cloud sessions load skills enabled for the claude.ai account at session start.
- In terminal Claude Code, account-skill sync requires Claude Code v2.1.273+ and a claude.ai sign-in. At session start the client downloads account skills to `~/.claude/skills/synced/` in the background and then checks for changes about every 10 minutes; additions, edits and removals can update a running session without a restart.
- A short non-interactive terminal run can finish before background sync completes. Set `CLAUDE_CODE_SYNC_SKILLS=1` when the run must wait for the account skill list. API-key authentication, Bedrock/no-feature-flag sessions, bare mode, safe mode and some managed-setting configurations do not perform this sync.
- Synced copies are download-only. Editing `~/.claude/skills/synced/` does not upload changes to claude.ai, and a later sync can overwrite local edits.
- A personal `~/.claude/skills/` skill does not reach Cowork or cloud sessions. To cover them, enable it on the claude.ai account (or commit it to the repo for cloud sessions).
- The API has its own upload lifecycle; nothing syncs into or out of it.
- The Claude Platform Agent Skills overview still says custom Skills do not sync across surfaces, while the newer, surface-specific Claude Code docs describe claude.ai account skills syncing into Cowork, cloud and signed-in terminal sessions. For those Claude Code/account-sync details, follow the more specific Claude Code page; keep the API lifecycle separate.

## Plugins, per surface

A plugin folder installs everywhere, but each surface loads a subset:

- **Skills**: chat, Cowork and Claude Code.
- **Agents (subagents) and hooks**: Cowork and Claude Code; ignored in chat.
- **Remote MCP (http/sse)**: all three (connect it from the plugin's Connectors tab in chat/Cowork).
- **Local MCP (command)**: Cowork on the user's computer and Claude Code; ignored in chat.
- **Top-level `bin/`**: Claude Code only; makes chat and Cowork refuse the whole plugin.
- **Where to add**: chat/Cowork use Customize > Plugins (account-level; a GitHub repo can be added as a marketplace). Claude Code uses `/plugin` or `claude plugin` (machine-level).
- An account-installed plugin appears in Claude Code as a synced plugin at the next session start. A plugin installed from the Claude Code command line stays on that machine and is not added back to the account.

## Rules

- Never assume something installed on one surface exists on another. Name the surface for each instruction.
- Distinguish "the model can do it" from "this plan, surface, or organization has it enabled".

## Sources

- https://code.claude.com/docs/en/skills (where skills live; Cowork/cloud behavior and claude.ai account sync)
- https://claude.com/docs/plugins/platform-support (component support and plugin install/sync direction)
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview (API and upload constraints; note the cross-surface wording conflict above)
