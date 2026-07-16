#!/usr/bin/env python3
"""Wayback CDX coverage census — session 41 (2026-07-16). See README.md for method.

Reads urls.json (extract_urls.py output); writes cdx_results.json. Queries capture
METADATA only (timestamps/status codes) — fetches no cited content. Outcomes:
covered_in_window (capture in 2023-10-01..2025-01-01) · covered_ever · no_captures ·
cdx_gated_403 (publisher-level CDX exclusion: coverage unknowable anonymously) ·
query_failed. For x.com/twitter.com URLs the domain-swapped twin is also tried.
Parallel (5 workers) + resumable via cdx_results_partial.json. Throttle politely:
the 2026-07-16 run saw transient connection resets under parallel load, resolved
by a serial ~1 s-spaced retry of the 40 affected URLs (RESULTS.md, methods notes)."""
import json, subprocess, time, threading
from urllib.parse import urlparse, quote
from concurrent.futures import ThreadPoolExecutor

BASE = "https://web.archive.org/cdx/search/cdx"

def cdx(url, window):
    q = f"{BASE}?url={quote(url, safe='')}&output=json&fl=timestamp,statuscode&limit=4"
    if window:
        q += "&from=20231001&to=20250101"
    for attempt in range(3):
        p = subprocess.run(["curl", "-s", "-m", "25", q], capture_output=True, text=True)
        out = p.stdout.strip()
        if "requires authorization" in out:
            return "GATED"
        if p.returncode == 0 and (out == "" or out.startswith("[")):
            if out == "":
                return []
            try:
                rows = json.loads(out)
                return rows[1:] if rows else []
            except json.JSONDecodeError:
                pass
        time.sleep(2 * (attempt + 1))
    return None

def swap_host(u):
    p = urlparse(u)
    h = p.netloc.lower().removeprefix("www.")
    if h == "x.com":
        return u.replace(p.netloc, "twitter.com", 1)
    if h in ("twitter.com", "mobile.twitter.com"):
        return u.replace(p.netloc, "x.com", 1)
    return None

def probe(item):
    u, src, strat = item["url"], item["source"], item["stratum"]
    rec = {"url": u, "source": src, "stratum": strat}
    variants = [u] + ([swap_host(u)] if swap_host(u) else [])
    win, ever = [], []
    gated = failed = False
    for v in variants:
        r = cdx(v, window=True)
        if r == "GATED":
            gated = True
            continue
        if r is None:
            failed = True
            continue
        if r:
            win.extend(r)
            continue
        r2 = cdx(v, window=False)
        if r2 == "GATED":
            gated = True
        elif r2 is None:
            failed = True
        elif r2:
            ever.extend(r2)
    if win:
        rec["outcome"] = "covered_in_window"
        rec["captures"] = win[:4]
    elif ever:
        rec["outcome"] = "covered_ever"
        rec["captures"] = ever[:4]
    elif gated:
        rec["outcome"] = "cdx_gated_403"
    elif failed:
        rec["outcome"] = "query_failed"
    else:
        rec["outcome"] = "no_captures"
    return rec

inp = json.load(open("urls.json"))
try:
    done = {r["url"]: r for r in json.load(open("cdx_results_partial.json"))
            if r.get("outcome") not in (None, "query_failed")}
except FileNotFoundError:
    done = {}
todo = [x for x in inp if x["url"] not in done]
print(f"resuming: {len(done)} done, {len(todo)} to go", flush=True)
results = list(done.values())
lock = threading.Lock()
n = 0
with ThreadPoolExecutor(max_workers=5) as ex:
    for rec in ex.map(probe, todo):
        with lock:
            results.append(rec)
            n += 1
            if n % 50 == 0:
                print(f"+{n}/{len(todo)}", flush=True)
                json.dump(results, open("cdx_results.json", "w"), indent=0)
json.dump(results, open("cdx_results.json", "w"), indent=0)
print("done", len(results), flush=True)
