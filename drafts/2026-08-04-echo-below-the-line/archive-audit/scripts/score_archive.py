"""Score the pre-registered archive audit.

Inputs
  results/clusters.json    the instrument's own published clusters (Stage 0)
  results/candidates.json  Stage A candidate units (mechanical, no judgement)
  evidence/ownership.json  Stage B evidence gate, per unit and per member

Rules, all fixed before any number existed (PREREGISTRATION-ARCHIVE.md; DEVIATIONS.md D1, D2):
  * primary set  = headline clusters whose published domain_count equals their masthead-list
                   length (the instrument truncates masthead lists at 40)
  * a member stays in a confirmed unit only if the ownership source names it (D2.1)
  * candidate units are never merged with one another, even under one operator (D2.2)
  * U = number of distinct publisher units among a cluster's mastheads
  * Q1 = share of primary clusters with U < 3          prediction >= 25 %
  * Q2 = median N/U over primary clusters              prediction >= 2.0
  * Q3 = at least one U < 3 cluster carries no syndication label from the instrument itself

Output: results/scores.json and results/summary.md
"""
import json, os, statistics
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(HERE, 'results')


def load():
    clusters = json.load(open(os.path.join(R, 'clusters.json')))['clusters']
    cands = json.load(open(os.path.join(R, 'candidates.json')))['units']
    ev_path = os.path.join(HERE, 'evidence', 'ownership.json')
    ev = json.load(open(ev_path))['units'] if os.path.exists(ev_path) else []
    return clusters, cands, {e['unit_id']: e for e in ev}


def build_partitions(cands, ev):
    """Three partitions of the domain space, as dicts domain -> unit label.

    candidate  Stage A as computed, no evidence applied
    confirmed  the pre-registered primary: units confirmed by a published ownership source,
               restricted to the members that source names; everything else a singleton
    operator   secondary only: confirmed members regrouped by the named operator, so one owner
               fragmented across several candidate units counts once
    """
    candidate, confirmed, operator = {}, {}, {}
    for g in cands:
        e = ev.get(g['id'])
        named = set()
        accepted = e and e.get('verdict') in ('CONFIRMED', 'SECONDARY')
        if accepted:
            named = {m.strip().lower() for m in e.get('members_named', [])}
        for m in g['members']:
            candidate[m] = g['id'] if g['size'] > 1 else 'solo:' + m
            if accepted and m in named and g['size'] > 1:
                confirmed[m] = g['id']
                operator[m] = 'op:' + e['operator']
            else:
                confirmed[m] = 'solo:' + m
                operator[m] = 'solo:' + m
    return {'candidate': candidate, 'confirmed': confirmed, 'operator': operator}


def units_in(cluster, part):
    return len({part.get(m, 'solo:' + m) for m in cluster['mastheads']})


def score_set(clusters, part):
    rows = []
    for c in clusters:
        u = units_in(c, part)
        rows.append({'date': c['date'], 'slot': c['slot'], 'N': c['domain_count'],
                     'n_mastheads': c['n_mastheads'], 'U': u,
                     'ratio': c['n_mastheads'] / u,
                     'below_threshold': u < (c['min_domains'] or 3),
                     'syndication_label': c['syndication_label'],
                     'phrase': c['phrase']})
    below = [r for r in rows if r['below_threshold']]
    return {
        'n_clusters': len(rows),
        'n_below_threshold': len(below),
        'share_below_threshold': (len(below) / len(rows)) if rows else None,
        'median_ratio': statistics.median([r['ratio'] for r in rows]) if rows else None,
        'mean_ratio': (sum(r['ratio'] for r in rows) / len(rows)) if rows else None,
        'max_ratio': max([r['ratio'] for r in rows], default=None),
        'n_below_unlabelled': sum(1 for r in below if not r['syndication_label']),
        'labels_among_below': dict(Counter(r['syndication_label'] for r in below)),
        'rows': rows,
    }


def main():
    clusters, cands, ev = load()
    parts = build_partitions(cands, ev)

    head = [c for c in clusters if c['slot'] == 'headline']
    primary = [c for c in head if c['domain_count'] == c['n_mastheads']]
    truncated = [c for c in head if c['domain_count'] != c['n_mastheads']]

    out = {'sets': {}, 'predictions': {}, 'inputs': {
        'n_clusters_total': len(clusters), 'n_headline': len(head),
        'n_primary': len(primary), 'n_truncated_headline': len(truncated),
        'n_candidate_units': len(cands),
        'n_units_with_evidence': len(ev),
        'evidence_verdicts': dict(Counter(e['verdict'] for e in ev.values())),
    }}
    for pname, part in parts.items():
        out['sets'][pname] = {
            'primary': score_set(primary, part),
            'truncated_headline_lower_bound': score_set(truncated, part),
            'all_clusters': score_set(clusters, part),
        }

    p = out['sets']['confirmed']['primary']
    q1 = p['share_below_threshold']
    q2 = p['median_ratio']
    q3_n = p['n_below_unlabelled']
    out['predictions'] = {
        'Q1': {'statement': 'share of primary headline clusters with U < 3 is >= 25 %',
               'value': q1, 'threshold': 0.25, 'holds': (q1 is not None and q1 >= 0.25)},
        'Q2': {'statement': 'median mastheads/U over primary headline clusters is >= 2.0',
               'value': q2, 'threshold': 2.0, 'holds': (q2 is not None and q2 >= 2.0)},
        'Q3': {'statement': 'at least one U < 3 cluster carries no syndication label',
               'value': q3_n, 'threshold': 1, 'holds': q3_n >= 1,
               'note': 'refuted means the instrument already flags every failing cluster'},
    }
    h1, h2 = out['predictions']['Q1']['holds'], out['predictions']['Q2']['holds']
    out['band'] = ('Band 1' if (h1 and h2) else 'Band 2' if (h1 or h2) else 'Band 3')
    if not out['predictions']['Q3']['holds']:
        out['band'] += ' + Band 4'
    json.dump(out, open(os.path.join(R, 'scores.json'), 'w'), indent=1)
    return out


if __name__ == '__main__':
    o = main()
    i = o['inputs']
    print(f"clusters {i['n_clusters_total']}  headline {i['n_headline']}  primary {i['n_primary']}  "
          f"truncated {i['n_truncated_headline']}")
    print(f"evidence: {i['n_units_with_evidence']} units  {i['evidence_verdicts']}")
    for pname in ('candidate', 'confirmed', 'operator'):
        s = o['sets'][pname]['primary']
        print(f"  {pname:10s} primary: U<3 in {s['n_below_threshold']}/{s['n_clusters']} "
              f"({(s['share_below_threshold'] or 0)*100:.1f} %)  median ratio "
              f"{s['median_ratio']:.2f}  max {s['max_ratio']:.2f}  unlabelled among below "
              f"{s['n_below_unlabelled']}")
    for k, v in o['predictions'].items():
        print(f"  {k}: {v['value']} vs {v['threshold']} -> {'HOLDS' if v['holds'] else 'REFUTED'}")
    print("BAND:", o['band'])
