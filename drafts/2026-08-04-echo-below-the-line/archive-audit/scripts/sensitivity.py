"""Sensitivity of the pre-registered result to the two rules that bound it, computed after the
Skeptic's session-91 review demanded it and named the direction it expected.

Two knobs, each defensible, neither pre-registered as primary:

  owner_merge   candidate units carrying the same named operator are merged (D2.2 forbids this in
                the primary; one confirmed owner is otherwise counted as up to nine publishers)
  newsnet_all   the two "News.Net" candidate units are accepted with ALL their members, on the
                strength of the operator's own corporate page naming the News.Net sites as a class,
                rather than only the 7 of 82 whose own pages name that operator. The other 75 are
                reachable (71 answered HTTP 200) and their own pages name a different brand.
  newsnet_class the same units accepted only for the members the class statement actually names —
                those carrying the "News.Net" brand. This is the defensible reading of that source,
                and it turns out to be exactly the members already confirmed per member.

Output: results/sensitivity.json, and a table on stdout.
"""
import json, os, statistics

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(HERE, 'results')
NEWSNET = ('cand-afghanistannews.net', 'cand-arabherald.com')

clusters = json.load(open(os.path.join(R, 'clusters.json')))['clusters']
cands = {g['id']: g for g in json.load(open(os.path.join(R, 'candidates.json')))['units']}
ev = {e['unit_id']: e for e in json.load(open(os.path.join(HERE, 'evidence', 'ownership.json')))['units']}

primary = [c for c in clusters if c['slot'] == 'headline' and c['domain_count'] == c['n_mastheads']]


def partition(owner_merge=False, newsnet_all=False, newsnet_class=False):
    part = {}
    for g in cands.values():
        e = ev.get(g['id'])
        accepted = e and e['verdict'] in ('CONFIRMED', 'SECONDARY')
        named = {m.lower() for m in (e['members_named'] if accepted else [])}
        if newsnet_all and g['id'] in NEWSNET and accepted:
            named = {m.lower() for m in g['members']}
        if newsnet_class and g['id'] in NEWSNET and accepted:
            named = {m.lower() for m in g['members'] if m.lower().endswith('news.net')}
        for m in g['members']:
            if accepted and g['size'] > 1 and m in named:
                part[m] = ('op:' + e['operator']) if owner_merge else g['id']
            else:
                part[m] = 'solo:' + m
    return part


def score(part):
    rows = [(c, len({part.get(m, 'solo:' + m) for m in c['mastheads']})) for c in primary]
    ratios = [c['n_mastheads'] / u for c, u in rows]
    below = [c for c, u in rows if u < (c['min_domains'] or 3)]
    return {'n': len(rows), 'n_below': len(below), 'share_below': len(below) / len(rows),
            'median_ratio': statistics.median(ratios), 'max_ratio': max(ratios),
            'n_ratio_ge_5': sum(1 for r in ratios if r >= 5)}


VARIANTS = [
    ('pre-registered primary (the scored result)', False, False, False),
    ('+ owner-merge only (the disclosed secondary)', True, False, False),
    ('+ News.Net: only the brand the source names', False, False, True),
    ('+ News.Net: ALL 82 members, on pattern', False, True, False),
    ('+ owner-merge AND all 82 on pattern', True, True, False),
]

if __name__ == '__main__':
    out = []
    print(f"{'variant':46s} {'U<3':>10s} {'median':>8s} {'max':>7s} {'Q1':>8s} {'Q2':>8s}  band")
    for name, om, nn, nc in VARIANTS:
        s = score(partition(om, nn, nc))
        q1, q2 = s['share_below'] >= 0.25, s['median_ratio'] >= 2.0
        band = 'Band 1' if (q1 and q2) else 'Band 2' if (q1 or q2) else 'Band 3'
        out.append({'variant': name, 'owner_merge': om, 'newsnet_all': nn, 'newsnet_class': nc,
                    'Q1_holds': q1, 'Q2_holds': q2, 'band': band, **s})
        print(f"{name:46s} {s['n_below']:2d}/{s['n']:2d} {s['share_below']*100:5.1f}% "
              f"{s['median_ratio']:8.2f} {s['max_ratio']:7.2f} "
              f"{'HOLDS' if q1 else 'fails':>8s} {'HOLDS' if q2 else 'fails':>8s}  {band}")
    json.dump({'primary_set_size': len(primary), 'variants': out},
              open(os.path.join(R, 'sensitivity.json'), 'w'), indent=1)
