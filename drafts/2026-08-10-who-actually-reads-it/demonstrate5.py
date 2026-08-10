#!/usr/bin/env python3
"""Third consumer, executed: the package that reads the object's master file list and does
not verify the checksums beside it. Same day, same measured absences.

Run because reading the source was not enough. Its models carry a result container with
explicit partial-failure tracking (FetchResult.data / .failed / .complete / .partial /
.total_failed, py_gdelt/models/common.py), which this session's first classification missed.
Only executing it settles what a caller actually receives.

Note recorded rather than worked around: the documented synchronous entry point
(client.events.query_sync) raised RuntimeError("Event loop is closed") on both windows in
this environment, so the async entry point is used instead. Both are the package's own
public API.
"""
import asyncio, json
from py_gdelt import GDELTClient
from py_gdelt.filters import EventFilter, DateRange

async def one(label, start, end):
    exc = None; res = None
    try:
        async with GDELTClient() as c:
            res = await c.events.query(EventFilter(date_range=DateRange(start=start, end=end)))
    except Exception as e:
        exc = f"{type(e).__name__}: {e}"
    row = {"label": label, "window": [start, end], "exception_raised_to_caller": exc,
           "returned_type": type(res).__name__ if res is not None else None}
    if res is not None:
        row["len_of_result"] = len(res)
        for attr in ("complete", "partial", "total_failed"):
            if hasattr(res, attr):
                row[attr] = getattr(res, attr)
        if hasattr(res, "failed"):
            row["failed_sample"] = [str(x)[:150] for x in list(res.failed)[:2]]
    print(json.dumps(row, indent=1)[:1400], flush=True)
    return row

async def main():
    out = [await one("day with 75 of 96 cycles listed-but-absent", "2022-11-11", "2022-11-11"),
           await one("control day, all served", "2022-11-09", "2022-11-09")]
    json.dump(out, open("demonstration-gdelt-py.json", "w"), indent=1)

asyncio.run(main())
