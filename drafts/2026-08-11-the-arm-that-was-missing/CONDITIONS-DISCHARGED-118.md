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
| 6 | the conditioning bias has a measurable direction | §2's closing caveat **withdrawn and replaced**; the sweep published as a table | live-account cell rate **0.0622–0.0717** against an unconditional **0.11566**; conditioned ratio **9.77–11.25**; **6.05 is a conservative floor** |
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
   null result on T is a null result" is retained *with that limit stated here*, and it is the
   weakest load-bearing step in the section.

## What is not claimed

Nothing shipped, nothing graduated, no packet. The Verifier's report is good only for
`INCREMENT-8.md` §§1–6 at `5c65e5d`, and this document changed that state — **anything that ships
owes a fresh gauntlet on the exact shipped state.**
