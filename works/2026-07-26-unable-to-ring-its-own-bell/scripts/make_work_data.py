#!/usr/bin/env python3
"""
scripts/make_work_data.py -- builds ../data.json for work.astro, stdlib only.

Reads the two frozen results files this instrument shipped:

  results/envelope.json    -- the real, uninjected decisional run (§4/§7).
  results/sensitivity.json -- the pre-registered power curve (§9.2): the same
                               battery re-run after hand-injecting homogenization
                               into decision units 61-73, at p in {0.05..0.50},
                               under two donor recipes (A, B).

and writes a single small JSON document with exactly the fields the page's
slider/recipe-switch interaction needs: one "run" object per (p, recipe) cell,
each shaped like the real run's own verdict so the client script never has to
know that p=0 comes from a different source file than p>0.

Determinism: no wall-clock, no randomness, no dict ordering the source JSON
doesn't already guarantee. Output is written with sort_keys=True and every
float rounded to a fixed number of digits (r4/r6 below), so re-running this
script against the same two input files byte-for-byte reproduces data.json.
Every number below is read from the two input files; none is invented here.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
WORK_DIR = HERE.parent
RESULTS_DIR = WORK_DIR / "results"
OUT_PATH = WORK_DIR / "data.json"

# Fixed decimal precision so the same float always serializes identically.
def r4(x):
    if x is None:
        return None
    return round(x, 4)


def r6(x):
    if x is None:
        return None
    return round(x, 6)


def load(name):
    with open(RESULTS_DIR / name, encoding="utf-8") as f:
        return json.load(f)


def metric_display(name):
    return {
        "mtld": "MTLD",
        "hapax_share": "hapax share",
        "top50_mass": "top-50 mass",
        "similarity": "similarity (trailing)",
    }[name]


def build():
    envelope = load("envelope.json")
    sensitivity = load("sensitivity.json")
    metrics = load("metrics.json")  # corpus sizes, so no count is typed by hand

    windows = envelope["windows"]
    ext_lo, ext_hi = windows["extension"]
    decisional = envelope["decisional"]
    dm = decisional["metrics"]
    metric_names = ["mtld", "hapax_share", "top50_mass", "similarity"]

    structurally_blind = sensitivity["structurally_blind_metrics"]

    metrics_meta = {}
    for name in metric_names:
        m = dm[name]
        fit = m["fit"]
        metrics_meta[name] = {
            "display": metric_display(name),
            "direction": m["direction"],
            "anomaly_rule": m["anomaly_rule"],
            "structurally_blind": name in structurally_blind,
            "fit_n": fit["n_fit"],
            "fit_df": fit["df"],
            "fit_t_crit": r4(fit["t_crit"]),
        }

    # ---- the real, uninjected run (p = 0) -----------------------------------
    real_metrics = {}
    for name in metric_names:
        m = dm[name]
        ext_rows = [r for r in m["rows"] if ext_lo <= r["index"] <= ext_hi]
        oob_units = sorted(r["index"] for r in ext_rows if r.get("out_of_band"))
        real_metrics[name] = {
            "delta_ref": r4(m["delta_ref"]),
            "delta_ext": r4(m["delta_ext"]),
            "delta": r4(m["delta"]),
            "label": m["label"],
            "a_ext": bool(m["a_ext"]),
            "out_of_band": len(oob_units) > 0,
            "out_of_band_units": oob_units,
        }
    # The real run's collapse-direction out-of-band units OUTSIDE the decision
    # window. They are isolated, so they satisfy no anomaly rule -- but the parent
    # instrument shipped the false claim that no such unit existed anywhere and was
    # refuted by its own data, so this page names them rather than filtering them
    # away with the window. Read from the same rows; never typed in.
    outside_decision_window = {}
    for name in metric_names:
        units = sorted(
            r["index"] for r in dm[name]["rows"]
            if r.get("out_of_band") and not (ext_lo <= r["index"] <= ext_hi)
        )
        if units:
            outside_decision_window[name] = units
    dv = decisional["verdict"]
    real_run = {
        "verdict": dv["verdict"],
        # Dated correction, 2026-08-04 (session 87): the notice travels with the
        # verdict into the file the page and any reuser actually parse.
        "verdict_status": dv["verdict_status"],
        "headline_state": dv["headline_state"],
        "kill_condition_met": bool(dv["kill_condition_met"]),
        "denominator": dv["denominator"],
        "any_anomaly_metrics": list(dv["any_anomaly_metrics"]),
        "anomaly_count": len(dv["any_anomaly_metrics"]),
        "metrics": real_metrics,
    }

    # ---- the injected power curve (p > 0), recipes A and B ------------------
    p_grid = sensitivity["p_grid"]  # [0.05, 0.10, ..., 0.50]
    p_values = [0.0] + [float(p) for p in p_grid]
    # p_keys pairs 1:1 with p_values and gives the exact string key each value
    # is stored under in "runs" below -- computed once, here, so the client
    # script never has to reproduce Python's float-to-string formatting.
    p_keys = ["0"] + [str(p) for p in p_grid]

    runs = {"A": {"0": real_run}, "B": {"0": real_run}}
    for recipe in ("A", "B"):
        curve = sensitivity["power_curve"][recipe]
        for p in p_grid:
            key = str(p)
            cell = curve[key]
            cell_metrics = {}
            for name in metric_names:
                cm = cell["metrics"][name]
                oob = cell["per_metric_out_of_band"][name]
                cell_metrics[name] = {
                    "delta_ref": r4(cm["delta_ref"]),
                    "delta_ext": r4(cm["delta_ext"]),
                    "delta": r4(cm["delta"]),
                    "label": cm["label"],
                    "a_ext": bool(cm["a_ext"]),
                    "out_of_band": bool(oob["any_out_of_band"]),
                    "out_of_band_units": sorted(oob["out_of_band_units"]),
                }
            v = cell["verdict"]
            runs[recipe][key] = {
                "verdict": v["verdict"],
                "verdict_status": v["verdict_status"],
                "headline_state": v["headline_state"],
                "kill_condition_met": bool(v["kill_condition_met"]),
                "denominator": v["denominator"],
                "any_anomaly_metrics": list(v["any_anomaly_metrics"]),
                "anomaly_count": len(v["any_anomaly_metrics"]),
                "metrics": cell_metrics,
            }

    recipes = {
        "A": {
            "donor_rank_range": sensitivity["recipes"]["A"]["donor_rank_range"],
            "donor_count": sensitivity["recipes"]["A"]["donor_count"],
            "note": sensitivity["recipes"]["A"]["note"],
        },
        "B": {
            "donor_rank_range": sensitivity["recipes"]["B"]["donor_rank_range"],
            "donor_count": sensitivity["recipes"]["B"]["donor_count"],
            "note": sensitivity["recipes"]["B"]["note"],
        },
    }

    firing_summary = {}
    for recipe in ("A", "B"):
        fs = sensitivity["firing_summary"][recipe]
        firing_summary[recipe] = {
            "battery_fires_at_p": fs["battery_fires_at_p"],
            "per_metric_first_out_of_band_p": dict(fs["per_metric_first_out_of_band_p"]),
            "per_metric_first_own_anomaly_p": dict(fs["per_metric_first_own_anomaly_p"]),
        }

    informativeness = {
        "bar_p": sensitivity["informativeness"]["bar_p"],
        "label": sensitivity["informativeness"]["label"],
        "note": sensitivity["informativeness"]["note"],
    }

    data = {
        # Dated correction, 2026-08-04 (session 87). Read from results/envelope.json,
        # not written here: the notice is defined once, in scripts/envelope_units.py.
        "_void_notice": envelope["_void_notice"],
        "corpus": {
            "units": metrics["n_units"],
            "tokens": sum(u["n_tokens"] for u in metrics["units"]),
            "envelope_window": windows["envelope"],
            "reference_window": windows["reference"],
            "extension_window": windows["extension"],
            "decision_units": list(range(ext_lo, ext_hi + 1)),
        },
        "delta_threshold": envelope["constants"]["delta_threshold"],
        "metrics_order": metric_names,
        "metrics_meta": metrics_meta,
        "p_values": p_values,
        "p_keys": p_keys,
        "recipes": recipes,
        "runs": runs,
        "firing_summary": firing_summary,
        "structurally_blind_metrics": structurally_blind,
        "real_run_out_of_band_outside_decision_window": outside_decision_window,
        "informativeness": informativeness,
        "injection_scope_note": sensitivity["injection_scope_note"],
    }
    return data


def main():
    data = build()
    text = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)
    OUT_PATH.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
