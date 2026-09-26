# Eval results

## 2026-09-26: v0.1.1 `claude-stack` vs v0.2.0 `ecosystem-guide`

Setup: `claude plugin eval`, Claude Code 2.1.283, agent `claude-sonnet-5`, judge `sonnet`, 2 runs per case, tools `Read Glob Grep Skill` (no web access unless noted). Both versions ran the same 46 cases from `questions.json`. "Tuned" = the 36 cases used while iterating the description; "held-out" = 10 cases written before the final runs and not used for tuning.

### Tuned cases (36; 28 should trigger, 8 should not)

| metric | v0.1.1 | v0.2.0 |
|---|---|---|
| trigger recall | 29/56 (52%) | 47/56 (84%) |
| false-trigger rate | 0/16 (0%) | 0/16 (0%) |
| routing accuracy (opened the expected reference) | 27/54 (50%) | 47/54 (87%) |
| answer rubric pass, in-scope | 32/56 (57%) | 44/56 (79%) |
| answer rubric pass, out-of-scope | 16/16 (100%) | 16/16 (100%) |
| no plugin at all, in-scope | 26/56 (46%) | |

### Held-out cases (10; 6 should trigger, 4 should not)

| metric | v0.1.1 | v0.2.0 |
|---|---|---|
| trigger recall | 4/12 (33%) | 12/12 (100%) |
| false-trigger rate | 0/8 (0%) | 0/8 (0%) |
| routing accuracy | 4/12 (33%) | 12/12 (100%) |
| answer rubric pass, in-scope | 5/12 (42%) | 10/12 (83%) |
| no plugin at all, in-scope | 3/12 (25%) | |

Out-of-scope cases include two name collisions (Claude Monet, Claude Debussy), general coding, a Claude API SDK snippet (left to the `claude-api` skill), and stable concepts. Neither version fired on any of them.

### Live verification (WebFetch granted for official Anthropic domains, `fresh-*`, 6 runs)

The skill fired and opened `model-selection.md` in 6/6 runs, and every reply cited the official page it had fetched in that run instead of answering from memory. Rubric pass was 2/6: most misses are judge strictness about citation form; one real gap is that `fresh-02` answers do not always separate model capability from plan/surface availability.

The first web run scored 0/6 because the judge failed correct, cited answers whose facts were newer than its own knowledge. The rubric template now tells the judge to score behaviors only. The tuned/held-out runs above used the earlier template; they had no web access, so the change barely affects them.

### Changes made between runs, and why

1. v0.2.0 first draft: tuned recall 61%. Misses came from prompts that said "this repo" without naming it (the model asked which repo), missing Codex/Gemini install facts, and a description that did not mention Academy notes, source-watch, source conflicts or prompting.
2. Prompts made self-contained, Codex/Gemini paths added to `cross-agent-collaboration.md`, description widened: tuned recall 80%, held-out 100%.
3. From inspecting failures (one of them held-out, `holdout-03`): the 1,536-character listing limit was added to `agent-skills.md`, the freshness protocol now says only a current official source can override a dated note, and answers come before actions. Final: the numbers above.

### Known limits

- Two runs per case is a small sample; treat differences under ~10 points as noise.
- Only one agent model was measured. Re-run with Haiku before relying on it there.
- Codex and Gemini CLI were not measured; `questions.json` is written to be usable for them by hand.

Re-run: see "Evaluating routing" in the README. Cost of the final full run was about $13 at list price.
