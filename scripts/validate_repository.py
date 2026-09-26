#!/usr/bin/env python3
"""Validate repository invariants for the knowledge pack.

Checks the Agent Skills spec constraints that hosts enforce at upload time,
this repo's context-budget policy, plugin/marketplace consistency, dated
references, eval-suite drift, and obvious secrets. Standard library only.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[1]

SPEC_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
RESERVED_WORDS = ("anthropic", "claude")
SPEC_MAX_BODY_LINES = 500          # Agent Skills best practice
POLICY_MAX_SKILL_LINES = 150       # this repo: keep the always-loaded body small
TOC_THRESHOLD_LINES = 100          # references longer than this need "## Contents"
STALE_WARN_DAYS = 90
MIN_CASES, MIN_NEGATIVE_CASES = 20, 5
LEGACY_NAMES = ("sonnet-stack", "claude-stack")
LEGACY_ALLOWED = {"CHANGELOG.md", "README.md", "scripts/bootstrap.py", "scripts/validate_repository.py",
                  "handoffs/claude-autonomous-implementation.md"}  # history, migration code, original prompt
SECRET_PATTERNS = [
    re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]
LINK_RE = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
DATE_RE = re.compile(r"^Last verified:\s*(\d{4}-\d{2}-\d{2})\s*$", re.M)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str] | None:
    """Parse the top-level keys of a YAML frontmatter block (values kept as raw text)."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    block, body = text[4:end], text[end + 5:]
    fields: dict[str, str] = {}
    current = None
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            current = m.group(1)
            fields[current] = m.group(2).strip()
        elif current and line.startswith((" ", "\t")):
            fields[current] += "\n" + line
    return fields, body


def tracked_files(root: Path) -> list[Path]:
    p = subprocess.run(["git", "-C", str(root), "ls-files", "-co", "--exclude-standard"],
                       text=True, capture_output=True)
    if p.returncode == 0:
        return [root / f for f in p.stdout.splitlines() if (root / f).is_file()]
    return [f for f in root.rglob("*") if f.is_file() and ".git" not in f.parts]


def validate(root: Path = DEFAULT_ROOT, today: date | None = None) -> tuple[list[str], list[str]]:
    today = today or date.today()
    errors: list[str] = []
    warnings: list[str] = []

    for p in ("AGENTS.md", "CLAUDE.md", "GEMINI.md", "README.md", "CHANGELOG.md",
              ".claude-plugin/plugin.json", ".claude-plugin/marketplace.json"):
        if not (root / p).exists():
            errors.append(f"Missing {p}")

    # --- Skill ---------------------------------------------------------------
    skill_dirs = sorted(d for d in (root / "skills").glob("*") if (d / "SKILL.md").exists())
    if len(skill_dirs) != 1:
        errors.append(f"Expected exactly one skill under skills/, found {[d.name for d in skill_dirs]}")
        return errors, warnings
    skill_dir = skill_dirs[0]
    skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    parsed = parse_frontmatter(skill_text)
    if not parsed:
        errors.append("SKILL.md must start with a closed YAML frontmatter block")
        return errors, warnings
    fm, body = parsed
    name, desc = fm.get("name", ""), fm.get("description", "")

    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        errors.append(f"Skill name '{name}' must be lowercase letters/digits/hyphens, max 64 chars")
    if any(w in name for w in RESERVED_WORDS):
        errors.append(f"Skill name '{name}' contains a reserved word {RESERVED_WORDS}; claude.ai/API uploads reject it")
    if name != skill_dir.name:
        errors.append(f"Skill name '{name}' must match its directory '{skill_dir.name}'")
    if not desc:
        errors.append("SKILL.md description missing")
    if len(desc) > 1024:
        errors.append(f"SKILL.md description is {len(desc)} chars (max 1024)")
    if re.search(r"[<>]", desc):
        errors.append("SKILL.md description must not contain XML/angle brackets")
    if re.match(r"(?i)(i|you|we)\b", desc):
        errors.append("SKILL.md description should be third person (not 'I/You/We ...')")
    extra = set(fm) - SPEC_FIELDS
    if extra:
        errors.append(f"Non-portable SKILL.md frontmatter {sorted(extra)}; claude.ai/API packaging rejects them")

    n_lines = len(skill_text.splitlines())
    if n_lines > SPEC_MAX_BODY_LINES:
        errors.append(f"SKILL.md has {n_lines} lines (spec guidance: < {SPEC_MAX_BODY_LINES})")
    elif n_lines > POLICY_MAX_SKILL_LINES:
        errors.append(f"SKILL.md has {n_lines} lines (repo policy: <= {POLICY_MAX_SKILL_LINES}); move detail to references/")
    if DATE_RE.search(body):
        errors.append("Keep dated facts out of SKILL.md; put 'Last verified' content in references/")

    linked = set()
    for target in LINK_RE.findall(body):
        if target.startswith(("http://", "https://")):
            continue
        path = (skill_dir / target).resolve()
        if not path.exists():
            errors.append(f"SKILL.md links to missing file: {target}")
        linked.add(path)

    for sub in ("references", "workflows"):
        for f in sorted((skill_dir / sub).glob("*.md")):
            rel = f"{sub}/{f.name}"
            text = f.read_text(encoding="utf-8")
            if f.resolve() not in linked:
                errors.append(f"{rel} is not linked from SKILL.md (orphaned or unreachable)")
            for target in LINK_RE.findall(text):
                if not target.startswith(("http://", "https://")) and target.endswith(".md"):
                    errors.append(f"{rel} links to {target}; keep references one level deep from SKILL.md")
            if len(text.splitlines()) > TOC_THRESHOLD_LINES and "## Contents" not in text:
                errors.append(f"{rel} exceeds {TOC_THRESHOLD_LINES} lines without a '## Contents' section")
            if sub == "references":
                m = DATE_RE.search(text)
                if not m:
                    errors.append(f"{rel} missing 'Last verified: YYYY-MM-DD'")
                else:
                    d = date.fromisoformat(m.group(1))
                    if d > today:
                        errors.append(f"{rel} Last verified date {d} is in the future")
                    elif (today - d).days > STALE_WARN_DAYS:
                        warnings.append(f"{rel} last verified {d} ({(today - d).days} days ago)")

    # --- Plugin / marketplace ----------------------------------------------
    try:
        plugin = json.loads((root / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        market = json.loads((root / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Plugin manifests unreadable: {exc}")
        plugin, market = {}, {}
    version = plugin.get("version", "")
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        errors.append(f"plugin.json version '{version}' is not semver")
    entries = {p.get("name"): p for p in market.get("plugins", [])}
    if plugin.get("name") not in entries:
        errors.append("marketplace.json has no entry matching plugin.json name")
    elif entries[plugin["name"]].get("source") != "./":
        errors.append("marketplace entry source must be './' (repository root is the plugin)")
    meta_version = re.search(r"^\s+version:\s*(\S+)", fm.get("metadata", ""), re.M)
    if not meta_version or meta_version.group(1) != version:
        errors.append("SKILL.md metadata.version must equal plugin.json version")
    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8") if (root / "CHANGELOG.md").exists() else ""
    top = re.search(r"^## (\d+\.\d+\.\d+)", changelog, re.M)
    if not top or top.group(1) != version:
        errors.append("Top CHANGELOG.md entry must match plugin.json version")

    # --- Sources -----------------------------------------------------------
    manifest = json.loads((root / "sources/manifest.json").read_text(encoding="utf-8"))
    ids = [s["id"] for s in manifest.get("sources", [])]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate source id in sources/manifest.json")
    for s in manifest.get("sources", []):
        if not s.get("url", "").startswith("https://"):
            errors.append(f"Non-HTTPS source: {s.get('id')}")

    # --- Evals -------------------------------------------------------------
    evals = json.loads((root / "evals/questions.json").read_text(encoding="utf-8"))
    cases = evals.get("cases", [])
    case_ids = [c.get("id") for c in cases]
    if len(cases) < MIN_CASES:
        errors.append(f"Need at least {MIN_CASES} eval cases")
    if len(case_ids) != len(set(case_ids)):
        errors.append("Duplicate eval id")
    ref_stems = {f.stem for sub in ("references", "workflows") for f in (skill_dir / sub).glob("*.md")}
    for c in cases:
        if not c.get("prompt") or not c.get("expect") or not isinstance(c.get("should_trigger"), bool):
            errors.append(f"Malformed eval (needs prompt, expect, boolean should_trigger): {c.get('id')}")
        if c.get("reads") and c["reads"] not in ref_stems:
            errors.append(f"Eval {c.get('id')} reads unknown reference '{c['reads']}'")
    if sum(1 for c in cases if c.get("should_trigger") is False) < MIN_NEGATIVE_CASES:
        errors.append(f"Need at least {MIN_NEGATIVE_CASES} should-not-trigger cases")
    build = root / "scripts/build_evals.py"
    if build.exists():
        p = subprocess.run([sys.executable, str(build), "--check"], text=True, capture_output=True)
        if p.returncode != 0:
            errors.append("Generated eval suite is out of date:\n  " + p.stdout.strip().replace("\n", "\n  "))

    # --- Hygiene -----------------------------------------------------------
    for f in tracked_files(root):
        rel = f.relative_to(root).as_posix()
        if f.suffix in {".png", ".jpg", ".pdf", ".zip"} or rel.startswith("tests/"):
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pat in SECRET_PATTERNS:
            if pat.search(text):
                errors.append(f"Possible secret in {rel} ({pat.pattern[:16]}...)")
        if rel not in LEGACY_ALLOWED and any(n in text for n in LEGACY_NAMES):
            errors.append(f"{rel} still references a legacy skill name {LEGACY_NAMES}")

    return errors, warnings


def main() -> int:
    errors, warnings = validate()
    for w in warnings:
        print(f"WARNING: {w}")
    if errors:
        print("VALIDATION FAILED")
        for e in errors:
            print(f"- {e}")
        return 1
    root = DEFAULT_ROOT
    n_sources = len(json.loads((root / "sources/manifest.json").read_text())["sources"])
    n_cases = len(json.loads((root / "evals/questions.json").read_text())["cases"])
    print(f"VALIDATION OK: {n_sources} sources, {n_cases} eval cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
