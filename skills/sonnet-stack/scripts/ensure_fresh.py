#!/usr/bin/env python3
"""Fast-forward the containing knowledge repo when safe and stale.

This script never discards changes and never rebases. It is designed to be
called by a local agent when the skill has already been installed from a Git
checkout (often via symlink).
"""
from __future__ import annotations
import argparse, json, subprocess, time
from pathlib import Path


def run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True)


def repo_root(start: Path) -> Path | None:
    p = run("git", "-C", str(start), "rev-parse", "--show-toplevel")
    return Path(p.stdout.strip()) if p.returncode == 0 else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-age-hours", type=float, default=24)
    ap.add_argument("--force", action="store_true")
    ns = ap.parse_args()

    root = repo_root(Path(__file__).resolve())
    if not root:
        print("Freshness check skipped: skill is not inside a Git checkout.")
        return 0

    cache = Path.home()/".cache"/"sonnet-stack"/"last-sync.json"
    cache.parent.mkdir(parents=True, exist_ok=True)
    if cache.exists() and not ns.force:
        try:
            last = json.loads(cache.read_text()).get("checked_at", 0)
            if time.time() - float(last) < ns.max_age_hours * 3600:
                print("Freshness check skipped: checked recently.")
                return 0
        except Exception:
            pass

    dirty = run("git", "-C", str(root), "status", "--porcelain")
    if dirty.returncode != 0 or dirty.stdout.strip():
        print("Freshness check: local changes present; not updating.")
        return 0

    fetch = run("git", "-C", str(root), "fetch", "--quiet", "--prune")
    if fetch.returncode != 0:
        print("Freshness check: fetch failed; keeping current version.")
        return 0

    branch = run("git", "-C", str(root), "branch", "--show-current").stdout.strip()
    upstream = run("git", "-C", str(root), "rev-parse", "--abbrev-ref", "@{upstream}")
    if not branch or upstream.returncode != 0:
        print("Freshness check: no tracking branch; keeping current version.")
        return 0

    pull = run("git", "-C", str(root), "merge", "--ff-only", upstream.stdout.strip())
    if pull.returncode == 0:
        print("Freshness check: repository is current (fast-forward applied if needed).")
        cache.write_text(json.dumps({"checked_at": time.time()}, indent=2))
    else:
        print("Freshness check: fast-forward not possible; keeping current version.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
