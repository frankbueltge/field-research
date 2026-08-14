#!/usr/bin/env python3
"""The account-state probe of PREREGISTRATION-117B-account-state.md, run at session 118.

Population, statistic, predictions and kill criteria were committed 2026-08-13, before any
response existed. Nothing in this file changes them; it only builds the three groups the
pre-registration fixed and calls the session-114 probe unchanged.

  T  (n=20) every distinct account cited by es.wikipedia.org|Protestas en Paraguay de 2023
  C1 (n=41) accounts not on that page, ALL of whose cited units in this corpus are absent,
            holding at least one unit in the target's cell (3-4y, W-article) — all of them
  C2 (n=41) accounts not on that page, NONE of whose cited units are absent, same cell —
            drawn with random.Random(117001), the seed fixed in the pre-registration

102 requests, one per account, at the account endpoint, never the video route. This is NOT
part of the window population: `ledger/`, `manifest-day2-onward.json` and `ledger.py` are not
touched, and nothing here reclassifies any ledger unit.

Usage: python3 probe_117b.py [run.json]
"""
import json
import random
import sys
import time

from cluster_model import load
from cluster_keys import page_index
from probe_account_state import probe, UA, DELAY, TIMEOUT

PAGE = "es.wikipedia.org|Protestas en Paraguay de 2023"
CELL = ("3-4y", "W-article")


def build(run_path):
    d, rows, excl, key = load(run_path)
    idx = page_index()
    for r in rows:
        r["page"] = idx.get(r["vid"])

    target_handles, on_page = [], set()
    for r in rows:
        if r["page"] == PAGE:
            on_page.add(r["handle"])
    target_handles = sorted(on_page)

    by_handle = {}
    for r in rows:
        by_handle.setdefault(r["handle"], []).append(r)

    c1_pool, c2_pool = [], []
    for h, v in by_handle.items():
        if h in on_page:
            continue
        if not any((r["band"], r["stratum"]) == CELL for r in v):
            continue
        a = sum(r["absent"] for r in v)
        if a == len(v):
            c1_pool.append(h)
        elif a == 0:
            c2_pool.append(h)
    c1_pool.sort()
    c2_pool.sort()

    c1 = list(c1_pool)                       # all of them, no sampling, no seed
    rng = random.Random(117001)
    c2 = rng.sample(c2_pool, 41) if len(c2_pool) >= 41 else list(c2_pool)

    return d, rows, {
        "T": target_handles, "C1": c1, "C2": c2,
        "pool_sizes": {"T": len(target_handles), "C1_pool": len(c1_pool),
                       "C2_pool": len(c2_pool)},
    }


def fisher_two_sided(a, b, c, d_):
    """Exact two-sided Fisher on the 2x2 [[a,b],[c,d]], by the total-probability rule."""
    from math import comb
    n = a + b + c + d_
    r1, r2, c1_ = a + b, c + d_, a + c
    def p(x):
        return comb(r1, x) * comb(r2, c1_ - x) / comb(n, c1_)
    obs = p(a)
    lo = max(0, c1_ - r2)
    hi = min(r1, c1_)
    return min(1.0, sum(p(x) for x in range(lo, hi + 1) if p(x) <= obs * (1 + 1e-9)))


def main(run_path):
    d, rows, pop = build(run_path)
    print(json.dumps(pop["pool_sizes"]))
    out = []
    stopped = None
    for grp in ("T", "C1", "C2"):
        for h in pop[grp]:
            r = probe(h)
            r.update({"handle": h, "group": grp})
            out.append(r)
            print(json.dumps({k: r.get(k) for k in
                              ("group", "handle", "http", "status_field",
                               "unique_id_returned", "bytes")}))
            # K3: a rate-limit or challenge stops the run at that point
            if r.get("http") in (429, 403) or (r.get("http") == 200
                                               and r.get("bytes", 10 ** 6) < 20000):
                stopped = {"at": len(out), "handle": h, "group": grp, "http": r.get("http"),
                           "bytes": r.get("bytes")}
                break
            time.sleep(DELAY)
        if stopped:
            break

    tab, codes = {}, {}
    for r in out:
        g = r["group"]
        s = r.get("status_field")
        tab.setdefault(g, {"n": 0, "readable": 0, "nonzero": 0})
        tab[g]["n"] += 1
        if s is not None:
            tab[g]["readable"] += 1
            if s != 0:
                tab[g]["nonzero"] += 1
        codes.setdefault(g, {})
        codes[g][str(s)] = codes[g].get(str(s), 0) + 1
    for g, t in tab.items():
        t["nonzero_share"] = t["nonzero"] / t["readable"] if t["readable"] else None

    test = None
    if tab.get("T", {}).get("readable") and tab.get("C1", {}).get("readable"):
        a = tab["T"]["nonzero"]; b = tab["T"]["readable"] - a
        c = tab["C1"]["nonzero"]; dd = tab["C1"]["readable"] - c
        test = {"table_T_vs_C1": [[a, b], [c, dd]],
                "fisher_two_sided_p": fisher_two_sided(a, b, c, dd)}
    test2 = None
    if tab.get("T", {}).get("readable") and tab.get("C2", {}).get("readable"):
        a = tab["T"]["nonzero"]; b = tab["T"]["readable"] - a
        c = tab["C2"]["nonzero"]; dd = tab["C2"]["readable"] - c
        test2 = {"table_T_vs_C2": [[a, b], [c, dd]],
                 "fisher_two_sided_p": fisher_two_sided(a, b, c, dd)}
    test3 = None
    if tab.get("C1", {}).get("readable") and tab.get("C2", {}).get("readable"):
        a = tab["C1"]["nonzero"]; b = tab["C1"]["readable"] - a
        c = tab["C2"]["nonzero"]; dd = tab["C2"]["readable"] - c
        test3 = {"table_C1_vs_C2": [[a, b], [c, dd]],
                 "fisher_two_sided_p": fisher_two_sided(a, b, c, dd)}

    payload = {
        "schema": "field-research/account-state-probe/2", "session": 118,
        "preregistration": "PREREGISTRATION-117B-account-state.md, committed 2026-08-13",
        "run_source": run_path, "page": PAGE, "cell": list(CELL),
        "collected_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "endpoint": "https://www.tiktok.com/@<handle>", "user_agent": UA,
        "delay_s": DELAY, "timeout_s": TIMEOUT, "requests": len(out),
        "population": {k: pop[k] for k in ("T", "C1", "C2")},
        "pool_sizes": pop["pool_sizes"],
        "k3_stopped": stopped,
        "by_group": tab, "codes_by_group": codes,
        "primary_T_vs_C1": test, "secondary_T_vs_C2": test2, "descriptive_C1_vs_C2": test3,
        "no_code_table_published": ("This practice found no published table mapping the numeric "
                                    "state to a cause; nothing is read into it beyond 'the "
                                    "account object is not served'."),
        "results": out,
    }
    json.dump(payload, open("account-state-117b.json", "w"), indent=1)
    print(json.dumps({"by_group": tab, "primary": test, "secondary": test2,
                      "c1_vs_c2": test3, "k3": stopped}, indent=1))
    print("wrote account-state-117b.json")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "ledger/run-2026-08-13T0427Z.json")
