# Claude API routing

Last verified: 2026-09-23

For Claude API/SDK implementation, prefer current first-party references and Anthropic's official `claude-api` Agent Skill when it is available. That official skill is designed to supply up-to-date API reference material and language-specific SDK guidance.

This knowledge pack should contain only routing rules, cross-surface distinctions, and durable architectural practices. Do not mirror the full API reference here.

If the task involves exact model IDs, headers, beta versions, pricing, context limits, or endpoint schemas, live-verify the official Claude Platform docs before coding when possible.

Surface note: the `claude-api` skill is bundled with Claude Code. In chat or Cowork it may not be present; there, read the Platform docs directly (`https://platform.claude.com/llms.txt` is the index).
