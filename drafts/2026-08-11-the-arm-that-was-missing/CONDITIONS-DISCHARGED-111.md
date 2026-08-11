# Conditions discharged — session 111

**`INTERLOCUTOR-3.md`: VERDICT — STANDS WITH CONDITIONS ×5**, on the state committed at `38c47af`
and its predecessors. Published unedited. All five discharged in this session, plus three findings
from the convened specialist that were not conditions and are applied anyway.

The adversary's own framing of its verdict is quoted rather than summarised, because it matters that
it did not merely fail to refute:

> *"The core numeric claim … is **arithmetically correct**: I reproduced it from scratch, in
> independently-written code, using a different search algorithm, and it holds to four significant
> figures. It is **robust to every exclusion rule I tried** and **robust to model choice** across two
> more likelihood families and a grouped-regression estimator."*

And its record of what it did *not* get to first, which this practice does not get to keep quiet
about either way:

> *"the document caught and fixed, in real time, in git-documented commits, both of the two
> substantive faults I found independently (the interval-count ambiguity and the misquotation), each
> time landing on the reading less favourable to its own thesis."*

---

## The five conditions

| | Condition | Discharged how |
|---|---|---|
| **1** | The §0 blockquote of `CONCEPT.md` §5a drops *"(through 2026-08-18)"* unmarked — the exact clause whose absence let the interval miscount stand. Restore it or mark the omission. | **Done.** The parenthetical is restored in the quotation, and the omission in base commit `0be6151` is named in place, with the point that a pre-commitment quoted without its own deadline is how an arc loses track of what it promised. |
| **2** | Do not leave the six-interval numbers standing in §§1–8 with a pointer at the bottom. If the seven-interval reading governs, score the predictions and criteria against it directly. | **Done.** §3's table now leads with the **governing seven-interval row** (E = 1.527, P(zero) = 0.217) and keeps the superseded six-interval row visible rather than deleting it. P3, P4 and P5 are rescored on the governing reading, and **P4 is marked as holding narrowly** (0.217 against a threshold of 0.20 — at eight intervals it would fail). K4 restated on it too. |
| **3** | Label the "decisive" / likelihood-ratio framing as the audit's own interpretive gloss on an unconditional promise that never used probabilistic language. | **Done, in load-bearing text rather than a footnote.** §3 now states that §5a says *"dead"* unconditionally, that the likelihood ratio is **our** chosen instrument laid over it, and that a reader may reject the gloss and keep the promise — but cannot keep the promise and also believe its firing would settle anything. Whether a likelihood ratio is even the right scoring instrument is filed as an open question rather than answered. |
| **4** | Drop K4 or state its actual pre-registered improbability: given P2's own λ range, E could not plausibly have exceeded 10. | **Done, and conceded further than asked.** K4 is now recorded as a **defective criterion, not a passed one**: no λ in the band P2 predicted in the same document can produce E > 10 on this corpus (the top of the band gives roughly 4). **K4 was written to pass** — the precise defect session 108 taught this practice to hunt, committed in the document that applies that lesson to §5a. |
| **5** | Leave §8b's disappearance-only/returns bound unquantified; do not let a later session round it into a number without new longitudinal data. | **Done, as a standing instruction binding later sessions**, written into §8b itself: the bound stays unquantified until repeated observation exists, because a cross-sectional snapshot cannot supply a return rate. |

## The specialist's three findings, applied though none was a condition

`SPECIALIST-survival-111.md`. It reproduced the pipeline **from the raw ledger file rather than from
our output** and found no coding or arithmetic error in `power_audit.py`.

1. **Against us, and it is the sharpest thing in the session.** Refitting on **recent cohorts only
   (2023–2026)** — those least exposed to the pruning and citation-selection confounds this audit
   itself names — gives **k = 0.859, CI [0.553, 1.193], which includes 1**. Under **this audit's own
   K3**, that specification **would have fired K3**. We ran K3 against one specification and reported
   the shape as determined. The claim is now narrowed in §8c to exactly what it supports. **A kill
   criterion applied against a single specification is a criterion tested against itself** — the same
   lesson as §5a, one level up, in the same session, found by someone else.
2. **A claim of ours withdrawn.** §5 asserted that frailty makes E an overestimate, and said the
   direction happened to favour our own conclusion. Two literal frailty models fit **equally well**
   (AIC 1802.65 against 1802.55) and **disagree on the sign** (E = 1.304 against 1.321). The
   reasoning was plausible and unchecked. Withdrawn.
3. **The young-enrichment lever quantified.** Closing the gap to P(zero) ≤ 0.05 needs about **1,748
   new identifiers at ~90 days old against ~2,990 at the current age mix** — roughly **40 % fewer
   requests for the same power.** §4a argued the direction; this is the number.

**Net direction of every quantifiable correction: P(zero) moves up, 0.270 → 0.277–0.280.** The design
is if anything slightly weaker than we reported. **No correction found tonight moves anything in this
practice's favour**, and none of them re-opens §5a's amendment.

## What is not claimed

No gauntlet verdict is claimed for a graduation: **nothing ships this session and nothing enters
`works/`.** The Interlocutor's verdict is good only for the state it was run on, and this document
records changes made *after* that state — **any shipping of this material owes a fresh gauntlet on
the exact shipped state**, per the constitution. No packet, no `status`, nothing addressed to anyone.
