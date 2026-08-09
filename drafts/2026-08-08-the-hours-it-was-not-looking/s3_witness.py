#!/usr/bin/env python3
"""s3_witness.py — condition C-VIII: a second witness for every pre-2019-05 row.

The adversary found a genuine independent host holding *unzipped* copies of the same
files, frozen at around 2019-04. Its condition: a register row that says "absent" where a
public mirror holds the file is wrong, so every row before the snapshot's cutoff must be
checked against it.

For each cycle passed in, one HEAD against the snapshot host, plus (with --controls) the
neighbouring cycle as a control, so a 404 from the snapshot means "this cycle is missing
there too" and not "the snapshot has nothing around here".

Usage: s3_witness.py <cycles.json> <out.json>
       (cycles.json: {"absent": ["YYYYMMDDHHMMSS", ...]})
"""

from __future__ import annotations

import http.client
import json
import ssl
import sys
import time
from datetime import datetime, timedelta, timezone

HOST = "gdelt-open-data.s3.amazonaws.com"
CUTOFF = datetime(2019, 5, 1, tzinfo=timezone.utc)
FMT = "%Y%m%d%H%M%S"


def head(conn, path, tries=3):
    for a in range(tries):
        try:
            conn.request("HEAD", path)
            r = conn.getresponse()
            r.read()
            cl = r.getheader("Content-Length")
            return r.status, (int(cl) if cl else None), None
        except Exception as e:
            err = type(e).__name__ + ": " + str(e)[:100]
            time.sleep(0.5 * (a + 1))
            try:
                conn.close()
            except Exception:
                pass
            conn.__init__(HOST, timeout=45, context=ssl.create_default_context())
    return None, None, err


def main():
    cycles = json.load(open(sys.argv[1]))["absent"]
    out = sys.argv[2]
    ctx = ssl.create_default_context()
    conn = http.client.HTTPSConnection(HOST, timeout=45, context=ctx)
    rows = []
    for c in cycles:
        t = datetime.strptime(c, FMT).replace(tzinfo=timezone.utc)
        if t >= CUTOFF:
            rows.append({"cycle": c, "in_snapshot_range": False})
            continue
        st, cl, err = head(conn, f"/v2/gkg/{c}.gkg.csv")
        ctrl = (t - timedelta(minutes=15)).strftime(FMT)
        cst, ccl, cerr = head(conn, f"/v2/gkg/{ctrl}.gkg.csv")
        rows.append({"cycle": c, "in_snapshot_range": True, "status": st,
                     "content_length": cl, "err": err,
                     "control_cycle": ctrl, "control_status": cst,
                     "control_content_length": ccl, "control_err": cerr})
        print(f"  {c} snapshot={st} control({ctrl})={cst}", flush=True)
    inrange = [r for r in rows if r["in_snapshot_range"]]
    summary = {"checked": len(inrange),
               "absent_in_snapshot_too": sum(1 for r in inrange if r.get("status") == 404),
               "present_in_snapshot": sum(1 for r in inrange if r.get("status") == 200),
               "unresolved": sum(1 for r in inrange if r.get("status") is None),
               "controls_present": sum(1 for r in inrange if r.get("control_status") == 200),
               "out_of_snapshot_range": len(rows) - len(inrange)}
    json.dump({"host": HOST, "cutoff": "2019-05-01", "summary": summary, "rows": rows},
              open(out, "w"), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
