# Claude model selection

Last verified: 2026-10-11

Models change. Verify official documentation and the actual platform, provider, plan and account before recommending or pinning a model. This October 11, 2026 snapshot does not establish personal access or measured task quality.

## Current Claude API lineup (October 11, 2026 JST)

| Model and release | API ID | Base USD / million input-output tokens | Thinking / default effort |
| --- | --- | --- | --- |
| Fable 5.1, Sep 1 | `claude-fable-5-1` | $10 / $50 | Adaptive always on / high |
| Opus 5.5, Sep 22 | `claude-opus-5-5` | $4 / $20 | Adaptive always on / medium |
| Sonnet 5.5, Sep 28 | `claude-sonnet-5-5` | $2 / $10 | Adaptive / high |
| Haiku 5.5, Oct 7 | `claude-haiku-5-5` | From $0.10 / $0.50 | Adaptive / medium |

All four have a documented **1M context window and 128K standard maximum output**. Anthropic suggests Opus 5.5 for most workloads; evaluate Fable 5.1 for demanding reasoning/long agent runs, Sonnet 5.5 for faster everyday work and Haiku 5.5 for high-volume and latency-sensitive tasks. Prefer the least expensive model that meets **tested** quality, latency and reliability goals. Older models may remain useful.

**Haiku 5.5 has two pricing tiers.** Prompts of at most 100K tokens are $0.10 input / $0.50 output per million; for prompts over 100K, the whole request is billed at $0.50 / $2.50, including cached prompt tokens. Cache reads per million are Fable 5.1 $0.25, Opus 5.5 $0.20, Sonnet 5.5 $0.10 and Haiku 5.5 $0.01 (or $0.05 above 100K). Check official pricing for cache writes, batching, fast mode, geography and provider differences.

## Migration and product-surface caveats

- **Deadline:** `claude-sonnet-4-5-20250929` was deprecated September 30, 2026 and retires **November 30, 2026** on Anthropic-operated platforms. Its recommended replacement is `claude-sonnet-5-5`. Bedrock and Google Cloud set independent retirement dates. Haiku 4.5 is still listed as active.
- **Compatibility:** Opus 5.5 and Fable 5.1 do not permit disabling thinking, and forced tool selection may error. Sonnet 5.5 changes thinking and advisor-tool compatibility. Haiku 5.5 can reject earlier manual thinking budgets, non-default sampling settings, assistant prefills or legacy computer-tool types, and tokenizes some existing text differently. Read the model-specific migration guide before updating live applications; supported computer-tool versions vary by provider.
- **Claude Code:** `opus`, `sonnet`, `haiku` and `fable` are provider-dependent aliases, not frozen model IDs. Some partner providers still resolve aliases to older versions. Check `/model`, your provider deployment and CLI version. At this verification, minimum Claude Code versions for Opus/Sonnet/Haiku 5.5 are respectively 2.1.280 / 2.1.284 / 2.1.293.
- **Access and tests:** Published availability on Claude API/cloud platforms does not guarantee claude.ai, Cowork, region, plan or account access. Distinguish published specs, model availability for the account, successful requests and measured results. Query the Models API for applicable capability/limit metadata.

## Sources

- https://platform.claude.com/docs/en/models/overview
- https://platform.claude.com/docs/en/models/fable-5-1/overview
- https://platform.claude.com/docs/en/models/opus-5-5/overview
- https://platform.claude.com/docs/en/models/sonnet-5-5/overview
- https://platform.claude.com/docs/en/models/haiku-5-5/overview
- https://platform.claude.com/docs/en/about-claude/pricing
- https://platform.claude.com/docs/en/about-claude/model-deprecations
- https://platform.claude.com/docs/en/models/opus-5-5/migration-guide
- https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide
- https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide
- https://platform.claude.com/docs/en/models/fable-5-1/migration-guide
- https://code.claude.com/docs/en/model-config
- https://platform.claude.com/docs/en/release-notes/overview
