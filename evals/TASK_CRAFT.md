# Task-craft evaluation protocol

## Status

No model effectiveness measurement has been run for task-craft in this change. Unit tests and generated eval files are implementation checks only. Do not copy ecosystem-guide's v0.2.0 scores as task-craft scores.

## Layer 1 and 2: activation, routing and artifact quality

The canonical cases are in `evals/questions.json`, schema v2. Optional `skill` identifies the skill being graded; absence means `ecosystem-guide` for backward compatibility. New cases carry `task-craft` tags. `should_trigger` applies to that skill, not to every skill in the plugin. Old cases and held-out prompts must remain unchanged.

Generate with `python scripts/build_evals.py`; do not hand-edit `evals/claude-code/`. Use the existing manual `eval` workflow or the locally installed Claude Code evaluator described in README, after checking its current help. Do not automatically start paid calls. With results:

```
python scripts/summarize_evals.py results.json --tag task-craft --per-case
python scripts/summarize_evals.py results.json --exclude-tag task-craft --per-case
python scripts/summarize_evals.py results.json --tag holdout --per-case
```

Report per-skill denominators, false triggers and requirement preservation; do not mix the two skills into a claim about prompting improvement. New task-craft holdouts were written after the initial description was fixed and have not been used to tune it. The author also wrote those cases, so this is not independent test-set construction. If future tuning uses them, retire that holdout claim.

## Layer 3: actually use the designed prompts

`task-craft-outcomes.json` contains three task briefs and nine synthetic downstream inputs. Keep the inputs and answer keys away from the prompt designer. In separate fresh sessions give the same brief to a baseline designer without the plugin and a candidate designer with the plugin. Keep model, settings, context and resource limits equal; record which skills actually activated. Save the two resulting prompts unchanged.

Next, use each saved prompt in a fresh executor session on each test input, with no plugin in either executor. This isolates the effect of the prompt design, rather than giving only the candidate extra execution help. Record all attempts, errors and available cost/time data. Additional Claude/Codex/Gemini combinations are separate experiments, not pooled results. These fixtures test narrow preservation/extraction behavior, not overall research or coding ability.

Use `scripts/score_task_craft_outcomes.py records.json --output report.json` to score results. It makes no API calls. Records format:

```json
{
  "metadata": {"model":"actual executor model", "surface":"actual surface", "settings":{}, "skill_version":"0.3.0", "evidence_kind":"model-run"},
  "trials": 1,
  "prompts": {"schedule":{"baseline":"actual prompt", "candidate":"actual prompt"}, "evidence":{"baseline":"actual prompt", "candidate":"actual prompt"}, "source-choice":{"baseline":"actual prompt", "candidate":"actual prompt"}},
  "runs": [{"case_id":"out-s1", "arm":"baseline", "trial":1, "output":{"owner":"担当A","due":"4/12","status":"confirmed"}}]
}
```

The example is incomplete and is not a measured result. Supply both arms for every case/trial; missing attempts fail and make the comparison incomplete. Duplicate/unknown attempts are rejected. Outputs must parse as exactly the required JSON structure, types and values. Add designer model/settings, trace locations, actual activation and execution environment to the metadata when recording a real experiment.

## Decision rule

Agree on desired improvement and regression tolerance before running the experiment. Reject any change that loses a hard requirement or violates privacy even if mean score rises. Report raw counts and uncertainty; a small synthetic set cannot establish broad capability gains. For vague specifications and agent plans, supplement these fixtures with blinded rubric review and actual task completion evidence. Stop at the agreed trial/budget limit.
