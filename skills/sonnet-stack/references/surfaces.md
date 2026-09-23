# Claude product surfaces

Last verified: 2026-09-23

## claude.ai

Interactive Claude product surface. Custom Skills can be uploaded for individual use on eligible plans. Skills on claude.ai are managed separately from Claude Code filesystem skills and Claude API uploaded skills.

## Claude Code

Local/terminal coding agent. Project and personal Skills are filesystem-based. Claude Code can discover custom skills from project or user locations. Project instructions such as `CLAUDE.md` are persistent context, while Skills are better for on-demand reference/workflows.

## Claude API / Claude Platform

Programmatic surface. Custom Skills uploaded to the API are a separate lifecycle from claude.ai and Claude Code. API Skills run in a managed code-execution environment and have environment-specific constraints.

## Rule

Never assume a Skill installed on one surface automatically exists on another. When a user says "Claude", determine which surface is relevant before giving setup instructions.
