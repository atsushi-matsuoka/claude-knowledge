#!/usr/bin/env python3
"""Recommend a tier/model from declared facts. Never switches models or calls APIs."""
from __future__ import annotations
import argparse
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROLES = {0: 'efficient', 1: 'balanced', 2: 'high-capability'}


def recommend(task: dict, runtime: dict | None, catalog: dict, today: date | None = None) -> dict:
    today = today or date.today()
    if not isinstance(task, dict):
        raise ValueError('task must be an object')
    complexity = task.get('complexity', 'standard')
    if complexity not in ('simple', 'standard', 'complex'):
        raise ValueError('unknown complexity')
    risk = task.get('failure_cost', 'normal')
    if risk not in ('low', 'normal', 'high'):
        raise ValueError('unknown failure_cost')
    for key in ('semantic_precision', 'blocked_by_evidence', 'quality_failure'):
        if key in task and type(task[key]) is not bool:
            raise ValueError(f'{key} must be boolean')
    tier = {'simple': 0, 'standard': 1, 'complex': 2}[complexity]
    if risk == 'high' or task.get('semantic_precision', False):
        tier = 2
    elif task.get('quality_failure', False):
        tier = min(2, tier + 1)
    out = {'tier': tier, 'role': ROLES[tier], 'model': None, 'effort': None,
           'status': 'needs_runtime_check', 'action': 'recommendation_only',
           'switch_executed': False, 'requires_live_source_check': True,
           'effectiveness': 'unmeasured', 'reason': 'quality-first local policy, not a benchmark'}
    if task.get('blocked_by_evidence', False):
        out.update(status='repair_evidence_or_access_first', reason='a larger model cannot supply missing permissions/evidence')
        return out
    if task.get('surface') != 'api-responses':
        out.update(status='surface_specific_selection_needed', reason='API IDs are not ChatGPT/Work/Codex selector labels')
        return out
    if runtime is None:
        return out
    if not isinstance(runtime, dict) or runtime.get('surface') != task.get('surface'):
        raise ValueError('runtime surface must match the task')
    available = runtime.get('available_models')
    if not isinstance(available, list) or any(not isinstance(v, str) for v in available):
        raise ValueError('available_models must be a list of confirmed IDs')
    if runtime.get('evidence') not in ('user-confirmed', 'tool-listed') or not runtime.get('observed_on'):
        return out
    try:
        age = (today - date.fromisoformat(runtime['observed_on'])).days
    except (ValueError, TypeError):
        raise ValueError('invalid runtime observation date') from None
    if not 0 <= age <= 7:
        out['status'] = 'runtime_confirmation_stale'
        return out
    candidates = [m for m in catalog['models'] if m['id'] in available and m['surface'] == 'api-responses'
                  and m['status'] == 'candidate' and m['tier'] >= tier]
    if not candidates:
        out['status'] = 'required_tier_unavailable'
        return out
    model = min(candidates, key=lambda m: (m['tier'], m['id']))
    if not 0 <= (today - date.fromisoformat(model['evidence_as_of'])).days <= 14:
        out['status'] = 'needs_source_refresh'
        return out
    effort = {0: 'low', 1: 'medium', 2: 'high'}[tier]
    effort = task.get('requested_effort', effort)
    if effort not in model['efforts']:
        raise ValueError(f'unsupported effort for {model["id"]}: {effort}')
    out.update(model=model['id'], effort=effort, status='candidate_recommended',
               source=model['source'], runtime_evidence=runtime['evidence'])
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('task', type=Path)
    ap.add_argument('--runtime', type=Path)
    ns = ap.parse_args()
    try:
        task = json.loads(ns.task.read_text(encoding='utf-8'))
        runtime = json.loads(ns.runtime.read_text(encoding='utf-8')) if ns.runtime else None
        catalog = json.loads((ROOT/'skills/openai-guide/references/models.json').read_text(encoding='utf-8'))
        print(json.dumps(recommend(task, runtime, catalog), ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        ap.error(str(exc))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
