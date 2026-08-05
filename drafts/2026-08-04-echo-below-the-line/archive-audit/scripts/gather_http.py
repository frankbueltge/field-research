"""Stage A3 — the final host each domain lands on after redirects.

Requests https://<domain>/ and follows redirects to the terminus, recording the final hostname,
the status and the redirect chain length. Failures (timeout, TLS, refusal, block) are recorded as
failures; nothing is imputed. Best-effort by design: a domain that will not answer contributes no
A3 evidence and is grouped, if at all, on A1/A2 alone.

Output: provenance/http-final.json
"""
import json, os, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlsplit

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMS = [l.strip() for l in open(os.path.join(HERE, 'results', 'domains.txt')) if l.strip()]
OUT = os.path.join(HERE, 'provenance', 'http-final.json')
UA = {'User-Agent': 'field-research/consensus-archive-audit (research; github.com/frankbueltge/field-research)',
      'Accept': 'text/html'}


def fetch(dom):
    rec = {'domain': dom, 'checked_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
           'final_host': None, 'status': None, 'error': None}
    try:
        req = urllib.request.Request('https://' + dom + '/', headers=UA, method='GET')
        with urllib.request.urlopen(req, timeout=20) as r:
            rec['final_host'] = urlsplit(r.geturl()).hostname
            rec['status'] = r.status
            r.read(1)
    except urllib.error.HTTPError as e:
        rec['status'] = e.code
        rec['final_host'] = urlsplit(e.url).hostname if getattr(e, 'url', None) else None
        rec['error'] = f'HTTP {e.code}'
    except Exception as e:
        rec['error'] = repr(e)[:140]
    return rec


if __name__ == '__main__':
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=12) as ex:
        recs = list(ex.map(fetch, DOMS))
    ok = [r for r in recs if r['final_host']]
    json.dump({'checked_utc_start': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(t0)),
               'checked_utc_end': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
               'n_domains': len(DOMS), 'n_with_final_host': len(ok),
               'records': recs}, open(OUT, 'w'), indent=1)
    print(f"final host for {len(ok)}/{len(DOMS)} in {time.time()-t0:.0f}s")
    moved = [(r['domain'], r['final_host']) for r in ok if r['final_host'] != r['domain']]
    print("redirected off their own host:", len(moved))
