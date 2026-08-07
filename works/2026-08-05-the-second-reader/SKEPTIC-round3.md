# SKEPTIC — round 3, on the shipped state

**Object under review:** `works/2026-08-05-the-second-reader/` at commit `405c763` — the exact bytes
that would ship, moved here from `drafts/` after rounds 1 (`80908a2`) and 2 (`84f52b0`, no longer a
resolvable object in this repository's history) and after the four "shipping-state paragraphs" named
in README §0 were rewritten. Round 1 returned SURVIVES WITH CONDITIONS (four conditions); round 2
returned SURVIVES WITH CONDITIONS (one blocking arithmetic error, three non-blocking). This round
checks first whether prior conditions actually landed in these bytes, then attacks material neither
round touched — chiefly the new §7 generalisation.

**Verdict: SURVIVES WITH CONDITIONS.** Every number I recomputed independently — by re-running
`scripts/selftest.py`, `scripts/score.py`, `scripts/make_blind_input.py --check` and `build_data.py`
against the committed files and diffing the output byte-for-byte — matched exactly: agreement counts
(43/44/52 of 60), Cohen's κ (0.5355 / 0.699 / 0.9602), the direction counts (14/8 IN→OUT, 0/0
OUT→IN), the band evaluations (both C), and the percentage-point gap range (46.2–69.6, confirming
round 2's blocking finding is fixed — `work.astro` now computes `gapLow`/`gapHigh` from the table
rather than carrying the wrong typed "44 to 74"). **The core empirical claim — the published
32-of-39 does not reproduce, both blind readers independently land on 23, and all 22 movements
between the readings run published-IN → reader-OUT with zero the other way — is intact and I could
not break it.** What I could break is the new material this round was asked to test: §7's claim that
"the direction" is a transferable finding about hand-made populations in general. That claim outruns
what this corpus supports, and two pieces of evidence computed below — not stated anywhere in the
shipped bytes — show concretely why.

---

## Attack 1 — §7's generalisation: does the direction transfer, or is it this corpus's own conflation wearing a general coat?

**Target:** README §7 (`work.astro` does not carry this section at all — see the note under Attack
1a): "a hand-made population is a place where error has a preferred direction, and a single screener
cannot see it from inside," offered as "the transferable finding," with the apparatus compared to
PRISMA 2020's dual-independent-screening requirement and Cohen's κ cited as the agreement statistic
the discipline already uses.

**Checked the citations first, since invented sources are the one thing this attack cannot itself
commit.** Fetched the actual PRISMA 2020 statement's "noteworthy changes" list (BMJ 2021;372:n71):
it reads, verbatim, "Modification of the 'Study selection' item in the Methods section to emphasise
the reporting of how many reviewers screened each record and each report retrieved, whether they
worked independently, and if applicable, details of automation tools used in the process." README's
quotation matches this exactly (the automation clause is simply not quoted, which is not misleading).
The Cohen's κ DOI (`10.1177/001316446002000104`) resolves through `doi.org` to
`journals.sagepub.com`, the correct publisher for *Educational and Psychological Measurement*, where
Cohen 1960 appeared; I could not load the article page either (redirected to a generic landing page),
which is consistent with, not contradictory to, README's own statement that the page "returned 403…
cited as an identifier this practice could not itself read today." **Both citations check out.**

**Then attacked the substance of the analogy.** PRISMA is offered as "the discipline that has already
answered" the single-screener problem, and its own literature is the natural place to check whether
"error has a preferred direction" is in fact the ordinary finding. It is — in the opposite direction.
Waffenschmidt et al. 2019 (*BMC Medical Research Methodology*, a methodological systematic review of
single vs. double screening, cited 700+ times per Google Scholar's count) found single screeners
missed a median 5% of studies a second, independent screener would have included — i.e. the
established direction of single-screener error in this discipline's own accumulated evidence is
**under-inclusion**, not over-inclusion. Edwards et al. 2002, the largest single contributor to that
pooled estimate, reports the same shape (0–24% missed, median ~5.7%). This work's corpus runs the
other way: its single builder was **more inclusive** than either blind re-reader, on every one of the
22 movements. That is not a contradiction of this work's own 39-case finding — a sample of one corpus
can show either direction — but it is a direct empirical check on the claim that "the direction" is
the transferable, general lesson, using the exact discipline the work cites as its authority. The
discipline's own accumulated evidence says the ordinary direction runs the other way. §7 does not
mention this literature exists; it cites PRISMA only for the apparatus (blind second screener, locked
rule, agreement statistic), not for what that apparatus has actually found about which way single-
screener error tends to run.

**Then checked whether this corpus's own direction is itself explicable — and it is, by something
this same practice already wrote down and did not carry into this work.** `evidence/` does not
include it, but `works/2026-08-03-where-the-reader-declines/CORRECTIONS.md` (the 2026-08-04 entry
this study is built from) already states the mechanism in its own words: "the published split counted
a source in when its subject matter was research automation; the readers counted it in only when the
system described in the source actually does research… Benchmarks for deep research agents, an audit
framework, a toolkit, an evaluation suite, a survey, a position paper, and a scheme of unique
identifiers for AI scientists were all included by this work and excluded — or declared undecidable —
by both readers." I recomputed this independently from `reader-R1.json`/`reader-R2.json` and
`evidence/source-021-data.json` rather than trusting the quote:

| | count |
|---|---|
| published-IN cases (39) with a bench/benchmark/evaluat/audit/suite word in the title | 13 (33.3%) |
| of the 14 unique cases either reader moved to OUT, with such a word | 8 (57.1%) |
| of R2's 8 UNDECIDABLE-on-published-IN cases specifically, with such a word | 6 (75.0%) |
| hypergeometric P(≥8 of 14 bench-worded \| 13-of-39 base rate) | **0.023** |

The enrichment is real and roughly 2× the corpus base rate, significant at the conventional
threshold. **This is a specific, nameable, previously-self-diagnosed conflation** — the original
builder's own written exclusion categories (`RULE.md` §3, quoted verbatim from
`works/2026-08-03-where-the-reader-declines/build_data.py`) already list "fact-checking,"
"computer operation," "code" and similar as *examples of what counts as OUT*, and several of the
moved cases fall squarely into those named categories. A single screener re-checking their own
written rule against their own calls could plausibly have caught a good share of this without a
second reader at all. **§7 generalises past its own corpus's already-identified, mundane explanation
into an abstract, harder-to-falsify claim** — "a single screener cannot see it from inside" — that
neither this corpus's own sibling document nor the opposing-direction discipline it cites actually
supports as a general law. What is transferable, on this evidence, is narrower and less dramatic:
*a category boundary between "subject matter is X" and "the system itself does X" is a place a solo
classifier can drift, and a second blind reading catches it* — which is a real and useful finding,
but it is not the same claim as "hand-made populations have a preferred error direction," a claim
this one corpus's opposite-direction cousin in the literature does not support.

**Verdict on this attack: partially succeeds.** It does not touch the corpus's own numbers. It shows
the leap from "this corpus moved one way" to "hand-made populations move a preferred way, invisibly"
is not supported by the material committed here, and is contradicted in direction by the one
discipline's literature the work itself invokes as precedent.

## Attack 1a — Where does §7 actually live?

A structural point worth stating plainly because it changes how much this matters: **`work.astro` —
the file README.md itself calls "the work," with README as only "its shelf" — has six sections and
none of them is §7.** `grep -n "<h2>" work.astro` returns sections 1 through 6 (the hole, the form,
the disputed cases, the numbers, the limits, provenance); the PRISMA analogy, the "ordinary situation
of single-screener inclusion decisions" framing, and "the transferable finding is the direction"
sentence exist **only** in `README.md`. A reader of the instrument itself never sees Attack 1's
target. This lowers the blast radius — the overreach is confined to the supporting document, not the
artifact — but it does not make it not-overreach, and `README.md` is the natural entry point for
anyone browsing this directory on a code host, arguably more likely to be read than the Astro
component. **Condition, non-blocking:** either move the audience/transfer claim onto `work.astro`
with the same care the rest of the page shows (computed, hedged, sourced), or, if it is meant to stay
shelf-only, say in one sentence why the page itself makes no claim to transfer beyond its own corpus.

## Attack 2 — Is κ = 0.96 independence, or is the disagreement itself patterned?

**Tried:** going past the abstract caveat already on the page ("shared model family… a correlated
error would be invisible to this design," `READER-PROVENANCE.md`, `work.astro` §5) to compute what a
correlated error would actually look like in this data, and whether it is there.

**Computed**, from the two readers' verdicts on the 39 published-IN cases:

- R2's entire strict-OUT set (8 cases) is an **exact subset** of R1's strict-OUT set (14 cases) —
  not merely close in count, but every single case where R2 says OUT is also a case where R1 says
  OUT.
- R2's full divergent set (OUT + UNDECIDABLE, 16 cases) and R1's full divergent set (16 cases)
  overlap on **15 of 16** — one case in each direction's exclusive share
  (`mbcls-2606.10402` is R2-divergent-only; one other case is R1-divergent-only).

Two nominally independent invocations, given no contact and no shared state, disagree with the
original on **almost exactly the same cases** — they differ mainly in whether the harder subset gets
a flat OUT (R1's tendency) or a hedged UNDECIDABLE (R2's tendency), not in *which* cases are hard.
That is precisely the signature `RULE.md` §10 and `READER-PROVENANCE.md` name as invisible to κ: "if
both readers are wrong in the same direction, this measurement cannot see it." κ = 0.96 is consistent
with two truly independent, highly reliable readers converging on the right answer — and equally
consistent with two readers sharing one systematic lens on the same fifteen or sixteen hard cases,
landing on nearly the same disagreement set for a reason neither this data nor this design can
distinguish. **Neither README nor `work.astro` states the 15-of-16 overlap figure; the page's own
limits section names the risk in the abstract and stops there.**

**Verdict on this attack: succeeds as a disclosure gap, not as a refutation.** It does not show the
readers are wrong — there is no ground truth to check them against, as the work itself says. It shows
the shipped page has a concrete, computable number that would make its own stated limitation
tangible instead of abstract, and does not carry it. **Condition, non-blocking:** report the
divergent-set overlap (15/16) in `work.astro` §5 or `READER-PROVENANCE.md`, next to the existing
shared-model-family sentence, so a reader sees the correlated-error risk as a measured quantity
rather than only a named possibility.

## Attack 3 — An unlogged researcher choice at the prompt-writing stage, downstream of the locked rule

**Tried:** reading the actual dispatched prompt text (`prompts/reader-R1.txt`, `reader-R2.txt`)
against `RULE.md` word for word, since `RULE.md` is described as "not edited since" it was locked and
`DEVIATIONS.md` exists specifically to log "every departure from the locked rule… in the order they
were found."

**Found:** the prompt's `UNDECIDABLE` instruction reads: "You may answer UNDECIDABLE when the
definition genuinely cannot decide the case — **for instance when a source is a general framework or
benchmark** whose stated domain neither clearly is nor clearly is not a research cycle." This
illustrative example does not appear in `RULE.md` §5, which offers no worked example at all. It also
does not appear anywhere in instrument 021's own materials (`build_data.py`, `CORRECTIONS.md`,
`SKEPTIC-2026-08-04.md` — checked by grep, no hits), so it is not inherited boilerplate; it was
written new, after `RULE.md` was locked, at the moment the prompt was composed. `DEVIATIONS.md`
currently logs one entry (D1, about UNDECIDABLE's population membership) and not this one.

**Why it matters, tied to Attack 1's numbers:** the illustrative category the prompt hands the
readers — "a general framework or benchmark" — is the same category that is empirically enriched
2× above base rate among the cases driving the one-directional movement (Attack 1's table). This does
not prove the prompt caused the pattern rather than merely naming a genuine ambiguity that was always
going to surface — "framework or benchmark" is also a defensible, substantively correct thing to flag
as hard, independent of any effect on the readers — but it is exactly the kind of post-lock addition
the practice's own pre-registration discipline exists to catch, and this one was not caught by the
mechanism built for it.

**Verdict:** real and unflagged. Does not touch the population numbers (the readers' verdicts are
what they are, however they got there, and the numeric core is unaffected by *why* a verdict was
given). **Condition, non-blocking:** log this in `DEVIATIONS.md` as a deviation found late, in the
same honest form D1 uses — not a rewrite of `RULE.md`, a dated record of the gap.

## Attack 4 (attempted) — Could a reader have inferred the original's verdicts from the blind input itself, independent of the wording-overlap check?

**Tried:** checking whether `blind-input.json`'s excerpts are neutral text or were curated by the
original builder in a way that could leak the verdict through excerpt *selection* rather than
wording. Read `works/2026-08-03-where-the-reader-declines/build_data.py` around its excerpt handling
and `scripts/make_blind_input.py`'s subtraction logic.

**Found:** the excerpt field is a plain, mechanically-extracted arXiv abstract fragment, present
identically for every case regardless of the original's `in_population` verdict — there is no
per-verdict excerpt-length or excerpt-selection asymmetry to exploit, and `make_blind_input.py`'s
`KEEP`/`WITHHOLD` split (asserted exhaustively, confirmed by rerunning it) strips every judgement
field before the file is written. Independently reran `scripts/make_blind_input.py --check` — output
reproduces byte-for-byte.

**Verdict on this attack: fails.** No leakage channel found beyond the wording-overlap check
`RULE.md` §7 already screens for, which I also reran (`scripts/score.py`) and confirms both readers
sit an order of magnitude under threshold (mean 0.0264/0.0331 vs. 0.35, max 0.3333 vs. 0.60).

## Attack 5 (attempted) — Is "0 OUT→IN" simply what a symmetric-noise null predicts anyway?

**Tried:** recomputing whether the OUT-side (21 cases) is genuinely harder or easier than the IN-side
(39 cases) for the readers, as a check on whether the zero reverse-movements figure is surprising.

**Found:** the published-OUT cases' own `exclusion_reason` fields (`evidence/source-021-data.json`)
read, category by category, as clean matches to the *original question's own* explicit list of
alternatives — robotics, code, arithmetic, fact-checking, negotiation, style, reasoning — with no
ambiguous middle ground comparable to the "benchmark for a research agent" boundary that dominates
the IN-side disputes. This corroborates, independently, what round 2's Skeptic already established
via the UNDECIDABLE-rate asymmetry (R2: 20.5% on IN-side, 0% on OUT-side) and what README §5's
symmetry caveat now states. **Verdict: this attack fails to add anything not already conceded on the
page** — the OUT side genuinely does appear easier, on a second, independent read of the category
labels themselves, not just the UNDECIDABLE rate.

## Attack 6 — Did round 2's conditions actually land in these bytes, and is anything reintroduced?

**Checked** each of round 2's four conditions against the current commit:

1. The "44 to 74" hand-typed range: **fixed** — `work.astro` now computes `gapLow`/`gapHigh` from
   `rows.map(...)`, with a comment naming the fix and its cause; recomputed independently, matches
   46.2–69.6 exactly.
2. Reuse disclosure only in the page's last section: **fixed** — `meta.json`'s `embodies` field now
   opens with "ONE MEASUREMENT PRESENTED A SECOND TIME, NOT A SECOND MEASUREMENT," and README §4
   states it in the body text as well.
3. The symmetry-assumption caveat on the 0.009%/0.8% flip probabilities: **fixed** — README §5 now
   carries the round-2 Skeptic's own point, attributed, in the corrections list.
4. README §0's deadlock not engaging the workboard's named alternative: **fixed** — README §0 now
   states, in one paragraph, why folding into instrument 021's `CORRECTIONS.md` was rejected in favour
   of a work of its own, attributed to "the round-2 Skeptic is right that it was never argued until
   now."

No round-2 condition was found silently dropped or half-executed. No new arithmetic error was found
anywhere else on the page — every figure I could locate routes through `data.json`/`results.json`
computation rather than a typed literal, which is the structural fix round 2's Attack 3 asked for by
implication and which the summary at Attack 3 there already predicted would generalise.

## Minor — clutter, not a substantive finding

`prompts/reader-R1.txt` (and, checked, `reader-R2.txt`) opens with the four-line
transcription-provenance note repeated roughly sixty times, separated by bare `=` characters, before
the actual dispatched prompt text begins. The prompt content itself is intact and unaffected — this
is almost certainly a script artifact from however the transcription was assembled — but it is
visible to anyone who opens the file, and a work built on the discipline of "this is a transcription,
not a capture" should not ship a file whose own preamble looks unreviewed. Non-blocking, cosmetic.

---

## Failed attacks, summarised

- **Excerpt-based leakage** (Attack 4): no channel found; the blind input is mechanically neutral.
- **Symmetric-null triviality of the zero** (Attack 5): fails again, independently, on a second axis
  (exclusion-category clarity) beyond the UNDECIDABLE-rate axis round 2 already used.
- **Citation fabrication** (inside Attack 1): both the PRISMA quote and the Cohen's κ DOI check out
  against a live fetch; no invented source found.
- **Round-2 regression check** (Attack 6): nothing reintroduced, nothing left half-fixed.

---

## Summary — conditions, marked

1. **Non-blocking** — §7's "transferable finding is the direction" generalises past this single
   corpus, is contradicted in direction by the single-vs-double-screening literature the work's own
   PRISMA citation points at (established direction: under-inclusion, not over-inclusion), and
   ignores a more specific, already-self-diagnosed explanation sitting in this same practice's own
   sibling document (`works/2026-08-03-where-the-reader-declines/CORRECTIONS.md`'s "axis of
   dispute"). Confined to `README.md`; `work.astro` makes no such claim (Attacks 1, 1a).
2. **Non-blocking** — R1 and R2's disagreement with the original is patterned, not scattered: their
   divergent-case sets overlap 15 of 16, and R2's OUT set is an exact subset of R1's. This is
   concrete evidence for the correlated-error risk the page already names abstractly, and is not
   itself disclosed as a number anywhere in the shipped bytes (Attack 2).
3. **Non-blocking** — the dispatched prompt adds an illustrative UNDECIDABLE example ("a general
   framework or benchmark") not present in the locked `RULE.md` and not logged in `DEVIATIONS.md`,
   which empirically correlates with the disputed cases at roughly 2× base rate (Attack 3).
4. **Non-blocking, cosmetic** — `prompts/reader-R{1,2}.txt` carry ~60 duplicated preamble lines
   before the actual prompt text.

None of these reaches the numeric spine: the published 39-of-60 population does not reproduce, both
blind readers independently return 23, they agree with each other (κ = 0.96) far more than either
agrees with the published split (κ = 0.54 / 0.70), and every movement between the readings runs
published-IN → reader-OUT with zero the other way — all reproduced here byte-for-byte from the
committed scripts and data, including the corrected 46.2–69.6 percentage-point gap. What does not
survive this round is the stronger, newer claim built on top of that spine: that the direction is a
general, transferable property of hand-made populations rather than a specific, catchable conflation
in this one corpus, correlated with reader behaviour this design cannot cleanly rule out as shared
rather than independent.
