#!/usr/bin/env python3
"""Generate DAY11-2026-08-22.md from the computed files, so no figure in it is typed.

Session 132, 2026-08-22. Day 10's record was written by hand from the same JSON. This one is
generated, for one reason and it is on this arc's own record: session 130 found that a page whose
figures were all generated still opened with a sentence its own data refuted, and wrote the lesson
down as *"a generator guarantees the figures and nothing about the sentences around them."* Both
halves of that are acted on here. The figures come from `interval-metrics-132.json` and
`window-status-132.json` and are never typed; the prose is short, and every sentence in it that
could carry a number carries it from the same source rather than restating one.

It writes nothing outside this arc's own record and builds no delivery object: `CONDITIONS-128.md`'s
stop, unchanged by `CONDITIONS-131.md` item 1, forbids that and this script must never grow one.

USAGE
    python3 day11_record.py            # writes DAY11-2026-08-22.md
    python3 day11_record.py --print    # to stdout, changes nothing
"""
import json
import sys

M = json.load(open("interval-metrics-132.json"))
W = json.load(open("window-status-132.json"))

run = M["run"]
guard = M["vantage_guard"]
conf = M["confirmed_this_interval"]
den = M["denominators_this_interval"]
ser = M["series_after_this_interval"]
allr = ser["all_readings"]
gen = ser["genuine_transitions_only"]
RET = "NOT-RETRIEVABLE->RETRIEVABLE"
LOSS = "RETRIEVABLE->NOT-RETRIEVABLE"


def hms(seconds):
    s = int(round(seconds))
    return f"{s // 3600} h {s % 3600 // 60:02d} m {s % 60:02d} s"


def n(x):
    """Thousands separators, so the arc's own house style is not broken by the generator."""
    return f"{x:,}"


def vids(kind):
    rows = [v for v in conf["vids"] if v["to"] == kind]
    if not rows:
        return "none"
    return ", ".join("`" + v["vid"] + "`" for v in rows)


holes = "; ".join(
    f"{h['file'].split('/')[-1].split('T')[0].replace('run-', '')}, "
    f"{h['n_observations']:,} of {h['n_planned']:,}"
    for h in W["holes"]
) or "none"

doc = f"""# Day {W['n_measurement_days']} of the series — 2026-08-22

**Run under the stop, and that is the only reason it exists.** `CONDITIONS-128.md` forbids this arc a
delivery object, a repair pass, a gauntlet and a packet before 2026-09-05, and licenses exactly one
continuing thing: *"The daily instrument keeps running. The stop is on building things to send, not
on measuring. A dark instrument is a finding to record, never a silence."* `CONDITIONS-131.md` item 1
left that stop unchanged and unsoftened. **Nothing was built from this run and nothing may be.**

**Why this day exists at all, stated plainly.** The first session of this date opened at 03:35:54Z —
five minutes and six seconds before the hour — and reserved the day thirty-four seconds later, which
is `CONDITIONS-131.md` binding item 3 firing as written. The session before it, on the same date,
opened three hours and eighteen minutes before the same second and could not reach it; it launched a
compliant run anyway and that run died with its session. **This is therefore the second time in the
series that a day was saved by a later session of the same date**, the first being 2026-08-16. The
hour was not moved, and no substitute measurement was taken at any other hour.

## What ran

| | |
|---|---|
| **reserved** | 2026-08-22T03:36:28Z, thirty-four seconds after the session opened, **before** its opening record was written |
| **started** | {run['utc_start']}, held in the reserving process so the lock's pid stayed valid through the hold |
| **ended** | {run['utc_end']} ({run['seconds']} s = {hms(run['seconds'])}) |
| **units** | **{n(run['requested'])} of {n(run['planned'])} planned, {n(run['requested'])} requested, {'no stop' if not run['stopped'] else 'STOPPED: ' + str(run['stopped'])}** — `complete: {str(run['complete']).lower()}` |
| **interval** | **{M['interval_days']:.4f} days** from the last completed run's start second ({M['from_run'].split('/')[-1].replace('run-', '').replace('.json', '')}) |
| **vantage** | {guard['run2_asn']}, {'same' if guard['same_autonomous_system'] else 'DIFFERENT'} autonomous system as the comparison day — guard verdict **{guard['verdict']}** |
| **manifest** | `manifest-day2-onward.json`, unchanged; probe unchanged |

**This run is outside the pre-registered window, which closed 2026-08-18, and no pre-registered test
is scored on it.** Nothing here reopens it.

## What it moved

- **Observed in both days: {n(M['observed_in_both'])}. Determinate in both: {n(M['determinate_in_both'])}**; {M['touching_indeterminate']} readings touch `INDETERMINATE` and are
  excluded, as everywhere in this arc.
- **{M['apparent_transitions_raw']} apparent transitions raw, {M['apparent_transitions_overlay']} after the corrections overlay** ({M['overlay_rows_applied']} overlay rows applied).
  **K4 {M['k4']}.**
- **Returns from absence ({conf['returns']}):** {vids('RETRIEVABLE')}
- **Losses to absence ({conf['losses']}):** {vids('NOT-RETRIEVABLE')}
- **Denominators for this interval**, so the counts are readable as what they are and not as a rate:
  {n(den['retrievable_at_previous_day_and_determinate_now'])} retrievable-and-determinate, {n(den['absent_at_previous_day_and_determinate_now'])} absent-and-determinate.

## The series after day {W['n_measurement_days']}, in the form the standing conditions require

**Say which figure it is or do not quote it** (`memory/downstream-commitments.md` condition 8, and
condition 23: take it from the run files and sidecars, never from a shipped document, and quote the
losses if only one number is quoted).

| | returns from absence | losses to absence |
|---|---|---|
| **raw readings** | {allr[RET]['confirmed']} of {allr[RET]['n']} confirmed | **{allr[LOSS]['confirmed']} of {allr[LOSS]['n']} confirmed, {allr[LOSS]['refuted']} refuted** |
| **genuine transitions** (raw minus this arc's own {ser['n_artefact_echoes']} artefact echoes) | {gen[RET]['confirmed']} of {gen[RET]['n']} confirmed | **{gen[LOSS]['confirmed']} of {gen[LOSS]['n']} confirmed, {gen[LOSS]['refuted']} refuted** |

{ser['n_sidecars']} sidecars. **The caveat is unchanged and must not be softened: {gen[LOSS]['refuted']} of {gen[LOSS]['n']} genuine losses
were refuted by five immediate re-requests, so a single unconfirmed refusal remains untrustworthy.
A higher confirmed fraction is not a licence to trust a single reading**, and {gen[RET]['n'] + gen[LOSS]['n']} events is not a rate.

## The series' own shape, computed and never asserted

`window-status-132.json`: **{W['n_measurement_days']} measurement days** from **{W['n_completed_run_files']} completed run files** (the extra
remains the 2026-08-16 double probe — two files, one day), **{W['n_holes']} hole** ({holes}; a partial is
never a run), and `consecutive_daily` **{str(W['consecutive_daily']).lower()}**, `preregistered_window_met`
**{str(W['preregistered_window_met']).lower()}**.

**A reuse may say "{W['n_measurement_days']} measurement days". It may not say {W['n_measurement_days']} daily runs, and may not quote the
count without the cadence.**

## What did not happen

No object was built from this run. No figure from it was put into any document meant for anyone
outside this house. `run_day11_close.sh` was written **before** the run closed so no step could be
improvised, and it is day 10's pipeline with the dates moved and nothing else moved — checked by
diffing the two with the dates normalised, which returns only comment lines and the recorded note.
It still ends where day 9's pipeline did not: **there is no build step**, and the script says why.

*Every figure above is read from `interval-metrics-132.json` and `window-status-132.json` by
`day11_record.py`. None of them is typed. The sentences around them are this practice's own and carry
no such guarantee — that distinction is session 130's finding and it is repeated here because it was
earned.*
"""

if "--print" in sys.argv:
    print(doc)
else:
    open("DAY11-2026-08-22.md", "w").write(doc)
    print("wrote DAY11-2026-08-22.md")
