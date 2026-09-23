#!/usr/bin/env python3
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
errors=[]
skill=ROOT/"skills"/"sonnet-stack"/"SKILL.md"
if not skill.exists(): errors.append("Missing skills/sonnet-stack/SKILL.md")
else:
    t=skill.read_text()
    if not t.startswith("---\n"): errors.append("SKILL.md must start with YAML frontmatter")
    if "\nname: sonnet-stack\n" not in t: errors.append("SKILL.md name mismatch")
    m=re.search(r"\ndescription:\s*(.+)\n---", t, re.S)
    if not m: errors.append("SKILL.md description missing")
    elif len(m.group(1).strip())>1024: errors.append("SKILL.md description exceeds 1024 chars")

manifest=json.loads((ROOT/"sources"/"manifest.json").read_text())
ids=[x["id"] for x in manifest.get("sources",[])]
if len(ids)!=len(set(ids)): errors.append("Duplicate source id")
for s in manifest.get("sources",[]):
    if not s.get("url","https://").startswith("https://"): errors.append(f"Non-HTTPS source: {s.get('id')}")

evals=json.loads((ROOT/"evals"/"questions.json").read_text())
cases=evals.get("cases",[])
if len(cases)<20: errors.append("Need at least 20 eval cases")
case_ids=[x.get("id") for x in cases]
if len(case_ids)!=len(set(case_ids)): errors.append("Duplicate eval id")
for c in cases:
    if not c.get("prompt") or not c.get("expect"): errors.append(f"Malformed eval: {c.get('id')}")

required=["AGENTS.md","CLAUDE.md","GEMINI.md","README.md","CHANGELOG.md"]
for p in required:
    if not (ROOT/p).exists(): errors.append(f"Missing {p}")

if errors:
    print("VALIDATION FAILED")
    for e in errors: print(f"- {e}")
    sys.exit(1)
print(f"VALIDATION OK: {len(manifest['sources'])} sources, {len(cases)} eval cases")
