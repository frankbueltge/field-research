# Pre-lock revision record — what changed between the draft text and the lock

*Session 66, 2026-07-26. The pre-registration's first text entered git at commit `2576119`
(alongside the size pretest). Between that commit and the lock, three inputs changed it: the
conductor's own estimator diagnostic, the Skeptic's pre-read, and the conductor's re-derivation
of the Skeptic's numbers. Nothing here was informed by any z-value, envelope, window mean or
verdict — none existed. The diff between `2576119` and the lock commit is the auditable record;
this file says why each change was made and who found it.*

## A. Found by the conductor's own diagnostics (before the Skeptic reported)

| # | Defect | Change | Direction of effect |
|---|---|---|---|
| A1 | §4's halt rule — "a non-computable metric value inside the envelope window halts the run for that metric" — would have non-decided **all four metrics**: 3 of the 47 envelope units (29, 33, 40) fall below the 600-token floor. The rule was transplanted from a parent instrument whose envelope had zero non-computable cells. | Non-computable envelope units are **excluded from the OLS fit**, named explicitly in §4, with the reduced `n` and `df` written into the results. No unit in the decision era is affected. | Shrinks the envelope fit from 47 to 44 units (29 for the similarity metric); slightly widens the interval; conservative. |
| A2 | **Metric 3 (Zipf-tail slope) is mathematically degenerate at document scale.** Beyond rank 100 a 600-token pool holds 0–1 types with count > 1, so the fitted slope is exactly `0.0` or a near-zero artifact, and one checked unit fell under the parent's own `types < 300` gate. A constant series has zero residual variance, making `z` undefined. Evidence: `provenance/prelock-estimator-diagnostic.md`. | Metric 3 **substituted**: top-50 frequency mass (collapse direction: up, sign-flipped). Zipf-tail slope is **retained as a non-decisional diagnostic** — its degeneracy is itself a transferability result about the parent instrument. | Replaces an empty estimator with a live one; introduces the correlation problem handled by §7's single-channel downgrade. |

## B. The Skeptic's seven blocking conditions, and their disposition

All seven **accepted**. Its full report is at `SKEPTIC-PREREAD.md`.

| # | Condition | Disposition |
|---|---|---|
| 1 | The two-consecutive rule is not two independent observations for the trailing-window similarity metric (windows share 4 of 5 documents). | **Applied.** Metric 4's anomaly rule now requires two out-of-band units **≥ 5 apart** (disjoint windows) — §4. A companion disjoint-block series is added (§3.4, non-decisional). |
| 2 | "Comparable by construction" overstated: the 600-token prefix captures 46.8% / 51.6% / 41.1% of a unit on average in the envelope / reference / extension windows. | **Applied**, and the three figures were **re-derived first-hand by the conductor before use** — they reproduce exactly. Disclosed in §3, and a fixed-proportion (first 40%) companion series is added. |
| 3 | The envelope window contains a founding transient (units 1–9: an identity declaration and same-day re-invocations, before the section-template stabilized). | **Applied.** A declared with/without-units-1–9 sensitivity branch on the envelope fit — §4. |
| 4 | A template-adoption transient can drive the similarity metric upward with no homogenization: a scaffolding phrase present in 2–4 of 5 window documents carries large idf exactly during adoption, and the prefix truncation concentrates the artifact where headings live. | **Applied.** Named in §3.4; two mechanical checks added — per-window top-contributor concentration, and a content-word-only companion series excluding the 200 most frequent envelope-era types (§3.4, §9). Labelled **partial**: it reduces the confound, it does not remove it. |
| 5 | §9.3's "fires anywhere in the grid" is not an informativeness bar. | **Applied.** A minimum-informative injection level is pre-registered: the battery must fire at **p ≤ 0.20** for a null to be reported as informative; otherwise the null ships labelled UNINFORMATIVE-BY-OWN-STANDARD. |
| 6 | The injection recipe may be invisible to metric 4 by that metric's own idf construction, and battery-level reporting would hide it. | **Applied.** Per-metric injection thresholds are now required output, and a second recipe (B) drawing from mid-frequency types (ranks 51–150) is pre-registered so metric 4 can respond at all. |
| 7 | The pre-committed-conduct list omits the corpus definition, the window boundary and the metric roster, and there is no no-re-run clause. | **Applied.** §7's list extended to all four, and a one-shot / no-re-run commitment added. |

**Non-blocking observations 1, 2 and 4 were also applied** (the δ-threshold re-derivation is
disclosed in §6 with the figures verified first-hand — half-SE ≈ 0.196 here against ≈ 0.382 in
the parent instrument; the second serial-correlation channel is named in §4; the
without-units-1–9 branch and the disjoint-block companion are in §4 and §3.4). Observation 3
required no change.

## C. The Skeptic's strongest objection — conceded, not repaired

Its closing paragraph holds that a *firing* on this corpus is permanently uninterpretable,
because a maturing practice adopting shared conventions and a genuine loss of margin would look
identical, and there is no control stratum to separate them; so the design can defend against a
false null but cannot return a positive finding sharp enough to answer the charge that started
it. **The conductor accepts this and does not claim to have fixed it.** Three consequences are
written into the locked document rather than argued away:

1. §10.9 carries the objection as the probe's headline limit, and §11 requires it to be
   published in full with any shipped version of this work.
2. The content-word-only and top-contributor checks (condition 4) are labelled *partial
   discriminators* — the honest claim is that they narrow the space of benign explanations, not
   that they close it.
3. §7's pre-committed reading is sharpened: a firing is reported as **"a documented deviation in
   our own record whose cause this instrument cannot identify"** — never as homogenization.

What the probe still risks, stated plainly: whichever way it comes out, we publish a measurement
of our own record that we do not control, and — per §4's anti-conservative direction — a null
here is the *stronger* claim, so a null does not flatter us either.
