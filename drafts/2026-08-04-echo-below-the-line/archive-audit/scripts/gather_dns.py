"""Stage A2 — authoritative nameserver sets for every domain in the archive, over DNS-over-HTTPS.

Primary resolver: dns.google. Fallback: cloudflare-dns.com. Both are asked with the standard
JSON DNS API. Every answer is written with its query timestamp and the resolver that answered;
failures are written as failures and never imputed.

Output: provenance/dns-ns.json
"""
import json, os, sys, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMS = [l.strip() for l in open(os.path.join(HERE, 'results', 'domains.txt')) if l.strip()]
OUT = os.path.join(HERE, 'provenance', 'dns-ns.json')

RESOLVERS = [('dns.google', 'https://dns.google/resolve?name={}&type=NS'),
             ('cloudflare-dns.com', 'https://cloudflare-dns.com/dns-query?name={}&type=NS')]
HDR = {'accept': 'application/dns-json',
       'User-Agent': 'field-research/consensus-archive-audit (research; github.com/frankbueltge/field-research)'}


def parents(host):
    """The host itself, then each parent label set down to two labels."""
    parts = host.split('.')
    out = []
    for i in range(0, len(parts) - 1):
        out.append('.'.join(parts[i:]))
    return out


def query(name, resolver_url):
    url = resolver_url.format(urllib.parse.quote(name))
    raw = urllib.request.urlopen(urllib.request.Request(url, headers=HDR), timeout=25).read()
    d = json.loads(raw)
    ns = sorted({a['data'].rstrip('.').lower()
                 for a in d.get('Answer', []) if a.get('type') == 2})
    return ns, d.get('Status')


def lookup(host):
    """NS records are published at the zone apex; walk up from the host until a zone answers."""
    rec = {'domain': host, 'queried_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
           'ns': None, 'ns_zone': None, 'resolver': None, 'error': None, 'tried': []}
    for cand in parents(host):
        for rname, rurl in RESOLVERS:
            try:
                ns, status = query(cand, rurl)
                rec['tried'].append({'name': cand, 'resolver': rname, 'status': status, 'n_ns': len(ns)})
                if ns:
                    rec.update(ns=ns, ns_zone=cand, resolver=rname)
                    return rec
                break                      # resolver answered, just no NS at this level
            except Exception as e:
                rec['tried'].append({'name': cand, 'resolver': rname, 'error': repr(e)[:120]})
                rec['error'] = repr(e)[:120]
                time.sleep(1.0)
    return rec


if __name__ == '__main__':
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=8) as ex:
        recs = list(ex.map(lookup, DOMS))
    ok = [r for r in recs if r['ns']]
    json.dump({'queried_utc_start': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(t0)),
               'queried_utc_end': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
               'resolvers': [r[0] for r in RESOLVERS],
               'n_domains': len(DOMS), 'n_resolved': len(ok),
               'records': recs}, open(OUT, 'w'), indent=1)
    print(f"resolved {len(ok)}/{len(DOMS)} in {time.time()-t0:.0f}s")
    print("unresolved:", [r['domain'] for r in recs if not r['ns']][:25])
