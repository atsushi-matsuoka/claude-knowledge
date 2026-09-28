#!/usr/bin/env python3
"""Score supplied synthetic or reported model outputs; no API calls or provenance claims."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARMS = ('baseline', 'candidate')


def equal(a, b) -> bool:
    if type(a) is not type(b):
        return False
    if isinstance(b, dict):
        return a.keys() == b.keys() and all(equal(a[k], v) for k, v in b.items())
    if isinstance(b, list):
        return len(a) == len(b) and all(equal(x, y) for x, y in zip(a, b))
    return a == b


def parse_output(text: str):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('duplicate JSON key')
            result[key] = value
        return result
    def no_constants(value):
        raise ValueError('nonstandard JSON constant')
    return json.loads(text, object_pairs_hook=unique, parse_constant=no_constants)


def score(fixtures: dict, data: dict) -> dict:
    if not isinstance(data, dict) or not isinstance(fixtures, dict):
        raise ValueError('records and fixtures must be objects')
    if data.get('evidence_kind') not in ('synthetic', 'reported-model-run'):
        raise ValueError('evidence_kind must be synthetic or reported-model-run')
    meta = data.get('metadata', {})
    if not isinstance(meta, dict) or not isinstance(data.get('prompts'), dict) or not isinstance(data.get('runs', []), list):
        raise ValueError('invalid metadata, prompts or runs container')
    for key in ('designer_models', 'executor_model', 'executor_settings', 'surface', 'timestamp', 'trace_reference'):
        if key not in meta or meta[key] is None:
            raise ValueError(f'missing metadata: {key}')
    for key in ('executor_model', 'surface', 'timestamp', 'trace_reference'):
        if not isinstance(meta[key], str) or not meta[key].strip():
            raise ValueError(f'nonempty metadata required: {key}')
    if not isinstance(meta['executor_settings'], dict) or not isinstance(meta['designer_models'], dict):
        raise ValueError('model settings and designer_models must be objects')
    for arm in ARMS:
        if not isinstance(meta['designer_models'].get(arm), str) or not meta['designer_models'][arm].strip():
            raise ValueError('both designer model IDs required')
        if not isinstance(data.get('prompts', {}).get(arm), str) or not data['prompts'][arm].strip():
            raise ValueError('both actual designed prompts required')
    trials = data.get('trials')
    if type(trials) is not int or trials < 1:
        raise ValueError('positive integer trials required')
    cases = {c['id']: c for c in fixtures['cases']}
    if not cases or len(cases) != len(fixtures['cases']):
        raise ValueError('nonempty unique fixture IDs required')
    indexed = {}
    for run in data.get('runs', []):
        if not isinstance(run, dict):
            raise ValueError('each run must be an object')
        key = (run.get('case_id'), run.get('arm'), run.get('trial'))
        if key[0] not in cases or key[1] not in ARMS or type(key[2]) is not int or not 1 <= key[2] <= trials:
            raise ValueError('unknown attempt')
        if key in indexed:
            raise ValueError('duplicate attempt')
        error = run.get('error')
        if error is not None and not isinstance(error, str):
            raise ValueError('error must be a string or null')
        indexed[key] = run
    result = {'evidence_kind': data['evidence_kind'], 'arms': {}, 'failures': [],
              'provenance_verified': False, 'general_capability_gain_proven': False}
    for arm in ARMS:
        passed = missing = 0
        for cid, c in cases.items():
            for trial in range(1, trials + 1):
                run = indexed.get((cid, arm, trial))
                has_error = bool(run and isinstance(run.get('error'), str) and run['error'].strip())
                absent = run is None or ('output' not in run and not has_error)
                missing += absent
                ok = False
                if not absent and not has_error:
                    try:
                        value = run['output']
                        value = parse_output(value) if isinstance(value, str) else value
                        ok = equal(value, c['expected'])
                    except (ValueError, TypeError):
                        pass
                passed += ok
                if not ok:
                    result['failures'].append({'case_id': cid, 'arm': arm, 'trial': trial, 'missing': absent})
        total = len(cases) * trials
        result['arms'][arm] = {'passed': passed, 'total': total, 'missing': missing, 'rate': passed/total}
    result['complete'] = all(a['missing'] == 0 for a in result['arms'].values())
    result['observed_delta'] = (result['arms']['candidate']['rate'] - result['arms']['baseline']['rate']
                                if result['complete'] and data['evidence_kind'] == 'reported-model-run' else None)
    result['limitation'] = 'Arithmetic on supplied records only; independently check traces, matched conditions and hidden test exposure.'
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('records', type=Path)
    ns = ap.parse_args()
    try:
        report = score(json.loads((ROOT/'evals/outcomes.json').read_text(encoding='utf-8')),
                       json.loads(ns.records.read_text(encoding='utf-8')))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        ap.error(str(exc))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['complete'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
