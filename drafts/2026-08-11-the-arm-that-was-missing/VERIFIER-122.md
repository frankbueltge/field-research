# Verifier — session 122, commit `95ab278`

**Object under review:** the working tree at `95ab278` (clean; `git status --porcelain` empty;
commit dated 2026-08-16 00:19:37 +0000). Primary document `DRIFT-122.md`.

**Method.** Every number in the table of figures below was recomputed by code written for this
review, reading the run files in `ledger/` directly. `drift_122.py` was not called to produce any
figure in that table; it was executed exactly once, at the end, to a scratch path, for the single
purpose of checking one quoted stdout key and regeneration determinism. `build_deliverable.py` was
run twice to scratch paths. No file in the repository was modified by this review.

---

## Verdict

**FAIL.** Two blocking findings, both statements of fact about the session's own work rather than
about the measurement. **Every measured number in `DRIFT-122.md` is correct.** All 68 figures I
recomputed agree, most of them to the last digit of the IEEE double; the four Fisher exact
*p*-values were re-derived in exact rational arithmetic and agree with the shipped floats to the
last unit in the last place. The failure class that ended the last two sessions — a time asserted
in prose that nothing on disk supports — **does not recur**: every one of the 24 temporal tokens in
`DRIFT-122.md` traces to a file.

Blocking findings, numbered first:

1. **`DRIFT-122.md` lines 88–89** — the reported result of the `prose_vs_json.py` audit ("Pass 1
   audited 60 numbers and left **11 unmatched**") does not reproduce against the document it
   describes, and no artifact of the run exists on disk. See Finding 1.
2. **`DRIFT-122.md` line 12** — "No file either reviewer of sessions 120 or 121 read has been
   rewritten" is false. This commit rewrites three files that those reviewers demonstrably read.
   See Finding 2.

Both are one-line repairs and neither touches a measurement.

---

## Table of every figure recomputed

`§` is the section of `DRIFT-122.md`. "Mine" is the value my own code produced.

### The gap and its two clocks (§1)

| claim | claimed | mine | agree |
|---|---|---|---|
| ages actually computed against | `2026-08-11T11:24:06Z` | `days[0]` is the baseline union; `ledger/baseline-union.json → run_utc_start` = `2026-08-11T11:24:06Z` | YES |
| table declares | `2026-08-14T03:43:47Z` | `ledger/run-2026-08-14T0343Z.json → run_utc_start`; `deliverable/reference-baseline.json → t_ref_utc` | YES |
| the gap | 2.6803 days | 231581 s = 2.680335648148148 d | YES |
| `days[0]["utc_start"]` for ages, `newest["utc_start"]` for `t_ref_utc` | as quoted | `git show 95ab278~1:…/build_deliverable.py` line 179 `t_ref = calendar.timegm(time.strptime(days[0]["utc_start"], …))`; line 364 `"t_ref_utc": newest["utc_start"],` — the line numbers `drift-122.json` states are exact | YES |

### §2 — the age-band table, every cell

Recomputed from `ledger/run-2026-08-14T0343Z.json` with the stated exclusions (arm `B-truncated`
out: 249; `INDETERMINATE` out: 37; non-19-digit out of the age tables only: 7; pooled n = 3583).

| band | n shipped | mine | n corrected | mine | absent | mine | rate shipped | mine | rate corrected | mine | Δ | mine | agree |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0-1y | 500 | 500 | 499 | 499 | 24 | 24 | 4.8000 % | 4.8000 | 4.8096 % | 4.8096 | +0.0096 | +0.0096 | YES |
| 1-2y | 771 | 771 | 766 | 766 | 59 | 59 | 7.6524 % | 7.6524 | 7.7023 % | 7.7023 | +0.0500 | +0.0500 | YES |
| 2-3y | 795 | 795 | 793 | 793 | 96 | 96 | 12.0755 % | 12.0755 | 12.1059 % | 12.1059 | +0.0305 | +0.0305 | YES |
| 3-4y | 670 | 670 | 673 | 673 | 109 | 109 | 16.2687 % | 16.2687 | 16.1961 % | 16.1961 | −0.0725 | −0.0725 | YES |
| 4-5y | 456 | 456 | 457 | 457 | 74 | 74 | 16.2281 % | 16.2281 | 16.1926 % | 16.1926 | −0.0355 | −0.0355 | YES |
| 5y+ | 384 | 384 | 388 | 388 | 68 | 68 | 17.7083 % | 17.7083 | 17.5258 % | 17.5258 | −0.1826 | −0.1826 | YES |

The "n as shipped / absent" column is identical, cell for cell, to `deliverable/reference-baseline.json
→ by_age_band` (500/771/795/670/456/384 and 24/59/96/109/74/68). **The claim that the shipped table
reproduces from the run files is therefore confirmed independently of `drift_122.py`.**

| claim | claimed | mine | agree |
|---|---|---|---|
| units changing band | 24 | 24; identical vid set to `drift-122.json → units_changing_band`, identical directions | YES |
| direction breakdown | 1 / 6 / 8 / 5 / 4 | 0-1y→1-2y **1**, 1-2y→2-3y **6**, 2-3y→3-4y **8**, 3-4y→4-5y **5**, 4-5y→5y+ **4** | YES |
| "not one of the twenty-four was absent" | 24 of 24 RETRIEVABLE | 24 of 24 `RETRIEVABLE` in the raw run file **and** with `ledger/corrections.json` applied (the one overlay row for this run file, `7016669364938149122`, is not a crosser) | YES |
| pooled, both ways | 435 / 3583 = 12.140664247837007 % | `repr(435/3583*100)` = `12.140664247837007`; exact decimal 12.140664247837008094…; unchanged under either clock | YES |
| `by_year` untouched | untouched | `by_year` identical between `reference-baseline.json` and `…-CORRECTED-2026-08-16.json` | YES |
| pooled cell untouched | untouched | `pooled` identical (also `by_stratum`) | YES |

### §2 — the gradient test, all four rows, both versions

Fisher two-sided recomputed by summing hypergeometric tables no more likely than the observed one,
in `fractions.Fraction` (exact rationals; the pooled corrected *p* is a 101-digit numerator over a
110-digit denominator), then converted to float for comparison.

| group | ratio shipped | mine | ratio corrected | mine | *p* shipped | mine (exact→float) | *p* corrected | mine (exact→float) | agree |
|---|---|---|---|---|---|---|---|---|---|
| pooled | 3.6892× | 3.689236111111111 | 3.6439× | 3.6439003436426116 | 6.4466 × 10⁻¹⁰ | 6.446636838056335e-10 | 7.6558 × 10⁻¹⁰ | 7.6557743720365817e-10 | YES |
| W-article | 3.4013× | 3.4013157894736836 | 3.3650× | 3.3649720149253732 | 1.8036 × 10⁻⁶ | 1.8035510480786784e-06 | 3.2159 × 10⁻⁶ | 3.2158825030024731e-06 | YES |
| F-forum | 3.7037× | 3.7037037037037033 | 3.5714× | 3.571428571428571 | 9.4948 × 10⁻² | 0.094948027314809683 | 9.8321 × 10⁻² | 0.098321370444341805 | YES |
| W-other-ns | 4.8073× | 4.807291666666667 | 4.8073× | 4.807291666666667 | 4.9425 × 10⁻⁴ | 0.0004942478835822774 | 4.9425 × 10⁻⁴ | 0.0004942478835822774 | YES |

The 2×2 cells I recomputed match the shipped and corrected JSON exactly: pooled young [24, 500] →
[24, 499], old [68, 384] → [68, 388]; W-article [16, 308]→[16, 307], [47, 266]→[47, 268]; F-forum
[2, 50]→[2, 50], [8, 54]→[8, 56]; W-other-ns [6, 142] and [13, 64] both ways.

| claim | mine | agree |
|---|---|---|
| "the fourth row does not move at all — no unit of that stratum crossed the 0-1y or 5y+ boundary" | W-other-ns has 4 crossers, all interior: 1-2y→2-3y ×1, 2-3y→3-4y ×2, 3-4y→4-5y ×1. None touches 0-1y or 5y+ | YES |
| "the forum arm stays the one that does not clear conventional significance" | 0.0949 and 0.0983, both > 0.05; the other three < 0.001 | YES |

### §4 — the caller-side drift

Reference table held fixed at the corrected rates; the panel's 3613 datable identifiers re-aged.
(3613 = 3869 observations − 249 `B-truncated` − 7 undatable; the 37 `INDETERMINATE` are *in*,
because a caller's list is a list of identifiers, not of readings.)

| days after `t_ref` | expected claimed | mine | drift claimed | mine | agree |
|---|---|---|---|---|---|
| 0 | 12.0275 % | 12.027451 % | — | 0.0 | YES |
| 1 | 12.0310 % | 12.030984 % | +0.0035 pp | +0.0035330266282704303 | YES |
| 7 | 12.0617 % | 12.061663 % | +0.0342 pp | +0.03421261292645833 | YES |
| 30 | 12.2538 % | 12.253839 % | +0.2264 pp | +0.22638891566771902 | YES |
| 90 | 12.6379 % | 12.637933 % | +0.6105 pp | +0.6104822168843824 | YES |
| 180 | 13.2152 % | 13.215199 % | +1.1877 pp | +1.1877480612001237 | YES |
| 365 | 14.4500 % | 14.449969 % | +2.4225 pp | +2.422518562422897 | YES |
| 730 | 16.1923 % | 16.192313 % | +4.1649 pp | +4.164862732010631 | YES |

| claim | claimed | mine | agree |
|---|---|---|---|
| crossover | 26 days | 26 (stepped one day at a time, 0…1095) | YES |
| drift at crossover | 0.1925 pp | 0.1925055937959913 | YES |
| worst bookkeeping cell | 0.1826 pp | 0.1825601374570468 (the 5y+ cell, matching §2's −0.1826) | YES |
| the inversion | corrected 3-4y 16.1961 % above 4-5y 16.1926 % | 0.16196136701337296 vs 0.16192560175054704 | YES |
| receiver's eleven at 90 days | −0.0007 pp | −0.0006502775059258337 | YES |
| receiver's eleven at a year | +2.8446 pp | +2.8446128980238656 | YES |

The receiver-eleven turn is real and not an artifact of rounding: the histogram is
{2-3y:7, 3-4y:2, 4-5y:2} at day 0, {2-3y:7, 4-5y:4} at day 90, {3-4y:7, 4-5y:2, 5y+:2} at day 365.

### §4 — the stated limits

| claim | mine | agree |
|---|---|---|
| baseline union 11 h 41 m wide | `baseline-union.json` 2026-08-11T11:24:06Z → 23:05:18Z = 11:41:12, `components` lists four runs | YES |
| ~1.9 h spread of ages within a run | run durations 1.424 / 1.811 / 1.876 / 1.840 / 1.896 h | YES (as "roughly") |
| "this arc is five days into its window" | five complete run files, 2026-08-11 … 2026-08-15 | YES |

### §5 — the tool

| claim | claimed | mine | agree |
|---|---|---|---|
| test count | 94 → 108 | ran `selftest_presence_check.py` at `95ab278~1` (v0.2.1): **94 passed, 0 failed**; at `95ab278` (v0.3.0): **108 passed, 0 failed**, exit 0 | YES |
| section 8 size | (implied 14) | 108 − 94 = 14, and I count 14 `check`/`check_true` calls in section 8 | YES |
| "an assertion that the drift is exactly zero on the reference day" | present | `check("drift is exactly zero on the reference day", d0["drift_pp"], 0.0)` | YES |
| `STALE_AFTER_DAYS` | 26 | `presence_check.py:139` = 26; `drift-122.json → when_the_design_half_overtakes_the_bookkeeping_half.days` = 26; my own crossover = 26 | YES |
| `drift()` does what §5 says | both figures, reference-time one leads | `drift()` returns `expected_with_the_list_aged_at_the_reference_time`, `expected_with_the_list_aged_at_now`, signed `drift_pp`, both histograms, and a `which_one_is_defensible` naming the reference-time reading; `main()` prints the reference-time figure first and the now-aged one indented beneath it | YES |
| warns on both streams past the threshold | yes | `presence_check.py:728–734`: stdout `print` and a second `print(..., file=sys.stderr)` | YES |
| "nothing else in this file changed" | deliberate | the v0.2.1→v0.3.0 diff removes **9** non-comment lines: two version strings, the old `age_d > 30` staleness block, and the old single-line expectation print. Everything else is additive (128 added) | YES |

### §5 — the live run (`functional-test-122.json`)

| claim | in the file | agree |
|---|---|---|
| 2026-08-16 | `started_utc` 2026-08-16T00:16:53Z, `finished_utc` 00:17:14Z | YES |
| 11 identifiers | `list.n_items` = 11, 11 observations, `refused_lines` [] | YES |
| 5 confirmation requests | one `NOT-RETRIEVABLE` reading with `confirmation.passes` = 5, `states` a 5-element array; no other observation carries a confirmation | YES |
| vantage AS396982 | `vantage.asn` = "AS396982", `source` https://ipinfo.io/json | YES |
| "1.9 days old" | `baseline_currency.age_days_at_measurement` = 1.856; the tool prints it `:.1f` → "1.9 day(s)". I recomputed the gap from `started_utc` and the declared `t_ref`: 1.856 | YES |
| "+0.0000 pp" | `frozen_reference_drift.drift_pp` = 0.0; both histograms {2-3y:7, 3-4y:2, 4-5y:2}. I recomputed both histograms at both clocks and they are identical | YES |
| the expectation behind it | I recomputed `expected_absent_rate`, `expected_lo`, `expected_hi` from the corrected band table: 0.13592625615723686 / 0.11229543023739788 / 0.16360454794148888 — exact float match to the file, and an exact match to my day-0 receiver-eleven figure in §4 | YES |

### §2 and §6 — what the correction does and does not reach

| claim | mine | agree |
|---|---|---|
| `series/presence-series.csv` carries no changed value | 3869 rows, identical row order and ids; **0** differing cells across the 9 shared columns; the old `band` column equals the new `band_at_baseline` in all 3869 rows | YES |
| `series/presence-series.json` gains three fields and changes none | added exactly `age_y_by_day`, `band_by_day`, `created`; **0** changed values in the 8 pre-existing unit fields; all six top-level keys identical | YES |
| `presence-series.json` is 1.9 MB | 1,903,915 bytes | YES |
| the six dated corrected files exist | all six present in `deliverable/` and `deliverable/series/` | YES |
| the originals are untouched | the commit stat for `95ab278` adds the dated files and touches no original bundle artifact — `README.md`, `LETTER.md`, `LIMITS.md`, `MANIFEST.json`, `reference-baseline.json`, `FIGURES.md`, `gradient-test.json`, `expectation.json`, `presence-series.csv`, `presence-series.json` are all unchanged | YES |
| 24 units are in a different band in the corrected CSV | `band_at_baseline` ≠ `band_at_2026-08-14` in exactly 24 rows | YES |

### §7 — the bet

| claim | mine | agree |
|---|---|---|
| the bet text | verbatim in `journal/2026-08-16.md`, committed at `94675e5` **2026-08-16 00:05:38 +0000** — before `drift-122.json` and before the live run. Genuinely pre-registered | YES |
| "the same failure session 120 recorded against itself" | `journal/2026-08-15.md` line 190: "It is recorded as a bet that could not lose, which is not a bet." | YES |

---

## Independent checks of the repair machinery

**The rebuild runs and is deterministic.** `python3 build_deliverable.py --out <tmp> --cutoff
2026-08-14T23:59:59Z` from the draft directory: exit 0, twice. The two trees differ in exactly two
lines — `MANIFEST.json → built_utc` and the generation stamp in `FIGURES.md`. Every other file is
byte-identical between runs.

**The dated corrected artifacts are exactly what a fresh rebuild produces.** Byte-identical:
`reference-baseline-CORRECTED-2026-08-16.json`, `gradient-test-CORRECTED-2026-08-16.json`,
`expectation-CORRECTED-2026-08-16.json`, `series/presence-series-CORRECTED-2026-08-16.csv`,
`series/presence-series-overlay-CORRECTED-2026-08-16.csv`. `FIGURES-CORRECTED-2026-08-16.md`
differs from my rebuild in one line only, its own build stamp (`2026-08-16T00:14:24Z` against my
run's clock). Nothing in these files was hand-written.

**`drift-122.json` regenerates byte-identically.** `python3 drift_122.py --out <tmp>` reproduces
the committed file byte for byte, and its stdout summary is
`{"reproduces_shipped_table": true, "gap_days": 2.6803, "bands_that_move": 6,
"units_changing_band": 24, "panel_drift_365d_pp": 2.4225, "inversions": 1}` — so the
`reproduces_shipped_table: true` quoted at §2 is the script's own console output and is real.

**The new assertion in `build_deliverable.py` fires. Mutation-tested in copies, never in the
repository file.** Two independent mutations, each in its own copy under a scratch directory:

- re-introducing V1 (band each unit at `t_first` instead of at its own day) →
  `AssertionError: V1 regression: 6995836797225913606 is banded at a time the reference table does
  not declare`, exit 1;
- leaving the banding correct but declaring the wrong `t_ref_utc` (`2026-08-11T11:24:06Z`) → the
  same assertion, exit 1.

The assertion catches the defect from **both** directions, and it re-derives the band from the
declared string via `strptime` rather than comparing two strings to each other. §3's "V1 is not
merely repaired; it cannot recur silently" is substantiated.

**No typed timestamp.** I extracted all 24 date/time/duration tokens from `DRIFT-122.md` and
traced each to a file: `2026-08-16` (commit `95ab278` at 00:19:37Z, `journal/2026-08-16.md`,
`functional-test-122.json → started_utc`), `2026-08-14T23:59:59Z` (the `--cutoff` value, and
`drift-122.json → panel_cutoff`), `2026-08-11T11:24:06Z` (`baseline-union.json`),
`2026-08-14T03:43:47Z` (`run-2026-08-14T0343Z.json`), 2.6803 days, 26 days, 90/7 days, 11 h 41 m,
1.9 h, 1.9 days, five days, v0.1/v0.2.1/v0.3.0. **Every one is read or computed. The session-121
blocking failure does not recur.**

---

## Findings

### Finding 1 — BLOCKING. The `prose_vs_json.py` audit result does not reproduce
**`DRIFT-122.md` lines 88–89.**

> "Pass 1 audited 60 numbers and left **11 unmatched**; all eleven are the rounded mantissas and
> exponents of the four gradient rows above … Pass 2 flagged 13 statements…"

I ran `python3 prose_vs_json.py DRIFT-122.md` from the draft directory against the committed file:

```
DRIFT-122.md: pass 1 — 65 numbers audited, 16 not found in any JSON of this draft
DRIFT-122.md: pass 2 — 15 claims whose FORM is the form all three published failures took
```

The paragraph is self-referential — it adds numbers and claims of its own — so I removed lines
88–96 to approximate the state the tool would have seen "before it was committed":

```
pass 1 — 63 numbers audited, 14 not found
pass 2 — 13 claims
```

**Pass 2's 13 reproduces exactly.** Pass 1's does not, in either count. I then tried to reach
60/11. Removing lines 77–81 as well — the W-other-ns table row and the paragraph that introduces
it — gives **60 audited but 12 unmatched**, and that reconstruction contradicts the sentence's own
description, because a three-row table cannot produce eleven figures that are "the rounded
mantissas and exponents of the **four** gradient rows above." No state I could construct yields
60/11. No stdout capture of the run exists anywhere in the draft directory.

**What is *not* wrong here:** the disposition's conclusion. I checked the 14 currently-unmatched
values by hand against the two gradient JSONs and against my own recomputation from the run files:
every one is a correct 5-significant-figure rounding of a value that exists in
`deliverable/gradient-test.json` or `deliverable/gradient-test-CORRECTED-2026-08-16.json`. **None
is an unsourced number** — that part of the sentence is true. It is the audit *statistics* that are
wrong, in the one paragraph whose whole function is to demonstrate that the numbers were checked.

This is blocking because it is a stated result of a verification, it is the arc's own named
failure class ("a figure in prose that exists nowhere in the data"), and the fix is to re-run the
tool on the committed file, write the stdout to a dated artifact, and quote it.

### Finding 2 — BLOCKING. "No file either reviewer read has been rewritten" is false
**`DRIFT-122.md` line 12.**

The commit stat for `95ab278` shows three rewritten files that the reviewers of sessions 120 and
121 demonstrably read:

- **`build_deliverable.py`**, 88 lines changed. `VERIFIER-120.md` line 134 records
  "**Command:** `python3 build_deliverable.py --out <scratch>` from the draft directory", and line
  185 quotes its behaviour ("`build_deliverable.py` computes every unit's age once, at …") — that
  reading *is* finding V1.
- **`deliverable/tools/presence_check.py`**, 152 lines changed. `VERIFIER-121.md` §4 is a
  code-level read of it, including the `VIDEO_PATH_RE` defect.
- **`deliverable/tools/selftest_presence_check.py`**, 61 lines added. `VERIFIER-121.md` finding 1
  ran it and recounted its assertions by AST parsing.

The intended scope is plainly the bundle's *data artifacts* — the semicolon that follows joins it
to "the corrected artifacts are new files carrying their date in their name", and for those
artifacts the claim is true, which I verified file by file. But as written it is a categorical
claim about the repository, it is false, and it is contradicted by §5 and §6 of the same document.
Under `PROTOCOL.md` ("the verdict is only good for the exact state it was run on") this is exactly
the sentence a later reader would rely on. One-line repair: narrow it to the bundle artifacts.

### Finding 3 — NOT BLOCKING. A quotation attributed to the wrong document
**`DRIFT-122.md` lines 23–24:** "the session-120 errata (E6) say *"three days apart"*".

E6 is `deliverable/GAUNTLET-2026-08-15.md` line 47 and it says "three days **earlier**". The string
"three days **apart**" appears at `CONDITIONS-120.md` line 38, in the V1 disposition row — a
different document. The substance (a round number against the measured 2.6803) is unaffected, and
both texts are in the record; only the attribution is wrong.

### Finding 4 — NOT BLOCKING. The live run does not record which baseline it read
**`functional-test-122.json`.** The file records `tool`, `tool_version`, list, vantage, probe,
confirmation policy and `baseline_currency.declared_t_ref_utc`, but **no baseline file path**
(`baseline_note` is `null` and there is no path field). I identified the table by arithmetic: the
expectation and both CI bounds match `reference-baseline-CORRECTED-2026-08-16.json` exactly, and do
not match `presence-baseline.json` (whose `t_ref` is 2026-08-12T03:40:00Z and whose cells are
494/775/790/673/461/382). A third party could not do that from the artifact alone. Recording the
resolved baseline path and its sha256 in the output would close it.

Worth stating plainly, since §5 does not: the "+0.0000 pp" demonstration is computed against the
**corrected** table, which is not part of the shipped bundle. That is the right table to use; it
just is not the one a receiver holding bundle v0.1 would get.

### Finding 5 — NOT BLOCKING. "eight sessions" is uncited
**`DRIFT-122.md` line 176.** The document gives no basis. The record supports it:
`presence_check.py` carries "Session 113, 2026-08-12" in its own header, and the defect was first
named at session 120 (E6) — 113 through 120 inclusive is eight. Checkable, but the reader has to
assemble it.

### Finding 6 — NOT BLOCKING. One assertion in selftest section 8 is a restatement, not a test
**`deliverable/tools/selftest_presence_check.py`**, the last check of section 8:

```
check_true("the staleness threshold is the measured one, not a round number",
           pc.STALE_AFTER_DAYS == 26, pc.STALE_AFTER_DAYS)
```

This asserts a module constant against a literal. It cannot fail unless someone edits the constant,
and — despite its name — it does not check the threshold against the measurement, because it never
reads `drift-122.json`. It is a change-detector, not a test. **The other 13 assertions of section 8
are real:** they build a synthetic baseline with hand-chosen cells (0.10 and 0.30), construct a
19-digit identifier whose decoded creation time is exact and which sits two months inside the 4-5y
band, and then check hard-derived outcomes — a 120.0-day clock gap, histograms {4-5y:1} then
{5y+:1}, expectations 0.10 then 0.30, a signed drift of exactly 20.0 pp, zero drift on the
reference day, and four distinct `None` paths. I confirmed the value 26 independently anyway (my
own crossover search gives 26), so the constant is right; only the assertion is weak.

### Finding 7 — NOT BLOCKING. A stale code comment
**`drift_122.py` line 240:** "How many individual units change band over those 3.01 days" — the
measured gap is 2.6803 days. Comment only; it does not reach any output or the document.

### Finding 8 — NOT BLOCKING. The rebuild is deterministic except for its own clock
Noted for completeness rather than as a defect: `built_utc` in `MANIFEST.json` and the generation
stamp in `FIGURES.md` change on every run, so the bundle is not byte-reproducible across runs. The
document makes no determinism claim, and every *number* is stable.

### Finding 9 — NOT BLOCKING. The one outside-world claim carries its source elsewhere
Answering the standing question — is anything in `DRIFT-122.md` a claim about the outside world
that needs a source and does not have one? Almost the whole document is about files in this
repository. The single external claim is §4's "the receiver's own eleven identifiers — a real
external list this house did not choose". Its source is in the record but not in this document:
`receiver-list.txt` header cites `https://playground.tiktok-audit.com/api-na/`, read 2026-08-12
(session 112). The live endpoint and vantage of §5 are recorded with their sources inside
`functional-test-122.json` (`https://www.tiktok.com/oembed?url=`, `https://ipinfo.io/json`).
No other sentence in `DRIFT-122.md` asserts anything about the world.

---

## What I could not check, and why

1. **`https://playground.tiktok-audit.com/api-na/`** — the origin of the receiver's eleven. NOT
   CHECKED: I did not make any network request during this review. The identifiers I used are the
   ones in `receiver-list.txt`, and the claim I verified is arithmetic on them, not their
   provenance. That the eleven were read from that dashboard on 2026-08-12 rests on a session-112
   record I did not re-fetch.
2. **The live probe results in `functional-test-122.json`** — the ten `RETRIEVABLE` and one
   `NOT-RETRIEVABLE` readings. NOT CHECKED against the endpoint: re-running the probe would be a
   new measurement at a different time, not a verification of that one. What I did check is that
   every *derived* figure in that file is correct given its own recorded observations.
3. **The exact pre-commit text of `DRIFT-122.md`** — Finding 1 could not be resolved further
   because no intermediate state exists on disk or in git. I report what the tool returns on the
   committed file and on the closest reconstructions, and I do not speculate about which text
   produced 60/11.
4. **Whether session 120 and 121 reviewers read files beyond those named** — I checked
   `VERIFIER-120.md` and `VERIFIER-121.md` for the three files Finding 2 names and stopped there;
   the finding needs only one counterexample and has three.
5. **The `.partial` files and the day-6 run** — outside the stated scope of this review.
   `ledger/day6-stdout.txt` is empty and `ledger/day6-stderr.txt` is one line; I did not evaluate
   the day-6 move, and `DRIFT-122.md` makes no claim about it.
6. **The correctness of the Wilson interval implementation** in `power_audit.wilson`. NOT
   INDEPENDENTLY RE-DERIVED: I verified that the CIs in the corrected artifacts are reproduced by
   the shipped code and that the receiver-eleven CI bounds propagate correctly through the
   expectation, but I did not re-implement the Wilson formula. No figure in `DRIFT-122.md` depends
   on a CI.

---

*Recomputation scripts for this review were written to a scratch directory outside the repository
and are not part of this commit. Nothing in the repository was modified by this review. This
verdict covers commit `95ab278` and nothing after it.*
