# Claude Knowledge Pack

A reviewed, version-controlled knowledge and practice pack about the Claude ecosystem, shared by Claude (chat, Cowork, Claude Code), Codex and Gemini CLI. GitHub is the source of truth.

## Design

- **Two focused portable skills.** `ecosystem-guide` handles changing Claude product knowledge; `task-craft` applies prompting, specification and evaluation methods. Each uses portable frontmatter and can be distributed in this plugin or installed separately.
- **Small always-on footprint.** Hosts see concise descriptions; each skill body and its matching references load only when needed. Do not load both entire folders for every request.
- **Different triggers.** Product/surface questions use ecosystem-guide. Prompt design, substantial idea-to-spec work and AI workflow improvement use task-craft. Simple direct execution and stable conceptual explanations need neither practice procedure nor extra retrieval.
- **Official docs win.** Volatile facts live in references with `Last verified` dates and `## Sources`. The skill verifies live when it can, and says when it cannot.
- **Measured, not assumed.** Historical ecosystem-guide results remain in evals/RESULTS.md. task-craft has test infrastructure but its model effectiveness is unmeasured; activation, artifact quality and downstream outcomes are separate.
- **Reviewed updates only.** The monthly source watcher opens an issue naming which references cite each changed page; it never rewrites knowledge itself.

## Install

### Claude: chat, Cowork and Claude Code (recommended)

The repository root is a plugin and a one-plugin marketplace.

- **claude.ai / Cowork**: Customize > Plugins > add marketplace `atsushi-matsuoka/claude-knowledge`, then install `claude-knowledge`. Account installs also reach Claude Code sessions signed in with the same account.
- **Claude Code only**:

  ```bash
  claude plugin marketplace add atsushi-matsuoka/claude-knowledge
  claude plugin install claude-knowledge@matsuoka-knowledge
  ```

  Update later with `claude plugin marketplace update matsuoka-knowledge`. The skill appears as `claude-knowledge:ecosystem-guide`.

Plugin UI labels and sync behavior change; check https://claude.com/docs/plugins/overview if a step differs. A private repository needs GitHub access granted on each surface.

### Codex and Gemini CLI

```bash
python scripts/bootstrap.py --repo-url https://github.com/atsushi-matsuoka/claude-knowledge.git
```

Clones (or fast-forwards a clean checkout) to `~/.local/share/claude-knowledge` and links both `~/.agents/skills/ecosystem-guide` and `~/.agents/skills/task-craft`. Add `--claude-code` to also link `~/.claude/skills/ecosystem-guide` if you prefer a live checkout over the plugin in Claude Code; do not use both, or the skill is listed twice. `skills/ecosystem-guide/scripts/ensure_fresh.py` fast-forwards a linked checkout at most once a day.

ChatGPT Projects and Gemini apps without skill support can use the routing text in `adapters/`.

### Migration from `claude-stack` / `sonnet-stack`

Version 0.2.0 renamed the skill. Re-running `bootstrap.py` removes old `claude-stack` and `sonnet-stack` symlinks that point into this checkout; it never deletes ordinary directories. Install the plugin for Claude afterwards.

## Layout

```text
.claude-plugin/        plugin.json + marketplace.json (repo root = plugin)
skills/ecosystem-guide/
  SKILL.md             trigger, routing table, freshness protocol
  references/          dated, source-linked notes (loaded on demand)
  workflows/           update-knowledge-pack.md
  agents/openai.yaml   Codex display metadata
skills/task-craft/
  SKILL.md             task-design trigger and work contract
  references/          original method notes and worked examples
  workflows/           prompt repair, idea-to-spec, agent planning, iteration
evals/questions.json   agent-neutral cases (should_trigger, reads, expect)
evals/claude-code/     generated claude plugin eval suite
sources/               official pages watched for changes
scripts/               validate, build/summarize evals, source watch, bootstrap
tests/                 unit tests for the scripts
AGENTS.md              shared repo instructions (CLAUDE.md and GEMINI.md import it)
```

## Practice layer: use task-craft for the work itself

For example: 「この曖昧なアイデアを、試せる最小仕様にして」, 「このプロンプトが不確実性を消してしまうので直して」, or 「このAI作業を公平に比較する評価を設計して」. The skill should return a usable artifact, not merely describe Claude features. When a task also depends on current Claude product facts, consult ecosystem-guide only for that subtask.

This first practice layer uses reviewed public Anthropic educational text and official documentation. It does **not** mean the full Academy was learned. Academy pages/lesson bodies not obtained remain incomplete; no exercises or real-model effectiveness tests were executed here. See `academy-notes/2026-09-27-practice-intake.md`, `skills/task-craft/references/learning-provenance.md` and `evals/TASK_CRAFT.md`.

The plugin package now contains both skills. An unmerged PR is not a deployed update: update the installed package only after review and merge. The routing text in `adapters/` is a template, not a claim that account-level instructions were changed.

## Updating knowledge

Follow `skills/ecosystem-guide/workflows/update-knowledge-pack.md`. In short: verify against the first-party page, edit the smallest reference, update its date, add an eval case if behavior can regress, then:

```bash
python scripts/build_evals.py            # after editing evals/questions.json
python scripts/validate_repository.py
python -m unittest discover -s tests
python scripts/check_sources.py --no-network
```

Academy notes go to Google Drive or `academy-notes/` first (see `docs/google-drive.md`) and are summarized, never copied.

## Evaluating routing

Cases retain schema v2; optional `skill` chooses the graded target, with ecosystem-guide as the backward-compatible default. All new cases carry a task-craft tag. Use `scripts/summarize_evals.py ... --tag task-craft` for that skill and `--exclude-tag task-craft` for the original skill. Do not pool their scores as evidence of improved prompt design. See `evals/TASK_CRAFT.md` for a separate downstream-output comparison.

Requires Claude Code and uses real model calls (counted against your plan or API bill).

```bash
# cheap smoke run: 1 run per case, with-plugin only
claude plugin eval . --trust-plugin --no-publish --runs 1 --ablation none --json /tmp/smoke.json

# full comparison against the no-plugin baseline
claude plugin eval . --trust-plugin --no-publish --runs 2 -j 6 \
  --model claude-sonnet-5 --judge-model sonnet --json /tmp/full.json

python scripts/summarize_evals.py /tmp/full.json --per-case
```

Add `--allow-tools WebFetch` to test live verification. The latest measured results are in `evals/RESULTS.md`.

## Privacy

Do not put patient-identifiable information, clinical records, credentials, API keys, or organization-restricted material into this repository or the Drive inbox unless your organization's policy and agreements explicitly allow it. The validator scans for common key formats but cannot detect clinical data.
