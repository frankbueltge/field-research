#!/usr/bin/env python3
"""Correcting this session's own first harness.

demonstrate.py wrapped the call in warnings.catch_warnings(record=True). The package
does its downloading in forked worker processes, which INHERIT the parent's warning
recorder — so the children recorded into their own copies and the parent saw nothing.
The reported "0 warnings" was an artifact of our harness, not a property of the package.

This run uses no warnings machinery at all: default interpreter settings, stderr to a
file, stdout captured. It measures what a caller actually gets.
"""
import json, datetime, gdelt
gd = gdelt.gdelt(version=2)
t0 = datetime.datetime.now(datetime.UTC)
res = gd.Search(["2022 Nov 11"], table="events", coverage=True)
out = {
  "harness": "no warnings filter, default interpreter settings",
  "rows_returned": int(len(res)),
  "distinct_cycles": int(res["DATEADDED"].nunique()),
  "exception_raised": None,
  "returned_type": type(res).__name__,
  "columns_mentioning_missing_or_coverage": [c for c in res.columns
        if any(t in str(c).lower() for t in ("missing", "coverage", "absent", "complete"))],
  "seconds": round((datetime.datetime.now(datetime.UTC) - t0).total_seconds(), 1),
}
json.dump(out, open("demonstration-default-harness.json", "w"), indent=1)
print(json.dumps(out, indent=1))
