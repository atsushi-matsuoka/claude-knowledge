# Performance evaluation protocol

## Initial state

All initial cases are development/smoke material visible to the author. There is no independent holdout claim. All expected outputs are synthetic. No real-model comparison has been run.

## Experiments

A. Routing: present cases.json prompts in fresh sessions with the pack available; record actual Skill activation, references opened, model recommendation and unauthorized-action attempts. Check negative cases as well. A script selecting a tier does not measure LLM activation.

B. Skill ablation: same task, designer model/settings, tools and budget in fresh sessions, without/with gpt-workbench. Blindly grade produced specs/prompts with fixed criteria: preserved constraints (mandatory), correctness/evidence, usability and unnecessary overhead. Keep task-craft or other overlapping Skills out of both arms, or explicitly label a different comparison.

C. Downstream: give both designers only the brief in outcomes.json, never its cases/answers. Freeze prompts. Execute each on independently prepared inputs with the same executor/settings and neither Skill in the executor. Record both arms for every case/trial, output or nonblank error, model/settings, timestamp, prompt version, trace reference and observed cost/time. Do not choose only the best run. The bundled fixtures are smoke tests, not an uncontaminated final test.

D. Model selection: deliberately vary candidate models under an equivalent task/tool budget. It is not a same-model Skill ablation. Report quality first, then observed whole-job latency/cost and retry burden. Do not extrapolate API token prices to subscription usage quotas. Start with an authorized small budget; no automatic paid runs.

## Offline scoring

Run `python scripts/score_outputs.py records.json`. Required fields:
- evidence_kind: synthetic or reported-model-run
- metadata: designer_models (baseline/candidate), executor_model, executor_settings, surface, timestamp, trace_reference
- prompts: baseline/candidate actual designed prompt
- trials: positive integer
- runs: case_id, arm (baseline/candidate), trial, and output or nonblank error

Missing rows or absent output/error payloads make the comparison incomplete and suppress the delta. Invalid recorded outputs and explicit errors count as observed failures. A scorer cannot authenticate traces: it always reports provenance_verified=false and general_capability_gain_proven=false. Self-labeling data as model output is not verification.

## Acceptance before tuning

Reject privacy violations, lost hard constraints and unauthorized actions regardless of average scores. Set task-specific quality/latency targets before running; retain unchanged baseline artifacts. Independently authored final cases should include vague specs, precise edits, code reviews, blocked tools and source contradictions, not only extraction. Report per-task counts, uncertainty and missing runs; stop at the budget/iteration boundary. Do not call a wider prompt or more elaborate process an improvement without outcomes.

## Academy-derived practice probes

The learn-* cases are development contracts authored while implementing the procedures. They are not independent holdouts or executions of the Academy's exercises. For real-model testing, independently prepare new tasks for requirement preservation, approval/stop behavior, research grounding, data/period reconciliation, and coding save/reopen regression. Use the same model/settings for Skill ablation; evaluate changed models/effort separately.

For open-ended artifacts grade requirement preservation, usability, evidence and critical boundaries separately. A single critical authorization breach blocks promotion regardless of the mean score. Measure completed usable work, observed full cost and total latency; first-token delay is a separate value. Curriculum validators only verify record consistency, not truth of reading or real task quality.
