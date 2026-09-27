# Evaluate the outcome, not the appearance of the prompt

Last verified: 2026-09-27

## Basis

Anthropic's evaluation guidance calls for explicit success criteria and task-representative tests. Its agent-evaluation guidance distinguishes an agent's trace from the actual outcome. The thresholds and test fixtures in this repository are local engineering choices, not claimed Anthropic benchmarks.

## Three separate questions

1. **Selection:** did the intended skill activate, and did unrelated skills stay out of the way?
2. **Artifact:** did the produced prompt/specification preserve the user's requirements, resolve relevant ambiguities and provide executable checks?
3. **Downstream outcome:** when the produced prompt is actually used on fresh inputs, is the resulting work more correct, complete or useful?

A pass at the first two levels does not prove the third. For structured tasks, check parsed outputs, omissions, extra fields, types and unsupported claims with code. For open-ended plans, use a prewritten rubric and human review where substantive judgment matters. Assess correctness separately from polish and verbosity.

## Controlled comparison

Freeze the task, model identifier, surface, settings, inputs, allowed tools and scoring rule. Record baseline and with-skill attempts in fresh sessions, with the same information and resource limits. Change only skill availability in the comparison. Keep the original user request as a baseline; do not deliberately degrade it. Do not show the test answers to the prompt designer. Record failures and all attempts, not only the best output.

Use development examples for refinement. Keep held-out cases out of tuning; once used to choose a change, retire them from the untouched holdout claim and prepare new cases. Repeat when affordable and authorized. Report denominators and small-sample limitations, including time and tokens when observed. No paid evaluation without authorization.

## Stop and report

Retain a change only when it improves the predefined target without critical regression on preserved requirements. Otherwise report mixed results, no demonstrated benefit or unmeasured effect. Unit-test success is not an LLM effectiveness result.

## Sources

- https://platform.claude.com/docs/en/test-and-evaluate/develop-tests
- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- https://github.com/anthropics/courses/blob/master/real_world_prompting/03_prompt_engineering.ipynb
