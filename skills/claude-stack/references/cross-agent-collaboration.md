# Claude ↔ Codex ↔ Gemini collaboration

Last verified: 2026-09-23

## Default pattern

Use a shared artifact as the handoff boundary:

1. Discovery / requirement shaping.
2. `SPEC.md` with goal, scope, constraints, non-goals, acceptance criteria, and tests.
3. Implementation by the execution agent.
4. Independent review by a different model when failure cost justifies it.
5. The implementation agent verifies review findings and fixes only valid issues.

Avoid asking one model to generate a huge "perfect prompt" for another when a stable specification would work better.

## Suggested roles for a non-engineer

- Conversational model: clarify the rough idea and expose decisions.
- Codex / coding agent: implement, run tests, inspect failures, and produce a concrete result.
- Claude or another independent model: review design, UX, edge cases, or code when independent critique is valuable.

The roles are not fixed by brand. Re-evaluate them on real tasks and eval results.

## Shared knowledge

Use GitHub as the reviewed source of truth. Local agent skill installations should point to or sync from that repository. Use Google Drive as a learning inbox and human-readable archive, not a competing canonical copy.
