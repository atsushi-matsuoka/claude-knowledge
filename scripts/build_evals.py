#!/usr/bin/env python3
"""Generate the `claude plugin eval` suite from evals/questions.json.

questions.json stays the single, agent-neutral source of eval cases. This
script renders one case directory per question under evals/claude-code/:

  <id>/prompt.md            the user prompt plus run limits
  <id>/graders/skill.md     tool_used: Skill (fires / must not fire)
  <id>/graders/expect.md    llm rubric built from the case's `expect` list
  <id>/graders/route.md     tool_used: Read of the expected reference (optional)

Usage:
  python scripts/build_evals.py          # write/refresh the suite
  python scripts/build_evals.py --check  # exit 1 if the suite is out of date
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "evals" / "questions.json"
SUITE = ROOT / "evals" / "claude-code"
SKILLS = ROOT / "skills"
KEEP = {"README.md", "results", ".gitignore"}


def skill_name() -> str:
    names = []
    for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
        m = re.search(r"^name:\s*(\S+)\s*$", skill_md.read_text(encoding="utf-8"), re.M)
        if m:
            names.append(m.group(1))
    if len(names) != 1:
        raise SystemExit(f"Expected exactly one skill under skills/, found {names}")
    return names[0]


def js_escape(s: str) -> str:
    """Escape regex metacharacters without Python's `\\-`, which JS unicode regexes reject."""
    return re.sub(r"([.*+?^${}()|\[\]\\/])", r"\\\1", s)


def yaml_str(s: str) -> str:
    return "'" + s.replace("'", "''") + "'"


def render_case(case: dict, skill: str) -> dict[str, str]:
    tags = ", ".join(case.get("tags", []) + (["should-trigger"] if case["should_trigger"] else ["should-not-trigger"]))
    files: dict[str, str] = {}
    files["prompt.md"] = (
        "---\n"
        f"description: {yaml_str('Generated from evals/questions.json case ' + case['id'])}\n"
        f"tags: [{tags}]\n"
        "max_turns: 12\n"
        "timeout_seconds: 300\n"
        "allowed_tools: [Read, Glob, Grep, Skill]\n"
        "---\n\n"
        f"{case['prompt'].strip()}\n"
    )
    skill_pattern = r'"skill"\s*:\s*"(?:[\w-]+:)?' + js_escape(skill) + '"'
    if case["should_trigger"]:
        files["graders/skill.md"] = (
            "---\ntype: tool_used\ntool: Skill\n"
            f"input_match: {yaml_str(skill_pattern)}\n"
            "---\n"
        )
    else:
        files["graders/skill.md"] = (
            "---\ntype: tool_used\ntool: Skill\n"
            f"input_match: {yaml_str(skill_pattern)}\n"
            "min: 0\nmax: 0\narm: both\n"
            "---\n"
        )
    points = "\n".join(f"- {p}" for p in case["expect"])
    files["graders/expect.md"] = (
        "---\ntype: llm\n---\n\n"
        f"The user asked:\n\n> {case['prompt'].strip()}\n\n"
        "PASS only if the final response satisfies every point below (wording may differ; "
        "judge substance, not formatting):\n\n"
        f"{points}\n\n"
        + ("FAIL if any point is missing, contradicted, or if the response states a changing product "
           "fact (price, limit, model detail, availability) as certain without a source or date caveat.\n"
           if case["should_trigger"] else "FAIL if any point is missing or wrong.\n")
    )
    if case.get("reads"):
        read_pattern = js_escape(case["reads"]) + r"\.md"
        files["graders/route.md"] = (
            "---\ntype: tool_used\ntool: Read\n"
            f"input_match: {yaml_str(read_pattern)}\n"
            "arm: with-only\n"
            "---\n"
        )
    return files


def desired_tree() -> dict[Path, str]:
    data = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    skill = skill_name()
    tree: dict[Path, str] = {}
    for case in data["cases"]:
        for rel, text in render_case(case, skill).items():
            tree[SUITE / case["id"] / rel] = text
    return tree


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ns = ap.parse_args()
    tree = desired_tree()
    wanted_cases = {p.relative_to(SUITE).parts[0] for p in tree}
    existing_cases = {p.name for p in SUITE.iterdir() if p.is_dir() and p.name not in KEEP} if SUITE.exists() else set()

    drift = [str(p.relative_to(ROOT)) for p, t in tree.items() if not p.exists() or p.read_text(encoding="utf-8") != t]
    stale_cases = sorted(existing_cases - wanted_cases)
    extra_files = [
        str(p.relative_to(ROOT))
        for c in wanted_cases & existing_cases
        for p in (SUITE / c).rglob("*")
        if p.is_file() and p not in tree
    ]

    if ns.check:
        problems = drift + [f"stale case dir: evals/claude-code/{c}" for c in stale_cases] + [f"unexpected file: {f}" for f in extra_files]
        if problems:
            print("EVAL SUITE OUT OF DATE (run python scripts/build_evals.py):")
            for p in problems:
                print(f"- {p}")
            return 1
        print(f"EVAL SUITE OK: {len(wanted_cases)} cases")
        return 0

    for c in stale_cases:
        shutil.rmtree(SUITE / c)
    for f in extra_files:
        (ROOT / f).unlink()
    for p, t in tree.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(t, encoding="utf-8")
    print(f"Wrote {len(wanted_cases)} cases to {SUITE.relative_to(ROOT)} (removed {len(stale_cases)} stale)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
