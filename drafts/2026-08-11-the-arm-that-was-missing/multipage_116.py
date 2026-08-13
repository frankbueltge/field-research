#!/usr/bin/env python3
"""The simplification inside the page key, measured rather than hoped about.

Session 116, 2026-08-13. No new requests.

`cluster_keys.page_index` assigns each video to ONE citing page — the first the corpus files
happen to yield (`idx.setdefault`). A video cited by several pages therefore contributes to the
page key as though it had one citer. That is a partition imposed on a structure that is really a
hypergraph, and it can only LOSE page-level dependence, never invent it.

Two questions, both answerable from files already collected:

  1. How much of the corpus is multiply cited at all?
  2. Does the dependence structure change if every citation is used? The crossed design effect
     itself needs a partition and cannot be recomputed this way, but the COMPONENT ENVELOPE can:
     connectivity does not care whether a unit belongs to one page or five, so components can be
     built over every (video, page) edge and the envelope recomputed.

Usage: python3 multipage_116.py
"""
import glob
import json

from cluster_model import load
from cluster_keys import page_index
from crossed_model import agg, stats

RUN = "ledger/run-2026-08-13T0427Z.json"
SINGLE_MEMBERSHIP_COMPONENTS = 2394           # crossed-116.json, primary.components.count
SINGLE_MEMBERSHIP_ENVELOPE = 1.9414419490049107  # ... .components.deff_component_key


def all_pages():
    """vid -> EVERY page or thread that cites it, from the same corpus files page_index reads."""
    pages = {}

    def add(vid, key):
        pages.setdefault(str(vid), set()).add(key)

    for f in glob.glob("corpus-*.wikipedia.org.json"):
        d = json.load(open(f))
        wiki = d["meta"]["wiki"]
        for r in d["rows"]:
            add(r["vid"], f"{wiki}|{r['page']}")
    for f in ("expansion-111/corpus-round2.json", "expansion-111/corpus-round3.json",
              "expansion-111/corpus-A2-namespaces.json"):
        try:
            d = json.load(open(f))
        except FileNotFoundError:
            continue
        for r in d.get("rows", []):
            add(r["vid"], f"{r.get('wiki','?')}|{r.get('page','?')}")
    try:
        for r in json.load(open("corpus-hn.json"))["rows"]:
            add(r["vid"], "forum|" + str(r.get("hn_object_id")))
    except FileNotFoundError:
        pass
    try:
        for r in json.load(open("expansion-111/new-editions.json"))["rows"]:
            add(r["vid"], f"{r.get('src','?')}|{r.get('page','?')}")
    except FileNotFoundError:
        pass
    return pages


def main():
    pages = all_pages()
    _, rows_all, _, _ = load(RUN)
    pidx = page_index()
    rows = [r for r in rows_all if r["vid"] in pidx]
    N, A = len(rows), sum(r["absent"] for r in rows)

    multi = [r for r in rows if len(pages.get(r["vid"], ())) > 1]
    counts = [len(pages.get(r["vid"], {pidx[r["vid"]]})) for r in rows]

    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for r in rows:
        union(("a", r["handle"]), ("v", r["vid"]))
        for p in pages.get(r["vid"], {pidx[r["vid"]]}):
            union(("v", r["vid"]), ("p", p))

    comp = {}
    for r in rows:
        comp.setdefault(find(("v", r["vid"])), []).append(r)
    comps = sorted(comp.values(), key=len, reverse=True)
    cmap = {x["vid"]: i for i, c in enumerate(comps) for x in c}
    ag = agg(rows, lambda r: cmap[r["vid"]])
    s = stats(N, A, ag, ag, ag, fpc=False)

    out = {
        "session": 116, "run": RUN, "units_in_analysis": N, "absent": A,
        "units_cited_on_more_than_one_page": len(multi),
        "share_multiply_cited": len(multi) / N,
        "max_pages_for_one_unit": max(counts),
        "absent_among_multiply_cited": sum(r["absent"] for r in multi),
        "absence_rate_multiply_cited": sum(r["absent"] for r in multi) / len(multi),
        "absence_rate_pooled": A / N,
        "components_single_membership": SINGLE_MEMBERSHIP_COMPONENTS,
        "components_full_membership": len(comps),
        "largest_component_full_membership": len(comps[0]),
        "largest_share_full_membership": len(comps[0]) / N,
        "envelope_single_membership": SINGLE_MEMBERSHIP_ENVELOPE,
        "envelope_full_membership": s["deff_account_only"],
        "envelope_difference": s["deff_account_only"] - SINGLE_MEMBERSHIP_ENVELOPE,
    }
    json.dump(out, open("multipage-116.json", "w"), indent=1)
    print(f"multiply cited: {out['units_cited_on_more_than_one_page']} of {N} = "
          f"{100*out['share_multiply_cited']:.2f}%, up to {out['max_pages_for_one_unit']} pages")
    print(f"absence rate among them {100*out['absence_rate_multiply_cited']:.2f}% against pooled "
          f"{100*out['absence_rate_pooled']:.2f}%")
    print(f"components {SINGLE_MEMBERSHIP_COMPONENTS} -> {out['components_full_membership']}, "
          f"largest {out['largest_component_full_membership']} units")
    print(f"envelope {SINGLE_MEMBERSHIP_ENVELOPE:.4f} -> {out['envelope_full_membership']:.4f} "
          f"(+{out['envelope_difference']:.4f})")
    print("wrote multipage-116.json")


if __name__ == "__main__":
    main()
