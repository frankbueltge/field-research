#!/usr/bin/env python3
"""The control arm: ask the platform's own credential-free oEmbed endpoint, once per
sampled video, whether that video is publicly retrievable today.

No account, no key, no application. Sequential, one request at a time, with a fixed delay.
A throttling response (HTTP 429) ends the run rather than provoking a retry storm — the
run is then reported as short, never padded.

robots.txt was read to the end before this ran (`tiktok-robots-2026-08-11.txt`): the
`User-agent: *` group does not disallow `/oembed`, and this client is none of the named
crawlers. The consideration is recorded rather than assumed.
"""
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "field-research/1.0 (independent research instrument; sequential, 1 req/s)"
DELAY = 1.0

corpus = json.load(open("corpus-merged.json"))
rows = corpus["rows"]
sample = corpus["sample"]

out = []
stopped = None
t0 = time.time()
for i, vid in enumerate(sample):
    r = rows[vid]
    target = f"https://www.tiktok.com/@{r['handle']}/video/{vid}"
    url = "https://www.tiktok.com/oembed?url=" + urllib.parse.quote(target, safe="")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    rec = {"vid": vid, "handle": r["handle"], "created": r["created"],
           "year": r["year"], "wiki": r["wiki"], "page": r["page"]}
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
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
            rec["body_code"] = json.loads(body).get("code")
            rec["body_message"] = json.loads(body).get("message")
        except Exception:
            rec["body_snippet"] = body[:120].decode("utf-8", "replace")
        if e.code == 429:
            stopped = {"at": i, "reason": "HTTP 429 — throttled; run ended by design"}
            out.append(rec)
            break
    except Exception as e:
        rec.update(http=None, transport_error=type(e).__name__ + ": " + str(e)[:120])
    out.append(rec)
    if (i + 1) % 50 == 0:
        print(f"{i+1}/{len(sample)} {time.time()-t0:.0f}s", file=sys.stderr)
    time.sleep(DELAY)

json.dump({"run_utc_start": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)),
           "seconds": round(time.time() - t0, 1),
           "requested": len(out), "planned": len(sample),
           "stopped": stopped, "delay_s": DELAY, "results": out},
          open("probe-results.json", "w"), indent=1)
print(json.dumps({"requested": len(out), "seconds": round(time.time() - t0, 1),
                  "stopped": stopped}))
