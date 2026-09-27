#!/usr/bin/env python3
"""Check learning provenance records, not whether a person/AI really learned.

The generated map never substitutes for an authenticated course export or model
experiment. No network requests, credentials, model invocation or side effects
except --render writing the map.
"""
from __future__ import annotations
import argparse
import json
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo
from check_sources import check_url

ROOT = Path(__file__).resolve().parents[1]
READ = {'text-sections', 'transcript-sections', 'pdf-sections'}
COVERAGE = READ | {'shell-only', 'index-outline', 'outline-only', 'attachment-unavailable'}


def safe_file(root: Path, rel: str) -> bool:
    return (isinstance(rel, str) and not Path(rel).is_absolute()
            and (root/rel).resolve().is_relative_to(root.resolve())
            and (root/rel).is_file())


def audit(data: dict, root: Path = ROOT, today: date | None = None) -> list[str]:
    today = today or datetime.now(ZoneInfo('Asia/Tokyo')).date()
    errors = []
    try:
        if data['schema_version'] != 1:
            errors.append('unsupported curriculum schema')
        survey = date.fromisoformat(data['surveyed_on'])
        if survey > today:
            errors.append('survey date is in the future')
        scope = data['scope']
        if type(scope.get('complete')) is not bool or not scope.get('definition') or not scope.get('limitations'):
            errors.append('explicit curriculum scope and limitations required')
        if scope.get('complete') and not scope.get('completeness_evidence'):
            errors.append('complete catalogue claim requires completeness_evidence')
        for route in data['discovery']:
            check_url(route['url'])
            if not route.get('observed'):
                errors.append('discovery observation required')
        rows = data['resources']
        ids = [r['id'] for r in rows]
        if len(ids) != len(set(ids)):
            errors.append('duplicate resource id')
        indexed = {r['id']: r for r in rows}
        for r in rows:
            rid = r['id']
            check_url(r['url'])
            if 'alternate_url' in r:
                check_url(r['alternate_url'])
            if r['kind'] not in ('academy', 'developer') or r['priority'] not in ('core', 'supplement', 'conditional'):
                errors.append(f'{rid}: invalid kind/priority')
            if r['coverage'] not in COVERAGE:
                errors.append(f'{rid}: invalid coverage')
            if any(not isinstance(r.get(k), str) or not r[k].strip() for k in ('title','reason','gap','next_action')):
                errors.append(f'{rid}: rationale, gap and revisit action required')
            if not isinstance(r.get('locators'), list) or any(not isinstance(x,str) or not x.strip() for x in r['locators']):
                errors.append(f'{rid}: locators must be a string list')
            elif r['coverage'] in READ and not r['locators']:
                errors.append(f'{rid}: read sections need locators')
            if date.fromisoformat(r['checked_on']) > survey:
                errors.append(f'{rid}: check date exceeds survey date')
            if type(r.get('course_completed')) is not bool:
                errors.append(f'{rid}: completion must be boolean')
            elif r['course_completed'] and (r['coverage'] not in READ or not r.get('completion_evidence')):
                errors.append(f'{rid}: completion claim lacks lesson evidence')
            for status, default, claimed, evidence in (
                ('exercise_status', 'not-run', 'executed', 'exercise_evidence'),
                ('model_effect', 'unmeasured', 'measured', 'measurement_evidence')):
                if r.get(status) not in (default, claimed):
                    errors.append(f'{rid}: invalid {status}')
                elif r[status] == claimed and not r.get(evidence):
                    errors.append(f'{rid}: {status} claim needs separate evidence')
            if 'attachment_url' in r:
                u = urlsplit(r['attachment_url'])
                if (u.scheme != 'https' or u.hostname != 'd2xo500swnpgl1.cloudfront.net'
                    or not u.path.startswith('/uploads/oaiacademy/') or not u.path.endswith('.pdf')
                    or u.username or u.password or u.query or u.port not in (None,443)
                    or r['kind'] != 'academy' or urlsplit(r['url']).hostname != 'academy.openai.com'):
                    errors.append(f'{rid}: attachment must retain its public Academy wrapper and exact PDF URL')
                if type(r.get('attachment_pages')) is not int or r['attachment_pages'] < 1:
                    errors.append(f'{rid}: attachment page count required')
        cases = json.loads((root/'evals/cases.json').read_text(encoding='utf-8'))['cases']
        case_ids = {c['id'] for c in cases}
        units = data['learning_units']
        if len({u['id'] for u in units}) != len(units):
            errors.append('duplicate learning-unit id')
        for u in units:
            uid = u['id']
            if not u.get('scope') or not u.get('example_section') or not u.get('basis') or not u.get('probes'):
                errors.append(f'{uid}: incomplete source-to-procedure-to-probe mapping')
            for src in u['basis']:
                if src not in indexed or indexed[src]['coverage'] not in READ:
                    errors.append(f'{uid}: operationalized basis must be actually read sections: {src}')
            if not safe_file(root,u['procedure']):
                errors.append(f'{uid}: missing/unsafe procedure')
            elif '## '+u['example_section'] not in (root/u['procedure']).read_text(encoding='utf-8'):
                errors.append(f'{uid}: missing original-example section')
            if not set(u['probes']).issubset(case_ids):
                errors.append(f'{uid}: unknown development probe')
            for key, initial, evidence in (
                ('academy_exercise_status','not-run','academy_exercise_evidence'),
                ('real_model_status','unmeasured','real_model_evidence')):
                if u.get(key) != initial and not u.get(evidence):
                    errors.append(f'{uid}: unsupported exercise/effect claim')
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        errors.append('malformed curriculum: '+str(exc))
    return errors


def render(data: dict) -> str:
    academy = [r for r in data['resources'] if r['kind']=='academy']
    counts = Counter(r['coverage'] for r in academy)
    lines = ['# Academy coverage and action map', '',
             '<!-- Generated from academy-inventory.json by scripts/audit_curriculum.py --render. -->', '',
             'Surveyed: '+data['surveyed_on'], '',
             f"Survey set: {len(academy)} Academy entries (courses/groups, series/sessions and resources; not {len(academy)} completed courses), "
             f"{len(data['resources'])-len(academy)} developer supplements, {len(data['learning_units'])} action mappings.", '',
             '**Global catalogue completeness: not established. Course completion, Academy exercises and real-model effects are not established by this audit.**', '',
             '## Coverage of the surveyed Academy entries', '']
    lines += [f'- {key}: {n}' for key,n in sorted(counts.items())]
    lines += ['', '## Scope limitations', ''] + ['- '+x for x in data['scope']['limitations']]
    lines += ['', '## Audience priorities', ''] + [f"- {x['name']} ({x['priority']}): {x['reason']}" for x in data['audiences']]
    lines += ['', '## Inventory', '', '| ID | Resource | Priority | Actual access |', '|---|---|---|---|']
    lines += [f"| {r['id']} | [{r['title']}]({r['url']}) | {r['priority']} | {r['coverage']} |" for r in data['resources']]
    lines += ['', 'Exact read sections/pages, attachment identity, rationale and next action live in the JSON record. A PDF-section row includes only the listed pages, not the whole deck.', '', '## Learning to action', '']
    lines += [f"- {u['title']}: `{u['procedure']}`; development probes: "+', '.join('`'+p+'`' for p in u['probes'])+'.' for u in data['learning_units']]
    lines += ['', '## Unresolved conflicts', '']
    lines += [f"- {c['finding']} {c['resolution']}" for c in data['conflicts']]
    lines += ['', '## Next learning pass', '',
              'Prioritize accessible lesson bodies for Agents and Workflows, API agents/retrieval/evaluation/production, and missing Skill Lab attachments. Reconcile the newer catalogue and Codex series. Leadership, teaching and voice are conditional, not declared unnecessary. Developer supplements do not discharge missing Academy lessons.', '',
              'Rediscover public catalogue/community/series routes during the first weekly maintenance pass of each month. Retry important access gaps when a new public body or authorized note is available. Do not load this inventory for ordinary task execution.', '']
    return '\n'.join(lines)


def validate(root: Path = ROOT) -> list[str]:
    try:
        data = json.loads((root/'curriculum/academy-inventory.json').read_text(encoding='utf-8'))
        errors = audit(data,root)
        if not errors and (root/'curriculum/academy-map.md').read_text(encoding='utf-8') != render(data):
            errors.append('generated academy-map.md is stale; run audit_curriculum.py --render')
        return errors
    except (OSError, ValueError) as exc:
        return ['curriculum unreadable: '+str(exc)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render',action='store_true')
    args = parser.parse_args()
    data = json.loads((ROOT/'curriculum/academy-inventory.json').read_text(encoding='utf-8'))
    errors = audit(data)
    if not errors and args.render:
        (ROOT/'curriculum/academy-map.md').write_text(render(data),encoding='utf-8')
    if not errors:
        errors = validate()
    print('\n'.join(errors) if errors else 'CURRICULUM VALID: records/mappings only; course completion and model effects not established')
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
