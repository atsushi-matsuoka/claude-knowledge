# Workflow: update the knowledge pack

1. Identify the trigger: Academy learning, source-change alert, user correction, or newly released Claude capability.
2. Locate the smallest affected reference/workflow.
3. Check `sources/manifest.json` for canonical sources and volatility.
4. Verify the relevant current first-party source(s).
5. Update concise original guidance; do not paste source text wholesale.
6. Update the file's `Last verified` date.
7. Add or revise an eval case if the change could regress routing or factual behavior.
8. Run `python scripts/validate_repository.py`.
9. Review the diff for accidental loss of negations, limits, product-surface distinctions, or uncertainty.
10. Commit through a reviewable PR for substantive changes.
