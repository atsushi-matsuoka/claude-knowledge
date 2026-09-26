# Claude Knowledge Pack

A reviewed, version-controlled knowledge pack about the Claude ecosystem, shared by Claude (chat, Cowork, Claude Code), Codex and Gemini CLI. GitHub is the source of truth.

## Design

- **One portable skill, `ecosystem-guide`.** Written to the open Agent Skills spec (portable frontmatter only, no reserved words in the name), so the same folder works as a Claude plugin skill, a claude.ai upload, and a Codex/Gemini skill.
- **Small always-on footprint.** Hosts see only the ~700-character description. The ~60-line `SKILL.md` loads when relevant; each reference loads only when its row in the routing table applies.
- **Trigger narrowly.** The description targets questions whose answer changes over time or differs by surface, and names what it is *not* for (general coding, stable concepts, other vendors alone, API code that the `claude-api` skill covers).
- **Official docs win.** Volatile facts live in references with `Last verified` dates and `## Sources`. The skill verifies live when it can, and says when it cannot.
- **Measured, not assumed.** `evals/questions.json` is the agent-neutral case set; a generated `claude plugin eval` suite measures trigger recall, false triggers, routing and answer quality against a no-plugin baseline.
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

Clones (or fast-forwards a clean checkout) to `~/.local/share/claude-knowledge` and links `~/.agents/skills/ecosystem-guide`. Add `--claude-code` to also link `~/.claude/skills/ecosystem-guide` if you prefer a live checkout over the plugin in Claude Code; do not use both, or the skill is listed twice. `skills/ecosystem-guide/scripts/ensure_fresh.py` fast-forwards a linked checkout at most once a day.

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
evals/questions.json   agent-neutral cases (should_trigger, reads, expect)
evals/claude-code/     generated claude plugin eval suite
sources/               official pages watched for changes
scripts/               validate, build/summarize evals, source watch, bootstrap
tests/                 unit tests for the scripts
AGENTS.md              shared repo instructions (CLAUDE.md and GEMINI.md import it)
```

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
