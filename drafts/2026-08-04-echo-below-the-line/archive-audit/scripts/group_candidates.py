"""Stage A — union-find over the three mechanical evidence relations. No judgement, no ownership.

A1  same registrable domain (eTLD+1, explicit suffix list below)
A2  identical authoritative nameserver set (>= 2 nameservers, exact sorted tuple)
A3  identical final host after redirects (leading 'www.' stripped), when at least one of the two
    domains is not already that host — i.e. a domain that lands on somebody else's front door

Output: results/candidates.json — the candidate units, each with the relations that built it.
"""
import json, os
from collections import defaultdict

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(HERE, 'results')

# Two-label public suffixes occurring in this corpus' TLD space. Explicit, not inferred.
TWO_LABEL = {
    'co.uk', 'org.uk', 'me.uk', 'ltd.uk', 'plc.uk', 'net.uk', 'sch.uk', 'ac.uk', 'gov.uk',
    'com.au', 'net.au', 'org.au', 'co.nz', 'net.nz', 'org.nz', 'co.za', 'org.za',
    'com.br', 'com.mx', 'com.ar', 'com.co', 'com.pe', 'com.tr', 'com.sg', 'com.my',
    'com.ph', 'com.pk', 'com.ng', 'com.gh', 'co.in', 'net.in', 'org.in', 'co.il',
    'co.ke', 'co.th', 'com.tw', 'com.hk', 'com.cn', 'co.jp', 'or.jp', 'ne.jp', 'com.ua',
    'co.id', 'com.vn', 'com.eg', 'com.sa', 'com.bd', 'com.np', 'com.lb', 'com.cy',
    'co.ug', 'co.tz', 'com.jm', 'com.bo', 'com.ec', 'com.uy', 'com.py', 'com.do',
    'com.gt', 'com.ni', 'com.pa', 'com.ve', 'org.pk', 'net.pk', 'com.mt', 'com.pr',
}


def norm(h):
    h = (h or '').strip().lower().rstrip('.')
    return h[4:] if h.startswith('www.') else h


def etld1(host):
    parts = norm(host).split('.')
    if len(parts) >= 3 and '.'.join(parts[-2:]) in TWO_LABEL:
        return '.'.join(parts[-3:])
    return '.'.join(parts[-2:]) if len(parts) >= 2 else norm(host)


class UF:
    def __init__(self):
        self.p = {}
        self.why = defaultdict(list)

    def find(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b, rel):
        ra, rb = self.find(a), self.find(b)
        self.why[tuple(sorted((a, b)))].append(rel)
        if ra != rb:
            self.p[rb] = ra


def build():
    doms = [l.strip() for l in open(os.path.join(R, 'domains.txt')) if l.strip()]
    dns = {r['domain']: r for r in json.load(open(os.path.join(HERE, 'provenance', 'dns-ns.json')))['records']}
    http = {r['domain']: r for r in json.load(open(os.path.join(HERE, 'provenance', 'http-final.json')))['records']}

    uf = UF()
    for d in doms:
        uf.find(d)

    # A1 — same registrable domain
    by_reg = defaultdict(list)
    for d in doms:
        by_reg[etld1(d)].append(d)
    for reg, members in by_reg.items():
        for m in members[1:]:
            uf.union(members[0], m, f'A1:{reg}')

    # A2 — identical nameserver set
    by_ns = defaultdict(list)
    for d in doms:
        ns = dns.get(d, {}).get('ns') or []
        if len(ns) >= 2:
            by_ns[tuple(ns)].append(d)
    for ns, members in by_ns.items():
        for m in members[1:]:
            uf.union(members[0], m, 'A2:' + '|'.join(ns))

    # A3 — identical final host, where that host is somebody's front door and not their own
    by_final = defaultdict(list)
    for d in doms:
        f = norm(http.get(d, {}).get('final_host'))
        if f and f != norm(d):
            by_final[f].append(d)
    for f, members in by_final.items():
        # a single domain landing on a foreign host groups with that host if it is in the corpus
        pool = members + ([f] if f in set(doms) else [])
        for m in pool[1:]:
            uf.union(pool[0], m, f'A3:{f}')

    groups = defaultdict(list)
    for d in doms:
        groups[uf.find(d)].append(d)

    out = []
    for root, members in groups.items():
        members = sorted(members)
        rels = defaultdict(int)
        for pair, why in uf.why.items():
            if pair[0] in members and pair[1] in members:
                for w in why:
                    rels[w.split(':')[0]] += 1
        out.append({'id': f'cand-{members[0]}', 'size': len(members), 'members': members,
                    'relation_counts': dict(rels),
                    'ns_sets': sorted({tuple(dns.get(m, {}).get('ns') or []) and
                                       '|'.join(dns[m]['ns']) for m in members if dns.get(m, {}).get('ns')}),
                    'final_hosts': sorted({norm(http.get(m, {}).get('final_host')) for m in members
                                           if http.get(m, {}).get('final_host')})})
    out.sort(key=lambda g: -g['size'])
    json.dump({'n_domains': len(doms), 'n_candidate_units': len(out), 'units': out},
              open(os.path.join(R, 'candidates.json'), 'w'), indent=1)
    return out


if __name__ == '__main__':
    out = build()
    multi = [g for g in out if g['size'] > 1]
    print(f"candidate units {len(out)}  (multi-member {len(multi)}, singletons {len(out)-len(multi)})")
    for g in out[:15]:
        print(f"  {g['size']:3d}  {g['relation_counts']}  {', '.join(g['members'][:6])}"
              + (' …' if g['size'] > 6 else ''))
