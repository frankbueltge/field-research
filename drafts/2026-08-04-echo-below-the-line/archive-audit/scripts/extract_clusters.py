"""Stage 0 — read the audited instrument's own committed dated snapshots and extract,
per day, the clusters it published with masthead lists.

Input : provenance/consensus/YYYY-MM-DD.json  (copied verbatim from the site repository,
        commit recorded in provenance/SOURCE.md; latest.json is excluded as a duplicate)
Output: results/clusters.json  — one record per published cluster
        results/domains.txt    — the distinct domains, one per line, sorted

No judgement here: this only reads what the instrument committed.
"""
import json, glob, os, hashlib, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAP = os.path.join(HERE, 'provenance', 'consensus')
OUT = os.path.join(HERE, 'results')
os.makedirs(OUT, exist_ok=True)

DATED = re.compile(r'^\d{4}-\d{2}-\d{2}\.json$')

clusters, digests, days = [], {}, []
for path in sorted(glob.glob(os.path.join(SNAP, '*.json'))):
    name = os.path.basename(path)
    if not DATED.match(name):
        continue                      # latest.json duplicates a dated file
    raw = open(path, 'rb').read()
    digests[name] = hashlib.sha256(raw).hexdigest()
    d = json.loads(raw)
    days.append(d.get('date'))
    for slot in ('headline', 'runner_up'):
        c = d.get(slot)
        if not isinstance(c, dict):
            continue
        mast = c.get('mastheads')
        if not mast:
            continue
        clusters.append({
            'date': d.get('date'),
            'slot': slot,
            'phrase': c.get('phrase'),
            'sample_title': c.get('sample_title'),
            'domain_count': c.get('domain_count'),
            'article_count': c.get('article_count'),
            'mastheads': [m.strip().lower() for m in mast],
            'n_mastheads': len(mast),
            'syndication_label': (c.get('syndication') or {}).get('label'),
            'tld_share': (c.get('syndication') or {}).get('tld_share'),
            'echo_index': d.get('echo_index'),
            'articles_scanned': (d.get('stats') or {}).get('articles_scanned'),
            'domains_scanned': (d.get('stats') or {}).get('domains_scanned'),
            'min_domains': (d.get('stats') or {}).get('min_domains'),
            'shingle_n': (d.get('stats') or {}).get('shingle_n'),
        })

doms = sorted({m for c in clusters for m in c['mastheads']})
json.dump({'source_files': digests, 'n_day_files': len(digests), 'clusters': clusters},
          open(os.path.join(OUT, 'clusters.json'), 'w'), indent=2, ensure_ascii=False)
open(os.path.join(OUT, 'domains.txt'), 'w').write('\n'.join(doms) + '\n')

head = [c for c in clusters if c['slot'] == 'headline']
mismatch = [(c['date'], c['slot'], c['domain_count'], c['n_mastheads'])
            for c in clusters if c['domain_count'] != c['n_mastheads']]
print(f"day files            {len(digests)}")
print(f"clusters             {len(clusters)}  (headline {len(head)}, runner-up {len(clusters)-len(head)})")
print(f"distinct domains     {len(doms)}")
print(f"domain mentions      {sum(c['n_mastheads'] for c in clusters)}")
print(f"published domain_count != len(mastheads): {len(mismatch)}")
for m in mismatch:
    print("   ", m)
