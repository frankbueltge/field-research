#!/usr/bin/env python3
"""Merge the coded correction entries and derive every figure the page shows.

Inputs (produced by the coding pass, committed beside the artifact):
  data/corrections.csv   one row per coded correction entry
  data/shipped_units.csv the denominator: every shipped unit at the pre-registration commit

Output:
  data/data.json         every number the page renders, and nothing the page does not

No figure on the page may exist outside data.json. `make_page.py --check` re-renders
the page from this file and fails on a one-byte difference.
"""
import csv, json, os, sys
from datetime import date

ART = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "artifacts", "cycle-001",
    "2026-09-03-who-finds-the-error")
DATA = os.path.join(ART, "data")

SELF_CODES = ("self-unprompted", "self-machine-check", "self-convened-adversary",
              "self-after-external-prompt")
EXT_CODES = ("external-sibling", "external-architect",
             "external-machine-gate", "external-other")

TODAY = "2026-09-03"


def d(s):
    y, m, dd = (int(x) for x in s.split("-"))
    return date(y, m, dd)


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main():
    rows = load("corrections.csv")
    units = load("shipped_units.csv")
    comp = load("completeness.csv")
    excl = load("excluded.csv")

    for r in rows:
        r["standing_days"] = (
            (d(r["correction_date"]) - d(r["origin_date"])).days
            if r["correction_date"] != "unstated" and r["origin_date"] != "unstated"
            else None)

    shipped = [r for r in rows if r["stratum"] == "SHIPPED"]
    draft = [r for r in rows if r["stratum"] == "DRAFT"]

    def tally(rs):
        t = {}
        for r in rs:
            t[r["finder"]] = t.get(r["finder"], 0) + 1
        return dict(sorted(t.items()))

    def bucket(rs):
        s = sum(1 for r in rs if r["finder"] in SELF_CODES)
        e = sum(1 for r in rs if r["finder"] in EXT_CODES)
        u = sum(1 for r in rs if r["finder"] == "unstated")
        return {"self": s, "external": e, "unstated": u}

    def days(rs):
        v = sorted(r["standing_days"] for r in rs if r["standing_days"] is not None)
        if not v:
            return {"n": 0}
        n = len(v)
        med = v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2
        return {"n": n, "min": v[0], "max": v[-1], "median": med,
                "mean": round(sum(v) / n, 1), "values": v}

    # The corrected object is the directory the correction file sits in — derived,
    # never supplied by a coder, so it cannot drift from the filesystem.
    for r in rows:
        r["object"] = os.path.dirname(r["file"])
    corrected_objects = sorted({r["object"] for r in shipped})

    # The standing-error curve: how many published errors were live and uncorrected
    # on each day of the practice's life. An error is "live" from its origin_date
    # (inclusive) to its correction_date (exclusive).
    first = min(d(u["date"]) for u in units)
    last = d(TODAY)
    curve = []
    span = (last - first).days
    for i in range(span + 1):
        day = date.fromordinal(first.toordinal() + i)
        live = sum(1 for r in shipped
                   if r["origin_date"] != "unstated"
                   and r["correction_date"] != "unstated"
                   and d(r["origin_date"]) <= day < d(r["correction_date"]))
        curve.append({"date": day.isoformat(), "live": live})
    peak = max(curve, key=lambda c: c["live"])

    ship_b = bucket(shipped)

    # Sensitivity 1 — the mixed class reassigned to external. Pre-declared as a
    # deviation (D3): one entry states the practice found the defect during an audit
    # that a sibling's questions set off. It is coded self; this asks whether P1's
    # verdict depends on that choice.
    mixed = sum(1 for r in shipped if r["finder"] == "self-after-external-prompt")
    sens_mixed = {"self": ship_b["self"] - mixed,
                  "external": ship_b["external"] + mixed}

    # Sensitivity 2 — the overlapping delivery errata collapsed to one entry.
    # Five shipped entries describe defects in the same work that a later dated
    # entry also repairs; counting each separately inflates the total.
    ov = [r for r in shipped if r["overlap_note"] and "ERRATA" in r["file"]]
    sens_overlap = {"n": len(shipped) - max(0, len(ov) - 1),
                    "self": ship_b["self"] - max(0, len(ov) - 1),
                    "external": ship_b["external"]}
    out = {
        "generated_from": "data/corrections.csv + data/shipped_units.csv",
        "today": TODAY,
        "population_files": 13,
        "shipped_units": len(units),
        "shipped_units_by_kind": {
            k: sum(1 for u in units if u["kind"] == k)
            for k in ("work", "artifact", "delivery", "presentation")},
        "entries_total": len(rows),
        "shipped": {
            "n": len(shipped),
            "objects_corrected": len(corrected_objects),
            "objects": corrected_objects,
            "finders": tally(shipped),
            "buckets": ship_b,
            "standing_days": days(shipped),
            "consequences": {c: sum(1 for r in shipped if r["consequence"] == c)
                             for c in sorted({r["consequence"] for r in shipped})},
        },
        "draft": {
            "n": len(draft),
            "finders": tally(draft),
            "buckets": bucket(draft),
            "standing_days": days(draft),
        },
        "completeness": comp,
        "completeness_unfiled": sum(1 for c in comp if c["filed"] == "false"),
        "excluded": excl,
        "curve": curve,
        "curve_peak": peak,
        "curve_first_day": first.isoformat(),
        "rows": rows,
    }

    # Pre-registered decisions, evaluated here so they cannot be argued after the fact.
    unstated_share = (ship_b["unstated"] / len(shipped)) if shipped else 1.0
    # EXPLORATORY, not a test. The cut date was chosen after seeing the data and is
    # not pre-registered: 2026-09-01 is the first day a sibling practice is recorded
    # reading this practice's shipped files. Reported because the alternative — an era
    # in which nobody outside was looking — is the obvious innocent explanation of a
    # self-found majority, and leaving it unstated would be the dishonest choice.
    CUT = "2026-09-01"
    era = {}
    for name, sel in (("before_any_outside_reader",
                       [r for r in shipped if r["correction_date"] < CUT]),
                      ("after_first_outside_reader",
                       [r for r in shipped if r["correction_date"] >= CUT])):
        era[name] = {"n": len(sel), **bucket(sel)}
    out["era_exploratory"] = {"cut": CUT, "note":
        "Post-hoc split, chosen after seeing the data. Not a pre-registered test.",
        **era}

    out["sensitivity"] = {
        "mixed_class_as_external": sens_mixed,
        "errata_collapsed_to_one": sens_overlap,
        "verdict_unchanged": (sens_mixed["self"] >= sens_mixed["external"])
                             == (ship_b["self"] >= ship_b["external"])
                             and (sens_overlap["self"] >= sens_overlap["external"])
                             == (ship_b["self"] >= ship_b["external"]),
    }
    out["decisions"] = {
        "K1_underpowered": len(shipped) < 10,
        "K1_threshold": 10,
        "K2_record_will_not_bear": unstated_share > 1 / 3,
        "K2_unstated_share": round(unstated_share, 4),
        "P1_external_outnumber_self": ship_b["external"] > ship_b["self"],
        "P1_falsified": ship_b["self"] >= ship_b["external"],
        "K3_convention_is_not_the_record":
            any(c["filed"] == "false" for c in comp),
    }

    with open(os.path.join(DATA, "data.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)

    print(json.dumps({k: v for k, v in out.items()
                      if k not in ("curve", "rows")}, indent=1)[:4000])


if __name__ == "__main__":
    main()
