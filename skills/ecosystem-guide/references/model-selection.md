# Claude model selection

Last verified: 2026-11-23

Models change. Verify official documentation and the actual platform, provider, plan and account before recommending or pinning a model. This November 23, 2026 snapshot does not establish personal access, applicable retention terms, or measured task quality.

## Current published Claude API lineup (November 23, 2026 JST)

| Model and release | API ID | Base USD / million input-output tokens | Thinking / default effort |
| --- | --- | --- | --- |
| Fable 5.2, Nov 9 | `claude-fable-5-2` | $8 / $40 | Adaptive always on / high |
| Opus 5.5, Sep 22 | `claude-opus-5-5` | $4 / $20 | Adaptive always on / medium |
| Sonnet 5.5, Sep 28 | `claude-sonnet-5-5` | $2 / $10 | Adaptive / high |
| Haiku 5.5, Oct 7 | `claude-haiku-5-5` | From $0.10 / $0.50 | Adaptive / medium |

All four have a documented **1M context window and 128K standard maximum output**. Anthropic suggests Opus 5.5 for most workloads; evaluate Fable 5.2 for demanding reasoning/long agent runs when Opus 5.5 at higher effort fails task-specific evals, Sonnet 5.5 for faster everyday work and Haiku 5.5 for high-volume and latency-sensitive tasks. Prefer the least expensive model that meets **tested** quality, latency and reliability goals. Older models may remain useful.

**Haiku 5.5 has two pricing tiers.** Prompts of at most 100K tokens are $0.10 input / $0.50 output per million; for prompts over 100K, the whole request is billed at $0.50 / $2.50, including cached prompt tokens. Cache reads per million are Fable 5.2 $0.20, Opus 5.5 $0.20, Sonnet 5.5 $0.10 and Haiku 5.5 $0.01 (or $0.05 above 100K). Fable 5.1 remains listed as a legacy model ($10/$50 input/output and $0.25 cache reads); it is not deleted solely due to age. Check official pricing for cache writes, batching, fast mode, geography and provider differences.

## Fable 5.2 / Mythos 5.2 rollout and migration (November 9, 2026)

- **Two distinct access routes:** Fable 5.2 (`claude-fable-5-2`) is the published general model; Mythos 5.2 (`claude-mythos-5-2`) shares its core specs and $8/$40 pricing but requires verification through an Anthropic program. Publication is not approval for a specific organization, user, region or Claude surface. Do not route ordinary users automatically to Mythos.
- **Retention is an eligibility gate:** Fable 5.2 and Mythos 5.2 require **30-day retention** and are not available under zero data retention (ZDR) unless Anthropic explicitly authorizes it. A Claude API workspace lacking the required retention returns HTTP 400. They are also not supported on Priority Tier. Never infer patient/organization-restricted data is permitted just from published model availability.
- **Thinking/prefix integrity:** Both enforce prefix binding for all accounts. Reusing later-turn thinking blocks after modifying an earlier `system` prompt, tool definition or message can return HTTP 400. They can read older models' thinking blocks on the Claude API and Google-managed Claude on Google Cloud, but other models cannot read Fable/Mythos 5.2 thinking blocks. Across accounts, those blocks can be dropped; preserve append-only histories and regression-test migrations and model fallbacks.
- **Tool compatibility:** On most platforms `computer_20251124` is rejected; use `computer_toolset_20260801` (Amazon Bedrock retains an exception). For the beta advisor tool, a Fable 5.2 or Mythos 5.2 executor accepts only one of these models as advisor. Forced tool choices remain restricted. Validate each provider's actual support before switching.
- **Safeguard behavior:** Anthropic reports that some cyber and research-biology prompts to Fable 5.2 may be handled by an older-model fallback under its safety safeguards. This does not imply an account can select Mythos, or that Fable 5.2 always executes the requested model. Inspect actual model information and evaluate task-specific behavior; do not assume a published benchmark transfers to biomedical workflows.

## Migration and product-surface caveats

- **Fast-mode deadline (November 30, 2026):** Fast mode on Claude Opus 4.8 was deprecated October 30 and is scheduled for removal November 30. Requests to `claude-opus-4-8` with `speed: "fast"` will fail after removal. Migrate fast-mode usage to a supported route such as Opus 5.5 after checking beta headers, product/provider support, premium pricing and real latency/cost; **this is a fast-mode retirement, not proof that all Opus 4.8 API access ends that day**. Test the requested model and whether `usage.speed` actually shows fast execution.

- **Deadline:** `claude-sonnet-4-5-20250929` was deprecated September 30, 2026 and retires **November 30, 2026** on Anthropic-operated platforms. Its recommended replacement is `claude-sonnet-5-5`. Bedrock and Google Cloud set independent retirement dates. Haiku 4.5 is still listed as active.
- **Compatibility:** Opus 5.5 and Fable 5.1 do not permit disabling thinking, and forced tool selection may error. Sonnet 5.5 changes thinking and advisor-tool compatibility. Haiku 5.5 can reject earlier manual thinking budgets, non-default sampling settings, assistant prefills or legacy computer-tool types, and tokenizes some existing text differently. Read the model-specific migration guide before updating live applications; supported computer-tool versions vary by provider.
- **Claude Code:** `opus`, `sonnet`, `haiku` and `fable` are provider-dependent aliases, not frozen model IDs. Some partner providers still resolve aliases to older versions. Check `/model`, your provider deployment and CLI version. At this verification, minimum Claude Code versions for Opus/Sonnet/Haiku 5.5 are respectively 2.1.280 / 2.1.284 / 2.1.293.
- **Access and tests:** Published availability on Claude API/cloud platforms does not guarantee claude.ai, Cowork, region, plan or account access. Distinguish published specs, model availability for the account, successful requests and measured results. Query the Models API for applicable capability/limit metadata.
- **Google Cloud route added October 22, 2026:** Anthropic-managed Claude Models on Google Cloud is separate from Google-managed Claude on Google Cloud. Its Anthropic-operated API uses Google Cloud IAM, Google Cloud Marketplace billing and the `AnthropicGoogleCloud` client, not the Google-managed Vertex client. Model IDs may match, but the authentication, capabilities, quotas and rollout must be checked for the specific route. This does **not** establish access for any Google project or Claude account.

## Sources

- https://platform.claude.com/docs/en/models/overview
- https://platform.claude.com/docs/en/models/fable-5-2/overview
- https://platform.claude.com/docs/en/models/mythos-5-2/overview
- https://platform.claude.com/docs/en/models/fable-5-2/migration-guide
- https://www.anthropic.com/claude-fable-and-mythos-5-2
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
- https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed
- https://platform.claude.com/docs/en/build-with-claude/fast-mode
