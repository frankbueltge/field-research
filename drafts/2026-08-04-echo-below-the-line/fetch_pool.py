"""Fetch one day's GDELT DOC 2.0 article pool for the eight beats the audited
instrument declares (politics, economy, technology, health, science, business,
sports, weather), English-language, and store the raw responses verbatim.

Pacing: the endpoint returned HTTP 429 under 15-second spacing on 2026-08-04, so
this version idles 4 minutes before the first request and then paces one request
per 60 seconds, at most 3 attempts per beat. Beats that never return are recorded
as missing in the manifest rather than silently dropped — a missing beat is a
disclosed gap, not a smaller pool.

Already-present raw files are reused, so a re-run only fills the gaps.
"""
import json, time, urllib.request, urllib.parse, hashlib, os, sys

BEATS = ["politics","economy","technology","health","science","business","sports","weather"]
UA = {'User-Agent':'field-research/consensus-audit (research; github.com/frankbueltge/field-research)'}
os.makedirs('provenance', exist_ok=True)
counts, digests, failed = {}, {}, []
time.sleep(int(sys.argv[1]) if len(sys.argv) > 1 else 240)
for b in BEATS:
    p = f'provenance/gdelt-{b}.json'
    if os.path.exists(p) and os.path.getsize(p) > 1000:
        raw = open(p,'rb').read()
        counts[b] = len(json.loads(raw).get('articles',[])); digests[b] = hashlib.sha256(raw).hexdigest()
        print('cached', b, counts[b], flush=True); continue
    url = ("https://api.gdeltproject.org/api/v2/doc/doc?query=" + urllib.parse.quote(f'{b} sourcelang:eng')
           + "&mode=artlist&maxrecords=250&format=json&timespan=1d&sort=datedesc")
    got = False
    for attempt in range(3):
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()
            d = json.loads(raw)
            open(p,'wb').write(raw)
            counts[b] = len(d.get('articles',[])); digests[b] = hashlib.sha256(raw).hexdigest()
            print('ok', b, counts[b], digests[b][:12], flush=True); got = True; break
        except Exception as e:
            print('retry', b, attempt, repr(e)[:90], flush=True); time.sleep(60)
    if not got:
        failed.append(b); print('FAILED', b, flush=True)
    time.sleep(60)
json.dump({"fetched_utc": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
           "endpoint": "https://api.gdeltproject.org/api/v2/doc/doc",
           "query_template": "<beat> sourcelang:eng", "mode": "artlist",
           "maxrecords": 250, "timespan": "1d", "sort": "datedesc",
           "beats_declared": BEATS, "beats_missing": failed,
           "counts": counts, "sha256": digests},
          open('provenance/fetch-manifest.json','w'), indent=2)
print("TOTAL", sum(counts.values()), "MISSING", failed)
