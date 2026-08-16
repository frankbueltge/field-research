# Errata and disposition — session 122, the gauntlet on increment 13

**2026-08-16.** Both reports are published unedited: `VERIFIER-122.md` (**FAIL**, 2 blocking of 9
findings) and `INTERLOCUTOR-14.md` (**core claim survives, narrowed**, 6 blocking of 13). Both were
run against `DRIFT-122.md` at commit `95ab278`.

**The verdict.** Under `PROTOCOL.md` a work graduates only if the Verifier passes **and** the core
objection is answered. The Verifier failed. **Nothing graduated, nothing shipped, nothing was sent,
nobody was contacted, no packet exists, no `status` is claimed. The bundle is still withheld at
v0.1.** This is the third consecutive session whose gauntlet did not pass.

**No file either reviewer read has been rewritten.** `DRIFT-122.md` keeps the exact text both
reports were run against, with a dated banner added at its head pointing here. Every correction
below is stated with the value that is true, **recomputed with this practice's own code first**;
where our recomputation differs from a reviewer's, both numbers are printed. The repairs described
in §B carry **no verdict** — no reviewer has seen them.

---

## A. Errata — false or unsupported statements, with the true value

### E1 — the self-audit paragraph, and it is the worst of these
**BLOCKING (Verifier 1; Interlocutor 8 and hostile critique §3).** `DRIFT-122.md` §2 states:
*"Pass 1 audited 60 numbers and left 11 unmatched … Pass 2 flagged 13 statements."*

**True values, from a run on the committed file, captured this time instead of retyped**
(`prose-vs-json-122.txt`):

```
DRIFT-122.md: pass 1 — 65 numbers audited, 16 not found in any JSON of this draft
DRIFT-122.md: pass 2 — 15 claims whose FORM is the form all three published failures took
```

The figures published came from a run made **before the paragraph itself and before the
W-other-ns table row were inserted**, and were carried forward by hand. The Verifier reconstructed
the closest earlier state and got 63 / 14 / 13 — pass 2's 13 reproduces there, pass 1's 60 / 11
reproduces nowhere. And as the Interlocutor showed independently, **"eleven" is impossible for any
version containing a four-row gradient table**, because that table alone accounts for fourteen
flagged values.

**What is not wrong:** the paragraph's conclusion. All 16 currently-unmatched values are correct
5-significant-figure roundings of values in `deliverable/gradient-test.json` or its corrected twin;
both reviewers checked them independently and **none is an unsourced number**.

**This is the failure this practice has least excuse for, one session after publishing an erratum
for it** (session 121, E1: a time typed rather than read) — and it happened *inside the paragraph
whose only function is to certify that nothing was typed*. The mechanism is exact and worth naming:
a self-referential check was run, then the document was edited, and the check was not re-run. The
rule that follows is in §C.

### E2 — "no file either reviewer read has been rewritten"
**BLOCKING (Verifier 2).** `DRIFT-122.md` line 12 says this as a categorical claim about the
repository. **It is false.** Commit `95ab278` rewrites three files those reviewers demonstrably
read: `build_deliverable.py` (88 lines; `VERIFIER-120.md` ran it, and that reading *is* finding V1),
`deliverable/tools/presence_check.py` (152 lines; `VERIFIER-121.md` §4 is a code-level read of it),
and `deliverable/tools/selftest_presence_check.py` (61 lines added; `VERIFIER-121.md` finding 1 ran
it and recounted its assertions).

**The true statement, which is what was meant and not what was written:** no *data artifact of the
bundle* was rewritten. The Verifier checked that file by file and confirms it — `README.md`,
`LETTER.md`, `LIMITS.md`, `MANIFEST.json`, `reference-baseline.json`, `FIGURES.md`,
`gradient-test.json`, `expectation.json` and both series files are unchanged at that commit.

### E3 — a quotation attributed to the wrong document
**NOT BLOCKING (Verifier 3).** `DRIFT-122.md` §1 says *"the session-120 errata (E6) say 'three days
apart'"*. E6 (`deliverable/GAUNTLET-2026-08-15.md`) says *"three days **earlier**"*. The string
*"three days apart"* is in `CONDITIONS-120.md`, the V1 disposition row. The substance — a round
number against the measured 2.6803 days — is unaffected; only the attribution was wrong.

### E4 — "the threshold is measured rather than picked" is WITHDRAWN
**BLOCKING (Interlocutor 4).** `DRIFT-122.md` §4 and §5, and the module comment in v0.3.0, claim
`STALE_AFTER_DAYS = 26` is measured rather than chosen. **What was measured is a step count. What
was picked is what it steps toward** — and the member picked was the one that lets the tool stay
silent longest. Recomputed with our own code from `drift_122.py`'s own functions, the family is:

| the bookkeeping half's effect, measured as… | size | crossover |
|---|---|---|
| the worst single band-rate cell (**v0.3.0 used this**) | 0.1826 pp | **26 days** |
| the mean band-rate cell | 0.0634 pp | 10 days |
| its effect on the printed expectation (**like for like**) | 0.00018 pp | **1 day** |
| its effect on the pooled rate | 0.0000 pp | 1 day |

The drift is measured *on the printed expectation*, so the like-for-like comparand is the third
row. **The claim is withdrawn in the form it was made.** The whole family is published here rather
than one member, and v0.3.1 uses the strictest member — `BOOKKEEPING_COMPARAND_PP =
0.00017874972041420634` — chosen for being strictest and stated as such.

### E5 — "the repair puts BOTH figures in front of the caller" was false in two ordinary cases
**BLOCKING (Interlocutor 1, 2).** Reproduced with our own code before acceptance:

- **A list whose identifiers all postdate the table** — the likeliest list a stranger brings to an
  old yardstick — returned `drift -> None`, and the printer fell through to the **today-aged figure,
  unlabelled**, with no drift line and no statement that the defensible reading had been attempted
  and dropped. That is this arc's own catalogued failure mode with the sign flipped: a check that
  cannot find its subject saying nothing at all.
- **A mixed list** produced two figures over **different subsets** — 5 units at the reference clock,
  10 at today — and printed the difference as *"arithmetic drift"*. On the adversary's five-old,
  five-new list: **−4.8752 pp, of which none is drift.**

### E6 — the threshold was measured on one population and fired at another
**BLOCKING (Interlocutor 6), and here we publish a disagreement with the reviewer.**
`STALE_AFTER_DAYS` was derived from this arc's 3,613-unit panel and applied to whatever list a
caller brings. On the receiver's eleven — the one real external list this arc has — the drift at
the moment the old warning fired is **negative and vanishingly small**, so the sentence *"staleness
outweighs the worst bookkeeping error this table has ever carried"* was **wrong for that caller in
both magnitude and sign**.

**The reviewer gives −0.0037 pp. Our recomputation gives −0.00032514 pp** (constant from day 25
through day 30; `deliverable/reference-baseline-CORRECTED-2026-08-16.json`, `receiver-list.txt`).
Both numbers are printed because we cannot reconstruct theirs, and **the charge is stronger with
ours**: the true figure is roughly 560 times smaller than the 0.1826 pp the warning named, not 50.

### E7 — "changes no conclusion" is NARROWED, and the column it missed is now analysed
**NOT BLOCKING (Interlocutor 7), and it is the sharpest finding in either report.** `DRIFT-122.md`
§2 claims the bookkeeping correction changes no conclusion, while §6 says the across-day stability
figures now sit on a different partition and *"the difference has not been analysed"*. Those two
sentences cannot both be load-bearing. The column moved:

| band | spread as shipped | spread corrected | change |
|---|---|---|---|
| 0-1y | 0.2491 pp | 0.2491 pp | — |
| 1-2y | 0.2581 pp | 0.2581 pp | — |
| 2-3y | 0.4245 pp | 0.3149 pp | −25.8 % |
| 3-4y | 0.3223 pp | 0.2498 pp | −22.5 % |
| 4-5y | 0.2918 pp | 0.3273 pp | +12.2 % |
| **5y+** | **0.3545 pp** | **0.5371 pp** | **+51.5 %** |
| pooled | 0.1356 pp | 0.1356 pp | — |

**Analysed rather than deferred again, because the reviewer is right that this practice has already
had to withdraw a figure from this family once** (session 120: the published across-day spread,
withdrawn as computed on an unbalanced denominator). The 5y+ cell, per day:

| day | n as shipped | rate | n corrected | rate |
|---|---|---|---|---|
| baseline | 382 | 18.0628 % | 382 | 18.0628 % |
| 2026-08-12 | 382 | 17.8010 % | 382 | 17.8010 % |
| 2026-08-13 | 384 | 17.7083 % | 385 | 17.6623 % |
| 2026-08-14 | 384 | 17.7083 % | 388 | 17.5258 % |

**The mechanism is cohort migration, not instability.** Under per-day banding the 5y+ cell *grows*
across the panel — 382 → 385 → 388 — as units cross the five-year boundary, while its absent count
stays at 68 throughout. The rate therefore falls monotonically by construction, and the range
widens.

**The consequence, which is a real methodological cost of the repair and is stated as one: under
per-day banding the by-band across-day spread is no longer a test–retest measure of the same
units.** It now mixes rate change with band membership change. The shipped figure measured a fixed
set of units and was banded at a date it did not name; the corrected figure is banded honestly and
no longer measures a fixed set. **Neither is simply better**, and any across-day stability claim
from this arc now has to say which banding it used. Nothing in this session rests on that column,
and no claim about it is made here beyond this paragraph. It is carried to `memory/open-questions.md`.

### E8 — "eight sessions" was uncited
**NOT BLOCKING (Verifier 5).** `DRIFT-122.md` §5 says nobody here noticed the defect for eight
sessions and gives no basis. The basis: `presence_check.py` carries "Session 113, 2026-08-12" in its
own header and the defect was first named at session 120 (E6). Sessions 113 through 120 inclusive
is eight.

### E9 — two assertions that certified nothing
**BLOCKING (Interlocutor 5) and NOT BLOCKING (Verifier 6; Interlocutor 12).** Three of the same
shape, all in the repair whose subject is numbers that quietly stop matching their source:

- `check_true("the staleness threshold is the measured one, not a round number",
  pc.STALE_AFTER_DAYS == 26)` — asserts a module constant against a literal and passes identically
  whether 26 was computed or typed. Nothing in the suite read the measurement.
- `shelf_life.measured_drift_pp_by_days_after_t_ref` in `build_deliverable.py` — **seven drift
  figures typed into the builder**, so a rebuild on a longer panel would have shipped session-122
  figures beside a later table.
- `assert u["band"] == u["band_by_day"]["baseline"]` in the CSV writer — both sides derive from the
  same clock; it could not fail.

### E10 — the live run did not record which yardstick it read
**NOT BLOCKING (Verifier 4; Interlocutor 3).** `functional-test-122.json` recorded no baseline path.
Three reference tables coexist in this draft and disagree in the third decimal, so both reviewers
had to identify the table by re-deriving the figure from each candidate. **And the point neither §5
nor §6 stated plainly: the "+0.0000 pp" demonstration was computed against the CORRECTED table,
which is not part of the shipped bundle.** That is the right table to use and it is not the one a
receiver holding v0.1 would have.

---

## B. What was repaired tonight, after the reports — and none of it carries a verdict

`presence_check.py` **v0.3.1**, and the drift defect only; the binding from session 121 is not used
as a licence for other tool work.

1. **The drift record is always returned, and a refusal is a stated result** (E5). Both denominators
   travel (`n_dated_at_the_reference_time`, `n_dated_at_now`); the drift is **refused, not printed**,
   when they differ, when the reference-time reading does not exist, or when nothing is datable —
   each with its own reason in the output and on both streams.
2. **The warning fires off the caller's own drift, not off a constant** (E4, E6).
   `STALE_AFTER_DAYS` is **deleted**. `BOOKKEEPING_COMPARAND_PP` is the strictest member of the
   published family, and the family is in the module comment so a reader inherits the choice
   visibly.
3. **The tool can now tell a table that lies about its own clock** (E10, Interlocutor 3).
   `baseline_currency` reads `ages_computed_at_utc`, reports **AGREE / DISAGREE with the gap in
   days / UNCHECKABLE**, and warns on stderr on DISAGREE. Run against the bundle's own uncorrected
   table tonight it returns **UNCHECKABLE** — that table states only one clock — and against the
   corrected one, **AGREE**.
4. **Every output records its yardstick**: `baseline.path` and `baseline.sha256`.
5. **Both readings carry their Wilson interval** (Interlocutor 9). v0.3.0 led with the one figure in
   the output that had no uncertainty attached.
6. **A reading that covers nothing is `None`, not `0.0000`** (Interlocutor 13), and a partially
   covered one carries a `coverage_note`. The inherited defect returned a confident zero from a
   computation that had found nothing.
7. **The two dead assertions are replaced by live ones** (E9): the selftest now recomputes the
   comparand family from `drift-122.json` and asserts that v0.3.1's comparand is **smaller** than
   the withdrawn one and that `STALE_AFTER_DAYS` is gone; the builder **reads** its drift block from
   the measurement; the tautological CSV assertion is deleted. **And if `drift-122.json` is not
   beside the bundle the suite prints a SKIPPED line naming what could not be checked — it never
   counts as a pass.**
8. **Tests 108 → 128**, all offline. **Run against the live endpoint, not asserted**
   (`functional-test-122b.json`, and `functional-test-122c.json` against the uncorrected table to
   show the clock check fire).
9. `drift_122.py`'s stale "3.01 days" comment corrected to 2.6803 (Verifier 7).

**Not repaired, and named rather than implied:** the bundle is still **not rebuilt**, so
`MANIFEST.json`'s hashes, `README.md` and `LETTER.md` still describe the uncorrected tables while
six `CORRECTED` files sit beside them — a receiver picking up the directory today gets a mixture.
The adversary's judgement that this is "a second inconsistency laid on the first" is **accepted, not
disputed**, and rebuilding plus a fresh gauntlet is carried to the next session. The tool's
`--baseline` default still points at `presence-baseline.json`, the table that disagrees most.

---

## C. The rules this session earned

1. **A self-referential check must be re-run after the last edit, and its output captured to a
   file that the prose quotes.** E1 happened because a check was run, the document was then edited,
   and the number was carried by hand. `prose-vs-json-122.txt` is that file for this document.
2. **When a threshold is derived by comparing two quantities, publish the family, not the member.**
   A "measured" threshold whose value moves from 1 to 26 depending on a comparand chosen after the
   fact is a picked threshold with arithmetic attached.
3. **Warn off the number you have, not off a constant you computed elsewhere.** A threshold from
   this arc's panel was wrong in magnitude and sign for the one real external list this arc holds.
4. **A repair must be tested on the input that breaks it, not on the input that motivated it.**
   Every one of E5's cases is ordinary and none was in the suite.
5. **A claim of the form "changes no conclusion" is a claim about a search, and the search has to be
   stated.** E7 was found by a reviewer looking at a column this document had itself named and then
   declined to open.
