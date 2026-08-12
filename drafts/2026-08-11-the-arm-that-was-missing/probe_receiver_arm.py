#!/usr/bin/env python3
"""Arm R — the eleven identifiers the receiver's own dark dashboard watches.

Registered in `PREREGISTRATION-112-ADDENDUM.md` before it ran. **Arm R is not part of the
window's population**: not in `manifest-day2-onward.json`, not in the §5a count, not in any fit.

The identifiers are transcribed from session 108's derivation of the receiver's public page
(`drafts/2026-08-10-one-receiver-to-the-floor/dashboard-derived-raw.txt`, fetched 2026-08-10,
HTTP 200), together with that page's own per-video totals across its 279-row series, so each row
carries what the receiver's instrument last recorded beside what the credential-free route returns
today.

**The handle is a placeholder and that is not a shortcut.** Session 109's Interlocutor established
live, and this practice reproduced it before accepting it (`REFUTATION-REPRODUCED.md`), that the
endpoint ignores the `@handle` segment of the URL entirely and resolves on the identifier alone.
Using a fixed placeholder therefore changes nothing about what is measured and makes the absence of
per-video handle data explicit rather than invented.

The probe itself is `ledger.py`'s, imported and not re-implemented, so arm R is measured by the same
instrument as the corpus.
"""
import importlib.util
import json
import sys
import time

spec = importlib.util.spec_from_file_location("ledger", "ledger.py")
ledger = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ledger)

# vid: (observations, Available days, Error days, NotAvailable days) across the receiver's
# 279-row series, 2025-04-09 .. 2026-01-14, as derived at session 108.
RECEIVER_SERIES = {
    "7366758818765638917": (279, 0, 16, 263),
    "7368154048836406544": (279, 0, 18, 261),
    "7074367286571814190": (279, 0, 17, 262),
    "7117394257064840490": (279, 0, 18, 261),
    "7134492331117595950": (279, 0, 15, 264),
    "7164125023886691626": (279, 0, 18, 261),
    "7376726215178128673": (279, 0, 15, 264),
    "7332960275127110954": (279, 213, 20, 46),
    "7347581705299053826": (279, 0, 16, 263),
    "7376437810644946222": (279, 0, 14, 265),
    "7361448925972155679": (238, 0, 14, 224),
}
PLACEHOLDER_HANDLE = "tiktok"     # ignored by the endpoint; see the module docstring


def main(out_path):
    van = ledger.vantage()                       # before the first measurement request
    print(json.dumps({"vantage": van}), file=sys.stderr)
    t0 = time.time()
    obs = []
    for vid, (n, avail, err, notavail) in RECEIVER_SERIES.items():
        rec = {"vid": vid, "handle": PLACEHOLDER_HANDLE, "arm": "R"}
        rec.update(ledger.probe_one(vid, PLACEHOLDER_HANDLE))
        rec["state"] = ledger.classify(rec)
        rec["created_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                           time.gmtime(int(vid) >> 32)) if len(vid) == 19 else None
        rec["receiver_series"] = {"observations": n, "api_available_days": avail,
                                  "api_error_days": err, "api_not_available_days": notavail}
        obs.append(rec)
        time.sleep(ledger.DELAY)

    counts = {}
    for r in obs:
        counts[r["state"]] = counts.get(r["state"], 0) + 1
    out = {"schema": ledger.SCHEMA,
           "run_id": "arm-R-2026-08-12",
           "arm": "R — the eleven identifiers the receiver's dashboard watches",
           "not_part_of_window_population": True,
           "identifier_source": ("drafts/2026-08-10-one-receiver-to-the-floor/"
                                 "dashboard-derived-raw.txt, derived from "
                                 "https://playground.tiktok-audit.com/api-na/ fetched 2026-08-10"),
           "receiver_series_span": "2025-04-09 .. 2026-01-14, 279 rows, last generated 2026-01-14",
           "run_utc_start": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)),
           "run_utc_end": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "seconds": round(time.time() - t0, 1),
           "vantage": van,
           "probe": {"endpoint": ledger.ENDPOINT, "user_agent": ledger.UA,
                     "delay_s": ledger.DELAY, "timeout_s": ledger.TIMEOUT,
                     "unchanged_since": "session 109 census (census.py), 2026-08-11T04:05:44Z"},
           "counts": counts,
           "observations": obs}
    json.dump(out, open(out_path, "w"), indent=1)
    print(json.dumps({"counts": counts, "seconds": out["seconds"]}))
    for r in obs:
        print(f"  {r['vid']}  created {r['created_utc']}  http={r.get('http')}  "
              f"{r['state']:<16} receiver: {r['receiver_series']['api_available_days']}/"
              f"{r['receiver_series']['observations']} days available through the interface")


if __name__ == "__main__":
    main(sys.argv[1])
