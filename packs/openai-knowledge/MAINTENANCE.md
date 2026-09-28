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

## Source access failures

Read `http_status` when present. A 403 or other failed fetch remains a visible
failure; a browser being able to read the same public page does not make the
runner check successful. Use an authorized browser for semantic review, retain
the access limitation, and retry in a later maintenance run. Do not remove the
source, weaken access restrictions or manufacture a reviewed hash merely to make
CI green. Where the exact fetched body was not inspected, leave the reviewed
baseline unset even if an observation hash exists.

The weekly maintenance task handles both this pack and the separate existing
personal `optimize-model-prompt` Skill when it is actually accessible. Do not
create a second overlapping schedule or assume that personal Skill was migrated.

## Curriculum discovery and deepening

During the first weekly maintenance pass of each month, rediscover the public course catalogue, audience/community routes and relevant API/Codex/agent series. Do not limit discovery to already registered URLs. Review unresolved core gaps on other weekly passes when a usable public body or authorized note becomes available. Inventory counts describe the surveyed set, not a complete authenticated catalogue.

Maintain curriculum/academy-inventory.json: exact public source, priority and rationale, access coverage and read sections, unresolved gaps, and a concrete revisit action. Preserve catalogue/search discrepancies and duplicate wrapper/series identities. Never call unseen material unnecessary. Broad learning does not require loading the catalogue in every task.

For a new learning unit, link actually read sources to the smallest original procedure and development probes. Developer supplements do not complete an Academy course. Selected PDF/transcript reading is not whole-video/whole-course completion. Keep exercise execution and model effects separately evidenced; failures retrieving attachments remain visible. Watch Academy wrapper URLs, and manually verify linked attachment identity/content when reviewing them; wrapper hashes alone cannot prove unchanged PDFs. Do not broaden the source fetch allowlist to arbitrary CDNs.

After changing the ledger run python scripts/audit_curriculum.py --render and the full pack validation/tests. When adding watch sources, run the network watcher and retain actual successes/failures; never promote an uninspected observation hash to reviewed_sha256. Record curriculum gaps separately from mechanical validation success.
