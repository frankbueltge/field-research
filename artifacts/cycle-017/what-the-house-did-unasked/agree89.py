#!/usr/bin/env python3
"""Reading 89 (session 287): compares this reading's join of each deed to its mending (join89.json) with the Atelier's
(`data/sort.json` of *On Its Own Account* at ulysses aa8a96e), pair by pair, after join89.py had coded every pair.

Usage: python3 agree89.py <path to the Atelier's sort.json>
Writes agree89.json: agreement on the three classes of CODEBOOK89.md (count and Cohen's kappa), agreement on the five
codes, the lines each reading finds the mending taking out, and every disagreement.
"""
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
CLASS = {'same': 'joined', 'lines': 'joined', 'name': 'joined', 'file': 'file', 'log': 'log'}
CODE = {'same_commit': 'same', 'lines': 'lines', 'name': 'name', 'file': 'file', 'log_only': 'log'}


def kappa(pairs):
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n / n
    return round((po - pe) / (1 - pe), 3) if pe < 1 else 1.0


def main():
    at = json.loads(Path(sys.argv[1]).read_text())['act']['deeds']
    A = {(int(d['row']), int(d['n'])): d for d in at}
    mine = json.loads((HERE / 'join89.json').read_text())['pairs']
    rows, by_pair, dis = [], {}, []
    for p in mine:
        a = A.get((p['row'], p['deed']))
        if a is None or a.get('join') in (None, 'none'):
            dis.append({'row': p['row'], 'deed': p['deed'], 'field': p['code'], 'atelier': None,
                        'why': 'not a mended pair in the Atelier record'})
            continue
        same_repair = p['repair'].startswith(a['repair'][1]) if a.get('repair') else False
        a_lines = sum(n for _, n in a.get('evidence') or []) if a['join'] == 'lines' else None
        rows.append((p, a, same_repair, a_lines))
        by_pair[f"{p['row']}|{p['deed']}"] = a['join']
        if p['class'] != CLASS[a['join']] or not same_repair:
            dis.append({'row': p['row'], 'deed': p['deed'], 'field': p['code'], 'atelier': a['join'],
                        'same_repair': same_repair})
    cls = [(p['class'], CLASS[a['join']]) for p, a, _, _ in rows]
    code = [(CODE[p['code']], a['join']) for p, a, _, _ in rows]
    both_lines = [(p['lines_taken_out'], al) for p, a, _, al in rows if p['code'] == 'lines' and a['join'] == 'lines']
    res = {'reading': 89, 'session': 287, 'atelier_commit': 'aa8a96e', 'pairs': len(mine), 'compared': len(rows),
           'same_repair': sum(s for _, _, s, _ in rows),
           'class_agree': sum(a == b for a, b in cls), 'class_kappa': kappa(cls),
           'code_agree': sum(a == b for a, b in code), 'code_kappa': kappa(code),
           'code_table': {f'{a}|{b}': n for (a, b), n in sorted(Counter(code).items())},
           'both_lines': len(both_lines), 'lines_equal': sum(a == b for a, b in both_lines),
           'lines_field_total': sum(a for a, _ in both_lines), 'lines_atelier_total': sum(b for _, b in both_lines),
           'disagreements': dis}
    res['P144'] = 'held' if res['class_agree'] >= 70 else 'failed'
    (HERE / 'agree89.json').write_text(json.dumps({'results': res, 'by_pair': by_pair}, indent=1,
                                                  ensure_ascii=False) + '\n')
    print(json.dumps(res, indent=1))


if __name__ == '__main__':
    main()
