#!/usr/bin/env python3
"""09-23's six hand-read real errors under the four registered matching arithmetics.
Session 172, 2026-09-27. Pure arithmetic on adjudication.json; no corpus needed."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lattice as L                                                  # noqa: E402
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
out = os.path.join(ROOT, 'artifacts/2026-09-27-the-range-of-the-method/data/errors.json')
real = [r for r in json.load(open(L.ADJ))['M'] if r['verdict'] == 'real']
rows = []
for r in real:
    num = r['printed'].replace('%', '').strip()
    p, d = float(num), L.H._decimals(num)
    k, n = r['pair']
    rows.append({'doc': r['doc'], 'printed': r['printed'], 'k': k, 'n': n,
                 'exact': round(100.0 * k / n, 4),
                 'flagged': {m: L.verdict(m, p, d, (k, n)) == 'inconsistent' for m in L.MATCHERS}})
tot = {m: {'errors': sum(x['flagged'][m] for x in rows),
           'documents': len({x['doc'] for x in rows if x['flagged'][m]})} for m in L.MATCHERS}
json.dump({'source': 'artifacts/2026-09-23-a-number-you-cannot-check/data/adjudication.json',
           'errors': rows, 'totals': tot}, open(out, 'w'), indent=1)
print(json.dumps(tot))
