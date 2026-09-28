#!/usr/bin/env python3
"""Validate this standalone pack using only the standard library; never invoke models."""
from __future__ import annotations
import json
import re
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from check_sources import check_url
import audit_curriculum

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {'name', 'description', 'metadata', 'license', 'compatibility', 'allowed-tools'}
LINKS = re.compile(r'\]\(([^)#\s]+)(?:#[^)]*)?\)')


def validate(root: Path = ROOT) -> list[str]:
    errors = []
    try:
        version = (root/'VERSION').read_text(encoding='utf-8').strip()
        pack = json.loads((root/'pack.json').read_text(encoding='utf-8'))
        if not re.fullmatch(r'\d+\.\d+\.\d+', version) or pack['version'] != version:
            errors.append('invalid/inconsistent pack version')
        changelog = (root/'CHANGELOG.md').read_text(encoding='utf-8')
        top = re.search(r'^## (\d+\.\d+\.\d+)', changelog, re.M)
        if not top or top.group(1) != version:
            errors.append('CHANGELOG version mismatch')
        found = {p.parent.name for p in (root/'skills').glob('*/SKILL.md')}
        if set(pack['skills']) != found or len(found) != len(pack['skills']):
            errors.append('skill inventory mismatch')
        today = datetime.now(ZoneInfo('Asia/Tokyo')).date()
        for name in pack['skills']:
            skill = root/'skills'/name
            text = (skill/'SKILL.md').read_text(encoding='utf-8')
            parts = text.split('---\n', 2)
            if len(parts) != 3 or parts[0]:
                errors.append(f'{name}: malformed frontmatter')
                continue
            fields = dict(re.findall(r'^([a-z-]+):[ \t]*(.*)$', parts[1], re.M))
            if set(fields) - ALLOWED or fields.get('name') != name or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
                errors.append(f'{name}: invalid skill fields/name')
            if not 1 <= len(fields.get('description', '')) <= 700 or len(text.splitlines()) > 150:
                errors.append(f'{name}: context budget exceeded')
            v = re.search(r'^  version: (\S+)$', parts[1], re.M)
            if not v or v.group(1) != version:
                errors.append(f'{name}: metadata.version mismatch')
            linked = set()
            for target in LINKS.findall(parts[2]):
                if target.startswith('https://'):
                    check_url(target)
                    continue
                p = (skill/target).resolve()
                if not p.is_relative_to(skill.resolve()) or not p.is_file():
                    errors.append(f'{name}: missing/unsafe reference {target}')
                linked.add(p)
            for ref in (skill/'references').glob('*.md'):
                content = ref.read_text(encoding='utf-8')
                if ref.resolve() not in linked:
                    errors.append(f'{name}: orphan reference {ref.name}')
                verified = re.search(r'^Last verified: (\d{4}-\d{2}-\d{2})$', content, re.M)
                if not verified or date.fromisoformat(verified.group(1)) > today:
                    errors.append(f'{name}: invalid verification date in {ref.name}')
                if '\n## Sources\n' not in content:
                    errors.append(f'{name}: missing Sources in {ref.name}')
                for target in LINKS.findall(content):
                    if not target.startswith('https://'):
                        errors.append(f'{name}: reference links must stay one level deep')
        manifest = json.loads((root/'sources/manifest.json').read_text(encoding='utf-8'))
        ids = [s['id'] for s in manifest['sources']]
        if len(ids) != len(set(ids)):
            errors.append('duplicate source IDs')
        for source in manifest['sources']:
            check_url(source['url']); check_url(source['fetch_url'])
            if source['coverage'] not in ('text-sections-read', 'index-extract', 'outline-only'):
                errors.append('unclassified retrieval coverage')
        catalog = json.loads((root/'skills/openai-guide/references/models.json').read_text(encoding='utf-8'))
        model_ids = [m['id'] for m in catalog['models']]
        if len(model_ids) != len(set(model_ids)):
            errors.append('duplicate model IDs')
        for m in catalog['models']:
            check_url(m['source'])
            if m['account_access'] != 'unknown' or m['effectiveness'] != 'unmeasured':
                errors.append('initial catalogue must not claim access or measured quality')
            if type(m['tier']) is not int or m['tier'] not in (0, 1, 2) or not m['efforts']:
                errors.append('invalid model tier/efforts')
        cases = json.loads((root/'evals/cases.json').read_text(encoding='utf-8'))['cases']
        if len(cases) < 24 or len({c['id'] for c in cases}) != len(cases):
            errors.append('insufficient/duplicate evaluation cases')
        for c in cases:
            if c['skill'] not in found or type(c['should_trigger']) is not bool or not c['expect']:
                errors.append('invalid case target/contract')
            if c['split'] != 'development':
                errors.append('initial cases are not independent holdouts')
        for name in found:
            own = [c for c in cases if c['skill'] == name]
            if len(own) < 8 or sum(not c['should_trigger'] for c in own) < 3:
                errors.append(f'{name}: missing positive/negative coverage')
        for p in root.rglob('*'):
            if not p.is_file() or '__pycache__' in p.parts or '.local' in p.parts or p.suffix not in ('.md', '.py', '.json', '.yaml', '.yml'):
                continue
            text = p.read_text(encoding='utf-8')
            if re.search(r'(?:sk-ant-|sk-proj-)[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{30,}', text):
                errors.append('possible secret: '+str(p.relative_to(root)))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append('malformed pack: '+str(exc))
    errors.extend(audit_curriculum.validate(root))
    return errors


if __name__ == '__main__':
    failures = validate()
    print('\n'.join(failures) if failures else 'PACK VALID: structure, versions, sources, model candidates and eval contracts')
    raise SystemExit(bool(failures))
