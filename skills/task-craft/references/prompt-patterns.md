# Diagnose, then choose the prompt technique

Last verified: 2026-09-27

## Basis

Anthropic's official Real world prompting lesson 3 teaches a draft/test/diagnose/change/retest cycle rather than applying every trick at once. Its educational model examples are not current model-selection advice. The following failure-to-action table is an original operational adaptation.

| Observed failure | First repair | Test |
|---|---|---|
| Wrong task or audience | State the deliverable and what it will be used for | Same input, correct scope |
| Missing facts are invented | Supply evidence boundaries and an explicit missing-value rule | Incomplete input stays incomplete |
| Counts, exclusions or uncertainty change | Add a short must-preserve checklist | Negated, bounded and uncertain examples |
| Output cannot be parsed | Specify keys/types and invalid-input behavior; use host-native schema only if available | Parse output and reject extra/missing fields |
| Examples are copied too literally | Vary examples and include a boundary case | Novel entities, order and phrasing |
| Context is ignored | Remove irrelevant text; label evidence and source locations | Conflicting and distractor passages |
| A multi-step result drifts | Add one intermediate artifact and check | Stop if the intermediate artifact fails |
| Tool use fails | Inspect permissions, input schema and actual tool errors | Do not treat a prompt rewrite as an access fix |

## Draft structure, not a mandatory template

Include purpose, relevant input, instructions, constraints, output contract and acceptance checks only as needed. Separate instruction from source data with clear headings or delimiters. Add representative examples when they resolve ambiguity, not as decoration. Use a role only when it changes perspective or tone usefully. Do not demand disclosure of private chain-of-thought; ask for an answer, concise rationale and verifiable evidence.

For revisions, show the repaired prompt first, then a short mapping from observed failures to the changed clauses. When no failing outputs were supplied, call the diagnosis provisional and propose tests; do not report an improvement measurement.

## Sources

- https://github.com/anthropics/courses/blob/master/real_world_prompting/03_prompt_engineering.ipynb
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
