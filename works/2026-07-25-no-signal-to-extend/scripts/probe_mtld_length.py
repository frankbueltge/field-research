#!/usr/bin/env python3
"""MTLD length-artifact probe (PROBE-mtld-length.md, session 65).

NON-DECISIONAL diagnostic. It cannot change the locked instrument's verdict; it decides only
how the MTLD excursion is reported. The design and the decision rule were committed to git
BEFORE this script's data was fetched (see PROBE-mtld-length.md).

Reuses the locked instrument's own tokenizer, seeded draw and MTLD implementation unchanged,
so the probe reads the same 150 drawn abstracts per unit that the shipped MTLD number was
computed on -- up to records the archive added or revised since the frozen run, which the probe
measures and reports rather than assuming away.

Per unit it reports:
  n_kept / n_kept_frozen       -- re-fetch difference against provenance/counts.json
  mean_tokens / median_tokens  -- token length of the 150 drawn abstracts
  undefined_share              -- share of drawn abstracts whose bidirectional MTLD is None
  mtld_recomputed              -- MTLD by the shipped definition (sanity check)
  mtld_trunc120                -- the same statistic on abstracts truncated to their first
                                  120 tokens, restricted to drawn abstracts with >= 120 tokens

Usage:
  python3 scripts/probe_mtld_length.py --corpus <dir with cs.CL.jsonl> --out <results.json>
"""

import argparse
import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from metrics import MTLD_DRAW, mtld_bidirectional, seeded_order  # noqa: E402
from tokenizer import tokenize  # noqa: E402

STRATUM = "cs.CL"
PROBE_UNITS = ("2016H1", "2019H1", "2022H2", "2026H1")
TRUNC_LEN = 120


def load_cell(path, unit):
    """All filtered records of one (stratum, unit) cell, from the corpus JSONL."""
    rows = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            if record["unit"] == unit:
                rows.append(record)
    return rows


def probe_unit(rows, stratum, unit, draw_size=MTLD_DRAW, trunc_len=TRUNC_LEN):
    """The per-unit probe statistics. Pure: takes rows, returns a dict."""
    ids = [r["id"] for r in rows]
    tokens_by_id = {r["id"]: tokenize(r["abstract"]) for r in rows}
    order = seeded_order(stratum, unit, ids)
    drawn = order[: min(draw_size, len(ids))]

    lengths = [len(tokens_by_id[rid]) for rid in drawn]

    shipped_scores, n_undefined = [], 0
    for rid in drawn:
        score = mtld_bidirectional(tokens_by_id[rid])
        if score is None:
            n_undefined += 1
        else:
            shipped_scores.append(score)

    # Length channel closed: fixed token count, same draw, same tokenizer.
    trunc_scores, n_eligible, n_trunc_undefined = [], 0, 0
    for rid in drawn:
        tokens = tokens_by_id[rid]
        if len(tokens) < trunc_len:
            continue
        n_eligible += 1
        score = mtld_bidirectional(tokens[:trunc_len])
        if score is None:
            n_trunc_undefined += 1
        else:
            trunc_scores.append(score)

    return {
        "unit": unit,
        "n_kept": len(rows),
        "n_drawn": len(drawn),
        "mean_tokens": statistics.mean(lengths) if lengths else None,
        "median_tokens": statistics.median(lengths) if lengths else None,
        "min_tokens": min(lengths) if lengths else None,
        "max_tokens": max(lengths) if lengths else None,
        "n_undefined": n_undefined,
        "undefined_share": n_undefined / len(drawn) if drawn else None,
        "mtld_recomputed": statistics.mean(shipped_scores) if shipped_scores else None,
        "n_eligible_trunc": n_eligible,
        "n_trunc_undefined": n_trunc_undefined,
        "mtld_trunc120": statistics.mean(trunc_scores) if trunc_scores else None,
    }


def classify(rise_trunc, rise_shipped):
    """The decision rule, fixed in PROBE-mtld-length.md before the fetch."""
    if rise_trunc >= 0.5 * rise_shipped:
        return "NOT A LENGTH ARTIFACT"
    if rise_trunc <= 0.25 * rise_shipped:
        return "SUBSTANTIALLY A LENGTH ARTIFACT"
    return "PARTIAL / INCONCLUSIVE"


def main(argv=None):
    parser = argparse.ArgumentParser(description="MTLD length-artifact probe (non-decisional).")
    parser.add_argument("--corpus", required=True, help="Directory holding cs.CL.jsonl.")
    parser.add_argument("--frozen-counts", default=None, help="provenance/counts.json of the frozen run.")
    parser.add_argument("--shipped-results", default=None, help="results/results.json of the frozen run.")
    parser.add_argument("--out", required=True, help="Where to write the probe result JSON.")
    parser.add_argument(
        "--sensitivity", default=None,
        help="Comma-separated truncation lengths for the POST-HOC robustness annex "
             "(not part of the locked probe design; reported as post hoc).",
    )
    args = parser.parse_args(argv)

    corpus_path = os.path.join(args.corpus, f"{STRATUM}.jsonl")
    cells = {unit: load_cell(corpus_path, unit) for unit in PROBE_UNITS}
    units = [probe_unit(cells[unit], STRATUM, unit) for unit in PROBE_UNITS]
    by_unit = {u["unit"]: u for u in units}

    if args.frozen_counts:
        with open(args.frozen_counts, encoding="utf-8") as handle:
            frozen = json.load(handle)["cells"][STRATUM]
        for unit in PROBE_UNITS:
            by_unit[unit]["n_kept_frozen"] = frozen[unit]["kept"]
            by_unit[unit]["refetch_delta"] = by_unit[unit]["n_kept"] - frozen[unit]["kept"]

    shipped = {}
    if args.shipped_results:
        with open(args.shipped_results, encoding="utf-8") as handle:
            rows = json.load(handle)["strata"][STRATUM]["metrics"]["mtld"]["rows"]
        shipped = {r["unit"]: r["value"] for r in rows}
        for unit in PROBE_UNITS:
            by_unit[unit]["mtld_shipped"] = shipped.get(unit)

    verdict = None
    if shipped:
        rise_shipped = shipped["2026H1"] - shipped["2022H2"]
        rise_trunc = by_unit["2026H1"]["mtld_trunc120"] - by_unit["2022H2"]["mtld_trunc120"]
        verdict = {
            "rise_shipped_2022H2_to_2026H1": rise_shipped,
            "rise_trunc120_2022H2_to_2026H1": rise_trunc,
            "half_threshold": 0.5 * rise_shipped,
            "quarter_threshold": 0.25 * rise_shipped,
            "classification": classify(rise_trunc, rise_shipped),
            "undefined_share_change_2022H2_to_2026H1": (
                by_unit["2026H1"]["undefined_share"] - by_unit["2022H2"]["undefined_share"]
            ),
            "mean_token_change_2022H2_to_2026H1": (
                by_unit["2026H1"]["mean_tokens"] - by_unit["2022H2"]["mean_tokens"]
            ),
        }

    sensitivity = None
    if args.sensitivity:
        sensitivity = {
            "note": "POST HOC, not part of the locked probe design. Same draw, same tokenizer; "
                    "only the truncation length varies. Reported for robustness, decides nothing.",
            "rows": [],
        }
        for trunc in (int(t) for t in args.sensitivity.split(",")):
            row = {"trunc_len": trunc, "by_unit": {}}
            for unit in PROBE_UNITS:
                stats = probe_unit(cells[unit], STRATUM, unit, trunc_len=trunc)
                row["by_unit"][unit] = {
                    "mtld_trunc": stats["mtld_trunc120"],
                    "n_eligible": stats["n_eligible_trunc"],
                }
            row["rise_2022H2_to_2026H1"] = (
                row["by_unit"]["2026H1"]["mtld_trunc"] - row["by_unit"]["2022H2"]["mtld_trunc"]
            )
            sensitivity["rows"].append(row)

    result = {
        "probe": "MTLD length artifact (PROBE-mtld-length.md)",
        "decisional": False,
        "stratum": STRATUM,
        "trunc_len": TRUNC_LEN,
        "draw_size": MTLD_DRAW,
        "units": units,
        "verdict": verdict,
        "post_hoc_sensitivity": sensitivity,
    }
    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
