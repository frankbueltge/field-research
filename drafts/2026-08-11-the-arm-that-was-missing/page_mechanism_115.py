#!/usr/bin/env python3
"""What is an article that co-loses 17 of its 23 cited videos?

Session 115, 2026-08-13. **No new requests** — this reads run files and corpus files already
collected. Pre-registered in `PREREGISTRATION-115.md` §0 as the zero-request item session 114's
gauntlet put ahead of the ~2,744-request account arm.

Session 114's adversary found that the **citing page** clusters absences harder than the account
(DEFF 1.8854 against 1.4289) and that the effect is carried by one article. It then asked the
question no instrument on this arc could answer: *is that an event, a topic, or a sweep?* This
file does not answer it either — nothing reachable from a credential-free endpoint can say why a
video is gone. What it can do is **narrow which explanations survive the data we already hold**:

  * **Shared era.** If a page's videos are co-absent because they were all posted in the same
    weeks and old videos are likelier gone, the page effect should disappear once absence is
    permuted **within creation-week x arm cells**. That is the same null session 114 used on the
    account key, re-pointed at the page key.
  * **Shared account.** If a page's co-absence is really its accounts' co-absence, the page effect
    should disappear once absence is permuted **within account**. Pages and accounts cross-cut, so
    this is a real test rather than a tautology.
  * **Neither.** If the page effect survives both, something operates at the level of the citing
    document — an event whose footage went together, or a moderation sweep over a topic — and this
    arc has no instrument that can separate those two and says so.

Output: `page-mechanism-115.json`.
"""
import json
import math
import random
import sys
import time

import cluster_model as cm
import cluster_keys as ck

RUN = "ledger/run-2026-08-12T0341Z.json"
DRAWS = 10000
SEED = 20260813
WEEK_S = 7 * 24 * 3600


def deff_analytic(g):
    N = sum(len(v) for v in g.values())
    K = len(g)
    if N == 0 or K < 2:
        return None
    a = sum(r["absent"] for v in g.values() for r in v)
    p = a / N
    if p in (0.0, 1.0):
        return None
    ss = sum((sum(r["absent"] for r in v) - p * len(v)) ** 2 for v in g.values())
    v_cluster = K / (K - 1) * ss / N ** 2
    v_binom = p * (1 - p) / N
    return {"n": N, "groups": K, "rate": p, "deff": v_cluster / v_binom}


def rho_of(groups_dict):
    return cm.icc(groups_dict)


def permute_within(rows, cellfn, draws, seed, group_of):
    """Null: shuffle the absence labels WITHIN each cell, keeping the group structure fixed.

    This is a permutation, not a resample: the number of absences in each cell is held exactly,
    so nothing about the cell's own rate can drive the result. The statistic is the intra-class
    correlation over `group_of`.
    """
    rng = random.Random(seed)
    cells = {}
    for i, r in enumerate(rows):
        cells.setdefault(cellfn(r), []).append(i)
    gidx = {}
    for i, r in enumerate(rows):
        k = group_of(r)
        if k is not None:
            gidx.setdefault(k, []).append(i)
    obs = rho_of({k: [rows[i] for i in ii] for k, ii in gidx.items()})
    labels = [r["absent"] for r in rows]
    sims = []
    for _ in range(draws):
        draw = list(labels)
        for ii in cells.values():
            vals = [labels[i] for i in ii]
            rng.shuffle(vals)
            for i, v in zip(ii, vals):
                draw[i] = v
        g = {k: [{"absent": draw[i]} for i in ii] for k, ii in gidx.items()}
        v = rho_of(g)
        if v is not None:
            sims.append(v)
    sims.sort()
    ge = sum(1 for s in sims if s >= obs)
    return {"observed_rho": obs, "draws": len(sims),
            "null_mean": sum(sims) / len(sims),
            "null_p95": sims[int(0.95 * len(sims))], "null_max": sims[-1],
            "n_ge_observed": ge, "p_value": (ge + 1) / (len(sims) + 1)}


def main():
    d, rows, excl, key = cm.load(RUN)
    idx = ck.page_index()
    for r in rows:
        r["page"] = idx.get(r["vid"])
        r["created"] = int(r["vid"]) >> 32
        r["week"] = r["created"] // WEEK_S
    att = [r for r in rows if r["page"]]

    out = {"session": 115, "run": RUN, "no_new_requests": True,
           "population": {"analysable": len(rows), "with_a_citing_page": len(att),
                          "excluded_from_load": excl}}

    # ---------------- 1. the article itself, in full ---------------------------------------
    heaviest = "es.wikipedia.org|Protestas en Paraguay de 2023"
    art = sorted([r for r in att if r["page"] == heaviest], key=lambda r: r["created"])
    out["heaviest_page"] = {
        "key": heaviest,
        "units": len(art),
        "absent": sum(r["absent"] for r in art),
        "distinct_handles": len(set(r["handle"] for r in art)),
        "creation_span_days": round(
            (art[-1]["created"] - art[0]["created"]) / 86400, 2) if len(art) > 1 else None,
        "videos": [{"vid": r["vid"], "handle": r["handle"],
                    "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(r["created"])),
                    "absent": r["absent"], "arm": r["arm"]} for r in art],
    }
    absent_days = [r["created"] / 86400 for r in art if r["absent"]]
    present_days = [r["created"] / 86400 for r in art if not r["absent"]]

    def spread(xs):
        if len(xs) < 2:
            return None
        m = sum(xs) / len(xs)
        return round(math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1)), 3)
    out["heaviest_page"]["creation_sd_days_absent"] = spread(absent_days)
    out["heaviest_page"]["creation_sd_days_present"] = spread(present_days)
    out["heaviest_page"]["note"] = (
        "Creation dates are decoded from the identifiers by this arc's stated dating rule "
        "(created = int(vid) >> 32), validated at session 109 against the dark dashboard's own "
        "displayed dates, 9 of 11 to within 60 seconds. Absence is public retrievability from one "
        "vantage on 2026-08-12 and never means deletion.")

    # ---------------- 2. how much of the page effect is that one article? ------------------
    gp_all = ck.by_page(att, idx)
    gh_all = cm.groups(att)
    out["design_effects"] = {
        "page_key_all": deff_analytic(gp_all),
        "account_key_all": deff_analytic(gh_all),
    }
    sizes = sorted(((len(v), k) for k, v in gp_all.items()), reverse=True)[:10]
    out["largest_pages"] = [
        {"key": k, "units": n, "absent": sum(r["absent"] for r in gp_all[k]),
         "distinct_handles": len(set(r["handle"] for r in gp_all[k]))} for n, k in sizes]

    # ---------------- 3. the two nulls, on the page key ------------------------------------
    band_of = {}
    for r in att:
        band_of[r["vid"]] = (r["arm"], r["band"])
    out["null_page_within_ageband_arm"] = permute_within(
        att, lambda r: (r["arm"], r["band"]), DRAWS, SEED, lambda r: r["page"])
    out["null_page_within_creation_week"] = permute_within(
        att, lambda r: r["week"], DRAWS, SEED + 1, lambda r: r["page"])
    out["null_page_within_account"] = permute_within(
        att, lambda r: r["handle"], DRAWS, SEED + 2, lambda r: r["page"])
    # and the mirror image: does the ACCOUNT effect survive permuting within page?
    out["null_account_within_page"] = permute_within(
        att, lambda r: r["page"], DRAWS, SEED + 3, lambda r: r["handle"])

    # ---------------- 4. the same, with the one article removed ----------------------------
    att2 = [r for r in att if r["page"] != heaviest]
    out["without_the_heaviest_page"] = {
        "n": len(att2),
        "page_key_deff": deff_analytic(ck.by_page(att2, idx)),
        "account_key_deff": deff_analytic(cm.groups(att2)),
        "null_page_within_ageband_arm": permute_within(
            att2, lambda r: (r["arm"], r["band"]), DRAWS, SEED + 4, lambda r: r["page"]),
    }

    json.dump(out, open("page-mechanism-115.json", "w"), indent=1, ensure_ascii=False)

    h = out["heaviest_page"]
    print(f"heaviest page {h['key']}: {h['units']} units, {h['absent']} absent, "
          f"{h['distinct_handles']} handles, creation span {h['creation_span_days']} days")
    print(f"  creation sd (days) absent={h['creation_sd_days_absent']} "
          f"present={h['creation_sd_days_present']}")
    print(f"page DEFF {out['design_effects']['page_key_all']['deff']:.4f}  "
          f"account DEFF {out['design_effects']['account_key_all']['deff']:.4f}")
    for k in ("null_page_within_ageband_arm", "null_page_within_creation_week",
              "null_page_within_account", "null_account_within_page"):
        v = out[k]
        print(f"  {k}: rho={v['observed_rho']:.4f} null_mean={v['null_mean']:.4f} "
              f"p95={v['null_p95']:.4f} p={v['p_value']:.5f}")
    w = out["without_the_heaviest_page"]
    print(f"without that article: page DEFF {w['page_key_deff']['deff']:.4f} "
          f"account DEFF {w['account_key_deff']['deff']:.4f} "
          f"p={w['null_page_within_ageband_arm']['p_value']:.5f}")


if __name__ == "__main__":
    sys.exit(main())
