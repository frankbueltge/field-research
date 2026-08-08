"""Increment 2 — the census of PREREGISTRATION-2.md, computed by prefix query instead of per-URL.

WHY THE ROUTE CHANGED, recorded here rather than in a commit message
--------------------------------------------------------------------
The pre-registration specifies "one query to the public capture index per URL". Executed that way
the archive answered in 8-14 s per query cold and degraded to roughly one per minute under four
concurrent workers; 336 URLs would not finish in a session. The index also answers a *prefix* query
-- every capture of every URL beneath a path -- in about ten seconds, so one query replaces eighty.

**The measured values are identical either way.** A prefix query returns the same capture rows,
each carrying its own `original` URL; the per-URL numbers are obtained by grouping those rows. What
changes is the fetch schedule, not the sample, the window, the fields or the definitions. The
sampled URLs remain exactly those drawn under seed 20260808 in `PREREGISTRATION-2.md` §3, and they
remain the unit of analysis. `census_prefix_selftest.py` checks the two routes agree on the URLs
already measured the slow way.

The prefix response is capped by the server, so each authority-window is subdivided until no slice
comes back at the cap; a slice that cannot be subdivided further is recorded as `TRUNCATED` and its
URLs are excluded from the percentages with a stated count, never silently.

Writes census-prefix.json (per sampled URL, same fields as census.py) and frame-wide totals.
"""
import json, os, re, sys, time, gzip, zlib, random, datetime as dt
import urllib.request, urllib.parse

BASE = "/home/user/field-research/drafts/2026-08-08-does-the-date-move"
UA = "field-research/1.0 (non-commercial research; polite, rate-limited)"
SEED, SAMPLE = 20260808, 80
W24 = ("20240801", "20260731")
W12 = ("20250801", "20260731")
CAP = 150000

PREFIXES = {
    "nist":     "www.nist.gov/publications/",
    "epa":      "www.epa.gov/newsreleases/",
    "govuk":    "www.gov.uk/government/publications/",
    "energy":   "www.energy.gov/articles/",
    "receiver": "standards.digital.gov/",
}


def decode_body(raw, enc):
    if raw[:2] == b"\x1f\x8b":
        return gzip.decompress(raw)
    if enc and "deflate" in enc.lower():
        for w in (-15, 15):
            try:
                return zlib.decompress(raw, w)
            except Exception:  # noqa: BLE001
                continue
    return raw


def get(url, timeout=300, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                hdr = {k.lower(): v for k, v in r.headers.items()}
                return decode_body(r.read(), hdr.get("content-encoding"))
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(5 * (i + 1))
    raise last


def cdx_prefix(prefix, frm, to):
    q = urllib.parse.urlencode({
        "url": prefix, "matchType": "prefix", "output": "json",
        "fl": "original,timestamp", "from": frm, "to": to,
        "filter": "statuscode:200", "limit": str(CAP),
    })
    body = get("https://web.archive.org/cdx/search/cdx?" + q)
    s = body.decode("utf-8", "replace").strip()
    if not s:
        return [], False
    rows = json.loads(s)
    rows = rows[1:] if rows and rows[0][0] == "original" else rows
    return rows, len(rows) >= CAP


def day_windows(frm, to, n):
    a = dt.datetime.strptime(frm, "%Y%m%d").date()
    b = dt.datetime.strptime(to, "%Y%m%d").date()
    step = max(1, ((b - a).days + 1) // n)
    out, cur = [], a
    while cur <= b:
        end = min(b, cur + dt.timedelta(days=step - 1))
        out.append((cur.strftime("%Y%m%d"), end.strftime("%Y%m%d")))
        cur = end + dt.timedelta(days=1)
    return out


def harvest(prefix, frm, to, depth=0):
    """All (original, timestamp) rows under prefix in [frm,to], subdividing on the server cap."""
    rows, capped = cdx_prefix(prefix, frm, to)
    print(f"    {'  '*depth}{frm}-{to}: {len(rows)} rows{' CAPPED' if capped else ''}", flush=True)
    if not capped:
        return rows, []
    if depth >= 4:
        return rows, [(frm, to)]                 # cannot subdivide further: recorded, not hidden
    got, trunc = [], []
    for a, b in day_windows(frm, to, 6):
        r, t = harvest(prefix, a, b, depth + 1)
        got += r
        trunc += t
        time.sleep(1.0)
    return got, trunc


def norm(u):
    u = re.sub(r"^https?://", "", u).split("#")[0]
    u = re.sub(r"^www\.", "www.", u)
    return u.rstrip("/").lower()


def measure_from_rows(url, by_url):
    ts = sorted(by_url.get(norm(url), []))
    rec = {"url": url, "n24": len(ts), "truncated": False}
    in12 = [t for t in ts if W12[0] <= t[:8] <= W12[1]]
    rec["n12"] = len(in12)
    rec["months24"] = len({t[:6] for t in ts})
    rec["months12"] = len({t[:6] for t in in12})
    rec["first"] = ts[0] if ts else None
    rec["last"] = ts[-1] if ts else None
    rec["pairable"] = False
    rec["span_days"] = None
    if len(ts) >= 2:
        d = (dt.datetime.strptime(ts[-1], "%Y%m%d%H%M%S")
             - dt.datetime.strptime(ts[0], "%Y%m%d%H%M%S")).days
        rec["span_days"] = d
        rec["pairable"] = d >= 30
    return rec


def main():
    t0 = time.time()
    frames = json.load(open(f"{BASE}/frames.json"))
    out = {"generated_utc": dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
           "route": "prefix query, see module docstring", "seed": SEED,
           "window24": W24, "window12": W12,
           "frame_sizes": {k: (len(v) if isinstance(v, list) else v) for k, v in frames.items()},
           "authorities": {}, "frame_wide": {}, "truncated_windows": {}}

    for key in ("receiver", "nist", "epa", "govuk", "energy"):
        if key not in frames or not isinstance(frames[key], list):
            continue
        frame = sorted(set(frames[key]))
        urls = frame if len(frame) <= SAMPLE else sorted(random.Random(SEED).sample(frame, SAMPLE))
        print(f"{key}: prefix {PREFIXES[key]} frame {len(frame)} sample {len(urls)}", flush=True)
        rows, trunc = harvest(PREFIXES[key], *W24)
        by_url = {}
        for orig, ts in rows:
            by_url.setdefault(norm(orig), []).append(ts)
        out["authorities"][key] = [measure_from_rows(u, by_url) for u in urls]
        out["truncated_windows"][key] = trunc
        # frame-wide, a free by-product of the route: every distinct URL seen under the prefix
        in_frame = {norm(u) for u in frame}
        seen = {u: v for u, v in by_url.items() if u in in_frame}
        out["frame_wide"][key] = {
            "frame_urls": len(frame),
            "frame_urls_with_any_capture_24m": len(seen),
            "distinct_urls_under_prefix": len(by_url),
            "total_captures_under_prefix_24m": sum(len(v) for v in by_url.values()),
        }
        json.dump(out, open(f"{BASE}/census-prefix.json", "w"), indent=1)
        print(f"  {key} done: {out['frame_wide'][key]}", flush=True)

    out["elapsed_s"] = round(time.time() - t0, 1)
    json.dump(out, open(f"{BASE}/census-prefix.json", "w"), indent=1)
    print("done in", out["elapsed_s"], "s", flush=True)


if __name__ == "__main__":
    main()
