# SKEPTIC — round 2, on the corrected state

**Object under review:** `drafts/2026-08-05-the-second-reader/` at commit `84f52b0` on
`research/session-2026-08-05-3`. Round 1 (`SKEPTIC.md` in this directory) returned SURVIVES WITH
CONDITIONS against `80908a2` and named four conditions; this round attacks the state produced by
executing them, per the mandate: a correction is where a new false claim usually enters.

**Verdict: SURVIVES WITH CONDITIONS.** The core claim is untouched by every attack below: the
published 39-of-60 population does not reproduce under blind re-reading, both readers independently
return 23, they agree with each other (κ = 0.960) far more than either agrees with the published
split (κ = 0.536 / 0.699), and all 22 movements between readings run published-IN → reader-OUT with
zero the other way. Every one of these numbers was recomputed here from the committed files and
matched exactly. But one of the four round-1 conditions was executed with a genuine arithmetic error
that is live on the page at the reviewed commit, one correction is real but under-propagated, and the
"why not `works/`" argument in README §0, while structurally sound, omits an option the practice's
own workboard had already named. None of this reaches the spine of the claim; one of them is
BLOCKING for shipping regardless.

---

## Attack 1 — The qualified reproducibility sentence: right-sized, or does the page lean on the stronger version elsewhere?

**Target:** "the same instrument reproduces its own verdict… a shared tendency would look exactly
like agreement here" (`work.astro` §4, README §1).

**Checked:** every use of "reproduc-" in both files (`grep`), and where in reading order each first
appears.

**Found:** the qualified sentence is the *first* place on the page the reproducibility claim is
made — it sits in §4, at the point the κ = 0.96 table is shown, with the shared-model-family caveat
in the same sentence, not deferred to a later section as round 1's Attack 1 found it doing at
`80908a2`. The lede and §§1–2 describe what happened ("agreed with each other far more than either
agreed with the published split… both returned a population half the size") without using the loaded
word "reproduces" at all, so there is no earlier, unqualified assertion for the qualified one to
retroactively soften. The one other "reproduc-" use (§5: "two independent readers converging is
evidence that a reading reproduces, not that it is correct") is about whether **23** is *right*, a
different claim, and is itself immediately hedged. **This condition is satisfied — right-sized, not
under- or over-claiming.** Non-blocking, resolved.

## Attack 2 — "One measurement presented a second time": complete, or does something else still read as fresh?

**Target:** the reused-run disclosure in README §4 and `work.astro` §6 (Provenance).

**Checked:** diffed `reader-R1.json`, `reader-R2.json`, `RULE.md` against
`drafts/2026-08-04-second-reader-021/` — **byte-identical**, confirming the disclosure's own
factual content is accurate, not merely asserted.

**Found a placement gap, not a content gap.** The disclosure lives only in `work.astro`'s §6
("Provenance"), the last section on the page, and in README §4. Two places upstream of it still
describe the reading as if newly made, with no nearby qualifier:
- the lede: "Two readers have now made that judgement from scratch, blind…" — true, but "now"
  invites the reading "for this page," when the run is the one already spent on 2026-08-04 to write
  a dated correction into instrument 021 four sessions earlier;
- `meta.json`'s `embodies` field — untouched by this round's diff (`git show --stat 84f52b0` lists it
  with 0 insertions/deletions) — still reads: "Two readers made the judgement again from scratch,
  blind, under a decision rule and a scoring script committed before either of them saw a case,"
  with no reuse qualifier anywhere. `meta.json` is exactly the surface a catalogue listing or an
  automated indexer would read without ever reaching `work.astro` §6.

A reader who stops before the last section, or who only ever sees `meta.json`, comes away thinking
this is a second execution. **Non-blocking condition:** add a one-clause reuse qualifier to the lede
or to `meta.json`'s `embodies` field, not only to the page's last section.

## Attack 3 — Ratio-fragility passage: recompute the gap, and the denominators

**Target:** "Read the gap, not the ratio… 44 to 74 points in every branch above… denominators of 3,
4, 5 or 10" (`work.astro` §4).

**Recomputed** (from `results.json` and `data.json` at `84f52b0`, exact fractions, not the
displayed rounding):

| row | machine % | blind % | gap (pp) |
|---|---|---|---|
| published (n=39) | 82.05 | 35.90 | **46.15** |
| R1, undecidables outside (n=23) | 82.61 | 13.04 | **69.57** |
| R2, undecidables outside (n=23) | 86.96 | 17.39 | **69.57** |
| R1, undecidables inside (n=26) | 80.77 | 19.23 | **61.54** |
| R2, undecidables inside (n=31) | 83.87 | 32.26 | **51.61** |

The true range across the five rows the table actually shows is **46.2 to 69.6 points** — not
44 to 74. No branch has a gap of 44 or of 74; those numbers only appear if you combine the smallest
machine share from one branch (80.8 %, R1-inside) with the largest blind share from a *different*
branch (35.9 %, published) to get 44.9→44, and the largest machine share (87.0 %, R2-outside) with
the smallest blind share from yet another branch (13.0 %, R1-outside) to get 74.0 — an unpaired
cross-branch construction, not a quantity that occurs in any single branch, despite the text's own
claim "in every branch above."

The denominators claim is correct: the blind-reader `contextualizes` counts are exactly 3, 4, 5, 10
across the four re-split branches, confirmed against `results.json`.

**This is a genuine, checkable factual error, live on the page, in the exact passage this round
added to fix round 1's Attack 4 condition** — the passage arguing the percentage-point gap is the
*robust* figure in contrast to the fragile ratio. It is not a fragility-of-small-n problem itself
(the true 46.2–69.6 range is a completely different kind of error: a typed number that does not
match a recomputation, not a number sensitive to one case moving). **BLOCKING** for landing at this
commit, though it does not touch the core claim, since the qualitative point — the gap is wide in
every branch and does not shrink to nothing — survives under either the wrong or the correct
numbers.

*(Noted for transparency, not as part of this round's grading: a later commit on this branch,
`6637776` — "A range we typed instead of counted: 44-74 was never in the table, 46.2-69.6 is" —
already corrects this to the exact figures recomputed above, after the commit under review. That
this was independently caught and fixed corroborates the finding rather than superseding the verdict
on `84f52b0`, which is the state named for this round.)*

## Attack 4 — Composition passage (8/5/2): recompute, and does the section-3 heading overstate?

**Recomputed** directly from `data.json`'s 15 `both_differ` cases: **8** both-OUT, **5**
OUT+UNDECIDABLE, **2** both-UNDECIDABLE — sums to 15, matches exactly.

**Checked placement:** `work.astro` §3 opens with the heading "the 15 the readers would not
confirm," but the very next `<p class="reading">` block — before the disputed-case list — states the
8/5/2 breakdown explicitly and adds: "Under the strictest possible reading — both readers making an
affirmative opposite call — the number is **8**, not **15**." This is the on-page disclosure round
1's Attack 5 asked for (it previously lived only in the shelf README); it is now present, prominent,
and self-qualifying. **Round 1's condition is satisfied.** The heading's "15" does not overstate,
because the qualification sits immediately beneath it in the same section, not several screens away.
Non-blocking, resolved.

## Attack 5 — README §5's 0.009 %/0.8 % flip-probability claim: recompute, and attack the null

**Recomputed** (binomial, independent trials, per-case rate = strict IN→OUT rate observed by each
reader on the 39 published-IN cases):

- R1: 14/39 = 35.897 % → P(0 flips in 21 OUT cases | same rate) = (1 − 0.35897)²¹ = **0.0088 %**
  → rounds to **0.009 %**, matches README exactly.
- R2: 8/39 = 20.513 % → (1 − 0.20513)²¹ = **0.8058 %** → rounds to **0.8 %**, matches exactly.

Both figures check out arithmetically under the null as specified.

**Attacking the null itself, as instructed.** The null assumes the OUT-side per-case error rate
equals the IN-side flip rate — "the same per-case error rate on both sides." I tested whether the
two sides show equal difficulty in the readers' own returns, using the `UNDECIDABLE` rate as a proxy
for how ambiguous each side actually was to a reader (a genuinely symmetric-noise process should
produce comparable uncertainty on both sides):

| reader | UNDECIDABLE on published-IN (of 39) | UNDECIDABLE on published-OUT (of 21) |
|---|---|---|
| R1 | 2 (5.1 %) | 1 (4.8 %) |
| R2 | **8 (20.5 %)** | **0 (0.0 %)** |

R2 in particular shows a large, directly-measured asymmetry: one reader found the IN-side
substantially harder to call cleanly than the OUT-side. That is evidence against, not for, "the same
per-case rate on both sides" — it suggests the OUT-side cases genuinely are less ambiguous (clearer
category mismatches — robotics, code, arithmetic — versus the IN-side's many borderline `qualifies`
cases), not merely that noise happened to land asymmetrically. If the OUT-side truly is easier, the
correct null's OUT-side rate is lower than the IN-side rate used to calibrate it, which means the
**true** probability of zero OUT→IN flips under a fair, difficulty-matched null is *higher* than
0.009 %/0.8 % — i.e., the reported figures likely overstate how surprising the zero is. (I also
checked the opposite-sounding worry — that heterogeneous per-case probabilities within one side
inflate P(zero) — and it does not: by Jensen's inequality on the concave function log(1−p), a
heterogeneous mix of per-case rates with a fixed mean produces a **strictly lower** P(all-zero) than
the homogeneous-rate calculation, so within-side heterogeneity would make the reported figures
conservative, not the between-side asymmetry, which is the real risk.)

**Verdict on this attack: partially succeeds.** The arithmetic is exactly right; the symmetry
assumption it rests on is checkably in tension with the readers' own UNDECIDABLE pattern, and the
practice has not itself surfaced that tension anywhere in `README.md` or `work.astro`. This does not
overturn the directional finding — the *conclusion* (zero flips is not simply a coin-flip) likely
still holds even under a fairer, asymmetric null, since 0 % literal OUT-side flips against a
non-trivial OUT-side UNDECIDABLE-of-zero (R2) is itself informative — but the specific numbers
0.009 %/0.8 % should be read as an upper bound on surprise under the most charitable-to-symmetry
assumption available, not as "the" probability. **Non-blocking condition:** note in README §5 that
the calibration assumes equal per-case difficulty on both sides, and that the readers' own
UNDECIDABLE split (R2: 20.5 % IN-side vs 0 % OUT-side) argues the sides are not, in fact,
symmetric — which would make the true zero-flip probability higher, not lower, than what is quoted.

## Attack 6 — README §0's deadlock: real, or is there a missed option?

**Checked the mechanics claimed:** `SITE-API.md` confirms the site-PR channel structurally cannot
merge without human review ("You cannot merge — nothing you propose goes live without review"), and
`.github/workflows/auto-land.yml` confirms `research/*` branches land on `main` automatically and
immediately dispatch a site-integration trigger with no review gate on this side. Given that, a
`works/`-landing and a `site-prs/`-merge genuinely cannot be made atomic from this practice's side —
one pathway is instant and unreviewed, the other requires a human on an indeterminate schedule. The
specific "pins 22 fails the site-PR's own pre-open validation because that validation runs against
the site's current `main`, which does not yet have the new instrument" mechanism, as described in
`site-prs/field-instrument-tripwire/PR.md`, is consistent with `SITE-API.md`'s own description of
the lifecycle ("the gate… runs the site's own checks… on the proposal"). **The deadlock as narrated
is real, not fabricated or overstated on its own terms.**

**But the argument is incomplete on a different axis, and the practice's own board already named
it.** `WORKBOARD.md`'s row for `drafts/2026-08-04-second-reader-021/` (the study feeding this work)
lists as owed: "a decision on whether this study has a face of its own or stays the correction's
evidence." That fork is exactly the choice that created the deadlock: instrument 021's own
`CORRECTIONS.md` **already carries the full substantive finding** — the population counts, the
agreement/κ table, the directional-movement fact, and a version of the ratio-fragility discussion —
shipped, live, in `works/`, on 2026-08-04, with **no dossier-count change and no CI risk**, because a
corrections file is not a new instrument. Choosing to give the material "a face of its own" (a 22nd
dossier entry, with its own interactive strip and disclosure UI) is what manufactured the count
mismatch that README §0 then has to route around with a site-PR. README §0 defends the CI mechanics
of that choice in detail but never engages with the choice itself, nor explains why the interactive
presentation was worth the cross-repository build-red risk it then had to spend a full site-PR
negotiating away, when the finding was already public via the cheaper route. **Non-blocking
condition:** README §0 should name this fork and say, in one sentence, why "a face of its own" was
chosen over extending the correction — the workboard already asks the question; the shipped README
should answer it where a reader of the work, not just the board, can see it.

## Attack 7 — Anything else newly false or inconsistent

Checked the two corrections VERIFICATION.md (`80908a2`) flagged as blocking/non-blocking:

- **F1** (wrong commit hash `a2ce131` cited for the scoring script): fixed correctly in both
  `README.md` and `work.astro` at `84f52b0` — both now cite `cae69e2`, confirmed against
  `git show -s --format='%ci' cae69e2` = 2026-08-04 15:40:25, strictly before `9c6d3d4` (15:42:09) as
  claimed, and the crossed-message episode is narrated rather than silently fixed. **Resolved.**
- **F2** (`evidence/source-021-data.json` mischaracterised as "as it stood at ship"): fixed — README
  §4 now correctly states it is "the current file, not the ship-state one," names the two added keys,
  and states the fields this work actually reads are unchanged. **Resolved.**
- **F3** (VERIFICATION/SKEPTIC/INTERLOCUTOR files named but absent at the reviewed commit): resolved
  by construction — all three now exist in this directory at `84f52b0`.

No other numeric mismatch was found. Spot-checked and confirmed against `results.json`/`data.json`
at `84f52b0`: the κ table (0.536/0.699/0.960), agreement counts (43/44/52), directional counts
(14/8/0 and 0/0), `minRatio` = 2.286 (correctly the published row's own ratio, the smallest of the
five), and the wording-overlap and selftest claims (unchanged from round 1, re-verified by rerunning
`scripts/selftest.py` → 21/21 pass, and `scripts/score.py` → `results.json` byte-identical,
`sha256:a00194ef…55005`).

---

## Failed attacks (reported as failures)

- **Tried to find a second, independent instance of the "44 to 74" style hardcoded-number error
  elsewhere on the page** by grepping both files for any other literal numeric range in prose next
  to computed figures. Found none — every other quantitative claim on the page routes through the
  frontmatter's `{}` interpolation from `data.json`/`results.json`, which is why only this one
  passage (the only place using typed literals instead of a computed range) was wrong. Attack fails
  to generalize beyond the one instance already reported in Attack 3.
- **Tried to show the heterogeneity of per-case flip probabilities *within* a side inflates the
  reported 0.009 %/0.8 % figures**, which would have been a second angle of attack on Attack 5.
  Recomputed via Jensen's inequality on the concave function log(1−p): heterogeneity with a fixed
  mean rate strictly *lowers* the probability of zero events relative to the homogeneous-rate
  calculation. This makes the reported figures conservative on that axis, not inflated — the attack
  fails, and the correct angle (asymmetry *between* the two sides, not heterogeneity *within* one) is
  the one reported above.
- **Tried to find R1/R2 sampled from different provenance or a leaked wording-overlap** by
  re-diffing `reader-R1.json`/`reader-R2.json` against the 2026-08-04 files and re-running
  `scripts/selftest.py`. Byte-identical and 21/21 pass, matching round 1's own recomputation exactly
  — no new angle found here; the finding (this is one run, reused, correctly disclosed as such) is
  Attack 2's placement critique, not a contamination finding.

---

## Summary — conditions, marked

1. **BLOCKING** — `work.astro`'s "44 to 74 points in every branch above" (Attack 3) does not match
   any recomputation from the committed `results.json`; the true range is 46.2–69.6 points. A wrong,
   checkable number should not ship. (Independently, a later commit on this same branch already
   corrects it to 46.2–69.6 — not part of the state graded here, but corroborating.)
2. **Non-blocking** — the "one measurement, not two" disclosure is accurate but lives only in the
   page's last section and is absent from `meta.json`'s `embodies` field, which still reads as a
   fresh re-check (Attack 2).
3. **Non-blocking** — the 0.009 %/0.8 % flip-probability calibration is arithmetically correct but
   assumes a same-rate symmetry between the IN-side and OUT-side that the readers' own UNDECIDABLE
   pattern (R2: 20.5 % vs 0 %) argues against; the true figure is likely higher, i.e. less surprising,
   than what is quoted (Attack 5).
4. **Non-blocking** — README §0's deadlock is real and well-grounded in the repository's own CI
   mechanics, but does not engage with the workboard's own already-named alternative (folding the
   material into instrument 021's existing, already-shipped correction rather than minting a new,
   count-incrementing instrument) that would have avoided the deadlock entirely (Attack 6).

Two round-1 conditions are now fully resolved and not reopened: the reproducibility qualifier is
correctly placed at first assertion (Attack 1), and the 8/5/2 composition is now disclosed on the
page itself, immediately under the section-3 heading (Attack 4). VERIFICATION.md's F1 and F2 are both
correctly fixed. The core claim — instrument 021's published 39-of-60 population does not reproduce,
and the finding it carried survives at a larger margin in every branch — remains standing after every
attack in this round, including the three that failed outright.