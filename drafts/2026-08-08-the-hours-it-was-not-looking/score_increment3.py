#!/usr/bin/env python3
"""score_increment3.py — score increment 3 against PREREGISTRATION-3.md.

Reads the six sweep files, the per-cycle screen ratios, and the API probes, and writes
one scored result file. Every prediction is scored HELD / NOT HELD against the wording
committed before the first request, and the wording is quoted in the output so the score
can be checked without the pre-registration open beside it.

Usage: score_increment3.py <scratch-dir> <out.json>
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timedelta, timezone

FMT = "%Y%m%d%H%M%S"
STEP = timedelta(minutes=15)
WINDOW_START, WINDOW_END = "20221110220000", "20221111183000"
SERIES = [("en", "gkg"), ("en", "export"), ("en", "mentions"),
          ("tr", "gkg"), ("tr", "export"), ("tr", "mentions")]


def load(path):
    rows, header, footer = [], None, None
    if not os.path.exists(path):
        return None, None, None
    for line in open(path, encoding="utf-8"):
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue                      # a truncated last line of a killed run
        k = r.get("k")
        if k == "header":
            header = r
        elif k == "footer":
            footer = r
        else:
            rows.append(r)
    return header, rows, footer


def runs_of(cycles):
    ts = sorted(datetime.strptime(c, FMT).replace(tzinfo=timezone.utc) for c in cycles)
    out, cur = [], []
    for t in ts:
        if cur and t - cur[-1] == STEP:
            cur.append(t)
        else:
            if cur:
                out.append(cur)
            cur = [t]
    if cur:
        out.append(cur)
    return out


def main():
    scratch, out = sys.argv[1], sys.argv[2]
    res = {"series": {}, "predictions": {}}

    per = {}
    for stream, typ in SERIES:
        h, rows, f = load(os.path.join(scratch, f"sweep-{stream}-{typ}.jsonl"))
        if rows is None:
            res["series"][f"{stream}-{typ}"] = {"state": "NOT RUN"}
            continue
        absent = [r["c"] for r in rows if r["k"] == "absent"]
        mism = [r for r in rows if r["k"] == "size-mismatch"]
        unres = [r for r in rows if r["k"] == "unresolved"]
        other = [r for r in rows if r["k"] == "other-status"]
        per[(stream, typ)] = {"absent": absent, "mismatch": mism,
                              "unresolved": unres, "other": other}
        res["series"][f"{stream}-{typ}"] = {
            "state": "COMPLETE" if f else "PARTIAL",
            "listed": (f or h or {}).get("total"),
            "probed": (f or {}).get("done"),
            "absent": len(absent), "size_mismatch": len(mism),
            "unresolved": len(unres), "other_status": len(other),
            "throttled": (f or {}).get("throttled"),
            "elapsed_s": (f or {}).get("elapsed_s"),
            "rate_per_s": (f or {}).get("rate_per_s"),
            "started": (h or {}).get("started"), "finished": (f or {}).get("finished"),
        }

    eng = per.get(("en", "gkg"))
    if eng:
        absent = set(eng["absent"])
        window = {c for c in absent if WINDOW_START <= c <= WINDOW_END}
        outside = sorted(absent - window)

        # ---- P1 -------------------------------------------------------------------
        expect = []
        t = datetime.strptime(WINDOW_START, FMT).replace(tzinfo=timezone.utc)
        end = datetime.strptime(WINDOW_END, FMT).replace(tzinfo=timezone.utc)
        while t <= end:
            expect.append(t.strftime(FMT)); t += STEP
        got = [c for c in expect if c in absent]
        res["predictions"]["P1"] = {
            "text": "the full sweep returns all 83 known cycles as absent on .gkg.csv.zip",
            "expected": len(expect), "absent_of_those": len(got),
            "verdict": "HELD" if len(got) == len(expect) else "NOT HELD"}

        # ---- P2 -------------------------------------------------------------------
        res["predictions"]["P2"] = {
            "text": "outside that window, fewer than 500 listed English gkg cycles are absent",
            "measured": len(outside),
            "verdict": "HELD" if len(outside) < 500 else "NOT HELD"}

        # ---- P3 — the decisive one ------------------------------------------------
        screen = json.load(open(os.path.join(scratch, "screen-en-gkg.json")))["ratio"]
        unflagged = [c for c in outside
                     if screen.get(c) is not None and screen[c] >= 0.20]
        flagged = [c for c in outside if screen.get(c) is not None and screen[c] < 0.20]
        noratio = [c for c in outside if screen.get(c) is None]
        res["predictions"]["P3"] = {
            "text": ("among the absent cycles outside the known window, at least one is "
                     "NOT flagged by the index's own byte-column screen at threshold 0.20"),
            "outside_window_absent": len(outside),
            "flagged_by_screen": len(flagged),
            "not_flagged_by_screen": len(unflagged),
            "no_ratio": len(noratio),
            "unflagged_examples": [{"cycle": c, "ratio": screen[c]} for c in unflagged[:15]],
            "verdict": "HELD" if unflagged else "NOT HELD"}

        # ---- P5 -------------------------------------------------------------------
        rr = runs_of(absent)
        long_runs = [r for r in rr if len(r) >= 4]
        res["predictions"]["P5"] = {
            "text": "the absent set forms at most 20 contiguous runs of length >= 4 cycles",
            "runs_total": len(rr), "runs_ge_4": len(long_runs),
            "runs": [{"length": len(r),
                      "first": r[0].strftime("%Y-%m-%dT%H:%M:%SZ"),
                      "last": r[-1].strftime("%Y-%m-%dT%H:%M:%SZ")}
                     for r in sorted(rr, key=len, reverse=True)[:25]],
            "verdict": "HELD" if len(long_runs) <= 20 else "NOT HELD"}

        # ---- P6 / P7 --------------------------------------------------------------
        mism = eng["mismatch"]
        big = [m for m in mism if m.get("cl") is not None and m["d"] > 0
               and abs(m["cl"] - m["d"]) / m["d"] > 0.01]
        small_decl = [m for m in big if m["cl"] > m["d"]]
        large_decl = [m for m in big if m["cl"] < m["d"]]
        res["predictions"]["P6"] = {
            "text": ("the number of served English gkg cycles whose Content-Length differs "
                     "from the declared size by more than 1 % is between 1 and 2,000"),
            "any_mismatch": len(mism), "over_1pct": len(big),
            "examples": [{"cycle": m["c"], "declared": m["d"], "served": m["cl"]}
                         for m in sorted(big, key=lambda m: -abs(m["cl"] - m["d"]))[:15]],
            "verdict": "HELD" if 1 <= len(big) <= 2000 else "NOT HELD"}
        res["predictions"]["P7"] = {
            "text": "more disagreements are declared-too-small than declared-too-large",
            "declared_too_small": len(small_decl), "declared_too_large": len(large_decl),
            "verdict": "HELD" if len(small_decl) > len(large_decl) else "NOT HELD"}

        res["window"] = {"start": WINDOW_START, "end": WINDOW_END,
                         "cycles_expected": len(expect), "cycles_absent": len(got)}
        res["outside_window_absent_cycles"] = outside

    # ---- P4: the free second copy ------------------------------------------------
    api = {}
    for name in ("news", "world", "said", "government", "trump"):
        p = os.path.join(scratch, f"api-window-{name}.json")
        if os.path.exists(p):
            d = json.load(open(p))
            api[name] = {"expected": d.get("expected"), "returned": d.get("returned"),
                         "missing_count": d.get("missing_count"),
                         "resolution": d.get("date_resolution"),
                         "first_missing": (d.get("missing") or [None])[0],
                         "last_missing": (d.get("missing") or [None])[-1],
                         "missing": d.get("missing")}
    res["api_window"] = api
    if api and eng:
        ref = api.get("world") or list(api.values())[0]
        miss = set(ref.get("missing") or [])
        absent = set(eng["absent"])
        res["predictions"]["P4"] = {
            "text": ("a free, unauthenticated second copy published by the same organisation "
                     "shows the November 2022 window as a gap at cycle resolution"),
            "api_missing_buckets": len(miss),
            "api_missing_but_file_served": sorted(miss - absent),
            "file_absent_but_api_returned": sorted(absent & set()) or
                                            sorted(c for c in absent
                                                   if c in (ref.get("returned_set") or [])),
            "verdict": "HELD" if miss else "NOT HELD"}

    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps({k: v.get("verdict") for k, v in res["predictions"].items()}, indent=1))
    print(json.dumps(res["series"], indent=1))


if __name__ == "__main__":
    main()
