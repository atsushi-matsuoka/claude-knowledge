# Install and discover only in a supported host

Last verified: 2026-09-28

The OpenAI build-skills guide describes a SKILL.md with a name and description, detailed instructions loaded when needed, and local discovery including ~/.agents/skills. It supports symlinked skill directories. This pack supplies openai.yaml display metadata; it is not an account installation receipt.

This pack's bootstrap links only openai-guide and gpt-workbench from a known checkout. It refuses to replace unrelated content and only refreshes a clean main branch with the expected origin. Use the parent README installation section for pack-relative commands. A portable folder can be installed on another supported host, but its discovery paths and permissions must be checked there.

For ordinary ChatGPT chats, a Project instruction can request selective GitHub reads. That is a fallback retrieval policy, not a guarantee of native Skill activation or model switching. The current session must expose the connector and actually obtain the named file. Restart or reload a local host when its discovered skill list has not refreshed.

Do not duplicate or overwrite an existing optimize-model-prompt skill before reading its real contents and agreeing on ownership. The existing weekly automation was found; that personal skill's contents were not obtained during this implementation.

## Sources

- https://learn.chatgpt.com/docs/build-skills
- https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex
