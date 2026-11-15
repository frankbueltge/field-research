"""Study 78 (session 276, 2026-11-15) — the paper's two readings, both on handoffs from the Atelier.

Usage: python3 -I analyse78.py <path to mongodump_full_snapshot/>

(1) Handoff ho-2026-11-15-atelier-8: of the harmed who wrote a first report in the press, how many are the press
    writing about itself? Reads check78/harmed-press.json (one reading per case, with its reason) and
    check77/press-sample.json, and restates check 77's estimate with the press-on-itself cases set apart.
(2) Handoff ho-2026-11-15-atelier-9: who entered the first report of each incident. Recounts, from the snapshot's
    own `submitters` field, how many first reports one submitter entered, by the year of the incident. The
    submitter is not named here: the count is about the record's intake, not about a person.

Writes results78.json and data78.js. No report text is read into or written to this repository. Standard library only.
No predictions were written: the five texts of part (1) had been read in session 275 and again before this script.
"""
import csv, json, os, sys, collections, math

csv.field_size_limit(10**9)
HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = sys.argv[1]
SNAP_SHA = 'c10825888fb716bb91a67319f3292324a7f962f68e6e82326aedd4d694a7aad0'
J = lambda *p: json.load(open(os.path.join(HERE, *p)))
R77 = J('results77.json')
PS = J('check77', 'press-sample.json')
HP = J('check78', 'harmed-press.json')
D = json.loads(open(os.path.join(HERE, 'data75.js')).read().split('=', 1)[1].rstrip(';\n'))
ROW = {r[0]: r for r in D['rows']}


def wilson(k, n, z=1.96):
    p = k / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    d = 1 + z * z / n
    return (c - h) / d, (c + h) / d


# ---------------------------------------------------------------- (1) the harmed in the press, and the press itself
drawn_harmed = sorted(int(x['id']) for x in PS['items'] if x['code'] == 'harmed')
cases = {x['id']: x for x in HP['items']}
assert sorted(i for i, x in cases.items() if x['in_draw']) == drawn_harmed == R77['press']['harmed_ids']
itself = sorted(i for i in drawn_harmed if cases[i]['press_itself'])
outside = sorted(i for i in drawn_harmed if not cases[i]['press_itself'])
pop, n = R77['press']['population'], R77['press']['drawn']
lo, hi = wilson(len(outside), n)
est = lambda p: round(p * pop)
floor = R77['A']['final_harmed']
part1 = {
    'drawn': n, 'population': pop, 'harmed_in_draw': drawn_harmed,
    'press_itself_in_draw': itself, 'harmed_outside_the_press_in_draw': outside,
    'outside_pct': round(100 * len(outside) / n, 1), 'outside_ci95_pct': [round(100 * lo, 1), round(100 * hi, 1)],
    'outside_estimated_in_class': est(len(outside) / n), 'outside_estimated_in_class_ci': [est(lo), est(hi)],
    'whole_record_estimate_by_the_codebook': R77['whole_record']['estimate'],
    'whole_record_estimate_by_the_codebook_ci': R77['whole_record']['estimate_ci'],
    'whole_record_estimate_without_the_press_itself': floor + est(len(outside) / n),
    'whole_record_estimate_without_the_press_itself_ci': [floor + est(lo), floor + est(hi)],
    'atelier_case_outside_the_draw': [i for i, x in cases.items() if not x['in_draw']],
    'press_itself_all_found': sorted(i for i, x in cases.items() if x['press_itself']),
    'harmed_found_in_the_press': sorted(cases),
}
part1['whole_record_estimate_without_the_press_itself_pct'] = round(
    100 * part1['whole_record_estimate_without_the_press_itself'] / R77['all_first_reports'], 1)

# ---------------------------------------------------------------- (2) who entered each first report


def rows(name):
    with open(os.path.join(SNAP, name), newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


inc = rows('incidents.csv')
rep = {}
for r in rows('reports.csv'):
    try:
        rep[int(r['report_number'])] = r
    except ValueError:
        pass


def first_report(nums):  # the rule of analyse75.py, unchanged
    cand = [rep[x] for x in nums if x in rep]
    if not cand:
        return None

    def key(r):
        try:
            e = float(r['epoch_date_published'])
        except ValueError:
            e = None
        return (e is None, e if e is not None else 0, int(r['report_number']))
    return sorted(cand, key=key)[0]


sub = {}
for r in inc:
    fr = first_report(json.loads(r['reports']) if r['reports'] else [])
    if fr:
        sub[int(r['incident_id'])] = fr['submitters']
assert len(sub) == R77['all_first_reports']
cnt = collections.Counter(sub.values())
top, top_n = cnt.most_common(1)[0]
alone = {i for i, s in sub.items() if s == top}
by_year = {}
for i in sub:
    y = ROW[i][1]
    k = 'before 2018' if (y is None or y < 2018) else str(y)
    x = by_year.setdefault(k, [0, 0])
    x[1] += 1
    x[0] += i in alone
kinds = collections.Counter(ROW[i][2] for i in alone)
part2 = {
    'first_reports': len(sub), 'submitter_values': len(cnt),
    'top_alone': top_n, 'top_alone_pct': round(100 * top_n / len(sub), 1),
    'second': cnt.most_common(2)[1][1], 'third': cnt.most_common(3)[2][1],
    'top_with_others': sum(c for s, c in cnt.items() if top in s),
    'by_year': by_year,
    'top_by_first_reporter_class': dict(kinds),
    'atelier_figure': 1059,
    'atelier_rule': 'the earliest-submitted report of each incident; this count takes the earliest-published, the rule of analyse75.py',
    'top_ids': sorted(alone),
}

res = {'study': 78, 'session': 276, 'date': '2026-11-15', 'cycle': 15, 'programme_step': 3,
       'snapshot_sha256': SNAP_SHA, 'snapshot_fetched': '2026-11-15, a fourth time, matched by hash before reading',
       'press_itself': part1, 'intake': part2}
json.dump(res, open(os.path.join(HERE, 'results78.json'), 'w'), indent=1)
open(os.path.join(HERE, 'data78.js'), 'w').write('window.D78=' + json.dumps(res, separators=(',', ':')) + ';\n')
print(json.dumps({k: v for k, v in part1.items() if 'estimate' in k or 'outside' in k}, indent=0))
print(json.dumps({k: v for k, v in part2.items() if k != 'top_ids'}, indent=0))
