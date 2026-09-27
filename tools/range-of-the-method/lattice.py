#!/usr/bin/env python3
"""The range of the method — session 172, 2026-09-27.

Runs 09-23's hand-over rule (tools/a-number-you-cannot-check/handover.py, imported) across
the lattice of its own registered choices, as fixed in
artifacts/2026-09-27-the-range-of-the-method/PREREGISTRATION.md §2.

    lattice.py <raw_dir> <out_dir>

<raw_dir> holds abstracts.json (M), abstracts_A.json (A) and field.json (F), all outside the
repository (protocol §7). Only counts, identifiers and digests are written to <out_dir>.
No model, no network.
"""
import hashlib
import html
import itertools
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'a-number-you-cannot-check'))
import handover as H                                               # noqa: E402

PIN = os.path.join(ROOT, 'artifacts/2026-09-23-a-number-you-cannot-check/data/corpora.json')
ADJ = os.path.join(ROOT, 'artifacts/2026-09-23-a-number-you-cannot-check/data/adjudication.json')

WINDOWS = [10, 20, 40, 80, None]                      # None = whole sentence
CONNECTIVES = {
    'all+slash': (['out of', 'of the', 'of', 'among', 'in'], True),
    'no-in': (['out of', 'of the', 'of', 'among'], True),
    'no-in-among': (['out of', 'of the', 'of'], True),
    'words-only': (['out of', 'of the', 'of', 'among', 'in'], False),
    'slash-only': ([], True),
}
SPLITS = {'.;!?': r'[.;!?]\s+', '.!?': r'[.!?]\s+', 'newline': None}
PAIRINGS = ['greedy', 'many']
TEXTS = ['fetched', 'decoded']
MATCHERS = ['round', 'round-or-trunc', 'last-digit', 'half-point']
BASE = {'window': 40, 'conn': 'all+slash', 'split': '.;!?', 'pairing': 'greedy',
        'text': 'fetched', 'match': 'round-or-trunc'}


def word_re(conns):
    alt = '|'.join(c.replace(' ', r'\s+') for c in conns)
    return re.compile(r'(?<![\w.,])(' + H.INTNUM + r')\s+(?:' + alt + r')\s+(' + H.INTNUM +
                      r')(?!\.\d)(?![\w])', re.I)


def sentences(text, split):
    for line in H.normalise(text).split('\n'):
        if split is None:
            if line.strip():
                yield line
            continue
        start = 0
        for m in re.finditer(split, line):
            piece = line[start:m.end()]
            if piece.strip():
                yield piece
            start = m.end()
        tail = line[start:]
        if tail.strip():
            yield tail


def pairs_in(sentence, pct_num_spans, rxs):
    """handover.pairs_in with the regex list as a parameter; otherwise identical."""
    found = []
    for rx in rxs:
        for m in rx.finditer(sentence):
            k, n = H._val(m.group(1)), H._val(m.group(2))
            if k != int(k) or n != int(n):
                continue
            k, n = int(k), int(n)
            if not (0 <= k <= n and n >= 2):
                continue
            a, b = (m.start(1), m.end(1)), (m.start(2), m.end(2))
            if any(s <= a[0] < e or s <= b[0] < e for s, e in pct_num_spans):
                continue
            found.append({'span': (m.start(), m.end()), 'k': k, 'n': n})
    seen, uniq = set(), []
    for p in sorted(found, key=lambda x: x['span']):
        if p['span'] in seen:
            continue
        seen.add(p['span'])
        uniq.append(p)
    return uniq


def tokens(text, window, conn, split, pairing):
    """Every percentage token: (value, decimals, pair-or-None, sentence-index, token-text)."""
    conns, slash = CONNECTIVES[conn]
    rxs = ([word_re(conns)] if conns else []) + ([H.PAIR_SLASH_RE] if slash else [])
    out = []
    for si, sent in enumerate(sentences(text, SPLITS[split])):
        pcts = [{'span': (m.start(), m.end()), 'ns': (m.start(1), m.end(1)),
                 'value': H._val(m.group(1)), 'dec': H._decimals(m.group(1)),
                 'text': m.group(0), 'pair': None} for m in H.PCT_RE.finditer(sent)]
        if not pcts:
            continue
        prs = pairs_in(sent, [p['ns'] for p in pcts], rxs)
        lim = float('inf') if window is None else window
        cands = sorted((H.gap(p['span'], q['span']), i, j)
                       for i, p in enumerate(pcts) for j, q in enumerate(prs)
                       if H.gap(p['span'], q['span']) <= lim)
        used_p, used_q = set(), set()
        for g, i, j in cands:
            if i in used_p or (pairing == 'greedy' and j in used_q):
                continue
            used_p.add(i)
            used_q.add(j)
            pcts[i]['pair'] = (prs[j]['k'], prs[j]['n'])
        for p in pcts:
            out.append((p['value'], p['dec'], p['pair'], si, p['text']))
    return out


def matches(kind, p, d, k, n):
    exp = 100.0 * k / n
    if kind == 'round':
        return abs(p - H._round_half_up(exp, d)) < 1e-9
    if kind == 'round-or-trunc':
        return H._matches(p, d, k, n)
    if kind == 'last-digit':
        return abs(p - exp) <= 10 ** (-d) + 1e-9
    return abs(p - exp) <= 0.5 + 1e-9


def verdict(kind, value, dec, pair):
    if pair is None:
        return 'not_recomputable'
    k, n = pair
    if matches(kind, value, dec, k, n):
        return 'consistent'
    if matches(kind, value, dec, n - k, n):
        return 'complement'
    return 'inconsistent'


def load(raw):
    pin = json.load(open(PIN))
    corpora = {}
    m = json.load(open(os.path.join(raw, 'abstracts.json'), encoding='utf-8'))
    a = json.load(open(os.path.join(raw, 'abstracts_A.json'), encoding='utf-8'))
    f = {d['id']: d['text'] for d in json.load(open(os.path.join(raw, 'field.json'),
                                                    encoding='utf-8'))['docs']}
    audit = {}
    for key, src in (('M', m), ('A', a), ('F', f)):
        docs, miss = [], []
        for d in pin[key]['docs']:
            t = src.get(d['id'])
            if t is not None and hashlib.sha256(t.encode()).hexdigest() == d['sha256']:
                docs.append((d['id'], t))
            else:
                miss.append(d['id'])
        corpora[key] = docs
        audit[key] = {'pinned': len(pin[key]['docs']), 'digest_matched': len(docs),
                      'not_matched': miss}
    return corpora, audit


def main():
    raw, out = sys.argv[1], sys.argv[2]
    corpora, audit = load(raw)
    real = [r for r in json.load(open(ADJ))['M'] if r['verdict'] == 'real']
    screens, flags, per_doc_base = [], [], {}
    for window, conn, split, pairing, text in itertools.product(
            WINDOWS, CONNECTIVES, SPLITS, PAIRINGS, TEXTS):
        spec = {'window': window, 'conn': conn, 'split': split, 'pairing': pairing, 'text': text}
        row = dict(spec)
        toks_by_corpus = {}
        for key, docs in corpora.items():
            all_t, per_doc = [], []
            for did, t in docs:
                tt = tokens(html.unescape(t) if text == 'decoded' else t,
                            window, conn, split, pairing)
                all_t.extend((did,) + x for x in tt)
                per_doc.append((len(tt), sum(1 for x in tt if x[2] is not None)))
            toks_by_corpus[key] = all_t
            n = len(all_t)
            r = sum(1 for x in all_t if x[3] is not None)
            row[key] = {'tokens': n, 'recomputable': r, 'rate': round(100.0 * r / n, 4)}
            if all(spec[k] == BASE[k] for k in spec):
                per_doc_base[key] = per_doc
        screens.append(row)
        for kind in MATCHERS:
            frow = dict(spec, match=kind)
            for key, all_t in toks_by_corpus.items():
                v = [verdict(kind, x[1], x[2], x[3]) for x in all_t]
                frow[key] = {c: v.count(c) for c in ('consistent', 'complement', 'inconsistent')}
            kept = 0
            for e in real:
                for x in toks_by_corpus['M']:
                    if (x[0] == e['doc'] and x[5].replace(' ', '') == e['printed'].replace(' ', '')
                            and x[3] == tuple(e['pair'])
                            and verdict(kind, x[1], x[2], x[3]) == 'inconsistent'):
                        kept += 1
                        break
            frow['known_real_errors_flagged'] = kept
            flags.append(frow)
        print(json.dumps({k: row[k] for k in spec} | {c: row[c]['rate'] for c in corpora}),
              file=sys.stderr)
    rng = random.Random(20260927)
    boot = {}
    for key, per_doc in per_doc_base.items():
        rates = []
        for _ in range(2000):
            s = [per_doc[rng.randrange(len(per_doc))] for _ in per_doc]
            rates.append(100.0 * sum(r for _, r in s) / max(1, sum(n for n, _ in s)))
        rates.sort()
        boot[key] = {'low': round(rates[49], 4), 'high': round(rates[1949], 4),
                     'resamples': 2000, 'seed': 20260927}
    json.dump({'audit': audit, 'base': BASE, 'known_real_errors': len(real),
               'bootstrap_base': boot, 'screens': screens, 'flags': flags},
              open(os.path.join(out, 'lattice.json'), 'w'), indent=0)


if __name__ == '__main__':
    main()
