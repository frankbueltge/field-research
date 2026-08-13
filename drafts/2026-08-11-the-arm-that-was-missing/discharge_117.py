#!/usr/bin/env python3
"""Discharging the domain specialist's qualifications on the session-117 scan.

Session 117, 2026-08-13. Every figure the specialist reported is recomputed here with this
practice's own code FIRST, before any of it is quoted (the standing check of session 116:
where a figure exists both in a file we computed and in a document someone else wrote, the
prose quotes ours and names theirs beside it).

Three items, in the specialist's own order of value:

  (2) THE POOLED / LEAVE-ONE-OUT INCONSISTENCY. `coloss_power_117.py::detectability()` used
      POOLED cell rates while the scan itself used leave-one-page-out. Two output files
      therefore disagree about "expected" for the same page and run, with no cross-reference.
      Recomputed here both ways, and the difference is published.

  (4) BENJAMINI-YEKUTIELI. BH is proven under independence or PRDS; these p-values share
      nuisance-parameter estimates and PRDS is not demonstrated. BY needs no such assumption.

  (3) INTERNAL-REFERENCE CONTAMINATION. Leave-one-page-out removes the tested page's own
      contribution to its baseline. It does NOT remove contamination from OTHER small pages
      (n < 5, never scanned) sitting in the same narrow cell. Measured.

NOT DONE HERE, AND THE REASON IS A COMMITMENT, NOT AN OVERSIGHT: the specialist's first
recommendation is to extend this arc's account-level intra-class machinery to the page level,
so a page-level effective-n accompanies the exact tail. Session 116 committed in the record
that no further clustering dimension enters this arc's variance treatment before the window
closes on 2026-08-18. That commitment is honoured; the recommendation is filed for after.

Usage: python3 discharge_117.py
"""
import collections
import json

import cluster_keys as ck
import cluster_model as cm
from coloss_117 import MIN_CELL, N_MIN, PARAGUAY, bh, cell_of, tails

RUN = "ledger/run-2026-08-13T0427Z.json"
JA = "ja.wikipedia.org|瀬乃真帆子"


def by_benjamini_yekutieli(pvals, q=0.05):
    """BY: BH with the p-values inflated by the harmonic number c(m). No PRDS assumed."""
    m = len(pvals)
    c = sum(1.0 / i for i in range(1, m + 1))
    order = sorted(range(m), key=lambda i: pvals[i])
    qv = [1.0] * m
    running = 1.0
    for rank in range(m, 0, -1):
        i = order[rank - 1]
        running = min(running, pvals[i] * m * c / rank)
        qv[i] = running
    return {"c_m": c, "rejected": {i for i in range(m) if qv[i] < q}, "q": qv}


def pages_and_rates(rows, idx):
    att = [r for r in rows if r["vid"] in idx]
    by_page = collections.defaultdict(list)
    for r in att:
        by_page[idx[r["vid"]]].append(r)
    n_cell = collections.Counter()
    a_cell = collections.Counter()
    for r in att:
        n_cell[cell_of(r)] += 1
        a_cell[cell_of(r)] += r["absent"]
    return att, by_page, n_cell, a_cell


def ps_for(units, n_cell, a_cell, loo):
    """Cell probabilities for one page's units; leave-one-page-out if loo is True."""
    pn = collections.Counter()
    pa = collections.Counter()
    if loo:
        for r in units:
            pn[cell_of(r)] += 1
            pa[cell_of(r)] += r["absent"]
    out = []
    for r in units:
        c = cell_of(r)
        n = n_cell[c] - pn[c]
        out.append((a_cell[c] - pa[c]) / n if n >= MIN_CELL else a_cell[c] / n_cell[c])
    return out


def detect_sweep(by_page, n_cell, a_cell, loo):
    scanned = {k: v for k, v in by_page.items() if len(v) >= N_MIN}
    alpha = 0.05 / len(scanned)
    rows = []
    for page, units in scanned.items():
        ps = ps_for(units, n_cell, a_cell, loo)
        need = next((a for a in range(len(units) + 1) if tails(ps, a)[0] <= alpha), None)
        rows.append({"page": page, "n": len(units), "expected": sum(ps),
                     "min_detectable_absent": need,
                     "min_detectable_excess": None if need is None else need - sum(ps),
                     "min_detectable_share": None if need is None else need / len(units)})
    sh = sorted(r["min_detectable_share"] for r in rows if r["min_detectable_share"])
    ex = sorted(r["min_detectable_excess"] for r in rows if r["min_detectable_excess"])
    return {"loo": loo, "alpha": alpha, "pages": len(rows),
            "median_share": sh[len(sh) // 2], "min_share": sh[0], "max_share": sh[-1],
            "median_excess": ex[len(ex) // 2],
            "paraguay": next(r for r in rows if r["page"] == PARAGUAY),
            "undetectable_at_any_count": sum(1 for r in rows
                                             if r["min_detectable_absent"] is None)}


def cell_contamination(by_page, n_cell, a_cell, page_key):
    """How much of the tested page's reference cell is other SMALL, never-scanned pages?"""
    units = by_page[page_key]
    cells = collections.Counter(cell_of(r) for r in units)
    out = []
    for c, k in cells.items():
        small_n = small_a = big_n = big_a = 0
        for p, us in by_page.items():
            if p == page_key:
                continue
            for r in us:
                if cell_of(r) != c:
                    continue
                if len(us) < N_MIN:
                    small_n += 1
                    small_a += r["absent"]
                else:
                    big_n += 1
                    big_a += r["absent"]
        out.append({
            "cell": list(c), "units_of_tested_page_in_cell": k,
            "reference_units_total": small_n + big_n,
            "reference_units_from_pages_under_5": small_n,
            "share_of_reference_from_pages_under_5":
                small_n / (small_n + big_n) if (small_n + big_n) else None,
            "absence_rate_in_small_pages": small_a / small_n if small_n else None,
            "absence_rate_in_scanned_pages": big_a / big_n if big_n else None,
            "leave_one_out_rate_used": (small_a + big_a) / (small_n + big_n)
                                       if (small_n + big_n) else None})
    return out


def main():
    d, rows, excl, key = cm.load(RUN)
    idx = ck.page_index()
    att, by_page, n_cell, a_cell = pages_and_rates(rows, idx)
    scanned = sorted(k for k, v in by_page.items() if len(v) >= N_MIN)

    pv, meta = [], []
    for page in scanned:
        units = by_page[page]
        ps = ps_for(units, n_cell, a_cell, True)
        a = sum(r["absent"] for r in units)
        up, low = tails(ps, a)
        pv.append(up)
        meta.append({"page": page, "n": len(units), "absent": a, "expected": sum(ps),
                     "p_upper": up})
    rej_bh, q_bh = bh(pv)
    by = by_benjamini_yekutieli(pv)

    flags_bh = sorted((meta[i]["page"] for i in rej_bh))
    flags_by = sorted((meta[i]["page"] for i in by["rejected"]))
    i_par = next(i for i, m in enumerate(meta) if m["page"] == PARAGUAY)
    i_ja = next(i for i, m in enumerate(meta) if m["page"] == JA)

    loo = detect_sweep(by_page, n_cell, a_cell, True)
    pooled = detect_sweep(by_page, n_cell, a_cell, False)

    out = {
        "schema": "field-research/discharge-117/1", "session": 117, "run": RUN,
        "note": "recomputed with this practice's own code before any specialist figure is quoted",
        "item4_multiplicity": {
            "m": len(pv), "c_m_harmonic": by["c_m"],
            "bh_flagged": flags_bh, "by_flagged": flags_by,
            "same_set": flags_bh == flags_by,
            "paraguay": {"p_upper": pv[i_par], "q_bh": q_bh[i_par], "q_by": by["q"][i_par]},
            "ja": {"p_upper": pv[i_ja], "q_bh": q_bh[i_ja], "q_by": by["q"][i_ja]}},
        "item2_detectability_pooled_vs_loo": {
            "leave_one_page_out": loo, "pooled": pooled,
            "paraguay_expected_loo": loo["paraguay"]["expected"],
            "paraguay_expected_pooled": pooled["paraguay"]["expected"],
            "paraguay_expected_relative_gap":
                pooled["paraguay"]["expected"] / loo["paraguay"]["expected"] - 1},
        "item3_reference_contamination": {
            "paraguay": cell_contamination(by_page, n_cell, a_cell, PARAGUAY),
            "ja": cell_contamination(by_page, n_cell, a_cell, JA)},
        "item1_page_level_effective_n": {
            "computed": False,
            "reason": ("session 116 committed that no further clustering dimension enters this "
                       "arc's variance treatment before the window closes 2026-08-18; the "
                       "specialist's first recommendation is filed for after that date")},
    }
    json.dump(out, open("discharge-117.json", "w"), indent=1)

    m4 = out["item4_multiplicity"]
    print(f"ITEM 4  m={m4['m']}  c(m)={m4['c_m_harmonic']:.4f}")
    print(f"  BH flags {len(flags_bh)}   BY flags {len(flags_by)}   same set: {m4['same_set']}")
    print(f"  Paraguay  p {m4['paraguay']['p_upper']:.4e}  q_BH {m4['paraguay']['q_bh']:.4e}  "
          f"q_BY {m4['paraguay']['q_by']:.4e}")
    print(f"  ja        p {m4['ja']['p_upper']:.4e}  q_BH {m4['ja']['q_bh']:.4e}  "
          f"q_BY {m4['ja']['q_by']:.4e}")
    m2 = out["item2_detectability_pooled_vs_loo"]
    for tag in ("leave_one_page_out", "pooled"):
        s = m2[tag]
        print(f"ITEM 2  {tag:20s} median share {100*s['median_share']:.1f} %  "
              f"range [{100*s['min_share']:.1f}, {100*s['max_share']:.1f}]  "
              f"median excess {s['median_excess']:.4f}  "
              f"Paraguay needs {s['paraguay']['min_detectable_absent']} "
              f"(expected {s['paraguay']['expected']:.4f})")
    print(f"ITEM 2  Paraguay expected pooled/LOO gap "
          f"{100*m2['paraguay_expected_relative_gap']:.2f} %")
    for c in out["item3_reference_contamination"]["paraguay"]:
        print(f"ITEM 3  cell {c['cell']}  reference {c['reference_units_total']} units, "
              f"{c['reference_units_from_pages_under_5']} from pages < 5 "
              f"({100*c['share_of_reference_from_pages_under_5']:.1f} %); "
              f"absence small {100*c['absence_rate_in_small_pages']:.2f} % vs scanned "
              f"{100*c['absence_rate_in_scanned_pages']:.2f} %; LOO rate used "
              f"{100*c['leave_one_out_rate_used']:.2f} %")
    print("wrote discharge-117.json")


if __name__ == "__main__":
    main()
