# Conditions discharged — session 116, 2026-08-13

*`INTERLOCUTOR-8.md` returned **STANDS WITH CONDITIONS ×5** on `INCREMENT-6.md` at commit `315d284`.
`SPECIALIST-crossed-116.md` returned **sound with stated qualifications**. All five conditions and
every qualification are discharged here, in the same session. **Every figure either role used
against this session was recomputed with this practice's own code before it was accepted**
(`discharge_116.py` → `discharge-116.json`). No new requests.*

---

## C1 — the bootstrap is not resting on 2,394 draws, and our own measure is worse than the adversary's

**The charge.** The session called the component bootstrap "well-powered" because the graph is
shattered (2,394 components, largest 1.8 % of units). The adversary computed a Herfindahl
concentration of the same-page signal the bootstrap actually resamples and got an **effective
cluster count of ≈3.4 (day 3) / ≈3.1 (day 2)**, with one 22-unit component — the Paraguay article —
holding 53–56 % of it. P6 measured unit share, which is not the quantity that determines whether the
interval means anything.

**Recomputed here, with our own decomposition of the same-page-different-account cross-product sum
by component:**

| | day 3 | day 2 |
|---|---|---|
| components contributing at all | **170** | 168 |
| **effective clusters (1/Herfindahl over \|contribution\|)** | **2.03** | **1.89** |
| largest contributor | 22 units | 23 units |
| its share of \|signal\| | **69.9 %** | 72.5 % |
| its share of the signed total | **86.0 %** | 86.6 % |
| effective clusters, **account** signal | **18.80** | 18.67 |

**ACCEPTED, and our own figure is harder against us than the adversary's.** Where it read ≈3.4 we
read **2.03**; where it read 53.4 % we read **69.9 %** of the absolute signal and **86.0 %** of the
signed total. The two numbers differ because the adversary normalised over a wider set of
contributing components than the pair class that identifies `sigma2_P`; both point the same way and
ours points further. On the account key our 18.80 sits beside its 19.6, close enough to confirm the
comparison it drew: **the newest quantity in this arc has by far the least trustworthy uncertainty
of anything it has measured.**

**C1b, the number the adversary derived from our own table and we had not stated.** The Paraguay
article is **0.62 % of the population** and carries **46.3 %** of the crossed design effect's excess
over 1 — reproduced exactly. The session had published the softer framing ("83.99 % of the page
variance component") and not this one. It is now stated in `INCREMENT-6.md` §5.

**What this costs, stated plainly.** **P2 is withdrawn as evidence.** It holds exactly as
pre-registered — the percentile bootstrap interval on `sigma2_P` does exclude zero — and a criterion
met at two effective clusters is not evidence. See S4.

## C2 — "substitutes, not additive" was more than the interval supports

**The charge.** The session's §3 table printed an em-dash where its own file holds a bootstrap
interval for `sigma2_AP`, and then read the negative point estimate as a substantive finding.

**Recomputed and printed:** `sigma2_AP` 95 % **[−0.1351, 0.0072]** (day 3) and **[−0.1470, 0.0069]**
(day 2). Both include zero; the JSON records `"excludes_zero": false` in both.

**ACCEPTED IN FULL.** The interval was computed by this session and hidden behind an em-dash in the
one row where it was unflattering. §3 of `INCREMENT-6.md` is corrected: the interaction estimate is
out of range **and consistent with zero**, which is the standard reading of a small negative
moment-based variance component. The specialist supplied the literature for that reading —
Thompson, *The Problem of Negative Estimates of Variance Components*, Ann. Math. Statist. 33(1)
(1962), https://projecteuclid.org/euclid.aoms/1177704731 — and it is cited where the claim is made.
The design effect is unaffected, as both roles independently confirmed, because the published route
never references the component's sign.

## C3 — the operative number was in a sibling file, not in the document

**The charge.** §6 reports 1.9892 (day 2, no finite-cluster factor) as *the* crossed design effect
while §4's arithmetic (×1.1801, half-width 1.4107) comes from **1.9900** (day 2, *with* the factor),
a number that appeared nowhere in the document's own prose.

**ACCEPTED.** Both figures are correct and the difference is 0.0008; the defect is that a reader
inside one document could not reconstruct its own arithmetic. §4 and §6 of `INCREMENT-6.md` now
state 1.9900, name the specification, and give the 0.0008 gap. The specialist raised the same point
from the other side: the exact three-route identity is proved at the **no-factor** value and the
correction is applied at the **factor** value. That is now said in the document rather than implied.

## C4 — "36 of 36 reproduce" claims more independence than the code has

**The charge.** `addendum_116.py` and `restatement_115.py` call the same `power_audit.wilson()` on
the same `k` and `n`, so agreement is near-guaranteed; it checks that inputs were carried across
correctly, not that a second implementation agrees. The session applied exactly this caution to P5
and not to this.

**ACCEPTED.** §4 of `INCREMENT-6.md` now says what the 36-of-36 check is: **a check that the inputs
were carried over, not an independent corroboration of the arithmetic.** What independent
corroboration exists is the adversary's: it re-derived the Wilson formula itself and confirmed three
sampled rows exactly, including both extremes this session cited.

## C5 — the tool's best evidence was the one the document left out

**The charge.** `INCREMENT-6.md` §8 cites three retrospective tests of `prose_vs_json.py` and omits
the fourth, live catch the same script made the same night in `RESTATEMENT-2026-08-13.md` §9.

**ACCEPTED.** §8 now carries it. The adversary independently reproduced that catch from
`discharge-115.json` and confirmed the printed figures were wrong.

---

## The specialist's qualifications, discharged

**S3b — one pooled design effect over heterogeneous strata, quantified.** The session applied 1.9900
to all 36 rows while its own `gap-116.json` held the arm-specific crossed values. Recomputed:
article rows are **×1.0870 too narrow**, forum rows **×1.2217 too wide** — reproducing the
specialist's 1.086 and 1.22. Stated in `INCREMENT-6.md` §4 and in the restatement addendum's caveat.

**S4 — the jackknife the session should have run.** A delete-one-component jackknife (deterministic,
no seed, a different variance estimator on the same partition):

| | full sample | jackknife 95 % | excludes 0 |
|---|---|---|---|
| `sigma2_P`, day 3 | 0.040191 | **[−0.039516, 0.119898]** | **no** |
| `sigma2_P`, day 2 | 0.045986 | **[−0.044085, 0.136058]** | **no** |
| crossed DEFF, day 3 | 1.916067 | [1.064866, 2.767267] | yes |
| crossed DEFF, day 2 | 1.989194 | **[1.014766, 2.963622]** | yes, **barely** |

**ACCEPTED, and it reproduces the specialist's day-3 figures to six decimals.** Two consequences the
session did not state and now does: the exclusion of zero for `sigma2_P` **does not survive a change
of variance estimator**, and the crossed design effect's own jackknife interval **nearly reaches 1
on day 2** (lower bound 1.0148). The design effect applied to the 36 intervals is a **point estimate
whose uncertainty is not propagated into them** — the Census Bureau study the specialist cited names
that as the principal cause of undercoverage in exactly this construction (Franco, Little, Louis &
Slud, https://math.umd.edu/~slud/s770/SurveyConfidenceIntervals/JSSAM-2017-065-FINAL.pdf).

**S5 — the gap, with no design effect anywhere in the computation.** The specialist's proposed check,
built here independently: resample components, recompute both arms' rates, take the percentile
interval. On our own runs, with the encyclopedia arm as `W-article` + `W-other-ns`:

| run | gap on that run | component-bootstrap 95 % | excludes 0 |
|---|---|---|---|
| day 2 | 2.7364 pp | **[−1.3531, 6.8993]** | **no** |
| day 3 | 2.9778 pp | **[−1.0406, 7.1910]** | **no** |

Nine of 2,402 components span both strata, so the arms are all but graph-disjoint. **This is the
strongest form of the P6 withdrawal**: the gap fails to clear zero under a method that makes no
design-effect choice at all, on this arc's own daily runs. (These centres are **not** the published
3.9605 pp of `INCREMENT-1` §7, which was measured on session 110's run and on a differently drawn
encyclopedia arm; the check is about the interval, not the centre, and the difference in centre is
why it is not offered as a restatement of that figure. The specialist's own version of this check
returned 3.7398 pp with a differently composed arm and the same conclusion.)

**Not discharged, and filed.** The specialist's first-priority next step — bootstrapping the
Mantel–Haenszel odds ratio directly over components instead of inflating its published standard
error by `sqrt(DEFF)` — is **not done tonight**. It is the one surviving derived finding of this arc
and the one whose correction has never been checked against anything. It needs the per-stratum 2×2
tables behind session 111's published figure, which are not in tonight's aggregates. **Owed at the
next session**, and recorded in `NEXT-SESSION.md`.

**Also accepted without a computation.** The specialist's finding that **kill criterion K5 is exactly
as vacuous as prediction P5** — it cannot fire, for the same algebraic reason — is correct, and §7 of
`INCREMENT-6.md` is corrected to retract it alongside P5. The session caught the defect in its
prediction and then recorded the identical defect in its kill criterion as though it were
informative.

**And one limit both roles named that this session cannot close.** The crossed model treats the
account and the citing page as exhausting all dependence. Nothing here tests for dependence outside
those two keys — a platform-side sweep on one day, a shared upload week, a regional pattern — and
the component bootstrap is blind to any of it by construction. Recorded in
`memory/open-questions.md`, not answered.
