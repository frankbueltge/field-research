#!/usr/bin/env python3
"""autoloop — the unattended arm.

One command that runs the whole loop against a corpus fetched the same minute, and
appends a single line to a series. Nothing here needs a person: it is the same
DATA -> QUESTION -> EXPERIMENT -> ANALYSIS -> WRITE -> REVIEW pipeline the session of
2026-09-03 ran by hand, wired to a schedule.

What is committed each night: one line in `series.jsonl`, and one compact per-run file
under `runs/` holding the 66 test outcomes without the corpus. The corpus itself is NOT
committed — it is 2,000 records of third-party metadata a day and the series does not
need it kept; each row carries the corpus's SHA-256 and its counts instead.

What the series is for: the loop's yield is a measurement, and a measurement taken once
is not a series. Whether 14 findings a night is stable, whether the null-world rate
stays at 5 %, and whether the loop breaks on a day arXiv answers differently — none of
that is knowable from one run.

Usage: python3 tools/autoloop/run_series.py [--dir tools/autoloop/series] [--per-cat 300]
Exit status is non-zero when the run failed to produce a row, so a scheduled job that
goes green means the measurement landed.
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


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        sys.stderr.write(p.stderr[-2000:])
    return p.returncode == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=os.path.join(HERE, "series"))
    ap.add_argument("--per-cat", type=int, default=300)
    ap.add_argument("--replicates", type=int, default=500)
    args = ap.parse_args()

    os.makedirs(os.path.join(args.dir, "runs"), exist_ok=True)
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    t0 = time.time()

    with tempfile.TemporaryDirectory() as tmp:
        corpus = os.path.join(tmp, "corpus.json")
        results = os.path.join(tmp, "results.json")
        review = os.path.join(tmp, "review.json")
        breaks = os.path.join(tmp, "breaks-data.json")

        ok_fetch = run([sys.executable, os.path.join(HERE, "fetch.py"), "--out", corpus,
                        "--breaks", breaks, "--per-cat", str(args.per_cat)])
        if not ok_fetch or not os.path.exists(corpus):
            print("DATA stage produced no corpus; no row written", file=sys.stderr)
            return 1
        raw = open(corpus, "rb").read()
        ok_loop = run([sys.executable, os.path.join(HERE, "loop.py"), "--corpus", corpus,
                       "--out", results, "--replicates", str(args.replicates)])
        if not ok_loop:
            print("EXPERIMENT stage failed; no row written", file=sys.stderr)
            return 1
        run([sys.executable, os.path.join(HERE, "review.py"), "--corpus", corpus,
             "--results", results, "--out", review])

        res = json.load(open(results))
        rev = json.load(open(review)) if os.path.exists(review) else {}
        data_breaks = json.load(open(breaks)) if os.path.exists(breaks) else []

        compact = [{"key": c["key"], "p": c["p"], "effect": c["effect"], "n1": c["n1"],
                    "n0": c["n0"], "significant": c["significant"], "bh": c["bh_survivor"],
                    "failures": c["failures"]} for c in res["claims"]]
        json.dump({"day": day, "corpus_sha256": hashlib.sha256(raw).hexdigest(),
                   "corpus_records": res["corpus"]["records"], "tests": compact},
                  open(os.path.join(args.dir, "runs", f"{day}.json"), "w"), indent=1, sort_keys=True)

        row = {
            "day": day,
            "fetched_utc": res["corpus"]["fetched_utc"],
            "corpus_records": res["corpus"]["records"],
            "corpus_sha256": hashlib.sha256(raw).hexdigest(),
            "hypotheses": res["hypotheses"],
            "raw_findings": res["M1_raw_findings"],
            "bh_survivors": res["M2_bh_survivors"],
            "bonferroni_survivors": res["M2_bonferroni_survivors"],
            "review_kills": res["M4_review_kills"],
            "replicating_split_half": res["M6_replicating"],
            "null_findings_per_run": res["M3_null_world"]["findings_per_run_mean"],
            "null_per_test_rate": res["M3_null_world"]["per_test_rejection_rate"],
            "distinct_pairs_among_bh": rev.get("redundancy", {}).get("distinct_pairs_among_bh_survivors"),
            "review_disagreements": len(rev.get("disagreements", [])),
            "breaks": len(res["breaks"]) + len(data_breaks),
            "seconds": round(time.time() - t0, 1),
        }

    path = os.path.join(args.dir, "series.jsonl")
    with open(path, "a") as f:
        f.write(json.dumps(row, sort_keys=True) + "\n")
    print(json.dumps(row, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
