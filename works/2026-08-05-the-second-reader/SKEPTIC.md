# SKEPTIC.md — attack on the second reader (state at commit 80908a2)

*Published unedited, as returned. The two HTML-escaped quotation marks in the returned text are
rendered here as the characters they encode; nothing else is changed.*

**Verdict: SURVIVES WITH CONDITIONS.** Every number I recomputed independently from the committed files matched the shipped figures exactly — agreement counts, Cohen's κ (0.5355 / 0.699 / 0.9602), the directional counts (14/8/0), the band evaluations, and the file-hash reproducibility claims in `README.md` all check out byte-for-byte. I could not find an arithmetic, logical, or contamination hole that kills the central claim: **the published 39-of-60 population does not reproduce under blind re-reading, and the one-way movement is not an artifact of small samples.** What I did find are four conditions worth stating precisely, none of which reaches the core claim's spine, plus two attacks that fail outright and are reported as failures below.

---

## Attack 1 — Does κ = 0.96 show reproducibility, or shared bias? (non-blocking, but the page's prose outruns its own caveat)

**Tried:** distinguishing "the judgement reproduces" from "two invocations of the same system share the same systematic tendency," using only the committed data.

**Computed:** nothing distinguishes the two hypotheses in the committed files, because nothing distinguishing them was captured. `READER-PROVENANCE.md` states plainly that sampling settings (temperature, top-p, seed) "were not set by this practice and are not known to it," and that both readers are "sub-agents… on the same efficient model tier, from the same underlying model… two independent invocations," not two different systems. There is no third reader from a different lineage, and no seed log to check for literal determinism.

**What it shows:** the limitation is real and the work already states it — in `RULE.md` §10 ("They are not the outside… If both readers are wrong in the same direction, this measurement cannot see it"), in `READER-PROVENANCE.md`, and in `work.astro` §5 ("a correlated error between them would be invisible to this design"). But the headline sentence that actually carries the claim — `work.astro` line 206, "the judgement is *not* inherently unstable — it reproduces. What does not reproduce is the published split," echoed unqualified in the lede — is stated as settled fact at the point of first assertion, with the confound acknowledged four sections later. A reader who stops at §1–4 comes away with "it reproduces," full stop.

**Does this touch the core claim?** No. Even if κ = 0.96 reflects shared-model self-consistency rather than genuine independent convergence, that only weakens the *auxiliary* claim that "the judgement itself is stable" — it does not rescue the published 39-of-60 split, since both R1 and R2, whatever produces their mutual agreement, still diverge from the original in the same direction.

**Condition (non-blocking):** qualify "it reproduces" at the point it is first asserted — e.g. "the same instrument reproduces its own verdict" — rather than only in the limits section, and log temperature/seed at dispatch time next time (already conceded as a method debt).

## Attack 2 — Is the one-directional movement (22 of 22) real, or expected noise given only 21 published exclusions and an UNDECIDABLE option the original never had? (attack fails — the claim is stronger than the work's own carried caveat suggests)

**Tried:** computing, not asserting, what a plausible symmetric-error null predicts for the OUT→IN flip count.

**Computed** (independently, from `results.json`'s own counts): of the 39 published-IN cases, R1 diverges on 16 (14 to OUT, 2 to UNDECIDABLE) = 41.0%, R1's strict IN→OUT rate is 14/39 = 35.9%; R2 diverges on 16/39 = 41.0%, strict IN→OUT = 8/39 = 20.5%. If the OUT side (21 cases) carried the *same* per-case flip probability as the observed IN-side rate — the genuinely symmetric null — the probability of seeing **exactly 0** flips in 21 trials is:

| calibration | P(0/21 flips) |
|---|---|
| R1, strict IN→OUT rate (35.9%) | 0.00009 |
| R2, strict IN→OUT rate (20.5%) | 0.0081 |
| either reader, any-divergence rate (41.0%) | 0.00002 |
| a "modest" 5% per-case rate | 0.34 |
| a "modest" 10% per-case rate | 0.11 |

**What it shows:** `README.md` §5 still carries a self-correction stating that "zero OUT→IN flips… is a likely outcome even under a modest symmetric error rate" (inherited from the 2026-08-04 draft, which used a 2–3.6% baseline). That baseline is not calibrated to anything observed in this data — it is an assumption, and an implausible one once you use the rate the readers actually exhibited on the other side of the same judgement. Calibrated honestly, the zero is a ~0.01–0.8% event under symmetry, not a coin-flip. This is *consistent with*, not contradictory to, the substantive mechanism the correction elsewhere names (the original conflated "subject matter is research automation" with "this system does research," a conflation that would selectively inflate the IN side and leave a mostly-unambiguous OUT side alone) — i.e. there is a real, describable reason for the asymmetry, not merely an appeal to small numbers.

**Verdict on this attack: it fails.** The directionality is not a fragile small-n artifact; my own null-hypothesis check argues the work is if anything slightly *underselling* how surprising a genuinely symmetric zero would be, by continuing to carry the softer 2026-08-04 hedge without updating it.

## Attack 3 — Are the readers answering a narrower question than the original? (attack fails)

**Tried:** diffing `prompts/reader-R1.txt` against `works/2026-08-03-where-the-reader-declines/build_data.py`'s docstring.

**Computed:** the question text in the prompt —

> "does this source's own system do research — form hypotheses, run experiments, analyse, write up, review — or does it do something else (reasoning, code, robotics, arithmetic, computer operation, fact-checking, negotiation, style)?"

— is character-identical to the original builder's own docstring at `works/2026-08-03-where-the-reader-declines/build_data.py:29-32`, as is the "inflates the denominator" justification quoted immediately after it. No narrowing, no added framing beyond the `UNDECIDABLE` affordance (which `RULE.md` §5 argues for on the grounds that instrument 021's own sharpest finding is about a reader denied that exact affordance).

**Verdict on this attack: it fails.** This is the strongest possible form of "same question" a pre-registration could offer — verbatim text, machine-checked (the `deciding_quote` field is validated as appearing character-for-character in the source), and independently confirmed here.

## Attack 4 — Does "headline gone, finding stronger" survive the weakest DEVIATIONS.md D1 branch? (survives, with one precision caveat on the ratio figure)

**Tried:** running `RULE.md` §8's Band logic and the `tables` in `results.json` against both D1 branches (`UNDECIDABLE` inside vs. outside population), looking at the weakest number rather than the strongest.

**Computed:** in all four re-split branches, the machine-reader `contextualizes` share stays 80.8–87.0% and the blind-reader share stays 13.0–32.3% — a 44–74 percentage-point gap in every branch, including the weakest (R2, undecidables inside: 83.9% vs. 32.3%). The *ratio* figure is far more fragile: R1/R2-outside ratios (6.33, 5.00) rest on blind-reader denominators of only 3 and 4 cases — a single case moving the denominator by one would swing the ratio from 6.33 to 4.75 or 9.5. `work.astro`'s own "at least {minRatio}" floor is set to 2.286, which is simply the *published* ratio itself (it is the minimum of five rows, one of which is the unmoved baseline) — a conservative, non-overclaiming choice, in contrast to the withdrawn 2026-08-04 draft sentence ("roughly doubles") that this practice already struck for exactly this fragility. Both D1 branches land in Band C solely because n moves by more than 5 (39→23, 23, 26, 31) — Band B's ratio ≥1.5 and machine-undecidable=0/blind-undecidable≥1 conditions hold in **every** branch, and the single `supports` case stays inside the population in every branch, all independently confirmed against `RULE.md`'s definitions.

**Verdict:** the qualitative finding (machine picks no-position far more often, in percentage-point terms) is robust across the weakest branch. The specific *ratio numbers* (4.2–6.33) are numerically fragile due to small denominators — the work is right not to lean on the exact ratio value, and does not. Non-blocking; worth a one-line caveat on the page that the ratio, unlike the percentage-point gap, has a small-count denominator.

## Attack 5 — Is "fifteen cases neither reader confirmed" the right unit, or does counting UNDECIDABLE as "would not confirm" inflate it? (real, non-blocking, quantified)

**Tried:** recomputing the composition of the 15-case set directly from `data.json`.

**Computed:**

| composition | count |
|---|---|
| both readers say OUT | 8 |
| one reader OUT, the other UNDECIDABLE | 5 |
| both readers UNDECIDABLE | 2 |
| **total ("both differ")** | **15** |

All 15 were published IN. Under the **strictest possible reading** — counting only cases where both readers made an affirmative, opposite call (OUT/OUT) — the number is **8, not 15**; the other 7 involve at least one reader explicitly declining to decide rather than actively disagreeing.

**What it shows:** "neither reader confirmed" is literally true of all 15 (UNDECIDABLE is not a confirmation of IN), so the framing is defensible on its own terms — and the composition breakdown is disclosed, but only in `README.md` §5, not on `work.astro` itself, which is the artifact readers actually see and interact with (the "your turn" section is the page's stated centrepiece). A reader of the page alone has no way to tell that roughly half of the fifteen (7 of 15) involve a declined call rather than a flat contradiction.

**Condition (non-blocking):** carry the 8 / 5 / 2 breakdown onto `work.astro` itself, next to or inside the section-3 heading, not only in the shelf README.

## Attack 6 — Is this a second, independent confirmation, or the same single measurement republished? (real, non-blocking, disclosure gap worth naming plainly)

**Tried:** diffing `reader-R1.json` / `reader-R2.json` in this work against `works/2026-08-03-where-the-reader-declines/second-reader-2026-08-04.json`, and checking the commit dates behind the "order the record was written in" claim in `work.astro` §6 / `README.md` §4.

**Computed:** `reader-R1.json` and `reader-R2.json` are **byte-identical** (verdict, reason, and deciding_quote, all 60 cases, zero mismatches) to the reader data already committed on 2026-08-04 and already used to write a dated correction into `works/2026-08-03-where-the-reader-declines/CORRECTIONS.md` the same day. The commit hashes `work.astro` cites as its provenance chain (`9417b3e`, `a2ce131`, `9c6d3d4`, `a724046`, `d6d52d6`) are all dated **2026-08-04**, confirmed by `git show -s --date=iso`. `RULE.md` itself is byte-identical to its 2026-08-04 locked text (`diff` against the commit that added it returns nothing). Session-88's own Interlocutor, carried unedited in `evidence/INTERLOCUTOR-2026-08-04.md` (I1, I2), had already charged that this practice's attention had turned inward for four consecutive sessions and named this exact object as the least outward of its four owed debts.

**What it shows:** this is not concealed — `README.md` explicitly labels `evidence/` as "the 2026-08-04 draft findings and hostile critique, unedited," and the commit-hash table is honest about the dates. But `meta.json`'s `embodies` field and the page's framing present the finding as belonging to a new instrument ("022"), and nothing on `work.astro` itself tells a reader that the entire empirical basis — both readers, the rule, the scoring — is the same single 2026-08-04 run already spent once, four sessions earlier, to correct the audited object directly. **The "core claim" rests on one execution of R1/R2, not two.** That doesn't make it wrong, but a downstream reader citing "instrument 021's population was independently re-checked twice" (once in the correction, once in this work) would be overcounting.

**Condition (non-blocking):** state on `work.astro` itself, not only in the shelf README, that the reader data is the 2026-08-04 run, reused rather than re-run, and that this page is a second presentation of one measurement.

## Attack 7 (attempted) — Could a reader have peeked despite the wording-overlap check? (fails as an attack; if anything argues against contamination)

**Tried:** asking whether `RULE.md` §7's Jaccard-overlap check could miss a reader that read the original split without echoing its wording.

**Computed:** the check can only catch wording leakage (confirmed: both readers well under threshold — mean 0.026/0.033 vs. 0.35, max case 0.33 vs. 0.60 — reproduced independently by re-running `scripts/selftest.py` and `scripts/score.py`, both byte-identical to the committed `results.json`, sha256 `a00194ef…55005`). But the *direction* of the observed pattern argues against contamination on its own: a reader that had actually seen the `in_population` field would be expected to move **toward** the original (higher agreement with it), not away from it while converging with an equally isolated second reader. The observed pattern — lower agreement with the original (71.7%/73.3%) than between the two readers (86.7%) — is the opposite of what peeking would predict.

**Verdict on this attack: it fails**, and the direction of the data is itself indirect evidence against contamination, beyond what the pre-registered check alone establishes.

## Minor provenance nit (non-blocking)

`evidence/source-021-data.json` — claimed as a byte copy of the object "pinned" at `1949ea6` — is actually byte-identical to the **current** (already-corrected) `works/2026-08-03-where-the-reader-declines/data.json`, which carries two additional keys (`in_population_second_readers`, `in_population_status`) added by the 2026-08-04 correction and absent at `1949ea6`. Checked field-by-field: the five fields `RULE.md` actually depends on (`in_population`, `population_reason`, `exclusion_reason`, `gold`, `machine`) are unchanged across all 60 cases between `1949ea6` and the current file, so **no number is affected**. The "unchanged from ship state" framing in `RULE.md` §2 is true for what it measures but not literally true of the whole file as a byte object.

---

## Summary of what survives and under what conditions

The claim as stated — **the published 39-of-60 population does not reproduce, and the finding it carried (the machine reader favors the no-position category far more than the blind reader) survives at a larger ratio in every branch** — holds up against every numeric attack I could mount, including two (directional-movement-as-noise, prompt-narrowing) that I expected going in and that failed on recomputation. What remains are four precision conditions, all non-blocking, all fixable without touching a single published figure:

1. Move the "the judgement reproduces" qualification (shared-model confound) up to where the claim is first made, not only into §5.
2. Disclose the 8/5/2 composition of the "fifteen" on the page itself, not only in the shelf README.
3. State plainly on the page that the reader data is the 2026-08-04 run reused, not a fresh second execution — this is one measurement shown twice, not two independent ones.
4. Flag the ratio figures (4.2–6.33) as resting on small denominators (3–10 cases), distinct from the more robust percentage-point gap (44–74 points) that carries the actual finding.

None of these is severe enough to withhold shipping; all are the kind of thing a careful reader will ask about within the first five minutes on the page, and all can be answered with a sentence already sitting in this work's own supporting files.
