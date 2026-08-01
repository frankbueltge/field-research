# Verification — published in full

*The Verifier, convened 2026-08-01 against the frozen state of this draft, independently of the hand
that built it. Its report is reproduced without edit. The disposition follows and does not alter it.*

**Note on what this verdict covers.** It was run on the state before the Interlocutor's four
findings and the Verifier's own seven were executed. Under this practice's constitution a verdict is
good only for the exact state it was run on, so **this verdict does not cover the current state of
the directory** and nothing here may ship on it. That is not a defect of the verification; it is
what a verdict is.

---

# VERIFICATION REPORT — "What the Record Rests On"

## Verdict: **PASS WITH FINDINGS**

All four headline weighted estimates, the full population inventory, and nearly every specific count
in the prose reproduce exactly under independent re-derivation from raw data — including from the
actual pinned snapshot, whose SHA-256 I verified myself against a copy of the file that happened to
already be present locally. The external literature citations resolve and their quoted figures
(especially the five Pew numbers and the Reyes Ayala 9.6%/33.2%/25.1% table) check out precisely. I
found no fabrication. I did find several real, checkable errors in the prose — none of which touch
the four headline numbers, but one of which (Finding 2) violates the instrument's own stated
statistical discipline.

## What I independently re-derived (all matched)

Using my own script, reading `inventory.json`, `sample.json`, and `probe-2026-08-01.json` directly —
not by re-running `analyse.py` — and separately reading `reports.csv` straight out of the pinned
snapshot (`sha256 fa13c20…` confirmed byte-for-byte):

- Population: 7,408 total rows, 6,602 included, 806 excluded (805 `variant:unreviewed` + 1
  `variant:approved`), 6,541 distinct URLs, 119 records over 58 shared URLs, 6,358 English — all
  exact.
- Age distribution and "2,036 of 6,602 sourced records published 2025/2026" (1,448 + 588) — exact.
- Integrity classes: 19 bad-date-order records, 46 register-stand-in records — exact, including
  report 2587's "Lorem ipsum" text and report 3205's substantive text, both confirmed by direct read.
- Headline estimates: hard-gone 2.714% [1.11–4.32], withheld 23.615% [16.72–30.51],
  still-holds-of-served 95.158% [92.14–98.17], still-delivers 64.344% [56.83–71.86] — all match
  `results.json` to 3+ decimal places, including the stratified variance, finite-population
  correction, Kish design effect (1.643) and effective n (158.2).
- Archive coverage 97.96%→98.0% and precedence 90.12%→90.1%, with the precedence estimate correctly
  dropping flagged bad-date records (verified for report 357 and 2167 specifically, and the resulting
  n=17/20, k=15 in the 2019 stratum matches exactly).
- Calibration counts: 97 sent, 63 decidable, 53 holds, 44/82 of NOT_APPLICABLE, 8 archived-absent,
  the five ABSENT report numbers (121, 488, 796, 6881, 1521) with their listed overlaps — all exact.
- The 7 user-agent flips (57, 93, 1215, 1751, 2612, 3456, 7059) and 24 CDX_UNAVAILABLE (9.2%) —
  exact.
- Fingerprints: spot-checked 6 random sampled records plus report 121 by recomputing shingle hashes
  independently from raw CSV text — all matched.
- `build_inventory.py --check` against the actual pinned snapshot passes (byte-identical rebuild).
- MANIFEST.json's licence claim matches the snapshot's own `license.txt` verbatim in substance.

## Findings

**1. NON-BLOCKING — `FINDINGS.md`, "Age" section: "against 11 to 15 of 20 in every other stratum."**
Independently computing the "still delivers the stored passage" count per stratum from
`probe-2026-08-01.json` gives: 2015:12, 2016:14, 2017:14, 2018:14, **2019:10**, 2020:15, 2021:13,
2022:13, 2023:14, 2024:12, 2025:13, 2026:11. The 2019 stratum is 10, outside the stated 11–15 range.
Fix: change to "10 to 15."

**2. NON-BLOCKING — `FINDINGS.md`, "The vantage measured itself" section: "would lower the withheld
rate by roughly 2.7 points."** Of the 7 records that flipped to 200 on the honest-string retry, only
2 (reports 2612, 7059) were originally in the `withheld` class (401/402/403/451); the other 5 were
generic 4xx/other, not part of that indicator at all. Reclassifying just those 2 and recomputing the
same stratified-weighted estimator used everywhere else in the instrument gives a delta of **~1.87
points**, not 2.7. The figure 2.7 appears to come from the unweighted raw count of all 7 flips over
260 (7/260 = 2.69%) — an unweighted bare percentage applied to a claim about the weighted corpus
rate, which is exactly what METHOD.md says this instrument "does not print." Fix: either state ~1.9
points (restricted to the 2 actually-withheld flips, properly weighted) or rescope the sentence to
"the does-not-answer-200 rate" (whose correct weighted delta is ~3.3 points — still not 2.7).

**3. NON-BLOCKING — `METHOD.md`, literature section: "the paper that gave the field the term
*content drift*"** (attributed to Jones et al. 2016). I read the actual paper (fetched from PLOS
ONE). It states outright: *"The Hiberlink project coined the term Reference rot to denote the
combination of two problems,"* of which content drift is one component defined there, not coined
there. The term predates this paper by the paper's own account. Fix: attribute the term to the
Hiberlink project, or drop the coinage claim.

**4. NON-BLOCKING — undisclosed denominator composition.** The task asked specifically whether SHELL
sits in the "still holds" denominator and whether the prose says so: it does, and it doesn't.
`analyse.py`'s `in_l3_scope()` includes SHELL (200-response, <100 extractable words) in the
denominator for the 95.2%/2.0% figures, but excludes BOT_WALL/NO_HELD_TEXT/NON_HTML/
REGISTER_STAND_IN. The two headline rows in `FINDINGS.md`'s summary table sum to 97.2%, not 100%
(n=176 in scope: 162 HOLDS + 5 ABSENT + 2 PARTIAL + 7 SHELL); PARTIAL and SHELL fill the missing
~2.8% with no row or footnote explaining it. Fix: add a line disclosing that SHELL and PARTIAL sit
inside the denominator, or give them their own rows.

**5. NON-BLOCKING — `FINDINGS.md`: "Two further pages … hold the passage in full."** Direct
inspection of the calibration records for the 7 SHELL cases shows **three**, not two, scored
`ARCHIVED_COPY_HOLDS` (reports 953 and 2034 at overlap 1.0, and **1878 at overlap 0.83**, which
clears the ≥0.50 `HOLDS` threshold used everywhere else in the instrument). The sentence is
defensible only under an undisclosed stricter "exactly 1.0" reading of "in full," inconsistent with
the document's own stated threshold. Fix: say "three further pages … hold the passage" (consistent
with ≥0.50), or explicitly define "in full" as 1.0 and reconcile why 1878 is excluded.

**6. NON-BLOCKING — minor citation nit.** `METHOD.md` cites "Bowers, J., Stanton, C., Zittrain, J.
(2021)"; the paper's actual byline (confirmed via SSRN/Berkman Klein listings) is Zittrain, Bowers,
Stanton — author order only, no other error. Identifiers, title, and year are all correct.

**7. NON-BLOCKING — trivial spelling.** MANIFEST.json refers to the snapshot's "licence.txt"; the
file inside the snapshot is actually named `license.txt`. Content matches exactly; filename spelling
only.

## What I could not check

- The Perma paper's specific framing ("the earliest large study to separate 'returns 200' from
  'still holds the cited material', by hand") — I confirmed the paper's topic, authors, year, and
  headline percentages (70%/50%) from the Cambridge listing, but the fetch did not surface enough of
  the body text to confirm or refute the specific methodological characterization.
- I did not exhaustively grep every file in the repository for stray mentions of the two
  withheld/unread citations (Nyayachavadi et al., Bowers/Stanton/Zittrain) — I confirmed no figures
  from either appear in `METHOD.md` or `FINDINGS.md` (the only two files that discuss them) by
  reading both in full.
- I did not re-run the live probe (correctly out of scope — the live web moves and a fresh probe
  would not, and should not, match). I also did not re-query the Wayback CDX index live to double
  check individual capture timestamps; I checked internal consistency of the recorded CDX data
  against the flag-exclusion logic instead.
- `probe-2026-08-01.json` (462 KB) was queried and sampled programmatically rather than read
  end-to-end; I targeted every class and record referenced in the prose rather than reading it
  linearly.

## Note on scope

Per the brief, I am not treating "draft, not shipped" or "the live probe isn't reproducible" as
findings — both are already disclosed and are not defects. I did not find any place where the prose
treats the one-day probe result as a stable property of the world; the "one vantage, one day" caveat
and "conjecture, not a finding" framing (age/withholding correlation) are both present and correctly
hedged.

---

## Disposition — all seven executed

Written by the conductor. Every finding was applied; none was argued with.

1. **"11 to 15" → "10 to 15."** Applied. The 2019 stratum is 10.
2. **The 2.7-point figure.** Applied, and it is the finding of this verification. The paragraph now
   gives **1.87 weighted points** for the withheld rate and **3.32** for the does-not-answer rate,
   both recomputed here with the same stratified estimator and both matching the Verifier's numbers.
   The error is named in the document where it happened: an unweighted 7/260 printed as a weighted
   delta, in the one paragraph about the instrument measuring itself, inside a work whose method file
   says it does not print bare percentages.
3. **The coinage claim.** Applied. The line now attributes the vocabulary to the Hiberlink project,
   quoting the paper's own sentence, and no longer credits the 2016 paper with the term.
4. **The denominator.** Applied. `FINDINGS.md` now states, under the table, that the 176-record
   denominator also holds 2 `PARTIAL` and 7 `SHELL` records that appear in neither row.
5. **"Two further pages … in full."** Applied. It is **three**, at 1.00, 1.00 and 0.83, against four
   that do not hold or could not be fetched. The stricter reading was undisclosed and is withdrawn.
6. **Author order.** Applied: Zittrain, Bowers, Stanton.
7. **`license.txt`.** Applied in `MANIFEST.json` and `METHOD.md`.

**What this leaves.** Findings 2 and 5 are the same species of error and both are in this
practice's favour when made: a delta that sounds larger, a class that sounds cleaner. Neither
changed a headline number, and the Verifier said so plainly. What it also means is that the four
numbers a reader would quote survived independent re-derivation from the raw snapshot by a different
hand and a different code path — including the variance, the correction and the design effect — and
that is the part of this report that matters most.