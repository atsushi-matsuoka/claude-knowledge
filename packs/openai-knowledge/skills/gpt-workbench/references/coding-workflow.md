# Context and feedback for coding work

Last verified: 2026-09-28

For substantial coding changes, inspect repository instructions, current revision and the affected files. State the observable behavior, evidence/reproduction, preserved interfaces and acceptance check. Give a usable first proposal when nonblocking details are missing; do not ask a non-engineer to choose a stack unnecessarily.

Reproduce the failure or record why reproduction is unavailable. Make the smallest warranted change, run the affected regression, then the appropriate broader checks. Distinguish an environment failure from a failed application test. A command's success is not enough if the saved artifact or visible behavior is wrong.

Keep a short entry map to versioned context; load details only when needed. For long tasks retain input versions, progress and verified results. Use separate workspaces/branches for writers and read-only independent review by default; reconcile supported findings before integration. Do not mandate long plans, multiple agents or maximum effort for every change.

Dated Academy command examples are not the installation specification. Check current official surface-specific docs rather than reverting working config from an old slide. No account or model switch is executed by this reference.

## Original probe

A settings change displays Saved but is lost on reopening. Acceptance requires save, reopen and compare, while preserving the public API. Report the actual failing-before/passing-after evidence, or explicitly label the test unexecuted. A later resumed run rechecks the current revision before modifying it.

## Sources

- https://academy.openai.com/public/clubs/builders-etkn1/resources/codex-101-introduction-and-onboarding-2026-03-18
- https://academy.openai.com/public/clubs/builders-etkn1/resources/codex-102-practical-workflows-2026-03-18
- https://academy.openai.com/public/clubs/builders-etkn1/resources/codex-103-advanced-workflows-and-automation-2026-03-18
- https://learn.chatgpt.com/docs/prompting
- https://openai.com/index/harness-engineering/
- https://learn.chatgpt.com/docs/build-skills
