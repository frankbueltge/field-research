#!/usr/bin/env python3
"""Two follow-ups to demonstrate.py, both executing the same package's own code:

(a) which cycles came back — cross-checked against this practice's own register;
(b) where the package's warning goes: the same worker called IN-PROCESS emits a
    Python warning; called through the package's own process pool (as every real
    query does) the caller sees nothing.
"""
import warnings, json, io, contextlib
import gdelt
from gdelt.parallel import _mp_worker

gd = gdelt.gdelt(version=2)

# (a) which cycles
res = gd.Search(["2022 Nov 11"], table="events", coverage=True)
got = sorted(str(x) for x in res["DATEADDED"].unique())
reg = json.load(open("/home/user/field-research/drafts/2026-08-08-the-hours-it-was-not-looking/availability-register-v1.0.json"))
absent = {r["cycle"] for r in reg["rows"]
          if r["cycle"].startswith("20221111")
          and r["series"].get("English/export", {}).get("verdict") == "absent"}
grid = [f"20221111{h:02d}{m:02d}00" for h in range(24) for m in (0, 15, 30, 45)]
expected_served = [c for c in grid if c not in absent]

# (b) the warning path, in-process vs through the pool
url = "http://data.gdeltproject.org/gdeltv2/20221111000000.export.CSV.zip"   # a listed, absent file
buf = io.StringIO()
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    with contextlib.redirect_stderr(buf):
        r = _mp_worker(url, table="events")
inproc = {"returned": type(r).__name__, "warnings_in_process": [str(x.message) for x in w]}

out = {
  "cycles_returned": len(got),
  "cycles_expected_served_per_register": len(expected_served),
  "exact_match_with_register": got == expected_served,
  "first_returned": got[:3], "last_returned": got[-3:],
  "in_process_worker_on_an_absent_listed_file": inproc,
}
json.dump(out, open("demonstration-crosscheck.json", "w"), indent=1)
print(json.dumps(out, indent=1))
