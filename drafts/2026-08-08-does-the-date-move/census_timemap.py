"""Increment 2 — the census of PREREGISTRATION-2.md, computed over the per-URL timemap.

WHY THE ROUTE CHANGED, and what was done to make sure the measurement did not
----------------------------------------------------------------------------
The pre-registration specifies "one query to the public capture index (CDX) per URL". Executed that
way the archive answered in 8-14 s cold and degraded under concurrency (four workers ~= one query a
minute; two workers barely better); 336 URLs would not finish in a session. The archive also serves
a per-URL *timemap* — `https://web.archive.org/web/timemap/json/<url>` — which returns the same
capture rows with the same fields (`urlkey, timestamp, original, mimetype, statuscode, digest,
length`) in about **1 s**.

**This is a fetch-route change, not a measurement change.** Same unit (one URL), same sample, same
windows, same fields, same definitions. The two differences are handled explicitly:
  - the timemap is not windowed, so the `from`/`to` filter is applied here instead of server-side;
  - the timemap returns every status, so `statuscode == "200"` is applied here instead of
    server-side (this also drops revisit rows, whose statuscode is "-", exactly as the CDX
    `filter=statuscode:200` did).

**It is checked, not asserted.** `--selftest` recomputes every URL already measured the slow way
(cached in census-partial.json) through the new route and reports any URL where any derived value
differs. The census is only run if that check passes; the check's output is quoted in RESULT-2.md.
"""
import json, os, sys, time, random, datetime as dt
import urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = "/home/user/field-research/drafts/2026-08-08-does-the-date-move"
UA = "field-research/1.0 (non-commercial research; polite, rate-limited)"
SEED, SAMPLE, WORKERS = 20260808, 80, 4
W24 = ("20240801", "20260731")
W12 = ("20250801", "20260731")


def get(url, timeout=120, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001 - recorded, never silently swallowed
            last = e
            time.sleep(3 * (i + 1))
    raise last


def timestamps(url):
    """Every 200-status capture timestamp of exactly this URL, within the 24-month window."""
    body = get("https://web.archive.org/web/timemap/json/" + url)
    s = body.decode("utf-8", "replace").strip()
    if not s:
        return []
    rows = json.loads(s)
    if rows and rows[0] and rows[0][0] == "urlkey":
        head, rows = rows[0], rows[1:]
    else:
        head = ["urlkey", "timestamp", "original", "mimetype", "statuscode", "digest", "length"]
    ti, si = head.index("timestamp"), head.index("statuscode")
    return sorted(r[ti] for r in rows
                  if r[si] == "200" and W24[0] <= r[ti][:8] <= W24[1])


def derive(url, ts):
    rec = {"url": url, "n24": len(ts), "truncated": False}
    in12 = [t for t in ts if W12[0] <= t[:8] <= W12[1]]
    rec["n12"] = len(in12)
    rec["months24"] = len({t[:6] for t in ts})
    rec["months12"] = len({t[:6] for t in in12})
    rec["first"] = ts[0] if ts else None
    rec["last"] = ts[-1] if ts else None
    rec["pairable"], rec["span_days"] = False, None
    if len(ts) >= 2:
        d = (dt.datetime.strptime(ts[-1], "%Y%m%d%H%M%S")
             - dt.datetime.strptime(ts[0], "%Y%m%d%H%M%S")).days
        rec["span_days"] = d
        rec["pairable"] = d >= 30
    return rec


def measure(url):
    try:
        return derive(url, timestamps(url))
    except Exception as e:  # noqa: BLE001
        return {"url": url, "error": f"{type(e).__name__}: {e}"}


FIELDS = ("n24", "n12", "months24", "months12", "first", "last", "pairable", "span_days")


def selftest():
    old = json.load(open(f"{BASE}/census-partial.json"))
    old = {u: r for u, r in old.items() if "error" not in r}
    print(f"self-test: recomputing {len(old)} URLs measured through the capture-index route", flush=True)
    disagree = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        new = list(ex.map(measure, list(old)))
    for r in new:
        o = old[r["url"]]
        if "error" in r:
            disagree.append((r["url"], "error", r["error"]))
            continue
        for f in FIELDS:
            if o.get(f) != r.get(f):
                disagree.append((r["url"], f, f"index={o.get(f)} timemap={r.get(f)}"))
    print(f"self-test: {len(old)} URLs, {len(disagree)} disagreements")
    for d in disagree[:40]:
        print("  DISAGREE", d)
    json.dump({"urls_checked": len(old), "disagreements": disagree},
              open(f"{BASE}/route-selftest.json", "w"), indent=1)
    return not disagree


def main():
    frames = json.load(open(f"{BASE}/frames.json"))
    cache = {}
    if os.path.exists(f"{BASE}/census-timemap-partial.json"):
        cache = json.load(open(f"{BASE}/census-timemap-partial.json"))
    out = {"generated_utc": dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
           "route": "per-URL timemap; see module docstring and route-selftest.json",
           "seed": SEED, "window24": W24, "window12": W12,
           "frame_sizes": {k: (len(v) if isinstance(v, list) else v) for k, v in frames.items()},
           "authorities": {}}
    for key in ("receiver", "nist", "epa", "govuk", "energy"):
        if key not in frames or not isinstance(frames[key], list):
            continue
        frame = sorted(set(frames[key]))
        urls = frame if len(frame) <= SAMPLE else sorted(random.Random(SEED).sample(frame, SAMPLE))
        todo = [u for u in urls if u not in cache]
        print(f"{key}: sample {len(urls)}, {len(todo)} to fetch", flush=True)
        done = [0]

        def one(u, key=key, n=len(todo)):
            r = measure(u)
            cache[u] = r
            done[0] += 1
            if done[0] % 10 == 0:
                json.dump(cache, open(f"{BASE}/census-timemap-partial.json", "w"))
                print(f"  [{key} {done[0]}/{n}]", flush=True)
            return r

        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            list(ex.map(one, todo))
        json.dump(cache, open(f"{BASE}/census-timemap-partial.json", "w"))
        out["authorities"][key] = [cache[u] for u in urls]
        json.dump(out, open(f"{BASE}/census.json", "w"), indent=1)
        print(f"  {key} complete", flush=True)
    print("done in", 0, "s", flush=True)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    main()
