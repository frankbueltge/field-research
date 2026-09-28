#!/usr/bin/env python3
"""Twenty Augusts — session 173, 2026-09-28. Run 09-23's hand-over rule over five Augusts.

    analyse.py <raw_dir> <data_dir>

Imports handover.py (09-23) and lattice.py (09-27) unchanged. Writes only counts,
identifiers and digests. No model, no network.
"""
import hashlib
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'a-number-you-cannot-check'))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'range-of-the-method'))
import handover as H                                               # noqa: E402
import lattice as L                                                # noqa: E402

YEARS = [2006, 2011, 2016, 2021, 2026]
PIN = os.path.join(ROOT, 'artifacts/2026-09-23-a-number-you-cannot-check/data/corpora.json')
SEED, DRAWS = 20260928, 2000


def sha(t):
    return hashlib.sha256(t.encode('utf-8')).hexdigest()


def per_doc(text):
    toks = H.analyse(text)
    v = [t['verdict'] for t in toks]
    wo = [L.verdict('round-or-trunc', val, dec, pair)
          for val, dec, pair, _, _ in L.tokens(text, 40, 'words-only', '.;!?', 'greedy')]
    return {'tokens': len(v), 'recomputable': sum(x != 'not_recomputable' for x in v),
            'consistent': v.count('consistent'), 'complement': v.count('complement'),
            'inconsistent': v.count('inconsistent'),
            'tokens_wo': len(wo), 'recomputable_wo': sum(x != 'not_recomputable' for x in wo),
            'chars': len(text)}


def rates(rows):
    t = sum(r['tokens'] for r in rows)
    return {'S': 100 * sum(r['recomputable'] for r in rows) / t,
            'C': 100 * sum(r['consistent'] for r in rows) / t,
            'S_wo': 100 * sum(r['recomputable_wo'] for r in rows) / sum(r['tokens_wo'] for r in rows),
            'D': 100 * sum(r['consistent'] > 0 for r in rows) / len(rows)}


def main():
    raw, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    pin = {d['id']: d['sha256'] for d in json.load(open(PIN))['M']['docs']}
    rng = random.Random(SEED)
    years, manifest = {}, {}
    for y in YEARS:
        src = json.load(open(os.path.join(raw, f'{y}.json'), encoding='utf-8'))
        docs = src['docs']
        audit = None
        if y == 2026:
            ok = [d for d in docs if pin.get(d['id']) == sha(d['text'])]
            audit = {'pinned': len(pin), 'returned': len(docs), 'digest_matched': len(ok)}
            docs = ok
        rows = [per_doc(d['text']) for d in docs]
        tot = {k: sum(r[k] for r in rows) for k in rows[0]}
        pt = rates(rows)
        boots = {k: [] for k in pt}
        for _ in range(DRAWS):
            b = rates([rows[rng.randrange(len(rows))] for _ in rows])
            for k in pt:
                boots[k].append(b[k])
        ci = {k: [round(sorted(v)[int(0.025 * DRAWS)], 2), round(sorted(v)[int(0.975 * DRAWS) - 1], 2)]
              for k, v in boots.items()}
        years[str(y)] = {'documents': len(rows), 'esearch_count': src['esearch_count'],
                         'fetched_at_utc': src['fetched_at_utc'], 'term': src['term'],
                         'totals': tot, 'rates': {k: round(v, 2) for k, v in pt.items()}, 'ci95': ci,
                         'pct_per_abstract': round(tot['tokens'] / len(rows), 3),
                         'chars_per_abstract': round(tot['chars'] / len(rows), 1),
                         'docs_with_a_percentage': sum(r['tokens'] > 0 for r in rows),
                         'audit_2026': audit}
        ds = [{'id': d['id'], 'sha256': sha(d['text'])} for d in docs]
        manifest[str(y)] = {'documents': len(ds),
                            'corpus_digest': hashlib.sha256(''.join(d['sha256'] for d in ds).encode()).hexdigest(),
                            'docs': ds}
        print(y, len(rows), tot['tokens'], tot['recomputable'], tot['consistent'], tot['inconsistent'],
              years[str(y)]['rates'], ci)
    json.dump({'seed': SEED, 'draws': DRAWS, 'years': years}, open(os.path.join(out, 'years.json'), 'w'), indent=1)
    json.dump(manifest, open(os.path.join(out, 'corpora.json'), 'w'), indent=0)


if __name__ == '__main__':
    main()
