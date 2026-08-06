#!/usr/bin/env python3
"""collect_signals_2.py — proof session 2. Collect H, S, V for GOVUK, NIST and IE.

Written AFTER corpus-2.json was committed (commit 5c0a771), so the corpora cannot be tuned
to the signals. EC is not re-collected: its signals are locked from session 94 (signals.json).

M-1  H = Last-Modified on a plain GET                                     (carried over unchanged)
M-3  V = a visible date, by the SAME pre-declared pattern set, unextended (carried over unchanged)
M-4  one run, one timestamp, all ages against it                          (carried over unchanged)
M-5  a failed fetch is NETFAIL and is excluded from percentages           (carried over unchanged)
M2-6 sitemap children followed one level, STREAMED, only corpus matches retained
M2-7 budget per authority: 60 children / 600 MB / 15 min. If it binds, unmatched corpus URLs are
     SITEMAP-UNRESOLVED — never NOT-IN-SITEMAP — and coverage is a lower bound with the number of
     unread children beside it.

Both arms are fetched: Arm A (corpora as first pre-registered) and Arm B (chrome-filtered, the
scored arm under amendment 4). A URL in both is fetched once.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
import time

from collect_signals import (  # the session-94 implementations, reused unchanged
    extract_v, get, normalise, normalise_v, parse_http_date, parse_iso,
)

UA = "Mozilla/5.0 (compatible; field-research/1.0; public-interest measurement)"
PAUSE = 0.7
MAX_CHILDREN = 60
MAX_BYTES = 600 * 1024 * 1024
MAX_SECONDS = 15 * 60

SITEMAPS = {
    "GOVUK": "https://www.gov.uk/sitemap.xml",
    "NIST": "https://www.nist.gov/sitemap.xml",
    "IE": "https://enterprise.gov.ie/sitemap.xml",
}

URL_BLOCK_RE = re.compile(r"<url>(.*?)</url>", re.S | re.I)
LOC_RE = re.compile(r"<loc>\s*([^<]+?)\s*</loc>", re.I)
LASTMOD_RE = re.compile(r"<lastmod>\s*([^<]+?)\s*</lastmod>", re.I)
CHILD_RE = re.compile(r"<sitemap>(.*?)</sitemap>", re.S | re.I)


def stream_sitemap(url: str, wanted: set[str], found: dict[str, str]) -> dict:
    """Stream one sitemap file, keeping only <url> blocks whose <loc> is in `wanted`."""
    started = time.time()
    proc = subprocess.Popen(
        ["curl", "-sS", "-L", "-A", UA, "--max-time", "300", url],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    buf = ""
    total = 0
    blocks = 0
    assert proc.stdout is not None
    while True:
        chunk = proc.stdout.read(1 << 20)
        if not chunk:
            break
        total += len(chunk)
        buf += chunk.decode("utf-8", "replace")
        last = buf.rfind("</url>")
        if last == -1:
            if len(buf) > 4 << 20:          # no <url> at all: keep only a small tail
                buf = buf[-4096:]
            continue
        head, buf = buf[: last + 6], buf[last + 6:]
        for b in URL_BLOCK_RE.findall(head):
            blocks += 1
            loc = LOC_RE.search(b)
            if not loc:
                continue
            key = normalise(loc.group(1))
            if key in wanted and key not in found:
                lm = LASTMOD_RE.search(b)
                iso = parse_iso(lm.group(1)) if lm else None
                if iso:
                    found[key] = iso
    proc.wait()
    return {"url": url, "bytes": total, "url_blocks": blocks,
            "seconds": round(time.time() - started, 1), "curl_exit": proc.returncode}


def sitemap_for(authority: str, wanted: set[str]) -> dict:
    """M2-6 / M2-7. Returns the found map plus a full, honest log of what was and was not read."""
    index_url = SITEMAPS[authority]
    started = time.time()
    found: dict[str, str] = {}
    log: list[dict] = []

    r = get(index_url, timeout=120)
    if not r.get("ok") or r.get("status") != 200:
        return {"index": index_url, "index_status": r.get("status", 0), "children_total": 0,
                "children_read": 0, "children_unread": 0, "budget_bound": "index-fetch-failed",
                "bytes": 0, "found": found, "log": log}

    body = r["body"]
    children = [LOC_RE.search(b).group(1) for b in CHILD_RE.findall(body) if LOC_RE.search(b)]
    is_index = bool(children)
    if not is_index:                                   # a plain <urlset> served at the index URL
        for b in URL_BLOCK_RE.findall(body):
            loc = LOC_RE.search(b)
            lm = LASTMOD_RE.search(b)
            if loc and lm:
                key = normalise(loc.group(1))
                iso = parse_iso(lm.group(1))
                if key in wanted and iso and key not in found:
                    found[key] = iso
        return {"index": index_url, "index_status": 200, "is_sitemap_index": False,
                "children_total": 0, "children_read": 0, "children_unread": 0,
                "budget_bound": None, "bytes": len(body), "found": found, "log": log}

    total_bytes = 0
    read = 0
    bound = None
    for child in children:
        if read >= MAX_CHILDREN:
            bound = "children-cap"
            break
        if total_bytes >= MAX_BYTES:
            bound = "byte-cap"
            break
        if time.time() - started >= MAX_SECONDS:
            bound = "time-cap"
            break
        entry = stream_sitemap(child, wanted, found)
        total_bytes += entry["bytes"]
        read += 1
        log.append(entry)
        if len(found) == len(wanted):
            bound = "all-corpus-urls-matched"
            break
    return {"index": index_url, "index_status": 200, "is_sitemap_index": True,
            "children_total": len(children), "children_read": read,
            "children_unread": len(children) - read, "budget_bound": bound,
            "bytes": total_bytes, "found": found, "log": log}


def main() -> int:
    c2 = json.load(open("corpus-2.json"))
    run_started = dt.datetime.now(dt.timezone.utc)
    out = {
        "instrument": "as-of-today",
        "stage": "signals, proof session 2",
        "preregistration": "PREREGISTRATION-2.md (with amendments 1-4)",
        "corpus_commit_note": "corpus-2.json committed in 5c0a771, before this file existed",
        "run_started_utc": run_started.isoformat(timespec="seconds"),
        "authorities": {},
    }

    for key, a in c2["authorities"].items():
        if a.get("fetch") != "OK":
            continue
        arm_a = a["arm_a_corpus"]
        arm_b = a["corpus"]
        union = list(dict.fromkeys(arm_a + arm_b))
        wanted = {normalise(u) for u in union}
        sm = sitemap_for(key, wanted)
        found = sm.pop("found")

        rows = []
        for url in union:
            r = get(url)
            time.sleep(PAUSE)
            k = normalise(url)
            s_val = found.get(k)
            if s_val is None and sm.get("budget_bound") in ("children-cap", "byte-cap", "time-cap"):
                s_state = "SITEMAP-UNRESOLVED"
            elif s_val is None:
                s_state = "NOT-IN-SITEMAP"
            else:
                s_state = "IN-SITEMAP"
            base = {"url": url, "arm_a": url in arm_a, "arm_b": url in arm_b,
                    "s": s_val, "s_state": s_state}
            if not r.get("ok") or r.get("status", 0) != 200:
                rows.append({**base, "fetch": "NETFAIL", "status": r.get("status", 0),
                             "error": r.get("error"), "h": None, "v": None})
                continue
            hdr = r["headers"]
            v = extract_v(r["body"])
            rows.append({**base, "fetch": "OK", "status": r["status"], "bytes": len(r["body"]),
                         "h": parse_http_date(hdr.get("last-modified")),
                         "h_raw": hdr.get("last-modified"),
                         "response_date": parse_http_date(hdr.get("date")),
                         "etag": hdr.get("etag"), "cache_control": hdr.get("cache-control"),
                         "age": hdr.get("age"),
                         "v": normalise_v(v["v_raw"]), "v_raw": v["v_raw"],
                         "v_rule": v["v_rule"], "v_context": v["v_context"]})
        out["authorities"][key] = {
            "seed": a["seed"], "arm_a_n": len(arm_a), "arm_b_n": len(arm_b),
            "fetched_n": len(union), "sitemap": sm, "rows": rows,
        }
        ok = sum(1 for x in rows if x["fetch"] == "OK")
        print(f"{key}: {ok}/{len(rows)} fetched; sitemap matched {len(found)}; "
              f"children {sm['children_read']}/{sm['children_total']} "
              f"({sm['bytes']/1e6:.1f} MB, bound={sm['budget_bound']})")

    out["run_finished_utc"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    with open("signals-2.json", "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
