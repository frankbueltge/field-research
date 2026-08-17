#!/usr/bin/env python3
"""panel_date_125 - how tightly the record can date the panel the age table rests on.

Session 125. The gauntlet's blocking objection: the citation panel's own construction date is
undisclosed anywhere in the 30-file bundle, leaving a survivorship confound open. This asks a
narrower question than "what is the date" - it asks what the record can BOUND, and computes it,
because a figure this practice types by hand is a figure it has failed on six times.

Lower bound: the panel cannot have been collected before the newest citation in it was created
  (corpus-merged.json meta.max_created).
Upper bound: the panel must have existed before the first ledger run measured it
  (INCREMENT-1: run 1 at 2026-08-11T04:05:44Z, taken here from the run file itself).
"""
import calendar, glob, json, time

def ts(s):
    s = s.replace("+00:00", "Z")
    return calendar.timegm(time.strptime(s, "%Y-%m-%dT%H:%M:%SZ"))

merged = json.load(open("corpus-merged.json"))["meta"]
lower = merged["max_created"]

# The earliest run file in the ledger is the first measurement taken over this panel.
runs = []
for p in sorted(glob.glob("ledger/run-*.json")):
    if p.endswith(".partial"):
        continue
    try:
        d = json.load(open(p))
    except (OSError, ValueError):
        continue
    if isinstance(d.get("run_utc_start"), str):
        runs.append((d["run_utc_start"], p))
runs.sort()
upper, upper_file = runs[0]

# What metadata the corpus files actually carry, counted rather than asserted.
fields, n_files, with_time = set(), 0, 0
for p in sorted(glob.glob("corpus-*.json")):
    m = json.load(open(p)).get("meta", {})
    n_files += 1
    fields |= set(m.keys())
    if any(isinstance(v, str) and "T" in v and v[:2] == "20" for v in m.values()):
        with_time += 1

out = {
 "objection": "the citation panel's construction date is undisclosed in the bundle",
 "corpus_files_examined": n_files,
 "corpus_files_carrying_any_timestamp": with_time,
 "distinct_meta_fields_across_corpus_files": sorted(fields),
 "lower_bound_utc": lower,
 "lower_bound_basis": "corpus-merged.json meta.max_created - the newest citation in the pool; "
                      "the pull cannot precede it",
 "upper_bound_utc": upper,
 "upper_bound_basis": "earliest completed ledger run over the panel (" + upper_file + ")",
 "bracket_days": round((ts(upper) - ts(lower)) / 86400.0, 4),
 "collection_timestamp_recorded_anywhere": False,
 "what_this_does_not_do": ("It does not date the panel. It states how wide the undated window is, "
                           "using only facts already in the repository. Closing the objection needs "
                           "either a recorded collection time or the bracket stated as a limit."),
}
json.dump(out, open("panel-date-125.json", "w"), indent=1)
print(json.dumps(out, indent=1))
