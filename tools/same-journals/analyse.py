#!/usr/bin/env python3
"""Same journals, two years — session 174, 2026-09-29. Analysis as pre-registered.

    analyse.py <raw_dir> <data_dir>

Imports handover.py (09-23) unchanged. Writes counts, identifiers and digests only.
No model, no network.
"""
import hashlib
import json
import os
import random
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'a-number-you-cannot-check'))
import handover as H                                               # noqa: E402

SEED, DRAWS, GAP = 20260929, 2000, 6.94 - 2.92
YEARS = ('2021', '2025', '2026')


def sha(t):
    return hashlib.sha256(t.encode('utf-8')).hexdigest()


def count(text):
    v = [t['verdict'] for t in H.analyse(text)]
    return {'tok': len(v), 'rec': sum(x != 'not_recomputable' for x in v), 'con': v.count('consistent')}


def add(a, b):
    for k in b:
        a[k] = a.get(k, 0) + b[k]
    return a


def pooled(js, tab, y, k='con'):
    t = sum(tab[j][y]['tok'] for j in js)
    return 100 * sum(tab[j][y][k] for j in js) / t if t else float('nan')


def pct(v, q):
    s = sorted(v)
    return round(s[min(len(s) - 1, int(q * len(s)))], 2)


def main():
    raw, out = sys.argv[1], sys.argv[2]
    P = json.load(open(os.path.join(raw, 'panel.json'), encoding='utf-8'))
    FR = json.load(open(os.path.join(raw, 'frames.json'), encoding='utf-8'))
    FJ = json.load(open(os.path.join(raw, 'frame_journals.json')))
    panel = P['panel']
    qual = sorted(j for j, v in panel.items() if v['qualifies'])
    tab, manifest = {}, {}
    for j in qual:
        tab[j] = {}
        for y in YEARS:
            docs = panel[j].get(y, {'docs': []})['docs']
            tab[j][y] = {'tok': 0, 'rec': 0, 'con': 0, 'docs': len(docs)}
            for d in docs:
                add(tab[j][y], count(d['text']))
            manifest.setdefault(j, {})[y] = [{'id': d['id'], 'sha256': sha(d['text'])} for d in docs]
    res = {'candidates': len(panel), 'qualifying': len(qual),
           'docs': {y: sum(tab[j][y]['docs'] for j in qual) for y in YEARS},
           'tokens': {y: sum(tab[j][y]['tok'] for j in qual) for y in YEARS},
           'C': {y: round(pooled(qual, tab, y), 2) for y in YEARS},
           'S': {y: round(pooled(qual, tab, y, 'rec'), 2) for y in YEARS}}
    W = pooled(qual, tab, '2026') - pooled(qual, tab, '2021')
    rng = random.Random(SEED)
    boots, b25 = [], []
    for _ in range(DRAWS):
        s = [qual[rng.randrange(len(qual))] for _ in qual]
        boots.append(pooled(s, tab, '2026') - pooled(s, tab, '2021'))
    res['W'] = round(W, 2)
    res['W_ci95'] = [pct(boots, 0.025), pct(boots, 0.975)]
    both = [j for j in qual if tab[j]['2021']['tok'] >= 5 and tab[j]['2026']['tok'] >= 5]
    rose = [j for j in both if tab[j]['2026']['con'] / tab[j]['2026']['tok'] > tab[j]['2021']['con'] / tab[j]['2021']['tok']]
    fell = [j for j in both if tab[j]['2026']['con'] / tab[j]['2026']['tok'] < tab[j]['2021']['con'] / tab[j]['2021']['tok']]
    res['Wj'] = {'journals': len(both), 'rose': len(rose), 'fell': len(fell),
                 'share_rose': round(100 * len(rose) / len(both), 2) if both else None}
    # frame side: per-journal token counts in the two August frames
    ft = {}
    for y in ('2021', '2026'):
        ft[y] = defaultdict(lambda: {'tok': 0, 'rec': 0, 'con': 0})
        for d in FR[y]['docs']:
            add(ft[y][FJ[y][d['id']]['jid']], count(d['text']))
    fr = {}
    for y in ('2021', '2026'):
        all_t = sum(v['tok'] for v in ft[y].values())
        in_t = sum(ft[y][j]['tok'] for j in qual if j in ft[y])
        in_c = sum(ft[y][j]['con'] for j in qual if j in ft[y])
        fr[y] = {'digest_matched': FR[y]['digest_matched'],
                 'C_whole_frame': round(100 * sum(v['con'] for v in ft[y].values()) / all_t, 2),
                 'token_coverage_by_panel': round(100 * in_t / all_t, 2),
                 'records_in_panel_journals': sum(1 for d in FR[y]['docs'] if FJ[y][d['id']]['jid'] in tab),
                 'C_panel_journals_only': round(100 * in_c / in_t, 2) if in_t else None, 'in_t': in_t}
    res['frames'] = fr
    K1 = len(qual) < 30
    res['K1_fired'] = K1
    res['K2_fired'] = abs(res['C']['2021'] - 2.92) > 3
    if not K1:
        w = {y: {j: (ft[y][j]['tok'] if j in ft[y] else 0) / fr[y]['in_t'] for j in qual} for y in ('2021', '2026')}
        r = {y: {j: (100 * tab[j][y]['con'] / tab[j][y]['tok'] if tab[j][y]['tok'] else 0.0) for j in qual}
             for y in ('2021', '2026')}
        comp = sum((w['2026'][j] - w['2021'][j]) * (r['2021'][j] + r['2026'][j]) / 2 for j in qual)
        rate = sum((r['2026'][j] - r['2021'][j]) * (w['2021'][j] + w['2026'][j]) / 2 for j in qual)
        gap = fr['2026']['C_panel_journals_only'] - fr['2021']['C_panel_journals_only']
        res['decomposition'] = {'composition': round(comp, 2), 'rate': round(rate, 2),
                                'composition_share_of_sum': round(100 * comp / (comp + rate), 1) if comp + rate else None,
                                'frame_gap_panel_journals': round(gap, 2),
                                'residual_gap_minus_parts': round(gap - comp - rate, 2),
                                'note': 'journals with no tokens in a year get rate 0 there'}
    p = {}
    p['P1'] = W > 0
    p['P2'] = W < GAP
    p['P3'] = res['W_ci95'][0] > 0 or res['W_ci95'][1] < 0
    lo, hi = sorted([res['C']['2021'], res['C']['2026']])
    p['P4'] = lo < res['C']['2025'] < hi
    p['P5'] = bool(both) and len(rose) / len(both) > 0.5
    p['P6'] = (not K1) and res['decomposition']['composition_share_of_sum'] is not None and res['decomposition']['composition_share_of_sum'] >= 50
    res['predictions_held'] = p
    res['per_journal'] = {j: {y: {k: tab[j][y][k] for k in ('docs', 'tok', 'rec', 'con')} for y in YEARS}
                          | {f'frame{y[2:]}_{k}': (ft[y][j][k] if j in ft[y] else 0)
                             for y in ('2021', '2026') for k in ('tok', 'con')}
                          for j in qual}
    res['seed'], res['draws'], res['fetched_at_utc'] = SEED, DRAWS, P['fetched_at_utc']
    json.dump(res, open(os.path.join(out, 'results.json'), 'w'), indent=1)
    json.dump({'term': P['term'], 'per': P['per'], 'min': P['min'],
               'candidates': {j: {y: panel[j][y]['count'] for y in ('2021', '2026')} | {'qualifies': panel[j]['qualifies']}
                              for j in sorted(panel)},
               'docs': manifest}, open(os.path.join(out, 'panel-manifest.json'), 'w'), indent=0)
    json.dump({y: sorted({v['jid'] for v in FJ[y].values()}) for y in FJ} | {
        'pmid_to_jid': {y: {k: v['jid'] for k, v in FJ[y].items()} for y in FJ}},
        open(os.path.join(out, 'frame-journals.json'), 'w'), indent=0)
    print(json.dumps({k: v for k, v in res.items() if k != 'per_journal'}, indent=1))


if __name__ == '__main__':
    main()
