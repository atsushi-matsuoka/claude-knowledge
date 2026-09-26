# Claude model selection

Last verified: 2026-09-23

Model availability and positioning change frequently. Do not maintain a rigid long-lived ranking here.

When selecting a Claude model:

1. Identify the task: conversational drafting, code implementation, difficult debugging/reasoning, long-agent run, latency-sensitive work, or cost-sensitive batch work.
2. Check the current Anthropic model documentation and the user's actual plan/surface.
3. Prefer the least expensive/fastest model that meets the quality requirement, then escalate for difficult design, debugging, or high-cost errors.
4. Distinguish model capability from product availability: a model may exist but not be enabled on a particular plan, surface, region, or account.

Do not infer availability from an old note. Verify it.

## Sources

- https://platform.claude.com/docs/en/about-claude/models/overview (models, IDs, context windows)
- https://platform.claude.com/docs/en/about-claude/pricing (API pricing)
- https://support.claude.com (plan usage limits and availability in claude.ai, Cowork and Claude Code)
