#!/usr/bin/env python3
"""C3, executed rather than inferred.

Runs the most-downloaded Python client for the object, unmodified and installed
from the registry, over one full day whose absences this practice measured and
dated (2026-08-09, availability-register-v1.0.json): 2022-11-11, where 75 of the
96 quarter-hours are listed in the object's own master file list with a byte size
and an MD5 and are not served.

Control: 2022-11-09, where every cycle of the same day is served.

Nothing here is patched. The only instrumentation is warnings capture, so the
session can report exactly what a caller who does not read warnings receives.
"""
import warnings, json, sys, datetime
import gdelt

gd = gdelt.gdelt(version=2)

def run(label, datestr, table):
    caught = []
    t0 = datetime.datetime.now(datetime.UTC)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        exc = None
        try:
            res = gd.Search([datestr], table=table, coverage=True)
        except Exception as e:
            res = None
            exc = f"{type(e).__name__}: {e}"
        caught = [str(x.message) for x in w]
    dt = (datetime.datetime.now(datetime.UTC) - t0).total_seconds()
    out = {
        "label": label, "date": datestr, "table": table,
        "exception_raised_to_caller": exc,
        "rows_returned": (None if res is None else int(len(res))),
        "distinct_cycles_in_result": None,
        "warnings_count": len(caught),
        "warnings_sample": caught[:4],
        "seconds": round(dt, 1),
    }
    if res is not None and "DATEADDED" in getattr(res, "columns", []):
        out["distinct_cycles_in_result"] = int(res["DATEADDED"].nunique())
    print(json.dumps(out, indent=1), flush=True)
    return out

results = []
results.append(run("day with 75 of 96 cycles listed-but-absent", "2022 Nov 11", "events"))
results.append(run("control day, all 96 cycles served", "2022 Nov 9", "events"))
json.dump(results, open("demonstration-gdeltpyr.json", "w"), indent=1)
