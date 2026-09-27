# Maintenance contract

1. Read AGENTS.md, this file, and the current main version. Do not maintain a PR as though deployed.
2. Inspect open source-watch issues, recent OpenAI releases and available authorized Academy notes. Update the smallest affected file; no wholesale mirroring.
3. Verify model IDs, supported reasoning values, prices, modes, tool compatibility and ChatGPT/Work/Codex/API availability from the most specific current first-party page. An API listing does not prove this account's access. Keep historical supported models when they have a legitimate use; do not retire them merely because a newer one exists.
4. For each learning unit record the actual retrieved section, principle, original procedure/example, and test. Keep outline/read/exercised/measured separate. Never report inaccessible pages as learned.
5. A fingerprint difference or a source fetch success is not a verified product change. Read the changed page; record conflicts and inaccessible scopes in the reference. Update Last verified only for material actually reviewed.
6. Update a source's reviewed_sha256 only after reviewing the exact observed content. If fetch_url changes, run check_sources.py --update and review the new baseline; never fabricate a hash. The watcher keeps observed and reviewed hashes separate.
7. Change model candidates separately from runtime profiles and empirical recommendations. New candidates are unmeasured until compared; do not change live account settings or unrelated skills.
8. Add targeted regressions when behavior changes. Do not tune against final holdouts. Cases already exposed to the implementer are development/smoke cases, not independent holdouts.
9. Run python scripts/validate.py, python -m unittest discover -s tests -v, and python scripts/check_sources.py --no-network. For source changes also run the network watcher and retain failures. For behavior claims run an authorized experiment using evals/PROTOCOL.md; otherwise say effect unmeasured.
10. Bump VERSION, pack.json, both SKILL metadata versions and the top CHANGELOG entry together after a released version. Stage all changes on a new branch and open a reviewable PR. No auto-merge or unapproved paid evaluation.

Report changed files, official URLs and retrieval coverage, verification commands and results, unresolved warnings, measured/unmeasured effects, and deployment state. Existing parent Claude maintenance and this pack must not rewrite each other's files. The existing personal optimize-model-prompt skill is a separate asset until its actual contents are obtained and a migration is approved.
