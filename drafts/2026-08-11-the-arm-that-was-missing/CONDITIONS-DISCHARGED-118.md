# Conditions discharged — session 118, 2026-08-14

*The Verifier's report on `INCREMENT-8.md` §§1–6 at state `5c65e5d` returned **SOUND WITH
QUALIFICATION**, six prose-against-file mismatches and nine conditions. All nine are discharged
here, in the same session. **Every figure the Verifier computed in its own scratchpad was
recomputed with this practice's own code before it was printed in this arc's prose** —
`discharge_118.py` → `discharge-118.json` — because session 115 was caught printing an
adversary's number while its own file said something slightly different, and the rule adopted
then binds here.*

## What the Verifier could not break

Every headline figure reproduced under independently written code: the three non-zero shares, all
five Fisher exact p-values, the population rebuild **including the exact seeded draw of C2**, the
residual excess and its exact tail, the Mantel–Haenszel point estimate and its
Robins–Breslow–Greenland variance, the component count, both bootstrap seeds, the jackknife, both
catalogue counts and the arXiv record. It confirmed independently that the pre-registration
predates the run, that the population was honoured exactly, that none of the flagged article's
identifiers is multi-cited (so the known join ambiguity does not touch this analysis), and that
`PREDICTION-118-propagation.md` was committed at 03:46:44Z, ahead of every commit of the
increment.

## The nine conditions

| # | Condition | Discharged how | Our figure |
|---|---|---|---|
| 1 | **M1** — strike `10202` from the new codes | §1 rewritten; the error named as a claim of novelty contradicted by our own file **and** by the governing pre-registration | `10202` is in `account-state-probe-114.json`; **only `10222` is new** |
| 2 | **M2** — the census cost is the day-3 number | §2 rewritten | **2,740** distinct accounts on day 3 (2,744 is day 2) |
| 3 | **M3/M4/M6** — the p-value, the range, the split count | all three corrected in place, each naming what version 1 said | **p = 0.0111**; deff **1.5373–1.6046** over five seeds and the jackknife; **two** like-for-like comparisons, not three |
| 4 | **M5** — one definition per width column | table rebuilt in Wald widths, the percentile intervals stated separately beneath it | bootstrap Wald width **1.2466** (seed 7), against the **1.2334** percentile width version 1 printed in that column |
| 5 | "three independent routes" | rewritten as **two routes, one run at five seeds**; three further seeds run for this discharge | 11 → **1.5727**, 12 → **1.5659**, 13 → **1.5373** — the last **below** the floor version 1 published |
| 6 | the conditioning bias has a measurable direction | §2's closing caveat **withdrawn and replaced**; the sweep published as a table | live-account cell rate **0.0622–0.0717** against an unconditional **0.11566**; conditioned ratio **9.77–11.25** — **superseded the same session by the addendum below, which propagates two further error sources and gives 7.88–11.73**; **6.05 is a conservative floor** |
| 7 | disclose the draws that drop a stratum | disclosed in §5 with the count per seed and the reason `degenerate_draws` misses them | **64, 69, 69, 70, 76 of 4,000** — 1.60 % to 1.90 % |
| 8 | isolate statistic from key before making the rule binding | computed on the same units and the **same component key**, published in §5 | absence proportion **2.1908** against log OR **1.5373–1.6046**; account key 1.4961, page key 1.9995 |
| 9 | the atlas negative, term by term | §6 rebuilt as a per-term table with every hit named | 0 on account suspension / deplatforming / takedown / deletion; **1** on *banning* (facial-recognition bans), **1** on *moderation* (moderators as researchers), **2** on *censorship* |

## The qualification we accept without a fix

**"Age-standardised" is the wrong word for this page.** All 22 units sit in one cell, so the
Poisson-binomial is exactly a binomial and nothing is standardised. Stated in §2; the scan is
age-standardised, this page is not, and the phrase overstated the arithmetic.

## The three observations nobody asked the Verifier for, and what we do with them

1. **The cell's reference rate is structurally a share of all-or-nothing accounts** — 349 of 415
   off-page units belong to accounts with zero absent units and 43 to accounts with every unit
   absent. The page's excess is therefore, structurally, an excess of *all-gone accounts*
   (14 of 20), not an excess of absence within accounts. **Accepted, and it is a different
   mechanism from the one §2's prose implies.** Filed in `memory/open-questions.md`; not resolved
   tonight.
2. **The exact tails assume unit independence in a corpus this arc has established is clustered.**
   Accepted. The exposure is mild here — the 10 live-account units span 9 accounts, the 22 page
   units span 20 — but the inconsistency with §5's own new rule is real, and **§2's tails are the
   first thing that rule will be applied to** once the window closes on 2026-08-18.
3. **Q4 is near-maximal by construction**, because C1 and C2 are defined by the very outcome the
   state field is tested against. **Accepted as a limit on what Q4 licenses**: it shows the field
   is not noise; it does not establish power at the level of a single page. §1's sentence "so the
   null result on T is a null result" was retained here *with that limit stated* — and the
   Interlocutor then required it struck outright (addendum, condition 6). **It is struck**; what
   the run licenses is that T and C1 do not differ by roughly 35 points or more.

## What is not claimed

Nothing shipped, nothing graduated, no packet. The Verifier's report is good only for
`INCREMENT-8.md` §§1–6 at `5c65e5d`, and this document changed that state — **anything that ships
owes a fresh gauntlet on the exact shipped state.**

---

# Addendum — the Interlocutor's twelve conditions

*`INTERLOCUTOR-10.md`, published unedited, on the state committed as `dd90725`. Its verdicts:
**C1 survives, its presentation does not; C2's conclusion survives, its stated numbers are
refuted; C3's narrow claim survives its hardest attack and comes out stronger, its general form is
refuted by measurement; C4's framing is refuted as counted.** All twelve conditions discharged the
same session. **Every figure below was recomputed with this practice's own code before it was
printed in this arc's prose** (`discharge_118b.py` → `discharge-118b.json`); where our number and
the adversary's differ slightly — the account-key design effects and the paired bootstrap, both of
which depend on draw counts and seeds — **the prose quotes ours and this note records that both
exist.***

## The one that matters, and it went through a Verifier and a nine-point discharge untouched

**Three `10222` responses return the full user object and a `uniqueId` matching the requested
handle** — `buzz_award`, `jere.ronkko`, `worldpadeltour`, all in C1 — and this document counted
them as *the account object is not served*. Confirmed by reading our own stored markers: of 102
responses, `0` → 69 with a user object, `10221` → 28 without, `10202` → 2 without, **`10222` → 3
with**. The pre-registration's binary (zero against non-zero) **stands as pre-registered and Q1–Q5
are scored on it**; the object-based reading is published beside it, and every affected figure with
it: **C1 41.46 % instead of 48.78 %, Q4 p = 1.348 × 10⁻⁴ instead of 9.128 × 10⁻⁶, Q3 p = 0.4141.**
No verdict changes. **The claim in our prose that non-zero means "the account object is not
served" is false for `10222` and is struck.**

The class of the error is what to keep: **we audited our prose against our files and never audited
our files against themselves.** A miscoded response sat in a column of stored booleans through a
probe, a derivation, a Verifier's gauntlet and nine discharged conditions.

## The twelve

| # | Condition | Discharged how | Our figure |
|---|---|---|---|
| 1 | `10222` misclassified | both classifications published in §1, the false sentence struck | C1 **17/41 = 0.4146** object-based; Q4 **p = 1.348 × 10⁻⁴**; Q3 **p = 0.4141** |
| 2 | §2 must reconcile with §3 | cross-referenced both ways; the contradiction stated in §2 | §3 rejects §2's weighting for one of its two categories at **p = 0.0111** |
| 3 | propagate the sampling error | sweep now runs over the exact interval **and** the mixed weight, under both classifications | P(live \| all-present) exact 95 % **[0.8347, 0.9940]**; honest ratio range **7.88–11.73**, against the 9.77–11.25 published; **sign-flip threshold 0.9482** now printed as the load-bearing number |
| 4 | the "unmeasured" category was measured | cited in §2 | **11 of 12** mixed handles at state 0 at session 114 |
| 5 | say what the §2 tail is | §2 rewritten | conditional expectation **7.2727**, P(≥ 7) = **0.7709**, Fisher on the page's 2×2 **exactly 1.0000**; dead side **9 of 12, tail 5.863 × 10⁻⁷** |
| 6 | strike the "null is a null" sentence | struck, replaced with what the run licenses | Newcombe **[−0.1926, +0.3028]** (pre-registered) / **[−0.1220, +0.3711]** (object-based); power **0.0798 / 0.2463 / 0.5719 / 0.8914** at 10/20/30/40 points |
| 7 | "never measured this statistic's variance" is false | withdrawn in §5, with the two files that refute it named | `INTERLOCUTOR-7.md`: **1.4124 / 1.4506** over cited handles, adopted at `RESTATEMENT-2026-08-13.md` L181 |
| 8 | withdraw "1.4289 was too small" | withdrawn; the sample named as the third confound | account-key log-OR design effect measured here **1.2883–1.3521**, *below* 1.4289 |
| 9 | fix "24 % to 27 %" and "three routes" | both corrected | **24.0 %–29.4 %**; **two** routes |
| 10 | matched estimators and the full key × statistic table | printed in §5; the general claim withdrawn | account **≈1.15**, page **≈1.25**, component **≈1.38** — an interaction, so a design effect belongs to a **(statistic, key, sample)** triple |
| 11 | an interval on both design effects | printed in §5 | gap median **0.5948**, 90 % **[0.0335, 1.2701]**, positive in **29 of 30**; ratio **1.3879**, 90 % **[1.0228, 1.7582]** |
| 12 | name the most influential component | named in §5 | it is the flagged article itself — 22 units, 19 accounts, Δ OR **0.1199** |

## The three we accept without a fix

1. **A6 — the account state is read backwards in time.** It was measured once, tonight, against
   absences observed yesterday and losses that predate this arc's first observation. C1 survives
   as a statement about the accounts' *present* state; the unqualified sentence *"whatever removed
   this article's cited evidence, it did not do so by removing the accounts"* asserts more than one
   snapshot can carry. **Accepted. Days 5–7 measure the five interface-disagreement units every
   day; a second account probe would give the arc its first two-point series and is not run
   tonight.**
2. **A4/A5 — the floor's sign is forced by Q4, not discovered.** Accepted, and it is why the
   0.9482 threshold rather than the ratio range is now the number §2 leads its robustness claim
   with.
3. **A7 — eight mixed accounts in the cell, eight requests, never probed.** They are the only
   category that would have tested the state field without selecting on an extreme. **The
   pre-registration excluded them by construction and nobody noticed the cost.** Filed for the
   next pre-registration, not smuggled into this one.

## What we do not accept

Nothing. Every attack that landed is discharged or accepted above. The hostile critique is
published unedited in `INTERLOCUTOR-10.md` §(c) and is answered in the journal, not here.
