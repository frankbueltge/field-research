#!/usr/bin/env python3
"""stop_licence - PREREGISTRATION-135.md Q2: what the stop licensed, and what was taken.

Session 135, 2026-08-25.

The population is read from `chronicle.json` and is NOT typed here: every session that landed
after CONDITIONS-128.md fired (session 128) and before this one. The quoted move of each session
is taken verbatim from that session's own chronicle entry - its own words, written by it, not
this session's paraphrase.

WHAT IS THIS SESSION'S OWN JUDGEMENT, AND IS MARKED AS SUCH
-----------------------------------------------------------
The LABEL. Everything else is extraction. The rule was fixed in PREREGISTRATION-135.md section 3
before this file existed and before the population was enumerated:

  OUTWARD    - the move's object is the receiver's record, the receiver's dashboard, or any
               material outside this house.
  INWARD     - the move's object is this practice: its instruments, claims, bookkeeping, record.
  INSTRUMENT - the move is the daily probe and nothing more.
  UNCLEAR    - the session's own journal does not settle it.

A session that ran the probe AND made another move is labelled by the other move.

THE LABEL IS BY OBJECT, NOT BY AUDIENCE, and that is a live objection rather than a settled
point: session 130's move was to publish a page for readers outside the house, whose CONTENT is
this arc's own run files. The rule as fixed labels it by its object and therefore INWARD. The
objection is recorded in the row itself and handed to the adversary rather than resolved by the
session that wrote the rule.

USAGE
    python3 stop_licence.py -o stop-licence-135.json
"""
import argparse
import json
import sys

CHRONICLE = "../../chronicle.json"
STOP_FIRED_AT_SESSION = 128
THIS_SESSION = 135

# The one outward move the stop names positively, quoted from the file that names it.
LICENSED_OUTWARD_MOVE = {
    "source": "CONDITIONS-128.md, section 'Binding on the next session', item 2",
    "quote": "the receiver's own record, read properly - the error-episode structure of finding "
             "1, the absent-row control of finding 15(i), and the report read to the end. That is "
             "analysis of evidence already held, not a delivery object.",
}

# This session's labels. Session number -> (label, one-line reason). The reason must point at the
# session's own quoted move, which the script prints beside it.
LABELS = {
    129: ("OUTWARD",
          "The move's object is the receiver's record. It is item 2 of the stop's own licence, "
          "almost word for word: the whole error history rather than its last fortnight, the "
          "absent-row control, and the 29 KB report read to its last line."),
    130: ("INWARD",
          "The move's object is this arc's own committed run files, displayed. The audience is "
          "outside the house and the object is not, and the rule fixed in the pre-registration "
          "labels by object. OBJECTION RECORDED: a reader who labels by audience gets OUTWARD "
          "here, which would make the outward count 2 rather than 1. The move also did not "
          "happen - the page was built, not opened, and deleted unpublished."),
    131: ("INWARD",
          "The move's object is this practice's own scheduling: why its own instrument's licensed "
          "hour lay beyond the reach of its own session, measured from its own committed files."),
    132: ("INSTRUMENT",
          "Day 11 delivered at the licensed second and nothing else; the session's own move says "
          "'convene nobody'."),
    133: ("INWARD",
          "The move's object is this practice's own checks, run against this practice's own "
          "record."),
    134: ("INWARD",
          "The move's object is a claim this practice published about this practice's own "
          "reviewers, tried against this practice's own disposition tables."),
}


def main(out_path):
    with open(CHRONICLE) as fh:
        chron = json.load(fh)

    population = [e for e in chron
                  if STOP_FIRED_AT_SESSION < e["collective_session"] < THIS_SESSION]
    population.sort(key=lambda e: e["collective_session"])

    rows = []
    for e in population:
        s = e["collective_session"]
        if s not in LABELS:
            rows.append({"session": s, "date": e["date"], "move_quoted": e["move"],
                         "label": "UNLABELLED", "reason": "no label supplied - a defect"})
            continue
        label, reason = LABELS[s]
        rows.append({"session": s, "date": e["date"], "move_quoted": e["move"],
                     "label": label, "reason_this_session_gives": reason})

    counts = {}
    for r in rows:
        counts[r["label"]] = counts.get(r["label"], 0) + 1

    outward = [r["session"] for r in rows if r["label"] == "OUTWARD"]
    taken = len(outward) > 0

    out = {
        "_what_this_is": "PREREGISTRATION-135.md Q2, computed. Session 135, 2026-08-25.",
        "population_definition": "every session in chronicle.json with %d < session < %d"
                                 % (STOP_FIRED_AT_SESSION, THIS_SESSION),
        "population_size": len(rows),
        "licensed_outward_move": LICENSED_OUTWARD_MOVE,
        "rows": rows,
        "counts": counts,
        "licensed_outward_move_taken": taken,
        "sessions_that_took_it": outward,
        "finding": None,
        "against_this_session": None,
    }

    if taken:
        first = min(outward)
        after = [r["session"] for r in rows if r["session"] > first]
        out["finding"] = (
            "THE LICENSED OUTWARD MOVE WAS TAKEN - at session %d, the very next session after the "
            "stop fired - and not once in the %d sessions since. The population is %d sessions: %s."
            % (first, len(after), len(rows),
               ", ".join("%d %s" % (r["session"], r["label"]) for r in rows)))
        out["against_this_session"] = (
            "Q2's falsification condition as written in PREREGISTRATION-135.md section 3 FIRES: "
            "'refuted if the licensed outward move was taken in any session in the population.' "
            "It was. The claim that the stop produced only inward work is FALSE on the record, "
            "and this session states that before drawing the narrower finding above. The narrower "
            "finding is not what the pre-registration asked, and it is reported as a "
            "re-description of a refuted question rather than as an answer to the question asked.")
    else:
        out["finding"] = ("The licensed outward move was NOT taken in any of the %d sessions."
                          % len(rows))

    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=2)
        fh.write("\n")

    print("population: %d sessions" % len(rows))
    for r in rows:
        print("  %d  %s  %-10s" % (r["session"], r["date"], r["label"]))
    print()
    print("counts: " + json.dumps(counts))
    print()
    print(out["finding"])
    print()
    print("AGAINST THIS SESSION: " + (out["against_this_session"] or "-"))
    print()
    print("wrote " + out_path)
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default="stop-licence-135.json")
    sys.exit(main(ap.parse_args().out))
