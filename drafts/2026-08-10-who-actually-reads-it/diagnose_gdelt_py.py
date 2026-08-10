#!/usr/bin/env python3
"""Diagnostic, so the session does not over-read demonstration-gdelt-py.json.
Counts what the package actually requested and what it did with each request."""
import asyncio, json, logging, re, io
from py_gdelt import GDELTClient
from py_gdelt.filters import EventFilter, DateRange

buf = io.StringIO()
h = logging.StreamHandler(buf); h.setLevel(logging.DEBUG)
logging.getLogger("py_gdelt").addHandler(h)
logging.getLogger("py_gdelt").setLevel(logging.DEBUG)

async def main():
    out = {}
    for label, d in [("outage day", "2022-11-11"), ("control", "2022-11-09")]:
        buf.truncate(0); buf.seek(0)
        async with GDELTClient() as c:
            res = await c.events.query(EventFilter(date_range=DateRange(start=d, end=d)))
        log = buf.getvalue()
        out[label] = {
            "date": d,
            "records": len(res), "complete": res.complete, "total_failed": res.total_failed,
            "log_lines": log.count("\n"),
            "downloading_lines": len(re.findall(r"Downloading:", log)),
            "not_found_lines": len(re.findall(r"File not found \(404\)", log)),
            "distinct_urls": len(set(re.findall(r"https?://\S+", log))),
            "sample_urls": sorted(set(re.findall(r"https?://\S+\.zip", log)))[:3],
            "warning_or_error_lines": [l for l in log.splitlines()
                                       if "error" in l.lower() or "warning" in l.lower()][:5],
        }
        print(json.dumps(out[label], indent=1), flush=True)
    json.dump(out, open("diagnose-gdelt-py.json", "w"), indent=1)

asyncio.run(main())
