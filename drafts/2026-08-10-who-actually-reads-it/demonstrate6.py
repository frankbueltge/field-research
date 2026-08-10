#!/usr/bin/env python3
"""Fourth consumer, executed: the one whose fetch path performs no status check at all.
Same day, same measured absences. Run in an empty working directory; the package writes
its downloads under a relative path of its own choosing.
"""
import os, json, datetime, zipfile
os.chdir("pygdelt-run")
from pygdelt.gdeltv2 import Events

ev = Events()
ev._download(datetime.datetime(2022, 11, 11), hide_progress=True)

root = None
for dirpath, _, files in os.walk("."):
    if any(f.endswith(".zip") for f in files):
        root = dirpath; break
zips = sorted(f for f in os.listdir(root) if f.endswith(".zip")) if root else []
rows = []
for f in zips:
    p = os.path.join(root, f)
    size = os.path.getsize(p)
    try:
        with zipfile.ZipFile(p) as z:
            ok, note = True, f"{len(z.namelist())} member(s)"
    except Exception as e:
        ok, note = False, f"{type(e).__name__}: {e}"
    rows.append({"file": f, "bytes": size, "is_a_zip": ok, "note": note})

out = {
  "day": "2022-11-11", "files_written": len(rows),
  "written_but_not_zip": sum(1 for r in rows if not r["is_a_zip"]),
  "written_and_zip": sum(1 for r in rows if r["is_a_zip"]),
  "exception_raised_to_caller": None,
  "sample_bad": [r for r in rows if not r["is_a_zip"]][:2],
  "sample_good": [r for r in rows if r["is_a_zip"]][:2],
}
json.dump(out, open("../demonstration-pygdelt.json", "w"), indent=1)
print(json.dumps(out, indent=1))
