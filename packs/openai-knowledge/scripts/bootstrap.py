#!/usr/bin/env python3
"""Safely clone/refresh a known checkout and link this pack; never edit account settings."""
from __future__ import annotations
import argparse
import subprocess
from pathlib import Path

REPO = 'https://github.com/atsushi-matsuoka/claude-knowledge.git'
SUBDIR = Path('packs/openai-knowledge')
NAMES = ('openai-guide', 'gpt-workbench')


def git(path: Path, *args: str) -> str:
    p = subprocess.run(['git', '-C', str(path), *args], text=True, capture_output=True, timeout=120)
    if p.returncode:
        raise RuntimeError('Git operation failed; checkout left intact: ' + ' '.join(args[:2]))
    return p.stdout.strip()


def refresh(path: Path) -> None:
    if git(path, 'remote', 'get-url', 'origin').removesuffix('.git') != REPO.removesuffix('.git'):
        raise ValueError('refusing unexpected origin')
    if git(path, 'branch', '--show-current') != 'main':
        raise ValueError('refusing non-main checkout')
    if git(path, 'status', '--porcelain'):
        raise ValueError('local changes: leaving checkout untouched')
    git(path, 'pull', '--ff-only', 'origin', 'main')


def install(pack: Path, target_root: Path) -> None:
    pairs = [(pack/'skills'/name, target_root/name) for name in NAMES]
    # Preflight every path before creating any links.
    for source, target in pairs:
        if not (source/'SKILL.md').is_file():
            raise ValueError('missing source skill')
        if target.is_symlink():
            if target.resolve(strict=False) != source.resolve():
                raise ValueError('refusing unrelated symlink: ' + target.name)
        elif target.exists():
            raise ValueError('refusing existing directory/file: ' + target.name)
    target_root.mkdir(parents=True, exist_ok=True)
    made = []
    try:
        for source, target in pairs:
            if not target.is_symlink():
                target.symlink_to(source.resolve(), target_is_directory=True)
                made.append(target)
    except OSError:
        for target in reversed(made):
            target.unlink()
        raise RuntimeError('symlink creation failed; new links rolled back') from None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--checkout', type=Path, required=True)
    ap.add_argument('--clone', action='store_true')
    ap.add_argument('--refresh', action='store_true')
    ns = ap.parse_args()
    checkout = ns.checkout.expanduser().resolve()
    if not checkout.exists():
        if not ns.clone:
            ap.error('checkout missing: specify --clone to create it')
        checkout.parent.mkdir(parents=True, exist_ok=True)
        p = subprocess.run(['git', 'clone', '--branch', 'main', '--single-branch', REPO, str(checkout)], timeout=120)
        if p.returncode:
            raise RuntimeError('clone failed; no skills installed')
    elif ns.refresh:
        refresh(checkout)
    pack = checkout/SUBDIR if (checkout/SUBDIR/'pack.json').is_file() else checkout
    if not (pack/'pack.json').is_file():
        raise ValueError('pack not found in checkout')
    install(pack, Path.home()/'.agents/skills')
    print('Local links installed. Verify host discovery; no account or model settings were changed.')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError, OSError, subprocess.TimeoutExpired) as exc:
        raise SystemExit(str(exc))
