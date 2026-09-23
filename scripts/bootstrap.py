#!/usr/bin/env python3
"""Install or update the knowledge repo and link its shared Agent Skill.

Safe properties:
- clone when missing
- fast-forward only when existing checkout is clean
- never resets or discards changes
- symlink when possible, copy as a fallback
"""
from __future__ import annotations
import argparse, os, shutil, subprocess, sys
from pathlib import Path

SKILL_NAME = "claude-stack"
LEGACY_SKILL_NAMES = ("sonnet-stack",)
DEFAULT_DEST = Path.home()/".local"/"share"/"claude-knowledge"


def run(*args: str, cwd: Path | None = None, check: bool = False):
    p = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    if check and p.returncode:
        raise RuntimeError((p.stderr or p.stdout).strip())
    return p


def clone_or_update(repo_url: str, dest: Path) -> None:
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        print(f"Cloning {repo_url} -> {dest}")
        run("git", "clone", "--filter=blob:none", repo_url, str(dest), check=True)
        return
    if not (dest/".git").exists():
        raise RuntimeError(f"Destination exists but is not a Git repo: {dest}")
    dirty = run("git", "-C", str(dest), "status", "--porcelain", check=True).stdout.strip()
    if dirty:
        print("Local checkout has changes; leaving it untouched.")
        return
    print(f"Updating {dest} with fast-forward only")
    run("git", "-C", str(dest), "pull", "--ff-only", check=True)


def install_link(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.is_symlink():
        current = Path(os.path.realpath(target))
        if current == source.resolve():
            print(f"OK {target} -> {source}")
            return
        target.unlink()
    elif target.exists():
        backup = target.with_name(target.name + ".backup")
        if backup.exists():
            raise RuntimeError(f"Refusing to replace existing {target}; backup already exists: {backup}")
        target.rename(backup)
        print(f"Backed up existing {target} -> {backup}")
    try:
        target.symlink_to(source, target_is_directory=True)
        print(f"Linked {target} -> {source}")
    except OSError:
        shutil.copytree(source, target)
        print(f"Symlink unavailable; copied {source} -> {target}")


def remove_legacy_links(dest: Path) -> None:
    for legacy in LEGACY_SKILL_NAMES:
        old_source = (dest/"skills"/legacy).resolve(strict=False)
        for target in (
            Path.home()/".claude"/"skills"/legacy,
            Path.home()/".agents"/"skills"/legacy,
        ):
            if target.is_symlink():
                resolved = target.resolve(strict=False)
                if resolved == old_source:
                    target.unlink()
                    print(f"Removed legacy link {target}")
            elif target.exists():
                print(f"Legacy path still exists and was not removed automatically: {target}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-url", default=os.environ.get("CLAUDE_KNOWLEDGE_REPO"))
    ap.add_argument("--dest", type=Path, default=DEFAULT_DEST)
    ap.add_argument("--skip-update", action="store_true", help="Use current checkout without git pull")
    ns = ap.parse_args()

    dest = ns.dest.expanduser().resolve()
    if not dest.exists() and not ns.repo_url:
        ap.error("--repo-url (or CLAUDE_KNOWLEDGE_REPO) is required for first install")
    if not ns.skip_update:
        repo_url = ns.repo_url
        if not repo_url and dest.exists():
            p = run("git", "-C", str(dest), "remote", "get-url", "origin")
            repo_url = p.stdout.strip() if p.returncode == 0 else None
        if not repo_url:
            ap.error("Cannot determine repository URL")
        clone_or_update(repo_url, dest)

    skill = dest/"skills"/SKILL_NAME
    if not (skill/"SKILL.md").exists():
        raise RuntimeError(f"Skill not found: {skill}")

    # Claude Code personal skill.
    install_link(skill, Path.home()/".claude"/"skills"/SKILL_NAME)
    # Codex USER scope. Gemini CLI also supports ~/.agents/skills as an alias.
    install_link(skill, Path.home()/".agents"/"skills"/SKILL_NAME)

    remove_legacy_links(dest)
    print("Installed. Restart/reload your local agent if it does not discover the skill immediately.")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
