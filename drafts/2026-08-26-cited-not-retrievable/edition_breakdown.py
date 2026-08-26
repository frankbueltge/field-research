#!/usr/bin/env python3
"""edition_breakdown - what the running instrument already knows, split by the citing encyclopedia.

Session 136, 2026-08-26. The first checkable increment of the concept gated today, and it is
computed OFFLINE from files already committed in this repository: no new corpus, no new fetch, no
new infrastructure. That constraint is `PREREGISTRATION-136.md` K-B, locked before this file was
written, and it is why this script makes no request of any kind.

WHAT IT JOINS
    ../2026-08-11-the-arm-that-was-missing/corpus-*.json            (the session-109 collection)
    ../2026-08-11-the-arm-that-was-missing/expansion-111/corpus-*.json  (the session-111 expansion)
        -> identifier -> {(wiki, namespace, page)} : where in the encyclopedia the citation sits
    ../2026-08-11-the-arm-that-was-missing/ledger/run-<DAY>T0341Z.json
        -> identifier -> RETRIEVABLE | NOT-RETRIEVABLE | INDETERMINATE on that measurement day

WHAT A STATE MEANS, AND IT IS NOT WHAT A LINK-CHECKER MEANS
    The instrument's states come from the platform's credential-free oEmbed endpoint:
    HTTP 200 -> RETRIEVABLE, HTTP 400 -> NOT-RETRIEVABLE, anything else -> INDETERMINATE
    (`../2026-08-11-the-arm-that-was-missing/ledger.py`, `classify`). NOT-RETRIEVABLE is the
    platform's single opaque refusal and means "not publicly retrievable from this vantage right
    now" - NEVER "deleted". Session 109's three-arm control established that an identifier that
    never existed returns the same 400 and that no 404 is ever returned.

THE NAMESPACE ASSUMPTION, STATED RATHER THAN BURIED
    Rows collected in session 111 carry an explicit `ns`. Rows collected in session 109 do not; the
    manifest's own arm metadata records that collection as article space ("MediaWiki exturlusage,
    21 Wikipedia language editions"). This script therefore treats an `ns`-less session-109 row as
    ns 0 AND reports every figure twice - all namespaces, and article space only - so that no
    published number rests on the assumption. If the two disagree, both are printed.

MULTIPLE CITATIONS OF ONE VIDEO
    An identifier can be cited in several editions and on several pages. Per-edition counts
    therefore sum to MORE than the distinct-identifier total, and the script prints both. Nothing
    here divides one by the other.

Usage:  python3 edition_breakdown.py <run-file> [-o out.json]
Offline. Reads committed files only, makes no request.
"""
import argparse
import collections
import glob
import hashlib
import json
import math
import os

ARC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "2026-08-11-the-arm-that-was-missing")
WIKI_ARMS = ("A", "A-new", "A2")


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def wilson(k, n, z=1.959963984540054):
    """Wilson score interval. Reported because a per-edition n of 9 is not a per-edition n of 900."""
    if n == 0:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def load_citations():
    """identifier -> list of (wiki, ns, page). Every corpus file in the arc, deduplicated."""
    paths = sorted(set(glob.glob(os.path.join(ARC, "corpus-*.json"))
                       + glob.glob(os.path.join(ARC, "expansion-111", "corpus-*.json"))))
    cites = collections.defaultdict(set)
    used = []
    for p in paths:
        try:
            d = json.load(open(p))
        except Exception:
            continue
        if not isinstance(d, dict) or "rows" not in d or "meta" not in d:
            continue
        meta = d["meta"]
        n_before = len(cites)
        for r in d["rows"]:
            if not isinstance(r, dict):
                continue          # some `rows` in this arc are bare id lists, not citation rows
            vid = r.get("vid")
            if not vid:
                continue
            wiki = r.get("wiki") or meta.get("wiki")
            if not wiki:
                continue
            ns = r.get("ns")
            ns = 0 if ns is None else int(ns)          # the stated assumption, applied here only
            cites[vid].add((wiki, ns, r.get("page") or ""))
        used.append({"path": os.path.relpath(p, os.path.dirname(os.path.abspath(__file__))),
                     "sha256": sha256(p), "rows": len(d["rows"]),
                     "new_identifiers": len(cites) - n_before})
    return cites, used


def build(run_path):
    run = json.load(open(run_path))
    states = {o["vid"]: o["state"] for o in run["observations"]
              if o.get("arm") in WIKI_ARMS}
    cites, used = load_citations()

    unattributed = sorted(v for v in states if v not in cites)

    out = {
        "schema": "field-research/edition-breakdown/1",
        "built_by": "edition_breakdown.py, session 136, 2026-08-26",
        "offline": True,
        "run_file": os.path.relpath(run_path, os.path.dirname(os.path.abspath(__file__))),
        "run_file_sha256": sha256(run_path),
        "run_utc_start": run.get("run_utc_start"),
        "vantage_asn": (run.get("vantage") or {}).get("asn"),
        "corpus_files": used,
        "arms_included": list(WIKI_ARMS),
        "arms_excluded": {"B": "Hacker News comments - a different population, not the encyclopedia",
                          "B-truncated": "display-truncated identifiers - the control arm, not videos"},
        "n_identifiers_measured": len(states),
        "n_identifiers_unattributed_to_any_edition": len(unattributed),
        "unattributed_identifiers": unattributed,
    }

    for scope, ns_filter in (("all_namespaces", None), ("article_space_only", 0)):
        # THE UNIT IS THE IDENTIFIER, INSIDE ONE EDITION. An earlier version of this script
        # counted per-edition states over CITATION ROWS while printing a distinct-identifier
        # column beside them, so a share and its n came from two different units (en: 1,343
        # identifiers against 1,414 "determinate"). Caught here before anything was published
        # from it. Row-level counts are kept, but separately and labelled.
        distinct = collections.defaultdict(set)
        pages_hit = collections.defaultdict(set)
        pages_all = collections.defaultdict(set)
        rows_by_edition = collections.Counter()
        citation_rows = collections.Counter()
        ids_in_scope = set()
        for vid, state in states.items():
            for (wiki, ns, page) in cites.get(vid, ()):
                if ns_filter is not None and ns != ns_filter:
                    continue
                ids_in_scope.add(vid)
                distinct[wiki].add(vid)
                rows_by_edition[wiki] += 1
                citation_rows[state] += 1
                pages_all[wiki].add((ns, page))
                if state == "NOT-RETRIEVABLE":
                    pages_hit[wiki].add((ns, page))

        per_edition = collections.defaultdict(collections.Counter)
        for wiki, vids in distinct.items():
            for vid in vids:
                per_edition[wiki][states[vid]] += 1

        totals = collections.Counter()
        for vid in ids_in_scope:
            totals[states[vid]] += 1
        det = totals["RETRIEVABLE"] + totals["NOT-RETRIEVABLE"]

        rows = []
        for wiki in sorted(per_edition, key=lambda w: (-len(distinct[w]), w)):
            c = per_edition[wiki]
            d = c["RETRIEVABLE"] + c["NOT-RETRIEVABLE"]
            lo, hi = wilson(c["NOT-RETRIEVABLE"], d)
            rows.append({
                "wiki": wiki,
                "distinct_identifiers": len(distinct[wiki]),
                "citation_rows": rows_by_edition[wiki],
                "unit": "distinct identifiers cited in this edition; one identifier counts once "
                        "here however many pages of this edition cite it",
                "RETRIEVABLE": c["RETRIEVABLE"],
                "NOT-RETRIEVABLE": c["NOT-RETRIEVABLE"],
                "INDETERMINATE": c["INDETERMINATE"],
                "determinate": d,
                "absent_share": (c["NOT-RETRIEVABLE"] / d) if d else None,
                "wilson95": [lo, hi],
                "pages_citing_any_of_these_videos": len(pages_all.get(wiki, ())),
                "pages_with_an_absent_citation": len(pages_hit.get(wiki, ())),
            })

        lo, hi = wilson(totals["NOT-RETRIEVABLE"], det)
        out[scope] = {
            "n_editions": len(per_edition),
            "n_distinct_identifiers": len(ids_in_scope),
            "n_citation_rows": sum(citation_rows.values()),
            "identifier_level": {
                "RETRIEVABLE": totals["RETRIEVABLE"],
                "NOT-RETRIEVABLE": totals["NOT-RETRIEVABLE"],
                "INDETERMINATE": totals["INDETERMINATE"],
                "determinate": det,
                "absent_share": (totals["NOT-RETRIEVABLE"] / det) if det else None,
                "wilson95": [lo, hi],
            },
            "citation_row_level": dict(citation_rows),
            "pages_citing_any_of_these_videos": sum(len(v) for v in pages_all.values()),
            "pages_with_at_least_one_absent_citation":
                sum(len(v) for v in pages_hit.values()),
            "share_of_those_pages_with_an_absent_citation":
                (sum(len(v) for v in pages_hit.values())
                 / sum(len(v) for v in pages_all.values()))
                if sum(len(v) for v in pages_all.values()) else None,
            "what_that_share_is_not": "NOT comparable to a whole-encyclopedia figure. The "
                "denominator is only those pages that cite one of these video identifiers, not "
                "all pages of the edition, and the numerator counts only this one platform's "
                "citations, not all broken references on the page.",
            "editions": rows,
        }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    out = build(a.run)
    text = json.dumps(out, indent=1, ensure_ascii=False)
    if a.out:
        open(a.out, "w").write(text + "\n")
        s = out["all_namespaces"]
        i = s["identifier_level"]
        print("wrote %s" % a.out)
        print("all namespaces: %d editions, %d distinct identifiers, %d citation rows"
              % (s["n_editions"], s["n_distinct_identifiers"], s["n_citation_rows"]))
        print("  absent %d of %d determinate = %.4f  [%.4f, %.4f]"
              % (i["NOT-RETRIEVABLE"], i["determinate"], i["absent_share"],
                 i["wilson95"][0], i["wilson95"][1]))
        print("  pages carrying at least one absent citation: %d"
              % s["pages_with_at_least_one_absent_citation"])
        t = out["article_space_only"]["identifier_level"]
        print("article space only: absent %d of %d determinate = %.4f"
              % (t["NOT-RETRIEVABLE"], t["determinate"], t["absent_share"]))
    else:
        print(text)


if __name__ == "__main__":
    main()
