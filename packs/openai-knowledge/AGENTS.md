# OpenAI knowledge and performance pack

This directory is an independent pack, not a change to the parent Claude plugin.
The goal is better completed work, not maximum tokens or an unconditional model upgrade.

- Product/model facts: `skills/openai-guide/`. Applied work: `skills/gpt-workbench/`.
- Read only the relevant reference. Keep both SKILL.md files short; dates and sources belong in references.
- Official publication, account availability, successful invocation, and measured suitability are separate claims. Never infer one from another.
- Use OpenAI first-party sources for changing facts. Record retrieval limitations and contradictory pages. Do not mark Academy courses complete from outlines.
- Safe local tests use disposable fixtures and no credentials. Run affected tests, fix failures introduced by the change, then run one full pack validation before a PR.
- Run `python scripts/validate.py` and `python -m unittest discover -s tests -v` from this directory. Tests do not invoke models.
- Keep evaluation inputs out of prompt optimization. Never invent runs, costs, scores or model switches. No paid model calls without an explicit authorization/budget.
- Keep changes inside this pack and its two named OpenAI workflows. Do not edit parent skills, historical handoffs, existing personal skills, account settings or production systems.
- Version this pack with VERSION, pack.json, both SKILL metadata.version fields and CHANGELOG. No automatic merge.
- Never store patient-identifiable information, credentials, internal clinical records or organization-restricted data. Use synthetic examples.

- Academy coverage is tracked in curriculum/academy-inventory.json. Update its generated map with scripts/audit_curriculum.py --render. Reading, operationalization, original local checks, Academy exercises and real-model effects are distinct; no completeness claim from public discovery alone.
