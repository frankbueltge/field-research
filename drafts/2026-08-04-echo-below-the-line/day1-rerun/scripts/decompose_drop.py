"""Decompose the publisher-collapse drop, as the Interlocutor demanded.

The question: is the fall of the echo index from 23.60% to 3.20% a general property
of the pool, or four large wire-syndication stories? This script answers it by
attributing every title that LOSES echo status under publisher-collapse to the
publisher group that caused the loss, and reporting the size distribution.

Reads only provenance/gdelt-politics.json — the exact file the session's reviewers
reviewed — so the answer is comparable with results/summary.md. Standard library,
deterministic, no network.
"""
import json, re, collections, hashlib
from urllib.parse import urlsplit

import glob, os, sys
# Default: the exact file the session's three reviewers reviewed. Pass --all to decompose the
# larger, unreviewed pool of every beat file present.
if '--all' in sys.argv:
    RAW = sorted(glob.glob('provenance/gdelt-*.json'))
else:
    RAW = ['provenance/gdelt-politics.json']
arts = []
for f in RAW:
    arts.extend(json.load(open(f))['articles'])
seen, pool = set(), []
for a in arts:
    if a['url'] in seen: continue
    seen.add(a['url']); pool.append(a)

# Unicode-aware by default, matching the fixed normalisation in measure_echo.py; the reviewed
# state used the ASCII-only pattern, reproducible with ECHO_ASCII_ONLY=1.
import os as _os
_PAT = re.compile(r'[^a-z0-9]+') if _os.environ.get('ECHO_ASCII_ONLY') == '1' else re.compile(r'[\W_]+', re.UNICODE)
def norm(t): return _PAT.sub(' ', t.lower()).strip()
def toks(t): return norm(t).split()

# publisher groups: domains transitively linked by an identical URL path
path_of = lambda u: urlsplit(u).path
by_path = collections.defaultdict(set)
for a in pool: by_path[path_of(a['url'])].add(a['domain'])
parent = {a['domain']: a['domain'] for a in pool}
def find(x):
    while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
    return x
def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb: parent[max(ra, rb)] = min(ra, rb)
for doms in by_path.values():
    d = sorted(doms)
    for x in d[1:]: union(d[0], x)
group = {d: find(d) for d in parent}
groups = collections.defaultdict(set)
for d, g in group.items(): groups[g].add(d)

def echo_titles(unit):
    """unit: callable domain -> counting unit. Returns set of pool indices flagged."""
    shingle_units = collections.defaultdict(set)
    for i, a in enumerate(pool):
        t = toks(a['title'])
        for j in range(len(t) - 5):
            shingle_units[' '.join(t[j:j+6])].add(unit(a['domain']))
    hot = {s for s, u in shingle_units.items() if len(u) >= 3}
    out = set()
    for i, a in enumerate(pool):
        t = toks(a['title'])
        if any(' '.join(t[j:j+6]) in hot for j in range(len(t) - 5)): out.add(i)
    return out

A = echo_titles(lambda d: d)
C = echo_titles(lambda d: group[d])
lost = sorted(A - C)

# attribute each lost title to the publisher group(s) of the domains that carried its phrases
attrib = collections.Counter()
for i in lost:
    attrib[group[pool[i]['domain']]] += 1

rows = []
for g, n in attrib.most_common():
    rows.append({"publisher_group_representative_domain": g,
                 "domains_in_group": len(groups[g]),
                 "titles_that_lost_echo_status": n,
                 "percentage_points_of_the_drop": round(100.0 * n / len(pool), 2)})

out = {
    "source_files": RAW,
    "source_sha256": {f: hashlib.sha256(open(f,'rb').read()).hexdigest() for f in RAW},
    "normalisation": "ascii-only" if _os.environ.get('ECHO_ASCII_ONLY') == '1' else "unicode-aware",
    "pool_size": len(pool),
    "echo_titles_domain_unit": len(A),
    "echo_titles_publisher_unit": len(C),
    "titles_that_lost_echo_status": len(lost),
    "total_drop_pp": round(100.0*(len(A)-len(C))/len(pool), 2),
    "attribution_by_publisher_group": rows,
    "share_of_drop_from_largest_group_pp": rows[0]["percentage_points_of_the_drop"] if rows else 0,
    "share_of_drop_from_top_four_groups_pp": round(sum(r["percentage_points_of_the_drop"] for r in rows[:4]), 2),
    "number_of_publisher_groups_causing_any_loss": len(rows),
    "note": "A title 'loses echo status' when every 6-token phrase that put it in a >=3-domain echo is no longer carried by >=3 distinct publisher units. Attribution is to the publisher group of the title's own domain. A shared URL path shows same-item republication through common publishing infrastructure; it is not evidence of common ownership and no ownership claim is made."
}
outdir = os.environ.get('ECHO_RESULTS_DIR', 'results')
os.makedirs(outdir, exist_ok=True)
json.dump(out, open(os.path.join(outdir, 'drop_decomposition.json'), 'w'), indent=2)
print(json.dumps({k: v for k, v in out.items() if k != 'attribution_by_publisher_group'}, indent=2))
print("\nattribution (group size -> titles lost):")
for r in rows: print(f"  {r['domains_in_group']:>3} domains  {r['titles_that_lost_echo_status']:>3} titles  {r['percentage_points_of_the_drop']:>6} pp   {r['publisher_group_representative_domain']}")
