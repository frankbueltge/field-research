#!/usr/bin/env python3
"""stop_clock - the arithmetic of PREREGISTRATION-135.md Q1, computed rather than typed.

Session 135, 2026-08-25.

WHY THIS IS A SCRIPT AND NOT THREE SENTENCES
--------------------------------------------
The arithmetic here is small enough to do in the head, and that is exactly the reason it is not
done in the head. This practice has had a hand-carried figure found wrong against a
machine-written artifact beside it in THREE CONSECUTIVE SESSIONS (`CONDITIONS-134.md` finding 2,
and `ERRATA-134.md` E48, which made the same error a fourth time inside the erratum correcting
it, forty minutes later). A session that responds to that record by typing four more dates into
prose has not read its own record.

Every date this file prints is derived from the INPUTS block below. Every input carries the file
and the sentence it was read from. Nothing here fetches anything; nothing here is a judgement.

WHAT THIS FILE DOES NOT DECIDE
------------------------------
It computes dates. Whether the stop should change is a decision, it is made in `INCREMENT-23.md`
under the constraints `PREREGISTRATION-135.md` §4 fixed before these numbers existed, and no
output of this script is an argument for any of the four admissible decisions.

USAGE
    python3 stop_clock.py -o stop-clock-135.json
"""
import argparse
import datetime
import json
import sys

# --------------------------------------------------------------------------------------------
# INPUTS. Each is a date or an interval read out of a named file. None is computed here, and none
# is this session's own judgement. A reader who disagrees with an output should disagree with one
# of these first.
# --------------------------------------------------------------------------------------------
INPUTS = {
    "reading_date": {
        "value": "2026-09-05",
        "source": "PROTOCOL.md, section 'The reading of 2026-09-05'",
        "quote": "The architect reads the four-week review and the first investigation together on "
                 "2026-09-05",
    },
    "stop_end_exclusive": {
        "value": "2026-09-05",
        "source": "CONDITIONS-128.md, section 'Binding on the next session'; unchanged by item 1 "
                  "of CONDITIONS-131.md, -132.md, -133.md and -134.md",
        "quote": "No repair pass, no tenth gauntlet, no packet from this arc before 2026-09-05.",
        "note": "'before' is exclusive: the earliest date the stop permits a packet is the "
                "reading date itself.",
    },
    "architect_bind_days": {
        "value": 7,
        "source": "PROTOCOL.md, section 'Leaving the house'",
        "quote": "a packet that reaches `prepared` is sent or withheld with a dated reason within "
                 "seven days - no packet lies undecided.",
        "note": "A CEILING on the architect's time, not a required wait. He may decide sooner, "
                "and this script reports both readings rather than the one that flatters this "
                "session's disclosed interest (PREREGISTRATION-135.md section 1).",
    },
    "today": {
        "value": "2026-08-25",
        "source": "date -u +%F, run at session open",
    },
    "in_practice_first_investigation_start": {
        "value": "2026-08-11",
        "source": "the arc directory's own slug, drafts/2026-08-11-the-arm-that-was-missing/",
    },
}


def d(s):
    return datetime.date.fromisoformat(s)


def main(out_path):
    reading = d(INPUTS["reading_date"]["value"])
    stop_end = d(INPUTS["stop_end_exclusive"]["value"])
    bind = INPUTS["architect_bind_days"]["value"]
    today = d(INPUTS["today"]["value"])

    # D_guaranteed: the latest date a packet may reach `prepared` such that the constitution's own
    # bind GUARANTEES a dated send-or-withhold decision on or before the reading.
    d_guaranteed = reading - datetime.timedelta(days=bind)

    # D_possible: the latest date a packet may reach `prepared` such that a decision before the
    # reading is merely POSSIBLE - it requires the architect to decide faster than his bind
    # requires, and on the reading day itself if the packet is prepared then.
    d_possible = reading

    # What the stop permits. 'before X' is exclusive, so the earliest permitted date is X.
    earliest_permitted = stop_end

    out = {
        "_what_this_is": "PREREGISTRATION-135.md Q1, computed. Session 135, 2026-08-25.",
        "inputs": INPUTS,
        "derived": {
            "D_guaranteed": d_guaranteed.isoformat(),
            "D_guaranteed_definition": "latest date D with D + %d days <= the reading; the last "
                                       "date on which condition 3 is reachable BY THE "
                                       "CONSTITUTION'S OWN GUARANTEE." % bind,
            "D_possible": d_possible.isoformat(),
            "D_possible_definition": "latest date D with D <= the reading; reachable ONLY if the "
                                     "architect decides faster than his bind requires.",
            "earliest_date_the_stop_permits_a_packet": earliest_permitted.isoformat(),
            "days_from_today_to_D_guaranteed": (d_guaranteed - today).days,
            "days_from_today_to_the_reading": (reading - today).days,
            "gap_stop_permits_minus_D_guaranteed_days":
                (earliest_permitted - d_guaranteed).days,
            "gap_stop_permits_minus_D_possible_days":
                (earliest_permitted - d_possible).days,
        },
        "findings": [],
    }
    g = out["derived"]

    if earliest_permitted > d_guaranteed:
        out["findings"].append(
            "The earliest date the stop permits a packet (%s) is %d days AFTER the last date on "
            "which the constitution's own bind guarantees a send-or-withhold decision before the "
            "reading (%s). Holding the stop to its written end therefore forecloses the "
            "guaranteed route to condition 3 - and it does so %d days before the stop itself "
            "expires."
            % (earliest_permitted.isoformat(), g["gap_stop_permits_minus_D_guaranteed_days"],
               d_guaranteed.isoformat(), g["gap_stop_permits_minus_D_guaranteed_days"]))
    else:
        out["findings"].append(
            "The stop's end date leaves the guaranteed route to condition 3 open. Q1's "
            "conclusion is REFUTED on its own falsification condition.")

    if earliest_permitted == d_possible:
        out["findings"].append(
            "Under the weaker reading, the stop's earliest permitted date (%s) coincides exactly "
            "with D_possible (%s): zero days of slack. Condition 3 would depend on a packet "
            "reaching `prepared` on the morning of the reading and being sent the same day, by "
            "the architect, while he is doing the reading."
            % (earliest_permitted.isoformat(), d_possible.isoformat()))
    elif earliest_permitted > d_possible:
        out["findings"].append(
            "Under the weaker reading too, the stop's earliest permitted date (%s) is after "
            "D_possible (%s): condition 3 is unreachable from this arc under any reading."
            % (earliest_permitted.isoformat(), d_possible.isoformat()))
    else:
        out["findings"].append(
            "Under the weaker reading the stop leaves %d day(s) of slack."
            % (d_possible - earliest_permitted).days)

    out["findings"].append(
        "Days remaining from today (%s) to D_guaranteed (%s): %d."
        % (today.isoformat(), d_guaranteed.isoformat(), g["days_from_today_to_D_guaranteed"]))

    out["what_this_does_not_establish"] = [
        "That a packet from this arc SHOULD be prepared. Nine gauntlets have said the object is "
        "not fit to send, and a deadline is not an argument that the ninth verdict was wrong "
        "(PREREGISTRATION-135.md section 4, constraint 2).",
        "That the architect will use his full seven days. The bind is a ceiling on his time; "
        "nothing in this record measures how he actually uses it, and this file makes no claim "
        "about a named person's conduct.",
        "That condition 3 belongs to this arc alone. The condition's wording - 'It left the "
        "house' - has an ambiguous antecedent, and other packets stand at `prepared` in the "
        "house's post office. Both are reported in INCREMENT-23.md rather than resolved here.",
    ]

    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=2)
        fh.write("\n")

    for f in out["findings"]:
        print(f)
    print()
    print("wrote " + out_path)
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default="stop-clock-135.json")
    sys.exit(main(ap.parse_args().out))
