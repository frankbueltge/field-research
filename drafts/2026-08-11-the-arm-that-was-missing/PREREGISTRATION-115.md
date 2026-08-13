# Pre-registration — session 115, day 3 of the window, and the dated restatement

*Written and committed on 2026-08-13 **before the first measurement request of this session left this
machine**, as at sessions 100–114. Everything below is a commitment, not a report. The scoring is in
`INCREMENT-5.md` and the deviations in `DEVIATIONS.md`.*

## 0. What this session is bound to, and by whom

`NEXT-SESSION.md` (session 114's addendum, written after its gauntlet) fixes the order:

1. the dated restatement of every interval this arc has published — **before any new measurement**;
2. day 3 of the pre-registered window;
3. the public scoring of the `grimhoundgaming` prediction, which day 3 settles;
4. consolidation, owed at this session at the latest.

The restatement is written first and measured second only in the sense that its **method** is fixed
here before either runs. The day-3 run is started as early as the session allows because it takes
about 1.8 hours of wall clock; the restatement is computed while it runs. **Neither result may be
allowed to change the other's stated method.**

## 1. Population — unchanged, and closed

**Day 3 measures `manifest-day2-onward.json`, 3,869 units, and nothing else.** The window population
was closed at session 111 and no identifier is added to it, in particular not from the account-state
arm session 114 opened (`probe_account_state.py`). That arm has no baseline inside this window and a
second series may not start without its own pre-registration.

The probe is `ledger.py`, **unchanged since the session-109 census**: the credential-free oEmbed
endpoint, sequential, one request per second, 25 s timeout, HTTP 429 ends the run by design. Changing
it between runs would make the runs incomparable.

## 2. Method, fixed in advance

**Day 3.**
`python3 ledger.py manifest-day2-onward.json ledger/run-<UTC>.json`, then `ledger_diff.py` twice —
against `ledger/baseline-union.json` **and** against `ledger/run-2026-08-12T0341Z.json` — then
`confirm_transition.py` on the day-2→day-3 diff. **A transition is written down only after five
immediate re-requests all agree with the new state.** The vantage is logged before the first
measurement request and the diff refuses to compare across autonomous systems.

**The restatement.** Every interval this arc has published that treats **one video as one
independent observation** is recomputed as a **Wilson interval on an effective sample size
`n_eff = n / DEFF`**, with `DEFF = 1.4289` — the closed-form clustered variance on the account key,
which needs no random seed (`INCREMENT-4.md` §3; *not* the 1.458 that session first printed off a
single bootstrap seed). **The point estimate `p = x/n` does not move and is republished unchanged
beside the widened bound.** Three things are stated in the restatement itself and are not optional:

- **1.4289 is a lower bound, not the correction.** The citing-page key gives 1.8854 on the same
  units, fragile and carried by one article (`es.wikipedia.org|Protestas en Paraguay de 2023`), but
  real. The restated intervals are therefore *still* possibly too narrow, and say so.
- **The pooled design effect is applied to stratified cells as an approximation.** Whether it is a
  reasonable proxy is **tested, not assumed**: a per-cohort design effect is computed on the same
  account key wherever a cohort has enough clusters to carry one, and the pooled figure is reported
  against them.
- **A likelihood-based interval is not a Wilson interval.** The Weibull shape CI
  (`POWER-AUDIT.md` §2, `k = 0.6959`, [0.5017, 0.8983]) is corrected by a **first-order Rao–Scott
  scaling of the profile deviance** — the χ² cut-off multiplied by DEFF — and that is labelled as
  the different, weaker operation it is.

**The subtract-first check (binding).** Before the restatement is published, every restated bound is
subtracted from its published counterpart and the differences are printed. Sessions 113 and 114 each
published a number their own tables refuted; this check exists because of them.

## 3. Predictions — written before the run

- **P1 — transitions in interval 2.** The forecast this practice is on the record for is 6.47–9.90
  transitions across the 24 intervals to the reading day, i.e. **0.27–0.41 per interval**. Predict
  **0, 1 or 2 confirmed transitions** in day 2 → day 3, `grimhoundgaming` excluded and counted
  separately under P2.
- **P2 — `grimhoundgaming`.** The account returned `status_field 10221` with no `userInfo` at
  ~23:45Z on 2026-08-12, while **6 of its 7 cited videos were RETRIEVABLE at 03:41Z that morning**
  (the seventh, `7623551369546304781`, was already NOT-RETRIEVABLE). Predict **all 7 NOT-RETRIEVABLE
  on day 3** — account death propagates to the video endpoint within one day.
- **P3 — the return persists.** `7446448990935354670` (`iidahmer`) went NOT-RETRIEVABLE →
  RETRIEVABLE in interval 1 and survived five re-requests. Predict it is **still RETRIEVABLE on day
  3**: a return that holds, not a flicker.
- **P4 — the pooled rate.** Day-2 determinate retrievability was **3,146 / 3,829 = 82.1624 %**.
  Predict day 3 within **±0.40 pp** of it.
- **P5 — indeterminacy churns.** Day 2 had **40 INDETERMINATE**. Predict day 3 in **15–70**, and
  **fewer than half of day 2's 40 identifiers** indeterminate again — i.e. indeterminacy is a
  property of the request, not of the video.
- **P6 — the restatement moves no centre and widens every bound.** Predict the subtract-first check
  shows **every recomputed half-width larger** than its published counterpart and **every point
  estimate identical to the published digit**.
- **P7 — the pooled DEFF is a fair proxy per cohort.** Predict the per-cohort design effects, where
  computable, **straddle 1.4289** rather than sitting systematically above or below it.

## 4. Kill criteria — each written with the candidate that could pass it

- **K1 — an incomplete day is a dark day, not a short one.** If the run stops on HTTP 429 with more
  than 10 % of the manifest unmeasured, **interval 2 is not scored**, and the day is recorded as
  dark. *Passable by:* a complete 3,869-unit run — days 1 and 2 both achieved one.
- **K2 — vantage.** If the run's ASN differs from **AS396982**, the run is flagged and **not
  diffed** against the previous days. *Passable by:* AS396982 again, as on days 1 and 2.
- **K3 — confirmation.** A transition whose five re-requests do not all agree with the new state is
  **not** written down as a transition; it is recorded as unconfirmed. *Passable by:* the interval-1
  return, which agreed 5/5.
- **K4 — the restatement withdraws if a centre moves.** If the subtract-first check shows any point
  estimate changing, the restatement is **wrong by construction** and is withdrawn before
  publication rather than explained. *Passable by:* identical centres with wider bounds — the
  arithmetic the method is designed to produce.
- **K5 — partial propagation is not a refutation.** On P2: **0 of 7** turning refutes propagation
  within one day; **7 of 7** confirms it; anything between is recorded as **not established** and
  the mechanism claim is not made in either direction. *Passable by:* 7 of 7, which is what the
  account state predicts if the endpoint follows it.

## 5. What this session will not claim

Nothing ships tonight unless a fresh gauntlet runs on the exact shipped state; `INTERLOCUTOR-6.md`'s
verdict is good only for state `75987b8`. No packet, no `status`, nothing addressed to anyone. The
organisation named as this arc's receiver has not been and will not be contacted by this practice.
