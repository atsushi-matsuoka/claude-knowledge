"""Regression tests for task-craft infrastructure, not real-model evaluation."""
from __future__ import annotations
import copy
import json
import shutil
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_evals
import bootstrap
import check_sources
import score_task_craft_outcomes as outcomes
import validate_repository


class TaskCraftTests(unittest.TestCase):
    def test_both_skills_exist(self):
        self.assertEqual({p.parent.name for p in (ROOT/'skills').glob('*/SKILL.md')}, {'ecosystem-guide', 'task-craft'})

    def test_existing_default_and_new_target(self):
        self.assertEqual(build_evals.skill_name(), 'ecosystem-guide')
        cases = json.loads((ROOT/'evals/questions.json').read_text())['cases']
        tc = [c for c in cases if c.get('skill') == 'task-craft']
        self.assertGreaterEqual(len(tc), 20)
        self.assertGreaterEqual(sum(not c['should_trigger'] for c in tc), 5)
        self.assertTrue(any('holdout' in c.get('tags', []) for c in tc))
        for c in tc:
            rendered = build_evals.render_case(c, c['skill'])
            self.assertIn('task-craft', rendered['graders/skill.md'])
            self.assertEqual('max: 0' in rendered['graders/skill.md'], not c['should_trigger'])
            if c.get('reads'):
                self.assertIn('task-craft', rendered['graders/route.md'])

    def test_source_watch_finds_new_skill_references(self):
        hits = check_sources.citing_files('https://platform.claude.com/docs/en/test-and-evaluate/develop-tests')
        self.assertTrue(any(p.startswith('skills/task-craft/references/') for p in hits))

    def test_second_skill_version_and_frontmatter_are_checked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'repo'
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns('.git', '__pycache__', '.bootstrap'))
            p = root/'skills/task-craft/SKILL.md'
            p.write_text(p.read_text().replace('version: 0.3.0', 'version: 9.9.9').replace('\nmetadata:', '\nwhen_to_use: always\nmetadata:'))
            errors, _ = validate_repository.validate(root, today=date.today())
            self.assertTrue(any('metadata.version' in e for e in errors))
            self.assertTrue(any('Non-portable' in e for e in errors))

    def test_task_reference_requires_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'repo'
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns('.git', '__pycache__', '.bootstrap'))
            p = root/'skills/task-craft/references/task-framing.md'
            p.write_text(p.read_text().replace('## Sources', '## Bibliography'))
            errors, _ = validate_repository.validate(root, today=date.today())
            self.assertTrue(any('Sources' in e for e in errors))

    def test_multi_skill_install_defaults(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)/'home'
            home.mkdir()
            with patch.object(Path, 'home', return_value=home), patch.object(sys, 'argv', ['bootstrap.py', '--skip-update', '--dest', str(ROOT)]):
                self.assertEqual(bootstrap.main(), 0)
            for name in ('ecosystem-guide', 'task-craft'):
                self.assertTrue((home/'.agents/skills'/name/'SKILL.md').is_file())
                self.assertFalse((home/'.claude/skills'/name).exists())

    def test_multi_skill_claude_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)/'home'
            home.mkdir()
            with patch.object(Path, 'home', return_value=home), patch.object(sys, 'argv', ['bootstrap.py', '--skip-update', '--dest', str(ROOT), '--claude-code']):
                self.assertEqual(bootstrap.main(), 0)
            for name in ('ecosystem-guide', 'task-craft'):
                self.assertTrue((home/'.claude/skills'/name/'SKILL.md').is_file())


class OutcomeScorerTests(unittest.TestCase):
    def setUp(self):
        self.fixtures = json.loads((ROOT/'evals/task-craft-outcomes.json').read_text())
        self.data = {
            'metadata': {'model':'synthetic', 'surface':'unit-test', 'settings':{}, 'skill_version':'0.3.0', 'evidence_kind':'synthetic-unit-test'},
            'trials':1,
            'prompts': {t: {a:'synthetic fixture, not a model prompt' for a in outcomes.ARMS} for t in self.fixtures['tasks']},
            'runs': [{'case_id':c['id'], 'arm':a, 'trial':1, 'output':copy.deepcopy(c['expected'])} for c in self.fixtures['cases'] for a in outcomes.ARMS]
        }

    def test_synthetic_perfect_score_is_not_effectiveness_evidence(self):
        r = outcomes.score(self.fixtures, self.data)
        self.assertEqual(r['arms']['candidate']['passed'], 9)
        self.assertFalse(r['model_effect_measured'])
        self.assertIsNone(r['observed_pass_rate_delta'])

    def test_missing_output_counts_as_failure(self):
        self.data['runs'].pop()
        r = outcomes.score(self.fixtures, self.data)
        self.assertFalse(r['complete'])
        self.assertEqual(sum(a['missing'] for a in r['arms'].values()), 1)
        self.assertIsNone(r['observed_pass_rate_delta'])

    def test_bad_json_is_failure(self):
        self.data['runs'][0]['output'] = 'not JSON'
        r = outcomes.score(self.fixtures, self.data)
        self.assertEqual(r['arms']['baseline']['passed'], 8)

    def test_explicit_tool_error_is_failure(self):
        self.data['runs'][0]['error'] = 'executor unavailable'
        r = outcomes.score(self.fixtures, self.data)
        self.assertEqual(r['arms']['baseline']['passed'], 8)

    def test_duplicate_attempt_is_rejected(self):
        self.data['runs'].append(copy.deepcopy(self.data['runs'][0]))
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            outcomes.score(self.fixtures, self.data)

    def test_unknown_attempt_is_rejected(self):
        self.data['runs'][0]['case_id'] = 'unknown'
        with self.assertRaisesRegex(ValueError, 'Unknown'):
            outcomes.score(self.fixtures, self.data)

    def test_missing_actual_prompts_is_rejected(self):
        del self.data['prompts']['schedule']['candidate']
        with self.assertRaisesRegex(ValueError, 'Missing actual'):
            outcomes.score(self.fixtures, self.data)

    def test_missing_metadata_is_rejected(self):
        del self.data['metadata']['model']
        with self.assertRaisesRegex(ValueError, 'metadata'):
            outcomes.score(self.fixtures, self.data)

    def test_strict_types_and_extra_keys(self):
        self.assertFalse(outcomes.strict_equal(True, 1))
        self.assertFalse(outcomes.strict_equal(1.0, 1))
        self.assertFalse(outcomes.strict_equal({'a':1, 'extra':2}, {'a':1}))
        self.assertFalse(outcomes.strict_equal(['A','B'], ['B','A']))

    def test_positive_trial_count_required(self):
        self.data['trials'] = 0
        with self.assertRaisesRegex(ValueError, 'positive'):
            outcomes.score(self.fixtures, self.data)


if __name__ == '__main__':
    unittest.main()
