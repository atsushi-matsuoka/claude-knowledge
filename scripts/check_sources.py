#!/usr/bin/env python3
"""Check canonical source URLs and record lightweight fingerprints.

A changed fingerprint is a review signal, not permission to rewrite knowledge.
Uses only Python standard library.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT/"sources"/"manifest.json"
STATUS = ROOT/"sources"/"source-status.json"


SKILL_DIR = ROOT/"skills"


def norm(data: bytes, content_type: str = "") -> bytes:
    """Reduce obvious noise without pretending this is semantic diffing."""
    text = data.decode("utf-8", errors="replace")
    if "html" in content_type:
        text = re.sub(r"(?is)<(script|style|noscript|svg)\b.*?</\1>", " ", text)
        text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text.encode("utf-8")


def citing_files(url: str) -> list[str]:
    """Knowledge files that cite this source URL - the places to review first."""
    hits = []
    for f in sorted(SKILL_DIR.rglob("*.md")):
        if url in f.read_text(encoding="utf-8"):
            hits.append(f.relative_to(ROOT).as_posix())
    return hits


def fetch(url: str) -> dict:
    req = Request(url, headers={"User-Agent":"claude-knowledge-source-watch/0.2"})
    with urlopen(req, timeout=30) as r:
        body = r.read(2_000_000)
        ctype = r.headers.get("Content-Type", "")
        return {
            "ok": True,
            "status": getattr(r, "status", 200),
            "final_url": r.geturl(),
            "etag": r.headers.get("ETag"),
            "last_modified": r.headers.get("Last-Modified"),
            "sha256": hashlib.sha256(norm(body, ctype)).hexdigest(),
        }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--update", action="store_true")
    ap.add_argument("--report", type=Path)
    ap.add_argument("--no-network", action="store_true")
    ns = ap.parse_args()
    manifest = json.loads(MANIFEST.read_text())
    previous = json.loads(STATUS.read_text()) if STATUS.exists() else {"sources":{}}
    out = {"generated_at": datetime.now(timezone.utc).isoformat(), "sources": {}}
    changed=[]; failed=[]

    if ns.no_network:
        print(f"Manifest OK: {len(manifest['sources'])} registered sources. Network check skipped.")
        return 0

    for src in manifest["sources"]:
        sid=src["id"]
        try:
            row=fetch(src.get("fetch_url", src["url"]))
        except (URLError, HTTPError, TimeoutError, OSError) as e:
            row={"ok":False,"error":str(e)}; failed.append(sid)
        row["checked_at"]=out["generated_at"]
        row["url"]=src["url"]
        out["sources"][sid]=row
        old=previous.get("sources",{}).get(sid,{})
        if row.get("ok") and old.get("sha256") and row.get("sha256") != old.get("sha256"):
            changed.append(sid)

    if ns.update:
        STATUS.write_text(json.dumps(out, indent=2, ensure_ascii=False)+"\n")

    lines=["# Source watch report", "", f"Checked: {out['generated_at']}", ""]
    lines += [f"Changed fingerprints: {len(changed)}", f"Failed checks: {len(failed)}", ""]
    if changed:
        lines += ["## Review required", ""]
        by_id = {s["id"]: s for s in manifest["sources"]}
        for x in changed:
            cites = citing_files(by_id[x]["url"])
            where = ", ".join(f"`{c}`" for c in cites) if cites else "no reference cites it yet"
            lines.append(f"- {x} ({by_id[x]['url']}) - review: {where}")
        lines.append("")
    if failed:
        lines += ["## Fetch failures"]+[f"- {x}" for x in failed]+[""]
    lines += ["A fingerprint change is a review signal, not proof that product behavior changed."]
    report="\n".join(lines)+"\n"
    print(report)
    if ns.report:
        ns.report.write_text(report)
    return 0 if not failed else 1

if __name__ == "__main__":
    raise SystemExit(main())
