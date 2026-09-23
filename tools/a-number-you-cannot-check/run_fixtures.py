#!/usr/bin/env python3
"""Run the hand-written fixtures against the rule. Session 168, 2026-09-23."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from handover import analyse                                        # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def run(verbose=True):
    cases = json.load(open(os.path.join(HERE, 'fixtures.json'), encoding='utf-8'))['cases']
    failures = []
    for c in cases:
        got = analyse(c['text'])
        want = c['tokens']
        ok = len(got) == len(want)
        if ok:
            for g, w in zip(got, want):
                if abs(g['value'] - w['value']) > 1e-9 or g['verdict'] != w['verdict'] \
                        or (g['pair'] or None) != (w['pair'] or None):
                    ok = False
                    break
        if not ok:
            failures.append((c['id'], [(g['value'], g['verdict'], g['pair']) for g in got],
                             [(w['value'], w['verdict'], w['pair']) for w in want]))
    if verbose:
        for fid, got, want in failures:
            print(f'  FAIL {fid}\n    got  {got}\n    want {want}')
        print(f'{len(cases)} fixtures, {len(failures)} failed')
    return len(cases), failures


if __name__ == '__main__':
    n, f = run()
    sys.exit(1 if f else 0)
