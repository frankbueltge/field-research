#!/usr/bin/env python3
"""The manifest every run from day 2 onward must use.

Written for the sessions that come after this one. Session 111 grew the corpus on the last
evening before the pre-registered window opened; if a later session runs `ledger.py` against
`manifest-run2.json` out of habit, the identifiers added tonight carry no exposure and the
expansion is silently wasted. This file produces the successor manifest so that cannot happen
by accident.

It is the union of:
  * `manifest-run2.json`  — arms A, B and B-truncated, exactly as session 110 ran them
  * the units actually baselined tonight — arms A-new and A2

**B-truncated is kept.** It is not videos; it is the harvest artefact session 110 measured
deliberately, and dropping it now would remove the control that keeps the artefact's size an
observed quantity rather than a footnote.

Identifiers collected tonight but NOT baselined before 00:00Z are deliberately excluded: they
carry a different exposure window and folding them in silently would corrupt the diff. They
remain in the collection files and a later session may open a second, separately dated arm
with them.
"""
import json
import sys
import time


def main(*baseline_runs):
    out = "manifest-day2-onward.json"
    runs = [r for r in baseline_runs if not r.startswith("out=")] or \
           ["expansion-111/baseline-run.json"]
    base = json.load(open("manifest-run2.json"))
    units = {u["vid"]: u for u in base["units"]}
    arms = dict(base["arms"])

    added = 0
    loaded = []
    for path in runs:
        try:
            run = json.load(open(path))
        except FileNotFoundError:
            print(f"NO BASELINE RUN at {path} — skipped", file=sys.stderr)
            continue
        loaded.append({"run": path, "run_id": run.get("run_id"),
                       "run_utc_start": run.get("run_utc_start"),
                       "observations": len(run["observations"])})
        for o in run["observations"]:
            v = str(o["vid"])
            if v not in units:
                units[v] = {"vid": v, "handle": o["handle"], "arm": o["arm"]}
                added += 1
        for k, v in run.get("arms", {}).items():
            arms.setdefault(k, v)
    if not loaded:
        print("NO BASELINE RUN loaded — merged manifest not written", file=sys.stderr)
        return 1
    run = {"run_id": "; ".join(str(l["run_id"]) for l in loaded),
           "run_utc_start": "; ".join(str(l["run_utc_start"]) for l in loaded)}
    baseline_run = "; ".join(l["run"] for l in loaded)

    man = {
        "run_id": "TEMPLATE — the running session sets this",
        "supersedes": "manifest-run2.json",
        "written_by": "session 111, 2026-08-11",
        "why": ("The corpus grew on the last evening before the pre-registered window opened. "
                "Every run from 2026-08-12 onward must use this manifest; running the old one "
                "would silently drop the identifiers added tonight."),
        "baselined_from": {"run": baseline_run, "run_id": run.get("run_id"),
                           "run_utc_start": run.get("run_utc_start")},
        "added_over_run2": added,
        "n_units": len(units),
        "arms": arms,
        "units": sorted(units.values(), key=lambda u: (u["arm"], u["vid"])),
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    json.dump(man, open(out, "w"), indent=1)
    by_arm = {}
    for u in man["units"]:
        by_arm[u["arm"]] = by_arm.get(u["arm"], 0) + 1
    print(json.dumps({"out": out, "n_units": len(units), "added_over_run2": added,
                      "by_arm": by_arm}))
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
