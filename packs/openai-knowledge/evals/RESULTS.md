# Results

Initial implementation: no real-model activation, model-routing quality, artifact-quality or downstream effectiveness experiment executed. No paid API calls.

Unit tests exercise the code with synthetic data, safe temporary files and mocked network responses. Their success establishes tested implementation behavior, not improved GPT task quality. Source-fetch smoke checks establish retrieval only. CI logs and the PR contain actual test counts and remaining retrieval failures.

Model candidates are unmeasured on the user's tasks. Academy learning remains partial as recorded in curriculum/academy-map.md. Account-level installation, model switching and host discovery are unconfirmed.

## Previous initial implementation checks — 2026-09-28 JST

Reviewed code head: `47ae31105a95013e482092fd70b8729842d77236`.
The pack tree tested locally was `4a1b61b48907fb1329788988bf6bd64e832c9ede`,
obtained from the CI artifact and reproduced with Git after extraction.

- `python scripts/validate.py`: passed.
- `python -m unittest discover -s tests -v`: 54 tests passed locally, including source HTTP status/redaction/recovery regressions.
- `python scripts/check_sources.py --no-network`: 17 official URLs passed the manifest check; this command makes no network requests.
- GitHub validation matrix for Python 3.12 and 3.13: https://github.com/atsushi-matsuoka/claude-knowledge/actions/runs/36347176685
- The parent Claude-pack validation also passed; its four pre-existing missing-Sources warnings are not fixes made by this pack.

## Previous 17-source retrieval (superseded below)

Run: https://github.com/atsushi-matsuoka/claude-knowledge/actions/runs/36347174237

At `2026-09-27T20:12:41.709892+00:00`, 16 of 17 sources returned content.
The `work-codex` Help Center page returned **HTTP 403** from the Actions runner.
The watcher correctly remained failed, retained its report and observation artifact,
and did not write main or create an issue from the unmerged branch.
Numeric HTTP status is retained; exception URLs, headers and bodies are not copied.

The public Help article could be read separately through the browser tool; that
is not proof of an Actions fetch succeeding. Keep the retrieval failure visible
and recheck through an authorized browser during semantic maintenance.
Do not disable access controls or replace the page with an unofficial mirror.

The committed source-status.json contains these actual observations. No
`reviewed_sha256` values have been manufactured from search snippets or page
hashes. Initial review-required signals do not imply that all pages changed.

## Not completed by these checks

No live model invocation, automatic model switch, runtime Skill activation,
controlled output-quality comparison, or full Academy course/exercise completion
was performed. The initial 32 routing/artifact cases and six outcome inputs were test
specifications, not 38 passed live-model experiments. The expanded suite is described below. CI does not install these
Skills in the user's account. Scheduled Actions activate only after merge to main.

## Academy survey expansion — 2026-09-28 JST

Implementation head: `0bdc018fe8133ca05e766c3cecdce9de03c56841`.
Before upload, the local tested pack Git tree matched the uploaded tree exactly:
`8446f82fb3468de674e6ddb648d506badb3f31fe`.

- Survey ledger: 30 Academy entries (course groups, series, sessions and resources, not 30 completed courses), seven developer supplements and seven source-to-procedure-to-probe mappings.
- Twelve Academy entries have recorded body/selected-section coverage: seven articles, one transcript and four PDFs. One article's reading is carried forward from the initial PR rather than freshly repeated. None is claimed as a completed course, exercise or model experiment. Other records remain outlines, shells or unavailable attachments.
- Added five practical references and 19 development evaluation specifications: 51 author-visible cases in total. The six synthetic downstream inputs are unchanged. The description and model-selection code/catalogue are unchanged; no new routing effectiveness claim.
- `python scripts/audit_curriculum.py --render`: map generated; the subsequent audit passed. It validates record consistency, not whether learning truly occurred.
- `python scripts/validate.py`: passed locally and in CI.
- `python -m unittest discover -s tests -v`: 75 tests passed locally (54 existing plus 21 curriculum regressions); CI passed on Python 3.12 and 3.13.
- `python scripts/check_sources.py --no-network`: 32-source configuration passed; no network requests in this command.
- OpenAI validation: https://github.com/atsushi-matsuoka/claude-knowledge/actions/runs/36357361772
- Parent validation: https://github.com/atsushi-matsuoka/claude-knowledge/actions/runs/36357361754

### Expanded network observation

Source run: https://github.com/atsushi-matsuoka/claude-knowledge/actions/runs/36357359083

At `2026-09-27T23:03:05.922420+00:00`, the watcher obtained content from 30 of 32 sources.
Two remained HTTP 403: `work-codex` (Help Center) and `learning-dev-harness`
(OpenAI's harness-engineering article). The latter's public text was read via
the browser; that is not a successful Actions fetch. The workflow remains
failed, with its observation artifact retained. No access controls were bypassed,
no sources removed to conceal failure, and no reviewed hashes fabricated.
The committed source-status.json preserves these actual observations.

The network monitor hashes registered web-page bodies only. Academy PDF
attachments require separate inspection; unchanged wrapper pages do not prove
unchanged attachments or complete lesson availability. New-course discovery and
important access gaps are also explicit maintenance work, not guaranteed by hashing.

### Remaining work and scope

Public discovery is not an exhaustive authenticated catalogue. Formal course
lesson bodies, API Bootcamp lessons and some Skill Lab attachments remain pending.
Selected slide/transcript reading does not complete a course. Academy exercises
and real-model activation/quality comparisons remain unexecuted. Independent
final cases still need preparation before claiming empirical gains.

The existing weekly maintenance task was expanded to rediscover catalogue/audience/series
routes during the first weekly pass of each month and revisit important gaps,
while preserving the unmerged-main guard, PR review and no unapproved paid calls.
GitHub schedules and deployment remain inactive for this unmerged PR; no user
account, existing personal Skill or parent Claude file was changed.
