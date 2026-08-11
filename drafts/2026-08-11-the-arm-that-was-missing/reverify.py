#!/usr/bin/env python3
"""Does the opaque HTTP 400 describe the video, or does it describe us?

Kill criterion K3 asks whether the non-200 responses are blanket refusals of this client
rather than statements about the video. That is a testable question, so it is tested here
rather than argued:

  arm A — every non-200 row from the main run, re-asked 3 times on fresh connections;
  arm B — a control sample of rows that returned 200, re-asked once, interleaved;
  arm C — a NEGATIVE CONTROL: well-formed but randomly generated ids that almost certainly
          correspond to no video. These are not claims about any real video; they are
          synthetic probes, generated with a fixed seed and published, whose only purpose
          is to learn what the endpoint says about something that does not exist.

If arm A reproduces, arm B reproduces, and arm C returns the same 400, then the 400 is
video-specific and means "not publicly retrievable through this route", with no finer
resolution than that.
"""
import json
import random
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "field-research/1.0 (independent research instrument; sequential, 1 req/s)"
DELAY = 1.0


def ask(handle, vid):
    target = f"https://www.tiktok.com/@{handle}/video/{vid}"
    url = "https://www.tiktok.com/oembed?url=" + urllib.parse.quote(target, safe="")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            b = r.read()
            j = {}
            try:
                j = json.loads(b)
            except Exception:
                pass
            return {"http": r.status, "bytes": len(b), "author": j.get("author_unique_id")}
    except urllib.error.HTTPError as e:
        b = e.read()
        try:
            j = json.loads(b)
            return {"http": e.code, "bytes": len(b), "code": j.get("code"),
                    "message": j.get("message")}
        except Exception:
            return {"http": e.code, "bytes": len(b), "snippet": b[:100].decode("utf-8", "replace")}
    except Exception as e:
        return {"http": None, "transport_error": type(e).__name__ + ": " + str(e)[:100]}


main = json.load(open("probe-results.json"))["results"]
bad = [r for r in main if r.get("http") != 200]
good = [r for r in main if r.get("http") == 200]

rnd = random.Random(20260811)
ctrl = rnd.sample(good, 40)

# arm C: synthetic ids. Top 32 bits = a unix timestamp drawn from the corpus range,
# low 32 bits random. Handle taken from a real row so the URL shape is identical.
syn = []
for i in range(20):
    ts = rnd.randint(1590000000, 1780000000)
    syn.append({"vid": str((ts << 32) | rnd.getrandbits(32)), "handle": "tiktok"})

out = {"arm_a": [], "arm_b": [], "arm_c": []}
t0 = time.time()

for rep in (1, 2, 3):
    for r in bad:
        res = ask(r["handle"], r["vid"])
        out["arm_a"].append({"rep": rep, "vid": r["vid"], "handle": r["handle"],
                             "year": r["year"], **res})
        time.sleep(DELAY)
    for r in ctrl[:14]:          # interleave controls between repetitions
        res = ask(r["handle"], r["vid"])
        out["arm_b"].append({"rep": rep, "vid": r["vid"], "handle": r["handle"],
                             "year": r["year"], **res})
        time.sleep(DELAY)
    ctrl = ctrl[14:] + ctrl[:14]

for s in syn:
    res = ask(s["handle"], s["vid"])
    out["arm_c"].append({"vid": s["vid"], "handle": s["handle"], "synthetic": True, **res})
    time.sleep(DELAY)

out["seconds"] = round(time.time() - t0, 1)
out["run_utc_start"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0))
json.dump(out, open("reverify-results.json", "w"), indent=1)
print(json.dumps({k: len(v) for k, v in out.items() if isinstance(v, list)}))
print("seconds", out["seconds"])
