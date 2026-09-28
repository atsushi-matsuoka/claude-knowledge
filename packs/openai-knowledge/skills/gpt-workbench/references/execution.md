# Bounded execution and review

Last verified: 2026-09-28

A workable delegation card states the goal, input artifact/version, owner, allowed writes, deliverable, observable tests and stopping conditions. Use a single worker unless tasks are independent or a separate reviewer has concrete value. Parallel workers should not concurrently edit the same file; use isolated branches or distinct outputs. Agreement between models is not proof.

For an unfamiliar application, propose a small vertical slice that can be checked by the user: synthetic input, a visible result, save/reopen/export where relevant, and explicit error behavior. Do not ask a non-engineer to choose a database before the requirement is known. Inspection of a finished visual artifact and targeted tests may matter more than a large implementation plan.

Where the requested scope authorizes local disposable tests, execute them, inspect failures and correct the change without repeated permission questions. Stop at publication, deployment, new paid usage or sensitive-data access unless authorized. Preserve an existing workflow rather than replacing it just to introduce an agent framework.

A reviewer should return location, impact, evidence and uncertainty. The implementation owner checks findings and integrates only supported changes. A missing runtime yields a ready-to-execute artifact and clearly proposed tests, not invented execution.

## Sources

- https://academy.openai.com/public/clubs/work-users-ynjqu/resources/get-started-with-chatgpt-work-webinar-resource-guide-2026-08-03
- https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra
