#!/usr/bin/env python3
"""build_deliverable - assemble the receiver-facing bundle from this arc's own run files.

Session 120, 2026-08-15. This script exists because of a charge this practice accepted in
public and did not dispute: that with three weeks left before its own constitution's reading,
nothing it has measured has left the house in a form anyone outside could pick up.

It takes the dated run files of the window instrument, which are the arc's primary record,
and writes a self-contained bundle under `deliverable/`. It invents nothing: every number in
the bundle is computed here from a run file on disk, and the bundle carries the sha256 of
every file it was built from.

    python3 build_deliverable.py [--out deliverable]

WHAT THE BUNDLE IS FOR, in one sentence, because it is the thing most easily got wrong:
a credential-free, dated record of whether named videos were publicly retrievable, plus a
reference population large enough to give a single reading an expectation. It is the
control arm of a two-sided comparison. It is NOT an audit of any research interface, and it
cannot on its own show that any platform's coverage claim is false.

Exclusions, applied here and stated in the bundle:

* arm `B-truncated` is a control arm of display-truncated identifiers that are NOT videos.
  It is excluded from every rate and reported separately, because including it would
  manufacture absence.
* `INDETERMINATE` observations (transport failures) are excluded from rates and counted.
* identifiers that are not 19 digits cannot be dated by the platform's modern scheme
  (session 110); they stay in the series and are excluded from age-banded rates only.
"""
import argparse
import calendar
import hashlib
import json
import math
import os
import time

import power_audit as pa

YEAR_S = 365.25 * 86400.0

# The window's dated runs, in order. The baseline union is day 1 by construction: it is the
# state every unit was in before the pre-registered window opened (see NEXT-SESSION.md
# warning 2 - the baseline is two run files, and the union is what the merged manifest was
# built from).
BASELINE = "ledger/baseline-union.json"
CORRECTIONS = "ledger/corrections.json"

STRATUM = {
    "A": "W-article",
    "A-new": "W-article",
    "A2": "W-other-ns",
    "B": "F-forum",
}

AGE_BANDS = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 99)]


def _drift_figures():
    """The measured caller-side drift, READ from the measurement that produced it (session 122).

    Interlocutor 14 finding 5. A block of drift figures typed beside a table that can be rebuilt
    on a longer panel is the V1 shape one level up: a declaration nobody checks, beside cells
    that moved. If the measurement is not on disk this returns a statement of that fact — never
    a number.
    """
    try:
        d = json.load(open("drift-122.json"))
        rows = d["half_two_caller_side_drift"]["lists"]["reference_population_itself"]["horizons"]
        return {str(r["days_after_t_ref"]): round(r["drift_pp_from_day0"], 4)
                for r in rows if r["days_after_t_ref"] > 0}
    except Exception as e:
        return {"unavailable": f"drift-122.json was not readable when this table was built "
                               f"({type(e).__name__}); no drift figures are asserted here"}


def band_label(lo, hi):
    return f"{lo}-{hi}y" if hi < 99 else f"{lo}y+"


def band_of(age_y):
    if age_y is None:
        return None
    for lo, hi in AGE_BANDS:
        if lo <= age_y < hi:
            return band_label(lo, hi)
    return None


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


REPLICATE_MARK = "-second-probe"


def discover_runs():
    """Every complete run file of the window, oldest first. A .partial is never a run."""
    out = []
    for name in sorted(os.listdir("ledger")):
        if not name.startswith("run-") or not name.endswith(".json"):
            continue
        p = os.path.join("ledger", name)
        d = json.load(open(p))
        if d.get("partial") or d.get("schema", "").endswith("/partial"):
            continue
        out.append((p, d))
    out.sort(key=lambda t: t[1]["run_utc_start"])
    return out


def fisher_two_sided(a, b, c, d):
    """Two-sided Fisher exact on the 2x2 [[a, b], [c, d]], by summing tables no more likely
    than the observed one. Written out here rather than imported so the bundle's own claim
    about its age gradient can be recomputed from this file alone."""
    n = a + b + c + d
    if min(a + b, c + d, a + c, b + d) < 0 or n == 0:
        return None
    def p(x):
        return (math.comb(a + b, x) * math.comb(c + d, a + c - x)) / math.comb(n, a + c)
    lo, hi = max(0, a + c - (c + d)), min(a + b, a + c)
    p0 = p(a)
    return min(1.0, sum(p(x) for x in range(lo, hi + 1) if p(x) <= p0 * (1 + 1e-9)))


def cell(n, absent):
    if n == 0:
        return {"n": 0, "absent": 0, "absent_rate": None, "absent_ci": [None, None]}
    lo, hi = pa.wilson(absent, n)
    return {"n": n, "absent": absent, "absent_rate": absent / n, "absent_ci": [lo, hi]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="deliverable")
    # Session 122. The bundle's coverage cut-off used to be whatever happened to be on disk when
    # the script ran, and `MANIFEST.json -> coverage` then described it after the fact. A freeze
    # that cannot be restated is a freeze nobody can check: with `--cutoff` the shipped bundle is
    # reproducible from a later working tree, which is the only reason the V1 repair below can be
    # shown as a difference in one file rather than asserted.
    ap.add_argument("--cutoff", default=None,
                    help="ignore run files starting after this UTC stamp (e.g. 2026-08-14T23:59:59Z)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    os.makedirs(os.path.join(a.out, "series"), exist_ok=True)

    base = json.load(open(BASELINE))
    runs = discover_runs()

    # Days: the baseline union first, then every complete window run that starts after it.
    days = [{"label": "baseline",
             "file": BASELINE,
             "run_id": base["run_id"],
             "utc_start": base["run_utc_start"],
             "utc_end": base["run_utc_end"],
             "sha256": sha256(BASELINE),
             "obs": base["observations"]}]
    # Session 124: TWO PROBES RAN ON 2026-08-16 (`DOUBLE-PROBE-122.md`). Both are complete,
    # both are in the ledger, and both were being discovered here as separate "measurement days"
    # with the SAME label - which produced a manifest claiming seven measurement days over six
    # days of measurement, a series carrying the label twice, and an `expectation.json` whose
    # cells for that day silently came from whichever run happened to be processed last. The
    # accident that cost the endpoint a doubled request load was also corrupting the artifact,
    # and nothing said so.
    #
    # The rule, stated rather than inferred: a run file whose name marks it a replicate is NOT a
    # measurement day. It is recorded in the manifest as a replicate, so it stays visible and
    # checkable, and the canonical run for that day is the one the record designates. Any
    # duplicate label that survives this is a hard error - the build refuses rather than
    # quietly picking one.
    replicates = []
    for p, d in runs:
        if d["run_utc_start"] <= base["run_utc_start"]:
            continue          # the baseline's own component runs
        if a.cutoff and d["run_utc_start"] > a.cutoff:
            continue          # session 122: the freeze, stated rather than incidental
        if REPLICATE_MARK in os.path.basename(p):
            replicates.append({"file": p, "label": d["run_utc_start"][:10],
                               "run_utc_start": d["run_utc_start"],
                               "sha256": sha256(p),
                               "why_not_a_day": ("a second complete pass over the same manifest on "
                                                 "the same UTC day; see DOUBLE-PROBE-122.md. It is "
                                                 "evidence about the instrument, not an additional "
                                                 "day of the series.")})
            continue
        days.append({"label": d["run_utc_start"][:10],
                     "file": p,
                     "run_id": d["run_id"],
                     "utc_start": d["run_utc_start"],
                     "utc_end": d["run_utc_end"],
                     "seconds": d.get("seconds"),
                     "planned": d.get("planned"),
                     "requested": d.get("requested"),
                     "stopped": d.get("stopped"),
                     "vantage_asn": d["vantage"]["asn"],
                     "vantage_country": d["vantage"]["country"],
                     "sha256": sha256(p),
                     "obs": d["observations"]})

    _seen = {}
    for _d in days:
        _seen.setdefault(_d["label"], []).append(_d["file"])
    _dupes = {k: v for k, v in _seen.items() if len(v) > 1}
    if _dupes:
        raise SystemExit(
            "refusing to build: two runs claim the same measurement day, and a bundle that "
            "silently keeps one of them is a bundle whose cells nobody can trace.\n"
            + json.dumps(_dupes, indent=1)
            + "\nDesignate the replicate by renaming it to carry '%s', the way "
              "DOUBLE-PROBE-122.md designated the second probe of 2026-08-16." % REPLICATE_MARK)
        # First gauntlet, E11: one archived run file carries an unfilled placeholder in its own
        # `run_id`, inherited from a manifest at session 113. The archived file is primary and is
        # never edited; the bundle must not repeat the placeholder as though it were a value.
        if "TEMPLATE" in str(days[-1]["run_id"]):
            days[-1]["run_id"] = ("UNKNOWN — the archived run file carries an unfilled placeholder "
                                  "in this field (first gauntlet, E11). The run is identified by "
                                  "its path, its start time and its sha256, all of which are in "
                                  "this entry; the archived file is primary and is not edited.")

    # ---- the overlay of refuted readings ------------------------------------------------
    # PREREGISTRATION-119-overlay-use.md: the raw run file is the primary record and is
    # never edited; the overlay is published beside it and every row it uses is named.
    # A row applies only where the run file actually carries the state the overlay refutes.
    corr = json.load(open(CORRECTIONS)) if os.path.exists(CORRECTIONS) else {"corrections": []}
    overlay = {}
    for c in corr["corrections"]:
        overlay[(c["run_file"], str(c["vid"]))] = c
    overlay_used = []

    # ---- the series -------------------------------------------------------------------
    units = {}
    for day in days:
        for o in day["obs"]:
            vid = str(o["vid"])
            u = units.setdefault(vid, {"vid": vid, "arm": o["arm"],
                                       "states": {}, "states_corrected": {}})
            u["states"][day["label"]] = o["state"]
            c = overlay.get((day["file"], vid))
            if c and o["state"] == c["state_in_run_file"]:
                u["states_corrected"][day["label"]] = c["corrected_state"]
                overlay_used.append({"day": day["label"], "vid": vid,
                                     "run_file": day["file"],
                                     "raw": o["state"], "corrected": c["corrected_state"],
                                     "authority": c["authority"], "reason": c["reason"]})
            else:
                u["states_corrected"][day["label"]] = o["state"]

    # V1 of the session-120 gauntlet, repaired 2026-08-16 (session 122) and measured before it
    # was repaired (`drift_122.py` -> `drift-122.json`, `DRIFT-122.md`).
    #
    # What was wrong: this line took the age of every unit at `days[0]` — the first day of the
    # panel — and line ~364 then declared the reference table's `t_ref_utc` to be the NEWEST day.
    # The two are 2.6803 days apart, 24 units sit in a different band under the two clocks, and
    # every published age-band cell of the shipped table is therefore a cell of a date the table
    # does not name. NOTHING about the observations changes: the 24 crossers are all retrievable,
    # so no `absent` count moves and the pooled rate is identical to the last digit.
    #
    # What it is now: each unit carries its age at EACH day's own measurement, so a day's table is
    # a table of that day. `age_y_at_baseline` is kept, with its old meaning and its honest name,
    # because the series CSV has shipped that column and a reader who has it must be able to
    # reproduce it; `age_y_at_<label>` is the one the per-day tables use.
    t_first = calendar.timegm(time.strptime(days[0]["utc_start"], "%Y-%m-%dT%H:%M:%SZ"))
    t_of_day = {d["label"]: calendar.timegm(time.strptime(d["utc_start"], "%Y-%m-%dT%H:%M:%SZ"))
                for d in days}
    for u in units.values():
        vid = u["vid"]
        if len(vid) == 19:
            created = int(vid) >> 32
            u["created"] = created
            u["created_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(created))
            age = (t_first - created) / YEAR_S
            u["age_y_at_baseline"] = round(age, 4) if age > 0 else None
            u["age_y_by_day"] = {}
            u["band_by_day"] = {}
            for lab, tr in t_of_day.items():
                age_lab = (tr - created) / YEAR_S
                u["age_y_by_day"][lab] = round(age_lab, 4) if age_lab > 0 else None
                u["band_by_day"][lab] = band_of(u["age_y_by_day"][lab])
        else:
            u["created"] = None
            u["created_utc"] = None
            u["age_y_at_baseline"] = None
            u["age_y_by_day"] = {d["label"]: None for d in days}
            u["band_by_day"] = {d["label"]: None for d in days}
        u["band"] = band_of(u["age_y_at_baseline"])
        u["stratum"] = STRATUM.get(u["arm"], u["arm"])

    labels = [d["label"] for d in days]
    ordered = sorted(units.values(), key=lambda u: (u["arm"], u["vid"]))

    for key, fname in (("states", "presence-series.csv"),
                       ("states_corrected", "presence-series-corrected.csv")):
        # Session 122, and it is a consequence of the V1 repair rather than a separate decision.
        # The column used to be called `band`, and it was the unit's band on the FIRST day of the
        # panel. Once the age tables are banded per day, a receiver joining that column to the
        # reference table would be joining two different bandings and would never see it — the
        # repair would have created the trap the repair exists to close. So the column says which
        # day it is the band of, and one column per day is written beside it. Nothing has been
        # sent to anyone and the bundle is withheld, so there is no compatibility debt to weigh
        # against saying it plainly.
        with open(os.path.join(a.out, "series", fname), "w") as f:
            # labels[0] is "baseline", so the per-day loop already emits the old `band` column
            # under its true name; writing it twice was this session's own first draft and is
            # not written here.
            f.write("video_id,arm,stratum,created_utc,age_y_at_baseline,"
                    + ",".join(f"band_at_{l}" for l in labels) + ","
                    + ",".join(labels) + "\n")
            # (v0.3.0 asserted `u["band"] == u["band_by_day"]["baseline"]` here. Interlocutor 14
            #  finding 12: both sides derive from t_first, so it could not fail. Removed rather
            #  than left standing as a check that certifies nothing. The assertion that carries
            #  the V1 claim is the one below the reference table, which was mutation-tested from
            #  both directions by the session-122 Verifier and fired both times.)
            for u in ordered:
                f.write(",".join([
                    u["vid"], u["arm"], u["stratum"], u["created_utc"] or "",
                    "" if u["age_y_at_baseline"] is None else f"{u['age_y_at_baseline']:.4f}",
                    *[(u["band_by_day"].get(l) or "") for l in labels],
                    *[u[key].get(l, "") for l in labels]]) + "\n")

    json_path = os.path.join(a.out, "series", "presence-series.json")
    json.dump({
        "schema": "field-research/public-presence-series/1",
        "what_this_is": ("one row per video identifier, one column per dated measurement day. "
                         "Each cell is the state of the platform's credential-free oEmbed "
                         "endpoint for that identifier on that day, from one vantage."),
        "what_the_states_mean": {
            "RETRIEVABLE": "the endpoint returned a usable public record, from this vantage, at that moment",
            "NOT-RETRIEVABLE": ("the endpoint refused with a single opaque HTTP 400. This code is "
                                "SEMANTICALLY EMPTY: a synthetic identifier that never existed "
                                "returns the same code (three-arm control, 20 synthetic ids, "
                                "2026-08-11). IT DOES NOT MEAN DELETED, removed, banned or private."),
            "INDETERMINATE": "transport failure or unexpected status. Not evidence either way.",
            "": "this identifier was not in the manifest of that day's run",
        },
        "days": [{k: v for k, v in d.items() if k != "obs"} for d in days],
        "n_units": len(ordered),
        "corrections_overlay": {
            "policy": corr.get("policy"),
            "rows_available": len(corr["corrections"]),
            "rows_applied": overlay_used,
            "note": ("`states` is the raw record of what the instrument returned and is "
                     "primary. `states_corrected` applies the overlay of readings this "
                     "practice's own confirmation step refuted with five immediate "
                     "re-requests. No archived run file is ever edited. Where the two "
                     "differ, both are published."),
        },
        "units": ordered,
    }, open(json_path, "w"), indent=1)

    # ---- the expectation, per day, on both arms ----------------------------------------
    def expectation_tables(state_key):
        per_day = {}
        for day in days:
            rows = []
            excluded = {"arm_B_truncated": 0, "indeterminate": 0, "undatable": 0}
            for o in day["obs"]:
                u = units[str(o["vid"])]
                state = u[state_key].get(day["label"])
                if o["arm"] == "B-truncated":
                    excluded["arm_B_truncated"] += 1
                    continue
                if state == "INDETERMINATE":
                    excluded["indeterminate"] += 1
                    continue
                # V1 repair (session 122): the band is the unit's band on THIS day, not on the
                # first day of the panel. `by_year` is unaffected — a creation year does not move.
                rows.append({"absent": 1 if state == "NOT-RETRIEVABLE" else 0,
                             "band": u["band_by_day"].get(day["label"]),
                             "stratum": u["stratum"],
                             "year": (u["created_utc"] or "")[:4] or None})
            n = len(rows)
            k = sum(r["absent"] for r in rows)
            by = {}
            for keyname, keyfn in (("by_age_band", lambda r: r["band"]),
                                   ("by_stratum", lambda r: r["stratum"]),
                                   ("by_year", lambda r: r["year"])):
                buckets = {}
                for r in rows:
                    key = keyfn(r)
                    if key is None:
                        excluded["undatable"] += (1 if keyname == "by_age_band" else 0)
                        continue
                    buckets.setdefault(key, []).append(r)
                by[keyname] = {kk: cell(len(v), sum(x["absent"] for x in v))
                               for kk, v in sorted(buckets.items())}
            # The crossed table. The age gradient is only interesting if it is not an
            # artefact of which source the older identifiers happen to come from, so the
            # bundle publishes the gradient WITHIN each source stratum as well as pooled.
            crossed = {}
            for r in rows:
                if r["band"] is None:
                    continue
                crossed.setdefault(r["stratum"], {}).setdefault(r["band"], []).append(r)
            by["by_stratum_band"] = {
                s: {b: cell(len(v), sum(x["absent"] for x in v))
                    for b, v in sorted(bs.items())}
                for s, bs in sorted(crossed.items())}
            per_day[day["label"]] = {
                "measured_utc_start": day["utc_start"],
                "pooled": cell(n, k),
                "excluded": excluded,
                **by,
            }

        # Across-day spread of the pooled and per-band rate. NOTE, and this is the caveat
        # that governs how it may be read: this is the SAME fixed panel measured again, so
        # the spread is the instrument's test-retest reproducibility, NOT the sampling
        # variability of an independently drawn population.
        stability = {}
        for band in [band_label(*b) for b in AGE_BANDS] + ["__pooled__"]:
            vals = []
            for label, d in per_day.items():
                c = d["pooled"] if band == "__pooled__" else d["by_age_band"].get(band)
                if c and c["absent_rate"] is not None:
                    vals.append((label, c["absent_rate"], c["n"]))
            if not vals:
                continue
            rates = [v[1] for v in vals]
            stability[band] = {
                "days": len(vals),
                "min": min(rates), "max": max(rates), "range": max(rates) - min(rates),
                "mean": sum(rates) / len(rates),
                "per_day": {v[0]: {"absent_rate": v[1], "n": v[2]} for v in vals},
            }
        return per_day, stability

    per_day, stability = expectation_tables("states")
    per_day_c, stability_c = expectation_tables("states_corrected")

    json.dump({
        "schema": "field-research/public-presence-expectation/1",
        "what_this_is": ("the reference absence rate of a large measured population, per day, "
                         "pooled and split by the age of the video, by the source the "
                         "identifier came from, and by year of creation. It is a yardstick: "
                         "it says what share of comparable identifiers this instrument could "
                         "not retrieve publicly on that day."),
        "how_to_use_it": ("for a list of identifiers of your own, compute the age profile, take "
                          "the matching per-band rates below, and weight them by your list's "
                          "profile. presence_check.py does this for you. The result is an "
                          "expectation, NOT a verdict on any individual identifier."),
        "excluded_from_all_rates": {
            "arm_B-truncated": ("display-truncated identifiers, a control arm. 248 of the 249 do not "
                                "resolve; ONE (`12345`) is a real video predating the platform's "
                                "current identifier scheme. The arm is excluded from every rate "
                                "because including it would manufacture absence, not because "
                                "every member is certainly not a video (first gauntlet, E7)."),
            "INDETERMINATE": "transport failures - not evidence either way",
        },
        "how_to_read_the_across_day_spread": (
            "the spread below is the SAME fixed panel of identifiers measured again on each "
            "day. It is the instrument's test-retest reproducibility - evidence that a "
            "reading is not an artefact of one day's network conditions. It is NOT the "
            "sampling variability of an independently drawn population, and it must not be "
            "used as a confidence interval for a new sample. The per-day Wilson intervals "
            "in `per_day` are the sampling uncertainty."),
        "per_day": per_day,
        "across_day_stability": stability,
        "corrected_arm": {
            "what_it_is": ("the same tables with the refuted-reading overlay applied. The raw "
                           "arm above is primary; both are published because they differ."),
            "per_day": per_day_c,
            "across_day_stability": stability_c,
        },
    }, open(os.path.join(a.out, "expectation.json"), "w"), indent=1)

    # ---- the reference baseline in the shape the shipped tool already reads -------------
    # presence_check.py (session 113) reads `field-research/public-presence-null/1`. The tool
    # is NOT modified for this bundle - modifying it would make measurements taken with the
    # bundle incomparable with this practice's own ledger. Instead the newest day's table is
    # written in the shape the unmodified tool expects.
    newest = days[-1]
    ref = {
        "schema": "field-research/public-presence-null/1",
        "written_by": "build_deliverable.py, session 120, for the receiver bundle",
        "what_this_measures": ("public retrievability of a video identifier from one network "
                               "vantage, through one credential-free endpoint, on one day. The "
                               "refusal code is semantically empty: a synthetic identifier that "
                               "never existed returns the same code. NOT-RETRIEVABLE DOES NOT "
                               "MEAN DELETED. See LIMITS.md."),
        "source_run": {"file": newest["file"], "run_id": newest["run_id"],
                       "vantage_asn": newest.get("vantage_asn", "AS396982"),
                       "sha256": newest["sha256"]},
        "t_ref_utc": newest["utc_start"],
        # V1 repair, session 122. The declaration above used to be a claim nobody checked and
        # was false for three sessions. It is now stated twice, from two different places in
        # this function, and asserted below — a single field cannot go quietly wrong again.
        "ages_computed_at_utc": newest["utc_start"],
        "shelf_life": {
            "why_this_is_here": ("this table is a measurement of one population on one day. A tool "
                                 "that ages a caller's list at TODAY and looks it up here is doing "
                                 "arithmetic against a clock that stopped. The size of that error "
                                 "was measured before it was disclosed: `drift-122.json`."),
            # Interlocutor 14 finding 5, repaired the same night: these seven figures were
            # TYPED here from the measurement rather than read from it, inside a repair whose
            # whole subject is numbers that quietly stop matching their source. They are now
            # read from `drift-122.json`, and if that file is absent the block says so instead
            # of shipping a stale literal beside a fresh table.
            "measured_drift_pp_by_days_after_t_ref": _drift_figures(),
            "drift_is_on": ("the reference population itself, re-aged against this fixed table; it "
                            "is what the printed expectation does, NOT a forecast of what "
                            "retrievability does"),
            "source": "drift_122.py, session 122, 2026-08-16",
        },
        "population": {"n_units_in_run": len(newest["obs"]),
                       "excluded_from_rates": per_day[newest["label"]]["excluded"],
                       "what_it_is": ("videos cited in public across 37 language editions of one "
                                      "encyclopedia (article and non-article namespaces) and in "
                                      "the public comments and stories of one technology forum. "
                                      "The count was published as 21 in versions 0.1-0.3 and was "
                                      "corrected at the first gauntlet (V3/E4) and re-derived "
                                      "independently at session 123.")},
        "pooled": per_day[newest["label"]]["pooled"],
        "by_age_band": per_day[newest["label"]]["by_age_band"],
        "by_stratum": per_day[newest["label"]]["by_stratum"],
        "by_year": per_day[newest["label"]]["by_year"],
        "arm": "raw run file, primary record; the corrected arm is in expectation.json",
    }
    # The assertion that makes V1 unrepeatable rather than merely repaired: every unit counted
    # into the shipped age table must have been banded at the time the table declares. Checked
    # against the units themselves, not against the two strings agreeing with each other.
    _t_declared = calendar.timegm(time.strptime(ref["t_ref_utc"], "%Y-%m-%dT%H:%M:%SZ"))
    for u in units.values():
        if u["created"] is None:
            continue
        _a = (_t_declared - u["created"]) / YEAR_S
        assert u["band_by_day"][newest["label"]] == band_of(_a if _a > 0 else None), (
            f"V1 regression: {u['vid']} is banded at a time the reference table does not declare")
    json.dump(ref, open(os.path.join(a.out, "reference-baseline.json"), "w"), indent=1)

    # ---- the gradient's own test, computed here so no one types it ---------------------
    # Youngest band against oldest band, pooled and inside each stratum. Written to its own file
    # BEFORE the tables page is rendered, because as of session 124 the page is built by reading
    # the bundle's files rather than from the variables in this function.
    newest_label = days[-1]["label"]
    # The gradient's own test, computed here so no one types it. Youngest band against
    # oldest band, pooled and inside each stratum.
    young, old = band_label(*AGE_BANDS[0]), band_label(*AGE_BANDS[-1])
    grad = []
    src = per_day[newest_label]
    pairs_to_test = [("pooled", src["by_age_band"])] + \
                    [(s, t) for s, t in sorted(src["by_stratum_band"].items())]
    for name, table in pairs_to_test:
        cy, co = table.get(young), table.get(old)
        if not cy or not co or not cy["n"] or not co["n"]:
            continue
        pv = fisher_two_sided(cy["absent"], cy["n"] - cy["absent"],
                              co["absent"], co["n"] - co["absent"])
        grad.append({"group": name,
                     "young_band": young, "young": [cy["absent"], cy["n"]],
                     "old_band": old, "old": [co["absent"], co["n"]],
                     "ratio_old_over_young": (co["absent_rate"] / cy["absent_rate"]
                                              if cy["absent_rate"] else None),
                     "fisher_two_sided_p": pv})
    json.dump({"schema": "field-research/age-gradient-test/1",
               "day": newest_label,
               "test": "two-sided Fisher exact, youngest age band against oldest",
               "arm": "raw run file (primary record)",
               "caveat": ("the pooled progression across the six bands is not strictly "
                          "monotone; the endpoints are what this table tests"),
               "results": grad},
              open(os.path.join(a.out, "gradient-test.json"), "w"), indent=1)

    # ---- the generated tables page -----------------------------------------------------
    # Session 124, CONDITIONS-123.md binding item 1. This page used to be assembled here, from
    # the same in-memory dicts that had just been written to `expectation.json`. That made the
    # page and the data file incapable of disagreeing - which sounds like a guarantee and is the
    # opposite of one: nothing checked that a cell came from the field its sentence names, and
    # three numbers on the page (0.0577 pp, 248 of 249, 37 language editions) were literals typed
    # into the f-strings, vouched for by the machine generation around them. `figures_page.py`
    # rebuilds the page from the files this bundle ships, through `figures.py`, so every figure
    # records the file and JSON path it was read from.
    import figures_page
    page_fx = figures_page.build(a.out, os.path.dirname(os.path.abspath(__file__)),
                                 built_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    page_fx.write(os.path.join(a.out, "FIGURES-PROVENANCE.json"))

    # ---- provenance --------------------------------------------------------------------
    manifest = {
        "schema": "field-research/deliverable-manifest/1",
        "built_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "built_by": "build_deliverable.py, session 120",
        "coverage": {
            "first_measurement_utc": days[0]["utc_start"],
            "last_measurement_utc": days[-1]["utc_start"],
            "n_measurement_days": len(days),
            "note": ("this bundle is a dated snapshot with a stated cut-off. The instrument that "
                     "produced it keeps running; a later version covers later days. A run that "
                     "was still in flight when the bundle was assembled is NOT in it, and the "
                     "absence of a day here is never evidence that the instrument was dark."),
        },
        "source_runs": [{k: v for k, v in d.items() if k != "obs"} for d in days],
        "corrections_file": {"path": CORRECTIONS,
                             "sha256": sha256(CORRECTIONS) if os.path.exists(CORRECTIONS) else None,
                             "rows_applied": len(overlay_used)},
        "n_units": len(ordered),
        "n_days": len(days),
        # Session 124: complete second passes over the same manifest on a day already in
        # the series. Named here rather than dropped silently, because a run that exists
        # and is not in the bundle is exactly the kind of absence this practice refuses to
        # leave unstated.
        "replicate_runs": replicates,
    }
    json.dump(manifest, open(os.path.join(a.out, "MANIFEST.json"), "w"), indent=1)

    print(json.dumps({
        "days": labels,
        "units": len(ordered),
        "pooled_absent_rate_per_day": {l: per_day[l]["pooled"]["absent_rate"] for l in labels},
        "pooled_n_per_day": {l: per_day[l]["pooled"]["n"] for l in labels},
    }, indent=1))


if __name__ == "__main__":
    main()
