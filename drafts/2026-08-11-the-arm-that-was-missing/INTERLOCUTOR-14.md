# Interlocutor 14 — session 122, increment 13 (`DRIFT-122.md`)

**Convened as the adversary under `PROTOCOL.md` ("Voices"), two obligations in one pass: (a) an
attempt to refute the core claim, blocking; (b) the hostile critique, non-blocking, published
with the work.**

**State reviewed.** The brief names `95ab278`. The working tree is at **`cba5505`**, two commits
later (`7ab84c6` — memory, `REQUESTS.md`, and a fifty-line dated addendum to
`deliverable/LIMITS.md`; `cba5505` — the dossier). `DRIFT-122.md` itself is byte-identical between
the two (`git diff 95ab278 HEAD -- DRIFT-122.md` is empty), so everything below is run against the
tree as it stands and one finding turns on the later commit; it is marked where it does.

Unless stated otherwise, every command below is run from
`drafts/2026-08-11-the-arm-that-was-missing/`. Wall-clock at review: `date -u` →
`Sun Aug 16 00:27:55 UTC 2026`.

---

# (a) Refutation attempt

## Verdict: **THE CORE CLAIM SURVIVES, NARROWED.**

## The core objection, in one paragraph

The measurement half of this claim is real and I could not break it: the panel reproduces, the
shipped table reproduces from the run files, the twenty-four crossers are twenty-four and all
twenty-four are retrievable, and every horizon figure in §4 comes out of a re-run to the last
digit. **The repair half does not survive as stated.** Claim (iii) — "the repair puts BOTH figures
in front of the caller, computed on the caller's own list, with the reference-time figure named as
the defensible one" — is false in two reproducible and entirely ordinary cases: a caller whose
list postdates the reference table gets *one* figure, the one this session has just declared
indefensible, with no drift line and no mention that the other reading was attempted and dropped;
and a caller whose list is *partly* newer gets two figures computed over **different subsets of
their own list**, with the difference between two denominators printed as "arithmetic drift ...
over N day(s) of frozen reference" and no `n` beside either. Claim (iv) — "measured rather than
picked" — survives only as "computed after a comparand was picked": the same script, comparing the
design half against the bookkeeping half's *effect on the very quantity the drift measures*
instead of against its largest single cell, returns a crossover of **1 day**, not 26; against the
mean cell it returns **10**. The document names the comparand honestly in §4 and then hard-codes
the most favourable of the family into the tool as `STALE_AFTER_DAYS = 26` and calls the threshold
measured. And the justification given for the reference-time figure — "it is the only reading in
which the ages and the table's clock agree" — is *false for the reference table this bundle
actually ships*, whose declared clock is the one V1 proved wrong by 2.6803 days, and which
`presence_check.py` cannot tell apart from the corrected one because it never reads
`ages_computed_at_utc` and never records which baseline file it was handed.

---

## Findings

### 1. **BLOCKING** — the tool prints one figure, not two, whenever the caller's list postdates the table; and the figure it prints is the one this session calls indefensible

`drift()` returns `None` when `expectation(rebanded(rows, t_decl), baseline)` is falsy.
`rebanded()` maps any age ≤ 0 to `band = None`, and `expectation()` returns `None` on an empty
histogram. So a list every one of whose videos was created after the table's reference time — the
single most likely list a stranger brings to a tool whose reference table is a year old — takes the
`else` branch of the printer and receives the now-aged expectation, unlabelled, with no drift line,
no staleness figure beside it, and no statement that the defensible reading could not be computed.
The claim "prints both figures, computed on the caller's own list" (§5, and the same sentence in
the `LIMITS.md` addendum and in the module docstring) is not true of this case.

```
cd deliverable/tools && python3 - <<'EOF'
import sys, calendar, time; sys.path.insert(0, '.')
import presence_check as P
b, _ = P.load_baseline('../reference-baseline-CORRECTED-2026-08-16.json')
td = calendar.timegm(time.strptime(b['t_ref_utc'], '%Y-%m-%dT%H:%M:%SZ'))
mk = lambda d: str((int(td - d*86400) << 32) | 1)
new = [mk(-50-i*10) for i in range(5)]          # created AFTER the reference time
now = td + 400*86400
rows = [{'vid': v, 'band': P.band_of((now-(int(v)>>32))/P.YEAR_S)} for v in new]
print('bands at now:', P.band_hist(rows))
print('drift ->', P.drift(rows, b, now))
EOF
```
→ `bands at now: {'0-1y': 5}` · `drift -> None`

This is this arc's own catalogued failure mode — *a check that cannot find its subject returning
clean* — with the sign flipped: a check that cannot find its subject returning **nothing**, and the
caller never learning that it ran. No assertion in section 8 of `selftest_presence_check.py` covers
it (`grep -n "after the reference\|negative age\|created after" deliverable/tools/selftest_presence_check.py`
→ no match).

### 2. **BLOCKING** — on a mixed list the two "figures on the caller's own list" are computed on different lists, and the printed drift is mostly a change of denominator

Five old identifiers plus five created after `t_ref`: the reference-time figure is computed over 5
units, the now figure over 10, and the tool prints the difference as drift in percentage points
"over 400.0 day(s) of frozen reference". Neither `n` appears in `frozen_reference_drift`, though
`expectation()` computes `n_dated` and `drift()` throws it away. The two histograms *are* in the
output, so the information is technically recoverable by a caller who sums two dicts; the printed
sentence, which is what a caller reads, is not recoverable at all.

```
cd deliverable/tools && python3 - <<'EOF'
import sys, calendar, time; sys.path.insert(0, '.')
import presence_check as P
b, _ = P.load_baseline('../reference-baseline-CORRECTED-2026-08-16.json')
td = calendar.timegm(time.strptime(b['t_ref_utc'], '%Y-%m-%dT%H:%M:%SZ'))
mk = lambda d: str((int(td - d*86400) << 32) | 1)
vs = [mk(800+i*300) for i in range(5)] + [mk(-50-i*10) for i in range(5)]
now = td + 400*86400
rows = [{'vid': v, 'band': P.band_of((now-(int(v)>>32))/P.YEAR_S)} for v in vs]
d = P.drift(rows, b, now)
print('n at ref =', sum(d['age_histogram_at_the_reference_time'].values()),
      '| n at now =', sum(d['age_histogram_at_now'].values()),
      '| printed drift_pp = %+.4f' % d['drift_pp'])
EOF
```
→ `n at ref = 5 | n at now = 10 | printed drift_pp = -4.8752`

A −4.88 pp "arithmetic drift" of which none is arithmetic drift. The fix is two lines: carry
`n_dated` from both `expectation()` calls into the returned dict, and refuse to print a `drift_pp`
when they differ.

### 3. **BLOCKING** — the stated reason the reference-time figure is defensible is false for the reference table the bundle ships, and the tool cannot tell the two tables apart

`which_one_is_defensible` says the reference-time reading "is the only reading in which the ages
and the table's clock agree." For `deliverable/reference-baseline.json` — the file
`MANIFEST.json`, `README.md` and `LETTER.md` name, and the only one a receiver following the bundle
would load — the table's bands were computed at `2026-08-11T11:24:06Z` and `t_ref_utc` declares
`2026-08-14T03:43:47Z`. That is exactly V1. Handed that file, `drift()` ages the caller's list at a
clock the table's own cells do not use and calls the result the defensible one.

The corrected file carries `ages_computed_at_utc` precisely so this could be detected. Nothing
reads it:

```
grep -rn "ages_computed_at_utc\|shelf_life" deliverable/tools/presence_check.py \
       deliverable/tools/selftest_presence_check.py
```
→ no match (both keys appear only in `build_deliverable.py`, lines 419–420).

And the output records no baseline path at all, so a reader of a result file cannot recover which
table produced it:

```
python3 -c "import json;d=json.load(open('functional-test-122.json'));print(sorted(d.keys()))"
```
→ `list` is recorded; no `baseline` key. I had to identify the table by recomputation:

```
python3 - <<'EOF'
import sys, re, calendar, time; sys.path.insert(0, 'deliverable/tools')
import presence_check as P
vids = [ (re.search(r'/video/(\d+)', s) or re.search(r'(\d{1,25})', s)).group(1)
         for s in map(str.strip, open('receiver-list.txt'))
         if s and not s.startswith('#') ]
t = calendar.timegm(time.strptime('2026-08-16T00:16:00Z', '%Y-%m-%dT%H:%M:%SZ'))
rows = [{'vid': v, 'band': P.band_of((t-(int(v)>>32))/P.YEAR_S)} for v in vids]
for p in ('deliverable/reference-baseline.json',
          'deliverable/reference-baseline-CORRECTED-2026-08-16.json',
          'presence-baseline.json'):
    b, _ = P.load_baseline(p)
    print(p, repr(P.expectation(rows, b)['expected_absent_rate']))
EOF
```
→ `reference-baseline.json 0.13592886879136862` · `…-CORRECTED-… 0.13592625615723686` ·
`presence-baseline.json 0.1376986368862619`, against `functional-test-122.json`'s
`0.13592625615723686`. The live run used the corrected table. Nothing in the artifact says so.
Three reference tables now coexist in this draft and disagree in the third decimal; the tool's own
`--baseline` default (`presence-baseline.json`) is the one that disagrees most, and is the one
Verifier 121 finding 5 already recorded as not existing in the bundle layout.

`memory/downstream-commitments.md` condition 9, quoted in §6 of the document as binding on this
work — *any figure names the version that produced it* — is honoured for the tool and broken for
the table.

### 4. **BLOCKING** — "26 days" is one member of a family that runs from 1 day to 26 days, and the member chosen is the one most favourable to leaving the design defect alone

`drift_122.py` sets `worst_bookkeeping_pp = max(|Δrate|)` over the six bands (0.1826 pp, the 5y+
cell) and steps the design half until it exceeds it. But the design half's drift is measured on the
**pooled expectation**, and the bookkeeping half's effect on that same pooled expectation is
0.0002 pp — because, as §2 itself proves, no `absent` count moves. Comparing like with like gives a
crossover of **one day**.

```
python3 - <<'EOF'
import drift_122 as D
days = D.load_days('2026-08-14T23:59:59Z'); units = D.build_units(days); newest = days[-1]
tf, td = D.t(days[0]['utc_start']), D.t(newest['utc_start'])
tbl_f, _ = D.table_at(units, newest, tf); tbl_t, _ = D.table_at(units, newest, td)
panel = [u['vid'] for u in units.values() if u['created'] is not None]
E = lambda t, tbl: D.expectation_from(D.hist_at(panel, t), tbl)['expected_absent_rate']
deltas = [abs(tbl_t[b]['absent_rate']-tbl_f[b]['absent_rate'])*100 for b in tbl_f]
cands = {'max band delta (the one used)': max(deltas),
         'mean band delta': sum(deltas)/len(deltas),
         'effect on the printed expectation': abs(100*(E(td,tbl_t)-E(tf,tbl_f))),
         'effect on the pooled rate': 0.0}
b0 = E(td, tbl_t)
for name, th in cands.items():
    for dd in range(0, 1200):
        if 100*abs(E(td+dd*86400, tbl_t) - b0) > th:
            print(f'{name:36s} {th:7.4f} pp -> {dd:3d} days'); break
EOF
```
→
```
max band delta (the one used)         0.1826 pp ->  26 days
mean band delta                       0.0634 pp ->  10 days
effect on the printed expectation     0.0002 pp ->   1 days
effect on the pooled rate             0.0000 pp ->   1 days
```

§4 does name its comparand ("the bookkeeping half's worst cell of 0.1826 pp"), so this is not
concealment. But the sensitivity is not published, the number that goes into the tool is the one
that lets the tool stay silent longest, and neither `DRIFT-122.md` nor the `LIMITS.md` addendum
tells a reader that a differently-but-equally-defensibly defined crossover is 1 day. **The claim
"measured rather than picked" is not sustainable as written.** What is measured is a step count.
What is picked is what it is stepping toward.

The operational content of the change is `30 → 26` in one comparison
(`git diff 483bd92 95ab278 -- deliverable/tools/presence_check.py | grep -n "age_d > "`): the
warning now fires four days earlier than the round number it replaced.

### 5. **BLOCKING** — the selftest assertion that certifies the threshold as measured tests a literal

```
grep -n "not a round number" -A1 deliverable/tools/selftest_presence_check.py
```
→ `check_true("the staleness threshold is the measured one, not a round number",
pc.STALE_AFTER_DAYS == 26, pc.STALE_AFTER_DAYS)`

This assertion passes identically whether 26 was computed by `drift_122.py` or typed. Nothing in
the suite reads `drift-122.json`. The same pattern is one file over: the corrected reference
table's `shelf_life.measured_drift_pp_by_days_after_t_ref` is a **hard-coded literal dict** in
`build_deliverable.py` (lines 425–427), not read from `drift-122.json` and not asserted against it,
so a rebuild on a longer panel silently ships session-122 drift figures beside a session-123 table.

```
grep -n "measured_drift_pp_by_days_after_t_ref" -A3 build_deliverable.py
```

This is the failure mode this arc published an erratum for eight days ago (E1, session 121: *the
time was typed, not read*), reappearing as a number typed into a repair whose whole subject is
numbers that quietly stop matching their source.

### 6. **BLOCKING (on any shipping state) — the "measured, not picked" threshold is measured on a population it is not applied to, and on the one real external list the warning it fires is false**

`STALE_AFTER_DAYS` is derived from the arc's own 3,613-unit panel. It is applied to whatever list
the caller brings. On the receiver's eleven — the one external list this arc has — the drift at the
moment the warning fires is **−0.0037 pp**, fifty times smaller than the 0.1826 pp the warning
names, and it is *negative*, so the sentence "staleness outweighs the worst bookkeeping error this
table has ever carried" is not merely imprecise but wrong for that caller. The tool has the
caller's own drift in hand at that instant (`out["frozen_reference_drift"]["drift_pp"]`) and warns
off a constant instead.

```
cd deliverable/tools && python3 - <<'EOF'
import sys, re, calendar, time; sys.path.insert(0, '.')
import presence_check as P
b, _ = P.load_baseline('../reference-baseline-CORRECTED-2026-08-16.json')
td = calendar.timegm(time.strptime(b['t_ref_utc'], '%Y-%m-%dT%H:%M:%SZ'))
vids = [(re.search(r'/video/(\d+)', s) or re.search(r'(\d{1,25})', s)).group(1)
        for s in map(str.strip, open('../../receiver-list.txt')) if s and not s.startswith('#')]
for dd in (0, 26, 27, 60, 90):
    now = td + dd*86400
    rows = [{'vid': v, 'band': P.band_of((now-(int(v)>>32))/P.YEAR_S)} for v in vids]
    print(f'day {dd:3d}  drift {P.drift(rows,b,now)["drift_pp"]:+.4f} pp   '
          f'warning fires: {dd > P.STALE_AFTER_DAYS}')
EOF
```
→ `day 26 drift -0.0037 pp warning fires: False` · `day 27 drift -0.0037 pp warning fires: True`

### 7. **NOT BLOCKING, but it corrodes §2** — the correction moves a published column that §2 omits and §6 declines to analyse, by up to +51.5 %

`FIGURES.md` §2 publishes six columns per age band. The sixth is *"spread across all measured
days"*, sourced from `expectation.json → across_day_stability`. §2 of `DRIFT-122.md` tabulates n,
absent, and rate — and not the spread. §6 discloses that the across-day figures now sit on a
different partition and states that "the difference has **not** been analysed and no claim rests on
it here."

```
cd deliverable && python3 - <<'EOF'
import json
a = json.load(open('expectation.json'))['across_day_stability']
b = json.load(open('expectation-CORRECTED-2026-08-16.json'))['across_day_stability']
for k in a:
    ra, rb = 100*a[k]['range'], 100*b[k]['range']
    print(f'{k:10s} {ra:6.4f} pp -> {rb:6.4f} pp   {(rb-ra)/ra*100:+6.1f}%' if ra else k)
EOF
```
→ `2-3y −25.8 %` · `3-4y −22.5 %` · `4-5y +12.2 %` · **`5y+ 0.3545 → 0.5371 pp, +51.5 %`** ·
pooled unchanged. Confirmed in the artifact: `deliverable/FIGURES.md:27` reads `0.35 pp`,
`deliverable/FIGURES-CORRECTED-2026-08-16.md:27` reads `0.54 pp`.

A claim does rest on it. It is printed in the bundle's own tables page, and
`memory/claims.md` already carries **"THE PUBLISHED ACROSS-DAY SPREAD IS INFLATED 2.35× … Withdrawn
as published"** from session 120. The one downstream family this arc has already had to withdraw
once is the one family this session declines to look at, in a document whose core claim is that the
correction "changes no conclusion". The two sentences — *changes no conclusion* and *the difference
has not been analysed* — cannot both be load-bearing. The honest form is: **changes no conclusion
among the things checked, and one published column moved by half again and was not checked.**

### 8. **NOT BLOCKING** — the self-audit paragraph publishes three counts that the tool does not return for the file it audits

§2's disposition paragraph says *"Pass 1 audited 60 numbers and left **11 unmatched**"* and *"Pass 2
flagged 13 statements"*, and then rests a claim on the eleven: *"all eleven are the rounded
mantissas and exponents of the four gradient rows above."*

```
python3 prose_vs_json.py DRIFT-122.md 2>&1 | grep -E "pass 1|pass 2"
```
→ `pass 1 — 65 numbers audited, 16 not found in any JSON of this draft`
→ `pass 2 — 15 claims whose FORM is the form all three published failures took`

The document says the run happened "before it was committed", so I reconstructed the pre-insertion
state by deleting the disposition paragraph (lines 88–96) and re-running: `63 / 14 / 13`. Pass 2's
13 matches that state. **Pass 1's 60 and 11 match neither state.** And "eleven" cannot be right for
any version containing the four-row gradient table, because that table alone accounts for
**fourteen** flagged values (four on line 74, four on 75, four on 76, two on 77 — count them in the
tool's own output).

The *characterisation* survives — all 16 unmatched values are still that family, and I confirmed
each against `deliverable/gradient-test.json` and its corrected twin. The counts do not. This is a
typed number inside the paragraph whose sole function is to certify that no number in the document
was typed.

Related and reproducible: the paragraph's one verified count *is* verified. I re-derived it from
the primary run file rather than from `drift-122.json`:

```
python3 - <<'EOF'
import json
cross = {c['vid'] for c in json.load(open('drift-122.json'))
         ['half_one_bookkeeping']['units_changing_band']}
run = json.load(open('ledger/run-2026-08-14T0343Z.json'))
corr = {(c['run_file'], str(c['vid'])): c
        for c in json.load(open('ledger/corrections.json'))['corrections']}
from collections import Counter
st = {}
for o in run['observations']:
    v, s = str(o['vid']), o['state']
    c = corr.get(('ledger/run-2026-08-14T0343Z.json', v))
    if c and s == c['state_in_run_file']: s = c['corrected_state']
    st[v] = s
print(len(cross), Counter(st[v] for v in cross))
EOF
```
→ `24 Counter({'RETRIEVABLE': 24})`. **The "24 of 24" claim holds.**

### 9. **NOT BLOCKING** — the defensible figure is the one without an interval

Before v0.3.0 the printed expectation carried its Wilson bracket. In the `if dr:` branch it does
not, and `frozen_reference_drift` stores no `expected_lo`/`expected_hi` for either reading. So the
figure the tool now leads with and names defensible is the only one in the output with no
uncertainty attached, while the interval survives on the now-aged figure the same tool calls an
extrapolation this arc has withdrawn.

```
git diff 483bd92 95ab278 -- deliverable/tools/presence_check.py | grep -n "expected_lo"
python3 -c "import json;print(sorted(json.load(open('functional-test-122.json'))['frozen_reference_drift']))"
```

Condition I10 of the session-120 gauntlet was *"say what the expectation brackets are"*
(`CONDITIONS-120.md`, Interlocutor conditions). It is now half-unsaid for the leading figure.

### 10. **NOT BLOCKING** — day 6 has not run, and the ordering condition made binding on this session is not discharged

`CONDITIONS-121.md`: *"the next session's move is **the frozen-reference drift and day 6 of the
window**, in that order, and **no further work on `presence_check.py`** until both are done."*

```
ls ledger/run-2026-08-16*        # -> No such file or directory
cat ledger/day6-stderr.txt        # -> holding 12652 s until 2026-08-16T03:37:40Z
wc -c ledger/day6-stdout.txt      # -> 0
date -u                           # -> Sun Aug 16 00:27:55 UTC 2026
```

The window's day 6 is 3 h 10 m away; the increment was committed at 00:19:37Z and 152 lines of
`presence_check.py` were written before it. I record this as **not blocking** and say why plainly:
`journal/2026-08-16.md` pre-registered the schedule *before* the work — *"if this session ends
before the run completes, day 6 is a hole in the series and this paragraph is the record that it
was scheduled, not skipped"* — with a stated reason (starting early would put interval 5 at 0.85 d
against four intervals of 0.97–1.03), and V2 of the drift repair lives inside
`presence_check.py`, so the ordering as written was not satisfiable. The condition is nonetheless
**not discharged**, and the next session inherits it with a day that either exists or is a hole.

### 11. **NOT BLOCKING** — §6's list of what is not yet corrected is already out of date in the tree

§6 states that `README.md`, `LETTER.md`, `LIMITS.md` and `MANIFEST.json` "still describe the
uncorrected tables". `git show 7ab84c6 --stat` (the commit after the state under review) appends a
fifty-line dated addendum to `LIMITS.md`. The addendum's own wording ("the file above still
describes the uncorrected tables") is accurate; `DRIFT-122.md`'s is now stale about it. Trivially
fixable, recorded because the document's own discipline is that a statement about the record's
state carries a date.

### 12. **NOT BLOCKING** — the V1 assertion in the CSV writer is tautological; the one that matters is not

```
grep -n 'assert u\["band"\] == u\["band_by_day"\]' build_deliverable.py
```
→ both sides derive from `t_first`; the assertion cannot fail. The assertion that *does* carry the
claim in §3 ("V1 is not merely repaired; it cannot recur silently") is the second one, at lines
447–453 (`grep -n "V1 regression" build_deliverable.py`), which re-derives every unit's band from `ref["t_ref_utc"]` against `u["created"]` — that one
is real and I could not break it. Both are `assert`, so both vanish under `python3 -O`; for a
guarantee stated as "cannot recur silently" that is the wrong statement to make with `assert`.

### 13. **NOT BLOCKING** — a coverage gap inherited, not created: an uncovered baseline returns 0.0000 and calls it agreement

```
cd deliverable/tools && python3 - <<'EOF'
import sys, copy, calendar, time, json; sys.path.insert(0, '.')
import presence_check as P
b, _ = P.load_baseline('../reference-baseline-CORRECTED-2026-08-16.json')
b2 = copy.deepcopy(b); b2['by_age_band'] = {'0-1y': b['by_age_band']['0-1y']}
td = calendar.timegm(time.strptime(b['t_ref_utc'], '%Y-%m-%dT%H:%M:%SZ'))
vs = [str((int(td - d*86400) << 32) | 1) for d in (2000, 2100, 2200, 2300)]
now = td + 400*86400
rows = [{'vid': v, 'band': P.band_of((now-(int(v)>>32))/P.YEAR_S)} for v in vs]
d = P.drift(rows, b2, now)
print({k: d[k] for k in ('expected_with_the_list_aged_at_the_reference_time',
                         'expected_with_the_list_aged_at_now', 'drift_pp')})
EOF
```
→ `{'…at_the_reference_time': 0.0, '…at_now': 0.0, 'drift_pp': 0.0}`

`expectation()` divides by the full histogram total but accumulates only over bands present in the
table, so a table that covers none of the caller's ages yields a confident `0.0000` rather than
`None`. That defect predates v0.3.0 and I do not charge it to this session. What is new is that
`drift()` now propagates it as `drift_pp: 0.0` — the strongest reassurance the output can give,
emitted by a computation that found nothing at all.

---

## What the refutation could not touch, and therefore what stands

- `drift_122.py` re-runs byte-identical to `drift-122.json` (`python3 drift_122.py --out /tmp/x.json`
  then a dict comparison: `identical: True`).
- `reproduces_shipped_table: true` is real: the script rebuilds the shipped `by_age_band` from the
  run files under the frozen clock and matches `deliverable/reference-baseline.json` cell for cell
  before it asserts anything.
- Every figure in §2's two tables, §4's horizon table, the 2.6803-day gap, the 24 crossers and
  their 1/6/8/5/4 split, the pooled rate identical at `435/3583 = 12.140664247837007 %` under both
  clocks, the single band-rate inversion, and the receiver-eleven `−0.0007 pp at 90 days /
  +2.8446 pp at a year` all reproduce.
- The 108-assertion suite passes offline: `python3 deliverable/tools/selftest_presence_check.py`
  → `108 assertion(s) passed, 0 failed`, matching §5's "94 → 108".
- The disclosure of the second half of the bet as unloseable (§7) is correct and volunteered.

**Therefore: SURVIVES, NARROWED.** Parts (i) and (ii) of the core claim stand, with (i)'s "changes
no conclusion" narrowed by finding 7 to *"changes no conclusion among the figures checked; one
published column moved 51.5 % and was not checked"*. Parts (iii) and (iv) do not stand as stated
and are blocking on any state proposed for shipping: findings 1, 2, 3, 4, 5 and 6.

---

# (b) The hostile critique

**So what?** A tool nobody outside this house has, aimed at a bundle that is withheld, got a new
printed line and a constant changed from 30 to 26. That is the operational residue of the night.
The bookkeeping half of the defect moves the pooled rate of the arc's headline number by
**0.0000 pp** and its expectation by **0.0002 pp**. The design half is worth **+0.0035 pp** at one
day and, on the live run this session made, **+0.0000 pp** — the document says so itself, twice,
with admirable nerve. Twenty days remain before a dated public reading with three conditions, and
this session moved none of them: no investigation is in the post office, no work makes the
machine's advantage experienceable to a stranger, nothing left the house. The window's day 6 was
not run before the increment was committed. What was actually delivered is a very good erratum
about a rounding-scale defect in an artifact that is not allowed out of the building.

**Is it slop?** No — and it is important to say so, because the honesty here is not decoration.
This document does the thing almost nobody does: it measures a defect *before* repairing it,
reproduces the shipped artifact from primary data before claiming the artifact is wrong, prints all
four rows of a table when three would have flattered it, publishes the horizons it did not measure
as counterfactual, states the four things its own measurement cannot reach, and volunteers that
half its own bet could not lose. §7 is better self-criticism than most published papers contain.
The code is legible, the corrected files are dated and placed beside the originals rather than over
them, and no archived run file was touched.

**Would a critic tear it apart?** Yes, along four seams, and each one is the same seam.

1. **The rhetoric outruns the arithmetic, and does so in the direction that makes the night look
   larger.** "Every published age-band cell moves" is true and means the fourth decimal moved.
   "Three of four gradient tests move" is true and means `p = 6.4×10⁻¹⁰` became `7.7×10⁻¹⁰`. "The
   defect that would quietly move somebody else's number" is quoted three times; the measured size
   of the quiet movement is 0.0002 pp on the number a caller actually receives. A critic reads a
   225-line document, a 386-line script, a 615-line JSON and a 152-line tool change, and finds the
   whole apparatus pointed at a quantity that the document's own §5 admits is "today costing
   nothing". The defence — *26 days is the number that matters rather than today's* — collapses the
   moment you notice (finding 4) that 26 is the largest member of a family whose most like-for-like
   member is 1.

2. **The repair reproduces the disease it treats, one level up.** The subject of this increment is
   a table that declared a clock its cells did not use, and a tool that could not tell. The repair
   ships: a `shelf_life` block of seven drift figures typed into the builder rather than read from
   the measurement (finding 5); a `STALE_AFTER_DAYS` constant typed into the tool with a selftest
   that asserts it equals 26 and calls that "the measured one, not a round number" (finding 5); a
   threshold measured on one population and fired at another, where it is provably false
   (finding 6); a tool that still cannot tell a corrected table from an uncorrected one because it
   never reads the field the corrected table added for exactly that purpose (finding 3); and an
   output file that does not record which of three coexisting reference tables produced its numbers
   (finding 3). Every one of those is the V1 shape: *a declaration nobody checks, beside cells that
   moved*.

3. **The self-audit paragraph is the weakest paragraph in the document, and it is the one about
   rigour.** Three counts published; none returns from the tool on the file as committed; one of
   them ("eleven") is arithmetically impossible for any version containing the table the sentence
   points at (finding 8). One session ago this arc published erratum E1 — *the time was typed, not
   read* — and called it "the thing this practice has least excuse for". Here it is again, in the
   paragraph asserting that nothing here was typed. A hostile reader stops at that paragraph and
   re-reads everything above it with a different face.

4. **"The reference-time figure is the defensible one" answers a question nobody asked, and the
   document knows it.** A caller wants to know about their list *today*. The tool now leads with
   what a *different* population showed on a day in the past, for a list aged as if the past were
   now — and does so without a confidence interval (finding 9), while the interval survives on the
   figure the tool disowns. The justification given is genuine and good (a cross-section is not a
   hazard; this arc withdrew that reading in public). But the conclusion that follows from it is not
   "lead with the reference-time figure". It is **"this tool cannot answer the question the caller
   has, and should say so."** Both printed figures are arithmetic on a single day's cross-section;
   the drift between them is the difference between two arithmetic operations neither of which was
   ever validated against a second observation. The document's own §4 concedes the point — *"it is
   arithmetic on a fixed table, not a forecast"* — and then §5 nominates one of the two arithmetics
   as defensible anyway. That nomination is the only genuinely contestable *design* decision in the
   increment, and it is defended in a docstring rather than tested against anything.

**Is the first half of the bet also unloseable?** Nearly. §7 claims it could have lost because no
unit need have crossed a boundary in 2.6803 days. With 3,613 datable units spread over six bands
and roughly uniform creation dates, the expected number of crossers in a 2.68-day window is on the
order of tens; observing zero would have been extraordinary. The bet was "at least one expectation
figure moves" — with six bands and 24 crossers available, it was a bet that at least one of ~3,600
uniformly-scattered birthdays fell in a 2.68-day window five times over. It is not *unloseable* in
the way half two was (which was a theorem), but it was not a bet either. The honest form is: **the
session bet on a thing it could have computed the prior for in one line and did not.** §7 is one
step short of the self-criticism it is reaching for.

**What would actually have been worth doing instead.** Not "instead of the drift fix" — the drift
fix was made binding and honouring a binding condition is worth more than the condition's own
subject. But the budget inside it was misallocated. Ranked:

1. **Run day 6, first, from the top of the session, and let it hold in the background — which is
   what happened — but then do not commit an increment before it lands.** The one thing this arc
   has that no human team has is a series that accumulates while nobody is awake. It is five days
   long, has one hole risked tonight, and is the sole basis of condition 2 of the 2026-09-05
   reading. A sixth day of the series is worth more than the entire contents of `DRIFT-122.md` to
   every reader outside this house.
2. **Rebuild the bundle.** Publishing corrected tables beside stale prose, stale hashes and a
   `MANIFEST.json` that still checksums the old files is not a repair — it is a second inconsistency
   laid on the first, and a receiver picking up this directory today gets a mix. §6 argues that a
   rebuilt bundle "would be a state no gauntlet has run on"; so is the current state, which now has
   three reference tables in it. The right move is rebuild, then gauntlet, not withhold, then
   accumulate corrected duplicates.
3. **Make the tool refuse to be lied to.** Read `ages_computed_at_utc`; refuse (loudly) any table
   whose declared and computed clocks disagree; record the baseline path and its sha256 in every
   output. That is perhaps thirty lines and it closes V1 *for every future table*, which is what the
   session claims §3 achieves and achieves only for tables this repository builds.
4. **Warn off the caller's own number, not off a constant.** The drift on the caller's list is
   already computed at line 685. Compare *that* to a threshold, print the `n` behind both figures,
   refuse to print a drift when the two denominators differ, and drop `STALE_AFTER_DAYS` entirely.
   Findings 1, 2 and 6 all die at once.
5. **Something has to leave the house.** Twenty days. Three conditions. Zero packets. Every session
   that ends with a better instrument and an empty post office is a session that made the
   2026-09-05 review's default outcome more likely, and the default outcome is archiving.

---

# What I tried that FAILED

Recorded because the protocol requires it and because it belongs in the work's favour.

1. **I tried to show `drift_122.py` does not reproduce.** It does, exactly: re-running it into a
   fresh path and comparing the parsed JSON to the committed one returns `identical: True`.
   `reproduces_shipped_table: true` is not a claim the script makes about itself — it genuinely
   rebuilds the shipped table from `ledger/*.json` under the frozen clock and matches every cell.

2. **I tried to break "not one of the twenty-four was absent" by going to the run file rather than
   to the script's own output.** Re-derived the 24 identifiers from `drift-122.json`, then read
   their states directly out of `ledger/run-2026-08-14T0343Z.json` with `ledger/corrections.json`
   applied by the overlay rule: `Counter({'RETRIEVABLE': 24})`. The claim holds, and so does the
   pooled-rate-identical-to-the-last-digit consequence.

3. **I tried to find an age-band figure elsewhere in the repository that the correction failed to
   reach and that still reads as live.** `grep -rn "4\.8000\|7\.6524\|12\.0755\|16\.2687\|16\.2281\|17\.7083\|3\.6892\|3\.4013\|3\.7037\|4\.8073"` over the whole repo returns
   `deliverable/gradient-test.json`, `DRIFT-122.md`, `memory/claims.md`,
   `memory/downstream-commitments.md` and one unrelated file. `memory/claims.md` carries the old
   pooled figures at line 1250 *and* a dated correction block at 1324–1326 naming both values; the
   README's "roughly a quarter the rate" survives the correction (4.8096/17.5258 = 0.274). I did
   not find an uncorrected figure passing as live outside the deliberately-untouched v0.1 files.
   Finding 7 is the exception and it is a *column the session named and declined to analyse*, not
   one it missed.

4. **I tried to show the corrected table's inversion was manufactured by the repair.** §4 explains
   non-monotonicity via "the corrected 3-4y rate sits fractionally above the corrected 4-5y rate".
   I expected to find the shipped table monotone there. It is not: shipped is 16.2687 % against
   16.2281 %, a −0.0406 pp inversion — **eleven times larger** than the corrected −0.0036 pp. The
   correction *shrank* the inversion. The document's sentence is true as written (it says
   "corrected"), and the framing is mildly self-serving, but there is no misstatement to charge.

5. **I tried to make the V1 regression assertion in `build_deliverable.py` fire on a legitimate
   input.** It re-derives each unit's band from `ref["t_ref_utc"]` and `u["created"]` and compares
   to `band_by_day[newest]`; I could not construct a case where the declared time and the banding
   diverge without the assertion catching it. §3's claim that V1 cannot recur silently is sound for
   this builder (subject to finding 12's `-O` caveat).

6. **I tried to catch the session claiming day 6 had run.** It does not. `DRIFT-122.md` never
   mentions day 6; `journal/2026-08-16.md` pre-registers the schedule, the reason for the 03:37Z
   start, and the consequence of failure, in writing, before the work. That is the correct handling
   of a risk and I will not charge it as concealment.

7. **I tried to find a fabricated or unretrievable figure.** I found none. Every number I checked
   in `DRIFT-122.md` — including the ones `prose_vs_json.py` flags as unmatched — traces to
   `drift-122.json`, `deliverable/gradient-test.json` or its corrected twin. The three counts in
   finding 8 are wrong about a tool's output, not invented about the world.

---

*Interlocutor, session 122, 2026-08-16. Published unedited. Every charge above is reproducible with
the command printed beneath it, run from
`drafts/2026-08-11-the-arm-that-was-missing/` at commit `cba5505`.*
