#!/usr/bin/env python3
"""Scoring PREREGISTRATION-117B-account-state.md against its own run, plus the one derived
question the probe makes answerable — and it is labelled post-hoc because it is.

Pre-registered part (§6, §7): Q1-Q5 and K1-K4, scored exactly as written on 2026-08-13.

Post-hoc part, declared as such: the pre-registration compares T (every account cited by the
article, whatever its videos did) against C1 (accounts ALL of whose corpus videos are absent).
Those are not like-for-like unless T's accounts are themselves all-gone. This splits T by its
own corpus behaviour and puts each part beside the control that matches it, and it counts how
many of the article's absent units belong to accounts the platform still serves — the units
account death cannot explain at all.

No design effect appears anywhere in this file and no interval on a rate is computed, so
session 116's stopping commitment is untouched. Nothing here reclassifies any ledger unit.

Usage: python3 derive_117b.py
"""
import json

from cluster_model import load
from cluster_keys import page_index
from probe_117b import PAGE, CELL, fisher_two_sided

probe = json.load(open("account-state-117b.json"))
state = {r["handle"]: r.get("status_field") for r in probe["results"]}
grp_of = {r["handle"]: r["group"] for r in probe["results"]}

d, rows, excl, key = load("ledger/run-2026-08-13T0427Z.json")
idx = page_index()
for r in rows:
    r["page"] = idx.get(r["vid"])

# ---- the pre-registered scoring -------------------------------------------------------
bg = probe["by_group"]
Q = {
    "Q1": {"claim": "fewer than half of T's 20 accounts return a non-zero state",
           "observed": f"{bg['T']['nonzero']} of {bg['T']['readable']} non-zero",
           "holds": bg["T"]["nonzero"] < bg["T"]["readable"] / 2},
    "Q2": {"claim": "T's non-zero share is lower than C1's",
           "observed": f"T {bg['T']['nonzero_share']:.4f} vs C1 {bg['C1']['nonzero_share']:.4f}",
           "holds": bg["T"]["nonzero_share"] < bg["C1"]["nonzero_share"]},
    "Q3": {"claim": "the T-against-C1 Fisher test reaches p < 0.05",
           "observed": f"p = {probe['primary_T_vs_C1']['fisher_two_sided_p']:.4f}",
           "holds": probe["primary_T_vs_C1"]["fisher_two_sided_p"] < 0.05},
    "Q4": {"claim": "C2's non-zero share is lower than C1's",
           "observed": (f"C2 {bg['C2']['nonzero_share']:.4f} vs C1 "
                        f"{bg['C1']['nonzero_share']:.4f}, Fisher p = "
                        f"{probe['descriptive_C1_vs_C2']['fisher_two_sided_p']:.3e}"),
           "holds": bg["C2"]["nonzero_share"] < bg["C1"]["nonzero_share"]},
    "Q5": {"claim": "at least 95 of the 102 requests return a readable state field",
           "observed": f"{sum(g['readable'] for g in bg.values())} of {probe['requests']}",
           "holds": sum(g["readable"] for g in bg.values()) >= 95},
}
K = {
    "K1": {"claim": "fewer than 80 of 102 return a readable state field -> no verdict",
           "fired": sum(g["readable"] for g in bg.values()) < 80},
    "K2": {"claim": "C1 or C2 below 30 accounts -> underpowered, not a null",
           "fired": min(bg["C1"]["n"], bg["C2"]["n"]) < 30},
    "K3": {"claim": "rate-limit or challenge -> stop and publish partial counts",
           "fired": probe["k3_stopped"] is not None},
    "K4": {"claim": "if Q4 fails the instrument is uninformative and NO conclusion about T is "
                    "drawn", "fired": not Q["Q4"]["holds"]},
}

# ---- post-hoc: T's own composition, and the units account death cannot explain ---------
by_handle = {}
for r in rows:
    by_handle.setdefault(r["handle"], []).append(r)

T = probe["population"]["T"]
comp = {"all-gone": [], "mixed": [], "all-present": []}
for h in T:
    v = by_handle.get(h, [])
    a = sum(x["absent"] for x in v)
    lab = "all-gone" if a == len(v) and v else ("all-present" if a == 0 else "mixed")
    comp[lab].append({"handle": h, "n_units": len(v), "n_absent": a,
                      "state": state[h], "dead": state[h] != 0})

page_rows = [r for r in rows if r["page"] == PAGE]
cross = {"absent_dead": 0, "absent_alive": 0, "present_dead": 0, "present_alive": 0}
for r in page_rows:
    dead = state.get(r["handle"], 0) != 0
    cross[("absent_" if r["absent"] else "present_") + ("dead" if dead else "alive")] += 1

# like-for-like: T's all-gone accounts against C1 (all-gone by construction), and T's
# all-present accounts against C2 (all-present by construction)
def share(lst):
    n = len(lst)
    dead = sum(1 for x in lst if x["dead"])
    return {"n": n, "dead": dead, "share": dead / n if n else None}

t_gone, t_pres, t_mixed = share(comp["all-gone"]), share(comp["all-present"]), share(comp["mixed"])
lfl = {}
if t_gone["n"]:
    a, b = t_gone["dead"], t_gone["n"] - t_gone["dead"]
    c, dd = bg["C1"]["nonzero"], bg["C1"]["readable"] - bg["C1"]["nonzero"]
    lfl["T_allgone_vs_C1"] = {"table": [[a, b], [c, dd]],
                              "fisher_two_sided_p": fisher_two_sided(a, b, c, dd)}
if t_pres["n"]:
    a, b = t_pres["dead"], t_pres["n"] - t_pres["dead"]
    c, dd = bg["C2"]["nonzero"], bg["C2"]["readable"] - bg["C2"]["nonzero"]
    lfl["T_allpresent_vs_C2"] = {"table": [[a, b], [c, dd]],
                                 "fisher_two_sided_p": fisher_two_sided(a, b, c, dd)}

# the residual: what is left of the article's excess once the units whose account the platform
# no longer serves are set aside. The reference rates are session 117's leave-one-page-out cell
# rates, which are UNCONDITIONAL on account state — no corpus-wide account census exists, so
# this is an excess against the ordinary population, not against a live-account population.
import coloss_117 as cl

pages, meta = cl.scan(rows, idx, 5)
target = next(p for p in pages if p["page"] == PAGE)
att = [r for r in rows if r["vid"] in idx]
by_page_units = [r for r in sorted(att, key=lambda r: idx[r["vid"]]) if idx[r["vid"]] == PAGE]
# rebuild the same order scan() used: it iterates `by_page[page]` in insertion order over rows
order = [r for r in att if idx[r["vid"]] == PAGE]
assert len(order) == len(target["_ps"]) == target["n"]

alive_ps, alive_a, dead_ps, dead_a = [], 0, [], 0
for r, p in zip(order, target["_ps"]):
    if state.get(r["handle"], 0) == 0:
        alive_ps.append(p)
        alive_a += r["absent"]
    else:
        dead_ps.append(p)
        dead_a += r["absent"]
up_alive, low_alive = cl.tails(alive_ps, alive_a)
residual = {
 "page_total": {"n": target["n"], "absent": target["absent"], "expected": target["expected"],
                "p_upper": target["p_upper"]},
 "account_still_served": {"n": len(alive_ps), "absent": alive_a, "expected": sum(alive_ps),
                          "ratio": alive_a / sum(alive_ps) if sum(alive_ps) else None,
                          "p_upper_exact": up_alive, "p_lower_exact": low_alive},
 "account_not_served": {"n": len(dead_ps), "absent": dead_a, "expected": sum(dead_ps)},
 "caveat": ("the expectation is unconditional on account state; no corpus-wide account census "
            "exists, so this compares live-account units against the ordinary cell rate, not "
            "against a live-account cell rate. Post-hoc, and the split was chosen after the "
            "probe was read."),
}

out = {
 "schema": "field-research/account-state-117b-derived/1", "session": 118,
 "date": "2026-08-14",
 "source_probe": "account-state-117b.json",
 "source_run": "ledger/run-2026-08-13T0427Z.json (day 3) — no new request of any instrument",
 "preregistered_scoring": {"predictions": Q, "kill_criteria": K},
 "posthoc_declared": {
   "why": ("the pre-registration compares T against C1 without matching on T's own corpus "
           "behaviour; this section was written after the run and is descriptive"),
   "T_composition_in_corpus": {k: v for k, v in comp.items()},
   "T_shares": {"all-gone": t_gone, "mixed": t_mixed, "all-present": t_pres},
   "like_for_like": lfl,
   "page_units_by_absence_and_account_state": cross,
   "page_units_total": len(page_rows),
   "residual_excess": residual,
 },
 "cell": list(CELL), "page": PAGE,
}
json.dump(out, open("derived-117b.json", "w"), indent=1)
print(json.dumps({"Q": {k: v["holds"] for k, v in Q.items()},
                  "K": {k: v["fired"] for k, v in K.items()},
                  "T_shares": out["posthoc_declared"]["T_shares"],
                  "cross": cross, "lfl": lfl}, indent=1))
print("wrote derived-117b.json")
