#!/usr/bin/env python3
"""EXPLORATORY (added 2026-09-29 after the pre-registered results were seen).

    explore.py <data_dir>

From results.json only: (a) a journal bootstrap of the frame gap and its three parts;
(b) which journals carry the residual (frame records of a journal vs its own Jan-Jun sample).
"""
import json
import os
import random
import sys

D = sys.argv[1]
R = json.load(open(os.path.join(D, 'results.json')))
PJ = R['per_journal']
J = sorted(PJ)


def parts(js):
    T = {y: sum(PJ[j][f'frame{y[2:]}_tok'] for j in js) for y in ('2021', '2026')}
    if not all(T.values()):
        return None
    w = {y: {j: PJ[j][f'frame{y[2:]}_tok'] / T[y] for j in js} for y in T}
    r = {y: {j: (100 * PJ[j][y]['con'] / PJ[j][y]['tok'] if PJ[j][y]['tok'] else 0.0) for j in js} for y in T}
    f = {y: 100 * sum(PJ[j][f'frame{y[2:]}_con'] for j in js) / T[y] for y in T}
    comp = sum((w['2026'][j] - w['2021'][j]) * (r['2021'][j] + r['2026'][j]) / 2 for j in js)
    rate = sum((r['2026'][j] - r['2021'][j]) * (w['2021'][j] + w['2026'][j]) / 2 for j in js)
    gap = f['2026'] - f['2021']
    # the residual split by year: how far each August frame sits from its journals' Jan-Jun rates
    dev = {y: f[y] - sum(w[y][j] * r[y][j] for j in js) for y in T}
    return {'gap': gap, 'composition': comp, 'rate': rate, 'residual': gap - comp - rate,
            'frame21_minus_panel': dev['2021'], 'frame26_minus_panel': dev['2026']}


pt = parts(J)
rng = random.Random(20260929)
B = {k: [] for k in pt}
for _ in range(2000):
    p = parts([J[rng.randrange(len(J))] for _ in J])
    if p:
        for k in p:
            B[k].append(p[k])
ci = {k: [round(sorted(v)[int(0.025 * len(v))], 2), round(sorted(v)[int(0.975 * len(v)) - 1], 2)] for k, v in B.items()}
yb = {y: [] for y in ('2021', '2025', '2026')}
rng2 = random.Random(20260930)
for _ in range(2000):
    s = [J[rng2.randrange(len(J))] for _ in J]
    for y in yb:
        t = sum(PJ[j][y]['tok'] for j in s)
        yb[y].append(100 * sum(PJ[j][y]['con'] for j in s) / t)
panel_ci = {y: [round(sorted(v)[50], 2), round(sorted(v)[1949], 2)] for y, v in yb.items()}
carry = []
for j in J:
    for y in ('2021', '2026'):
        t = PJ[j][f'frame{y[2:]}_tok']
        if t:
            r = PJ[j][y]['con'] / PJ[j][y]['tok'] if PJ[j][y]['tok'] else 0.0
            carry.append({'jid': j, 'frame': y, 'frame_tokens': t, 'frame_agreeing': PJ[j][f'frame{y[2:]}_con'],
                          'expected_at_own_rate': round(t * r, 2),
                          'excess': round(PJ[j][f'frame{y[2:]}_con'] - t * r, 2)})
carry.sort(key=lambda c: -abs(c['excess']))
out = {'registered': 'EXPLORATORY, added 2026-09-29 after the pre-registered results were seen',
       'point': {k: round(v, 2) for k, v in pt.items()}, 'ci95_journal_bootstrap': ci,
       'draws_used': len(B['gap']), 'panel_C_ci95_journal_bootstrap': panel_ci, 'largest_excess_journal_frames': carry[:8],
       'excess_sum': {y: round(sum(c['excess'] for c in carry if c['frame'] == y), 2) for y in ('2021', '2026')}}
json.dump(out, open(os.path.join(D, 'explore.json'), 'w'), indent=1)
print(json.dumps(out, indent=1))
