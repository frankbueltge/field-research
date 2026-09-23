#!/usr/bin/env python3
"""Mutation test of the hand-over rule (R-6). Session 168, 2026-09-23.

Each mutation is a single textual change to handover.py, applied by anchor against the
file's own text. A mutation whose anchor is not found exactly once is a FAILED MUTATION
and is reported as such -- bad test 11 of 2026-09-22 was a tamper that corrupted nothing.
A mutation no fixture catches is a hole in the fixtures and is reported, not hidden.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = open(os.path.join(HERE, 'handover.py'), encoding='utf-8').read()
FIX = json.load(open(os.path.join(HERE, 'fixtures.json'), encoding='utf-8'))['cases']

MUTATIONS = [
    ('M01 window widened to 200',        'WINDOW = 40', 'WINDOW = 200'),
    ('M02 window narrowed to 5',         'WINDOW = 40', 'WINDOW = 5'),
    ('M03 k<=n check dropped',           'if not (0 <= k <= n and n >= 2):', 'if not (0 <= k and n >= 2):'),
    ('M04 n>=2 check dropped',           'if not (0 <= k <= n and n >= 2):', 'if not (0 <= k <= n and n >= 1):'),
    ('M05 A-2 exclusion dropped',        "if any(s <= a[0] < e or s <= b[0] < e for s, e in pct_num_spans):   # A-2\n                continue",
                                          'pass'),
    ('M06 one-to-one dropped',           'if i in used_p or j in used_q:', 'if i in used_p:'),
    ('M07 truncation reading dropped',   "return abs(p - _round_half_up(exp, d)) < 1e-9 or abs(p - _trunc(exp, d)) < 1e-9",
                                          'return abs(p - _round_half_up(exp, d)) < 1e-9'),
    ('M08 rounding reading dropped',     "return abs(p - _round_half_up(exp, d)) < 1e-9 or abs(p - _trunc(exp, d)) < 1e-9",
                                          'return abs(p - _trunc(exp, d)) < 1e-9'),
    ('M09 complement reading dropped',   "elif _matches(p['value'], p['decimals'], n - k, n):\n            p['verdict'] = 'complement'",
                                          "elif False:\n            p['verdict'] = 'complement'"),
    ('M10 thousands separators dropped', "return float(s.replace(',', ''))", "return float(s.split(',')[0])"),
    ('M11 sentence splitting dropped',   "for m in re.finditer(r'[.;!?]\\s+', line):", "for m in re.finditer(r'(?!x)x', line):"),
    ('M12 A-3 reverted, table split',    "line = line.replace('|', ' ')            # A-3: a table row is one sentence",
                                          "line = line.replace('|', '\\n')"),
    ('M13 markdown emphasis kept',       "line = re.sub(r'\\*+', '', line)", 'pass'),
    ('M14 among/in links dropped',       "(?:out\\s+of|of\\s+the|of|among|in)", '(?:out\\s+of|of\\s+the|of)'),
    ('M15 slash pairs dropped',          'for rx in (PAIR_WORD_RE, PAIR_SLASH_RE):', 'for rx in (PAIR_WORD_RE,):'),
    ('M16 decimals always zero',         "return len(s.split('.')[1]) if '.' in s else 0", 'return 0'),
    ('M17 the word percent dropped',     "\\s*(%|percent\\b)", '\\s*(%)'),
    ('M18 tie-break reversed',           'cands.sort()', 'cands.sort(reverse=True)'),
    ('M19 of the dropped',               "(?:out\\s+of|of\\s+the|of|among|in)", '(?:out\\s+of|of|among|in)'),
    ('M20 link syntax not stripped',     "text = LINK_RE.sub(r'\\1', text)", 'pass'),
]


def verdicts(analyse, case):
    got = analyse(case['text'])
    return [(round(g['value'], 6), g['verdict'], tuple(g['pair']) if g['pair'] else None) for g in got]


def expected(case):
    return [(round(t['value'], 6), t['verdict'], tuple(t['pair']) if t['pair'] else None)
            for t in case['tokens']]


def main():
    ns = {}
    exec(compile(SRC, 'handover.py', 'exec'), ns)
    base = ns['analyse']
    baseline_ok = all(verdicts(base, c) == expected(c) for c in FIX)
    print(f'baseline: {len(FIX)} fixtures, all pass = {baseline_ok}')
    rows, holes, broken = [], [], []
    for name, old, new in MUTATIONS:
        count = SRC.count(old)
        if count != 1:
            broken.append((name, count))
            rows.append({'mutation': name, 'applied': False, 'anchor_occurrences': count,
                         'caught_by': []})
            continue
        mutant_src = SRC.replace(old, new, 1)
        assert mutant_src != SRC, name
        mns = {}
        try:
            exec(compile(mutant_src, 'mutant.py', 'exec'), mns)
            mut = mns['analyse']
            caught = []
            for c in FIX:
                try:
                    ok = verdicts(mut, c) == expected(c)
                except Exception:                                   # noqa: BLE001
                    ok = False
                if not ok:
                    caught.append(c['id'])
        except Exception as exc:                                    # noqa: BLE001
            caught = [f'<mutant failed to load: {type(exc).__name__}>']
        rows.append({'mutation': name, 'applied': True, 'anchor_occurrences': 1,
                     'caught_by': caught})
        if not caught:
            holes.append(name)
    for r in rows:
        mark = 'NOT APPLIED' if not r['applied'] else (f"caught by {len(r['caught_by'])}"
                                                       if r['caught_by'] else 'SURVIVED')
        print(f"  {r['mutation']:<36} {mark}")
    print(f'{len(MUTATIONS)} mutations, {len(broken)} anchors not unique, {len(holes)} survived')
    json.dump({'baseline_all_fixtures_pass': baseline_ok, 'mutations': rows,
               'anchors_not_unique': broken, 'survived': holes},
              open(os.path.join(HERE, 'mutation-results.json'), 'w', encoding='utf-8'),
              indent=2, ensure_ascii=False)
    return 0


if __name__ == '__main__':
    sys.exit(main())
