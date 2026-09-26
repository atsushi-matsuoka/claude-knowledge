"""Tests for the repository tooling. Run: python -m unittest discover -s tests"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_repository  # noqa: E402


def git(*args: str, cwd: Path) -> str:
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.com",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.com"}
    return subprocess.run(["git", *args], cwd=cwd, env=env, check=True, text=True, capture_output=True).stdout


def copy_repo(dst: Path) -> Path:
    ignore = shutil.ignore_patterns(".git", "results", "__pycache__")
    shutil.copytree(ROOT, dst, ignore=ignore)
    return dst


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.repo = copy_repo(self.tmp / "repo")
        self.skill = next((self.repo / "skills").glob("*/SKILL.md"))

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def errors(self):
        return validate_repository.validate(self.repo, today=date(2026, 9, 26))[0]

    def test_repository_is_valid(self):
        self.assertEqual(self.errors(), [])

    def test_reserved_word_in_name_is_rejected(self):
        text = self.skill.read_text().replace("name: ecosystem-guide", "name: claude-helper", 1)
        self.skill.write_text(text)
        self.assertTrue(any("reserved word" in e for e in self.errors()))

    def test_non_portable_frontmatter_is_rejected(self):
        text = self.skill.read_text().replace("\nmetadata:", "\nwhen_to_use: always\nmetadata:", 1)
        self.skill.write_text(text)
        self.assertTrue(any("Non-portable" in e for e in self.errors()))

    def test_description_over_limit_is_rejected(self):
        text = self.skill.read_text().replace("description: ", "description: " + "x" * 1100, 1)
        self.skill.write_text(text)
        self.assertTrue(any("max 1024" in e for e in self.errors()))

    def test_orphan_reference_is_rejected(self):
        (self.skill.parent / "references" / "orphan.md").write_text("# Orphan\n\nLast verified: 2026-09-26\n")
        self.assertTrue(any("orphan.md is not linked" in e for e in self.errors()))

    def test_missing_verified_date_is_rejected(self):
        ref = self.skill.parent / "references" / "mcp.md"
        ref.write_text(ref.read_text().replace("Last verified:", "Checked:"))
        self.assertTrue(any("missing 'Last verified" in e for e in self.errors()))

    def test_stale_reference_only_warns(self):
        errors, warnings = validate_repository.validate(self.repo, today=date(2027, 9, 26))
        self.assertEqual(errors, [])
        self.assertTrue(warnings)

    def test_version_mismatch_is_rejected(self):
        p = self.repo / ".claude-plugin" / "plugin.json"
        data = json.loads(p.read_text())
        data["version"] = "9.9.9"
        p.write_text(json.dumps(data))
        errs = self.errors()
        self.assertTrue(any("metadata.version" in e for e in errs))
        self.assertTrue(any("CHANGELOG" in e for e in errs))

    def test_secret_is_detected(self):
        (self.repo / "notes.md").write_text("key: sk-ant-" + "a" * 40 + "\n")
        self.assertTrue(any("Possible secret" in e for e in self.errors()))

    def test_eval_drift_is_detected(self):
        q = self.repo / "evals" / "questions.json"
        data = json.loads(q.read_text())
        data["cases"][0]["prompt"] += " (edited)"
        q.write_text(json.dumps(data))
        self.assertTrue(any("out of date" in e for e in self.errors()))


class BuildEvalsTests(unittest.TestCase):
    def test_suite_matches_questions(self):
        p = subprocess.run([sys.executable, str(ROOT / "scripts" / "build_evals.py"), "--check"],
                           text=True, capture_output=True)
        self.assertEqual(p.returncode, 0, p.stdout)

    def test_every_case_has_trigger_grader_with_skill_name(self):
        suite = ROOT / "evals" / "claude-code"
        cases = json.loads((ROOT / "evals" / "questions.json").read_text())["cases"]
        for c in cases:
            grader = (suite / c["id"] / "graders" / "skill.md").read_text()
            self.assertIn("ecosystem-guide", grader)
            self.assertEqual("max: 0" in grader, not c["should_trigger"], c["id"])


class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.home = self.tmp / "home"
        self.home.mkdir()
        self.origin = copy_repo(self.tmp / "origin")
        git("init", "-q", "-b", "main", cwd=self.origin)
        # A background auto-gc can repack objects while a local-path clone copies
        # them; disable it and clone through file:// like a real remote.
        git("config", "gc.auto", "0", cwd=self.origin)
        git("config", "gc.autoDetach", "false", cwd=self.origin)
        git("add", "-A", cwd=self.origin)
        git("commit", "-qm", "init", cwd=self.origin)
        self.dest = self.tmp / "checkout"

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def run_bootstrap(self, *extra: str) -> subprocess.CompletedProcess:
        env = {**os.environ, "HOME": str(self.home)}
        return subprocess.run([sys.executable, str(ROOT / "scripts" / "bootstrap.py"),
                               "--repo-url", self.origin.as_uri(), "--dest", str(self.dest), *extra],
                              env=env, text=True, capture_output=True)

    def test_fresh_install_links_agents_path_only_by_default(self):
        p = self.run_bootstrap()
        self.assertEqual(p.returncode, 0, p.stderr)
        link = self.home / ".agents" / "skills" / "ecosystem-guide"
        self.assertTrue((link / "SKILL.md").exists())
        self.assertFalse((self.home / ".claude" / "skills" / "ecosystem-guide").exists())

    def test_claude_code_flag_links_personal_skill(self):
        p = self.run_bootstrap("--claude-code")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertTrue((self.home / ".claude" / "skills" / "ecosystem-guide" / "SKILL.md").exists())

    def test_legacy_links_into_checkout_are_removed(self):
        first = self.run_bootstrap()
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        legacy = self.home / ".claude" / "skills" / "claude-stack"
        legacy.parent.mkdir(parents=True, exist_ok=True)
        legacy.symlink_to(self.dest / "skills" / "claude-stack", target_is_directory=True)
        unrelated = self.home / ".agents" / "skills" / "sonnet-stack"
        unrelated.mkdir(parents=True)
        p = self.run_bootstrap()
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertFalse(legacy.is_symlink())
        self.assertTrue(unrelated.exists(), "ordinary directories must never be deleted")

    def test_dirty_checkout_is_left_untouched(self):
        first = self.run_bootstrap()
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        marker = self.dest / "LOCAL_EDIT.md"
        marker.write_text("local work\n")
        (self.origin / "NEW.md").write_text("upstream\n")
        git("add", "-A", cwd=self.origin)
        git("commit", "-qm", "upstream", cwd=self.origin)
        p = self.run_bootstrap()
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("leaving it untouched", p.stdout)
        self.assertTrue(marker.exists())
        self.assertFalse((self.dest / "NEW.md").exists())


class EnsureFreshTests(unittest.TestCase):
    def test_outside_git_checkout_is_a_noop(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            script = tmp / "ensure_fresh.py"
            shutil.copy(ROOT / "skills" / "ecosystem-guide" / "scripts" / "ensure_fresh.py", script)
            env = {**os.environ, "HOME": str(tmp)}
            p = subprocess.run([sys.executable, str(script)], env=env, text=True, capture_output=True, cwd=tmp)
            self.assertEqual(p.returncode, 0)
            self.assertIn("not inside a Git checkout", p.stdout)
        finally:
            shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main()
