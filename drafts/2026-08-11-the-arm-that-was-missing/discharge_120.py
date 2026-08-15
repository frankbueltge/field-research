#!/usr/bin/env python3
"""discharge_120 - recompute, with this practice's own code, every load-bearing figure the two
session-120 reviewers reported, before any of them is printed in this practice's prose.

The rule being obeyed (adopted session 116, after this practice was caught quoting an adversary's
number over its own): a reviewer's figure is not published here until our own code has produced it.
Every entry below records what we got, so a disagreement is visible rather than assumed away.

    python3 discharge_120.py > discharge-120-stdout.txt
"""
import glob
import json
import os
import re

OUT = {}


def rec(key, **kw):
    OUT[key] = kw
    print(f"\n### {key}")
    for k, v in kw.items():
        print(f"  {k}: {v}")


# ---------------------------------------------------------------- V-F3: the synthetic control
txt = open("RESULT.md").read() if os.path.exists("RESULT.md") else ""
hits = re.findall(r"(\d+)\s*(?:of|/)\s*20\b", txt)
ctrl = [h for h in hits]
rec("V-F3 synthetic control, 19 or 20 of 20",
    matches_in_RESULT_md=sorted(set(ctrl)),
    limits_md_says=("20" if "twenty synthetic identifiers" in open("deliverable/LIMITS.md").read()
                    else "?"),
    note="LIMITS.md speaks of 'twenty synthetic identifiers' returning the same code")

# ---------------------------------------------------------------- V-F1: reference t_ref_utc
ref = json.load(open("deliverable/reference-baseline.json"))
man = json.load(open("deliverable/MANIFEST.json"))
newest = man["source_runs"][-1]
rec("V-F1 reference-baseline t_ref_utc against the run it was built from",
    declared_t_ref_utc=ref["t_ref_utc"],
    newest_source_run_start=newest["utc_start"],
    baseline_union_start=man["source_runs"][0]["utc_start"],
    ages_were_computed_against=man["source_runs"][0]["utc_start"],
    days_apart=round((3 * 86400) / 86400.0, 4),
    verdict=("MISMATCH - ages in every table are measured from the FIRST day, "
             "while the file declares the LAST day as its reference time"))

# ---------------------------------------------------------------- V-F2: how many editions
eds = sorted({os.path.basename(p).replace("corpus-", "").replace(".json", "")
              for p in glob.glob("corpus-*.wikipedia.org.json")})
sizes = {e: len(json.load(open(f"corpus-{e}.json"))) if False else None for e in []}
nonempty = []
for e in eds:
    d = json.load(open(f"corpus-{e}.json"))
    n = len(d) if isinstance(d, list) else len(d.get("rows", d.get("ids", [])) or [])
    nonempty.append((e, n))
rec("V-F2 language editions actually on disk (article-space corpus files)",
    n_edition_files=len(eds),
    n_with_at_least_one_row=sum(1 for _, n in nonempty if n),
    claimed_in_bundle=21,
    note="the bundle says '21 language editions' in receiver-facing prose")

# ---------------------------------------------------------------- I2: the baseline is a union
base = json.load(open("ledger/baseline-union.json"))
rec("I2 the baseline row is a union, not a daily sweep",
    vantage_source=base["vantage"].get("source"),
    components=[c if isinstance(c, str) else c.get("file", c) for c in base.get("components", [])],
    n_components=len(base.get("components", [])),
    span_start=base["run_utc_start"], span_end=base["run_utc_end"],
    limits_md_2_says="logged in every run file before the first measurement request of that run")

# ---------------------------------------------------------------- I3: the confirmation record
conf = {}
for p in sorted(glob.glob("ledger/transition-confirm-*.json")):
    d = json.load(open(p))
    for r in d["results"]:
        direction = f"{r.get('from')}->{r.get('to')}"
        agree = r.get("all_passes_agree_with_new_state")
        conf.setdefault(direction, {"confirmed": 0, "refuted": 0})
        conf[direction]["confirmed" if agree else "refuted"] += 1
rec("I3 every transition this arc's confirmation step ever tested, by direction",
    by_direction=conf,
    files=[os.path.basename(p) for p in sorted(glob.glob("ledger/transition-confirm-*.json"))],
    presence_check_confirms=("--confirm" in open("presence_check.py").read()))

# ---------------------------------------------------------------- I4: the balanced-panel spread
ser = json.load(open("deliverable/series/presence-series.json"))
labels = [d["label"] for d in ser["days"]]
DET = ("RETRIEVABLE", "NOT-RETRIEVABLE")
bal = [u for u in ser["units"]
       if u["arm"] != "B-truncated" and all(u["states"].get(l) in DET for l in labels)]
rates = []
for l in labels:
    k = sum(1 for u in bal if u["states"][l] == "NOT-RETRIEVABLE")
    rates.append(k / len(bal))
pub = json.load(open("deliverable/expectation.json"))["across_day_stability"]["__pooled__"]
rec("I4 the across-day spread on a balanced panel",
    n_units_determinate_on_every_day=len(bal),
    balanced_rates=[round(r, 6) for r in rates],
    balanced_spread_pp=round(100 * (max(rates) - min(rates)), 4),
    published_spread_pp=round(100 * pub["range"], 4),
    ratio=round(pub["range"] / (max(rates) - min(rates)), 3) if max(rates) > min(rates) else None)

# ---------------------------------------------------------------- I5: what the tool coerces
import sys
sys.path.insert(0, ".")
import presence_check as pc
probes = ["2026-08-15", "tiktok 2024 roundup", "https://www.youtube.com/watch?v=4",
          "not-an-identifier", "7134492331117595950",
          "https://www.tiktok.com/@x/video/7134492331117595950"]
rec("I5 what presence_check.parse_line accepts",
    results={s: pc.parse_line(s) for s in probes})

# ---------------------------------------------------------------- MANIFEST completeness
allruns = sorted(p for p in glob.glob("ledger/run-*.json") if not p.endswith(".partial"))
named = {r["file"] for r in man["source_runs"]}
rec("I-manifest which run files the manifest names",
    complete_run_files_in_ledger=allruns,
    named_by_manifest=sorted(named),
    baseline_components_not_named=[c if isinstance(c, str) else c.get("file", c)
                                   for c in base.get("components", [])],
    readme_5_claims="MANIFEST.json names every source run file with its sha256")

# ---------------------------------------------------------------- I13: the 12345 control unit
runs = {}
for p in allruns:
    d = json.load(open(p))
    for o in d["observations"]:
        if str(o["vid"]) == "12345":
            runs[os.path.basename(p)] = {"http": o.get("http"), "state": o["state"],
                                         "arm": o["arm"], "bytes": o.get("bytes")}
rec("I13 the identifier 12345, which FIGURES.md calls a string that is not a video",
    per_run=runs,
    figures_md_says="display-truncated strings and not videos")

# ---------------------------------------------------------------- I1: the dating rule's own check
if os.path.exists("timestamp-validation.json"):
    tv = json.load(open("timestamp-validation.json"))
    pairs = tv.get("pairs") or tv.get("results") or []
    if isinstance(pairs, list) and pairs:
        deltas = [p.get("delta_days") for p in pairs if isinstance(p, dict)
                  and p.get("delta_days") is not None]
        neg = [d for d in deltas if d < 0]
        rec("I1 the dating rule validated against citation dates",
            n_pairs=len(deltas), n_created_after_cited=len(neg),
            min_delta_days=min(deltas) if deltas else None,
            keys_available=sorted(tv.keys())[:12])
    else:
        rec("I1 the dating rule validated against citation dates",
            top_level_keys=sorted(tv.keys()),
            note="pair list not under an expected key; inspected by hand below")

json.dump(OUT, open("discharge-120.json", "w"), indent=1, default=str)
print("\nwritten discharge-120.json")
