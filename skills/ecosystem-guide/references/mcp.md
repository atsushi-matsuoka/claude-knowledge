# MCP with Claude

Last verified: 2026-09-23

Use MCP when the task needs live external tools or data. Use a Skill when the task needs reusable instructions, decision logic, references, or a repeatable workflow. They are complementary: MCP exposes capabilities; a Skill can teach the agent when and how to use them.

Before giving setup commands, verify the current Claude Code / Claude Platform MCP documentation because transport options, configuration locations, and authentication patterns can change.

Security: treat MCP servers as code/data integrations with real permissions. Prefer least privilege, explicit authentication boundaries, and trusted servers. Do not embed secrets in knowledge files.

## Sources

- https://code.claude.com/docs/en/mcp
- https://claude.com/docs/connectors/overview (connectors in claude.ai and Cowork)
