#!/usr/bin/env python3
"""Arm `local` of PREREGISTRATION.md §3. One honest GET per eligible unit, named UA only.

Reuses the population committed at artifacts/2026-09-15-whose-refusal-is-it/data/population.json
and the robots/challenge rules of tools/refusal-shape/{coding.py,probe.py}, unchanged.

    python3 tools/another-network/local_probe.py
"""
import datetime
import hashlib
import json
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
OLD_ART = ROOT / "artifacts/2026-09-15-whose-refusal-is-it"
ART = ROOT / "artifacts/2026-09-24-another-network"
DATA = ART / "data"

sys.path.insert(0, str((ROOT / "tools/refusal-shape").resolve()))
from coding import parse_robots, robots_disallows  # noqa: E402

NAMED_UA = "Meridian/1.0 (field research reachability probe; +https://frankbueltge.de/field)"
TIMEOUT = 25
MIN_SPACING = 2.0
MAX_SPACING = 10.0
CHALLENGE_MARKS = [
    "just a moment", "cf-mitigated", "enable javascript", "captcha", "cloudflare",
    "checking your browser", "ddos", "access denied", "are you a robot",
]
ROBOTS_EXCLUDED = {
    "H:en-wikipedia-org", "H:query-wikidata-org", "H:www-reddit-com", "C:api-coingecko-com",
}

last_hit = {}
robots_cache = {}


def space(host, delay):
    wait = min(max(MIN_SPACING, delay or 0), MAX_SPACING)
    prev = last_hit.get(host)
    if prev is not None:
        gap = time.time() - prev
        if gap < wait:
            time.sleep(wait - gap)
    last_hit[host] = time.time()


class KeepRedirects(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        self.chain = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.chain.append([code, newurl])
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def request(url, delay=None, keep=4096):
    host = urllib.parse.urlsplit(url).netloc
    space(host, delay)
    headers = {"Accept": "*/*", "User-Agent": NAMED_UA}
    rec = {"url": url, "status": None, "final_url": None, "redirects": [],
           "bytes": None, "server": None, "error": None, "body_head": None}
    handler = KeepRedirects()
    opener = urllib.request.build_opener(handler)
    req = urllib.request.Request(url, headers=headers)
    try:
        with opener.open(req, timeout=TIMEOUT) as r:
            body = r.read(keep)
            rec.update(status=r.status, final_url=r.url, bytes=len(body),
                       server=r.headers.get("Server"))
            rec["body_head"] = body[:keep].decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        body = b""
        try:
            body = e.read(keep)
        except Exception:
            pass
        rec.update(status=e.code, final_url=e.url, bytes=len(body),
                   server=e.headers.get("Server") if e.headers else None)
        rec["body_head"] = body[:keep].decode("utf-8", "replace")
    except Exception as e:
        rec["error"] = f"{type(e).__name__}: {e}"[:200]
    rec["redirects"] = handler.chain
    low = (rec["body_head"] or "").lower()
    rec["challenge"] = any(m in low for m in CHALLENGE_MARKS)
    return rec


def robots_for(url):
    parts = urllib.parse.urlsplit(url)
    host = parts.netloc
    if host in robots_cache:
        return robots_cache[host]
    r = request(f"{parts.scheme}://{host}/robots.txt")
    text = ""
    if r["status"] and 200 <= r["status"] < 300:
        text = r["body_head"] or ""
        if r.get("bytes") == 4096:
            try:
                req = urllib.request.Request(f"{parts.scheme}://{host}/robots.txt",
                                              headers={"User-Agent": NAMED_UA, "Accept": "*/*"})
                space(host, None)
                with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                    text = resp.read(200000).decode("utf-8", "replace")
            except Exception:
                pass
    entry = {"host": host, "status": r["status"], "error": r["error"],
             "served": bool(text.strip()), "bytes": len(text),
             "crawl_delay": parse_robots(text)[1], "text": text}
    robots_cache[host] = entry
    return entry


def refuses(rec):
    if rec["error"]:
        return True
    if rec["status"] in (401, 403, 429):
        return True
    if rec["challenge"]:
        return True
    return False


def main():
    pop = json.loads((OLD_ART / "data/population.json").read_text())
    pop_raw = (OLD_ART / "data/population.json").read_bytes()
    units = [u for u in pop["units"] if u["unit_id"] not in ROBOTS_EXCLUDED]
    assert len(units) == 65, f"expected 65 eligible units, got {len(units)}"

    out = []
    for i, u in enumerate(units, 1):
        parts = urllib.parse.urlsplit(u["url"])
        path = parts.path + (("?" + parts.query) if parts.query else "") or "/"
        rb = robots_for(u["url"])
        blocked = robots_disallows(rb.get("text") or "", path) if rb["served"] else False
        rec = {"unit_id": u["unit_id"], "stratum": u["stratum"], "url": u["url"],
               "recorded_status": u["recorded_status"]}
        if blocked:
            rec["skipped_robots_at_probe_time"] = True
            rec["local"] = None
            print(f"[{i}/65] {u['unit_id']:<58} ROBOTS-DISALLOW (newly found), not probed")
        else:
            r = request(u["url"], rb["crawl_delay"])
            if r["status"] is None and r["error"]:
                time.sleep(5)
                r2 = request(u["url"], rb["crawl_delay"])
                r2["retry_of"] = r["error"]
                r = r2
            rec["local"] = r
            rec["local_refuses"] = refuses(r)
            print(f"[{i}/65] {u['unit_id']:<58} status={r['status']} error={r['error']} "
                  f"refuses={rec['local_refuses']}")
        out.append(rec)

    (DATA / "population-snapshot.json").write_text(json.dumps({
        "_note": "sha256 of the reused 09-15 population.json, recorded before this arm's probe ran.",
        "source": "artifacts/2026-09-15-whose-refusal-is-it/data/population.json",
        "sha256": hashlib.sha256(pop_raw).hexdigest(),
        "units_total": len(pop["units"]),
        "units_eligible": len(units),
        "robots_excluded": sorted(ROBOTS_EXCLUDED),
    }, indent=1) + "\n")

    (DATA / "local.json").write_text(json.dumps({
        "_note": "Arm `local`, PREREGISTRATION.md §3. One GET per eligible unit, named UA only, "
        "one vantage, one session, this date.",
        "probed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "named_user_agent": NAMED_UA,
        "python": sys.version.split()[0],
        "units": out,
    }, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {DATA/'local.json'}")


if __name__ == "__main__":
    main()
