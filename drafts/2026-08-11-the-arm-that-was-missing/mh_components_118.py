#!/usr/bin/env python3
"""The queued correction: bootstrap the Mantel-Haenszel odds ratio over connected components
instead of inflating its published standard error by sqrt(DEFF).

Session 118, 2026-08-14. Queued by session 116's gauntlet (`NEXT-SESSION.md`, "Added after the
gauntlet (session 116)"), which named it "the one derived-statistic correction in this session
that was never checked against anything" and set it as the first analytic task after day 4 is
measured. No new request of any instrument: this reads run files already on disk.

WHAT IS AND IS NOT A NEW CLUSTERING DIMENSION. Session 116 committed that no FURTHER clustering
dimension enters this arc's variance treatment before 2026-08-18. The account x page component is
the dimension already adopted there; applying it to a statistic that until now carried only an
inflation by sqrt(DEFF) is not a new dimension, and session 116's own post-gauntlet queue asked
for exactly this.

Steps:
  1. Reconstruct the published Mantel-Haenszel odds ratio from the underlying run files, with
     the Robins-Breslow-Greenland variance, and check it against the figure this arc published
     at session 111 (OR 1.7841, SE(log) 0.13946, CI [1.3574, 2.3449]).
  2. Resample CONNECTED COMPONENTS of the bipartite account x page graph with replacement and
     recompute the whole MH statistic inside each draw. Two seeds, so the seed-to-seed spread is
     on the record beside the interval (the defect session 116 was built to stop repeating).
  3. Run the delete-one-component jackknife beside it, as session 116's standing rule requires
     of every percentile-bootstrap interval this arc publishes.

Usage: python3 mh_components_118.py [draws]
"""
import json
import math
import random
import sys

from cluster_model import load
from cluster_keys import page_index
from crossed_model import components

A_RUN = "ledger/run-2026-08-11T1124Z.json"
A2_RUN = "expansion-111/baseline-run.json"
PUBLISHED = {"or": 1.7841, "se_log": 0.13946, "ci": [1.3574, 2.3449]}


def mh(rows):
    """MH odds ratio for RETRIEVABILITY of arm A against arm A2, stratified by creation year.

    Per stratum: a = A live, b = A absent, c = A2 live, d = A2 absent. Strata with an empty
    margin contribute nothing to either sum and are dropped, which is what MH does anyway.
    """
    strata = {}
    for r in rows:
        s = strata.setdefault(r["year"], [0, 0, 0, 0])
        live = 0 if r["absent"] else 1
        if r["arm"] == "A":
            s[0 if live else 1] += 1
        else:
            s[2 if live else 3] += 1
    num = den = 0.0
    R = S = 0.0
    pr = ps = qr = qs = 0.0
    used = 0
    for y, (a, b, c, d) in sorted(strata.items()):
        n = a + b + c + d
        if n == 0 or (a + b) == 0 or (c + d) == 0:
            continue
        used += 1
        Rk = a * d / n
        Sk = b * c / n
        R += Rk
        S += Sk
        P = (a + d) / n
        Q = (b + c) / n
        pr += P * Rk
        ps += P * Sk + Q * Rk
        qs += Q * Sk
    if R == 0 or S == 0:
        return None
    or_mh = R / S
    var_log = pr / (2 * R * R) + ps / (2 * R * S) + qs / (2 * S * S)
    return {"or": or_mh, "se_log": math.sqrt(var_log), "strata_used": used,
            "ci": [or_mh * math.exp(-1.96 * math.sqrt(var_log)),
                   or_mh * math.exp(1.96 * math.sqrt(var_log))]}


def main(draws=4000):
    _, rows_a, _, _ = load(A_RUN)
    _, rows_b, _, _ = load(A2_RUN)
    rows = [r for r in rows_a if r["arm"] == "A"] + [r for r in rows_b if r["arm"] == "A2"]

    point = mh(rows)
    reproduces = (abs(point["or"] - PUBLISHED["or"]) < 5e-4
                  and abs(point["se_log"] - PUBLISHED["se_log"]) < 5e-5)

    pidx = page_index()
    # components() needs every unit attributed to a citing page; unattributed units cannot enter
    # the graph and are counted here rather than dropped silently.
    attributed = [r for r in rows if r["vid"] in pidx]
    unattributed = len(rows) - len(attributed)
    comp_rows = components(attributed, pidx)          # lists of rows
    K = len(comp_rows)
    sizes = sorted((len(c) for c in comp_rows), reverse=True)
    point_attributed = mh(attributed)

    # -------- component bootstrap, two seeds
    boots = {}
    for seed in (7, 8):
        rng = random.Random(seed)
        vals, degenerate = [], 0
        for _ in range(draws):
            drawn = []
            for _ in range(K):
                drawn.extend(comp_rows[rng.randrange(K)])
            m = mh(drawn)
            if m is None:
                degenerate += 1
                continue
            vals.append(math.log(m["or"]))
        vals.sort()
        mean = sum(vals) / len(vals)
        sd = (sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)) ** 0.5
        lo = vals[int(0.025 * len(vals))]
        hi = vals[int(0.975 * len(vals))]
        boots[str(seed)] = {
            "draws": draws, "usable": len(vals), "degenerate_draws": degenerate,
            "se_log_or": sd, "deff_log_or": (sd / point_attributed["se_log"]) ** 2,
            "percentile_ci_or": [math.exp(lo), math.exp(hi)],
            "excludes_1": math.exp(lo) > 1 or math.exp(hi) < 1,
        }

    # -------- delete-one-component jackknife (session 116's standing rule)
    jack = []
    for j in range(K):
        drawn = [r for i, c in enumerate(comp_rows) if i != j for r in c]
        m = mh(drawn)
        if m:
            jack.append(math.log(m["or"]))
    jm = sum(jack) / len(jack)
    jack_se = math.sqrt((len(jack) - 1) / len(jack) * sum((v - jm) ** 2 for v in jack))
    worst = max(jack, key=lambda v: abs(v - math.log(point_attributed["or"])))
    jackknife = {
        "components_deleted_one_at_a_time": len(jack),
        "se_log_or": jack_se, "deff_log_or": (jack_se / point_attributed["se_log"]) ** 2,
        "ci_or": [point_attributed["or"] * math.exp(-1.96 * jack_se),
                  point_attributed["or"] * math.exp(1.96 * jack_se)],
        "largest_single_component_move_in_or": math.exp(worst) - point_attributed["or"],
        "excludes_1": point_attributed["or"] * math.exp(-1.96 * jack_se) > 1,
    }

    out = {
        "schema": "field-research/mh-component-bootstrap/1", "session": 118,
        "date": "2026-08-14",
        "queued_by": "session 116 gauntlet, NEXT-SESSION.md",
        "sources": {"arm_A": A_RUN, "arm_A2": A2_RUN},
        "units": {"A": sum(1 for r in rows if r["arm"] == "A"),
                  "A2": sum(1 for r in rows if r["arm"] == "A2")},
        "point_estimate": point,
        "point_estimate_attributed_only": point_attributed,
        "unattributed_units_excluded_from_graph": unattributed,
        "published_at_session_111": PUBLISHED,
        "reproduces_published": reproduces,
        "components": {"count": K, "largest_units": sizes[0],
                       "singletons": sum(1 for s in sizes if s == 1),
                       "units_covered": sum(sizes), "units_total": len(rows)},
        "component_bootstrap": boots,
        "delete_one_component_jackknife": jackknife,
        "the_substitution_it_replaces": {
            "method": "published SE(log OR) inflated by sqrt(DEFF)",
            "deff_used_at_session_115": 1.4289,
            "deff_used_at_session_116_crossed": 1.9900,
        },
    }
    json.dump(out, open("mh-components-118.json", "w"), indent=1)
    print(json.dumps({k: out[k] for k in
                      ("point_estimate", "reproduces_published", "components",
                       "component_bootstrap", "delete_one_component_jackknife")}, indent=1))
    print("wrote mh-components-118.json")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 4000)
