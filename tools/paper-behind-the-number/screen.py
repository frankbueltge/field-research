#!/usr/bin/env python3
"""The mechanical screen and its null, per PREREGISTRATION §4. Session 170, 2026-09-25.

HIT for a unit in a text: an integer k stands immediately before the printed value in
parentheses — `k (p)`, `k (p%)`, `k/n (p%)` — AND some integer n in the same text gives
100·k/n equal to p rounded half-up or truncated at p's printed decimals.
NULL: each unit is screened against the text of a DIFFERENT paper (a derangement, fixed seed).
"""
import json, os, random, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'a-number-you-cannot-check'))
from handover import _matches  # noqa: E402  (09-23's own rounding test, unchanged)

INT_RE = re.compile(r'(?<![\d.,])\d{1,3}(?:,\d{3})+(?![\d.])|(?<![\d.,])\d+(?![\d.])')


def num_str(printed):
    return re.match(r'[\d,]+(?:\.\d+)?', printed).group(0)


def ints_in(text):
    return {int(m.group(0).replace(',', '')) for m in INT_RE.finditer(text)}


def hit(unit, text, ints=None):
    p = num_str(unit['printed'])
    rx = re.compile(r'(?<![\d.,])(\d{1,3}(?:,\d{3})+|\d+)(?:\s*/\s*(\d+))?\s*[(\[]\s*' + re.escape(p) + r'\s*%?\s*[)\],;]')
    ks = [(int(m.group(1).replace(',', '')), m.group(2)) for m in rx.finditer(text)]
    if not ks:
        return False
    ints = ints if ints is not None else ints_in(text)
    for k, n_inline in ks:
        cands = [int(n_inline)] if n_inline else sorted(i for i in ints if i >= max(k, 2))
        for n in cands:
            if n >= max(k, 1) and n >= 2 and _matches(unit['value'], unit['decimals'], k, n):
                return True
    return False


def derangement(items, seed):
    rnd = random.Random(seed)
    while True:
        perm = items[:]
        rnd.shuffle(perm)
        if all(a != b for a, b in zip(items, perm)):
            return perm


def run(W, seed=20260925):
    u = json.load(open(os.path.join(W, 'units.json')))
    units = u['units_list']
    docs = sorted({x['doc'] for x in units})
    texts = {d: open(os.path.join(W, 'txt', d + '.txt')).read() for d in docs}
    ints = {d: ints_in(t) for d, t in texts.items()}
    other = dict(zip(docs, derangement(docs, seed)))
    rows = []
    for x in units:
        o = other[x['doc']]
        rows.append({"uid": x['uid'], "true": hit(x, texts[x['doc']], ints[x['doc']]),
                     "null": hit(x, texts[o], ints[o]), "null_doc": o})
    return rows


if __name__ == "__main__":
    W = sys.argv[1]
    rows = run(W)
    json.dump(rows, open(os.path.join(W, 'screen.json'), 'w'), indent=1)
    n = len(rows)
    t = sum(r['true'] for r in rows); z = sum(r['null'] for r in rows)
    print(f"units {n}: true-paper hits {t} ({100*t/n:.2f}%), null hits {z} ({100*z/n:.2f}%)")
