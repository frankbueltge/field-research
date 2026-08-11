#!/usr/bin/env python3
"""The retrievability ledger — one dated run of the instrument.

This is session 109's census made repeatable. The probe itself is **unchanged**: the platform's
credential-free oEmbed endpoint, one request at a time, a fixed 1.0 s delay, the same
User-Agent, a 25 s timeout, and an HTTP 429 ends the run by design rather than provoking a
retry storm. Changing the probe between runs would make the runs incomparable, so it is not
changed — only the surrounding bookkeeping is new.

What is new, and why:

* **The vantage is logged before the first measurement request**, into the run file itself.
  Until session 109 wrote it down, every availability figure this practice had ever published
  came from one unlogged network location. A run whose autonomous system differs from the
  previous run's is flagged rather than compared to it (`ledger_diff.py` enforces this).
* **A stable schema with a version string**, so a run written weeks from now still diffs
  against this one.
* **Arms.** Each identifier carries the corpus it came from, so the union can be split back
  apart without re-deriving it.

robots.txt was read to the end before session 109's first run
(`tiktok-robots-2026-08-11.txt`): the `User-agent: *` group does not disallow `/oembed`, and
this client is none of the 25 named crawlers. The consideration is recorded rather than assumed.
"""
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

SCHEMA = "field-research/retrievability-ledger/1"
UA = "field-research/1.0 (independent research instrument; sequential, 1 req/s)"
DELAY = 1.0
TIMEOUT = 25
ENDPOINT = "https://www.tiktok.com/oembed?url="


def vantage():
    """Read the egress point. Recorded before the first measurement request, never after."""
    req = urllib.request.Request("https://ipinfo.io/json", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        d = json.load(r)
    org = d.get("org", "")
    asn = org.split()[0] if org.startswith("AS") else None
    # The autonomous system's registrant name is omitted under this practice's naming rule; the
    # AS number is published so anyone can resolve it themselves.
    return {"ip": d.get("ip"), "city": d.get("city"), "region": d.get("region"),
            "country": d.get("country"), "loc": d.get("loc"), "timezone": d.get("timezone"),
            "asn": asn, "registrant": "[redacted under this practice's naming rule]",
            "source": "https://ipinfo.io/json",
            "fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}


def classify(rec):
    """The three states, fixed in the pre-registration and applied here and nowhere else.

    NOT-RETRIEVABLE is the platform's single opaque refusal. Session 109's three-arm control
    established it is semantically empty: an identifier that never existed returns the same 400,
    and no 404 is ever returned. It therefore means 'not publicly retrievable from this vantage
    right now' and never 'deleted'.
    """
    if rec.get("http") == 200 and not rec.get("parse_error"):
        return "RETRIEVABLE"
    if rec.get("http") == 400:
        return "NOT-RETRIEVABLE"
    return "INDETERMINATE"


def probe_one(vid, handle):
    target = f"https://www.tiktok.com/@{handle}/video/{vid}"
    url = ENDPOINT + urllib.parse.quote(target, safe="")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    rec = {}
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read()
            rec.update(http=resp.status, bytes=len(body))
            try:
                j = json.loads(body)
                rec["author_unique_id"] = j.get("author_unique_id")
                rec["title_len"] = len(j.get("title") or "")
                rec["body_code"] = j.get("code")
            except Exception:
                rec["parse_error"] = True
    except urllib.error.HTTPError as e:
        body = e.read()
        rec.update(http=e.code, bytes=len(body))
        try:
            b = json.loads(body)
            rec["body_code"] = b.get("code")
            rec["body_message"] = b.get("message")
        except Exception:
            rec["body_snippet"] = body[:120].decode("utf-8", "replace")
    except Exception as e:
        rec.update(http=None, transport_error=type(e).__name__ + ": " + str(e)[:120])
    return rec


def main(manifest_path, out_path):
    manifest = json.load(open(manifest_path))
    units = manifest["units"]

    van = vantage()                      # BEFORE the first measurement request
    print(json.dumps({"vantage": van}), file=sys.stderr)

    t0 = time.time()
    obs, stopped = [], None
    for i, u in enumerate(units):
        rec = {"vid": u["vid"], "handle": u["handle"], "arm": u["arm"]}
        rec.update(probe_one(u["vid"], u["handle"]))
        rec["state"] = classify(rec)
        obs.append(rec)
        if rec.get("http") == 429:
            stopped = {"at": i, "reason": "HTTP 429 — throttled; run ended by design, never padded"}
            break
        if (i + 1) % 100 == 0:
            print(f"{i+1}/{len(units)} {time.time()-t0:.0f}s", file=sys.stderr, flush=True)
        time.sleep(DELAY)

    counts = {}
    for r in obs:
        counts.setdefault(r["arm"], {}).setdefault(r["state"], 0)
        counts[r["arm"]][r["state"]] += 1

    run = {"schema": SCHEMA,
           "run_id": manifest["run_id"],
           "run_utc_start": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)),
           "run_utc_end": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "seconds": round(time.time() - t0, 1),
           "vantage": van,
           "probe": {"endpoint": ENDPOINT, "user_agent": UA, "delay_s": DELAY,
                     "timeout_s": TIMEOUT,
                     "unchanged_since": "session 109 census (census.py), 2026-08-11T04:05:44Z"},
           "arms": manifest["arms"],
           "planned": len(units), "requested": len(obs), "stopped": stopped,
           "counts": counts,
           "observations": obs}
    json.dump(run, open(out_path, "w"), indent=1)
    print(json.dumps({"requested": len(obs), "planned": len(units),
                      "seconds": round(time.time() - t0, 1),
                      "stopped": stopped, "counts": counts}))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
