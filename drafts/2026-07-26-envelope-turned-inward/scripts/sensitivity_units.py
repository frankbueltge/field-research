"""
scripts/sensitivity_units.py — PREREGISTRATION.md §9: sensitivity and power.

Two required outputs, both non-decisional:

1. MDE per decisional metric per decision unit (61-73): the raw-units deviation from the
   REAL fitted trend needed to reach z = -t at that unit, using the REAL envelope fit
   (units 1-47, computed exactly as in `envelope_units.py`).

2. The synthetic-injection power curve (§9.2/§9.3/§9.4): for each grid p and each of the
   two donor recipes, every decision unit's (61-73) real 600-token prefix is homogenized
   by replacing a fraction p of its token POSITIONS with donor tokens, the four decisional
   metrics are recomputed on the injected prefixes, and the UNCHANGED envelope/verdict
   machinery (`envelope_units.py`'s fit, anomaly rules, classification ladder and §7
   verdict) is re-run -- with the envelope fit itself left untouched, since it is fitted
   only on the real, uninjected envelope-era units (1-47), which injection never reaches.

Injection mechanics, exactly as implemented (§9.2's text leaves some choices open; every
one made here is recorded so the run is reproducible from this docstring alone):

  - For a given (unit, p, recipe): `positions = list(range(600))` (already sorted),
    shuffled ONCE by `random.Random(f"20260726:inject:{unit}:{p}:{recipe}")`, then the
    first `round(p * 600)` entries of that shuffled list are the replaced positions --
    NOTE every grid value of p * 600 is already an exact integer (30, 60, ..., 300), so
    `round()` is never actually invoked on a fraction; it is used only as a documented
    safety net.
  - Donor list per recipe: recipe A = the 50 most frequent envelope-pool types (rank
    1-50); recipe B = envelope-pool types at ranks 51-150. Each recipe's donor list is
    shuffled ONCE, with its own fixed seed `random.Random(f"20260726:donors:{recipe}")`
    (independent of unit and p, so the same shuffled donor ORDER is reused for every
    unit/p under that recipe).
  - For a given (unit, p, recipe), the replaced positions (in the order they occur in
    the shuffled positions list, i.e. NOT re-sorted back to index order) are assigned
    consecutive tokens from a FRESH `itertools.cycle` over that recipe's shuffled donor
    list, restarting at the front of the donor list for every unit -- so a single unit's
    injected prefix is fully determined by (unit, p, recipe) alone, independent of
    whether other units are also being injected in the same run (required for the
    determinism test in `tests/`).
  - All 13 decision units (61-73) are injected SIMULTANEOUSLY for a given (p, recipe):
    this is the "homogenize the whole extension window under this p" reading of §9.2,
    consistent with it being a positive control for the battery's power, not a
    single-unit perturbation study.
  - The injected similarity metric's trailing window for decision unit x mixes the
    injected prefix of x (and of any other decision unit inside x's window) with the
    REAL prefixes of non-decision units in that window -- stated here and in the output
    per the task's explicit note; this is intended, not a bug.
  - Reference window (48-60) is never injected. Only the extension window's own anomaly
    rule (a_ext) and Delta_ext can change; a_ref/Delta_ref/ref_decidable are carried over
    unchanged from the real decisional run.
"""
import itertools
import json
import os
import random
import sys
from datetime import datetime, timezone

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_DRAFT_DIR = os.path.dirname(_SCRIPT_DIR)
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

import envelope_units as eu  # noqa: E402
import metrics_units as mu  # noqa: E402
from pools import load_pool  # noqa: E402

METRICS_PATH = os.path.join(_DRAFT_DIR, "results", "metrics.json")
UNITS_PATH = os.path.join(_DRAFT_DIR, "provenance", "units.jsonl")
OUT_PATH = os.path.join(_DRAFT_DIR, "results", "sensitivity.json")

P_GRID = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]
PREFIX_LEN = 600
RECIPES = ("A", "B")
INFORMATIVENESS_BAR_P = 0.20


# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------

def load_units_jsonl(path=UNITS_PATH):
    units = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                units.append(json.loads(line))
    return units


def real_prefix600_map(units_jsonl):
    return {u["index"]: u["tokens"][:PREFIX_LEN] for u in units_jsonl if u["n_tokens"] >= PREFIX_LEN}


# ---------------------------------------------------------------------------
# Donor recipes (§9.2)
# ---------------------------------------------------------------------------

def donor_list_for_recipe(pool, recipe):
    if recipe == "A":
        raw = [tok for tok, _count in pool.top_types(50)]
    elif recipe == "B":
        raw = [tok for tok, _count in pool.rank_slice(51, 150)]
    else:
        raise ValueError(recipe)
    rng = random.Random(f"20260726:donors:{recipe}")
    donors = list(raw)
    rng.shuffle(donors)
    return donors


def inject_prefix(prefix_tokens, unit_index, p, recipe, donor_list):
    """Deterministic from (unit_index, p, recipe, donor_list) alone -- see module
    docstring for the exact mechanics."""
    n = len(prefix_tokens)
    positions = list(range(n))
    positions.sort()
    rng = random.Random(f"20260726:inject:{unit_index}:{p}:{recipe}")
    rng.shuffle(positions)
    n_replace = round(p * n)
    selected = positions[:n_replace]
    injected = list(prefix_tokens)
    donor_cycle = itertools.cycle(donor_list)
    for pos in selected:
        injected[pos] = next(donor_cycle)
    return injected, sorted(selected)


# ---------------------------------------------------------------------------
# MDE (§9.1)
# ---------------------------------------------------------------------------

def compute_mde(units_metrics):
    """MDE per decisional metric per decision unit, using the REAL envelope fit."""
    out = {}
    for name, direction in eu.MARGIN_METRIC_DIRECTIONS.items():
        series = eu.series_from(units_metrics, eu.DEC_SERIES_GETTERS[name])
        fit_points = [(idx, v) for idx, v in series
                      if eu.ENVELOPE_RANGE[0] <= idx <= eu.ENVELOPE_RANGE[1] and v is not None]
        xs = [p[0] for p in fit_points]
        ys = [p[1] for p in fit_points]
        fit = eu.fit_linear(xs, ys)
        t_crit = fit["t_crit"]

        per_unit = []
        magnitudes = []
        for idx in range(eu.EXTENSION_RANGE[0], eu.EXTENSION_RANGE[1] + 1):
            se = eu.pred_se(fit, idx)
            magnitude = t_crit * se
            if direction == "low":
                required_direction = "decrease"
                required_raw_delta = -magnitude
            else:
                required_direction = "increase"
                required_raw_delta = magnitude
            per_unit.append({
                "index": idx, "se": se, "mde_magnitude": magnitude,
                "required_direction": required_direction, "required_raw_delta": required_raw_delta,
            })
            magnitudes.append(magnitude)
        out[name] = {
            "direction": direction, "t_crit": t_crit, "n_fit": fit["n"], "df": fit["df"],
            "per_unit": per_unit, "range": [min(magnitudes), max(magnitudes)],
        }
    return out


# ---------------------------------------------------------------------------
# Injected re-run of the decisional machinery (§9.2/§9.3)
# ---------------------------------------------------------------------------

def real_decisional_state(units_metrics):
    """Real (uninjected) fits + real a_ref/delta_ref/ref_decidable per metric, computed
    identically to envelope_units.py's decisional run."""
    state = {}
    for name, direction in eu.MARGIN_METRIC_DIRECTIONS.items():
        series = eu.series_from(units_metrics, eu.DEC_SERIES_GETTERS[name])
        fit_points = [(idx, v) for idx, v in series
                      if eu.ENVELOPE_RANGE[0] <= idx <= eu.ENVELOPE_RANGE[1] and v is not None]
        xs = [p[0] for p in fit_points]
        ys = [p[1] for p in fit_points]
        fit = eu.fit_linear(xs, ys)
        real_rows = eu.build_rows(series, fit, direction)
        ref_decidable = eu.window_decidable(real_rows, *eu.REFERENCE_RANGE)
        anomaly_fn = eu._ANOMALY_FNS[eu.DEC_ANOMALY_RULE[name]]
        a_ref = anomaly_fn(real_rows, *eu.REFERENCE_RANGE) if ref_decidable else None
        delta_ref = eu.window_mean_z(real_rows, *eu.REFERENCE_RANGE)
        state[name] = {
            "direction": direction, "fit": fit, "anomaly_fn": anomaly_fn,
            "ref_decidable": ref_decidable, "a_ref": a_ref, "delta_ref": delta_ref,
        }
    return state


def build_injected_docs(units_metrics, units_jsonl, p, recipe, donor_list):
    """Returns {index: injected_token_list} for units 61-73 only."""
    prefix_map = real_prefix600_map(units_jsonl)
    injected = {}
    for idx in range(eu.EXTENSION_RANGE[0], eu.EXTENSION_RANGE[1] + 1):
        tokens, _positions = inject_prefix(prefix_map[idx], idx, p, recipe, donor_list)
        injected[idx] = tokens
    return injected


def recompute_decision_unit_values(units_metrics, units_jsonl, injected_docs):
    """Recomputes the four decisional metrics at each decision unit (61-73) from the
    injected prefixes. Non-mtld/hapax/top50 metric (similarity) needs the REAL prefixes
    of the non-decision-unit window members, per the sim_trailing.window_indices already
    recorded in metrics.json (window structure itself never changes -- only token
    content of decision-unit members does)."""
    by_index = {u["index"]: u for u in units_metrics}
    real_prefix_map = real_prefix600_map(units_jsonl)

    new_values = {name: {} for name in eu.MARGIN_METRIC_DIRECTIONS}
    for idx in range(eu.EXTENSION_RANGE[0], eu.EXTENSION_RANGE[1] + 1):
        tokens = injected_docs[idx]
        new_values["mtld"][idx] = mu.mtld_bidirectional(tokens, threshold=mu.MTLD_THRESHOLD)
        new_values["hapax_share"][idx] = mu.parent_hapax_share(tokens)
        new_values["top50_mass"][idx] = mu.top50_frequency_mass(tokens)["mass"]

        window_indices = by_index[idx]["sim_trailing"]["window_indices"]
        docs = {}
        for wi in window_indices:
            docs[wi] = injected_docs[wi] if wi in injected_docs else real_prefix_map[wi]
        value, _contrib, _total = mu.window_similarity(window_indices, docs)
        new_values["similarity"][idx] = value
    return new_values


def evaluate_injected_run(units_metrics, real_state, new_values):
    """Re-runs the UNCHANGED envelope/verdict machinery on the injected decision-unit
    values: real fit, real a_ref/delta_ref, recomputed a_ext/delta_ext/label/verdict."""
    metrics_dict = {}
    per_metric_out_of_band = {}
    for name, direction in eu.MARGIN_METRIC_DIRECTIONS.items():
        rs = real_state[name]
        fit = rs["fit"]
        t_crit = fit["t_crit"]
        ext_rows = []
        for idx in range(eu.EXTENSION_RANGE[0], eu.EXTENSION_RANGE[1] + 1):
            v = new_values[name][idx]
            yhat = eu.predict(fit, idx)
            se = eu.pred_se(fit, idx)
            z_raw = (v - yhat) / se
            if direction == "low":
                z = z_raw
            else:
                z = -z_raw
            out = z < -t_crit
            ext_rows.append({"index": idx, "value": v, "z_raw": z_raw, "z": z, "out_of_band": out})

        ext_decidable = True  # all 13 decision units are computable by construction
        a_ext = rs["anomaly_fn"](ext_rows, *eu.EXTENSION_RANGE)
        delta_ext = sum(r["z"] for r in ext_rows) / len(ext_rows)
        a_ref = rs["a_ref"]
        delta_ref = rs["delta_ref"]
        delta = (delta_ext - delta_ref) if delta_ref is not None else None
        if a_ref is None or a_ext is None:
            label = "NON-DECIDABLE"
        else:
            label = eu.classify(a_ref, a_ext, delta)

        metrics_dict[name] = {
            "ref_decidable": rs["ref_decidable"], "ext_decidable": ext_decidable,
            "a_ref": a_ref, "a_ext": a_ext, "delta_ref": delta_ref, "delta_ext": delta_ext,
            "delta": delta, "label": label,
        }
        per_metric_out_of_band[name] = {
            "any_out_of_band": any(r["out_of_band"] for r in ext_rows),
            "out_of_band_units": [r["index"] for r in ext_rows if r["out_of_band"]],
            "a_ext": a_ext,
        }

    verdict = eu.evaluate_verdict(metrics_dict, list(eu.MARGIN_METRIC_DIRECTIONS.keys()))
    return metrics_dict, verdict, per_metric_out_of_band


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def build_power_curve(units_metrics, units_jsonl, pool):
    real_state = real_decisional_state(units_metrics)
    curve = {}
    firing_summary = {}
    for recipe in RECIPES:
        donor_list = donor_list_for_recipe(pool, recipe)
        curve[recipe] = {}
        battery_fires_at_p = None
        first_out_of_band_p = {name: None for name in eu.MARGIN_METRIC_DIRECTIONS}
        first_own_anomaly_p = {name: None for name in eu.MARGIN_METRIC_DIRECTIONS}
        for p in P_GRID:
            injected_docs = build_injected_docs(units_metrics, units_jsonl, p, recipe, donor_list)
            new_values = recompute_decision_unit_values(units_metrics, units_jsonl, injected_docs)
            metrics_dict, verdict, per_metric = evaluate_injected_run(units_metrics, real_state, new_values)
            curve[recipe][p] = {"metrics": metrics_dict, "verdict": verdict, "per_metric_out_of_band": per_metric}

            if battery_fires_at_p is None and verdict["step"] == 1:
                battery_fires_at_p = p
            for name in eu.MARGIN_METRIC_DIRECTIONS:
                if first_out_of_band_p[name] is None and per_metric[name]["any_out_of_band"]:
                    first_out_of_band_p[name] = p
                if first_own_anomaly_p[name] is None and per_metric[name]["a_ext"]:
                    first_own_anomaly_p[name] = p

        firing_summary[recipe] = {
            "battery_fires_at_p": battery_fires_at_p,
            "per_metric_first_out_of_band_p": first_out_of_band_p,
            "per_metric_first_own_anomaly_p": first_own_anomaly_p,
        }
    return curve, firing_summary


def structurally_blind_metrics(firing_summary):
    blind = []
    for name in eu.MARGIN_METRIC_DIRECTIONS:
        never = all(firing_summary[r]["per_metric_first_out_of_band_p"][name] is None for r in RECIPES)
        if never:
            blind.append(name)
    return blind


def informativeness_label(firing_summary):
    fires_le_bar = any(
        firing_summary[r]["battery_fires_at_p"] is not None
        and firing_summary[r]["battery_fires_at_p"] <= INFORMATIVENESS_BAR_P
        for r in RECIPES
    )
    fires_at_all = any(firing_summary[r]["battery_fires_at_p"] is not None for r in RECIPES)
    if fires_le_bar:
        return "INFORMATIVE"
    if fires_at_all:
        return "UNINFORMATIVE-BY-OWN-STANDARD"
    return "UNABLE-TO-RING-ITS-OWN-BELL"


def main():
    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        metrics = json.load(f)
    units_metrics = metrics["units"]
    units_jsonl = load_units_jsonl()
    pool = load_pool()

    mde = compute_mde(units_metrics)
    curve, firing_summary = build_power_curve(units_metrics, units_jsonl, pool)
    blind = structurally_blind_metrics(firing_summary)
    label = informativeness_label(firing_summary)

    out = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "p_grid": P_GRID,
        "recipes": {
            "A": {"donor_rank_range": [1, 50], "donor_count": 50,
                  "note": "near-universal function words; expected close to invisible to metric 4 (similarity) via idf-zeroing -- under test, not assumed."},
            "B": {"donor_rank_range": [51, 150], "donor_count": 100,
                  "note": "not near-universal; can move a within-window TF-IDF cosine."},
        },
        "mde": mde,
        "power_curve": curve,
        "firing_summary": firing_summary,
        "structurally_blind_metrics": blind,
        "informativeness": {
            "bar_p": INFORMATIVENESS_BAR_P,
            "label": label,
            "note": (
                "§9.4: applicable when §7's real decisional verdict is a step-2 null. Computed "
                "here unconditionally as the required sensitivity diagnostic regardless of what "
                "the real decisional run returned; see results/envelope.json for that verdict."
            ),
        },
        "injection_scope_note": (
            "Only decision units 61-73 are injected, simultaneously, for a given (p, recipe). "
            "The envelope fit itself is computed solely from the real, uninjected envelope-era "
            "units 1-47 and is identical across every (p, recipe) cell above. The injected "
            "similarity metric's trailing window for a decision unit mixes that unit's injected "
            "prefix (and any other decision unit inside its window) with the REAL prefixes of "
            "non-decision-unit window members -- intended, not an error (task note)."
        ),
    }
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=False, ensure_ascii=False)
    print(f"wrote {OUT_PATH}")
    print(f"informativeness: {label}")
    print(f"structurally blind: {blind}")


if __name__ == "__main__":
    main()
