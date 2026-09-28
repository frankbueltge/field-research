#!/usr/bin/env python3
"""Twenty Augusts — exploratory analysis (A-2, after the primary results were seen).

    explore_analyse.py <raw_dir> <data_dir>

For all seven frames: the primary measures, a bootstrap that resamples JOURNALS rather than
documents (clusters), the share of the frame held by its ten largest journals, and C with the
agreeing percentages of the frame's single largest contributing journal removed.
"""
import collections
import hashlib
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyse import per_doc, rates, sha                            # noqa: E402

FRAMES = ['2006', '2011', '2016', '2021', '2025', '2026', '2026-today']
SEED, DRAWS = 20260928, 2000


def main():
    raw, out = sys.argv[1], sys.argv[2]
    jn = json.load(open(os.path.join(raw, 'journals.json')))
    rng = random.Random(SEED)
    res, ids = {}, {}
    for f in FRAMES:
        src = json.load(open(os.path.join(raw, f'{f}.json'), encoding='utf-8'))
        docs = src['docs']
        ids[f] = [d['id'] for d in docs]
        rows = [dict(per_doc(d['text']), j=jn.get(d['id'], '?'), id=d['id']) for d in docs]
        pt = rates(rows)
        byj = collections.defaultdict(list)
        for r in rows:
            byj[r['j']].append(r)
        js = list(byj)
        cb = []
        for _ in range(DRAWS):
            samp = []
            for _ in js:
                samp += byj[js[rng.randrange(len(js))]]
            if sum(r['tokens'] for r in samp) and sum(r['tokens_wo'] for r in samp):
                cb.append(rates(samp)['C'])
        cb.sort()
        top = collections.Counter(r['j'] for r in rows).most_common(10)
        cons = collections.Counter()
        for r in rows:
            cons[r['j']] += r['consistent']
        lead, lead_n = cons.most_common(1)[0]
        rest = [r for r in rows if r['j'] != lead]
        res[f] = {'documents': len(rows), 'esearch_count': src['esearch_count'],
                  'fetched_at_utc': src['fetched_at_utc'],
                  'rates': {k: round(v, 2) for k, v in pt.items()},
                  'C_ci95_journal_clustered': [round(cb[int(0.025 * len(cb))], 2),
                                               round(cb[int(0.975 * len(cb)) - 1], 2)],
                  'journals': len(js), 'top10_share_of_records': round(100 * sum(n for _, n in top) / len(rows), 1),
                  'top3': top[:3],
                  'largest_contributor_of_agreeing': {'journal': lead, 'agreeing': lead_n,
                                                      'of_total': sum(cons.values()),
                                                      'records': len(byj[lead])},
                  'C_without_that_journal': round(rates(rest)['C'], 2),
                  'pct_per_abstract': round(sum(r['tokens'] for r in rows) / len(rows), 3),
                  'corpus_digest': hashlib.sha256(''.join(sha(d['text']) for d in docs).encode()).hexdigest()}
        print(f, json.dumps(res[f]))
    ov = len(set(ids['2026']) & set(ids['2026-today']))
    manifest = {f: [{'id': i, 'journal': jn.get(i)} for i in ids[f]] for f in ('2025', '2026-today')}
    json.dump({'registered': 'A-2, after the primary results were seen',
               'overlap_2026_pinned_vs_today': ov, 'frames': res},
              open(os.path.join(out, 'explore.json'), 'w'), indent=1)
    json.dump(manifest, open(os.path.join(out, 'explore-ids.json'), 'w'), indent=0)
    print('overlap', ov)


if __name__ == '__main__':
    main()
