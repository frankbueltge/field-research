#!/usr/bin/env python3
"""Legacy-identifier control — does the endpoint resolve arbitrary small integers?

Written to close condition 5 of `INTERLOCUTOR-2.md`: the first run of this control was an inline
command whose script was not committed and whose raw response bodies were not kept, unlike every
other piece of evidence on this arc. This version is the script, and it stores the **whole body** of
every response.

**The question.** The control arm returned one HTTP 200 among 249 identifiers that were supposed to be
phantoms: `12345`. Two readings with opposite consequences — a false positive in the instrument's
RETRIEVABLE state, which would bound every retrievability figure this arc has published; or a genuine
video whose identifier predates the platform's current 19-digit scheme.

**The reading, stated before the requests go out** (unchanged from the first run): if small integers
resolve generally, then "short identifier" is evidence of nothing and `12345` tells us nothing. If only
some resolve, the ones that do are real videos from before the current scheme.

Same probe discipline as the ledger: sequential, 1 req/s, same User-Agent, 25 s timeout.
"""
import json
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "field-research/1.0 (independent research instrument; sequential, 1 req/s)"
TESTS = ["1", "2", "7", "42", "12345", "12346", "54321", "99999", "123456", "1234567", "999999999"]

out = []
for v in TESTS:
    target = f"https://www.tiktok.com/@user/video/{v}"
    url = "https://www.tiktok.com/oembed?url=" + urllib.parse.quote(target, safe="")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    rec = {"vid": v, "requested_url": url,
           "fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            body = r.read()
            rec.update(http=r.status, bytes=len(body),
                       body=body.decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        body = e.read()
        rec.update(http=e.code, bytes=len(body), body=body.decode("utf-8", "replace"))
    except Exception as e:
        rec.update(http=None, transport_error=type(e).__name__ + ": " + str(e)[:120])
    out.append(rec)
    print(json.dumps({k: v2 for k, v2 in rec.items() if k != "body"}))
    time.sleep(1.0)

n200 = sum(1 for r in out if r.get("http") == 200)
json.dump({"purpose": "legacy-identifier control, session 110 — rerun with script and raw bodies "
                      "committed, discharging condition 5 of INTERLOCUTOR-2.md",
           "reading_fixed_before_the_requests":
               "if small integers resolve generally, '12345' shows nothing; if only some resolve, "
               "the ones that do are real videos predating the current identifier scheme",
           "user_agent": UA, "delay_s": 1.0,
           "n_tested": len(out), "n_http_200": n200,
           "results": out},
          open("legacy-id-control.json", "w"), indent=1)
print(f"\n{n200} of {len(out)} small integers returned HTTP 200")
