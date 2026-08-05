"""Third pass: the primary beat only, asked slowly, for as long as the session lasts.

The pre-registration scores exactly one head-to-head — day-1 politics against day-2 politics.
Everything else is secondary. Two passes at 60-90 s and 240 s spacing were refused with HTTP 429
on every attempt, so this pass asks for politics alone, once every 600 s, up to 10 times, and
stops the moment it succeeds. Nothing about the query changes.

If it never succeeds, Band 0 of the pre-registration fires and no prediction is scored.
"""
import json, time, urllib.request, urllib.parse, hashlib, os

UA = {'User-Agent': 'field-research/consensus-audit (research; github.com/frankbueltge/field-research)'}
URL = ("https://api.gdeltproject.org/api/v2/doc/doc?query=" + urllib.parse.quote('politics sourcelang:eng')
       + "&mode=artlist&maxrecords=250&format=json&timespan=1d&sort=datedesc")
SPACING, ATTEMPTS = 600, 10
log = open('provenance/fetch.log', 'a')

def say(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True); log.write(time.strftime('%H:%M:%S ') + s + '\n'); log.flush()

say(f'--- third pass: politics only, {ATTEMPTS} attempts, {SPACING}s apart')
for attempt in range(ATTEMPTS):
    if os.path.exists('provenance/gdelt-politics.json'):
        say('already present, stopping'); break
    try:
        raw = urllib.request.urlopen(urllib.request.Request(URL, headers=UA), timeout=120).read()
        d = json.loads(raw)
        n = len(d.get('articles', []))
        if n == 0:
            say('empty response, not written', attempt);
        else:
            open('provenance/gdelt-politics.json', 'wb').write(raw)
            say('ok politics', n, hashlib.sha256(raw).hexdigest()[:12]); break
    except Exception as e:
        say('retry politics', attempt, repr(e)[:90])
    if attempt < ATTEMPTS - 1:
        time.sleep(SPACING)
else:
    say('FAILED politics after', ATTEMPTS, 'slow attempts')
say('--- third pass ends')
