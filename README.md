# Claude Knowledge Pack

A version-controlled knowledge and workflow pack for Claude-related work across Claude Code, Codex, and Gemini CLI.

## Design

- **GitHub is the source of truth.** Keep reviewed knowledge, workflows, evals, and automation here.
- **Google Drive is the learning inbox.** Put Academy notes, PDFs, screenshots, and rough learning material there; summarize and verify before promoting content into this repository.
- **Official documentation wins.** Academy provides the curriculum; current Anthropic documentation provides volatile product facts.
- **Progressive disclosure.** The always-visible skill metadata stays small; detailed knowledge lives in `references/` and is read only when needed.
- **Safe freshness.** Local installs can fast-forward automatically. GitHub Actions detects source changes monthly. Knowledge prose is updated through review rather than silently rewritten.

## What this pack is for

Use the `sonnet-stack` skill for tasks involving Anthropic Claude, Claude Code, claude.ai, Claude API, Agent Skills, MCP with Claude, model selection, prompting practices, or cross-agent workflows where Claude is one of the participants.

The pack does **not** try to replace Anthropic's official `claude-api` skill. Claude Code already bundles that skill for API/SDK details. This pack focuses on product-surface distinctions, Academy-derived knowledge, workflow design, cross-agent coordination, and freshness policy.

## Repository layout

```text
claude-knowledge/
├── AGENTS.md
├── CLAUDE.md
├── GEMINI.md
├── curriculum/
├── academy-notes/
├── skills/sonnet-stack/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/
│   ├── workflows/
│   └── scripts/
├── sources/
├── evals/
├── scripts/
└── .github/workflows/
```

## Install locally

After this repository has a GitHub URL:

```bash
python scripts/bootstrap.py --repo-url https://github.com/atsushi-matsuoka/claude-knowledge.git
```

The bootstrapper clones or fast-forwards the repository and installs symlinks (copy fallback on platforms where symlinks are unavailable) into:

- Claude Code: `~/.claude/skills/sonnet-stack`
- Codex: `~/.agents/skills/sonnet-stack`
- Gemini CLI: the same `~/.agents/skills/sonnet-stack` path, which Gemini CLI supports as an interoperable alias

Re-run the command at any time to refresh. The skill itself also has a lightweight `ensure_fresh.py` helper that local agents may run when the local checkout is stale.

## Updating knowledge

1. Put Academy learning notes in Google Drive or `academy-notes/inbox/`.
2. Convert them into concise claims or workflows; do not copy course material wholesale.
3. Verify changing facts against official Anthropic sources in `sources/manifest.json`.
4. Update the relevant `references/*.md` file.
5. Update `last_verified` metadata and `CHANGELOG.md`.
6. Run:

```bash
python scripts/validate_repository.py
python scripts/check_sources.py --no-network
```

7. Review the diff before merge.

## Automation

- `validate.yml`: validates skill structure and repository invariants on pushes and PRs.
- `source-watch.yml`: runs monthly and on demand, checks official source URLs, records fingerprints/status, and opens or updates a GitHub issue when source content appears to have changed.

The watcher deliberately does **not** rewrite knowledge prose automatically. That protects the pack from site chrome changes, ambiguous release notes, and accidental regressions. Agents using the skill are instructed to verify volatile facts live when network access is available.

## Privacy

Do not put patient-identifiable information, clinical records, credentials, API keys, or organization-restricted material into this repository or the Drive learning inbox unless your organization's policy and service agreements explicitly allow it.
