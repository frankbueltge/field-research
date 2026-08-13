#!/usr/bin/env python3
"""Discharging conditions C4 and C5 of INTERLOCUTOR-6: a stable design effect, and the key
this session did not test.

C4: the published 1.458 is a percentile-width ratio from one 10,000-draw bootstrap, and its
seed-to-seed spread is larger than its last two digits. This computes the LINEARISED CLUSTERED
VARIANCE in closed form — no seed at all — and uses the bootstrap only to check it.

    V_cluster = K/(K-1) * sum_h (a_h - p*n_h)^2 / N^2        (ratio estimator, one stage)
    DEFF      = V_cluster / (p(1-p)/N)

C5: the adversary joined every unit back to the PAGE OR THREAD THAT CITES IT and found that key
clusters harder than the account key. This recomputes both keys from the corpus files, plus the
drop-one-page sensitivity that tells them apart.

Usage: python3 cluster_keys.py [run.json] [bootstrap draws] [seeds]
"""
import glob
import json
import random
import sys

from cluster_model import load, groups, kish, icc


def deff_analytic(g):
    """Linearised clustered variance of a ratio estimator against the binomial."""
    N = sum(len(v) for v in g.values())
    K = len(g)
    a = sum(r["absent"] for v in g.values() for r in v)
    p = a / N
    ss = sum((sum(r["absent"] for r in v) - p * len(v)) ** 2 for v in g.values())
    v_cluster = K / (K - 1) * ss / N ** 2
    v_binom = p * (1 - p) / N
    return {"n": N, "handles": K, "rate": p, "var_cluster": v_cluster,
            "var_binomial": v_binom, "deff": v_cluster / v_binom,
            "se_cluster": v_cluster ** 0.5, "se_binomial": v_binom ** 0.5}


def boot_widths(g, draws, seeds):
    """The published estimator, replicated across seeds, so its spread is on the record."""
    handles = list(g.values())
    K = len(handles)
    out = []
    for s in range(seeds):
        rng = random.Random(90000 + s)
        rates = []
        for _ in range(draws):
            n = a = 0
            for _ in range(K):
                v = handles[rng.randrange(K)]
                n += len(v)
                a += sum(r["absent"] for r in v)
            rates.append(a / n)
        rates.sort()
        out.append(rates[int(0.975 * draws)] - rates[int(0.025 * draws)])
    m = sum(out) / len(out)
    sd = (sum((x - m) ** 2 for x in out) / max(1, len(out) - 1)) ** 0.5
    return {"seeds": seeds, "draws": draws, "mean_width": m, "sd_width": sd,
            "min_width": min(out), "max_width": max(out)}


def page_index():
    """vid -> the page or thread that cites it, from the corpus files as collected."""
    idx = {}
    for f in glob.glob("corpus-*.wikipedia.org.json"):
        d = json.load(open(f))
        wiki = d["meta"]["wiki"]
        for r in d["rows"]:
            idx.setdefault(str(r["vid"]), f"{wiki}|{r['page']}")
    for f in ("expansion-111/corpus-round2.json", "expansion-111/corpus-round3.json",
              "expansion-111/corpus-A2-namespaces.json"):
        try:
            d = json.load(open(f))
        except FileNotFoundError:
            continue
        for r in d.get("rows", []):
            k = f"{r.get('wiki','?')}|{r.get('page','?')}"
            idx.setdefault(str(r["vid"]), k)
    try:
        d = json.load(open("corpus-hn.json"))
        for r in d["rows"]:
            idx.setdefault(str(r["vid"]), "forum|" + str(r.get("hn_object_id")))
    except FileNotFoundError:
        pass
    try:
        d = json.load(open("expansion-111/new-editions.json"))
        for r in d["rows"]:
            idx.setdefault(str(r["vid"]), f"{r.get('src','?')}|{r.get('page','?')}")
    except FileNotFoundError:
        pass
    return idx


def by_page(rows, idx):
    g = {}
    for r in rows:
        k = idx.get(r["vid"])
        if k:
            g.setdefault(k, []).append(r)
    return g


def pair_ratio(rows, keyfn_a, keyfn_b, label):
    """Pairs sharing key A but not key B, observed both-absent against expected."""
    from itertools import combinations
    buckets = {}
    for r in rows:
        buckets.setdefault(keyfn_a(r), []).append(r)
    p = sum(r["absent"] for r in rows) / len(rows)
    pairs = both = 0
    for v in buckets.values():
        for x, y in combinations(v, 2):
            if keyfn_b(x) != keyfn_b(y):
                pairs += 1
                both += x["absent"] * y["absent"]
    exp = pairs * p * p
    return {"label": label, "pairs": pairs, "both_absent": both,
            "expected": exp, "ratio": both / exp if exp else None}


def main(run_path, draws, seeds):
    d, rows, excl, key = load(run_path)
    gh = groups(rows)
    idx = page_index()
    gp = by_page(rows, idx)
    attributed = sum(len(v) for v in gp.values())

    # the same comparison on the identical subset, so the two keys are comparable
    sub = [r for r in rows if r["vid"] in idx]
    gh_sub = groups(sub)
    gp_sub = by_page(sub, idx)

    # drop the single heaviest page and see which key survives
    worst = max(gp_sub, key=lambda k: sum(r["absent"] for r in gp_sub[k]))
    sub2 = [r for r in sub if idx[r["vid"]] != worst]
    gh2, gp2 = groups(sub2), by_page(sub2, idx)

    out = {
        "run": run_path, "run_id": d["run_id"],
        "C4_analytic_handle_key_full_population": deff_analytic(gh),
        "C4_bootstrap_seed_spread": boot_widths(gh, draws, seeds),
        "C5_attributed_units": attributed, "C5_units_total": len(rows),
        "C5_handle_key_on_attributed_subset": deff_analytic(gh_sub),
        "C5_page_key_on_attributed_subset": deff_analytic(gp_sub),
        "C5_heaviest_page": {
            "key": worst, "units": len(gp_sub[worst]),
            "absent": sum(r["absent"] for r in gp_sub[worst]),
            "distinct_handles": len({r["handle"] for r in gp_sub[worst]})},
        "C5_handle_key_without_that_page": deff_analytic(gh2),
        "C5_page_key_without_that_page": deff_analytic(gp2),
        "C5_pairs_same_handle_different_page": pair_ratio(
            sub, lambda r: r["handle"], lambda r: idx[r["vid"]], "same handle, different page"),
        "C5_pairs_same_page_different_handle": pair_ratio(
            sub, lambda r: idx[r["vid"]], lambda r: r["handle"], "same page, different handle"),
        "rho_anova_handle_key": icc(gh), "m_kish_handle_key": kish(gh),
    }
    json.dump(out, open("cluster-keys-114.json", "w"), indent=1)
    a = out["C4_analytic_handle_key_full_population"]
    print(f"C4  analytic DEFF (handle key, no seed) = {a['deff']:.4f}   "
          f"n={a['n']} handles={a['handles']} rate={100*a['rate']:.2f}%")
    b = out["C4_bootstrap_seed_spread"]
    print(f"C4  published estimator over {b['seeds']} seeds x {b['draws']} draws: "
          f"width mean {100*b['mean_width']:.3f} pp  sd {100*b['sd_width']:.3f} pp  "
          f"range [{100*b['min_width']:.3f}, {100*b['max_width']:.3f}]")
    print(f"C5  attributed {attributed}/{len(rows)}")
    print(f"C5  handle key DEFF {out['C5_handle_key_on_attributed_subset']['deff']:.4f}  "
          f"(K={out['C5_handle_key_on_attributed_subset']['handles']})")
    print(f"C5  page   key DEFF {out['C5_page_key_on_attributed_subset']['deff']:.4f}  "
          f"(K={out['C5_page_key_on_attributed_subset']['handles']})")
    w = out["C5_heaviest_page"]
    print(f"C5  heaviest page: {w['key']}  units {w['units']} absent {w['absent']} "
          f"handles {w['distinct_handles']}")
    print(f"C5  without it: handle {out['C5_handle_key_without_that_page']['deff']:.4f}  "
          f"page {out['C5_page_key_without_that_page']['deff']:.4f}")
    for k in ("C5_pairs_same_handle_different_page", "C5_pairs_same_page_different_handle"):
        v = out[k]
        print(f"C5  {v['label']:32s} pairs {v['pairs']:6d} both {v['both_absent']:4d} "
              f"expected {v['expected']:7.1f} ratio {v['ratio']:.2f}")
    print("wrote cluster-keys-114.json")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "ledger/run-2026-08-12T0341Z.json",
         int(sys.argv[2]) if len(sys.argv) > 2 else 10000,
         int(sys.argv[3]) if len(sys.argv) > 3 else 10)
