# Claude model selection

Last verified: 2026-10-02

Model availability and positioning change frequently. Do not turn this snapshot into a permanent ranking.

## Current API / Platform snapshot

| Model | Current positioning | Claude API ID | Context / max output | Base API price (input / output MTok) |
|---|---|---|---|---|
| Claude Fable 5.1 | Demanding reasoning and long-horizon agentic work | `claude-fable-5-1` | 1M / 128K | $10 / $50 |
| Claude Opus 5.5 | Start here for most workloads; long-running agentic coding and knowledge work | `claude-opus-5-5` | 1M / 128K | $4 / $20 |
| Claude Sonnet 5.5 | Best combination of speed and intelligence | `claude-sonnet-5-5` | 1M / 128K | $2 / $10 |
| Claude Haiku 4.5 | Fastest current model; near-frontier intelligence | `claude-haiku-4-5-20251001` (alias `claude-haiku-4-5`) | 200K / 64K | $1 / $5 |

This table is the current Claude Platform view, not proof that a particular claude.ai plan, region, organization, cloud provider or account exposes the same choices. Effort defaults and availability also differ by surface; verify the exact surface before advising a user.

## Selection procedure

1. Identify the task: conversational drafting, code implementation, difficult debugging/reasoning, long-agent run, latency-sensitive work, or cost-sensitive batch work.
2. Check the current Anthropic model documentation and the user's actual plan/surface.
3. Start from the documented default candidate, then prefer the least expensive/fastest model that meets the task's measured quality requirement. Escalate when evals or the failure cost justify it.
4. Distinguish model capability from product availability: a model may exist but not be enabled on a particular plan, surface, region, provider, or account.
5. For a long-lived integration, check model lifecycle/deprecation information rather than assuming a current model remains available.

Do not infer availability from this dated snapshot. Verify it.

## Sources

- https://platform.claude.com/docs/en/models/overview (current lineup, IDs, context windows, base pricing)
- https://platform.claude.com/docs/en/models/fable-5-1/overview
- https://platform.claude.com/docs/en/models/opus-5-5/overview
- https://platform.claude.com/docs/en/models/sonnet-5-5/overview
- https://platform.claude.com/docs/en/models/haiku-4-5/overview
- https://platform.claude.com/docs/en/about-claude/pricing (complete API pricing, caching and batch details)
- https://support.claude.com (plan usage limits and availability in claude.ai, Cowork and Claude Code)
