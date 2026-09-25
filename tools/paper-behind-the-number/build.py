#!/usr/bin/env python3
"""Assemble the artifact's data/ from the session's working files. Session 170, 2026-09-25.

Inputs (outside the repository): refetch.json, fulltext-manifest.json, units.json, screen.json,
reading.tsv (the hand verdicts, written in session). Outputs (inside it): identifiers, digests,
verdicts and estimates only — no abstract or full text beyond one quoted sentence per read unit.
"""
import json, math, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'a-number-you-cannot-check'))
from handover import _matches  # noqa: E402

W, ART = sys.argv[1], sys.argv[2]
D = os.path.join(ART, 'data')
SEED = 20260925
STRICT_FLAG = '[strict: NR]'
# Where a NOT RECOVERED unit's counts are, assigned by hand from the reading notes.
NR_CLASS = {
    'supplement_or_figure': [12, 13, 16, 26, 27, 28, 41, 50, 56, 75, 107],
    'n_printed_k_not': [66, 68, 106],
    'printed_denominator_does_not_reproduce': [62, 84],
    'no_counts_in_the_text': [14, 32, 33, 58, 63, 101],
}
NR_OF = {s: c for c, ss in NR_CLASS.items() for s in ss}


def wilson(k, n, z=1.959963985):
    if n == 0:
        return [None, None]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(100 * (c - h), 2), round(100 * (c + h), 2)]


def pct(k, n):
    return round(100 * k / n, 2)


def main():
    ref = json.load(open(os.path.join(W, 'refetch.json')))
    man = json.load(open(os.path.join(W, 'fulltext-manifest.json')))
    u = json.load(open(os.path.join(W, 'units.json')))
    scr = {r['uid']: r for r in json.load(open(os.path.join(W, 'screen.json')))}
    units = u['units_list']

    json.dump({"note": "Corpus M of 2026-09-23 re-fetched 2026-09-25 by PMID; digest_match compares the "
                       "rebuilt abstract with the pinned SHA-256. Full texts: PMC E-utilities efetch, JATS XML, "
                       "kept outside the repository; sha256 is over the returned <article> element.",
               "refetched_at_utc": ref['fetched_at_utc'], "fulltext_fetched_at_utc": man['fetched_at_utc'],
               "abstracts": ref['rows'], "fulltexts": man['rows']},
              open(os.path.join(D, 'corpus.json'), 'w'), indent=1)

    json.dump({"note": "Every percentage token in a full-text paper's abstract that 09-23's rule calls "
                       "not_recomputable, with the mechanical screen's verdict on its own paper (true) and "
                       "on a different paper (null, fixed derangement).",
               "seed": SEED, "sample_index": u['sample_index'],
               "units": [{"uid": x['uid'], "doc": x['doc'], "printed": x['printed'],
                          "value": x['value'], "decimals": x['decimals'],
                          "screen_true": scr[x['uid']]['true'], "screen_null": scr[x['uid']]['null'],
                          "null_doc": scr[x['uid']]['null_doc']} for x in units]},
              open(os.path.join(D, 'units.json'), 'w'), indent=1)

    reading = []
    for line in open(os.path.join(W, 'reading.tsv')):
        s, verdict, k, n, note = line.rstrip('\n').split('\t')
        i = int(s[1:])
        x = units[u['sample_index'][i]]
        row = {"s": i, "uid": x['uid'], "doc": x['doc'], "printed": x['printed'],
               "abstract_sentence": x['sentence'][:320], "verdict": verdict,
               "k": int(k) if k else None, "n": int(n) if n else None, "note": note,
               "strict_nr": STRICT_FLAG in note, "nr_class": NR_OF.get(i)}
        if row['k'] is not None:
            row['recomputed'] = round(100 * row['k'] / row['n'], 4)
            row['matches'] = _matches(x['value'], x['decimals'], row['k'], row['n'])
        reading.append(row)
    reading.sort(key=lambda r: r['s'])
    json.dump({"note": "One verdict per sampled unit, written by this practice in session 170 from the "
                       "full text; no person read any of it. RC recovered-consistent, RI recovered-"
                       "inconsistent, NR not recovered, NA not a count proportion (PREREGISTRATION §3).",
               "reading": reading}, open(os.path.join(D, 'reading.json'), 'w'), indent=1, ensure_ascii=False)

    # ---- estimates
    V = {v: [r for r in reading if r['verdict'] == v] for v in ('RC', 'RI', 'NR', 'NA')}
    cp = [r for r in reading if r['verdict'] != 'NA']
    rec = [r for r in cp if r['verdict'] in ('RC', 'RI')]
    strict = [r for r in rec if not r['strict_nr']]
    sens_ri = [r for r in cp if 'Sensitivity: coded RI' in r['note']]

    rnd = random.Random(SEED)
    docs = sorted({r['doc'] for r in reading})
    by = {d: [r for r in reading if r['doc'] == d] for d in docs}
    boots = []
    for _ in range(10000):
        pick = [rnd.choice(docs) for _ in docs]
        rr = [r for d in pick for r in by[d] if r['verdict'] != 'NA']
        if rr:
            boots.append(100 * sum(r['verdict'] in ('RC', 'RI') for r in rr) / len(rr))
    boots.sort()

    n_units = len(units)
    t = sum(x['screen_true'] for x in json.load(open(os.path.join(D, 'units.json')))['units'])
    z = sum(x['screen_null'] for x in json.load(open(os.path.join(D, 'units.json')))['units'])
    sampled = {r['uid']: r for r in reading}
    su = [x for x in json.load(open(os.path.join(D, 'units.json')))['units'] if x['uid'] in sampled]
    conf = {"screen_hit_and_recovered": 0, "screen_hit_not_recovered": 0,
            "screen_miss_and_recovered": 0, "screen_miss_not_recovered": 0}
    for x in su:
        recd = sampled[x['uid']]['verdict'] in ('RC', 'RI')
        key = ("screen_hit" if x['screen_true'] else "screen_miss") + ("_and_recovered" if recd else "_not_recovered")
        conf[key] += 1

    abstracts = ref['rows']
    body = sum(r['has_body'] for r in man['rows'])
    est = {
        "availability": {"abstracts_refetched": len(abstracts),
                         "digest_match": sum(r['digest_match'] for r in abstracts),
                         "with_pmcid": sum(bool(r['pmcid']) for r in abstracts),
                         "fulltext_returned": sum(r['returned'] for r in man['rows']),
                         "fulltext_with_body": body, "rate": pct(body, len(abstracts)),
                         "rate_95": wilson(body, len(abstracts))},
        "population": {"papers_with_body": u['papers_with_body'], "papers_with_a_unit": u['papers_with_a_unit'],
                       "units": n_units},
        "sample": {"units": len(reading), "papers": len(docs),
                   "verdicts": {v: len(V[v]) for v in V},
                   "not_a_count_proportion": {"k": len(V['NA']), "n": len(reading),
                                              "rate": pct(len(V['NA']), len(reading)),
                                              "rate_95": wilson(len(V['NA']), len(reading))}},
        "recovered": {"k": len(rec), "n": len(cp), "rate": pct(len(rec), len(cp)),
                      "rate_95": wilson(len(rec), len(cp)),
                      "paper_cluster_bootstrap_95": [round(boots[249], 2), round(boots[9749], 2)],
                      "bootstrap_resamples": len(boots)},
        "recovered_strict": {"k": len(strict), "n": len(cp), "rate": pct(len(strict), len(cp)),
                             "rate_95": wilson(len(strict), len(cp)),
                             "note": "counts as NR every unit whose k needed summation across arms or was "
                                     "stated only as an empty complement"},
        "recovered_if_header_n_taken": {"k": len(rec) + len(sens_ri), "n": len(cp),
                                        "rate": pct(len(rec) + len(sens_ri), len(cp)),
                                        "added_as_RI": [r['s'] for r in sens_ri]},
        "not_recovered_by_class": {c: len(ss) for c, ss in NR_CLASS.items()},
        "inconsistent": {"k": len(V['RI']), "of_recovered": len(rec),
                         "units": [r['s'] for r in V['RI']]},
        "screen": {"population_true_hits": t, "population_null_hits": z, "units": n_units,
                   "true_rate": pct(t, n_units), "true_rate_95": wilson(t, n_units),
                   "null_rate": pct(z, n_units), "null_rate_95": wilson(z, n_units),
                   "sample_confusion": conf},
    }
    json.dump(est, open(os.path.join(D, 'estimates.json'), 'w'), indent=1)
    print(json.dumps(est, indent=1))


if __name__ == "__main__":
    main()
