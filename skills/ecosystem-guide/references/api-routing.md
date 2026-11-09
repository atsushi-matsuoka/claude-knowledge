# Claude API routing

Last verified: 2026-11-09

For Claude API/SDK implementation, prefer current first-party references and Anthropic's official `claude-api` Agent Skill when it is available. That official skill is designed to supply up-to-date API reference material and language-specific SDK guidance.

This knowledge pack should contain only routing rules, cross-surface distinctions, and durable architectural practices. Do not mirror the full API reference here.

If the task involves exact model IDs, headers, beta versions, pricing, context limits, or endpoint schemas, live-verify the official Claude Platform docs before coding when possible.

Surface note: the `claude-api` skill is bundled with Claude Code. In chat or Cowork it may not be present; there, read the Platform docs directly (`https://platform.claude.com/llms.txt` is the index).

## October 2026 API version and SDK migration

On October 21, 2026, Anthropic released API version `2026-10-21`. New major versions of the official Claude client SDKs (including Python 2.0.0 and TypeScript 1.0.0) and `ant` CLI 2.0.0 send it by default; direct HTTP callers select it through the `anthropic-version` header. An existing pinned client/header has **not** automatically migrated.

Treat an SDK/CLI major upgrade as a behavior change, not only a dependency refresh. In API version `2026-10-21`, Messages, token counting and Message Batches reject `temperature`, `top_p` and `top_k` (even default values), directly embedded `document` blocks in assistant messages, and nonempty `citations` arrays on user text blocks. Some Admin/Enterprise Analytics response fields were renamed. New SDK/CLI versions also have independent breaking changes. Review Anthropic's exact migration tables and run regression tests **before** a production upgrade; do not assume any of these changes apply to every old API version or to the separate Claude Agent SDK. On Amazon Bedrock, the new API version is unavailable for Claude 4.6 and earlier: retain the prior version/client for those calls or migrate the model first.

## Anthropic-managed Claude on Google Cloud

Announced October 22, 2026, **Claude Models on Google Cloud (Anthropic managed)** is different from the existing Google-managed Claude offering. The new route is Anthropic-operated, uses Google Cloud IAM and OAuth credentials, and is billed through Google Cloud Marketplace; its client is `AnthropicGoogleCloud` (not `AnthropicVertex`). It needs an enabled project, the appropriate role and a workspace ID; an Anthropic API key alone is not the authentication mechanism. Feature support and migration differ: for example, MCP tunnels are not available in this route. Check the specific platform documentation, account entitlement and deployment before claiming availability or compatibility. Published documentation is not proof of a successful call or account setup.

## November 2026: Messages API threads (beta)

Released November 2: **message threads** are a Messages API feature, not Claude chat/Cowork memory or Managed Agents sessions. With beta header `message-threads-2026-08-12`, the first request supplies the full conversation and `thread: {type: "create"}`; subsequent requests send the new messages and the previous response ID. A thread is append-only and expires 5 minutes after its last request, with deletion no more than 1 hour after last use. Keep an independent full conversation copy and a replay path when continuation returns `thread_not_found`; the SDK helper keeps its own copy only in memory. Threaded requests are **not ZDR eligible and not HIPAA eligible**, and the feature rejects HIPAA-ready organizations, Message Batches, and compaction. It does not change pricing or rate limits. Availability depends on API surface and entitlement; do not use it for restricted clinical content without an independently approved data-handling basis.

## November 2026: organization administration and usage

- October 29: the **Usage and Cost Analytics API** is a beta for Claude Console and Claude Enterprise organizations (header `analytics-usage-cost-2026-08-24`). It can group spend and requests by model, workspace or actor. Earlier Usage and Cost / Enterprise report APIs are **legacy but still supported**; migrate only when the dimensions or reporting format justify it. Admin API permissions and Enterprise analytics scopes differ.
- November 5: organization **IP allowlisting** is in beta. Console and Enterprise cover different endpoints and apps; cloud-hosted offerings such as Bedrock, Claude Platform on AWS and Google Cloud are not covered by this Claude Console allowlist. Restricting IPs can lock out owners, workers and mobile users. Plan allowed egress ranges and an admin recovery path before enabling it. The Admin API can also sign out Enterprise members everywhere (beta), but this does not remove their membership. No organization security settings were changed here.
- November 3: Anthropic introduced **text watermarking** on specified model/platform combinations. The watermark is not an extra visible token; on Sonnet 4.6, non-default sampling parameters can affect whether it is present. Check the exact coverage list and do not infer that every response is watermarked.

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
- https://platform.claude.com/docs/en/build-with-claude/message-threads
- https://platform.claude.com/docs/en/manage-claude/usage-cost-analytics-api
- https://platform.claude.com/docs/en/manage-claude/ip-allowlist
- https://platform.claude.com/docs/en/build-with-claude/text-watermark
