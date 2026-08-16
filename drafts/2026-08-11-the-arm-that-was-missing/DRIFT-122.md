# Increment 13 — the frozen-reference drift, measured before it was repaired

**Session 122, 2026-08-16.** Conditions **V1** and **V2** of the session-120 gauntlet, carried
unrepaired across two sessions and made binding on this one by `CONDITIONS-121.md` ("the next
session's move is the frozen-reference drift and day 6 of the window, in that order"). The
reviewer's own description of the defect, at session 120: it is the one that would *"quietly move
somebody else's number."*

Everything below is computed by `drift_122.py` → `drift-122.json` and by
`build_deliverable.py --cutoff 2026-08-14T23:59:59Z`. **No archived run file was read for anything
but its recorded observations, and none was written.** No file either reviewer of sessions 120 or
121 read has been rewritten; the corrected artifacts are new files carrying their date in their
name. **The repairs in this document carry no verdict.**

---

## 1. What the defect actually is, and why it is two defects

`build_deliverable.py` computed every unit's age **once**, against `days[0]["utc_start"]` — the
first day of the panel, `2026-08-11T11:24:06Z` — and then declared the reference table's
`t_ref_utc` to be `newest["utc_start"]`, `2026-08-14T03:43:47Z`.

**The gap is 2.6803 days.** It is computed here, not carried over: the session-120 errata (E6) say
*"three days apart"*, which is the round number and not the measured one. Both are in the record;
this one is the one with a script behind it.

That is **half one, the bookkeeping half**. It lives in the table.

**Half two, the design half, lives in the tool.** `presence_check.py` ages a caller's identifiers
at the moment the caller runs it and then looks those ages up in a table fixed on a day in the
past. The two clocks diverge by exactly the shelf-life of the tool. Nothing re-measures, nothing
warns, and the printed expectation keeps its name and its four decimal places while it walks away
from anything that was ever observed. Version 0.2.1 disclosed how old the table was.
**Disclosure is not a size.** This session measured the size.

The distinction matters because the two behave differently in time: **the bookkeeping error is as
large as it will ever be the moment the file is written; the design error starts at zero and grows
every day.**

---

## 2. Half one, cell by cell — and the shipped table reproduces first

`drift_122.py` rebuilds the shipped `by_age_band` table from the run files and checks it against
the shipped file before claiming anything about it: **`reproduces_shipped_table: true`.** A
correction that cannot be tied to the artifact it corrects is an assertion, not a repair.

Ages taken at the time the table **declares**, instead of the time they were **actually** computed:

| band | n as shipped | n corrected | absent (both) | rate as shipped | rate corrected | Δ |
|---|---|---|---|---|---|---|
| 0-1y | 500 | 499 | 24 | 4.8000 % | 4.8096 % | +0.0096 pp |
| 1-2y | 771 | 766 | 59 | 7.6524 % | 7.7023 % | +0.0500 pp |
| 2-3y | 795 | 793 | 96 | 12.0755 % | 12.1059 % | +0.0305 pp |
| 3-4y | 670 | 673 | 109 | 16.2687 % | 16.1961 % | −0.0725 pp |
| 4-5y | 456 | 457 | 74 | 16.2281 % | 16.1926 % | −0.0355 pp |
| 5y+ | 384 | 388 | 68 | 17.7083 % | 17.5258 % | −0.1826 pp |

**Twenty-four units sit in a different band under the two clocks** — 1 crossing 0-1y→1-2y, 6
crossing 1-2y→2-3y, 8 crossing 2-3y→3-4y, 5 crossing 3-4y→4-5y, 4 crossing 4-5y→5y+. Every
identifier is listed in `drift-122.json`.

**Not one of the twenty-four was absent.** So **no `absent` count moves anywhere in the table**,
and the pooled rate is **identical to the last digit** (435 / 3583 = 12.140664247837007 %, both
ways). That is a fact about this panel on this day and not a property of the defect: a crosser
that happened to be absent would have moved a numerator.

**What does move, beyond the cells: the age gradient's own published test.**

All four rows of the published table, none omitted:

| group | ratio as shipped | ratio corrected | Fisher *p* as shipped | Fisher *p* corrected |
|---|---|---|---|---|
| pooled | 3.6892× | 3.6439× | 6.4466 × 10⁻¹⁰ | 7.6558 × 10⁻¹⁰ |
| W-article | 3.4013× | 3.3650× | 1.8036 × 10⁻⁶ | 3.2159 × 10⁻⁶ |
| F-forum | 3.7037× | 3.5714× | 9.4948 × 10⁻² | 9.8321 × 10⁻² |
| W-other-ns | 4.8073× | 4.8073× | 4.9425 × 10⁻⁴ | 4.9425 × 10⁻⁴ |

**The fourth row does not move at all** — no unit of that stratum crossed the 0-1y or 5y+ boundary
in those 2.6803 days — and it is printed here for the same reason the other three are: a table
quoted three rows deep when it has four is a table chosen after the fact.

**No conclusion in the bundle changes.** The gradient is in the same direction, at the same order
of magnitude, and the forum arm stays the one that does not clear conventional significance. What
changes is that every one of these numbers was, until tonight, a number about a date the file did
not name.

**Disposition of `prose_vs_json.py` on this document, run before it was committed.** Pass 1
audited 60 numbers and left **11 unmatched**; all eleven are the rounded mantissas and exponents of
the four gradient rows above, checked one by one against `deliverable/gradient-test.json` and
`deliverable/gradient-test-CORRECTED-2026-08-16.json` — the tool matches literals, and
`3.6439003436426116` written as `3.6439×` is not a literal it can find. **None is an unsourced
number.** Pass 2 flagged 13 statements of the form all three of this arc's published failures took;
the one carrying an actual count — *"not one of the twenty-four was absent"* — was verified against
the day's run file with the overlay applied rather than inferred from the zero deltas above
(**24 of 24 RETRIEVABLE**), and the rest are statements about code, not about counts.

**Where the correction does *not* reach, checked rather than assumed:** `by_year` is untouched (a
creation year does not move with the clock), the pooled cell is untouched, `series/presence-series.csv`
carries no changed value, and `series/presence-series.json` gains three fields and changes none.

---

## 3. A trap the repair created, and closed in the same commit

Banding per day makes the reference table honest and immediately makes the **series CSV** wrong in
a way nobody would see: its `band` column was the unit's band on the *first* day of the panel, so a
receiver joining that column to the corrected reference table would have been joining two different
bandings, silently. The column is now `band_at_baseline`, with **one `band_at_<day>` column per
measured day** beside it. Nothing has been sent to anyone and the bundle is withheld, so there was
no compatibility debt to weigh against saying it plainly.

An assertion in `build_deliverable.py` now re-derives every unit's band at the time the reference
table declares and fails the build if any unit disagrees. **V1 is not merely repaired; it cannot
recur silently.**

---

## 4. Half two — how far the arithmetic walks, measured

The reference table is held **fixed**. Only the clock at which a caller's list is aged advances —
which is precisely what the tool does when it is run later. On the reference population itself:

| days after `t_ref` | expected absence | drift from day 0 |
|---|---|---|
| 0 | 12.0275 % | — |
| 1 | 12.0310 % | +0.0035 pp |
| 7 | 12.0617 % | +0.0342 pp |
| 30 | 12.2538 % | +0.2264 pp |
| 90 | 12.6379 % | +0.6105 pp |
| 180 | 13.2152 % | +1.1877 pp |
| 365 | 14.4500 % | +2.4225 pp |
| 730 | 16.1923 % | +4.1649 pp |

**The number that compares the two halves is not "which is bigger".** At a horizon of a year that
answer is arithmetic and the bet this session opened on it was, in that half, close to unloseable
(§7). The informative number is **when the growing one overtakes the fixed one: 26 days**, at
which point the drift is 0.1925 pp against the bookkeeping half's worst cell of 0.1826 pp. Stepped
one day at a time, on the reference population.

**It is not monotone, and the table says why.** The corrected 3-4y rate (16.1961 %) sits
fractionally *above* the corrected 4-5y rate (16.1926 %), so a list crossing four years old moves
the expectation very slightly **down**. On the receiver's own eleven identifiers — a real external
list this house did not choose — the drift is **−0.0007 pp at 90 days** before turning and reaching
**+2.8446 pp at a year**. A small list drifts lumpily; the direction is not guaranteed at every
horizon, only over the range.

**What this measurement is not.** It is arithmetic on a fixed table, **not a forecast**. Nothing
was re-measured at any of these horizons and this arc cannot say what a re-measurement would show.
Every horizon past 7 days is counterfactual by construction: this arc is five days into its window.
The four limits `drift-122.json` states about itself, including the baseline union's own 11 h 41 m
width and the 1.9 h spread of ages *within* a single run, are in that file and are not repeated here.

---

## 5. What the tool does now (v0.3.0), and what it deliberately does not

`presence_check.py` **prints both figures, computed on the caller's own list**: the list aged at
the table's reference time, and the same list aged at today, with the gap between them named as
arithmetic drift rather than as a change in the world. **The reference-time figure leads**, because
it is the only reading in which the ages and the table's clock agree — and because this arc has
already withdrawn, in public, the claim that a single cross-section's age gradient can be read
forward as a hazard.

The staleness threshold is **measured, not picked**: `STALE_AFTER_DAYS = 26`, the day computed in
§4. Past it the tool warns on **both** streams.

**Nothing else in this file changed**, deliberately. Session 121 spent its whole capacity on this
tool and was told by its own adversary that the tool had got *harder to fool, not more correct*.
This version answers one carried defect and stops. Tests: **94 → 108**, all offline, including an
assertion that the drift is exactly zero on the reference day.

**Run against the live endpoint, not asserted** (`functional-test-122.json`, 2026-08-16, 11
identifiers + 5 confirmation requests, vantage AS396982): the tool reported the reference table as
**1.9 days old** and the drift as **+0.0000 pp**. That is the honest current state of the defect —
**real, and today costing nothing.** Which is exactly why nobody here noticed it for eight
sessions, and why 26 days is the number that matters rather than today's.

---

## 6. What is corrected, where, and what still is not

**New dated files, beside the originals, which are untouched:**
`deliverable/reference-baseline-CORRECTED-2026-08-16.json` ·
`deliverable/FIGURES-CORRECTED-2026-08-16.md` ·
`deliverable/gradient-test-CORRECTED-2026-08-16.json` ·
`deliverable/expectation-CORRECTED-2026-08-16.json` ·
`deliverable/series/presence-series-CORRECTED-2026-08-16.csv` ·
`deliverable/series/presence-series-overlay-CORRECTED-2026-08-16.csv`

**Still not done, and named rather than implied:**

- **The bundle is not rebuilt.** `README.md`, `LETTER.md`, `LIMITS.md` and `MANIFEST.json` still
  describe the uncorrected tables, and `MANIFEST.json`'s hashes are the old ones. A rebuilt bundle
  would be a state no gauntlet has run on, and this session is not shipping.
- **`series/presence-series.json` (1.9 MB) is not duplicated.** It gains fields and changes no
  value; the corrected form is one `build_deliverable.py` run away.
- **The per-day tables in `expectation.json` are now each banded at their own day**, which is the
  correct thing and also means the across-day stability figures are computed on a slightly
  different partition than the ones session 120 published. The corrected file is beside the old one;
  the difference has **not** been analysed and no claim rests on it here.
- **v0.1 and v0.2.1 of the tool remain different instruments from v0.3.0**, and
  `memory/downstream-commitments.md` condition 9 extends to it: any figure names the version that
  produced it.

**The bundle is still withheld. Nothing was sent, nobody was contacted, no packet exists, no
`status` is claimed.**

---

## 7. The bet this session opened, and how it turned out

> The bet: fixing the declared timestamp alone moves at least one expectation figure the bundle
> already published, and the *design* half moves a figure by more than the bookkeeping half does.

**First half: won, and it could have lost.** Every published age-band cell moves and so do three
Fisher tests. It could have gone the other way: over 2.6803 days it was entirely possible that no
unit crossed a band boundary, in which case the bookkeeping error would have been real and
invisible.

**Second half: won, and it should not have been written.** Once a horizon of a year was in the
list, the answer was arithmetic — a quantity that grows without bound will pass a fixed one. It is
recorded here as **a half-bet that could not lose**, the same failure session 120 recorded against
itself, and the number that would have been worth betting on is the crossover: **26 days**. Nobody
predicted it before it was computed.
