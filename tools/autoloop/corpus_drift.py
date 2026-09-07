#!/usr/bin/env python3
"""autoloop — the drift probe.

Open question 41: the nightly series records a different `corpus_sha256` every night and
identical measurements. This probe asks whether the corpus moves at all, and whether the
digest that says it moved is measuring the records or the clock.

It changes nothing. `fetch.py` and `loop.py` are called as committed, through the same
entry points the nightly job uses; this file only fetches, hashes and compares.

What it writes (--out): for each fetch, the record count, the digest over the whole file
(as `run_series.py` computes it), the digest over the records array alone, the id set and
the published-date range; then the pairwise comparisons, and — with --loop — the loop's 66
test outcomes on the fresh corpus, compared key by key against a committed run file.

Usage:
  python3 tools/autoloop/corpus_drift.py --out <drift.json> [--fetches 2] [--per-cat 300]
                                         [--loop --against tools/autoloop/series/runs/2026-09-06.json]
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))


def sha256_file(path):
    """Exactly what run_series.py stores as corpus_sha256: the whole file's bytes."""
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def sha256_records(corpus):
    """The digest the series does not compute: the records alone, id-sorted, no timestamp."""
    recs = sorted(corpus["records"], key=lambda r: r["id"])
    blob = json.dumps(recs, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest()


def describe(path):
    corpus = json.load(open(path))
    dates = sorted(r["published_date"] for r in corpus["records"] if r.get("published_date"))
    return {
        "fetched_utc": corpus["fetched_utc"],
        "records": len(corpus["records"]),
        "records_deduplicated": corpus.get("records_deduplicated"),
        "returned_per_category": corpus.get("returned_per_category"),
        "file_digest": sha256_file(path),
        "records_digest": sha256_records(corpus),
        "published_date_min": dates[0] if dates else None,
        "published_date_max": dates[-1] if dates else None,
        "ids": sorted(r["id"] for r in corpus["records"]),
    }


def compare(a, b):
    sa, sb = set(a["ids"]), set(b["ids"])
    return {
        "file_digest_equal": a["file_digest"] == b["file_digest"],
        "records_digest_equal": a["records_digest"] == b["records_digest"],
        "ids_equal": sa == sb,
        "in_a_not_b": len(sa - sb),
        "in_b_not_a": len(sb - sa),
        "jaccard": round(len(sa & sb) / len(sa | sb), 6) if (sa | sb) else None,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--fetches", type=int, default=2)
    ap.add_argument("--per-cat", type=int, default=300)
    ap.add_argument("--gap-seconds", type=float, default=20.0)
    ap.add_argument("--loop", action="store_true", help="run loop.py on the last fetch")
    ap.add_argument("--against", default=None, help="committed runs/<day>.json to compare against")
    ap.add_argument("--replicates", type=int, default=500)
    args = ap.parse_args()

    out = {
        "probe": "corpus_drift",
        "run_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "fetch_module": "tools/autoloop/fetch.py, unmodified",
        "per_cat": args.per_cat,
        "fetches": [],
        "comparisons": [],
        "breaks": [],
    }

    with tempfile.TemporaryDirectory() as tmp:
        paths = []
        for i in range(args.fetches):
            path = os.path.join(tmp, f"corpus-{i}.json")
            brk = os.path.join(tmp, f"breaks-{i}.json")
            if i:
                time.sleep(args.gap_seconds)
            p = subprocess.run([sys.executable, os.path.join(HERE, "fetch.py"),
                                "--out", path, "--breaks", brk, "--per-cat", str(args.per_cat)],
                               capture_output=True, text=True)
            if p.returncode != 0 or not os.path.exists(path):
                out["breaks"].append({"stage": "DATA", "fetch": i, "detail": p.stderr[-400:]})
                continue
            d = describe(path)
            d["fetch_index"] = i
            d["data_breaks"] = len(json.load(open(brk))) if os.path.exists(brk) else None
            paths.append(path)
            out["fetches"].append(d)

        for i in range(len(out["fetches"])):
            for j in range(i + 1, len(out["fetches"])):
                c = compare(out["fetches"][i], out["fetches"][j])
                c["pair"] = [i, j]
                out["comparisons"].append(c)

        if args.loop and paths:
            results = os.path.join(tmp, "results.json")
            p = subprocess.run([sys.executable, os.path.join(HERE, "loop.py"),
                                "--corpus", paths[-1], "--out", results,
                                "--replicates", str(args.replicates)],
                               capture_output=True, text=True)
            if p.returncode != 0 or not os.path.exists(results):
                out["breaks"].append({"stage": "EXPERIMENT", "detail": p.stderr[-400:]})
            else:
                res = json.load(open(results))
                fresh = {c["key"]: c for c in res["claims"]}
                out["fresh_run"] = {
                    "corpus_records": res["corpus"]["records"],
                    "hypotheses": res["hypotheses"],
                    "raw_findings": res["M1_raw_findings"],
                    "bh_survivors": res["M2_bh_survivors"],
                    "bonferroni_survivors": res["M2_bonferroni_survivors"],
                    "null_findings_per_run": res["M3_null_world"]["findings_per_run_mean"],
                    "null_per_test_rate": res["M3_null_world"]["per_test_rejection_rate"],
                    "replicating_split_half": res["M6_replicating"],
                }
                if args.against and os.path.exists(args.against):
                    old = {t["key"]: t for t in json.load(open(args.against))["tests"]}
                    same, diff, missing = [], [], []
                    for k, o in old.items():
                        f = fresh.get(k)
                        if f is None:
                            missing.append(k)
                            continue
                        if o["p"] == f["p"] and o["n1"] == f["n1"] and o["n0"] == f["n0"]:
                            same.append(k)
                        else:
                            diff.append({"key": k,
                                         "old": {"p": o["p"], "n1": o["n1"], "n0": o["n0"]},
                                         "new": {"p": f["p"], "n1": f["n1"], "n0": f["n0"]}})
                    out["vector_vs_committed"] = {
                        "against": os.path.relpath(args.against, os.path.dirname(HERE) + "/.."),
                        "n_committed": len(old),
                        "identical": len(same),
                        "differing": len(diff),
                        "missing_from_fresh": missing,
                        "differences": diff,
                    }

    # Every night's committed run file against every other: distinct test vectors, not nights.
    runs_dir = os.path.join(HERE, "series", "runs")
    vectors = {}
    if os.path.isdir(runs_dir):
        for name in sorted(os.listdir(runs_dir)):
            if not name.endswith(".json"):
                continue
            d = json.load(open(os.path.join(runs_dir, name)))
            blob = json.dumps([[t["key"], t["p"], t["n1"], t["n0"]] for t in
                               sorted(d["tests"], key=lambda t: t["key"])],
                              separators=(",", ":")).encode()
            vectors[name[:-5]] = {"vector_digest": hashlib.sha256(blob).hexdigest(),
                                  "file_digest_recorded": d.get("corpus_sha256"),
                                  "records": d.get("corpus_records")}
    distinct = sorted({v["vector_digest"] for v in vectors.values()})
    out["committed_nights"] = {
        "nights": vectors,
        "distinct_test_vectors": len(distinct),
        "distinct_recorded_digests": len({v["file_digest_recorded"] for v in vectors.values()}),
    }

    with open(args.out, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print(json.dumps({"fetches": len(out["fetches"]),
                      "comparisons": out["comparisons"],
                      "committed": out["committed_nights"]["distinct_test_vectors"],
                      "breaks": len(out["breaks"])}, indent=1))
    return 0 if out["fetches"] else 1


if __name__ == "__main__":
    sys.exit(main())
