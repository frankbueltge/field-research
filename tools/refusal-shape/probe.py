#!/usr/bin/env python3
"""Probe every pre-registered unit under three honest request shapes.

PREREGISTRATION.md §2. Three arms per unit (bare / urllib / named), arm order seeded per unit,
one GET each, redirects followed, one retry on a transport error only. robots.txt is fetched for
the request host first with the named arm; if it disallows the path for `*`, the unit is NOT
probed. Per-host spacing is max(2 s, Crawl-delay) capped at 10 s.

No arm claims to be a browser and no arm attempts a challenge, a cookie or a token. That is a
design decision with a reason, stated in the pre-registration.

    python3 tools/refusal-shape/probe.py
"""
import datetime
import json
import pathlib
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from coding import parse_robots, robots_disallows  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA = ROOT / "artifacts/2026-09-15-whose-refusal-is-it/data"

NAMED_UA = "Meridian/1.0 (field research reachability probe; +https://frankbueltge.de/field)"
TIMEOUT = 25
MIN_SPACING = 2.0
MAX_SPACING = 10.0
SEED = 20260915

CHALLENGE_MARKS = [
    "just a moment", "cf-mitigated", "enable javascript", "captcha", "cloudflare",
    "checking your browser", "ddos", "access denied", "are you a robot",
]

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


def request(url, arm, delay=None, keep=200):
    """One GET. Returns a record; never raises. `keep` bounds the body excerpt recorded."""
    host = urllib.parse.urlsplit(url).netloc
    space(host, delay)
    headers = {"Accept": "*/*"}
    if arm == "named":
        headers["User-Agent"] = NAMED_UA
    # urllib's default UA is Python-urllib/3.x; the bare arm removes it entirely.
    rec = {"arm": arm, "url": url, "status": None, "final_url": None, "redirects": [],
           "bytes": None, "www_authenticate": False, "server": None, "challenge": False,
           "error": None, "body_head": None}
    handler = KeepRedirects()
    opener = urllib.request.build_opener(handler)
    if arm == "bare":
        opener.addheaders = []
    req = urllib.request.Request(url, headers=headers)
    try:
        with opener.open(req, timeout=TIMEOUT) as r:
            body = r.read(4096)
            rec.update(status=r.status, final_url=r.url,
                       bytes=len(body), server=r.headers.get("Server"),
                       www_authenticate=r.headers.get("WWW-Authenticate") is not None)
            rec["body_head"] = body[:keep].decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        body = b""
        try:
            body = e.read(4096)
        except Exception:
            pass
        rec.update(status=e.code, final_url=e.url, bytes=len(body),
                   server=e.headers.get("Server") if e.headers else None,
                   www_authenticate=bool(e.headers and e.headers.get("WWW-Authenticate")))
        rec["body_head"] = body[:keep].decode("utf-8", "replace")
    except Exception as e:
        rec["error"] = f"{type(e).__name__}: {e}"[:200]
    rec["redirects"] = handler.chain
    low = (rec["body_head"] or "").lower()
    rec["challenge"] = any(m in low for m in CHALLENGE_MARKS)
    return rec


def robots_for(url):
    """Fetch and cache robots.txt for a URL's host, with the named arm."""
    parts = urllib.parse.urlsplit(url)
    host = parts.netloc
    if host in robots_cache:
        return robots_cache[host]
    r = request(f"{parts.scheme}://{host}/robots.txt", "named")
    text = ""
    if r["status"] and 200 <= r["status"] < 300:
        # body_head is only the first 200 chars; refetch in full for a served policy
        try:
            req = urllib.request.Request(f"{parts.scheme}://{host}/robots.txt",
                                         headers={"User-Agent": NAMED_UA, "Accept": "*/*"})
            space(host, None)
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                text = resp.read(200000).decode("utf-8", "replace")
        except Exception:
            text = r["body_head"] or ""
    entry = {"host": host, "status": r["status"], "error": r["error"],
             "served": bool(text.strip()), "bytes": len(text),
             "crawl_delay": parse_robots(text)[1], "text": text[:4000]}
    robots_cache[host] = entry
    return entry


def main():
    pop = json.loads((DATA / "population.json").read_text())
    units = pop["units"]
    out = []
    for i, u in enumerate(units, 1):
        parts = urllib.parse.urlsplit(u["url"])
        path = parts.path + (("?" + parts.query) if parts.query else "") or "/"
        rb = robots_for(u["url"])
        blocked = robots_disallows(rb["text"], path) if rb["served"] else False
        rec = dict(u)
        rec["request_host"] = parts.netloc
        rec["robots"] = {k: rb[k] for k in ("status", "served", "bytes", "crawl_delay", "error")}
        rec["robots_blocked"] = blocked
        rec["arms"] = {}
        if blocked:
            rec["robots_rule"] = rb["text"][:600]
            print(f"[{i}/{len(units)}] {u['unit_id']}  ROBOTS-DISALLOW, not probed")
        else:
            order = ["bare", "urllib", "named"]
            random.Random(SEED + i).shuffle(order)
            rec["arm_order"] = order
            for arm in order:
                r = request(u["url"], arm, rb["crawl_delay"])
                if r["status"] is None and r["error"]:
                    time.sleep(5)
                    r2 = request(u["url"], arm, rb["crawl_delay"])
                    r2["retry_of"] = r["error"]
                    r = r2
                rec["arms"][arm] = r
            got = {a: rec["arms"][a]["status"] for a in ("bare", "urllib", "named")}
            print(f"[{i}/{len(units)}] {u['unit_id']:<58} {got}")
        # the host the identifier actually resolved to, for the post-hoc ground
        finals = [rec["arms"][a].get("final_url") for a in rec["arms"] if rec["arms"][a].get("final_url")]
        rec["resolved_host"] = urllib.parse.urlsplit(finals[0]).netloc if finals else None
        out.append(rec)

    # The published ground at the host a DOI actually resolved to (§2.2): read after the
    # probe, never used as a licence to re-request.
    resolved = {}
    for rec in out:
        h = rec.get("resolved_host")
        if h and h != rec["request_host"] and h not in resolved:
            rb = robots_for(f"https://{h}/")
            resolved[h] = {k: rb[k] for k in ("status", "served", "bytes", "crawl_delay", "error")}
            resolved[h]["text"] = rb["text"][:2000]
            print(f"  post-hoc robots {h}: {rb['status']} served={rb['served']}")

    (DATA / "probes.json").write_text(json.dumps({
        "_note": "One GET per arm per unit, run under PREREGISTRATION.md §2. One vantage, one "
        "night, one egress — every number here is bounded to that.",
        "probed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "named_user_agent": NAMED_UA,
        "python": sys.version.split()[0],
        "units": out,
        "robots_request_hosts": {h: {**{k: v[k] for k in ("status", "served", "bytes",
                                                          "crawl_delay", "error")},
                                     "text": v["text"][:2000]}
                                 for h, v in robots_cache.items()},
        "robots_resolved_hosts": resolved,
    }, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {DATA/'probes.json'}")


if __name__ == "__main__":
    main()
