# Prompting Claude

Last verified: 2026-09-23

Do not freeze model-specific prompting folklore into permanent rules. Newer models may need less scaffolding than older ones.

Prefer:

- Clear goal and success criteria.
- Relevant context, constraints, and examples only when they materially help.
- Explicit output requirements when format matters.
- Separation of facts, assumptions, and open questions.
- Iteration through concrete artifacts (spec, diff, test result) rather than ever-longer meta-prompts.

For large implementation tasks, create a durable specification with acceptance criteria and let the execution agent work from that artifact. This is usually more portable across Claude, Codex, and Gemini than generating a vendor-specific mega-prompt.

When a prompt technique depends on a model generation, verify current Anthropic prompting guidance before treating it as best practice.
