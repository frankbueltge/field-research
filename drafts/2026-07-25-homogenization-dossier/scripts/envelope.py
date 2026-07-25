"""
scripts/envelope.py — PREREGISTRATION.md §4-§7: the ordinary-drift envelope, anomaly
rule, per-metric classification, and stratum verdicts. Works from metrics.py's
per-stratum metrics JSON only — no corpus access, no re-tokenization, no re-sampling.

Reorientation (§3, §4): "every metric is reoriented so that collapse = negative"
applies to the four §3 margin metrics (mtld, hapax_share, zipf_slope, similarity).
Raw z = (y - yhat) / SE_pred is already collapse-negative for mtld, hapax_share and
zipf_slope: their stated collapse direction is "down" / "more negative", so a
lower-than-predicted value already yields a negative raw z. similarity's collapse
direction is "up" (more similar = more homogeneous), so its reoriented z is
-1 * raw z, per §3's explicit instruction ("similarity enters with sign flipped").

The marker channel (§8) is explicitly "NOT a margin metric" and is never folded into
that collapse-negative reorientation. §7's validity precondition instead defines its
own convention: math.NT's marker channel must not meet the anomaly rule in the
"excess direction" (§7: "anomaly rule (excess direction)"). This module keeps
marker-channel z UNREORIENTED (raw) and applies a positive-side rule to it
(z_raw > +t), never the negative-side rule used for the four margin metrics.

t-critical: t(0.975, df=14) = 2.1448 is hardcoded per §4, for the 16-unit envelope
(2 fitted parameters, df = 16 - 2 = 14). The quadratic sensitivity table (§4
"Sensitivity", explicitly non-decisional) extends the identical OLS prediction-interval
principle to a 3-parameter (quadratic) fit, df = 16 - 3 = 13, and uses the standard
t(0.975, df=13) = 2.1604 critical value. Neither the quadratic fit nor its critical
value feeds classification, anomaly rules, or verdicts anywhere in this module.
"""
import argparse
import json
import math
import os
import sys
from collections import Counter
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stats import ols_simple, ols_poly, predict_poly, poly_pred_se  # noqa: E402

T_CRIT_LINEAR = 2.1448   # t(0.975, df=14) — hardcoded per PREREGISTRATION.md §4.
T_CRIT_QUADRATIC = 2.1604  # t(0.975, df=13) — standard table value, sensitivity-only.
DELTA_THRESHOLD = 0.5

MARGIN_METRIC_DIRECTIONS = {
    "mtld": "low",
    "hapax_share": "low",
    "zipf_slope": "low",
    "similarity": "high",
}
DECISION_STRATA = ("cs.CL", "cs.CV")
CONTROL_STRATUM = "math.NT"
ALL_STRATA = ("cs.CL", "cs.CV", "math.NT")

BUCKET_MAP = {"CONTINUE": "DECLINE", "NEW-ONSET": "DECLINE", "PLATEAU": "PLATEAU", "REVERSE": "REVERSE"}


# ---------------------------------------------------------------------------
# Units / windows (§2, §5)
# ---------------------------------------------------------------------------

def half_year_units(start_year=2015, start_half=1, end_year=2026, end_half=1):
    units = []
    y, h = start_year, start_half
    while (y, h) <= (end_year, end_half):
        units.append(f"{y}H{h}")
        h, y = (2, y) if h == 1 else (1, y + 1)
    return units


UNITS = half_year_units()               # 23 units, 2015H1..2026H1
ENVELOPE_UNITS = UNITS[0:16]            # 2015H1..2022H2 (x = 0..15)
REFERENCE_UNITS = UNITS[16:20]          # 2023H1..2024H2
EXTENSION_UNITS = UNITS[20:23]          # 2025H1, 2025H2, 2026H1
MARKER_VALIDITY_UNITS = UNITS[16:23]    # 2023H1..2026H1 (§7 control precondition)


# ---------------------------------------------------------------------------
# Envelope fit + prediction SE (§4)
# ---------------------------------------------------------------------------

def fit_envelope_linear(xs_env, ys_env):
    a, b, xbar, sxx, ss_res = ols_simple(xs_env, ys_env)
    n = len(xs_env)
    df = n - 2
    s = math.sqrt(ss_res / df)
    return {"a": a, "b": b, "xbar": xbar, "sxx": sxx, "s": s, "df": df, "n": n}


def pred_se_linear(fit, x):
    return fit["s"] * math.sqrt(1 + 1.0 / fit["n"] + (x - fit["xbar"]) ** 2 / fit["sxx"])


def build_metric_table(unit_values, direction):
    """unit_values: list of (unit, x, value_or_None) for all UNITS, in order.
    direction: 'low' (collapse=down; raw z already collapse-negative),
               'high' (collapse=up, e.g. similarity; flip sign),
               'excess' (marker channel; unreoriented, positive-side rule).
    Returns (fit, rows).
    """
    env_points = [(x, v) for (unit, x, v) in unit_values[:16] if v is not None]
    if len(env_points) < 16:
        raise ValueError(
            f"envelope fit requires all 16 envelope-unit values present; got {len(env_points)}"
        )
    xs_env = [x for x, v in env_points]
    ys_env = [v for x, v in env_points]
    fit = fit_envelope_linear(xs_env, ys_env)

    rows = []
    for unit, x, v in unit_values:
        if v is None:
            rows.append({
                "unit": unit, "x": x, "value": None, "yhat": None, "se": None,
                "z_raw": None, "z": None, "out_of_band": False,
            })
            continue
        yhat = fit["a"] + fit["b"] * x
        se = pred_se_linear(fit, x)
        z_raw = (v - yhat) / se
        if direction == "low":
            z = z_raw
            out = z < -T_CRIT_LINEAR
        elif direction == "high":
            z = -z_raw
            out = z < -T_CRIT_LINEAR
        elif direction == "excess":
            z = z_raw
            out = z_raw > T_CRIT_LINEAR
        else:
            raise ValueError(f"unknown direction {direction!r}")
        rows.append({
            "unit": unit, "x": x, "value": v, "yhat": yhat, "se": se,
            "z_raw": z_raw, "z": z, "out_of_band": out,
        })
    return fit, rows


def anomaly_in_window(rows, window_units):
    """§4: out-of-band in two consecutive units of the window."""
    by_unit = {r["unit"]: r for r in rows}
    ordered = [by_unit[u] for u in window_units if u in by_unit]
    for i in range(len(ordered) - 1):
        if ordered[i]["out_of_band"] and ordered[i + 1]["out_of_band"]:
            return True
    return False


def window_mean_z(rows, window_units):
    by_unit = {r["unit"]: r for r in rows}
    vals = [by_unit[u]["z"] for u in window_units if u in by_unit and by_unit[u]["z"] is not None]
    if not vals:
        return None
    return sum(vals) / len(vals)


# ---------------------------------------------------------------------------
# Classification (§6)
# ---------------------------------------------------------------------------

def classify(a_ref, a_ext, delta):
    if not a_ref and not a_ext:
        return "NO-ANOMALY"
    if a_ext and delta is not None and delta <= -DELTA_THRESHOLD:
        return "NEW-ONSET" if not a_ref else "CONTINUE"
    if a_ext and delta is not None and abs(delta) < DELTA_THRESHOLD:
        return "PLATEAU"
    if delta is not None and delta >= DELTA_THRESHOLD:
        return "REVERSE"
    return None  # residual: reported by z-table, no headline label


def reverse_sublabel(rows, extension_units):
    by_unit = {r["unit"]: r for r in rows}
    ext_rows = [by_unit[u] for u in extension_units if u in by_unit]
    inside = all(r["z"] is not None and abs(r["z"]) < T_CRIT_LINEAR for r in ext_rows)
    return "FULL" if inside else "PARTIAL"


def metric_report(metric_name, direction, unit_values):
    fit, rows = build_metric_table(unit_values, direction)
    a_ref = anomaly_in_window(rows, REFERENCE_UNITS)
    a_ext = anomaly_in_window(rows, EXTENSION_UNITS)
    delta_ref = window_mean_z(rows, REFERENCE_UNITS)
    delta_ext = window_mean_z(rows, EXTENSION_UNITS)
    delta = (delta_ext - delta_ref) if (delta_ref is not None and delta_ext is not None) else None
    label = classify(a_ref, a_ext, delta)
    sub_label = reverse_sublabel(rows, EXTENSION_UNITS) if label == "REVERSE" else None
    return {
        "metric": metric_name,
        "direction": direction,
        "envelope_fit": {
            "intercept": fit["a"], "slope": fit["b"], "s": fit["s"],
            "df": fit["df"], "xbar": fit["xbar"], "sxx": fit["sxx"],
        },
        "rows": rows,
        "a_ref": a_ref,
        "a_ext": a_ext,
        "delta_ref": delta_ref,
        "delta_ext": delta_ext,
        "delta": delta,
        "label": label,
        "sub_label": sub_label,
    }


def marker_report(unit_values):
    fit, rows = build_metric_table(unit_values, "excess")
    a_ref = anomaly_in_window(rows, REFERENCE_UNITS)
    a_ext = anomaly_in_window(rows, EXTENSION_UNITS)
    a_validity_window = anomaly_in_window(rows, MARKER_VALIDITY_UNITS)
    delta_ref = window_mean_z(rows, REFERENCE_UNITS)
    delta_ext = window_mean_z(rows, EXTENSION_UNITS)
    delta = (delta_ext - delta_ref) if (delta_ref is not None and delta_ext is not None) else None
    return {
        "metric": "marker_rate",
        "direction": "excess",
        "envelope_fit": {
            "intercept": fit["a"], "slope": fit["b"], "s": fit["s"],
            "df": fit["df"], "xbar": fit["xbar"], "sxx": fit["sxx"],
        },
        "rows": rows,
        "a_ref": a_ref,
        "a_ext": a_ext,
        "a_validity_window_2023h1_2026h1": a_validity_window,
        "delta_ref": delta_ref,
        "delta_ext": delta_ext,
        "delta": delta,
    }


# ---------------------------------------------------------------------------
# Quadratic sensitivity (§4 "Sensitivity", explicitly non-decisional)
# ---------------------------------------------------------------------------

def quadratic_metric_report(direction, unit_values):
    env_points = [(x, v) for (unit, x, v) in unit_values[:16] if v is not None]
    if len(env_points) < 16:
        raise ValueError("quadratic sensitivity requires all 16 envelope-unit values present")
    xs = [x for x, v in env_points]
    ys = [v for x, v in env_points]
    coeffs, ss_res, xtx_inv = ols_poly(xs, ys, degree=2)
    n = len(xs)
    df = n - 3
    s = math.sqrt(ss_res / df)

    rows = []
    for unit, x, v in unit_values:
        if v is None:
            rows.append({"unit": unit, "x": x, "value": None, "z": None, "out_of_band": False})
            continue
        yhat = predict_poly(coeffs, x)
        se = poly_pred_se(s, xtx_inv, x, 2)
        z_raw = (v - yhat) / se
        if direction == "low":
            z, out = z_raw, z_raw < -T_CRIT_QUADRATIC
        elif direction == "high":
            z, out = -z_raw, -z_raw < -T_CRIT_QUADRATIC
        else:
            z, out = z_raw, z_raw > T_CRIT_QUADRATIC
        rows.append({"unit": unit, "x": x, "value": v, "yhat": yhat, "se": se, "z": z, "out_of_band": out})

    return {
        "non_decisional": True,
        "coeffs": coeffs,
        "df": df,
        "s": s,
        "rows": rows,
        "a_ref": anomaly_in_window(rows, REFERENCE_UNITS),
        "a_ext": anomaly_in_window(rows, EXTENSION_UNITS),
    }


# ---------------------------------------------------------------------------
# Per-stratum orchestration
# ---------------------------------------------------------------------------

def extract_unit_series(stratum_metrics, value_getter):
    by_unit = {u["unit"]: u for u in stratum_metrics["units"]}
    series = []
    for x, unit in enumerate(UNITS):
        cell = by_unit.get(unit)
        value = value_getter(cell) if cell is not None else None
        series.append((unit, x, value))
    return series


def compute_stratum_report(stratum_metrics):
    stratum = stratum_metrics["stratum"]
    metrics_out = {}
    quad_out = {}
    for metric_key, direction in MARGIN_METRIC_DIRECTIONS.items():
        series = extract_unit_series(stratum_metrics, lambda c, k=metric_key: c[k]["value"])
        metrics_out[metric_key] = metric_report(metric_key, direction, series)
        quad_out[metric_key] = quadratic_metric_report(direction, series)

    marker_series = extract_unit_series(stratum_metrics, lambda c: c["marker_rate"]["value"])
    marker_out = marker_report(marker_series)

    return {
        "stratum": stratum,
        "metrics": metrics_out,
        "marker": marker_out,
        "quadratic_sensitivity": quad_out,
    }


def kill_check(stratum_report):
    """§7 kill condition: <=1 of 4 margin metrics shows any collapse-direction
    anomaly (A_ref or A_ext) -> NO SIGNAL BEYOND ORDINARY DRIFT."""
    count = sum(
        1 for m in MARGIN_METRIC_DIRECTIONS
        if stratum_report["metrics"][m]["a_ref"] or stratum_report["metrics"][m]["a_ext"]
    )
    return count <= 1


def directional_finding_precondition(stratum_report):
    """§7: >=2 of 4 metrics with A_ext in the collapse direction."""
    count = sum(1 for m in MARGIN_METRIC_DIRECTIONS if stratum_report["metrics"][m]["a_ext"])
    return count >= 2


def headline_state(stratum_report):
    """§6: majority vote (strict majority, i.e. >=3 of 4) among metric labels, pooling
    CONTINUE and NEW-ONSET as one 'DECLINE' bucket. No bucket reaching a strict
    majority -> MIXED, reported metric-by-metric."""
    buckets = Counter()
    for m in MARGIN_METRIC_DIRECTIONS:
        label = stratum_report["metrics"][m]["label"]
        buckets[BUCKET_MAP.get(label, "NO-ANOMALY")] += 1
    for bucket, count in buckets.items():
        if count >= 3:
            return bucket, dict(buckets)
    return "MIXED", dict(buckets)


# ---------------------------------------------------------------------------
# Cross-stratum verdicts (§7)
# ---------------------------------------------------------------------------

def build_results(stratum_metrics_by_name):
    strata_reports = {s: compute_stratum_report(stratum_metrics_by_name[s]) for s in ALL_STRATA}

    math_report = strata_reports[CONTROL_STRATUM]
    math_marker_valid = not math_report["marker"]["a_validity_window_2023h1_2026h1"]
    math_a_ext_margin_count = sum(
        1 for m in MARGIN_METRIC_DIRECTIONS if math_report["metrics"][m]["a_ext"]
    )
    control_clear = math_a_ext_margin_count < 2

    verdicts = {}
    kills = {}
    for stratum in DECISION_STRATA:
        rep = strata_reports[stratum]
        kill = kill_check(rep)
        directional = directional_finding_precondition(rep)
        headline, bucket_counts = headline_state(rep)

        if kill:
            verdict = "NO SIGNAL BEYOND ORDINARY DRIFT"
        elif directional:
            if not math_marker_valid:
                verdict = (
                    "directional finding: margins shrinking beyond ordinary drift "
                    "(math.NT control downgraded to comparison stratum — marker-channel "
                    "validity precondition failed; informative only, no veto)"
                )
            elif control_clear:
                verdict = "directional finding: margins shrinking beyond ordinary drift"
            else:
                verdict = "shared shift — attribution open"
        else:
            verdict = "no directional finding (fewer than 2 metrics with A_ext)"

        kills[stratum] = kill
        verdicts[stratum] = {
            "kill_condition_met": kill,
            "directional_finding_precondition_met": directional,
            "headline_state": headline,
            "headline_bucket_counts": bucket_counts,
            "verdict": verdict,
        }

    both_decision_strata_no_signal = all(kills[s] for s in DECISION_STRATA)

    return {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "units": UNITS,
        "windows": {
            "envelope": ENVELOPE_UNITS,
            "reference": REFERENCE_UNITS,
            "extension": EXTENSION_UNITS,
            "marker_validity": MARKER_VALIDITY_UNITS,
        },
        "constants": {
            "t_crit_linear_df14": T_CRIT_LINEAR,
            "t_crit_quadratic_df13_sensitivity_only": T_CRIT_QUADRATIC,
            "delta_threshold": DELTA_THRESHOLD,
        },
        "strata": strata_reports,
        "control": {
            "math_nt_marker_channel_valid": math_marker_valid,
            "math_nt_a_ext_margin_metric_count": math_a_ext_margin_count,
            "control_clear": control_clear,
        },
        "verdicts": verdicts,
        "both_decision_strata_no_signal": both_decision_strata_no_signal,
        "familywise_false_positive_arithmetic": {
            "one_metric_A_ext_p_approx": 0.00123,
            "two_of_four_independent_p_approx": 9e-6,
            "two_of_four_totally_correlated_p_approx": 1.2e-3,
            "across_two_decision_strata_correlated_p_approx": 2.5e-3,
            "note": (
                "Static values disclosed per PREREGISTRATION.md §7, not computed from "
                "this run's data. Approximations; serial correlation in half-year units "
                "widens these further; direction of each approximation is noted in the "
                "shipped work, not here."
            ),
        },
    }


# ---------------------------------------------------------------------------
# Markdown summary
# ---------------------------------------------------------------------------

def render_markdown(results):
    lines = []
    lines.append("# Homogenization Dossier — envelope results")
    lines.append("")
    lines.append(f"Generated: {results['generated_utc']}")
    lines.append("")
    lines.append(f"Both decision strata NO SIGNAL: **{results['both_decision_strata_no_signal']}**")
    lines.append("")
    for stratum in ALL_STRATA:
        rep = results["strata"][stratum]
        lines.append(f"## {stratum}")
        lines.append("")
        lines.append("| metric | label | sub | A_ref | A_ext | Δ_ref | Δ_ext | δ |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for m in MARGIN_METRIC_DIRECTIONS:
            r = rep["metrics"][m]
            def fmt(v):
                return "—" if v is None else f"{v:.3f}"
            lines.append(
                f"| {m} | {r['label'] or '(residual)'} | {r['sub_label'] or ''} | "
                f"{r['a_ref']} | {r['a_ext']} | {fmt(r['delta_ref'])} | {fmt(r['delta_ext'])} | {fmt(r['delta'])} |"
            )
        marker = rep["marker"]
        lines.append("")
        lines.append(
            f"Marker channel (excess direction): A_ref={marker['a_ref']}, A_ext={marker['a_ext']}, "
            f"A_validity(2023H1-2026H1)={marker['a_validity_window_2023h1_2026h1']}"
        )
        lines.append("")
        if stratum in results["verdicts"]:
            v = results["verdicts"][stratum]
            lines.append(
                f"Verdict: **{v['verdict']}** "
                f"(kill_condition_met={v['kill_condition_met']}, "
                f"directional_finding_precondition_met={v['directional_finding_precondition_met']}, "
                f"headline_state={v['headline_state']}, buckets={v['headline_bucket_counts']})"
            )
            lines.append("")

    lines.append("## Control")
    lines.append("")
    c = results["control"]
    lines.append(
        f"math.NT marker-channel valid: **{c['math_nt_marker_channel_valid']}** — "
        f"A_ext margin-metric count: {c['math_nt_a_ext_margin_metric_count']} — "
        f"control_clear: {c['control_clear']}"
    )
    lines.append("")
    lines.append("## Familywise false-positive arithmetic (disclosed, static)")
    lines.append("")
    fp = results["familywise_false_positive_arithmetic"]
    lines.append(f"- P(one metric A_ext) ≈ {fp['one_metric_A_ext_p_approx']}")
    lines.append(f"- P(>=2 of 4, independent) ≈ {fp['two_of_four_independent_p_approx']}")
    lines.append(f"- P(>=2 of 4, totally correlated) ≈ {fp['two_of_four_totally_correlated_p_approx']}")
    lines.append(f"- P(across two decision strata, correlated) ≈ {fp['across_two_decision_strata_correlated_p_approx']}")
    lines.append("")
    lines.append("Sensitivity (quadratic envelope) is reported in the JSON results only; it is non-decisional.")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def load_metrics_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main(argv=None):
    parser = argparse.ArgumentParser(description="PREREGISTRATION.md §4-§7 envelope, classification, and verdicts.")
    parser.add_argument("--metrics-dir", required=True, help="Directory with <stratum>.metrics.json files (metrics.py output).")
    parser.add_argument("--outdir", required=True, help="Directory to write results.json and summary.md.")
    args = parser.parse_args(argv)

    stratum_metrics_by_name = {}
    for stratum in ALL_STRATA:
        path = os.path.join(args.metrics_dir, f"{stratum}.metrics.json")
        stratum_metrics_by_name[stratum] = load_metrics_json(path)

    results = build_results(stratum_metrics_by_name)

    os.makedirs(args.outdir, exist_ok=True)
    results_path = os.path.join(args.outdir, "results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, sort_keys=True)

    summary_path = os.path.join(args.outdir, "summary.md")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(render_markdown(results))

    print(f"wrote {results_path}")
    print(f"wrote {summary_path}")


if __name__ == "__main__":
    main()
