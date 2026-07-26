"""
scripts/envelope_units.py — PREREGISTRATION.md §4/§5/§6/§7/§8: the ordinary-drift
envelope, anomaly rule, per-metric classification and the verdict, over this draft's
own per-unit metrics (`results/metrics.json`, frozen input, never regenerated here).

Reuses `works/2026-07-25-no-signal-to-extend/scripts/stats.py` UNCHANGED for the OLS
machinery (`ols_simple`, `ols_poly`, `predict_poly`, `poly_pred_se`), and this draft's
own `scripts/tdist.py` for every t-critical value (never hardcoded, per §4).

Structure mirrors `works/2026-07-25-no-signal-to-extend/scripts/envelope.py` (the parent
instrument's envelope/classification/verdict module): the same reorientation convention
("low" = raw z already collapse-negative; "high" = sign-flipped; "excess" = the marker
channel's unreoriented positive-side rule), the same fixed-order §6 ladder, and the same
ordered 3-step §7 verdict procedure — adapted from the parent's (stratum, half-year)
grid to this instrument's (single corpus, unit-index) grid, and extended with:
  - metric 4's (similarity) five-apart anomaly exception (§4, Skeptic condition 1);
  - the §7 SINGLE-CHANNEL downgrade (hapax_share + top50_mass alone is not corroboration);
  - five declared non-decisional branches (§4 curvature + founding-transient; §3 prop40,
    sim_content, sim_block) run through the identical machinery, each with its own §7
    verdict, never influencing the decisional one.

Windows are FIXED unit-index ranges per §5 (envelope 1-47, reference 48-60, extension
61-73) — not recomputed from dates; §5 already fixes them as index ranges.
"""
import json
import math
import os
import sys
from collections import Counter
from datetime import datetime, timezone

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_DRAFT_DIR = os.path.dirname(_SCRIPT_DIR)
_REPO_ROOT = os.path.dirname(os.path.dirname(_DRAFT_DIR))
_PARENT_SCRIPTS = os.path.join(_REPO_ROOT, "works", "2026-07-25-no-signal-to-extend", "scripts")
for _p in (_PARENT_SCRIPTS, _SCRIPT_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from stats import ols_simple, ols_poly, predict_poly, poly_pred_se  # noqa: E402  (parent, UNCHANGED)
from tdist import t975  # noqa: E402

METRICS_PATH = os.path.join(_DRAFT_DIR, "results", "metrics.json")
OUT_PATH = os.path.join(_DRAFT_DIR, "results", "envelope.json")

# ---------------------------------------------------------------------------
# Windows (§5) — fixed unit-index ranges
# ---------------------------------------------------------------------------
ENVELOPE_RANGE = (1, 47)
REFERENCE_RANGE = (48, 60)
EXTENSION_RANGE = (61, 73)
COMBINED_V2_RANGE = (48, 73)   # §8: marker channel's single combined window
SIM_BLOCK_SIZE = 5

DELTA_THRESHOLD = 0.5
MIN_COMPUTABLE_FOR_DECIDABLE = 2

MARGIN_METRIC_DIRECTIONS = {
    "mtld": "low",
    "hapax_share": "low",
    "top50_mass": "high",
    "similarity": "high",
}
DEC_ANOMALY_RULE = {
    "mtld": "two_consecutive",
    "hapax_share": "two_consecutive",
    "top50_mass": "two_consecutive",
    "similarity": "five_apart",   # §4 Skeptic condition 1 exception
}
SINGLE_CHANNEL_PAIR = frozenset({"hapax_share", "top50_mass"})
FIRING_WORDING = "a documented deviation in our own record whose cause this instrument cannot identify"

BLOCK_INDEX_OF = {idx: (idx - 1) // SIM_BLOCK_SIZE for idx in range(1, 74)}


# ---------------------------------------------------------------------------
# Series extraction from results/metrics.json (frozen input)
# ---------------------------------------------------------------------------

def series_from(units, getter):
    """units: metrics.json['units'] list (index 1..73, in order). Returns
    [(index, value_or_None), ...] in index order."""
    return [(u["index"], getter(u)) for u in units]


DEC_SERIES_GETTERS = {
    "mtld": lambda u: u["prefix600"]["mtld"],
    "hapax_share": lambda u: u["prefix600"]["hapax_share"],
    "top50_mass": lambda u: u["prefix600"]["top50_mass"],
    "similarity": lambda u: u["sim_trailing"]["value"],
}
PROP40_SERIES_GETTERS = {
    "mtld": lambda u: u["prop40"]["mtld"],
    "hapax_share": lambda u: u["prop40"]["hapax_share"],
    "top50_mass": lambda u: u["prop40"]["top50_mass"],
}
SIM_CONTENT_GETTER = lambda u: u["sim_content"]["value"]  # noqa: E731
SIM_BLOCK_GETTER = lambda u: u["sim_block"]["value"]  # noqa: E731


# ---------------------------------------------------------------------------
# Envelope fit (§4) + prediction SE
# ---------------------------------------------------------------------------

def fit_linear(xs, ys):
    a, b, xbar, sxx, ss_res = ols_simple(xs, ys)
    n = len(xs)
    df = n - 2
    s = math.sqrt(ss_res / df)
    return {"degree": 1, "a": a, "b": b, "xbar": xbar, "sxx": sxx, "s": s, "n": n,
            "df": df, "t_crit": t975(df)}


def fit_quadratic(xs, ys):
    coeffs, ss_res, xtx_inv = ols_poly(xs, ys, degree=2)
    n = len(xs)
    df = n - 3
    s = math.sqrt(ss_res / df)
    return {"degree": 2, "coeffs": coeffs, "xtx_inv": xtx_inv, "s": s, "n": n,
            "df": df, "t_crit": t975(df)}


def pred_se(fit, x):
    if fit["degree"] == 1:
        return fit["s"] * math.sqrt(1 + 1.0 / fit["n"] + (x - fit["xbar"]) ** 2 / fit["sxx"])
    return poly_pred_se(fit["s"], fit["xtx_inv"], x, 2)


def predict(fit, x):
    if fit["degree"] == 1:
        return fit["a"] + fit["b"] * x
    return predict_poly(fit["coeffs"], x)


def build_rows(series, fit, direction):
    """direction: 'low' (raw z), 'high' (flip sign), 'excess' (marker channel,
    positive-side rule, never reoriented)."""
    t_crit = fit["t_crit"]
    rows = []
    for idx, v in series:
        if v is None:
            rows.append({"index": idx, "value": None, "yhat": None, "se": None,
                         "z_raw": None, "z": None, "out_of_band": False})
            continue
        yhat = predict(fit, idx)
        se = pred_se(fit, idx)
        # Degenerate-fit guard (never exercised by real corpus data, which is never
        # exactly collinear): a zero-residual fit gives se == 0 at every x. The
        # deviation (v - yhat) is then also exactly 0, so 0/0 is mathematically a
        # "no deviation, no uncertainty" case, not an infinite z; z_raw is defined
        # as 0.0 there rather than raising ZeroDivisionError. See
        # DEVIATIONS-CANDIDATES.md and tests/test_envelope_arithmetic.py.
        z_raw = 0.0 if se == 0.0 else (v - yhat) / se
        if direction == "low":
            z = z_raw
            out = z < -t_crit
        elif direction == "high":
            z = -z_raw
            out = z < -t_crit
        elif direction == "excess":
            z = z_raw
            out = z_raw > t_crit
        else:
            raise ValueError(f"unknown direction {direction!r}")
        rows.append({"index": idx, "value": v, "yhat": yhat, "se": se,
                     "z_raw": z_raw, "z": z, "out_of_band": out})
    return rows


# ---------------------------------------------------------------------------
# Anomaly rule (§4): two consecutive out-of-band units, EXCEPT metric 4
# (similarity), whose two out-of-band units must be >= 5 apart in index.
# ---------------------------------------------------------------------------

def rows_in_range(rows, lo, hi):
    return [r for r in rows if lo <= r["index"] <= hi]


def anomaly_two_consecutive(rows, lo, hi):
    w = rows_in_range(rows, lo, hi)
    w.sort(key=lambda r: r["index"])
    for i in range(len(w) - 1):
        if w[i]["out_of_band"] and w[i + 1]["out_of_band"]:
            return True
    return False


def anomaly_five_apart(rows, lo, hi):
    """§4 Skeptic condition 1, metric 4 only: two out-of-band units at least 5 apart
    in unit index (disjoint document sets), anywhere within the window -- not
    necessarily adjacent."""
    w = [r for r in rows_in_range(rows, lo, hi) if r["out_of_band"]]
    for i in range(len(w)):
        for j in range(i + 1, len(w)):
            if abs(w[j]["index"] - w[i]["index"]) >= 5:
                return True
    return False


def anomaly_two_consecutive_blocks(rows, lo, hi, block_index_of=BLOCK_INDEX_OF):
    """sim_block companion series only (see DEVIATIONS-CANDIDATES.md): the naive
    per-unit two-consecutive rule would trivially fire on any single out-of-band
    block, since up to 5 consecutive units all carry that one block's identical
    value/out_of_band status -- that tests nothing beyond "one block fired", not
    the two-independent-observations logic §3(e) restores disjoint blocks for.
    Collapses to one representative row per distinct block touched by the window,
    then requires two ADJACENT blocks (by block index, no gap) both out-of-band."""
    w = rows_in_range(rows, lo, hi)
    seen = {}
    for r in w:
        b = block_index_of[r["index"]]
        if b not in seen:
            seen[b] = r
    blocks_sorted = sorted(seen.items(), key=lambda kv: kv[0])
    for i in range(len(blocks_sorted) - 1):
        b0, r0 = blocks_sorted[i]
        b1, r1 = blocks_sorted[i + 1]
        if b1 == b0 + 1 and r0["out_of_band"] and r1["out_of_band"]:
            return True
    return False


_ANOMALY_FNS = {
    "two_consecutive": anomaly_two_consecutive,
    "five_apart": anomaly_five_apart,
    "two_consecutive_blocks": anomaly_two_consecutive_blocks,
}


def window_mean_z(rows, lo, hi):
    vals = [r["z"] for r in rows_in_range(rows, lo, hi) if r["value"] is not None]
    return sum(vals) / len(vals) if vals else None


def window_computable_count(rows, lo, hi):
    return sum(1 for r in rows_in_range(rows, lo, hi) if r["value"] is not None)


def window_decidable(rows, lo, hi, min_computable=MIN_COMPUTABLE_FOR_DECIDABLE):
    return window_computable_count(rows, lo, hi) >= min_computable


# ---------------------------------------------------------------------------
# Classification (§6) — fixed-order ladder, first match wins. Unchanged from
# the parent instrument's ladder (018's envelope.py `classify`).
# ---------------------------------------------------------------------------

def classify(a_ref, a_ext, delta):
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


def reverse_sublabel(rows, lo, hi, t_crit):
    w = rows_in_range(rows, lo, hi)
    inside = all(r["z"] is not None and abs(r["z"]) < t_crit for r in w)
    return "FULL" if inside else "PARTIAL"


def metric_report(name, direction, series, fit_lo, fit_hi, anomaly_rule, degree=1):
    fit_points = [(idx, v) for idx, v in series if fit_lo <= idx <= fit_hi and v is not None]
    xs = [p[0] for p in fit_points]
    ys = [p[1] for p in fit_points]
    fit = fit_linear(xs, ys) if degree == 1 else fit_quadratic(xs, ys)
    rows = build_rows(series, fit, direction)
    anomaly_fn = _ANOMALY_FNS[anomaly_rule]

    ref_decidable = window_decidable(rows, *REFERENCE_RANGE)
    ext_decidable = window_decidable(rows, *EXTENSION_RANGE)
    a_ref = anomaly_fn(rows, *REFERENCE_RANGE) if ref_decidable else None
    a_ext = anomaly_fn(rows, *EXTENSION_RANGE) if ext_decidable else None
    delta_ref = window_mean_z(rows, *REFERENCE_RANGE)
    delta_ext = window_mean_z(rows, *EXTENSION_RANGE)
    delta = (delta_ext - delta_ref) if (delta_ref is not None and delta_ext is not None) else None

    if a_ref is None or a_ext is None:
        label = "NON-DECIDABLE"
    else:
        label = classify(a_ref, a_ext, delta)
    sub_label = reverse_sublabel(rows, *EXTENSION_RANGE, fit["t_crit"]) if label == "REVERSE" else None

    fit_public = {
        "n_fit": fit["n"], "df": fit["df"], "t_crit": fit["t_crit"],
        "fit_range": [fit_lo, fit_hi], "degree": degree, "s": fit["s"],
    }
    if degree == 1:
        fit_public.update({"intercept": fit["a"], "slope": fit["b"], "xbar": fit["xbar"], "sxx": fit["sxx"]})
    else:
        fit_public.update({"coeffs": fit["coeffs"]})

    return {
        "metric": name, "direction": direction, "anomaly_rule": anomaly_rule,
        "fit": fit_public, "rows": rows,
        "ref_decidable": ref_decidable, "ext_decidable": ext_decidable,
        "a_ref": a_ref, "a_ext": a_ext,
        "delta_ref": delta_ref, "delta_ext": delta_ext, "delta": delta,
        "label": label, "sub_label": sub_label,
    }


# ---------------------------------------------------------------------------
# §7 verdict — ordered 3-step procedure, first applicable step wins
# ---------------------------------------------------------------------------

def plurality_bucket(labels, eligible_buckets, tie_label, bucket_map):
    all_counts = Counter(labels)
    bucket_counts = Counter()
    for lbl in labels:
        b = bucket_map.get(lbl)
        if b is not None:
            bucket_counts[b] += 1
    eligible = {b: bucket_counts.get(b, 0) for b in eligible_buckets}
    max_count = max(eligible.values()) if eligible else 0
    if max_count == 0:
        return tie_label, dict(bucket_counts), dict(all_counts)
    winners = [b for b, c in eligible.items() if c == max_count]
    if len(winners) == 1:
        return winners[0], dict(bucket_counts), dict(all_counts)
    return tie_label, dict(bucket_counts), dict(all_counts)


BUCKET_MAP = {"CONTINUE": "DECLINE", "NEW-ONSET": "DECLINE", "PLATEAU": "PLATEAU", "REVERSE": "REVERSE"}


def evaluate_verdict(metrics_dict, metric_names):
    """§7's ordered 3-step procedure over one branch's per-metric classification
    dicts. metric_names fixes both the order and the roster (4 for the decisional
    run and every branch except prop40, which has 3 -- see DEVIATIONS-CANDIDATES.md)."""
    ext_decidable = [m for m in metric_names if metrics_dict[m]["ext_decidable"]]
    ext_anomalous = [m for m in ext_decidable if metrics_dict[m]["a_ext"]]

    # Step 1: directional finding.
    if len(ext_anomalous) >= 2:
        single_channel = frozenset(ext_anomalous) == SINGLE_CHANNEL_PAIR
        labels = [metrics_dict[m]["label"] for m in ext_anomalous]
        headline, bucket_counts, all_counts = plurality_bucket(
            labels, ("DECLINE", "PLATEAU"), "MIXED (shrinking)", BUCKET_MAP
        )
        if single_channel:
            headline_state = "SINGLE-CHANNEL"
            verdict = (
                FIRING_WORDING + " -- SINGLE-CHANNEL (§7 pre-committed downgrade): the only "
                "two anomalous metrics are hapax_share and top50_mass, both derived from the "
                "same frequency table and negatively related by construction; not reported as "
                ">=2-of-4 corroboration."
            )
        else:
            headline_state = headline
            verdict = FIRING_WORDING
        return {
            "step": 1, "step_name": "directional_finding",
            "ext_decidable_metrics": ext_decidable, "ext_anomalous_metrics": ext_anomalous,
            "denominator": len(ext_decidable), "single_channel": single_channel,
            "headline_state": headline_state, "headline_bucket_counts": bucket_counts,
            "headline_label_counts": all_counts, "kill_condition_met": False, "verdict": verdict,
        }

    # Step 2: kill condition.
    any_decidable = [m for m in metric_names if metrics_dict[m]["ref_decidable"] or metrics_dict[m]["ext_decidable"]]
    any_anomalous = [m for m in any_decidable
                      if bool(metrics_dict[m]["a_ref"]) or bool(metrics_dict[m]["a_ext"])]
    if len(any_anomalous) <= 1:
        return {
            "step": 2, "step_name": "kill_condition",
            "any_anomaly_decidable_metrics": any_decidable, "any_anomaly_metrics": any_anomalous,
            "denominator": len(any_decidable), "headline_state": "NO SIGNAL",
            "headline_bucket_counts": {}, "headline_label_counts": {}, "kill_condition_met": True,
            "verdict": "NO SIGNAL BEYOND OUR OWN ORDINARY DRIFT",
        }

    # Step 3: plurality over all of this branch's metrics' labels.
    labels = [metrics_dict[m]["label"] for m in metric_names]
    headline, bucket_counts, all_counts = plurality_bucket(
        labels, ("DECLINE", "PLATEAU", "REVERSE"), "MIXED", BUCKET_MAP
    )
    if headline == "REVERSE":
        verdict = "REVERSE -- the documented anomaly did not persist against the envelope."
    elif headline == "MIXED":
        verdict = "MIXED (reported metric-by-metric)"
    else:
        verdict = f"{headline} (step-3 plurality; not a directional finding)"
    return {
        "step": 3, "step_name": "plurality_over_all_metrics", "denominator": len(labels),
        "headline_state": headline, "headline_bucket_counts": bucket_counts,
        "headline_label_counts": all_counts, "kill_condition_met": False, "verdict": verdict,
    }


# ---------------------------------------------------------------------------
# Branch builders
# ---------------------------------------------------------------------------

def build_branch(units, series_getters, anomaly_rules, fit_lo, fit_hi, degree=1):
    metrics_out = {}
    for name, direction in MARGIN_METRIC_DIRECTIONS.items():
        if name not in series_getters:
            continue
        series = series_from(units, series_getters[name])
        metrics_out[name] = metric_report(name, direction, series, fit_lo, fit_hi,
                                           anomaly_rules[name], degree=degree)
    names = [n for n in MARGIN_METRIC_DIRECTIONS if n in metrics_out]
    verdict = evaluate_verdict(metrics_out, names)
    return metrics_out, verdict, names


def similarity_out_of_band_contributors(units, similarity_report):
    """§3(d) partial discriminator: for every out-of-band unit of the DECISIONAL
    similarity metric, the 5 tokens contributing most to that window's summed
    cosine and their share of the total (already computed by stage 1, carried
    through unchanged from metrics.json's sim_trailing.top_contributors)."""
    by_idx = {u["index"]: u for u in units}
    out = []
    for row in similarity_report["rows"]:
        if row["out_of_band"]:
            u = by_idx[row["index"]]
            out.append({
                "index": row["index"], "z": row["z"],
                "window_indices": u["sim_trailing"]["window_indices"],
                "top_contributors": u["sim_trailing"]["top_contributors"],
            })
    return out


def build_marker_channel(units):
    """§8: marker channel envelope fitted on units 1-47, raw (UNreoriented) z,
    excess-direction rule (z > +t), evaluated over the COMBINED v2-era window
    48-73 (not split into ref/ext) -- never enters §7's counts."""
    series = series_from(units, lambda u: u["prefix600"]["marker_rate_per_1000"])
    context_series = series_from(units, lambda u: u["whole_unit"]["marker_rate_per_1000"])

    fit_points = [(idx, v) for idx, v in series if ENVELOPE_RANGE[0] <= idx <= ENVELOPE_RANGE[1] and v is not None]
    xs = [p[0] for p in fit_points]
    ys = [p[1] for p in fit_points]
    fit = fit_linear(xs, ys)
    rows = build_rows(series, fit, "excess")

    a_combined = anomaly_two_consecutive(rows, *COMBINED_V2_RANGE)
    delta_combined = window_mean_z(rows, *COMBINED_V2_RANGE)
    combined_decidable = window_decidable(rows, *COMBINED_V2_RANGE)

    ext_vals = [v for idx, v in series if EXTENSION_RANGE[0] <= idx <= EXTENSION_RANGE[1] and v is not None]
    ref_vals = [v for idx, v in series if REFERENCE_RANGE[0] <= idx <= REFERENCE_RANGE[1] and v is not None]
    env_vals = ys

    return {
        "metric": "marker_rate_per_1000_prefix600", "direction": "excess",
        "fit": {"n_fit": fit["n"], "df": fit["df"], "t_crit": fit["t_crit"],
                "fit_range": list(ENVELOPE_RANGE), "intercept": fit["a"], "slope": fit["b"],
                "xbar": fit["xbar"], "sxx": fit["sxx"], "s": fit["s"]},
        "rows": rows,
        "combined_window_v2_48_73": {
            "decidable": combined_decidable, "anomaly": a_combined if combined_decidable else None,
            "delta_mean_z": delta_combined,
        },
        "note": "Never enters §7's counts (§8). Excess-direction rule only (z > +t), not the collapse-side rule.",
        "levels": {
            "envelope_era_mean": sum(env_vals) / len(env_vals) if env_vals else None,
            "envelope_era_range": [min(env_vals), max(env_vals)] if env_vals else None,
            "reference_mean": sum(ref_vals) / len(ref_vals) if ref_vals else None,
            "extension_mean": sum(ext_vals) / len(ext_vals) if ext_vals else None,
            "extension_range": [min(ext_vals), max(ext_vals)] if ext_vals else None,
        },
        "context_whole_cell_rate": {
            "note": "Context only, never fed to an envelope.",
            "rows": [{"index": idx, "value": v} for idx, v in context_series],
        },
        "cross_genre_comparison_declared_invalid": {
            "note": (
                "§8: validity conditions for this comparison do not hold (the marker list is "
                "an excess-vocabulary list derived from a different genre/register/length "
                "regime). Reported as a level comparison only, no causal or attributional claim."
            ),
            "parent_instrument_published_levels_per_1000": {
                "cs.CL_baseline_to_2024H2": [50, 56, 95.1],
                "math.NT_control_flat": [27, 34],
            },
        },
    }


def zipf_diagnostic(units):
    """§3: the Zipf-tail slope's degeneracy at document scale, reported as a
    DIAGNOSTIC of the parent instrument's transferability. No verdict."""
    env = [u for u in units if ENVELOPE_RANGE[0] <= u["index"] <= ENVELOPE_RANGE[1]]
    values = []
    zero_count = 0
    noncomp_count = 0
    prefix_computable_count = 0
    for u in env:
        p = u["prefix600"]
        computable = p["computable"]
        slope = p["zipf_slope"]
        noncomp = p["zipf_non_computable"]
        values.append({"index": u["index"], "prefix600_computable": computable,
                       "zipf_slope": slope, "zipf_non_computable": noncomp})
        if computable:
            prefix_computable_count += 1
            if noncomp:
                noncomp_count += 1
            elif slope == 0.0:
                zero_count += 1
    return {
        "window": list(ENVELOPE_RANGE),
        "n_prefix600_computable": prefix_computable_count,
        "n_exactly_zero": zero_count,
        "n_non_computable": noncomp_count,
        "n_degenerate_total": zero_count + noncomp_count,
        "values": values,
    }


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def build_results(units):
    dec_metrics, dec_verdict, dec_names = build_branch(
        units, DEC_SERIES_GETTERS, DEC_ANOMALY_RULE, *ENVELOPE_RANGE, degree=1
    )
    sim_contributors = similarity_out_of_band_contributors(units, dec_metrics["similarity"])

    quad_metrics, quad_verdict, _ = build_branch(
        units, DEC_SERIES_GETTERS, DEC_ANOMALY_RULE, *ENVELOPE_RANGE, degree=2
    )

    transient_metrics, transient_verdict, _ = build_branch(
        units, DEC_SERIES_GETTERS, DEC_ANOMALY_RULE, 10, 47, degree=1
    )

    prop40_metrics, prop40_verdict, _ = build_branch(
        units, PROP40_SERIES_GETTERS,
        {"mtld": "two_consecutive", "hapax_share": "two_consecutive", "top50_mass": "two_consecutive"},
        *ENVELOPE_RANGE, degree=1
    )

    simcontent_getters = dict(DEC_SERIES_GETTERS)
    simcontent_getters["similarity"] = SIM_CONTENT_GETTER
    simcontent_metrics, simcontent_verdict, _ = build_branch(
        units, simcontent_getters, DEC_ANOMALY_RULE, *ENVELOPE_RANGE, degree=1
    )

    simblock_getters = dict(DEC_SERIES_GETTERS)
    simblock_getters["similarity"] = SIM_BLOCK_GETTER
    simblock_rules = dict(DEC_ANOMALY_RULE)
    simblock_rules["similarity"] = "two_consecutive_blocks"
    simblock_metrics, simblock_verdict, _ = build_branch(
        units, simblock_getters, simblock_rules, *ENVELOPE_RANGE, degree=1
    )

    marker = build_marker_channel(units)
    zipf_diag = zipf_diagnostic(units)

    def disagrees(v):
        return dec_verdict["headline_state"] != v["headline_state"]

    out = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "windows": {
            "envelope": list(ENVELOPE_RANGE), "reference": list(REFERENCE_RANGE),
            "extension": list(EXTENSION_RANGE), "combined_v2": list(COMBINED_V2_RANGE),
        },
        "constants": {
            "delta_threshold": DELTA_THRESHOLD,
            "min_computable_for_decidable": MIN_COMPUTABLE_FOR_DECIDABLE,
        },
        "decisional": {
            "note": "All-units linear prefix600 fit with sim_trailing -- THE decisional run (§4/§5).",
            "metrics": dec_metrics, "verdict": dec_verdict,
            "similarity_top_contributor_concentration_partial_discriminator": sim_contributors,
        },
        "marker_channel": marker,
        "zipf_tail_diagnostic": zipf_diag,
        "branches": {
            "quadratic_curvature": {
                "note": "§4 curvature check, t(0.975, n_fit-3). Decisional per §4's soft-downgrade rule if disagreeing.",
                "metrics": quad_metrics, "verdict": quad_verdict,
                "disagrees_with_decisional_headline": disagrees(quad_verdict),
            },
            "founding_transient_10_47": {
                "note": "§4 founding-transient branch: envelope fit restricted to computable units 10-47.",
                "metrics": transient_metrics, "verdict": transient_verdict,
                "disagrees_with_decisional_headline": disagrees(transient_verdict),
            },
            "prop40_fixed_proportion": {
                "note": (
                    "§3 fixed-proportion (first 40%) companion series. Only mtld/hapax_share/"
                    "top50_mass -- metrics.json's prop40 block has no similarity series (stage 1 "
                    "did not compute one; see DEVIATIONS-CANDIDATES.md). 3-metric roster."
                ),
                "metrics": prop40_metrics, "verdict": prop40_verdict,
                "disagrees_with_decisional_headline": disagrees(prop40_verdict),
            },
            "sim_content_companion": {
                "note": "§3(d) content-word-only companion series (200 most frequent envelope-pool types removed).",
                "metrics": simcontent_metrics, "verdict": simcontent_verdict,
                "disagrees_with_decisional_headline": disagrees(simcontent_verdict),
            },
            "sim_block_companion": {
                "note": (
                    "§3(e) disjoint-block companion series. Anomaly rule operationalized at "
                    "block granularity (two adjacent out-of-band BLOCKS, not units) -- see "
                    "DEVIATIONS-CANDIDATES.md for why the naive per-unit rule would be vacuous here."
                ),
                "metrics": simblock_metrics, "verdict": simblock_verdict,
                "disagrees_with_decisional_headline": disagrees(simblock_verdict),
            },
        },
        "soft_downgrade_unresolved": disagrees(quad_verdict),
    }
    return out


def main():
    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        metrics = json.load(f)
    units = metrics["units"]
    assert len(units) == 73, f"expected 73 units, got {len(units)}"

    out = build_results(units)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=False, ensure_ascii=False)
    print(f"wrote {OUT_PATH}")
    print(f"decisional headline_state: {out['decisional']['verdict']['headline_state']}")


if __name__ == "__main__":
    main()
