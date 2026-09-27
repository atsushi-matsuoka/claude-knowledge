"""Offline failure-report regressions; no network or model calls."""
import json
import sys
import unittest
from pathlib import Path
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import check_sources


class SourceDiagnosticTests(unittest.TestCase):
    def setUp(self):
        self.manifest = {'sources': [{'id': 'help', 'url': 'https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex',
                                     'fetch_url': 'https://help.openai.com/en/articles/20001275'}]}
        self.old = {'sources': {'help': {'observed_sha256': 'a' * 64, 'reviewed_sha256': 'b' * 64}}}

    @staticmethod
    def blocked(url):
        raise HTTPError(url + '?private-marker=do-not-log', 403, 'sensitive-body', {'sensitive-header': 'private'}, None)

    def test_http_status_without_exception_details(self):
        row = check_sources.observe(self.manifest, self.old, self.blocked)['sources']['help']
        self.assertEqual(row['http_status'], 403)
        self.assertFalse(row['ok'])
        self.assertTrue(row['review_required'])
        self.assertEqual(row['observed_sha256'], 'a' * 64)
        self.assertEqual(row['reviewed_sha256'], 'b' * 64)
        self.assertNotIn('private-marker', json.dumps(row))
        self.assertNotIn('sensitive', json.dumps(row))

    def test_report_shows_status_not_exception(self):
        state = check_sources.observe(self.manifest, self.old, self.blocked)
        report = check_sources.render_report(state, self.manifest)
        self.assertIn('FETCH FAILED (HTTP 403)', report)
        self.assertIn('Fetch failures: 1', report)
        self.assertNotIn('sensitive', report)
        self.assertNotIn('private-marker', report)

    def test_recovery_clears_obsolete_error_and_status(self):
        failed = check_sources.observe(self.manifest, self.old, self.blocked)
        row = check_sources.observe(self.manifest, failed, lambda url: 'c' * 64)['sources']['help']
        self.assertTrue(row['ok'])
        self.assertNotIn('http_status', row)
        self.assertNotIn('error', row)
        self.assertEqual(row['reviewed_sha256'], 'b' * 64)

    def test_non_http_failure_does_not_reuse_http_status(self):
        failed = check_sources.observe(self.manifest, self.old, self.blocked)
        def timeout(url):
            raise TimeoutError('do-not-publish')
        row = check_sources.observe(self.manifest, failed, timeout)['sources']['help']
        self.assertFalse(row['ok'])
        self.assertNotIn('http_status', row)
        self.assertEqual(row['error'], 'TimeoutError')
        self.assertEqual(row['observed_sha256'], 'a' * 64)


if __name__ == '__main__':
    unittest.main()
