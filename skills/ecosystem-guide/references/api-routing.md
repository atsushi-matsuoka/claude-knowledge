# Claude API routing

Last verified: 2026-10-26

For Claude API/SDK implementation, prefer current first-party references and Anthropic's official `claude-api` Agent Skill when it is available. That official skill is designed to supply up-to-date API reference material and language-specific SDK guidance.

This knowledge pack should contain only routing rules, cross-surface distinctions, and durable architectural practices. Do not mirror the full API reference here.

If the task involves exact model IDs, headers, beta versions, pricing, context limits, or endpoint schemas, live-verify the official Claude Platform docs before coding when possible.

Surface note: the `claude-api` skill is bundled with Claude Code. In chat or Cowork it may not be present; there, read the Platform docs directly (`https://platform.claude.com/llms.txt` is the index).

## October 2026 API version and SDK migration

On October 21, 2026, Anthropic released API version `2026-10-21`. New major versions of the official Claude client SDKs (including Python 2.0.0 and TypeScript 1.0.0) and `ant` CLI 2.0.0 send it by default; direct HTTP callers select it through the `anthropic-version` header. An existing pinned client/header has **not** automatically migrated.

Treat an SDK/CLI major upgrade as a behavior change, not only a dependency refresh. In API version `2026-10-21`, Messages, token counting and Message Batches reject `temperature`, `top_p` and `top_k` (even default values), directly embedded `document` blocks in assistant messages, and nonempty `citations` arrays on user text blocks. Some Admin/Enterprise Analytics response fields were renamed. New SDK/CLI versions also have independent breaking changes. Review Anthropic's exact migration tables and run regression tests **before** a production upgrade; do not assume any of these changes apply to every old API version or to the separate Claude Agent SDK. On Amazon Bedrock, the new API version is unavailable for Claude 4.6 and earlier: retain the prior version/client for those calls or migrate the model first.

## Anthropic-managed Claude on Google Cloud

Announced October 22, 2026, **Claude Models on Google Cloud (Anthropic managed)** is different from the existing Google-managed Claude offering. The new route is Anthropic-operated, uses Google Cloud IAM and OAuth credentials, and is billed through Google Cloud Marketplace; its client is `AnthropicGoogleCloud` (not `AnthropicVertex`). It needs an enabled project, the appropriate role and a workspace ID; an Anthropic API key alone is not the authentication mechanism. Feature support and migration differ: for example, MCP tunnels are not available in this route. Check the specific platform documentation, account entitlement and deployment before claiming availability or compatibility. Published documentation is not proof of a successful call or account setup.

## Managed Agents are a separate Platform surface

As of the October 9, 2026 Platform release notes, **dynamic workflows** are in beta for **Claude Managed Agents** (beta header `managed-agents-2026-04-01`). The relevant agent definition uses `multiagent.type: multiagent_20261001` and can enable `workflows.type: enabled`; multi-agent work runs server-side and exposes `workflow_run.*` events in the session stream. **Do not infer this feature exists in the Messages API, Agent SDK, Claude Code, or claude.ai chat.** Check the exact surface and entitlement before design or deployment.

For independent work that merits orchestration, set a session budget before running, and distinguish paused, failed and completed workflow runs. Prefer a single agent or a direct tool call for small tasks. Documentation of a beta is not evidence of account access, an executed run or improved real-world quality.

## Sources

- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/claude-api-skill
- https://platform.claude.com/docs/en/release-notes/overview
- https://platform.claude.com/docs/en/api/migration-2026-10-21
- https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed
- https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration
- https://platform.claude.com/docs/en/managed-agents/workflow-runs
