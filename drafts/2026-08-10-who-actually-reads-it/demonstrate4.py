#!/usr/bin/env python3
"""Second consumer, actively maintained (last release 2026-02-18), same day,
same measured absences. Unmodified, installed from the registry."""
import warnings, json
from gdelt_client import GdeltClient

out = []
for label, date in [("day with 75 of 96 cycles listed-but-absent", "2022 11 11"),
                    ("control day, all served", "2022 11 09")]:
    c = GdeltClient()
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        exc = None
        try:
            df = c.search(date=date, table="events", coverage=True)
        except Exception as e:
            df, exc = None, f"{type(e).__name__}: {e}"
        msgs = [str(x.message) for x in w]
    row = {"label": label, "date": date, "exception_raised_to_caller": exc,
           "rows_returned": None if df is None else int(len(df)),
           "warnings_seen_by_caller": len(msgs), "sample": msgs[:2]}
    if df is not None:
        col = [x for x in df.columns if str(x).upper() == "DATEADDED"]
        if col:
            row["distinct_cycles"] = int(df[col[0]].nunique())
        row["columns_marking_incompleteness"] = [x for x in df.columns
            if any(t in str(x).lower() for t in ("missing", "coverage", "absent", "complete"))]
    out.append(row); print(json.dumps(row, indent=1), flush=True)
json.dump(out, open("demonstration-gdelt-client.json", "w"), indent=1)
