"""Stage B, mechanised — each site's own copyright / publisher statement, read from its own page.

The pre-registration's primary evidence type is "a member site's own imprint or about page naming
the parent". This fetches every domain's home page and extracts the copyright-adjacent text, so the
evidence is gathered per member rather than sampled and generalised.

It decides nothing. It writes what each site says about itself; the ownership specialists' reports
and `scripts/build_ownership.py` decide what that is worth.

Output: provenance/footers.json
"""
import json, os, re, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMS = [l.strip() for l in open(os.path.join(HERE, 'results', 'domains.txt')) if l.strip()]
OUT = os.path.join(HERE, 'provenance', 'footers.json')
UA = {'User-Agent': 'field-research/consensus-archive-audit (research; github.com/frankbueltge/field-research)',
      'Accept': 'text/html'}

TAG = re.compile(r'<(script|style)[^>]*>.*?</\1>', re.S | re.I)
STRIP = re.compile(r'<[^>]+>')
WS = re.compile(r'\s+')
# copyright marks and the German/English publisher words that appear in imprints
MARK = re.compile(r'(©|&copy;|\(c\)\s*20|copyright|all rights reserved|published by|publisher:|'
                  r'part of|a division of|herausgeber|impressum)', re.I)


def text_of(html):
    t = TAG.sub(' ', html)
    t = STRIP.sub(' ', t)
    t = t.replace('&copy;', '©').replace('&amp;', '&').replace('&nbsp;', ' ')
    return WS.sub(' ', t)


def snippets(t):
    out = []
    for m in MARK.finditer(t):
        s = t[max(0, m.start() - 60): m.start() + 200].strip()
        if s not in out:
            out.append(s)
        if len(out) >= 6:
            break
    return out


def fetch(dom):
    rec = {'domain': dom, 'checked_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
           'status': None, 'snippets': [], 'error': None}
    try:
        r = urllib.request.urlopen(urllib.request.Request('https://' + dom + '/', headers=UA), timeout=25)
        rec['status'] = r.status
        rec['snippets'] = snippets(text_of(r.read(600000).decode('utf-8', 'replace')))
    except Exception as e:
        rec['error'] = repr(e)[:120]
    return rec


if __name__ == '__main__':
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=12) as ex:
        recs = list(ex.map(fetch, DOMS))
    ok = [r for r in recs if r['snippets']]
    json.dump({'checked_utc_start': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(t0)),
               'checked_utc_end': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
               'n_domains': len(DOMS), 'n_with_snippets': len(ok), 'records': recs},
              open(OUT, 'w'), indent=1)
    print(f"copyright/imprint text found for {len(ok)}/{len(DOMS)} domains in {time.time()-t0:.0f}s")
