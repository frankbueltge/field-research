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
that collapse-negative reorientation. §8 fixes its own convention: math.NT's marker
channel must not meet the anomaly rule in the "excess direction" (z > +2.1448). This
module keeps marker-channel z UNREORIENTED (raw) and applies a positive-side rule to
it, never the negative-side rule used for the four margin metrics. The DECISIONAL
marker statistic is computed by metrics.py over the same fixed 15,000-token seeded
pool as hapax/Zipf (constant sampling precision) — that is the series fed to the
envelope here. The whole-cell marker rate is carried through only as CONTEXT (raw
per-unit values, no envelope fit, never contributing to any anomaly/classification).

Classification ladder (§6, fixed order, first match wins):
  NO-ANOMALY -> NEW-ONSET -> CONTINUE -> PLATEAU -> REVERSE -> RESIDUAL.
RESIDUAL is an explicit label (every remaining configuration), not an absence of one.
REVERSE is gated: (A_ref OR A_ext) AND delta >= +0.5 — recovery must be recovery FROM
a documented anomaly in one of the two windows, not a swing between two
never-anomalous windows (that stays NO-ANOMALY, which is checked first anyway).

Non-computable units / non-decidable metric-windows (§3): a unit where a metric can't
be computed is excluded from that window's Delta mean and can't itself satisfy the
two-consecutive rule (both already fall out of anomaly_in_window/window_mean_z, which
skip None-valued units while preserving true calendar adjacency for the ones that ARE
present). Additionally, if fewer than 2 units in a window are computable for a metric,
that window's anomaly boolean (A_ref or A_ext) is UNDECIDABLE (represented as Python
None, not False) for that metric — such a metric's label becomes the explicit
"NON-DECIDABLE" tag, and it is excluded from the ±2-of-4 / <=1 stratum-level counts,
with the reduced denominator disclosed alongside every count in the output.

Stratum verdict (§7) is an ordered 3-step procedure (first applicable step wins):
  1. Directional finding: >=2 of the EXT-decidable metrics show A_ext -> headline is
     the plurality among just those anomalous metrics' labels (CONTINUE+NEW-ONSET
     pooled vs PLATEAU; tie -> "MIXED (shrinking)"), and the verdict sentence is
     further modulated by the math.NT control condition.
  2. Else kill condition: <=1 of the (ref-or-ext)-decidable metrics show any anomaly
     -> NO SIGNAL BEYOND ORDINARY DRIFT.
  3. Else: plurality label over all four metrics' labels (CONTINUE+NEW-ONSET pooled;
     REVERSE sub-labels pooled; NO-ANOMALY/RESIDUAL/NON-DECIDABLE count toward the
     denominator disclosed but can never win); tie or no eligible plurality -> MIXED.

t-critical: t(0.975, df=14) = 2.1448 is hardcoded per §4, for the 16-unit envelope
(2 fitted parameters, df = 16 - 2 = 14). The quadratic sensitivity table extends the
identical OLS prediction-interval principle to a 3-parameter (quadratic) fit,
df = 16 - 3 = 13, using the standard t(0.975, df=13) = 2.1604 critical value.

Soft downgrade rule (§4, decisional): the quadratic fit is no longer purely
non-decisional. Each decision stratum is evaluated under BOTH the linear and the
quadratic envelope via the identical 3-step §7 procedure; if the two envelopes
disagree on the resulting headline_state, both ship, and the stratum is marked
"soft_downgrade_unresolved" — the linear envelope alone cannot carry a verdict its
own curvature check contradicts. (The math.NT control inputs used inside that
3-step procedure are computed from the LINEAR envelope in both calls, for a single,
consistent control baseline; only the decision stratum's own headline_state is what
gets compared and disclosed as agreeing/disagreeing between the two envelope fits.)
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
T_CRIT_QUADRATIC = 2.1604  # t(0.975, df=13) — standard table value, quadratic fit.
DELTA_THRESHOLD = 0.5
MIN_COMPUTABLE_FOR_DECIDABLE = 2  # §3: fewer computable units in a window -> non-decidable

MARGIN_METRIC_DIRECTIONS = {
    "mtld": "low",
    "hapax_share": "low",
    "zipf_slope": "low",
    "similarity": "high",
}
DECISION_STRATA = ("cs.CL", "cs.CV")
CONTROL_STRATUM = "math.NT"
ALL_STRATA = ("cs.CL", "cs.CV", "math.NT")

# Only CONTINUE/NEW-ONSET/PLATEAU/REVERSE map to a pooled bucket; NO-ANOMALY,
# RESIDUAL and NON-DECIDABLE deliberately have no entry (they count toward
# disclosed denominators but can never win a plurality — see plurality_bucket()).
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


def window_computable_count(rows, window_units):
    by_unit = {r["unit"]: r for r in rows}
    return sum(1 for u in window_units if u in by_unit and by_unit[u]["value"] is not None)


def window_decidable(rows, window_units, min_computable=MIN_COMPUTABLE_FOR_DECIDABLE):
    """§3: a window is decidable for a metric only if it has enough computable units
    to possibly satisfy the two-consecutive anomaly rule at all."""
    return window_computable_count(rows, window_units) >= min_computable


# ---------------------------------------------------------------------------
# Classification (§6) — fixed-order ladder, first match wins
# ---------------------------------------------------------------------------

def classify(a_ref, a_ext, delta):
    """a_ref, a_ext: bool (both MUST be decided -- callers route non-decidable
    metrics to the explicit "NON-DECIDABLE" label before ever calling this)."""
    if not a_ref and not a_ext:
        return "NO-ANOMALY"
    if delta is not None:
        if a_ext and not a_ref and delta <= -DELTA_THRESHOLD:
            return "NEW-ONSET"
        if a_ext and delta <= -DELTA_THRESHOLD:
            return "CONTINUE"
        if a_ext and abs(delta) < DELTA_THRESHOLD:
            return "PLATEAU"
        if (a_ref or a_ext) and delta >= DELTA_THRESHOLD:
            return "REVERSE"
    return "RESIDUAL"


def reverse_sublabel(rows, extension_units):
    by_unit = {r["unit"]: r for r in rows}
    ext_rows = [by_unit[u] for u in extension_units if u in by_unit]
    inside = all(r["z"] is not None and abs(r["z"]) < T_CRIT_LINEAR for r in ext_rows)
    return "FULL" if inside else "PARTIAL"


def _classify_from_rows(rows):
    """Shared decidability + classification logic, usable for BOTH the linear rows
    (build_metric_table) and the quadratic rows (quadratic_metric_report) -- the two
    envelopes are compared later via the §4 soft-downgrade rule, so both must go
    through the identical ladder."""
    ref_decidable = window_decidable(rows, REFERENCE_UNITS)
    ext_decidable = window_decidable(rows, EXTENSION_UNITS)
    a_ref = anomaly_in_window(rows, REFERENCE_UNITS) if ref_decidable else None
    a_ext = anomaly_in_window(rows, EXTENSION_UNITS) if ext_decidable else None
    delta_ref = window_mean_z(rows, REFERENCE_UNITS)
    delta_ext = window_mean_z(rows, EXTENSION_UNITS)
    delta = (delta_ext - delta_ref) if (delta_ref is not None and delta_ext is not None) else None

    if a_ref is None or a_ext is None:
        label = "NON-DECIDABLE"
    else:
        label = classify(a_ref, a_ext, delta)
    sub_label = reverse_sublabel(rows, EXTENSION_UNITS) if label == "REVERSE" else None

    return {
        "ref_decidable": ref_decidable,
        "ext_decidable": ext_decidable,
        "a_ref": a_ref,
        "a_ext": a_ext,
        "delta_ref": delta_ref,
        "delta_ext": delta_ext,
        "delta": delta,
        "label": label,
        "sub_label": sub_label,
    }


def metric_report(metric_name, direction, unit_values):
    fit, rows = build_metric_table(unit_values, direction)
    classification = _classify_from_rows(rows)
    return {
        "metric": metric_name,
        "direction": direction,
        "envelope_fit": {
            "intercept": fit["a"], "slope": fit["b"], "s": fit["s"],
            "df": fit["df"], "xbar": fit["xbar"], "sxx": fit["sxx"],
        },
        "rows": rows,
        **classification,
    }


def marker_report(decisional_unit_values, context_unit_values):
    """decisional_unit_values: the fixed 15,000-token-pool marker rate (fed to the
    envelope). context_unit_values: the whole-cell marker rate (NEVER fed to an
    envelope; carried through as raw per-unit values only, for disclosure)."""
    fit, rows = build_metric_table(decisional_unit_values, "excess")
    a_ref = anomaly_in_window(rows, REFERENCE_UNITS)
    a_ext = anomaly_in_window(rows, EXTENSION_UNITS)
    a_validity_window = anomaly_in_window(rows, MARKER_VALIDITY_UNITS)
    delta_ref = window_mean_z(rows, REFERENCE_UNITS)
    delta_ext = window_mean_z(rows, EXTENSION_UNITS)
    delta = (delta_ext - delta_ref) if (delta_ref is not None and delta_ext is not None) else None

    context_rows = [{"unit": unit, "value": v} for (unit, x, v) in context_unit_values]

    return {
        "metric": "marker_rate_pool_decisional",
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
        "context_whole_cell_rate": {
            "note": "Context only -- heteroscedastic across cell sizes by construction, never fed to an envelope.",
            "rows": context_rows,
        },
    }


# ---------------------------------------------------------------------------
# Quadratic envelope (§4 "Sensitivity" + soft-downgrade rule)
# ---------------------------------------------------------------------------

def quadratic_metric_report(direction, unit_values):
    env_points = [(x, v) for (unit, x, v) in unit_values[:16] if v is not None]
    if len(env_points) < 16:
        raise ValueError("quadratic envelope requires all 16 envelope-unit values present")
    xs = [x for x, v in env_points]
    ys = [v for x, v in env_points]
    coeffs, ss_res, xtx_inv = ols_poly(xs, ys, degree=2)
    n = len(xs)
    df = n - 3
    s = math.sqrt(ss_res / df)

    rows = []
    for unit, x, v in unit_values:
        if v is None:
            rows.append({"unit": unit, "x": x, "value": None, "yhat": None, "se": None,
                          "z_raw": None, "z": None, "out_of_band": False})
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
        rows.append({"unit": unit, "x": x, "value": v, "yhat": yhat, "se": se,
                     "z_raw": z_raw, "z": z, "out_of_band": out})

    classification = _classify_from_rows(rows)
    return {
        "coeffs": coeffs,
        "df": df,
        "s": s,
        "rows": rows,
        **classification,
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

    marker_decisional_series = extract_unit_series(stratum_metrics, lambda c: c["marker_rate_pool"]["value"])
    marker_context_series = extract_unit_series(stratum_metrics, lambda c: c["marker_rate_whole_cell_context"]["value"])
    marker_out = marker_report(marker_decisional_series, marker_context_series)

    return {
        "stratum": stratum,
        "metrics": metrics_out,
        "marker": marker_out,
        "quadratic_sensitivity": quad_out,
    }


# ---------------------------------------------------------------------------
# §7 ordered 3-step stratum verdict
# ---------------------------------------------------------------------------

def _margin_ext_decidable_and_anomalous(metrics_dict):
    decidable = [m for m in MARGIN_METRIC_DIRECTIONS if metrics_dict[m]["ext_decidable"]]
    anomalous = [m for m in decidable if metrics_dict[m]["a_ext"]]
    return decidable, anomalous


def _margin_any_anomaly_decidable(metrics_dict):
    decidable = []
    anomalous = []
    for m in MARGIN_METRIC_DIRECTIONS:
        mr = metrics_dict[m]
        is_decidable = mr["ref_decidable"] or mr["ext_decidable"]
        if not is_decidable:
            continue
        decidable.append(m)
        if bool(mr["a_ref"]) or bool(mr["a_ext"]):
            anomalous.append(m)
    return decidable, anomalous


def plurality_bucket(labels, eligible_buckets, tie_label):
    """Generic §6/§7 plurality-vote helper. `labels` is the FULL list under
    consideration (including non-eligible ones like NO-ANOMALY/RESIDUAL/
    NON-DECIDABLE, which count toward the disclosed denominator but can never win).
    Returns (winner_or_tie_label, pooled_bucket_counts, all_label_counts)."""
    all_counts = Counter(labels)
    bucket_counts = Counter()
    for lbl in labels:
        bucket = BUCKET_MAP.get(lbl)
        if bucket is not None:
            bucket_counts[bucket] += 1
    eligible_counts = {b: bucket_counts.get(b, 0) for b in eligible_buckets}
    max_count = max(eligible_counts.values()) if eligible_counts else 0
    if max_count == 0:
        return tie_label, dict(bucket_counts), dict(all_counts)
    winners = [b for b, c in eligible_counts.items() if c == max_count]
    if len(winners) == 1:
        return winners[0], dict(bucket_counts), dict(all_counts)
    return tie_label, dict(bucket_counts), dict(all_counts)


def _math_control_info(math_report):
    """Computed once, from the LINEAR envelope, and shared by both decision strata's
    §7 evaluations (both the linear AND quadratic evaluation calls use this same
    control baseline -- see module docstring)."""
    marker_valid = not math_report["marker"]["a_validity_window_2023h1_2026h1"]
    decidable, anomalous = _margin_ext_decidable_and_anomalous(math_report["metrics"])
    control_clear = len(anomalous) < 2
    return {
        "marker_valid": marker_valid,
        "control_clear": control_clear,
        "ext_decidable_metrics": decidable,
        "ext_anomalous_metrics": anomalous,
    }


def evaluate_stratum(metrics_dict, math_info):
    """§7's ordered 3-step procedure over one envelope realization's per-metric
    classification dicts (metrics_dict: {metric_key: classification_dict}, as
    produced by metric_report()/quadratic_metric_report())."""
    ext_decidable, ext_anomalous = _margin_ext_decidable_and_anomalous(metrics_dict)

    # Step 1: directional finding.
    if len(ext_anomalous) >= 2:
        labels = [metrics_dict[m]["label"] for m in ext_anomalous]
        headline, bucket_counts, all_counts = plurality_bucket(
            labels, eligible_buckets=("DECLINE", "PLATEAU"), tie_label="MIXED (shrinking)"
        )
        if not math_info["marker_valid"]:
            verdict = (
                "directional finding: margins shrinking beyond ordinary drift "
                "(math.NT control downgraded to comparison stratum — marker-channel "
                "validity precondition failed; informative only, no veto)"
            )
        elif math_info["control_clear"]:
            verdict = "directional finding: margins shrinking beyond ordinary drift"
        else:
            verdict = "shared shift — attribution open"
        return {
            "step": 1,
            "step_name": "directional_finding",
            "ext_decidable_metrics": ext_decidable,
            "ext_anomalous_metrics": ext_anomalous,
            "denominator": len(ext_decidable),
            "headline_state": headline,
            "headline_bucket_counts": bucket_counts,
            "headline_label_counts": all_counts,
            "kill_condition_met": False,
            "verdict": verdict,
        }

    # Step 2: kill condition.
    any_decidable, any_anomalous = _margin_any_anomaly_decidable(metrics_dict)
    if len(any_anomalous) <= 1:
        return {
            "step": 2,
            "step_name": "kill_condition",
            "any_anomaly_decidable_metrics": any_decidable,
            "any_anomaly_metrics": any_anomalous,
            "denominator": len(any_decidable),
            "headline_state": "NO SIGNAL",
            "headline_bucket_counts": {},
            "headline_label_counts": {},
            "kill_condition_met": True,
            "verdict": "NO SIGNAL BEYOND ORDINARY DRIFT",
        }

    # Step 3: plurality over all four metrics' labels.
    labels = [metrics_dict[m]["label"] for m in MARGIN_METRIC_DIRECTIONS]
    headline, bucket_counts, all_counts = plurality_bucket(
        labels, eligible_buckets=("DECLINE", "PLATEAU", "REVERSE"), tie_label="MIXED"
    )
    if headline == "REVERSE":
        verdict = "REVERSE — the documented anomaly did not persist against the envelope."
    elif headline == "MIXED":
        verdict = "MIXED (reported metric-by-metric)"
    else:
        verdict = f"{headline} (step-3 plurality; not a directional finding)"
    return {
        "step": 3,
        "step_name": "plurality_over_all_four",
        "denominator": len(labels),
        "headline_state": headline,
        "headline_bucket_counts": bucket_counts,
        "headline_label_counts": all_counts,
        "kill_condition_met": False,
        "verdict": verdict,
    }


# ---------------------------------------------------------------------------
# Cross-stratum verdicts (§7) + soft-downgrade rule (§4)
# ---------------------------------------------------------------------------

def build_results(stratum_metrics_by_name):
    strata_reports = {s: compute_stratum_report(stratum_metrics_by_name[s]) for s in ALL_STRATA}

    math_report = strata_reports[CONTROL_STRATUM]
    math_info = _math_control_info(math_report)

    verdicts = {}
    for stratum in DECISION_STRATA:
        rep = strata_reports[stratum]
        linear_eval = evaluate_stratum(rep["metrics"], math_info)
        quadratic_eval = evaluate_stratum(rep["quadratic_sensitivity"], math_info)

        unresolved = linear_eval["headline_state"] != quadratic_eval["headline_state"]
        if unresolved:
            headline_state = f"UNRESOLVED (linear={linear_eval['headline_state']!r} vs quadratic={quadratic_eval['headline_state']!r})"
            verdict = (
                "§4 soft-downgrade rule: linear and quadratic envelopes disagree on this "
                f"stratum's headline state (linear: {linear_eval['headline_state']!r}, "
                f"quadratic: {quadratic_eval['headline_state']!r}). Both ship, marked unresolved."
            )
        else:
            headline_state = linear_eval["headline_state"]
            verdict = linear_eval["verdict"]

        verdicts[stratum] = {
            "linear": linear_eval,
            "quadratic": quadratic_eval,
            "soft_downgrade_unresolved": unresolved,
            "headline_state": headline_state,
            "kill_condition_met": linear_eval["kill_condition_met"],
            "verdict": verdict,
        }

    both_decision_strata_no_signal = all(
        verdicts[s]["kill_condition_met"] and not verdicts[s]["soft_downgrade_unresolved"]
        for s in DECISION_STRATA
    )

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
            "t_crit_quadratic_df13": T_CRIT_QUADRATIC,
            "delta_threshold": DELTA_THRESHOLD,
            "min_computable_for_decidable": MIN_COMPUTABLE_FOR_DECIDABLE,
        },
        "strata": strata_reports,
        "control": {
            "math_nt_marker_channel_valid": math_info["marker_valid"],
            "math_nt_control_clear": math_info["control_clear"],
            "math_nt_ext_decidable_metrics": math_info["ext_decidable_metrics"],
            "math_nt_ext_anomalous_metrics": math_info["ext_anomalous_metrics"],
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

def _fmt(v):
    return "—" if v is None else f"{v:.3f}"


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
        lines.append("| metric | label | sub | decidable(ref/ext) | A_ref | A_ext | Δ_ref | Δ_ext | δ |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for m in MARGIN_METRIC_DIRECTIONS:
            r = rep["metrics"][m]
            lines.append(
                f"| {m} | {r['label']} | {r['sub_label'] or ''} | "
                f"{r['ref_decidable']}/{r['ext_decidable']} | "
                f"{r['a_ref']} | {r['a_ext']} | {_fmt(r['delta_ref'])} | {_fmt(r['delta_ext'])} | {_fmt(r['delta'])} |"
            )
        marker = rep["marker"]
        lines.append("")
        lines.append(
            f"Marker channel (decisional, pool-based, excess direction): A_ref={marker['a_ref']}, "
            f"A_ext={marker['a_ext']}, A_validity(2023H1-2026H1)={marker['a_validity_window_2023h1_2026h1']}. "
            "Whole-cell rate reported as context only in the JSON (never fed to an envelope)."
        )
        lines.append("")
        if stratum in results["verdicts"]:
            v = results["verdicts"][stratum]
            lines.append(
                f"Verdict: **{v['verdict']}** "
                f"(headline_state={v['headline_state']}, step={v['linear']['step']}, "
                f"soft_downgrade_unresolved={v['soft_downgrade_unresolved']})"
            )
            lines.append("")

    lines.append("## Control")
    lines.append("")
    c = results["control"]
    lines.append(
        f"math.NT marker-channel valid: **{c['math_nt_marker_channel_valid']}** — "
        f"control_clear: {c['math_nt_control_clear']} — "
        f"ext-anomalous margin metrics: {c['math_nt_ext_anomalous_metrics']} "
        f"(of {len(c['math_nt_ext_decidable_metrics'])} decidable)"
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
    lines.append(
        "Sensitivity: each stratum's headline_state is computed under BOTH the linear "
        "and quadratic envelope (§4 soft-downgrade rule); disagreement is flagged "
        "'soft_downgrade_unresolved' above and both headlines ship in the JSON."
    )
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
