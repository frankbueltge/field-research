"""Second pass for the day-2 fetch: only the beats the first pass did not get.

The first pass was refused with HTTP 429 on every attempt. Nothing about the request
changes here except patience and order: the PRIMARY beat (politics — the pre-registered
head-to-head against day 1) is asked first, then the rest in the declared order, with a
long idle before the first request and 240 s between requests, 3 attempts per beat.

Already-present raw files are reused and never re-requested. The manifest is rewritten
from whatever is on disk at the end, so a partial pool is recorded as a partial pool.
"""
import json, time, urllib.request, urllib.parse, hashlib, os, sys

BEATS_DECLARED = ["politics","economy","technology","health","science","business","sports","weather"]
ORDER = ["politics","technology","health","economy","science","business","sports","weather"]
UA = {'User-Agent':'field-research/consensus-audit (research; github.com/frankbueltge/field-research)'}
IDLE = int(sys.argv[1]) if len(sys.argv) > 1 else 300
SPACING = 240
log = open('provenance/fetch.log','a')
def say(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True); log.write(time.strftime('%H:%M:%S ') + s + '\n'); log.flush()

say(f'--- second pass, idle {IDLE}s then {SPACING}s spacing, politics first')
time.sleep(IDLE)
first = True
for b in ORDER:
    p = f'provenance/gdelt-{b}.json'
    if os.path.exists(p) and os.path.getsize(p) > 1000:
        say('cached', b); continue
    if not first: time.sleep(SPACING)
    first = False
    url = ("https://api.gdeltproject.org/api/v2/doc/doc?query=" + urllib.parse.quote(f'{b} sourcelang:eng')
           + "&mode=artlist&maxrecords=250&format=json&timespan=1d&sort=datedesc")
    for attempt in range(3):
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()
            d = json.loads(raw)
            open(p,'wb').write(raw)
            say('ok', b, len(d.get('articles',[])), hashlib.sha256(raw).hexdigest()[:12]); break
        except Exception as e:
            say('retry', b, attempt, repr(e)[:90])
            if attempt < 2: time.sleep(SPACING)
    else:
        say('FAILED', b)

counts, digests, failed = {}, {}, []
for b in BEATS_DECLARED:
    p = f'provenance/gdelt-{b}.json'
    if os.path.exists(p) and os.path.getsize(p) > 1000:
        raw = open(p,'rb').read()
        counts[b] = len(json.loads(raw).get('articles',[])); digests[b] = hashlib.sha256(raw).hexdigest()
    else:
        failed.append(b)
json.dump({"fetched_utc": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
           "endpoint": "https://api.gdeltproject.org/api/v2/doc/doc",
           "query_template": "<beat> sourcelang:eng", "mode": "artlist",
           "maxrecords": 250, "timespan": "1d", "sort": "datedesc",
           "pacing_deviation_from_session_89": ("first pass: idle 0s, 75s between beats, 90s between attempts, "
                                                "all eight refused with HTTP 429. second pass: idle "
                                                f"{IDLE}s, {SPACING}s spacing, politics first."),
           "beats_declared": BEATS_DECLARED, "beats_missing": failed,
           "counts": counts, "sha256": digests},
          open('provenance/fetch-manifest.json','w'), indent=2)
say("TOTAL", sum(counts.values()), "MISSING", failed)
