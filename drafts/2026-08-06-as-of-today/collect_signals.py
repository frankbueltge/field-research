#!/usr/bin/env python3
"""collect_signals.py — collect the three currency signals H, S, V under M-1..M-5.

Reads corpus.json (committed before this script ran). Writes signals.json.

H — HTTP Last-Modified on a plain GET of the URL                       (M-1)
S — <lastmod> for that URL in the site's own XML sitemap               (M-2)
V — a visible date in the page, by the pre-declared pattern set only   (M-3)

IMPLEMENTATION NOTE, decided after the pre-registration and before any result was seen:
M-2 says "the sitemap(s) under .../sitemap.xml, following sitemap-index entries if
present, one level". This site serves a plain <urlset>, not an index, and paginates with
?page=N. Those pages are the sitemaps under that URL, so they are followed the same way
an index would be: page 1, 2, 3 … until a page yields no <url>, capped at 40 pages. The
count of pages actually read is recorded in the output.
"""

from __future__ import annotations

import datetime as dt
import html as htmllib
import json
import re
import subprocess
import time
from urllib.parse import urlsplit, urlunsplit

SITEMAP = "https://digital-strategy.ec.europa.eu/sitemap.xml"
UA = "Mozilla/5.0 (compatible; field-research/1.0; public-interest measurement)"
PAUSE = 0.7
MAX_SITEMAP_PAGES = 40

MONTHS = ("January|February|March|April|May|June|July|August|September|October|November|December")
DATE_PAT = rf"(\d{{1,2}}\s+(?:{MONTHS})\s+\d{{4}}|\d{{4}}-\d{{2}}-\d{{2}}|\d{{2}}/\d{{2}}/\d{{4}})"
V1_RE = re.compile(rf"Last\s+update[d]?\s*[:\-]?\s*(.{{0,40}})", re.I | re.S)
V2_RE = re.compile(rf"(?:Publication\s+date|Published)\s*[:\-]?\s*(.{{0,40}})", re.I | re.S)
DATE_RE = re.compile(DATE_PAT, re.I)
TIME_RE = re.compile(r"<time[^>]*\bdatetime\s*=\s*[\"']([^\"']+)[\"']", re.I)
URL_RE = re.compile(r"<url>(.*?)</url>", re.S | re.I)
LOC_RE = re.compile(r"<loc>\s*([^<]+?)\s*</loc>", re.I)
LASTMOD_RE = re.compile(r"<lastmod>\s*([^<]+?)\s*</lastmod>", re.I)


def normalise(url: str) -> str:
    s = urlsplit(url)
    path = s.path.rstrip("/") or "/"
    # sitemap entries on this site are emitted as http://; compare on host+path only
    return urlunsplit(("https", s.netloc, path, "", ""))


def get(url: str, timeout: int = 60) -> dict:
    """One GET. Returns status, headers (lowercased keys), body."""
    proc = subprocess.run(
        ["curl", "-sS", "-L", "-A", UA, "--max-time", str(timeout), "-D", "-", url],
        capture_output=True, text=True, errors="replace",
    )
    if proc.returncode != 0:
        return {"ok": False, "error": f"curl exit {proc.returncode}: {proc.stderr.strip()[:200]}"}
    raw = proc.stdout
    # with -L there may be several header blocks; keep the last
    parts = re.split(r"\r?\n\r?\n", raw)
    head_idx = 0
    for i, p in enumerate(parts):
        if re.match(r"HTTP/\d", p.strip()):
            head_idx = i
    head = parts[head_idx]
    body = "\n\n".join(parts[head_idx + 1:])
    status = 0
    m = re.match(r"HTTP/[\d.]+\s+(\d{3})", head.strip())
    if m:
        status = int(m.group(1))
    headers = {}
    for line in head.splitlines()[1:]:
        if ":" in line:
            k, _, v = line.partition(":")
            headers[k.strip().lower()] = v.strip()
    return {"ok": True, "status": status, "headers": headers, "body": body}


def parse_http_date(value: str | None) -> str | None:
    if not value:
        return None
    for fmt in ("%a, %d %b %Y %H:%M:%S %Z", "%a, %d %b %Y %H:%M:%S %z"):
        try:
            d = dt.datetime.strptime(value, fmt)
            if d.tzinfo is None:
                d = d.replace(tzinfo=dt.timezone.utc)
            return d.astimezone(dt.timezone.utc).isoformat()
        except ValueError:
            continue
    return None


def parse_iso(value: str | None) -> str | None:
    if not value:
        return None
    v = value.strip().replace("Z", "+00:00")
    try:
        d = dt.datetime.fromisoformat(v)
    except ValueError:
        try:
            d = dt.datetime.strptime(v[:10], "%Y-%m-%d")
        except ValueError:
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=dt.timezone.utc)
    return d.astimezone(dt.timezone.utc).isoformat()


def visible_text(page: str) -> str:
    t = re.sub(r"<(script|style)\b.*?</\1>", " ", page, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = htmllib.unescape(t)
    return re.sub(r"\s+", " ", t)


def extract_v(page: str) -> dict:
    """M-3, in order, first match wins. The pattern set is fixed by the pre-registration."""
    text = visible_text(page)
    for rule, rx in (("V1-last-update", V1_RE), ("V2-published", V2_RE)):
        for m in rx.finditer(text):
            d = DATE_RE.search(m.group(1))
            if d:
                return {"v_raw": d.group(1), "v_rule": rule, "v_context": m.group(0)[:90]}
    m = TIME_RE.search(page)
    if m:
        return {"v_raw": m.group(1), "v_rule": "V3-time-element", "v_context": None}
    return {"v_raw": None, "v_rule": None, "v_context": None}


def normalise_v(raw: str | None) -> str | None:
    if not raw:
        return None
    iso = parse_iso(raw)
    if iso:
        return iso
    for fmt in ("%d %B %Y", "%d/%m/%Y"):
        try:
            return dt.datetime.strptime(raw.strip(), fmt).replace(tzinfo=dt.timezone.utc).isoformat()
        except ValueError:
            continue
    return None


def fetch_sitemap() -> tuple[dict[str, str], list[dict]]:
    """M-2. Returns (normalised url -> lastmod iso, per-page log)."""
    index: dict[str, str] = {}
    log = []
    for page in range(1, MAX_SITEMAP_PAGES + 1):
        url = SITEMAP if page == 1 else f"{SITEMAP}?page={page}"
        r = get(url, timeout=90)
        if not r.get("ok") or r.get("status") != 200:
            log.append({"page": page, "status": r.get("status", 0), "urls": 0, "stop": "fetch-failed"})
            break
        blocks = URL_RE.findall(r["body"])
        for b in blocks:
            loc = LOC_RE.search(b)
            lm = LASTMOD_RE.search(b)
            if not loc:
                continue
            key = normalise(loc.group(1))
            if lm:
                iso = parse_iso(lm.group(1))
                if iso and key not in index:
                    index[key] = iso
        log.append({"page": page, "status": 200, "urls": len(blocks), "bytes": len(r["body"])})
        if not blocks:
            break
        time.sleep(PAUSE)
    return index, log


def main() -> int:
    corpus = json.load(open("corpus.json"))
    run_started = dt.datetime.now(dt.timezone.utc)

    sitemap_index, sitemap_log = fetch_sitemap()

    rows = []
    for url in corpus["corpus"]:
        r = get(url)
        time.sleep(PAUSE)
        if not r.get("ok") or r.get("status", 0) != 200:
            rows.append({
                "url": url, "fetch": "NETFAIL",
                "status": r.get("status", 0), "error": r.get("error"),
                "h": None, "s": sitemap_index.get(normalise(url)), "v": None,
            })
            continue
        hdr = r["headers"]
        v = extract_v(r["body"])
        rows.append({
            "url": url,
            "fetch": "OK",
            "status": r["status"],
            "bytes": len(r["body"]),
            "h": parse_http_date(hdr.get("last-modified")),
            "h_raw": hdr.get("last-modified"),
            "response_date": parse_http_date(hdr.get("date")),
            "etag": hdr.get("etag"),
            "cache_control": hdr.get("cache-control"),
            "age": hdr.get("age"),
            "s": sitemap_index.get(normalise(url)),
            "in_sitemap": normalise(url) in sitemap_index,
            "v": normalise_v(v["v_raw"]),
            "v_raw": v["v_raw"],
            "v_rule": v["v_rule"],
            "v_context": v["v_context"],
        })

    out = {
        "instrument": "as-of-today",
        "preregistration": "PREREGISTRATION.md",
        "run_started_utc": run_started.isoformat(timespec="seconds"),
        "run_finished_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "corpus_size": len(corpus["corpus"]),
        "sitemap_url": SITEMAP,
        "sitemap_pages_read": sitemap_log,
        "sitemap_urls_indexed": len(sitemap_index),
        "rows": rows,
    }
    with open("signals.json", "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    ok = sum(1 for r in rows if r["fetch"] == "OK")
    print(f"{ok}/{len(rows)} fetched; sitemap indexed {len(sitemap_index)} urls "
          f"over {len(sitemap_log)} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
