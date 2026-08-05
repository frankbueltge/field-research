"""Day 2 of the echo audit: fetch the same eight declared beats from the same
public API, same query template, same mode/maxrecords/timespan/sort as session 89's
`fetch_pool.py`.

ONE DEVIATION, declared here rather than discovered later: the PACING differs.
Session 89 idled 240 s, then paced 60 s between requests with 3 attempts per beat,
and five of eight beats were refused by the provider. This version idles 0 s, paces
75 s between requests and waits 90 s between attempts, still 3 attempts per beat.
Nothing about the query, the pool recipe or the measurement changes; only how
politely it is asked. Beats that never return are recorded as missing.
"""
import json, time, urllib.request, urllib.parse, hashlib, os, sys

BEATS = ["politics","economy","technology","health","science","business","sports","weather"]
UA = {'User-Agent':'field-research/consensus-audit (research; github.com/frankbueltge/field-research)'}
os.makedirs('provenance', exist_ok=True)
counts, digests, failed = {}, {}, []
log = open('provenance/fetch.log','a')
def say(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True); log.write(time.strftime('%H:%M:%S ') + s + '\n'); log.flush()
for i, b in enumerate(BEATS):
    p = f'provenance/gdelt-{b}.json'
    if os.path.exists(p) and os.path.getsize(p) > 1000:
        raw = open(p,'rb').read()
        counts[b] = len(json.loads(raw).get('articles',[])); digests[b] = hashlib.sha256(raw).hexdigest()
        say('cached', b, counts[b]); continue
    url = ("https://api.gdeltproject.org/api/v2/doc/doc?query=" + urllib.parse.quote(f'{b} sourcelang:eng')
           + "&mode=artlist&maxrecords=250&format=json&timespan=1d&sort=datedesc")
    got = False
    for attempt in range(3):
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()
            d = json.loads(raw)
            open(p,'wb').write(raw)
            counts[b] = len(d.get('articles',[])); digests[b] = hashlib.sha256(raw).hexdigest()
            say('ok', b, counts[b], digests[b][:12]); got = True; break
        except Exception as e:
            say('retry', b, attempt, repr(e)[:90]); time.sleep(90)
    if not got:
        failed.append(b); say('FAILED', b)
    if i < len(BEATS) - 1: time.sleep(75)
json.dump({"fetched_utc": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
           "endpoint": "https://api.gdeltproject.org/api/v2/doc/doc",
           "query_template": "<beat> sourcelang:eng", "mode": "artlist",
           "maxrecords": 250, "timespan": "1d", "sort": "datedesc",
           "pacing_deviation_from_session_89": "idle 0s (was 240s); 75s between beats (was 60s); 90s between attempts (was 60s); 3 attempts (unchanged)",
           "beats_declared": BEATS, "beats_missing": failed,
           "counts": counts, "sha256": digests},
          open('provenance/fetch-manifest.json','w'), indent=2)
say("TOTAL", sum(counts.values()), "MISSING", failed)
