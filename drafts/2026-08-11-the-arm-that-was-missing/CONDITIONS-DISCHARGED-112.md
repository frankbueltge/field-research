# The six conditions, discharged — session 112

`INTERLOCUTOR-4.md` returned **STANDS WITH CONDITIONS ×6** on state `c886ea0`. All six are
discharged here, in the same session, on the same day. The verdict is published unedited; this
document says what changed and where.

**The adversary's own summary of its refutation attempt, quoted rather than characterised:**
*"Every headline number I tried to break, held."* It re-derived the arm percentages, the diff
arithmetic, the transition's full chain, the disappearance and return denominators with exact
Clopper–Pearson intervals, the exposure-corrected likelihood-ratio range (its weighting gave
**5.82–14.93** against the published **5.83–14.96**) and — from a from-scratch coordinate-descent
maximum likelihood — the underlying Weibull fit (**k = 0.6474** against **0.6476**), writing its own
code against the raw files rather than running ours. It checked every quoted string in both
documents against source and reports both of this arc's documented standing errors absent this
session.

---

**1. The exposure correction had no committed script.** Discharged: `window_exposure_correction.py`
is committed and its output reproduces the figures §3a first published. The defect was
traceability, not correctness — but the document's own claim is that every figure comes from a
committed script, and one section did not honour it. The script's population is the full dated live
corpus (**1,745.0 identifier-days against 3,142, 0.555 of a day**); §3a's text now carries those
figures rather than the first computation's restriction to identifiers determinate at both ends
(1,730.2 / 3,109), so the document states one number for one quantity.

**2. `OBJECT-ANSWER.md`'s D1 table showed the pre-correction seven-interval figures.** Discharged by
an explicit dated note rather than a silent update: the column is left as computed, the discrepancy
is named, and the reason it does not move D1 is stated — D1's input is the per-day rate over 24 full
intervals, not the seven-interval window. The adversary independently confirmed that reading.

**3. The "0.85 to 0.94" probability was the uncorrected figure**, three paragraphs above the
document's own correction of the same quantity. Discharged: **0.83 to 0.93**, with the uncorrected
figure named beside it.

**4. The return-rate interval was stated as 0.21–0.68 days.** Discharged: **0.19–0.68**. The
earlier low end was the arms' mean exposure; the true minimum is the 26 identifiers baselined at
23:05Z.

**5. The vantage paragraph named `…131` as a baseline address.** It is the session-109 census's
address and belongs to no component of the baseline union. Discharged: the four baseline runs used
`…141`, `…133`, `…129`, `…136`, this run `…143`, arm R `…128` — **six runs, six addresses, one
autonomous system**, which is a better statement of the arc's comparability guarantee than the wrong
one it replaces.

**6. D3's "went dark" and "demonstrably not sustained" overreached one stale timestamp.** Discharged
by withdrawal rather than softening: *"demonstrably not sustained"* is withdrawn; what is observed is
one page that has not regenerated its own timestamp in 209 days while describing itself in the
present tense, and we do not know whether the instrument stopped, paused, moved, or produces output
we cannot see. **The n = 1, small-to-large character of the generalisation is now named in D3 itself**
— the way D1's threshold sensitivity already was — and D3 is labelled the weakest of the three tests.
The verdict does not change; what it rests on is now stated at its real weight.

---

## And the non-blocking critique changed the work, which is the point of publishing it

The hostile critique's sharpest paragraph is about **arm R**, and it is right in a way this practice
did not see: the receiver's own paper frames those videos as failing the interface *"without an
apparent reason"*, never as gone from the public web — so nine of ten being publicly retrievable is
close to what their own paper implies. In the critique's words, a reviewer who knows that paper
*"would call arm R a well-executed measurement of a fact nobody was in serious doubt about."*

**Accepted, and acted on rather than noted.** `INCREMENT-2.md` §4 now re-prices arm R downward in
its own text: **as evidence about the platform it is worth close to nothing; as a demonstration that
the harness can be pointed at any named identifier in fifteen seconds with no credential, it is the
answer to D2 and the reason the harness must ship.** `OBJECT-ANSWER.md` §D2a carries the same
re-pricing. The version of arm R that *would* carry evidence — a public-presence arm running
**simultaneously** with an interface check, which is what would separate the receiver's 181 Error
video-days from a platform failure — is named as the thing this practice cannot produce, because the
simultaneity requires the other instrument to be running.

**One correction this practice found before the adversary reported it**, recorded because the
standing check that caught it is only worth having if its catches are published: the §5a quotation in
§3 had elided the parenthetical *(through 2026-08-18)* without marking the omission. It is restored,
and it is the exact trim session 111 was made to undo — the same error one session later, in the same
arc, caught this time by our own hand before an adversary's.

**What the verdict is good for.** This state, and nothing else. `INCREMENT-2.md` and
`OBJECT-ANSWER.md` changed after `c886ea0`; anything that ships owes a fresh gauntlet on the exact
shipped state.
