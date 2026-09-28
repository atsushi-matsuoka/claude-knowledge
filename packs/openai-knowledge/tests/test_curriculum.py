"""Offline record-integrity regressions, not Academy or real-model evaluations."""
from __future__ import annotations
import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import audit_curriculum as curriculum
import check_sources


class CurriculumTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((ROOT/'curriculum/academy-inventory.json').read_text(encoding='utf-8'))
        self.today=date.fromisoformat(self.data['surveyed_on'])

    def row(self,id):
        return next(r for r in self.data['resources'] if r['id']==id)

    def errors(self):
        return curriculum.audit(self.data,ROOT,self.today)

    def test_current_inventory_and_generated_map(self):
        self.assertEqual(curriculum.validate(ROOT),[])

    def test_global_completion_requires_evidence(self):
        self.data['scope']['complete']=True
        self.assertTrue(any('completeness_evidence' in e for e in self.errors()))

    def test_scope_cannot_hide_limitations(self):
        self.data['scope']['limitations']=[]
        self.assertTrue(self.errors())

    def test_navigation_shell_cannot_complete_course(self):
        r=self.row('agents-course');r['course_completed']=True;r['completion_evidence']='synthetic false claim'
        self.assertTrue(any('completion claim' in e for e in self.errors()))

    def test_read_claim_needs_section_locators(self):
        self.row('codex103')['locators']=[]
        self.assertTrue(any('locators' in e for e in self.errors()))

    def test_conditional_decision_requires_reason_and_revisit(self):
        for field in ('reason','next_action'):
            with self.subTest(field=field):
                original=self.row('educators')[field]
                self.row('educators')[field]=''
                self.assertTrue(any('rationale' in e for e in self.errors()))
                self.row('educators')[field]=original

    def test_exercise_claim_needs_separate_evidence(self):
        self.row('activator')['exercise_status']='executed'
        self.assertTrue(any('separate evidence' in e for e in self.errors()))

    def test_reading_does_not_measure_effect(self):
        self.row('data-science')['model_effect']='measured'
        self.assertTrue(any('separate evidence' in e for e in self.errors()))

    def test_duplicate_sources_fail(self):
        self.data['resources'].append(copy.deepcopy(self.data['resources'][0]))
        self.assertTrue(any('duplicate resource' in e for e in self.errors()))

    def test_unknown_basis_and_outline_basis_fail(self):
        for src in ('missing','api-agents'):
            with self.subTest(src=src):
                self.data['learning_units'][0]['basis']=[src]
                self.assertTrue(any('actually read' in e for e in self.errors()))

    def test_missing_probe_is_detected(self):
        self.data['learning_units'][0]['probes']=['nonexistent-case']
        self.assertTrue(any('unknown development probe' in e for e in self.errors()))

    def test_unsafe_procedure_is_detected(self):
        self.data['learning_units'][0]['procedure']='../../outside.md'
        self.assertTrue(any('unsafe procedure' in e for e in self.errors()))

    def test_missing_original_example_is_detected(self):
        self.data['learning_units'][0]['example_section']='not present'
        self.assertTrue(any('original-example' in e for e in self.errors()))

    def test_arbitrary_attachment_host_is_rejected(self):
        self.row('codex101')['attachment_url']='https://example.org/training.pdf'
        self.assertTrue(any('attachment must' in e for e in self.errors()))

    def test_cdn_watch_access_has_not_been_enabled(self):
        with self.assertRaises(ValueError):
            check_sources.check_url(self.row('codex101')['attachment_url'])

    def test_future_survey_date_is_rejected(self):
        self.data['surveyed_on']='2099-01-01'
        self.assertTrue(any('future' in e for e in self.errors()))

    def test_stale_generated_map_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'pack'
            shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.git','__pycache__'))
            p=root/'curriculum/academy-map.md';p.write_text(p.read_text()+'tampered\n')
            self.assertTrue(any('stale' in e for e in curriculum.validate(root)))

    def test_malformed_container_returns_error(self):
        for bad in (None,[],{}):
            with self.subTest(bad=bad):
                self.assertTrue(curriculum.audit(bad,ROOT,self.today))

    def test_cli_does_not_claim_learning_effect(self):
        p=subprocess.run([sys.executable,str(ROOT/'scripts/audit_curriculum.py')],capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertIn('not established',p.stdout)

    def test_generated_map_is_deterministic(self):
        self.assertEqual(curriculum.render(self.data),curriculum.render(copy.deepcopy(self.data)))

    def test_source_report_finds_curriculum_file(self):
        src={'id':'catalogue','url':'https://academy.openai.com/pages/courses'}
        state={'observed_at':'synthetic','sources':{'catalogue':{'review_required':True,'ok':True}}}
        self.assertIn('curriculum/academy-inventory.json',check_sources.render_report(state,{'sources':[src]},ROOT))
