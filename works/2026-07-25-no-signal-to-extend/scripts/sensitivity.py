#!/usr/bin/env python3
"""Operating characteristic of the locked decision rule: what could this null have excluded?

A negative result is only worth its weight if the instrument could have seen the effect had it
been there. This script derives that from the frozen run alone -- it introduces no new data, no
new measurement and no new threshold. It reads the same prediction-interval standard errors the
decision rule already used and states, per (stratum, metric), the smallest collapse-direction
deviation from the fitted ordinary-drift trend that would have put a unit out of band:

    MDE(unit) = t_crit * se(unit)          [in the metric's own units]

and the same figure as a percentage of that unit's fitted trend value. The rule additionally
requires TWO CONSECUTIVE out-of-band units inside a window, so the reported figure is the
per-unit floor, not the full requirement -- a deviation smaller than this is invisible to the
instrument by construction, and one at this size is detected only if it persists.

The second half of this module (POWER CURVE, below) goes one step further: it actually injects a
synthetic collapse-direction shift into the extension window and re-runs the locked rule, rather
than just comparing a floor against SE. See its own docstring for why that injection is
legitimate -- in short, the envelope is fit on 2015H1-2022H2 only, and injection never touches
those 16 units, so the fitted trend line is byte-for-byte the frozen one.

Usage:
  python3 scripts/sensitivity.py --results results/results.json --out results/sensitivity.json
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from envelope import (  # noqa: E402
    ALL_STRATA,
    MARGIN_METRIC_DIRECTIONS,
    anomaly_in_window,
    build_metric_table,
)
from envelope import EXTENSION_UNITS as ENVELOPE_EXTENSION_UNITS  # noqa: E402

EXTENSION_UNITS = ENVELOPE_EXTENSION_UNITS  # ("2025H1", "2025H2", "2026H1") -- single source


def mde_rows(results, units=EXTENSION_UNITS):
    """Per (stratum, metric, unit): the smallest detectable collapse-direction deviation."""
    t_crit = results["constants"]["t_crit_linear_df14"]
    rows = []
    for stratum, block in results["strata"].items():
        for metric, payload in block["metrics"].items():
            by_unit = {r["unit"]: r for r in payload["rows"]}
            for unit in units:
                row = by_unit[unit]
                mde = t_crit * row["se"]
                rows.append({
                    "stratum": stratum,
                    "metric": metric,
                    "unit": unit,
                    "collapse_direction": payload["direction"],
                    "yhat": row["yhat"],
                    "se": row["se"],
                    "mde_absolute": mde,
                    "mde_percent_of_trend": (100.0 * mde / abs(row["yhat"])) if row["yhat"] else None,
                    "observed_z": row["z"],
                })
    return rows


def summarize(rows):
    """The headline range per stratum, over the extension window."""
    out = {}
    for row in rows:
        bucket = out.setdefault(row["stratum"], {"min_percent": None, "max_percent": None, "metrics": {}})
        pct = row["mde_percent_of_trend"]
        if pct is None:
            continue
        if bucket["min_percent"] is None or pct < bucket["min_percent"]:
            bucket["min_percent"] = pct
        if bucket["max_percent"] is None or pct > bucket["max_percent"]:
            bucket["max_percent"] = pct
        bucket["metrics"].setdefault(row["metric"], []).append(pct)
    return out


# ---------------------------------------------------------------------------
# POWER CURVE: synthetic-injection operating characteristic (Skeptic's objection)
# ---------------------------------------------------------------------------
#
# "A clean read from an instrument never shown capable of ringing the bell is not
# distinguishable from a bell that cannot ring." The MDE floor above answers a weaker
# question (how big would ONE unit's deviation need to be to leave the band); this
# answers the Skeptic's actual question: inject a real effect and see whether the
# LOCKED RULE -- the same two-consecutive-out-of-band test that produced the shipped
# verdict -- actually fires.
#
# Why the injection is legitimate: the ordinary-drift envelope (fit, yhat, se) is
# fit exclusively on the 16 ENVELOPE units, 2015H1-2022H2 (envelope.ENVELOPE_UNITS).
# The injection below only ever rewrites the three EXTENSION units, 2025H1/2025H2/
# 2026H1 -- units 16 positions past the end of the fitting window. Feeding the
# (partially rewritten) 23-unit series back through envelope.build_metric_table()
# therefore refits from the SAME untouched 16 envelope points every time; the
# resulting fit, yhat and se are byte-identical to the frozen run's own. Nothing
# about "how sensitive could this instrument have been" is begged by also moving
# the goalposts -- the goalposts (the fitted trend line) never move.
#
# Sign convention: a naive `value * (1 - d)` rescaling is wrong for two of the four
# metrics -- zipf_slope's fitted trend is negative (~-0.9), where multiplying by
# (1 - d) makes the value LESS negative (an improvement, not a collapse), and
# similarity's collapse direction is "high" (more similar = more homogeneous), where
# a shrinking multiplier moves it the wrong way entirely. Instead the shift is
# additive, sized off the fitted trend's magnitude, and signed against the metric's
# OWN collapse direction (the same direction envelope.MARGIN_METRIC_DIRECTIONS
# already declares and envelope.build_metric_table() already reorients around):
#
#     direction == "low"  (mtld, hapax_share, zipf_slope): value_injected = value - d*|yhat|
#     direction == "high" (similarity):                    value_injected = value + d*|yhat|
#
# Recomputation of the standardized deviation and the out-of-band test is NOT
# reimplemented here -- both calls below (build_metric_table, anomaly_in_window) are
# imported straight from envelope.py, the same functions the locked rule itself
# uses. This module only builds the injected input series and reads the boolean
# results back out; the reorientation arithmetic and the two-consecutive-out-of-band
# rule lived entirely inside envelope.py already and decompose cleanly for reuse.

INJECTION_GRID_STEP = 0.005   # 0.5%
INJECTION_GRID_MAX = 0.30     # 30%
INJECTION_UNITS = EXTENSION_UNITS  # the "sustained" shift is applied to all three


def injection_grid(step=INJECTION_GRID_STEP, dmax=INJECTION_GRID_MAX):
    """d = 0.005, 0.010, ..., 0.30 (60 points), each a fraction of the fitted trend
    level. Rounded to avoid float-accumulation drift across the grid."""
    n = round(dmax / step)
    return [round((i + 1) * step, 10) for i in range(n)]


def inject_unit_values(unit_values, direction, d, yhat_by_unit, injection_units=INJECTION_UNITS):
    """Shift only the extension-window entries of `unit_values` (a list of
    (unit, x, value) triples covering all 23 units, in order) by a sustained
    collapse-direction amount d*|yhat|. Envelope-window and reference-window
    entries pass through unchanged -- see module docstring for why that keeps the
    refit identical to the frozen fit. `yhat_by_unit` supplies each extension
    unit's FROZEN fitted trend value (itself unaffected by the injection, since it
    depends only on x and the untouched envelope fit)."""
    out = []
    for unit, x, value in unit_values:
        if unit in injection_units and value is not None:
            yhat = yhat_by_unit[unit]
            if direction == "low":
                value = value - d * abs(yhat)
            elif direction == "high":
                value = value + d * abs(yhat)
            else:
                raise ValueError(f"unsupported margin-metric collapse direction: {direction!r}")
        out.append((unit, x, value))
    return out


def fires_at(unit_values, direction, d, yhat_by_unit):
    """True iff injecting a sustained shift of size d fires the locked rule's
    two-consecutive-out-of-band requirement inside the extension window --
    computed entirely by envelope.py's own build_metric_table/anomaly_in_window,
    not reimplemented here."""
    injected = inject_unit_values(unit_values, direction, d, yhat_by_unit)
    _, rows = build_metric_table(injected, direction)
    return anomaly_in_window(rows, EXTENSION_UNITS)


def power_curve_for_metric(unit_values, direction, yhat_by_unit, grid):
    """Per-d firing booleans (aligned to `grid`) and the smallest d in the grid at
    which the locked rule fires in the extension window. None if it never fires
    anywhere on the grid -- reported as-is, not smoothed over."""
    fires_by_d = [fires_at(unit_values, direction, d, yhat_by_unit) for d in grid]
    smallest = next((d for d, fires in zip(grid, fires_by_d) if fires), None)
    return fires_by_d, smallest


def power_curve_for_stratum(stratum_block, grid):
    """Per-metric power curves for one stratum, plus the smallest d at which at
    least 2 of the 4 margin metrics fire simultaneously (all four injected at the
    SAME d) -- the pre-registered §7 threshold for a directional finding."""
    metrics_out = {}
    fire_count_by_d = [0] * len(grid)
    for metric, direction in MARGIN_METRIC_DIRECTIONS.items():
        rows = stratum_block["metrics"][metric]["rows"]
        unit_values = [(r["unit"], r["x"], r["value"]) for r in rows]
        yhat_by_unit = {r["unit"]: r["yhat"] for r in rows}
        fires_by_d, smallest = power_curve_for_metric(unit_values, direction, yhat_by_unit, grid)
        # Diagnostic only (not used by fires_at itself): the FROZEN, un-injected
        # reoriented z at each extension unit. A metric that sits well on the
        # anti-collapse side already (large positive z) needs a much bigger d
        # before an injected collapse-direction shift even reaches the trend
        # line, let alone the band -- this is what makes mtld's grid-relative
        # insensitivity legible instead of looking like a bug.
        baseline_z = [r["z"] for r in rows if r["unit"] in INJECTION_UNITS]
        metrics_out[metric] = {
            "direction": direction,
            "smallest_firing_d": smallest,
            "fires_by_d": fires_by_d,
            "baseline_z_extension_units": baseline_z,
        }
        for i, fires in enumerate(fires_by_d):
            if fires:
                fire_count_by_d[i] += 1

    smallest_two_of_four = next(
        (d for d, count in zip(grid, fire_count_by_d) if count >= 2), None
    )
    return {
        "metrics": metrics_out,
        "fire_count_by_d": fire_count_by_d,
        "smallest_d_two_of_four_metrics": smallest_two_of_four,
    }


def power_curve(results, strata=ALL_STRATA):
    grid = injection_grid()
    strata_out = {}
    for stratum in strata:
        strata_out[stratum] = power_curve_for_stratum(results["strata"][stratum], grid)
    return {
        "note": (
            "Synthetic collapse-direction injection into the three extension units "
            "(2025H1, 2025H2, 2026H1) only -- the envelope is fit on 2015H1-2022H2 "
            "exclusively, so injection never disturbs that fit; the refit reproduces "
            "the frozen envelope byte-for-byte. Shift is additive and signed against "
            "each metric's own collapse direction (value - d*|yhat| when direction is "
            "'low', value + d*|yhat| when direction is 'high'), never a naive "
            "multiplicative rescale, which moves zipf_slope (negative-valued trend) "
            "and similarity ('high' collapse direction) the wrong way. Standardized "
            "deviation and the out-of-band test are computed by envelope.py's own "
            "build_metric_table()/anomaly_in_window() -- not reimplemented here."
        ),
        "injection_units": list(INJECTION_UNITS),
        "grid_d": grid,
        "grid_step": INJECTION_GRID_STEP,
        "grid_max": INJECTION_GRID_MAX,
        "strata": strata_out,
    }


def power_curve_headline(power_curve_payload):
    """Compact per-stratum headline: smallest d for the >=2-of-4 directional-finding
    threshold, and the per-metric [min, max] smallest-firing-d range (skipping any
    metric that never fires on the grid)."""
    out = {}
    for stratum, block in power_curve_payload["strata"].items():
        firing = [
            m["smallest_firing_d"] for m in block["metrics"].values()
            if m["smallest_firing_d"] is not None
        ]
        never_fired = sorted(
            metric for metric, m in block["metrics"].items() if m["smallest_firing_d"] is None
        )
        out[stratum] = {
            "smallest_d_two_of_four_metrics": block["smallest_d_two_of_four_metrics"],
            "per_metric_smallest_firing_d_range": [min(firing), max(firing)] if firing else None,
            "metrics_never_firing_on_grid": never_fired,
        }
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description="Minimum detectable effect of the locked rule.")
    parser.add_argument("--results", default="results/results.json")
    parser.add_argument("--out", default="results/sensitivity.json")
    args = parser.parse_args(argv)

    with open(args.results, encoding="utf-8") as handle:
        results = json.load(handle)

    rows = mde_rows(results)
    pc = power_curve(results)
    payload = {
        "note": (
            "Derived from the frozen run's own prediction intervals; no new data, no new "
            "threshold. Per-unit floor only -- the locked rule also requires two consecutive "
            "out-of-band units in a window."
        ),
        "t_crit": results["constants"]["t_crit_linear_df14"],
        "extension_units": list(EXTENSION_UNITS),
        "rows": rows,
        "summary_percent_of_trend": summarize(rows),
        "power_curve": pc,
        "power_curve_headline": power_curve_headline(pc),
    }
    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
    print(json.dumps(payload["summary_percent_of_trend"], indent=2, sort_keys=True))
    print(json.dumps(payload["power_curve_headline"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
