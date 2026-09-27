# Workflow: plan bounded agent work

1. Define the final deliverable, evidence required and authorization boundary. Check which tools and accounts are actually accessible.
2. Start with a single worker. Split only when dependencies, independent review or context limits justify it. Never claim another model was invoked unless a tool result confirms it.
3. For each task record owner, input version, dependencies, allowed paths/actions, output artifact and acceptance check. Use branches or distinct files for independent workers; keep review read-only unless editing is explicitly assigned.
4. Set a small first iteration, stopping conditions and escalation rules. Do not invent permission for spending, credential changes, publication or deployment.
5. Give the worker a concise handoff, not the full chat. Test intermediate artifacts before dependent work proceeds. Record actual failures and unresolved assumptions.
6. Have the integration owner reconcile review findings against source evidence and tests. Fix valid findings only; do not blindly apply every reviewer suggestion.
7. Finish with results, evidence, tests and unresolved items. Stop at the authorized boundary.
