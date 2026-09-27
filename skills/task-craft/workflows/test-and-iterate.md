# Workflow: test and iterate

1. Before revising the prompt, record success conditions and failure cost. Separate skill selection, prompt/spec quality and downstream task outcomes.
2. Keep a baseline and prepare representative inputs, including missing data, conflicting/negated claims, edge cases and irrelevant requests. Write expected outcomes independently of the model response.
3. Freeze model/surface/settings/tool access and budgets for comparable runs. Do not give test answers to the prompt designer. Do not tune on held-out cases.
4. If the authorized runtime exists, run and retain all attempts, including errors. Otherwise label the experiment unexecuted. Never make up model outputs, usage or scores.
5. For deterministic tasks use a strict parser and exact expected structure/types. For open-ended tasks use a fixed rubric and independent review. Count unreadable or incomplete outputs as failures, not omitted data.
6. Change the smallest cause of an observed failure, rerun the same development cases and inspect regressions. Use fresh held-out cases for the final comparison.
7. Report sample sizes, raw pass counts, cost/time if observed and limitations. Stop when mandatory acceptance criteria are met or the agreed iteration limit is reached. Do not label activation or unit-test gains as downstream effectiveness.
