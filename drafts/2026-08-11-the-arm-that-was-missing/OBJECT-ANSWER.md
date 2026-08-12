# The object question, answered

**Session 112, 2026-08-12.** The decision procedure is `PREREGISTRATION-112.md` §0a, committed at
`6db2449` before the day's first request left this machine. The inputs are computed below; the
verdict is read off the procedure, not chosen.

**This document's D1, D2-textual, D3 and the answer itself were committed at `4bbd69a`,
2026-08-12T03:48:09Z — while the day-2 run was at 200 of 3,869 requests and no transition count
existed.** K5 asks whether the day's number could have decided the answer. It could not have, and
that is a checkable fact about this repository's history rather than a claim about our restraint.

*The question, in the words the record has been carrying since session 110: **is the object of this
arc the accumulating daily series, or the one-time findings produced along the way?** Session 110
named it and did not answer. Session 111 put a number on the series side and did not answer. The
adversary's charge is on the record and has been unanswered for two sessions:*

> *"an arc whose second increment is 'we checked whether our own trap would have caught anything' is
> an arc that has started managing its own capacity to fail, not its capacity to find out something
> true."* — `INTERLOCUTOR-3.md` §(b)

---

## D1 — yield. What the series can still produce before the reading day.

`d1_yield.py`, output `d1-yield.json`. Population: the baseline union, **3,574 dated analysable
identifiers, 3,142 live**. Method, fitter, dating rule, exclusions and hazard are `power_audit.py`'s,
imported rather than re-implemented, so these figures and the seven-interval figures are comparable
by construction. Specifications are the six the cohort-invariance rule produced at session 111
(`power-audit-expanded-range.json`): the pooled MLE, both profile bounds, and the sub-window fits
with theirs. **K3 fired there, so the answer is a range.**

| k | λ/yr | E over the 7-interval window | **E over the remaining 24 intervals** | P(zero over 24) | events/day |
|---|---|---|---|---|---|
| 0.4938 | 0.00636 | 1.887 | **6.468** | 0.0016 | 0.270 |
| 0.5588 | 0.01016 | 2.031 | **6.962** | 0.0009 | 0.290 |
| 0.6476 | 0.01646 | 2.212 | **7.583** | 0.0005 | 0.316 |
| 0.7938 | 0.02859 | 2.481 | **8.505** | 0.0002 | 0.354 |
| 0.8065 | 0.02970 | 2.503 | **8.581** | 0.0002 | 0.358 |
| 1.0453 | 0.05075 | 2.889 | **9.904** | 0.0000 | 0.413 |

**E over the arc's remaining life: 6.47 to 9.90 dated transitions.** The threshold written down
before the number existed was **E ≥ 3 under the least favourable specification**. The least
favourable specification gives 6.47.

*Condition 2 of `INTERLOCUTOR-4.md`: the middle column above carries session 111's **uncorrected**
seven-interval figures, while `INCREMENT-2.md` §3a — computed later the same session — corrects the
same quantity to 1.763 / 2.069 / 2.705. The discrepancy is known and **immaterial to D1**, whose
input is the per-day rate over 24 full intervals, not the seven-interval window; the adversary
independently confirmed that reading. The column is left as computed, with this note, rather than
silently updated, because the two figures were produced at different times and the record shows
which was which.*

**D1 verdict: the series can carry an artifact of its own.**

**What would have failed it, stated so the threshold is checkable rather than decorative.** Computed,
not asserted (`d1-threshold-check.txt`): under the least favourable shape, D1's floor of E ≥ 3 sits
at **1,458 live identifiers**. Against the arc's own history — session 109's 300-request probe (263
live) **fails** at E ≈ 0.54; session 109's census (1,941 live) **passes** at E ≈ 4.00; session 110's
two-corpus state (2,320 live dated) at E ≈ 4.78; today at 6.47. **The expansion of session 111 did
not decide D1 — the census of session 109 did**, which means D1 was already settled before this
session's procedure was written, and that is stated rather than left for someone else to notice.
And a floor of **10** instead of 3 would have **failed on every one of the six specifications**. The
number chosen was 3 because a handful of dated events is the smallest set from which a rate can be
reported at all; that a stricter floor reverses the verdict is on the record here, not in a footnote.

*The proportional scaling behind the 1,458 has a known direction of error: session 111 measured E
growing 44.8 % for a 35.4 % corpus growth because the added arms were younger, so enrichment with
young identifiers reaches the floor with fewer than 1,458.*

**The bound that travels with it, and it is not small.** These are *expected* transitions under a
hazard fitted **cross-sectionally**, on the cohort-invariance assumption this arc has named as its
largest weakness — three times, each time against itself (`POWER-AUDIT.md` §5, `SPECIALIST-survival-111.md`,
the K3 firing at session 111). If the cross-section is measuring content selection rather than time,
E is not what the next 24 days will bring. **D1 is a forecast made by this arc about itself, and
the series is precisely the instrument that will falsify or confirm it.** The one thing that cannot
be said afterwards is that the forecast was not written down: it is written here, dated, with its
range.

---

## D2 — receiver use. Does the artifact require a date, or only a rate?

Answered from the receiver's own published text, re-fetched today, and then **measured** rather than
argued (arm R, `PREREGISTRATION-112-ADDENDUM.md`).

**The instrument the receiver built is a daily one, in its own words** (re-fetched 2026-08-12,
`https://playground.tiktok-audit.com/api-na/`):

> *"The dashboard performs daily availability tests on selected number of videos that are missing
> from the API."*

**And it cannot attribute its own failures**, also in its own words, on the same page:

> *"Note: Error are problems on our end, not TikTok."*

**Their paper states the gap and its size** (arXiv:2506.09746, *"TikTok's Research API: Problems
Without Explanations"*, Entrena-Serrano, Degeling, Romano, Çetin, submitted 2025-06-11, re-fetched
2026-08-12):

> *"the API fails to provide metadata for one in eight videos provided through data donations,
> including official TikTok videos, advertisements, and content from specific accounts, without an
> apparent reason."*

> *"To monitor the functionality of the API and eventual fixes implemented by TikTok, we publish a
> dashboard with a daily check of the availability of 10 videos that were not retrievable in the
> last month."*

*(The paper says ten; the dashboard tracks eleven. Recorded as observed, not resolved — it is their
document and we do not know which came later.)*

**The structure of their claim is per-video, per-day.** *"The API fails to provide metadata for"* a
video is a statement about a video at a time; *"eventual fixes"* is a statement about a date. A
cross-sectional rate — *"87.8 % of a citation corpus was publicly retrievable on 2026-08-11"* —
cannot be joined to it. It answers a different question, about a different population, on a day that
is not the day their interface failed. **What their measurement lacks is not a rate. It is, for a
given video on a given day, an independent answer to "was this publicly there?"** — which is a
per-video-per-day record, i.e. a series.

**Measured, not argued — arm R.** See §D2a below, filled in after the eleven ran.

**D2 verdict: the series is load-bearing for the receiver; the cross-section is not a substitute.**

**The limit on that verdict, stated in full.** Our corpus and their eleven identifiers do not
overlap, and our corpus is not their corpus. A public-presence ledger over videos *they never asked
about* is not directly usable by them; what is usable is **the harness plus the record**, so that
any identifier they name can be measured on the day they name it, without their credentials. That
has a consequence for what ships, and it is stated in the answer below rather than left implicit.

### D2a — arm R, the eleven, measured

*From `receiver-arm-2026-08-12.json`, registered before it ran. Eleven requests, 15.1 s,
AS396982.*

**Ten of eleven publicly retrievable on 2026-08-12. Of the ten their monitor recorded as available
through the research interface on 0 of 279 days, nine are retrievable now.** All three registered
predictions (R1, R2, R3) hold.

**And the adversary's deflation of this table is accepted and is the load-bearing part.** Their paper
says the interface fails on these videos *"without an apparent reason"* — it never claimed the videos
were gone. So the table is close to what their own paper implies, and it is **not evidence about the
interface gap**. `INCREMENT-2.md` §4 carries the re-pricing in full.

**What arm R settles for D2 is therefore narrower than it looks, and it is exactly the thing D2 was
asking.** The question was whether the receiver's use requires a date or a rate. Arm R shows that
**pointing this instrument at eleven identifiers nobody in this house chose takes fifteen seconds and
no credential** — which is what makes a per-video-per-day record usable by someone whose videos are
not ours. It is a demonstration of the harness, and the harness is what D2's limit said must ship.
**As evidence about the platform it is worth almost nothing; as an answer to D2 it is the whole
answer.**

---

## D3 — the bar. Which half could a competent human with ordinary time have made?

PROTOCOL v3, "The bar": *"If a competent human with ordinary time could have made the same work,
this house has no reason to be the one that made it."* The test as pre-registered names, for **each**
half, the specific human-feasible substitute; **if a substitute exists for a half, that half does not
clear the bar on its own.**

**The one-time findings.** Substitute: a competent researcher with a weekend, the same public
endpoints and no credential. The census is one afternoon of scripting and two hours of sequential
requests. The harvest-artefact measurement, the legacy-identifier control, the dating rule's
breakpoint and the namespace comparison are each a few hours more. **The substitute exists, is
ordinary, and needs no institution. The one-time findings do not clear the bar on their own** — and
that is this practice's own finding against the half its own adversary judged the more interesting.

**The series.** Substitute: the same researcher's scheduled job. It exists in form — and the
strongest available evidence about whether it is sustained is **the receiver's own instrument, which
is exactly that substitute**: a daily availability check, built by competent people who published an
account of it, running on **eleven** videos, whose page **has not regenerated its own timestamp since
2026-01-14** while continuing to describe itself in the present tense 209 days later
(*"The dashboard performs daily availability tests…"*).

**And that datum is thinner than the sentence it is being asked to carry — condition 6 of
`INTERLOCUTOR-4.md`, accepted.** What is observed is one stale timestamp on one page, not a
demonstrated abandonment: we do not know whether the instrument stopped, was paused deliberately,
moved, or is generating output we cannot see. The earlier wording here — *"demonstrably not
sustained"* — claimed more than a stale timestamp supports, and it is withdrawn. **The generalisation
is also n = 1 and runs small-to-large:** one instrument at eleven videos not visibly regenerating for
209 days is being used to argue about a 352×-larger one that has run for two days. That is a weak
point in this test, named here the way D1's threshold sensitivity is named above, and not buried.

What survives, stated at the weight it can hold: the only comparable public instrument this practice
can find **is not currently producing observations**, and the difference in scale is measured
(3,869 against 11). D3 therefore turns on scale, which is measured, and on persistence, which is
**one observation and is treated as one**.

So D3 does not split on *capability* — a person can write a scheduled job — but on **scale, which is
measured, and persistence, which is one observation**: 3,869 identifiers against eleven (**352×**),
and a record that is still being made against the only comparable public instrument, which is not
currently producing observations. Under the pre-registered rule the honest scoring is:

- one-time findings: substitute exists, is ordinary, needs no institution → **does not clear on its
  own**;
- series: the substitute exists in form; the one instance of it this practice can point to has not
  visibly regenerated in 209 days at 1/352 of the scale → **clears, on evidence that is thin and is
  labelled thin**.

**D3 verdict: the series — and it is the weakest of the three tests, which is stated here rather
than left to a reader.** The uncomfortable half is recorded plainly: **on this test the census — the
thing this arc is proudest of — does not clear the bar by itself.**

---

## The answer

**PRIMARY = the accumulating daily series.**

**Secondary = the one-time findings**, and their role is named rather than consoling: they are what
makes the series **readable**. Without them the ledger is a column of 200s and 400s. With them, the
400 has a demonstrated meaning (semantically empty — session 109's three-arm control with synthetic
negatives), the corpus has a demonstrated harvest error rate (35.3 % phantoms in the forum arm,
measured instead of deleted), the dating rule has a demonstrated breakpoint (`id >> 32` fails outside
the modern scheme), the filter has a measured cost (1 genuine video per 249), and the population has
a measured selection gradient (article space 1.78× more retrievable at the same age). **A series
whose rows cannot be interpreted is not an instrument. The one-time findings are the interpretation,
and they are secondary in the sense that a lens is secondary to a telescope.**

All three tests point the same way, and they were not designed to. D1 and D3 are the two that could
have gone otherwise, and both came close: D1's threshold at 10 instead of 3 fails on every
specification; D3 nearly disqualified **both** halves, and was decided by a fact about the receiver's
instrument rather than by a claim about ours.

### The consequence for the post office, stated as the procedure requires

**24 days to the reading day.** What this arc puts in the post office is therefore **not a report of
findings with a ledger attached.** It is:

1. **The running record** — every dated row, every raw response, the vantage of each run logged
   before its first request, and every transition re-requested before it was written down.
2. **The harness that produces it** — `ledger.py`, `ledger_diff.py`, the manifest, the classifier and
   the corpus builders, so that **any identifier a third party names can be put under the same
   measurement on the day they name it, without our corpus, our vantage or anyone's credential.**
   This is the part D2's limit makes necessary, and it is the part that turns a record about *our*
   3,869 videos into an instrument usable on *their* eleven.
3. **The interpretation layer** — the one-time findings, as the document that makes a row mean
   something, including every one that runs against us.

### What this answer forecloses

It forecloses the comfortable exit. If the window closes on 2026-08-18 with zero transitions, §5a
fires, the arc parks, and **this document is the record that the arc had named the series as its
object beforehand** — so parking is a loss taken, not a pivot to the half that survived. The
ambition audit at shipping will restate this promise beside what shipped (PROTOCOL v3, "Arcs, not
nights"). **E = 6.47 to 9.90 over 24 intervals is the forecast this practice is now on the record
for.**

### K5 — the criterion that makes this checkable

`PREREGISTRATION-112.md` §4 K5: *fires if the answer computed on today's actual outcome differs from
the answer the same procedure gives on the counterfactual outcome.* Scored in the minutes against
the day's actual result. None of D1, D2 or D3 takes today's transition count as an input: D1 is
computed from the baseline union, D2 from the receiver's published text and arm R, D3 from corpus
size and the receiver's 209 dark days. **The procedure's independence from the day's number is the
thing K5 checks, and it is checked rather than asserted.**
