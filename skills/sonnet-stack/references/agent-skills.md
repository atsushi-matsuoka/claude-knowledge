# Agent Skills

Last verified: 2026-09-23

Agent Skills are directories centered on `SKILL.md`, with optional scripts, references, and assets. Their main advantage is progressive disclosure: metadata can be available for routing while detailed instructions/resources load only when relevant.

## Cross-agent design rule

Write the core skill against the open Agent Skills format. Keep vendor-specific adapters thin.

## Naming

For maximum portability, use conservative lowercase-hyphen names and avoid vendor-reserved words in the `name` field. Put vendor/product trigger words in the description instead.

## Description quality

The description is a routing surface. State both what the skill does and when it should trigger. Include important product keywords early, but keep the description concise enough to survive truncation in hosts with many installed skills.

## Resource strategy

- `SKILL.md`: decision rules and workflow skeleton.
- `references/`: detailed knowledge read only when needed.
- `scripts/`: deterministic tasks such as validation or source checking.
- `assets/`: templates or output resources, not general documentation.
