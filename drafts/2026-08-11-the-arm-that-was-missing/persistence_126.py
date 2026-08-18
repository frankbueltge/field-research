#!/usr/bin/env python3
"""persistence_126 - how stable is an absence, measured across the whole series rather than at
its edges.

Session 126, 2026-08-18. This computes finding 7 of `CONDITIONS-125.md`, which the previous
session's adversary found in this practice's own six-day series and which this practice, having
had the file for six days, had never looked at.

WHY IT MATTERS, STATED BEFORE THE NUMBERS
-----------------------------------------
The bundle's confirmation evidence is a 9-event transition record: every apparent state change
between two days was immediately re-requested five times, and the record says how many survived.
Nine events is a small sample and the bundle says so. But the same series carries a much larger,
entirely independent form of confirmation that the bundle never reports: an identifier that is
absent on day 1 and absent on all six days has had its absence re-observed five more times, at
24-hour spacing, from the same vantage. That is not the same quantity as an immediate re-request
- it cannot separate a persistent network condition from a persistent platform state, and it says
nothing about identifiers that were never absent - but it speaks to the question a receiver
actually has: *is a single refusal a fluke?*

WHAT IS AND IS NOT COUNTED
--------------------------
- The **non-control panel only**: arms `A`, `A2`, `A-new` and `B` (3,620 of the 3,869 rows).
  The control arm is `B-truncated` - identifiers deliberately mutilated so they cannot resolve -
  and its persistence is a property of the construction, not a measurement. The arms are read
  from the file rather than hard-coded to a count; only the control label is named here.
- A reading is **determinate** if it is RETRIEVABLE or NOT-RETRIEVABLE. INDETERMINATE readings
  are neither, and this practice established at session 115 that indeterminacy is a property of
  the request rather than of the video, so a day on which a unit read INDETERMINATE is a day that
  unit was not measured - it is excluded, never counted as agreement.
- "Ever absent" means at least one determinate NOT-RETRIEVABLE reading across the six days.
- "Absent on every day it was measured" means every determinate reading it has is
  NOT-RETRIEVABLE. A unit with exactly one determinate reading trivially satisfies that, so the
  count is reported both ways: all ever-absent units, and only those with >= 2 determinate days.
- "Absent on all six days" is the stricter reading: all six readings are NOT-RETRIEVABLE, so a
  single INDETERMINATE day breaks it.

TWO NUMBERS, AND WHY BOTH ARE PRINTED
-------------------------------------
`CONDITIONS-125.md` finding 7 records the previous session's adversary as finding that "412 of the
446 ever-absent identifiers are absent every day they were measured (92 %)". The 446 reproduces
exactly and so does the count of 7 multi-state units. **The 412 does not match the sentence
attached to it.** 412 is the count under *absent on all six days*; under *absent on every day it
was measured* - the wording the finding uses, and the one this practice's own established reading
of INDETERMINATE requires, since a day a unit read INDETERMINATE is a day it was not measured -
the count is 439 of 446. The 34-unit gap is 7 units that were genuinely retrievable on some day
and 27 whose only non-absent readings are INDETERMINATE.

Neither number is wrong; the label on 412 is. Both are printed, each with the definition that
produces it, and the bundle carries both. The stricter one is the conservative figure and is the
one a receiver should quote if they quote only one.

Every figure this session's record quotes about persistence is read from this script's output.
"""
import csv
import json
import sys

DAYS = ["baseline", "2026-08-12", "2026-08-13", "2026-08-14", "2026-08-15", "2026-08-16"]
DETERMINATE = {"RETRIEVABLE", "NOT-RETRIEVABLE"}
CONTROL_ARM = "B-truncated"


def main(path="deliverable-v0.3/series/presence-series.csv",
         out="persistence-126.json"):
    rows = list(csv.DictReader(open(path)))
    panel = [r for r in rows if r["arm"] != CONTROL_ARM]
    control = [r for r in rows if r["arm"] == CONTROL_ARM]

    ever_absent = []
    always_absent = []
    always_absent_multi = []
    absent_all_six = []
    only_indeterminate_breaks = []
    multi_state = []
    n_determinate_days = {}

    for r in panel:
        readings = [r[d] for d in DAYS]
        det = [x for x in readings if x in DETERMINATE]
        n_determinate_days[r["video_id"]] = len(det)
        if not det:
            continue
        states = set(det)
        if len(states) > 1:
            multi_state.append(r["video_id"])
        if "NOT-RETRIEVABLE" in states:
            ever_absent.append(r["video_id"])
            if states == {"NOT-RETRIEVABLE"}:
                always_absent.append(r["video_id"])
                if len(det) >= 2:
                    always_absent_multi.append(r["video_id"])
                if len(det) == len(DAYS):
                    absent_all_six.append(r["video_id"])
                else:
                    only_indeterminate_breaks.append(r["video_id"])

    ever_absent_multi = [v for v in ever_absent if n_determinate_days[v] >= 2]

    def pct(a, b):
        return round(100.0 * a / b, 4) if b else None

    def frac(a, b):
        """The same quantity as a proportion in [0,1]. `figures.pct` multiplies by 100, so the
        percent fields above must never be handed to it; these exist so the bundle's prose is
        rendered from a value of the type its renderer expects."""
        return (a / b) if b else None

    report = {
        "schema": "field-research/absence-persistence/1",
        "source": path,
        "computed_by": "persistence_126.py",
        "days": DAYS,
        "n_rows_total": len(rows),
        "control_arm": CONTROL_ARM,
        "n_panel_non_control": len(panel),
        "arms_in_panel": sorted({r["arm"] for r in panel}),
        "n_control_rows_excluded": len(control),
        "n_units_with_no_determinate_reading": sum(1 for r in panel
                                                   if n_determinate_days[r["video_id"]] == 0),
        "n_ever_absent": len(ever_absent),
        "n_absent_on_every_day_measured": len(always_absent),
        "pct_absent_on_every_day_measured": pct(len(always_absent), len(ever_absent)),
        "frac_absent_on_every_day_measured": frac(len(always_absent), len(ever_absent)),
        "n_ever_absent_with_2plus_determinate_days": len(ever_absent_multi),
        "n_absent_on_every_day_with_2plus_determinate_days": len(always_absent_multi),
        "pct_of_2plus_absent_on_every_day": pct(len(always_absent_multi), len(ever_absent_multi)),
        "n_absent_on_all_six_days": len(absent_all_six),
        "pct_absent_on_all_six_days": pct(len(absent_all_six), len(ever_absent)),
        "frac_absent_on_all_six_days": frac(len(absent_all_six), len(ever_absent)),
        "n_never_retrievable_but_broken_only_by_indeterminate": len(only_indeterminate_breaks),
        "reconciliation_of_the_two_readings": (
            "n_ever_absent = n_absent_on_all_six_days "
            "+ n_never_retrievable_but_broken_only_by_indeterminate "
            "+ n_units_with_more_than_one_determinate_state"
        ),
        "reconciliation_holds": (len(ever_absent) == len(absent_all_six)
                                 + len(only_indeterminate_breaks) + len(multi_state)),
        "n_units_with_more_than_one_determinate_state": len(multi_state),
        "units_with_more_than_one_determinate_state": sorted(multi_state),
        "what_this_is_not": (
            "Not an immediate re-request. Repeated absence at 24-hour spacing from one vantage "
            "cannot separate a persistent network or endpoint condition from a persistent "
            "platform state, and it says nothing about units that were never absent. It is "
            "independent of the 9-event transition-confirmation record and much larger."
        ),
    }
    json.dump(report, open(out, "w"), indent=1)
    print(json.dumps(report, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
