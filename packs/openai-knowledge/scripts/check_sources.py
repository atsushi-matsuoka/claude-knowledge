#!/usr/bin/env python3
"""Observe official-source fingerprints without rewriting knowledge or review baselines."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = Path(__file__).resolve().parents[1]
HOSTS = {'developers.openai.com', 'help.openai.com', 'academy.openai.com', 'learn.chatgpt.com', 'openai.com'}
MAX_BYTES = 2_000_000


def check_url(url: str) -> str:
    p = urlsplit(url)
    if p.scheme != 'https' or p.hostname not in HOSTS or p.username or p.password or p.port not in (None, 443) or p.query:
        raise ValueError('source must be a credential-free, query-free official HTTPS URL')
    return url


class OfficialRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        check_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url: str) -> str:
    req = Request(check_url(url), headers={'User-Agent': 'openai-knowledge-source-watch/0.1'})
    with build_opener(OfficialRedirects()).open(req, timeout=20) as response:
        check_url(response.geturl())
        body = response.read(MAX_BYTES + 1)
        if not body or len(body) > MAX_BYTES:
            raise ValueError('empty or oversized source body')
        text = body.decode('utf-8')
        if 'html' in response.headers.get('Content-Type', ''):
            text = re.sub(r'(?is)<(script|style|noscript|svg)\b.*?</\1>', ' ', text)
            text = re.sub(r'(?s)<[^>]+>', ' ', text)
        return hashlib.sha256(re.sub(r'\s+', ' ', text).strip().encode()).hexdigest()


def observe(manifest: dict, previous: dict, fetcher=fetch) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    out = {'schema_version': 1, 'observed_at': now, 'sources': {}}
    for src in manifest['sources']:
        old = previous.get('sources', {}).get(src['id'], {})
        row = {**old, 'url': src['url'], 'checked_at': now}
        # An earlier HTTP failure must not describe a later successful/non-HTTP check.
        row.pop('http_status', None)
        try:
            row['observed_sha256'] = fetcher(src['fetch_url'])
            row['ok'] = True
            row.pop('error', None)
        except (OSError, ValueError) as exc:
            row['ok'] = False
            # Keep only a numeric status, never exception URLs, headers or bodies.
            row['error'] = type(exc).__name__
            if isinstance(exc, HTTPError):
                row['http_status'] = exc.code
        row['review_required'] = (not row['ok'] or not row.get('reviewed_sha256') or
                                  row.get('observed_sha256') != row.get('reviewed_sha256'))
        out['sources'][src['id']] = row
    return out


def render_report(state: dict, manifest: dict, root: Path = ROOT) -> str:
    lines = ['# OpenAI source watch', '', f"Observed: {state['observed_at']}",
             'Fingerprint checks do not verify the meaning or accuracy of a page.', '']
    for src in manifest['sources']:
        row = state['sources'][src['id']]
        if not row['review_required']:
            continue
        documents = list((root/'skills').rglob('*.md')) + list((root/'curriculum').glob('*.json'))
        cites = [str(p.relative_to(root)) for p in documents
                 if src['url'] in p.read_text(encoding='utf-8')]
        label = 'FETCH FAILED' if not row['ok'] else 'REVIEW REQUIRED'
        detail = f" (HTTP {row['http_status']})" if not row['ok'] and 'http_status' in row else ''
        lines.append(f"- {label}{detail}: {src['id']} — {src['url']} — {', '.join(cites) or 'source ledger only'}")
    lines.extend(['', f"Fetch failures: {sum(not r['ok'] for r in state['sources'].values())}",
                  f"Review signals: {sum(r['review_required'] for r in state['sources'].values())}"])
    return '\n'.join(lines) + '\n'


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--no-network', action='store_true')
    ap.add_argument('--update', action='store_true')
    ap.add_argument('--report', type=Path)
    ns = ap.parse_args()
    manifest = json.loads((ROOT/'sources/manifest.json').read_text(encoding='utf-8'))
    for src in manifest['sources']:
        check_url(src['url']); check_url(src['fetch_url'])
    if ns.no_network:
        print(f"MANIFEST OK: {len(manifest['sources'])} official sources; network not run")
        return 0
    path = ROOT/'sources/source-status.json'
    old = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'sources': {}}
    state = observe(manifest, old)
    if ns.update:
        path.write_text(json.dumps(state, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    text = render_report(state, manifest)
    print(text)
    if ns.report:
        ns.report.write_text(text, encoding='utf-8')
    return 1 if any(not row['ok'] for row in state['sources'].values()) else 0


if __name__ == '__main__':
    raise SystemExit(main())
