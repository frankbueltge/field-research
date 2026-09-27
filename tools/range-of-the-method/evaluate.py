#!/usr/bin/env python3
"""Read lattice.json and decide the six registered predictions. Session 172, 2026-09-27."""
import json, os, statistics, sys
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..',
                 'artifacts/2026-09-27-the-range-of-the-method/data')
L = json.load(open(os.path.join(D, 'lattice.json')))
S, F, B, BASE = L['screens'], L['flags'], L['bootstrap_base'], L['base']
KEYS = ['window', 'conn', 'split', 'pairing', 'text']


def is_base(r, keys=KEYS):
    return all(r[k] == BASE[k] for k in keys)


out = {'corpora': {}}
for c in ('M', 'A', 'F'):
    rates = [r[c]['rate'] for r in S]
    base = next(r for r in S if is_base(r))[c]['rate']
    out['corpora'][c] = {'base_rate': base, 'min': min(rates), 'max': max(rates),
                         'median': round(statistics.median(rates), 4),
                         'range_width': round(max(rates) - min(rates), 4),
                         'bootstrap': B[c],
                         'bootstrap_width': round(B[c]['high'] - B[c]['low'], 4),
                         'specs_within_bootstrap': sum(B[c]['low'] <= x <= B[c]['high'] for x in rates),
                         'specs': len(rates)}
    incs = [r[c]['inconsistent'] for r in F]
    cons = [r[c]['consistent'] for r in F]
    out['corpora'][c]['inconsistent'] = {'min': min(incs), 'max': max(incs),
                                        'base': next(r for r in F if is_base(r) and r['match'] == BASE['match'])[c]['inconsistent']}
    out['corpora'][c]['consistent'] = {'min': min(cons), 'max': max(cons),
                                      'base': next(r for r in F if is_base(r) and r['match'] == BASE['match'])[c]['consistent']}
# one at a time, M
ooat = {}
for k in KEYS:
    rows = [r for r in S if is_base(r, [x for x in KEYS if x != k])]
    ooat[k] = {str(r[k]): {c: r[c]['rate'] for c in ('M', 'A', 'F')} for r in rows}
rows = [r for r in F if is_base(r)]
ooat['match'] = {r['match']: {'M_inconsistent': r['M']['inconsistent'], 'M_consistent': r['M']['consistent'],
                              'known_real_errors_flagged': r['known_real_errors_flagged']} for r in rows}
out['one_at_a_time'] = ooat
spread = {k: round(max(v['M'] for v in ooat[k].values()) - min(v['M'] for v in ooat[k].values()), 4)
          for k in KEYS}
out['one_at_a_time_M_spread'] = spread
m = out['corpora']['M']
p5_rows = [r for r in F if (r['window'] is None or r['window'] >= 40) and r['match'] in ('round', 'round-or-trunc')]
out['predictions'] = {
    'P1': {'ratio': round(m['range_width'] / m['bootstrap_width'], 2),
           'held': m['range_width'] >= 2 * m['bootstrap_width']},
    'P2': {'specs_M_above_A': sum(r['M']['rate'] > r['A']['rate'] for r in S), 'of': len(S),
           'held': all(r['M']['rate'] > r['A']['rate'] for r in S)},
    'P3': {'largest': max(spread, key=spread.get), 'held': max(spread, key=spread.get) == 'window'},
    'P4': {'min': m['inconsistent']['min'], 'max': m['inconsistent']['max'],
           'held': m['inconsistent']['max'] > 2 * m['inconsistent']['min']},
    'P5': {'rows': len(p5_rows), 'rows_keeping_all_six': sum(r['known_real_errors_flagged'] == 6 for r in p5_rows),
           'min_kept': min(r['known_real_errors_flagged'] for r in p5_rows),
           'held': all(r['known_real_errors_flagged'] == 6 for r in p5_rows)},
    'P6': {'max_rate_any': max(max(r[c]['rate'] for c in ('M', 'A', 'F')) for r in S),
           'held': all(r[c]['rate'] < 50 for r in S for c in ('M', 'A', 'F'))},
}
json.dump(out, open(os.path.join(D, 'evaluation.json'), 'w'), indent=1)
print(json.dumps(out, indent=1))
