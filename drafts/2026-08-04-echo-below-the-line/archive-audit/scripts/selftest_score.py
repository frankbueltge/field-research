"""Selftest for the archive-audit scoring, over fixtures worked out by hand.

Run before the real scoring, and again after. Every expected value below was computed on paper
first; if the code disagrees with the paper, the code is wrong until shown otherwise.
"""
import json, os, sys, tempfile, shutil, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CHECKS = []


def check(name, got, want):
    ok = got == want or (isinstance(want, float) and isinstance(got, float) and abs(got - want) < 1e-9)
    CHECKS.append((name, ok, got, want))


def load_module(root):
    spec = importlib.util.spec_from_file_location('score_archive', os.path.join(root, 'scripts', 'score_archive.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def fixture(tmp):
    os.makedirs(os.path.join(tmp, 'results'), exist_ok=True)
    os.makedirs(os.path.join(tmp, 'evidence'), exist_ok=True)
    os.makedirs(os.path.join(tmp, 'scripts'), exist_ok=True)
    shutil.copy(os.path.join(HERE, 'score_archive.py'), os.path.join(tmp, 'scripts', 'score_archive.py'))

    clusters = [
        # C1 untruncated: 4 mastheads, a1+a2 confirmed together, b1 and c1 alone -> U = 3, not below
        {'date': '2026-01-01', 'slot': 'headline', 'domain_count': 4, 'n_mastheads': 4,
         'mastheads': ['a1.com', 'a2.com', 'b1.com', 'c1.com'], 'min_domains': 3,
         'syndication_label': None, 'phrase': 'p1'},
        # C2 untruncated: 3 mastheads, all in the confirmed unit -> U = 1, below threshold, unlabelled
        {'date': '2026-01-02', 'slot': 'headline', 'domain_count': 3, 'n_mastheads': 3,
         'mastheads': ['a1.com', 'a2.com', 'a3.com'], 'min_domains': 3,
         'syndication_label': None, 'phrase': 'p2'},
        # C3 untruncated: 6 mastheads, unit + 1 outsider -> U = 2, below, and labelled
        {'date': '2026-01-03', 'slot': 'headline', 'domain_count': 6, 'n_mastheads': 6,
         'mastheads': ['a1.com', 'a2.com', 'a3.com', 'a4.com', 'a5.com', 'z1.com'],
         'min_domains': 3, 'syndication_label': 'wire/chain syndication', 'phrase': 'p3'},
        # C4 TRUNCATED headline (40 published, 3 listed) -> excluded from primary
        {'date': '2026-01-04', 'slot': 'headline', 'domain_count': 40, 'n_mastheads': 3,
         'mastheads': ['a1.com', 'a2.com', 'a3.com'], 'min_domains': 3,
         'syndication_label': None, 'phrase': 'p4'},
        # C5 runner-up -> not in the primary set either
        {'date': '2026-01-05', 'slot': 'runner_up', 'domain_count': 3, 'n_mastheads': 3,
         'mastheads': ['a1.com', 'a2.com', 'b1.com'], 'min_domains': 3,
         'syndication_label': None, 'phrase': 'p5'},
    ]
    cands = [
        # one candidate unit of five, of which the source names only four (a5 is split off, D2.1)
        {'id': 'cand-a', 'size': 5, 'members': ['a1.com', 'a2.com', 'a3.com', 'a4.com', 'a5.com']},
        # a second candidate unit under the SAME operator: never merged in the primary (D2.2)
        {'id': 'cand-b', 'size': 2, 'members': ['b1.com', 'b2.com']},
        # a unit with no evidence at all: split back to singletons
        {'id': 'cand-z', 'size': 2, 'members': ['z1.com', 'z2.com']},
        {'id': 'cand-c1.com', 'size': 1, 'members': ['c1.com']},
    ]
    ev = {'units': [
        {'unit_id': 'cand-a', 'operator': 'Acme Group', 'verdict': 'CONFIRMED',
         'members_named': ['a1.com', 'a2.com', 'a3.com', 'a4.com']},
        {'unit_id': 'cand-b', 'operator': 'Acme Group', 'verdict': 'CONFIRMED',
         'members_named': ['b1.com', 'b2.com']},
        {'unit_id': 'cand-z', 'operator': 'none found', 'verdict': 'HOSTING ARTEFACT',
         'members_named': []},
    ]}
    json.dump({'clusters': clusters}, open(os.path.join(tmp, 'results', 'clusters.json'), 'w'))
    json.dump({'units': cands}, open(os.path.join(tmp, 'results', 'candidates.json'), 'w'))
    json.dump(ev, open(os.path.join(tmp, 'evidence', 'ownership.json'), 'w'))


def main():
    tmp = tempfile.mkdtemp()
    fixture(tmp)
    m = load_module(tmp)
    m.HERE = tmp
    m.R = os.path.join(tmp, 'results')
    o = m.main()

    check('primary set excludes truncated and runner-up', o['inputs']['n_primary'], 3)
    check('truncated headline counted', o['inputs']['n_truncated_headline'], 1)

    conf = o['sets']['confirmed']['primary']
    # C1 -> {cand-a, cand-b, solo:c1} = 3 ; C2 -> {cand-a} = 1 ; C3 -> {cand-a, solo:a5, solo:z1} = 3
    check('C1 U', conf['rows'][0]['U'], 3)
    check('C2 U', conf['rows'][1]['U'], 1)
    check('C3 U (a5 split off, z1 split off)', conf['rows'][2]['U'], 3)
    check('below threshold count', conf['n_below_threshold'], 1)
    check('share below', conf['share_below_threshold'], 1 / 3)
    # ratios 4/3, 3/1, 6/3 -> median 2.0
    check('median ratio', conf['median_ratio'], 2.0)
    check('unlabelled among below', conf['n_below_unlabelled'], 1)

    cand = o['sets']['candidate']['primary']
    # candidate partition ignores evidence: C3 -> {cand-a, solo:z1... } z1 in cand-z (size 2) = 2 units
    check('C3 U under candidates', cand['rows'][2]['U'], 2)
    check('C1 U under candidates', cand['rows'][0]['U'], 3)

    op = o['sets']['operator']['primary']
    # operator partition merges cand-a and cand-b: C1 -> {op:Acme, solo:c1} = 2
    check('C1 U under operator merge', op['rows'][0]['U'], 2)
    check('C3 U under operator merge', op['rows'][2]['U'], 3)

    check('Q1 holds at 1/3 >= 0.25', o['predictions']['Q1']['holds'], True)
    check('Q2 holds at 2.0 >= 2.0', o['predictions']['Q2']['holds'], True)
    check('Q3 holds (one unlabelled)', o['predictions']['Q3']['holds'], True)
    check('band', o['band'], 'Band 1')

    # a fixture where every below-threshold cluster IS labelled -> Q3 refuted, Band 4 appended
    ev2 = json.load(open(os.path.join(tmp, 'evidence', 'ownership.json')))
    cl = json.load(open(os.path.join(tmp, 'results', 'clusters.json')))
    cl['clusters'][1]['syndication_label'] = 'wire/chain syndication'
    json.dump(cl, open(os.path.join(tmp, 'results', 'clusters.json'), 'w'))
    o2 = m.main()
    check('Q3 refuted when all below are labelled', o2['predictions']['Q3']['holds'], False)
    check('Band 4 appended', o2['band'].endswith('Band 4'), True)

    shutil.rmtree(tmp)
    bad = [c for c in CHECKS if not c[1]]
    for name, ok, got, want in CHECKS:
        print(('  ok   ' if ok else '  FAIL ') + f'{name}: got {got!r} want {want!r}')
    print(f"{len(CHECKS)-len(bad)}/{len(CHECKS)} selftest assertions pass")
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
