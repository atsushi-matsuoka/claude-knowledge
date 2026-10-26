"""Keep validation triggers bounded without disabling meaningful checks."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CIValidationPolicyTests(unittest.TestCase):
    def test_only_main_pushes_and_all_pull_requests_trigger_validation(self):
        workflow = (ROOT / '.github/workflows/validate.yml').read_text()
        trigger = re.search(r'^on:\n(.*?)(?=^\S)', workflow, re.M | re.S).group(1)
        trigger = '\n'.join(line for line in trigger.splitlines() if line.strip() and not line.lstrip().startswith('#'))
        self.assertEqual(trigger, '  push:\n    branches: [main]\n  pull_request:')
        self.assertIn('  group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}', workflow)
        self.assertIn('  cancel-in-progress: true', workflow)
        self.assertNotIn('continue-on-error', workflow)
        self.assertIn('python -m unittest discover -s tests', workflow)
        self.assertIn('python scripts/check_sources.py --no-network', workflow)
        self.assertIn('contents: read', workflow)

    def test_atomic_commit_guidance_is_present(self):
        instructions = (ROOT / 'AGENTS.md').read_text()
        self.assertIn('single tree/commit', instructions)
        self.assertIn('one coherent commit', instructions)
        self.assertIn('Do not use `[skip ci]`', instructions)


if __name__ == '__main__': unittest.main()
