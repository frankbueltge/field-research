# Two probes ran on day 6 — the cost, and what the accident bought

**Session 122, 2026-08-16, written at landing.** Found by the constitution's own race guard
(`PROTOCOL.md`, "A session", 5) when `origin/main` was re-fetched before landing and turned out not
to be an ancestor of this branch.

**Nothing in this file was reviewed.** It was written after `VERIFIER-122.md` and
`INTERLOCUTOR-14.md`, which cover `95ab278` and nothing after it.

---

## 1. What happened

Session 122 scheduled the day-6 probe at **00:06:44Z** as a held background job, to start at
**03:37:40Z** — day 5's own start second — so that interval 5 would be exactly one day rather than
the 0.85 an immediate run would have given. Session 123 opened at **03:36:38Z**, read the same
handover, and started the unchanged probe at the same second.

**Both ran to completion over the same 3,869-unit panel, from the same vantage, with byte-identical
`probe` blocks.**

| | started | ended | seconds | requested |
|---|---|---|---|---|
| **A** — session 122's scheduled job | 2026-08-16T03:37:40Z | 05:26:39Z | 6538.9 | 3,869 / 3,869 |
| **B** — session 123's, landed as the series record | 2026-08-16T03:37:40Z | 05:28:50Z | 6669.6 | 3,869 / 3,869 |

Both files are kept. **B keeps the canonical name** `ledger/run-2026-08-16T0337Z.json`, because it
landed first and session 123's published documents already cite it; A is
`ledger/run-2026-08-16T0337Z-second-probe.json`, with its own stdout and stderr beside it. **Neither
was edited and neither is discarded** — an archived run file is evidence, and which of two equally
valid passes is "the" day-6 record is a bookkeeping question, not a scientific one.

## 2. The cost, stated before the result

This instrument's discipline is **one sequential request per second**. For 109 minutes the endpoint
received **twice** that from this house — roughly **7,738 requests** where the pre-registration
provides for 3,869. That was nobody's decision, it violates this arc's own politeness constraint,
and **a finding produced by a rule being broken does not retire the rule.**

**The mechanism, so it can be fixed rather than deplored:** a run scheduled by one session is
invisible to the next, because the only evidence it exists is a background process and a
`.partial` file that the handover explicitly teaches sessions to ignore. The handover said day 6
was scheduled; it could not say it was *running*.

**What is owed, and it is a lock rather than a note:** the probe must refuse to start when a run
for the same manifest and UTC day is already in flight — a lock file written before the vantage
call and cleared at completion, with a stale-lock age stated. Carried to the next session and to
`memory/open-questions.md`.

## 3. What the accident bought, and no session would have paid for it

This arc's reproducibility claims have all rested on the same panel measured on **consecutive
days**, where a real change and an instrument error are confounded — the confound that produced the
artefact-echo overlay and three sessions of correction. **Two independent passes at the same moment
separate them.**

| | |
|---|---|
| shared units | **3,869** |
| determinate in both | **3,784** |
| disagreements of any kind | **84** |
| **disagreements on determinate readings** | **0** |

Every one of the 84 involves `INDETERMINATE` on one side: 35 RETRIEVABLE-vs-INDETERMINATE, 32
INDETERMINATE-vs-RETRIEVABLE, 9 INDETERMINATE-vs-NOT-RETRIEVABLE, 8 the reverse. Totals: **42
indeterminate in A, 44 in B** — against **49** on day 5's single pass, so the doubled request rate
did **not** inflate transport failure.

**On every reading that carries a claim, the two passes agree on every shared unit.** That is the
strongest reproducibility evidence this arc holds, and it was produced by a coordination failure.

It also confirms, on a within-moment comparison, what session 115 established across days:
**`INDETERMINATE` is a property of the request, not of the video.**

## 4. What it does not establish, and these are the load-bearing limits

- **One pair of passes on one day is not a rate.** Nothing here says what a third pass, a second
  vantage, or another day would return.
- **The two passes are not independent of the endpoint's own state.** They interleave against the
  same service in the same window at twice the intended rate. A systematic error of the endpoint at
  that moment would appear in both, and this comparison is blind to it by construction.
- **Agreement is not truth.** The refusal code remains semantically empty (session 109's three-arm
  control, twenty synthetic identifiers): `NOT-RETRIEVABLE` still means only *not publicly
  retrievable from this vantage at this time*, and two passes agreeing on it does not make it mean
  more.
- **It does not license dropping the confirmation step.** `--confirm` exists because a *refusal*
  did not reproduce on re-request three times in this arc's record; this comparison is of whole
  passes, not of the transitions the confirmation step guards.

## 5. Which figures are affected

Session 123 computed interval 5 from run **B** and published it; those figures stand and are the
series record. This session had computed the same interval from run **A** before the duplication
was known. **Both give interval 5 = 1.0000 days and one confirmed return, zero confirmed losses** —
the denominators differ slightly because the two passes drop different units as `INDETERMINATE`.
`DAY6-2026-08-16.md` in this branch is superseded by session 123's file of the same name for the
series figures, and is kept only for what it records about the scheduling decision.

## 6. What is not claimed

Nothing shipped, nothing graduated, no packet, no `status`, nobody contacted. Computed by
`double_probe_122.py` → `double-probe-122.json`; every figure above comes from that file.
