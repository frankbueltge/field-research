# SKEPTIC — round 4, on the shipped state

**Object under review:** `works/2026-08-05-the-second-reader/` at commit `515e404` — the exact bytes
that would ship. Round 3 graded `405c763` and returned SURVIVES WITH CONDITIONS (three non-blocking
conditions plus one cosmetic note). This round first checks whether round 3's conditions actually
landed in these bytes, then attacks the material that changed since: §7's rewrite, the new §6
correlated-reader bullet, `DEVIATIONS.md`'s new **D2**, and the roughly one-third cut to `README.md`
made to bring the record under Rule 6's 3,000-word ceiling.

**Verdict: SURVIVES WITH CONDITIONS.** The numeric spine reproduces exactly — reran
`scripts/selftest.py` (21/21 pass) and `scripts/score.py`; agreement counts (43/44/52 of 60), κ
(0.5355/0.699/0.9602), the band evaluations (both C), and **zero** published-OUT→reader-IN movements
all match, and `results.json` has no diff against the committed file. I pushed the single hardest
version of the strongest attack this round was pointed at — purging every benchmark-shaped title
entirely from the moved cases — and the one-directional movement still survives it (below). What does
not survive cleanly is round 3's own condition 2: `work.astro` — the instrument itself, as opposed to
this file, its "shelf" — is **byte-for-byte unchanged** since round 3. The correlated-reader
divergence figures and the D2 finding were added to `README.md` only. A reader who opens the page and
never opens the README still sees none of it, which is exactly the gap round 3's Attack 1a already
named for §7 and is now true a second time, for a second disclosure.

---

## Check 1 — Did round 3's three conditions land?

| # | round 3 condition | status |
|---|---|---|
| 1 | §7 overreach: withdraw or narrow the transferability claim | **Executed, and well.** §7 now states plainly "the general claim is withdrawn," cites Waffenschmidt et al. 2019 against its own earlier claim, and narrows to "a hand-made population can move a great deal under blind re-reading, and its owner cannot see which way from inside." See Check 3. |
| 2 | Disclose the correlated-reader divergence-set overlap (15/16), in `work.astro` §5 **or** `READER-PROVENANCE.md` | **Partially executed, in the wrong place.** The number is now in `README.md` §6 ("R1 diverges on 17, R2 on 16, union 18," overlap 15 — recomputed independently below, exact). It is in **neither** `work.astro` §5 nor `READER-PROVENANCE.md`, both of which round 3 named as the target. `git diff 405c763 515e404 -- work.astro READER-PROVENANCE.md` is empty — neither file was touched at all this round. |
| 3 | Log the unlogged prompt example in `DEVIATIONS.md` | **Executed.** D2 exists, dated, with the arithmetic (13/39 base rate, 8/14 = 57.1% of movements) reproduced below and correct. |
| — | cosmetic: duplicated preamble in `prompts/reader-R{1,2}.txt` | Not touched — `git diff 405c763 515e404 -- prompts/` is empty. Still present, still non-blocking. |

Condition 2 is the live issue. Round 3's Attack 1a made the structural point that `work.astro` has six
sections and none of them is §7 — the overreach was "confined to the supporting document," which
"lowers the blast radius." That same sentence now applies to the correlated-reader disclosure: it
too is confined to the supporting document. `work.astro` §5's "not the outside" bullet is unchanged
word-for-word from round 3's state; it still names the risk only in the abstract ("a correlated error
between them would be invisible to this design"), with no number beside it. Whoever reads the actual
page — the artifact a "code host" visitor lands on per round 3's own framing — still gets the abstract
caveat only.

**Recomputed the overlap figure independently, across all 60 cases** (README's new sentence, unlike
round 3's, scopes it to all 60, not just the 39 published-IN):

```
R1 diverges from the published split on: 17 cases
R2 diverges from the published split on: 16 cases
overlap: 15    union: 18
R1-only: mbcls-2606.04228, mbcls-2603.20262
R2-only: mbcls-2606.10402
```

Matches README's "17, 16, overlap 15, union 18" exactly. Restricting to the 39 published-IN cases
alone (round 3's original scope) reproduces round 3's own 16/16/overlap-15 figure and the "R2's OUT
set is an exact subset of R1's OUT set" claim, both confirmed again here.

**Condition, non-blocking:** move the correlated-divergence figure (or a version of it) into
`work.astro` §5 or `READER-PROVENANCE.md`, per round 3's original instruction — restating it in
README does not satisfy a condition that named the instrument specifically, for a reason (audience)
this session's own Attack 1a already gave.

---

## Check 2 — The strongest available attack: does D2's defence survive purging every benchmark-shaped case?

D2 says the prompt's unlogged UNDECIDABLE example ("a general framework or benchmark") "does not
overturn the result: the readers' stated exclusion reasons are about the system described, not the
title word."

**Read the actual reason fields** (`reader-R1.json`, `reader-R2.json`) for every published-IN case
with a bench/benchmark/evaluat/audit/suite word in the title that either reader moved off IN. Sample,
verbatim:

> *BioKGBench* → R1 OUT: "The system's own task is checking literature claims and knowledge-graph
> facts, not running a hypothesize-experiment-analyze cycle of its own."
> *MedSkillAudit* → R1 OUT: "The framework audits the quality of other agents' skill outputs rather
> than performing research itself."
> *Total Recall QA* → R2 UNDECIDABLE: "This evaluates agents answering complex questions via search
> and synthesis, a domain ambiguous between research and information retrieval."

None of the eight reasons says or implies "excluded because it is a benchmark." Every one names what
the described system does (checks claims, operates software, audits other agents' outputs, retrieves
and synthesizes without testing a hypothesis) — **the defence holds on direct inspection.**

**Then pushed harder than D2 itself does: what if every bench-worded case is thrown out entirely,**
not just checked for reason-wording?

```
R1 strict-OUT movements on published-IN:  14 total,  8 bench-worded,  6 WITHOUT any bench word
R2 strict-OUT movements on published-IN:   8 total,  3 bench-worded,  5 WITHOUT any bench word
Published-OUT → IN reversals, bench-worded or not:                    0, both readers
```

Delete every case whose title contains "bench," "benchmark," "evaluat," "audit," or "suite" from the
population entirely, and the movement is still 6-of-31 and 5-of-31 non-bench-worded published-IN
cases moving to OUT, against **zero** reversals in either direction. **The one-directional-movement
core claim is unaffected by even the strictest version of this test.** D2's defence, and the page's
headline, both survive this attack. This was the hardest line available and it did not land.

**Reproduced round 3's own hypergeometric figure independently**
(`hypergeom(M=39, n=13, N=14).sf` inclusive at 8): **P = 0.02306**, matching round 3's 0.023 exactly.

**One number in round 3's report does not reproduce, though it never reached the shipped bytes.**
Round 3 wrote: "of R2's 8 UNDECIDABLE-on-published-IN cases specifically, with such a word | 6
(75.0%)." Recomputing directly from `reader-R2.json` and the titles in
`evidence/source-021-data.json`, R2's eight UNDECIDABLE-on-published-IN cases are:

| case | bench-worded? | title |
|---|---|---|
| mbcls-2505.21935 | no | *From Reasoning to Learning: A Survey…* |
| mbcls-2510.02190 | yes | *Dr. Bench…* |
| mbcls-2601.12346 | yes | *MMDeepResearch-Bench…* |
| mbcls-2603.18516 | yes | *Total Recall QA: A Verifiable Evaluation Suite…* |
| mbcls-2604.18418 | yes | *MedProbeBench: Systematic Benchmarking…* |
| mbcls-2605.06177 | yes | *BioMedArena…Evaluating…* |
| mbcls-2606.10402 | no | *Harnessing the Collective Intelligence…* |
| mbcls-2607.26064 | no | *The Age of AI Agents Demands…* |

That is **5 of 8 (62.5%)**, not 6 of 8 (75.0%). This does not touch anything currently shipped —
`DEVIATIONS.md`'s D2 states only the 8/14 = 57.1% figure and does not repeat the 75% number, so the
error was not carried forward — but round 3's report is published unedited as historical record, and
this is a small, checkable slip inside a passage whose whole point was "recomputed this independently
… rather than trusting the quote." Non-blocking; noted for the record, not for correction (a
published review report is not edited after the fact, by this practice's own convention).

---

## Check 3 — Is §7's narrower claim defensible, and is the Waffenschmidt citation used fairly?

**Fetched Waffenschmidt et al. 2019 directly** (PMC6599339) rather than trusting either round's
characterization of it. Confirmed: the quoted sentence — "The median proportion of missed studies was
5% (range 0 to 58%)" — is **verbatim**, appearing identically in both the abstract and the results
section. The review is built on **4 evaluations**, 23 single-screening instances, 9 reviewers, 41,730
references. It reports **zero instances of the reverse direction** (single screening including *more*
than double screening) — the direction is exclusively under-inclusion in every evaluation the review
pooled. The review's own caveat, not mentioned by README, is that all four evaluations screened only
bibliographic-database citations, not the supplementary sources (registries, reference lists) a full
systematic review also uses — a limitation on the review's own generalizability that runs in the
direction of making its 5%-median finding *conservative*, not one that would let this corpus's
opposite direction back in. **The citation is used fairly: it is not overstated, the quote is exact,
and checking it did not surface a friendlier reading for the original claim §7 withdrew.**

**On the new claim's own defensibility:** "a hand-made population can move a great deal under blind
re-reading, and its owner cannot see which way from inside." This is now a possibility claim (*can*
move, not *does* move in a fixed direction), and a possibility claim is exactly what n = 1 can
establish — this corpus demonstrably did move, and its builder demonstrably did not anticipate which
way. The residual soft spot: "a hand-made population" is phrased as a generic noun phrase, and a
careless reading could still take "and its owner cannot see which way from inside" as a structural law
about self-review rather than a description of what happened once, here. That reading is available but
not forced — the surrounding sentences (explicit withdrawal, the opposing citation, "this corpus's
direction has a named mundane mechanism, not an inherent property") argue against it. **This attack
does not fully land**; it is a phrasing note, not a finding that the claim outruns its evidence the way
round 3's target did.

**Also checked:** the merge-commit citation added this round —
`2be352942c8657ccaec6e7e6f8de9c33904b83f6`, described as the actual merge of PR 413, parents `131fc56`
and `f3f0b7a`, correcting an earlier draft that cited the branch tip `f3f0b7a` as if it were the merge.
Fetched the commit page directly (the API route is confirmed closed to this session, as the page
itself says): it **is** a merge commit, its two parents are exactly `131fc56` and `f3f0b7a`, and the
message is "Merge pull request #413 from frankbueltge/field/pr-field-instrument-tripwire." No
fabrication found.

---

## Check 4 — Did the compression break anything?

Diffed `README.md` in full (`git diff 405c763 515e404 -- README.md`, 453 changed lines). The cut is a
sentence-level compression of the same claims, not a removal of support out from under a surviving
claim, with one partial exception: the "reader populations are still 26 and 31 against 39" sentence
(the D1 inclusive-branch numbers) was cut from README's prose entirely. Recomputed both figures
directly from `reader-R{1,2}.json` over all 60 cases (IN + UNDECIDABLE, including the one published-OUT
case each reader marked UNDECIDABLE): **26 and 31**, exactly the historical figures — and both numbers
are still live and computed in `work.astro` §5 (`{inside.R1.n}` / `{inside.R2.n}`). Not broken, just
deduplicated onto the instrument rather than restated in the shelf.

**Word ceiling, checked rather than trusted:** ran `tools/record_ceiling_check.py` with the exemption
set README's new opening note claims (the review reports, `RULE.md` + `DEVIATIONS.md`, `prompts/`,
`evidence/`). Counted total: **README.md (2,326) + READER-PROVENANCE.md (671) = 2,997 words — three
words under the 3,000 ceiling.** Compliant, but by a margin so thin that the next honest addition (for
instance, executing Check 1's still-open condition by adding a sentence to README rather than to
`work.astro`) would put it back over.

**One number in that same opening note does not check out.** It calls the exempted review reports
"the six review reports." Counting what is actually claimed as review reports (`VERIFICATION*.md`,
`SKEPTIC*.md`, `INTERLOCUTOR.md`, per §3's own listing) yields **seven**: `VERIFICATION.md`,
`SKEPTIC.md`, `INTERLOCUTOR.md`, `VERIFICATION-round2.md`, `SKEPTIC-round2.md`,
`VERIFICATION-round3.md`, `SKEPTIC-round3.md`. ("Six" is the right count for the *prior* graduated
work this practice reused the phrase from, where two rounds each produced a Verifier, Skeptic and
Interlocutor report — 3×2. This work only produced an Interlocutor in round 1, so the count is
3 + 2 + 2 = 7, not 6.) This is a hand-carried number, wrong by one, sitting inside the very paragraph
arguing for a word-ceiling exemption regime — the identical failure mode `tools/record_ceiling_check.py`'s
own docstring names as the reason the script exists ("a document about precision stops publishing
three different figures for the same file"). It does not change which files are actually exempt (all
seven are in fact excluded from the counted total, confirmed by rerunning the script with each named
explicitly), and it does not change compliance. **Condition, non-blocking, but worth the fix given
what the sentence is arguing for:** correct "six" to "seven," or state explicitly why `INTERLOCUTOR.md`
sits outside the "review reports" the sentence means.

---

## Failed attacks, summarised

- **Purging every benchmark-shaped title from the moved cases** (the strongest line offered): fails —
  6 of R1's 14 and 5 of R2's 8 strict-OUT movements carry no bench/benchmark/evaluat/audit/suite word
  at all, and the 0-reversal figure is unaffected regardless. The one-directional core claim survives
  its hardest available test.
- **Reading the readers' actual reason fields for bias toward the title word rather than the system
  described**: fails — every sampled reason names a property of the described system, none cites
  "benchmark" or "framework" as itself disqualifying.
- **Checking whether the Waffenschmidt citation is stretched**: fails — the quote is verbatim, the
  review's own scope caveat does not help the withdrawn claim, and the citation supports exactly what
  §7 now says it supports.
- **Checking whether the new merge-commit hash and parents are fabricated**: fails — independently
  confirmed against the public commit page.
- **Checking whether the compression silently orphaned a claim**: mostly fails — one figure (26/31)
  was cut from prose but remains live and computed in `work.astro`, not lost.
- **Reproducing every headline number** (agreement, κ, band, 0 reversals): all reproduce exactly;
  `results.json` has zero diff against committed state.

---

## Summary — conditions, marked

1. **Non-blocking, carried and not resolved.** Round 3's condition 2 (quantify the correlated-reader
   risk in the instrument, not just its shelf) landed in `README.md` only; `work.astro` and
   `READER-PROVENANCE.md` are byte-identical to round 3's state. The same is true of D2's finding —
   named in README §6, absent from `work.astro` §5's parallel bullet. **What must change:** add the
   overlap figure (or a pointer to D2) to `work.astro` §5 or `READER-PROVENANCE.md`.
2. **Non-blocking.** README's new word-ceiling exemption paragraph miscounts its own exemption list —
   "six review reports" where seven files meet the description it gives (§3's own listing). **What
   must change:** correct the count or explain the exclusion of `INTERLOCUTOR.md` from it.
3. **Non-blocking, informational, not a shipped defect.** `SKEPTIC-round3.md`'s own recomputed figure
   (6 of 8 UNDECIDABLE-on-IN cases bench-worded, 75%) does not reproduce — the correct figure is 5 of
   8 (62.5%). Not carried into `DEVIATIONS.md`'s D2, so nothing currently shipped is affected.
4. **Non-blocking, soft.** §7's rewritten claim is materially improved and its central move (citing
   Waffenschmidt against its own earlier claim) is fair and checks out; the residual generic phrasing
   ("a hand-made population... its owner cannot see which way from inside") could still be misread as
   a structural law rather than a description of this one corpus, though the surrounding text argues
   against that reading.
5. **Non-blocking, unresolved from round 3.** `prompts/reader-R{1,2}.txt` still carry the duplicated
   preamble; untouched this round.

None of these reaches the numeric spine. The published 32-of-39 does not reproduce, both blind
readers independently return 23, they agree with each other (κ = 0.96) far more than either agrees
with the published split, and every movement between the readings runs published-IN → reader-OUT with
zero the other way — including under the strictest test this round could construct against it,
purging every benchmark-shaped title from the population entirely. What round 3 flagged as overreach
is now a fairly cited, appropriately narrowed claim. What round 3 asked to be fixed in the instrument
itself is fixed in its shelf instead.
