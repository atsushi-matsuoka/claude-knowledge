# Choose a workflow proportionate to the task

Last verified: 2026-09-27

## Basis

Anthropic distinguishes prescribed workflows from agents that choose their next actions dynamically, and recommends starting simple. The article is architectural guidance, not a current SDK or model catalogue.

## Decision procedure

Use a single pass when the task is small and the output is easy to check. Use sequential steps when later work depends on a verifiable intermediate artifact. Parallelize only independent tasks with clear ownership; a shared file is not two independent tasks. Add a separate reviewer when the expected value of catching an error justifies the added time and usage. Do not equate two models agreeing with correctness.

For an autonomous workflow, define the tools actually available, observable feedback, retry bound, budget if supplied, checkpoint format, and actions requiring approval. In the absence of a specified budget, propose a small first iteration; do not authorize paid calls yourself. If a dependency fails, stop that path and report rather than inventing a successful result.

## Original task-card format

Task / owner / dependencies / input versions / allowed changes / output path / acceptance test / failure behavior / completion evidence.

Example: one agent drafts a specification, a second reviews constraints read-only, and the first reconciles supported findings before implementation. Use this only when a separate review is useful; do not deploy a three-agent pipeline for a sentence edit.

## Sources

- https://www.anthropic.com/engineering/building-effective-agents
- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
