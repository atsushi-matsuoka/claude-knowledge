# Results

Initial implementation: no real-model activation, model-routing quality, artifact-quality or downstream effectiveness experiment executed. No paid API calls.

Unit tests exercise the code with synthetic data, safe temporary files and mocked network responses. Their success establishes tested implementation behavior, not improved GPT task quality. Source-fetch smoke checks establish retrieval only. CI logs and the PR contain actual test counts and remaining retrieval failures.

Model candidates are unmeasured on the user's tasks. Academy learning remains partial as recorded in curriculum/academy-map.md. Account-level installation, model switching and host discovery are unconfirmed.

## Verified implementation checks — 2026-09-28 JST

Reviewed code head: `47ae31105a95013e482092fd70b8729842d77236`.
The pack tree tested locally was `4a1b61b48907fb1329788988bf6bd64e832c9ede`,
obtained from the CI artifact and reproduced with Git after extraction.

- `python scripts/validate.py`: passed.
- `python -m unittest discover -s tests -v`: 54 tests passed locally, including source HTTP status/redaction/recovery regressions.
- `python scripts/check_sources.py --no-network`: 17 official URLs passed the manifest check; this command makes no network requests.
- GitHub validation matrix for Python 3.12 and 3.13: https://github.com/atsushi-matsuoka/claude-knowledge/actions/runs/36347176685
- The parent Claude-pack validation also passed; its four pre-existing missing-Sources warnings are not fixes made by this pack.

## Actual source retrieval, not a clean network pass

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
was performed. The 32 routing/artifact cases and six outcome inputs are test
specifications, not 38 passed live-model experiments. CI does not install these
Skills in the user's account. Scheduled Actions activate only after merge to main.
