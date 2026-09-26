#!/usr/bin/env python3
"""Summarize `claude plugin eval --json` results into routing metrics.

Metrics (with-plugin runs unless noted):
  trigger recall      should-trigger runs where the skill fired
  false-trigger rate  should-not-trigger runs where the skill fired
  routing accuracy    runs that opened the expected reference (cases with `reads`)
  answer pass rate    runs whose `expect` rubric passed, split by in-scope / out-of-scope
  baseline answers    the same rubric in the no-plugin arm, when it was run

Usage:
  python scripts/summarize_evals.py results.json [more.json ...] [--labels old new] [--per-case]
                                    [--tag holdout | --exclude-tag holdout]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "evals" / "questions.json"


def ratio(hits: int, total: int) -> str:
    return "n/a" if total == 0 else f"{hits}/{total} ({hits / total:.0%})"


def grader(run: dict, name: str) -> dict | None:
    return next((g for g in run.get("graders", []) if g["name"] == name), None)


def summarize(path: Path, cases: dict[str, dict]) -> tuple[dict[str, str], list[tuple]]:
    """`cases` holds only the question ids to count; results for other ids are skipped."""
    data = json.loads(path.read_text(encoding="utf-8"))
    c = {k: [0, 0] for k in ("recall", "false", "route", "ans_in", "ans_out", "base_in", "base_out")}
    rows = []
    for res in data["cases"]:
        q = cases.get(res["name"])
        if q is None:
            continue
        pos = q["should_trigger"]
        fired_runs = 0
        with_runs = res["arms"].get("with", [])
        for run in with_runs:
            s, e, r = grader(run, "skill"), grader(run, "expect"), grader(run, "route")
            if s is not None:
                fired = s["passed"] if pos else not s["passed"]
                fired_runs += fired
                key = "recall" if pos else "false"
                c[key][0] += fired
                c[key][1] += 1
            if r is not None:
                c["route"][0] += r["passed"]
                c["route"][1] += 1
            if e is not None:
                key = "ans_in" if pos else "ans_out"
                c[key][0] += e["passed"]
                c[key][1] += 1
        for run in res["arms"].get("without", []):
            e = grader(run, "expect")
            if e is not None:
                key = "base_in" if pos else "base_out"
                c[key][0] += e["passed"]
                c[key][1] += 1
        rows.append((res["name"], "trigger" if pos else "silent", f"{fired_runs}/{len(with_runs)}",
                     res.get("aggregates", {}).get("score")))
    metrics = {
        "trigger recall": ratio(*c["recall"]),
        "false-trigger rate": ratio(*c["false"]),
        "routing accuracy": ratio(*c["route"]),
        "answer pass (in-scope)": ratio(*c["ans_in"]),
        "answer pass (out-of-scope)": ratio(*c["ans_out"]),
        "baseline answer pass (in-scope)": ratio(*c["base_in"]),
        "baseline answer pass (out-of-scope)": ratio(*c["base_out"]),
        "cost (USD)": f"{data.get('costUsd', 0):.2f}",
        "partial run": str(data.get("partial", False)),
    }
    return metrics, rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("results", nargs="+", type=Path)
    ap.add_argument("--labels", nargs="*")
    ap.add_argument("--per-case", action="store_true")
    ap.add_argument("--tag", help="only count cases carrying this tag")
    ap.add_argument("--exclude-tag", help="skip cases carrying this tag")
    ns = ap.parse_args()
    labels = ns.labels or [p.stem for p in ns.results]
    cases = {q["id"]: q for q in json.loads(QUESTIONS.read_text(encoding="utf-8"))["cases"]
             if (not ns.tag or ns.tag in q.get("tags", []))
             and (not ns.exclude_tag or ns.exclude_tag not in q.get("tags", []))}
    summaries = [summarize(p, cases) for p in ns.results]
    keys = list(summaries[0][0])
    print("| metric | " + " | ".join(labels) + " |")
    print("|---|" + "---|" * len(labels))
    for k in keys:
        print(f"| {k} | " + " | ".join(s[0][k] for s in summaries) + " |")
    if ns.per_case:
        for label, (_, rows) in zip(labels, summaries):
            print(f"\n### {label}\n\n| case | expected | skill fired | score |\n|---|---|---|---|")
            for name, exp, fired, score in rows:
                print(f"| {name} | {exp} | {fired} | {score} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
