"""Synthetic offline regressions. These tests do not measure model effectiveness."""
from __future__ import annotations
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import bootstrap
import check_sources
import route
import score_outputs
import validate


def read(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8'))


class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.catalog = read('skills/openai-guide/references/models.json')
        self.today = date.fromisoformat(self.catalog['models'][0]['evidence_as_of'])
        self.task = dict(surface='api-responses', complexity='simple', failure_cost='low')
        self.runtime = dict(surface='api-responses', evidence='tool-listed', observed_on=str(self.today),
                            available_models=[m['id'] for m in self.catalog['models']])

    def call(self):
        return route.recommend(self.task, self.runtime, self.catalog, self.today)

    def test_simple_efficient(self):
        r = self.call()
        self.assertEqual((r['tier'], r['effort']), (0, 'low'))
        self.assertFalse(r['switch_executed'])

    def test_standard_balanced(self):
        self.task['complexity'] = 'standard'
        self.assertEqual(self.call()['tier'], 1)

    def test_complex_high(self):
        self.task['complexity'] = 'complex'
        self.assertEqual(self.call()['tier'], 2)

    def test_short_semantic_precision_is_important(self):
        self.task['semantic_precision'] = True
        r = self.call()
        self.assertEqual((r['tier'], r['effort']), (2, 'high'))

    def test_risk_overrides_length(self):
        self.task['failure_cost'] = 'high'
        self.assertEqual(self.call()['tier'], 2)

    def test_observed_failure_escalates_one_tier(self):
        self.task['quality_failure'] = True
        self.assertEqual(self.call()['tier'], 1)

    def test_missing_evidence_does_not_select_model(self):
        self.task['blocked_by_evidence'] = True
        r = self.call()
        self.assertIsNone(r['model'])
        self.assertEqual(r['status'], 'repair_evidence_or_access_first')

    def test_no_runtime_no_selected_id(self):
        self.assertIsNone(route.recommend(self.task, None, self.catalog, self.today)['model'])

    def test_unknown_availability_not_assumed(self):
        self.runtime['evidence'] = 'not-yet-checked'
        self.assertIsNone(self.call()['model'])

    def test_stale_and_future_runtime_rejected(self):
        for offset in (-8, 1):
            self.runtime['observed_on'] = str(self.today + timedelta(days=offset))
            self.assertEqual(self.call()['status'], 'runtime_confirmation_stale')

    def test_no_silent_quality_downgrade(self):
        self.task['failure_cost'] = 'high'
        self.runtime['available_models'] = [m['id'] for m in self.catalog['models'] if m['tier'] < 2]
        self.assertEqual(self.call()['status'], 'required_tier_unavailable')

    def test_stronger_available_fallback(self):
        self.runtime['available_models'] = [m['id'] for m in self.catalog['models'] if m['tier'] == 1]
        r = self.call()
        self.assertEqual(r['model'], next(m['id'] for m in self.catalog['models'] if m['tier'] == 1))

    def test_chat_surface_never_uses_api_id(self):
        self.task['surface'] = 'chatgpt'
        self.assertIsNone(self.call()['model'])

    def test_unsupported_effort_rejected(self):
        self.task.update(complexity='complex', requested_effort='none')
        with self.assertRaisesRegex(ValueError, 'unsupported effort'):
            self.call()

    def test_catalog_staleness_blocks_selection(self):
        for m in self.catalog['models']:
            m['evidence_as_of'] = str(self.today-timedelta(days=15))
        self.assertEqual(self.call()['status'], 'needs_source_refresh')

    def test_invalid_classification_rejected(self):
        for changes in ({'complexity':'mystery'}, {'failure_cost':'maybe'}, {'semantic_precision':'false'}):
            with self.subTest(changes=changes):
                self.task.update(changes)
                with self.assertRaises(ValueError):
                    self.call()
                self.setUp()

    def test_selected_is_still_only_candidate(self):
        r = self.call()
        self.assertEqual(r['effectiveness'], 'unmeasured')
        self.assertTrue(r['requires_live_source_check'])
        self.assertEqual(r['action'], 'recommendation_only')


class ScoringTests(unittest.TestCase):
    def setUp(self):
        self.fixtures = read('evals/outcomes.json')
        self.data = {'evidence_kind':'synthetic', 'metadata':{
            'designer_models':{'baseline':'fixture', 'candidate':'fixture'}, 'executor_model':'fixture',
            'executor_settings':{}, 'surface':'test', 'timestamp':'2026-09-28', 'trace_reference':'synthetic-only'},
            'prompts':{'baseline':'synthetic baseline', 'candidate':'synthetic candidate'}, 'trials':1,
            'runs':[{'case_id':c['id'], 'arm':a, 'trial':1, 'output':copy.deepcopy(c['expected'])}
                    for c in self.fixtures['cases'] for a in score_outputs.ARMS]}

    def call(self):
        return score_outputs.score(self.fixtures, self.data)

    def test_perfect_synthetic_is_not_effectiveness(self):
        r = self.call()
        self.assertTrue(r['complete'])
        self.assertIsNone(r['observed_delta'])
        self.assertFalse(r['general_capability_gain_proven'])
        self.assertFalse(r['provenance_verified'])

    def test_absent_row_incomplete(self):
        self.data['runs'].pop()
        self.assertFalse(self.call()['complete'])

    def test_empty_payload_never_measured(self):
        self.data['evidence_kind'] = 'reported-model-run'
        for error in (None, '', '   '):
            with self.subTest(error=error):
                self.data['runs'][0].pop('output', None)
                self.data['runs'][0]['error'] = error
                r = self.call()
                self.assertFalse(r['complete'])
                self.assertIsNone(r['observed_delta'])

    def test_explicit_error_is_recorded_failure(self):
        run = self.data['runs'][0]
        run.pop('output'); run['error'] = 'model timeout'
        r = self.call()
        self.assertTrue(r['complete'])
        self.assertFalse(r['failures'][0]['missing'])

    def test_malformed_recorded_output_not_missing(self):
        for output in ('invalid-json', None, {}, True, 1.0):
            with self.subTest(output=output):
                self.data['runs'][0]['output'] = output
                r = self.call()
                self.assertTrue(r['complete'])
                self.assertEqual(r['arms']['baseline']['passed'], len(self.fixtures['cases'])-1)

    def test_duplicate_and_unknown_rejected(self):
        self.data['runs'].append(copy.deepcopy(self.data['runs'][0]))
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            self.call()
        self.data['runs'][-1]['case_id'] = 'invalid'
        with self.assertRaisesRegex(ValueError, 'unknown'):
            self.call()

    def test_missing_prompt_or_trace_rejected(self):
        del self.data['prompts']['baseline']
        with self.assertRaises(ValueError):
            self.call()
        self.setUp()
        self.data['metadata']['trace_reference'] = ''
        with self.assertRaises(ValueError):
            self.call()

    def test_boolean_counts_are_not_integers(self):
        self.assertFalse(score_outputs.equal(True, 1))
        self.assertFalse(score_outputs.equal(2.0, 2))
        self.assertFalse(score_outputs.equal({'a':1,'b':2}, {'a':1}))

    def test_error_type_rejected(self):
        self.data['runs'][0]['error'] = True
        with self.assertRaises(ValueError):
            self.call()

    def test_reported_runs_do_not_authenticate_provenance(self):
        self.data['evidence_kind'] = 'reported-model-run'
        r = self.call()
        self.assertEqual(r['observed_delta'], 0)
        self.assertFalse(r['provenance_verified'])

    def test_duplicate_json_keys_fail(self):
        self.data['runs'][0]['output'] = '{"total":999,"total":24,"improved":3,"evidence":"confirmed"}'
        self.assertEqual(self.call()['arms']['baseline']['passed'], len(self.fixtures['cases'])-1)

    def test_nonstandard_json_rejected(self):
        for text in ('NaN', 'Infinity'):
            with self.assertRaises(ValueError):
                score_outputs.parse_output(text)

    def test_malformed_record_containers_rejected(self):
        for records in ([], {'evidence_kind':'synthetic', 'metadata':[]},
                        {**self.data, 'runs':[None]}):
            with self.subTest(records=records), self.assertRaises(ValueError):
                score_outputs.score(self.fixtures,records)

    def test_cli_empty_payload_exit_two(self):
        del self.data['runs'][0]['output']
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'records.json'
            path.write_text(json.dumps(self.data))
            p = subprocess.run([sys.executable, str(ROOT/'scripts/score_outputs.py'), str(path)], capture_output=True, text=True)
            self.assertEqual(p.returncode, 2, p.stderr)
            self.assertFalse(json.loads(p.stdout)['complete'])


class SourceTests(unittest.TestCase):
    def setUp(self):
        self.manifest = {'sources':[{'id':'one','url':'https://developers.openai.com/api/docs/models',
                                     'fetch_url':'https://developers.openai.com/api/docs/models.md'}]}

    def test_credentials_and_lookalikes_rejected(self):
        for url in ('http://developers.openai.com/a', 'https://developers.openai.com.evil.org/a',
                    'https://user:pass@developers.openai.com/a', 'https://developers.openai.com/a?token=x',
                    'https://127.0.0.1/a', 'https://developers.openai.com:22/a'):
            with self.subTest(url=url), self.assertRaises(ValueError):
                check_sources.check_url(url)

    def test_initial_baseline_needs_review(self):
        state = check_sources.observe(self.manifest, {}, lambda url:'a'*64)
        self.assertTrue(state['sources']['one']['review_required'])
        self.assertNotIn('reviewed_sha256', state['sources']['one'])

    def test_failed_fetch_keeps_success_and_review_hashes(self):
        old = {'sources':{'one':{'observed_sha256':'a'*64, 'reviewed_sha256':'b'*64}}}
        state = check_sources.observe(self.manifest, old, lambda url: (_ for _ in ()).throw(OSError('connection failed')))
        row = state['sources']['one']
        self.assertEqual(row['observed_sha256'], 'a'*64)
        self.assertEqual(row['reviewed_sha256'], 'b'*64)
        self.assertTrue(row['review_required'])
        self.assertFalse(row['ok'])

    def test_change_stays_pending_across_runs(self):
        old = {'sources':{'one':{'observed_sha256':'a'*64, 'reviewed_sha256':'a'*64}}}
        first = check_sources.observe(self.manifest, old, lambda url:'b'*64)
        second = check_sources.observe(self.manifest, first, lambda url:'b'*64)
        self.assertTrue(second['sources']['one']['review_required'])

    def test_reviewed_unchanged_source_no_signal(self):
        old = {'sources':{'one':{'observed_sha256':'a'*64, 'reviewed_sha256':'a'*64}}}
        self.assertFalse(check_sources.observe(self.manifest, old, lambda url:'a'*64)['sources']['one']['review_required'])

    def test_failure_report_not_hidden_by_zero_changes(self):
        state = check_sources.observe(self.manifest, {}, lambda url: (_ for _ in ()).throw(OSError()))
        self.assertIn('FETCH FAILED', check_sources.render_report(state, self.manifest))

    def test_unsafe_redirect_rejected_before_request(self):
        with self.assertRaises(ValueError):
            check_sources.OfficialRedirects().redirect_request(None,None,302,'',{},'https://evil.org/')


class BootstrapTests(unittest.TestCase):
    def test_two_links_and_idempotence(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)/'skills'
            bootstrap.install(ROOT, target); bootstrap.install(ROOT, target)
            self.assertEqual({p.name for p in target.iterdir()}, set(bootstrap.NAMES))
            self.assertTrue(all((target/n/'SKILL.md').is_file() for n in bootstrap.NAMES))

    def test_unrelated_path_preflight_prevents_partial_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)/'skills'; target.mkdir()
            (target/'gpt-workbench').mkdir()
            with self.assertRaises(ValueError):
                bootstrap.install(ROOT, target)
            self.assertFalse((target/'openai-guide').exists())

    def test_wrong_symlink_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)/'skills'; target.mkdir()
            link = target/'openai-guide'; link.symlink_to('/nonexistent-other-skill')
            with self.assertRaises(ValueError):
                bootstrap.install(ROOT, target)
            self.assertEqual(os.readlink(link), '/nonexistent-other-skill')

    def test_link_failure_rolls_back_new_links(self):
        original = Path.symlink_to
        def link(path, source, **kwargs):
            if path.name == 'gpt-workbench':
                raise OSError('fixture failure')
            return original(path, source, **kwargs)
        with tempfile.TemporaryDirectory() as tmp, patch.object(Path,'symlink_to',link):
            target=Path(tmp)/'skills'
            with self.assertRaises(RuntimeError):
                bootstrap.install(ROOT,target)
            self.assertFalse(list(target.iterdir()))

    def test_refresh_checks_origin_branch_and_dirt(self):
        for responses in (['https://example.org/other'], [bootstrap.REPO, 'feature'], [bootstrap.REPO,'main',' M file']):
            with self.subTest(responses=responses), patch.object(bootstrap,'git',side_effect=responses) as run:
                with self.assertRaises(ValueError):
                    bootstrap.refresh(Path('/unused'))
                self.assertFalse(any('pull' in c.args for c in run.call_args_list))

    def test_refresh_uses_ff_only(self):
        with patch.object(bootstrap,'git',side_effect=[bootstrap.REPO,'main','','']) as run:
            bootstrap.refresh(Path('/unused'))
            self.assertEqual(run.call_args.args[1:], ('pull','--ff-only','origin','main'))

    def test_actual_local_clone_and_fast_forward(self):
        # A real local git remote verifies the CLI path without credentials/network.
        with tempfile.TemporaryDirectory() as tmp:
            temp=Path(tmp); origin=temp/'origin'; origin.mkdir(); home=temp/'home'; home.mkdir()
            for name in bootstrap.NAMES:
                source=origin/bootstrap.SUBDIR/'skills'/name
                source.mkdir(parents=True)
                (source/'SKILL.md').write_text('synthetic skill')
            (origin/bootstrap.SUBDIR/'pack.json').write_text('{}')
            def git(*args):
                subprocess.run(['git','-C',str(origin),*args],check=True,capture_output=True)
            git('init','-b','main'); git('config','user.name','fixture'); git('config','user.email','fixture@example.invalid')
            git('add','.'); git('commit','-m','initial synthetic pack')
            checkout=temp/'checkout'
            with patch.object(bootstrap,'REPO',origin.as_uri()), patch.object(Path,'home',return_value=home):
                with patch.object(sys,'argv',['bootstrap.py','--checkout',str(checkout),'--clone']):
                    self.assertEqual(bootstrap.main(),0)
                (origin/'updated.txt').write_text('second revision')
                git('add','.'); git('commit','-m','updated fixture')
                bootstrap.refresh(checkout)
                self.assertEqual((checkout/'updated.txt').read_text(),'second revision')
                (checkout/'local.txt').write_text('preserve me')
                with self.assertRaisesRegex(ValueError,'local changes'):
                    bootstrap.refresh(checkout)
                self.assertEqual((checkout/'local.txt').read_text(),'preserve me')
            self.assertTrue((home/'.agents/skills/gpt-workbench/SKILL.md').is_file())


class ValidationTests(unittest.TestCase):
    def test_repository_is_valid(self):
        self.assertEqual(validate.validate(ROOT), [])

    def test_next_patch_version_without_test_edits(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/'pack'
            shutil.copytree(ROOT,target,ignore=shutil.ignore_patterns('__pycache__'))
            old=(target/'VERSION').read_text().strip()
            major,minor,patch_version=map(int,old.split('.'))
            new=f'{major}.{minor}.{patch_version+1}'
            (target/'VERSION').write_text(new+'\n')
            pack=json.loads((target/'pack.json').read_text());pack['version']=new
            (target/'pack.json').write_text(json.dumps(pack))
            p=target/'CHANGELOG.md';p.write_text(p.read_text().replace('## '+old,'## '+new,1))
            for p in (target/'skills').glob('*/SKILL.md'):
                p.write_text(p.read_text().replace('  version: '+old,'  version: '+new,1))
            self.assertEqual(validate.validate(target), [])

    def test_missing_sources_is_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/'pack'
            shutil.copytree(ROOT,target,ignore=shutil.ignore_patterns('__pycache__'))
            p=target/'skills/gpt-workbench/references/examples.md'
            p.write_text(p.read_text().replace('## Sources','## Other'))
            self.assertTrue(any('missing Sources' in e for e in validate.validate(target)))

    def test_bad_version_is_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/'pack'
            shutil.copytree(ROOT,target,ignore=shutil.ignore_patterns('__pycache__'))
            p=target/'skills/gpt-workbench/SKILL.md'
            old=(target/'VERSION').read_text().strip()
            p.write_text(p.read_text().replace('  version: '+old,'  version: 999.0.0',1))
            self.assertTrue(any('metadata.version mismatch' in e for e in validate.validate(target)))

    def test_negative_cases_exist_for_both_skills(self):
        cases=read('evals/cases.json')['cases']
        for skill in ('openai-guide','gpt-workbench'):
            self.assertGreaterEqual(sum(c['skill']==skill and not c['should_trigger'] for c in cases), 3)


if __name__ == '__main__':
    unittest.main()
