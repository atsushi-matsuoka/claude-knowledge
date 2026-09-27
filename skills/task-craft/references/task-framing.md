# Frame the task before engineering its prompt

Last verified: 2026-09-27

## Basis and local implementation

Anthropic's prompting overview places success criteria and a way to test them before prompt optimization. The procedure below is this pack's implementation for a non-engineer; it is not a transcript of an Academy lesson.

## A compact work contract

Record only what affects the result: purpose; deliverable and audience; supplied inputs; must-preserve facts; hard constraints and exclusions; available tools and permissions; acceptance checks. Distinguish **provided**, **inferred**, **unknown**, and **proposed default**.

For each gap, decide whether it blocks progress. A missing patient-data permission, irreversible action, or contradictory output requirement is a blocker. A layout preference is usually a reversible default. Inspect relevant supplied files first. Ask the smallest set of blocking questions, with an explanation of the decision each unlocks; do not repeatedly ask things already supplied.

Give the user something to react to even before every detail is known: a small prototype specification, a draft with labeled placeholders, or two concrete options with their tradeoff. Never silently choose clinical endpoints, budget, sample size, software environment or data access.

## Make completion observable

Replace “easy to use” with a proposed test: “from the start screen, add a synthetic record, find it again, edit it, and export it without using a terminal.” Label this as a proposed criterion until agreed. Replace “better research plan” with the required sections and the evidence needed for each; do not invent feasibility.

A medical writing task may permit editorial changes but not factual correction. Preserve uncertainty and numbers, and report suspected factual problems separately.

## Sources

- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview
- https://platform.claude.com/docs/en/test-and-evaluate/develop-tests
