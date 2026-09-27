# Workflow: rough idea to testable specification

1. Identify the practical problem and the decision/output the user needs. Inspect supplied notes. Separate a request for a specification from permission to implement or deploy.
2. Draft a minimal work contract: goal, user, inputs, must-have behavior, exclusions, constraints and proposed observable checks. Use plain language, not a list of frameworks.
3. Distinguish blocking unknowns from reversible defaults. Ask only for blockers; show a useful draft with labeled assumptions meanwhile. Do not invent resources, data availability, budget or medical facts.
4. Show one small first version and what it deliberately excludes. Where a decision has a real tradeoff, give concise alternatives rather than quietly committing the user.
5. Produce a specification another worker can act on: outputs, input/output examples, error/missing-data behavior, permissions, acceptance checks and unresolved questions. Match detail to task size.
6. Verify the specification against the original request, especially negation and scope. When authorized to implement, proceed from the specification; otherwise stop at the requested artifact.

Return the specification first, then unresolved blockers and checks. Creating the specification does not mean the project has been implemented.
