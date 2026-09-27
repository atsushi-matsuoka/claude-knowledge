#!/usr/bin/env python3
"""Score supplied downstream model outputs; never invokes a model or API.

See evals/TASK_CRAFT.md for collection protocol. Synthetic fixtures are not
model-effectiveness evidence. Missing attempts count as failures and make the
comparison incomplete. Extra/duplicate attempts are rejected.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARMS = ("baseline", "candidate")


def strict_equal(actual, expected) -> bool:
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(strict_equal(actual[k], v) for k, v in expected.items())
    if isinstance(expected, list):
        return len(actual) == len(expected) and all(strict_equal(a, b) for a, b in zip(actual, expected))
    return actual == expected


def score(fixtures: dict, data: dict) -> dict:
    meta = data.get("metadata", {})
    for key in ("model", "surface", "settings", "skill_version", "evidence_kind"):
        if key not in meta:
            raise ValueError(f"Missing shared comparison metadata: {key}")
    if meta["evidence_kind"] not in ("model-run", "synthetic-unit-test"):
        raise ValueError("Unknown evidence_kind")
    if not all(isinstance(meta[k], str) and meta[k].strip() for k in ("model", "surface", "skill_version")):
        raise ValueError("Model, surface and skill_version must be nonempty strings")
    if not isinstance(meta["settings"], dict):
        raise ValueError("settings must be an object shared by both arms")
    trials = data.get("trials", 1)
    if type(trials) is not int or trials < 1:
        raise ValueError("trials must be a positive integer")
    cases = {c["id"]: c for c in fixtures["cases"]}
    if len(cases) != len(fixtures["cases"]):
        raise ValueError("Duplicate fixture id")
    for task in fixtures["tasks"]:
        for arm in ARMS:
            prompt = data.get("prompts", {}).get(task, {}).get(arm)
            if not isinstance(prompt, str) or not prompt.strip():
                raise ValueError(f"Missing actual designed prompt: {task}/{arm}")
    indexed = {}
    for run in data.get("runs", []):
        key = (run.get("case_id"), run.get("arm"), run.get("trial"))
        cid, arm, trial = key
        if cid not in cases or arm not in ARMS or type(trial) is not int or not 1 <= trial <= trials:
            raise ValueError(f"Unknown attempt: {key}")
        if key in indexed:
            raise ValueError(f"Duplicate attempt: {key}")
        indexed[key] = run
    result = {"metadata": meta, "scorer_only": True, "arms": {}, "failures": []}
    for arm in ARMS:
        passed = missing = 0
        for cid, case in cases.items():
            for trial in range(1, trials + 1):
                run = indexed.get((cid, arm, trial))
                ok = False
                if run is None:
                    missing += 1
                elif not run.get("error") and "output" in run:
                    output = run["output"]
                    try:
                        output = json.loads(output) if isinstance(output, str) else output
                        ok = strict_equal(output, case["expected"])
                    except (ValueError, TypeError):
                        pass
                if ok:
                    passed += 1
                else:
                    result["failures"].append({"case_id": cid, "arm": arm, "trial": trial, "missing": run is None})
        total = len(cases) * trials
        result["arms"][arm] = {"passed": passed, "total": total, "missing": missing, "rate": passed / total if total else None}
    complete = all(v["missing"] == 0 for v in result["arms"].values())
    result["complete"] = complete
    result["model_effect_measured"] = complete and bool(cases) and meta["evidence_kind"] == "model-run"
    result["observed_pass_rate_delta"] = (
        result["arms"]["candidate"]["rate"] - result["arms"]["baseline"]["rate"]
        if result["model_effect_measured"] else None
    )
    result["limitation"] = "Scores supplied outputs only; provenance and equivalent execution conditions need independent checking. This is not proof of general capability improvement."
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("records", type=Path)
    ap.add_argument("--fixtures", type=Path, default=ROOT / "evals/task-craft-outcomes.json")
    ap.add_argument("--output", type=Path)
    ns = ap.parse_args()
    try:
        result = score(json.loads(ns.fixtures.read_text(encoding="utf-8")), json.loads(ns.records.read_text(encoding="utf-8")))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        ap.error(str(exc))
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if ns.output:
        ns.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["complete"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
