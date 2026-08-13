#!/usr/bin/env python3
"""Does the loss of cited video evidence concentrate by SUBJECT, or only by age?

Session 117, 2026-08-13. Re-analysis of runs already collected — NO new requests, the window
ledger, its manifest and its probe are untouched, and the window population is not modified.

THIS IS NOT A VARIANCE TREATMENT. No design effect appears anywhere in this file and it
produces no interval on a rate. Session 116 committed that no further clustering dimension
enters this arc's variance treatment before 2026-08-18; this instrument is bound by that and
does not touch it.

THE QUESTION (pre-registered at PREREGISTRATION-117.md, committed before any figure below):
one article in this corpus, `es.wikipedia.org|Protestas en Paraguay de 2023`, has lost 17 of
its 23 cited videos across 20 distinct accounts. Session 114's gauntlet asked what that
actually is — event, topic, or sweep — and recorded that no instrument this arc had built
could see it. The obvious confound has never been divided out: those videos all date from one
2023 event, and this corpus already knows that older videos are less retrievable.

METHOD
  null      each unit absent independently with probability p(age band x stratum), estimated
            LEAVE-ONE-PAGE-OUT so a heavy page cannot inflate its own expectation; cells with
            < MIN_CELL units outside the page fall back to the stratum margin, counted.
  statistic per page with >= n_min units: observed absent A, expected E = sum p_i, and the
            EXACT Poisson-binomial tails Pr(X >= A) and Pr(X <= A) by DP convolution.
            No normal approximation, no seed, no design effect.
  multiple  Benjamini-Hochberg at q < 0.05, upper and lower declared as separate families,
            plus a family-wise figure from Monte-Carlo draws of the whole null (seed 117000,
            fixed in the pre-registration before the run).
  mechanism for each flagged page, a second expectation in which each unit's probability is
            its OWN ACCOUNT's absence rate estimated off that page. Fewer than POWER_FLOOR
            units with such an estimate => declared without power, no verdict. That floor was
            written before the join.

Usage: python3 coloss_117.py [run.json ...]
"""
import collections
import json
import random
import sys

import cluster_keys as ck
import cluster_model as cm

MIN_CELL = 30       # units outside the page a cell needs before it is used
N_MIN = 5           # pre-registered primary page-size threshold
N_MIN_SENS = 3      # pre-registered sensitivity threshold
Q = 0.05
MC_DRAWS = 10000
MC_SEED = 117000
POWER_FLOOR = 5     # units with an off-page account estimate, below which no verdict
PARAGUAY = "es.wikipedia.org|Protestas en Paraguay de 2023"


# ---------------------------------------------------------------- exact tails

def poisson_binomial(ps):
    """Exact pmf of the number of successes among independent, unequal p. DP convolution."""
    dist = [1.0]
    for p in ps:
        nxt = [0.0] * (len(dist) + 1)
        for k, v in enumerate(dist):
            nxt[k] += v * (1.0 - p)
            nxt[k + 1] += v * p
        dist = nxt
    return dist


def tails(ps, a):
    d = poisson_binomial(ps)
    up = sum(d[a:])
    low = sum(d[:a + 1])
    return min(1.0, up), min(1.0, low)


def bh(pvals, q=Q):
    """Benjamini-Hochberg. Returns the set of indices rejected and each item's q-value."""
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    qv = [1.0] * m
    running = 1.0
    for rank in range(m, 0, -1):
        i = order[rank - 1]
        running = min(running, pvals[i] * m / rank)
        qv[i] = running
    rejected = {i for i in range(m) if qv[i] < q}
    return rejected, qv


# ---------------------------------------------------------------- the scan

def cell_of(r):
    return (r["band"], r["stratum"])


def scan(rows, idx, n_min):
    """Per-page observed vs age-standardised expected, leave-one-page-out, exact tails."""
    att = [r for r in rows if r["vid"] in idx]
    by_page = collections.defaultdict(list)
    for r in att:
        by_page[idx[r["vid"]]].append(r)

    tot_n = collections.Counter()
    tot_a = collections.Counter()
    str_n = collections.Counter()
    str_a = collections.Counter()
    for r in att:
        tot_n[cell_of(r)] += 1
        tot_a[cell_of(r)] += r["absent"]
        str_n[r["stratum"]] += 1
        str_a[r["stratum"]] += r["absent"]

    pages = []
    fallbacks = 0
    used = 0
    for page, units in sorted(by_page.items()):
        if len(units) < n_min:
            continue
        pn = collections.Counter()
        pa = collections.Counter()
        psn = collections.Counter()
        psa = collections.Counter()
        for r in units:
            pn[cell_of(r)] += 1
            pa[cell_of(r)] += r["absent"]
            psn[r["stratum"]] += 1
            psa[r["stratum"]] += r["absent"]
        ps, fb = [], 0
        for r in units:
            c = cell_of(r)
            n_out = tot_n[c] - pn[c]
            if n_out >= MIN_CELL:
                ps.append((tot_a[c] - pa[c]) / n_out)
            else:
                s = r["stratum"]
                n_out_s = str_n[s] - psn[s]
                ps.append((str_a[s] - psa[s]) / n_out_s if n_out_s > 0 else
                          (sum(tot_a.values()) - sum(pa.values())) /
                          (sum(tot_n.values()) - sum(pn.values())))
                fb += 1
        fallbacks += fb
        used += len(units)
        a = sum(r["absent"] for r in units)
        up, low = tails(ps, a)
        pages.append({
            "page": page, "n": len(units), "absent": a,
            "expected": sum(ps), "excess": a - sum(ps),
            "p_upper": up, "p_lower": low,
            "handles": len({r["handle"] for r in units}),
            "fallback_units": fb,
            "median_age_y": sorted(r["age_y"] for r in units)[len(units) // 2],
            "strata": sorted({r["stratum"] for r in units}),
            "_ps": ps,
        })
    for tail in ("upper", "lower"):
        rej, qv = bh([p["p_" + tail] for p in pages])
        for i, p in enumerate(pages):
            p["q_" + tail] = qv[i]
            p["flag_" + tail] = i in rej
    return pages, {"pages_scanned": len(pages), "units_scanned": used,
                   "fallback_units": fallbacks,
                   "fallback_share": fallbacks / used if used else None,
                   "units_attributed": len(att), "units_total": len(rows)}


def scan_pooled(rows, idx, n_min):
    """K2: the same scan with the naive pooled baseline, no leave-one-out."""
    att = [r for r in rows if r["vid"] in idx]
    by_page = collections.defaultdict(list)
    for r in att:
        by_page[idx[r["vid"]]].append(r)
    n = collections.Counter()
    a_ = collections.Counter()
    for r in att:
        n[cell_of(r)] += 1
        a_[cell_of(r)] += r["absent"]
    pages = []
    for page, units in sorted(by_page.items()):
        if len(units) < n_min:
            continue
        ps = [a_[cell_of(r)] / n[cell_of(r)] for r in units]
        a = sum(r["absent"] for r in units)
        up, low = tails(ps, a)
        pages.append({"page": page, "n": len(units), "absent": a, "expected": sum(ps),
                      "p_upper": up, "p_lower": low})
    rej, qv = bh([p["p_upper"] for p in pages])
    for i, p in enumerate(pages):
        p["q_upper"] = qv[i]
        p["flag_upper"] = i in rej
    return pages


def fwer_monte_carlo(pages, draws=MC_DRAWS, seed=MC_SEED):
    """Family-wise: draw the whole null, keep the smallest tail per draw."""
    rng = random.Random(seed)
    mins = []
    for _ in range(draws):
        best = 1.0
        for p in pages:
            ps = p["_ps"]
            a = sum(1 for q in ps if rng.random() < q)
            up, low = tails(ps, a)
            best = min(best, up, low)
        mins.append(best)
    mins.sort()
    obs = min(min(p["p_upper"], p["p_lower"]) for p in pages)
    k = sum(1 for m in mins if m <= obs)
    return {"draws": draws, "seed": seed, "observed_min_tail": obs,
            "fwer_p": (k + 1) / (draws + 1),
            "null_min_tail_p05": mins[int(0.05 * draws)],
            "null_min_tail_median": mins[draws // 2]}


# ------------------------------------------------- the mechanism arm: page or account

def account_expectation(page_key, rows, idx):
    """Each unit's probability = its own account's absence rate on OTHER pages."""
    att = [r for r in rows if r["vid"] in idx]
    units = [r for r in att if idx[r["vid"]] == page_key]
    off = collections.defaultdict(lambda: [0, 0])
    for r in att:
        if idx[r["vid"]] != page_key:
            off[r["handle"]][0] += 1
            off[r["handle"]][1] += r["absent"]
    ps, covered, uncovered = [], [], []
    for r in units:
        n, a = off[r["handle"]]
        if n > 0:
            ps.append(a / n)
            covered.append(r)
        else:
            uncovered.append(r)
    out = {"page": page_key, "units": len(units),
           "units_with_off_page_account_estimate": len(covered),
           "power_floor": POWER_FLOOR,
           "has_power": len(covered) >= POWER_FLOOR}
    if covered:
        a = sum(r["absent"] for r in covered)
        up, low = tails(ps, a)
        out.update({"observed_absent_on_covered": a, "expected_from_accounts": sum(ps),
                    "excess": a - sum(ps), "p_upper": up, "p_lower": low,
                    # CORRECTED 2026-08-13, same session, before publication: the first
                    # version of this key summed each covered unit's off-page count, so ONE
                    # off-page video behind an account with five units on the page was
                    # reported as five. It is the evidence behind the estimate that matters,
                    # and it is counted once. The wrong figure is kept beside it, named.
                    "distinct_off_page_units_backing_the_estimates":
                        sum(off[h][0] for h in {r["handle"] for r in covered}),
                    "superseded_double_counted_figure":
                        sum(off[r["handle"]][0] for r in covered),
                    "distinct_accounts_backing": len({r["handle"] for r in covered})})
    return out


def herfindahl(pages, key="excess"):
    """Where does the total excess live? (session 116's standing check)"""
    vals = [max(0.0, p[key]) for p in pages]
    tot = sum(vals)
    if tot <= 0:
        return {"total": tot, "effective_pages": None, "top_share": None}
    sh = sorted((v / tot for v in vals), reverse=True)
    return {"total": tot, "effective_pages": 1.0 / sum(s * s for s in sh),
            "top_share": sh[0], "top3_share": sum(sh[:3])}


def main(run_paths):
    out = {"schema": "field-research/coloss-scan/1", "session": 117,
           "preregistration": "PREREGISTRATION-117.md",
           "note": "no new requests; window ledger, manifest and probe untouched",
           "min_cell": MIN_CELL, "n_min": N_MIN, "q": Q, "runs": {}}
    idx = ck.page_index()
    for path in run_paths:
        d, rows, excl, key = cm.load(path)
        pages, meta = scan(rows, idx, N_MIN)
        sens, _ = scan(rows, idx, N_MIN_SENS)
        pooled = scan_pooled(rows, idx, N_MIN)
        up = [p for p in pages if p["flag_upper"]]
        low = [p for p in pages if p["flag_lower"]]
        r = {
            "run_id": d["run_id"], "run_utc_start": d["run_utc_start"],
            "excluded": excl, "meta": meta,
            "n_flag_upper": len(up), "n_flag_lower": len(low),
            "flag_upper": [{k: v for k, v in p.items() if k != "_ps"} for p in up],
            "flag_lower": [{k: v for k, v in p.items() if k != "_ps"} for p in low],
            "sensitivity_n_min_3": {
                "pages_scanned": len(sens),
                "n_flag_upper": sum(1 for p in sens if p["flag_upper"]),
                "n_flag_lower": sum(1 for p in sens if p["flag_lower"]),
                "flag_upper": [{k: v for k, v in p.items() if k != "_ps"}
                               for p in sens if p["flag_upper"]]},
            "K2_pooled_baseline": {
                "pages_scanned": len(pooled),
                "n_flag_upper": sum(1 for p in pooled if p["flag_upper"]),
                "flag_upper": [p["page"] for p in pooled if p["flag_upper"]]},
            "fwer_monte_carlo": fwer_monte_carlo(pages),
            "herfindahl_of_positive_excess": herfindahl(pages),
            "paraguay": next(({k: v for k, v in p.items() if k != "_ps"}
                              for p in pages if p["page"] == PARAGUAY), None),
            "mechanism_arm": [account_expectation(p["page"], rows, idx)
                              for p in up] or
                             [account_expectation(PARAGUAY, rows, idx)],
        }
        out["runs"][path] = r

        print(f"\n=== {path}  ({d['run_utc_start']})")
        m = r["meta"]
        print(f"  attributed {m['units_attributed']}/{m['units_total']}   "
              f"pages scanned {m['pages_scanned']} (>= {N_MIN} units, {m['units_scanned']} units)   "
              f"fallback units {m['fallback_units']} ({100*m['fallback_share']:.2f} %)")
        print(f"  FLAGGED upper {len(up)}   lower {len(low)}   "
              f"(BH q<{Q}; pooled-baseline upper {r['K2_pooled_baseline']['n_flag_upper']}; "
              f"n>=3 upper {r['sensitivity_n_min_3']['n_flag_upper']})")
        f = r["fwer_monte_carlo"]
        print(f"  family-wise MC: observed min tail {f['observed_min_tail']:.3e}  "
              f"FWER p {f['fwer_p']:.4f}  (null 5th pct {f['null_min_tail_p05']:.3e})")
        h = r["herfindahl_of_positive_excess"]
        print(f"  positive excess total {h['total']:.2f} videos; effective pages "
              f"{h['effective_pages']:.2f}; heaviest page holds {100*h['top_share']:.1f} %")
        for p in sorted(up, key=lambda x: x["p_upper"])[:12]:
            print(f"    UP  {p['page'][:58]:58s} {p['absent']:3d}/{p['n']:3d} "
                  f"exp {p['expected']:6.2f}  excess {p['excess']:+6.2f}  "
                  f"q {p['q_upper']:.2e}  accounts {p['handles']:3d}  "
                  f"med age {p['median_age_y']:.1f}y")
        for p in sorted(low, key=lambda x: x["p_lower"])[:8]:
            print(f"    LOW {p['page'][:58]:58s} {p['absent']:3d}/{p['n']:3d} "
                  f"exp {p['expected']:6.2f}  excess {p['excess']:+6.2f}  "
                  f"q {p['q_lower']:.2e}  accounts {p['handles']:3d}")
        pg = r["paraguay"]
        if pg:
            print(f"  PARAGUAY  {pg['absent']}/{pg['n']} absent, expected {pg['expected']:.2f} "
                  f"({pg['excess']:+.2f}), p_up {pg['p_upper']:.3e}, q_up {pg['q_upper']:.3e}, "
                  f"accounts {pg['handles']}, median age {pg['median_age_y']:.2f}y")
        for m2 in r["mechanism_arm"]:
            print(f"  MECHANISM {m2['page'][:52]:52s} covered "
                  f"{m2['units_with_off_page_account_estimate']}/{m2['units']}  "
                  f"power {m2['has_power']}", end="")
            if "p_upper" in m2:
                print(f"  obs {m2['observed_absent_on_covered']} vs acct-exp "
                      f"{m2['expected_from_accounts']:.2f}  p_up {m2['p_upper']:.3e}")
            else:
                print()
    json.dump(out, open("coloss-117.json", "w"), indent=1)
    print("\nwrote coloss-117.json")


if __name__ == "__main__":
    main(sys.argv[1:] or ["ledger/run-2026-08-13T0427Z.json",
                          "ledger/run-2026-08-12T0341Z.json"])
