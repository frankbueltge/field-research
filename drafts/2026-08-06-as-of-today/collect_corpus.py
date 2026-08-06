#!/usr/bin/env python3
"""collect_corpus.py — build the corpus under C-RULE-1..4 of PREREGISTRATION.md.

Fetches the seed page once, extracts every same-host link whose path begins /en/, in
document order, normalises (drop query and fragment, drop trailing slash), deduplicates
keeping first appearance, drops the seed itself, and caps at 40.

Writes corpus.json. Collects no date signals — that is collect_signals.py, and the
corpus is committed before it runs so the selection cannot be tuned to the result.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
import sys
from urllib.parse import urljoin, urlsplit, urlunsplit

SEED = "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai"
HOST = "digital-strategy.ec.europa.eu"
CAP = 40
UA = "Mozilla/5.0 (compatible; field-research/1.0; public-interest measurement)"

HREF_RE = re.compile(r'<a\b[^>]*?\bhref\s*=\s*(?:"([^"]*)"|\'([^\']*)\')', re.I | re.S)


def fetch(url: str, timeout: int = 60) -> tuple[int, str]:
    """One GET via curl. Returns (status, body). Body is '' on failure."""
    out = subprocess.run(
        ["curl", "-sS", "-L", "-A", UA, "--max-time", str(timeout), "-w", "\n%{http_code}", url],
        capture_output=True, text=True,
    )
    if out.returncode != 0:
        return 0, ""
    body, _, code = out.stdout.rpartition("\n")
    try:
        return int(code), body
    except ValueError:
        return 0, ""


def normalise(url: str) -> str:
    """Drop query and fragment; drop a trailing slash on non-root paths. C-RULE-2."""
    s = urlsplit(url)
    path = s.path.rstrip("/") or "/"
    return urlunsplit((s.scheme, s.netloc, path, "", ""))


def main() -> int:
    started = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    status, html = fetch(SEED)
    if status != 200 or not html:
        print(f"seed fetch failed: status={status}", file=sys.stderr)
        return 1

    seed_norm = normalise(SEED)
    seen: set[str] = set()
    ordered: list[str] = []
    raw_hits = 0

    for m in HREF_RE.finditer(html):
        href = (m.group(1) or m.group(2) or "").strip()
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        absolute = urljoin(SEED, href)
        s = urlsplit(absolute)
        if s.scheme not in ("http", "https") or s.netloc != HOST:
            continue
        if not s.path.startswith("/en/"):
            continue
        raw_hits += 1
        norm = normalise(absolute)
        if norm == seed_norm or norm in seen:
            continue
        seen.add(norm)
        ordered.append(norm)

    corpus = ordered[:CAP]
    payload = {
        "instrument": "as-of-today",
        "preregistration": "PREREGISTRATION.md",
        "rule": "C-RULE-1..4",
        "seed": SEED,
        "seed_fetched_utc": started,
        "seed_status": status,
        "seed_bytes": len(html),
        "same_host_en_links_found": raw_hits,
        "distinct_after_normalisation": len(ordered),
        "cap": CAP,
        "corpus_size": len(corpus),
        "too_small_threshold": 15,
        "corpus": corpus,
    }
    with open("corpus.json", "w") as fh:
        json.dump(payload, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(f"seed {status}, {raw_hits} same-host /en/ links, {len(ordered)} distinct, corpus {len(corpus)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
