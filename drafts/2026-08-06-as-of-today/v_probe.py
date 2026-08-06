#!/usr/bin/env python3
"""v_probe.py — POST-HOC, LABELLED, SCORES NOTHING.

The pre-registered V pattern set (M-3) was written on the EC surface and, per the
pre-registration, is not extended inside a run. Hand-checking after the run found it blind to
NIST's own convention: NIST prints "Created ... / Updated August 4, 2026" — a label the pattern
set does not carry and a date format ("Month D, YYYY") that its date regex does not accept.

This script measures HOW blind, so that every V figure can be reported as a BOUND rather than a
number. It re-fetches the scored (arm B) pages of every authority, including EC's locked corpus,
and applies a widened pattern set. It does NOT modify signals.json, signals-2.json or results-2.json,
and no prediction is rescored on its output.

Writes v-probe.json.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
import time

from collect_signals import get, visible_text

MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
DATE = (rf"(?:\d{{1,2}}\s+(?:{MONTHS})\s+\d{{4}}"
        rf"|(?:{MONTHS})\s+\d{{1,2}},?\s+\d{{4}}"
        rf"|\d{{4}}-\d{{2}}-\d{{2}}"
        rf"|\d{{2}}/\d{{2}}/\d{{4}})")
LABEL = r"(?:last\s+update[d]?|updated|last\s+modified|modified|publication\s+date|published|created)"
WIDE = re.compile(rf"{LABEL}\s*[:\-–]?\s*({DATE})", re.I)


def probe(text: str):
    m = WIDE.search(text)
    return m.group(1) if m else None


def main() -> int:
    sig2 = json.load(open("signals-2.json"))
    ec = json.load(open("signals.json"))
    chrome = json.load(open("chrome-2.json"))["authorities"]
    ec_chrome = {u.rstrip("/") for u in chrome["EC"]["chrome"]} | {
        "https://digital-strategy.ec.europa.eu"}

    targets: dict[str, list[dict]] = {}
    for key, a in sig2["authorities"].items():
        targets[key] = [{"url": r["url"], "prereg_v": r.get("v")}
                        for r in a["rows"] if r["arm_b"] and r["fetch"] == "OK"]
    targets["EC"] = [{"url": r["url"], "prereg_v": r.get("v")}
                     for r in ec["rows"] if r.get("fetch") == "OK"
                     and r["url"].rstrip("/") not in ec_chrome]

    out = {
        "control": "post-hoc V probe — labelled, scores nothing",
        "probed_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "note": ("EC pages are re-fetched now, hours after their locked 08:26:37Z collection; "
                 "the probe measures the extractor, not EC's state at that time"),
        "authorities": {},
    }
    for key, rows in targets.items():
        found_by_probe = 0
        missed_by_prereg = 0
        detail = []
        for r in rows:
            resp = get(r["url"])
            time.sleep(0.4)
            if not resp.get("ok") or resp.get("status") != 200:
                detail.append({**r, "probe_v": None, "fetch": "NETFAIL"})
                continue
            v = probe(visible_text(resp["body"]))
            if v:
                found_by_probe += 1
                if not r["prereg_v"]:
                    missed_by_prereg += 1
            detail.append({**r, "probe_v": v, "fetch": "OK"})
        n = len(rows)
        prereg_n = sum(1 for r in rows if r["prereg_v"])
        out["authorities"][key] = {
            "n_arm_b_ok": n,
            "prereg_v_n": prereg_n,
            "prereg_v_share": round(100.0 * prereg_n / n, 1) if n else None,
            "probe_v_n": found_by_probe,
            "probe_v_share": round(100.0 * found_by_probe / n, 1) if n else None,
            "missed_by_prereg_pattern": missed_by_prereg,
            "rows": detail,
        }
        print(f"{key}: pre-registered V {prereg_n}/{n}, wider probe {found_by_probe}/{n}, "
              f"missed by the locked pattern {missed_by_prereg}")

    with open("v-probe.json", "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
