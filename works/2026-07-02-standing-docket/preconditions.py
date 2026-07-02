"""
preconditions.py -- Instrument 009, "The Standing Docket"

Codified defendant-selection gate. Runs the machine-checkable selection
preconditions (see README.md, "Defendant selection") against a raw World
Bank snapshot under data/raw/, on the same real-country universe the
runner scores (region.id != "NA", non-null values):

  2. N in [100, 10000]
  3. positive-value span >= 3 orders of magnitude
  4. reporting precision reaches the unit digit: REJECT if the majority
     (> 0.5) of non-null values are nonzero integers exactly divisible
     by 1000 (a storage/reporting-unit artifact would then drive the
     last-digit test)

Precondition 1 (official statistic of known provenance, raw snapshot
committed with source URL) is documentary, not machine-checkable -- it
lives in data/raw/PROVENANCE.md.

This script never runs a digit test: selection cannot see verdicts.

Usage:
    python3 preconditions.py wb-expgnfs-2023.json
"""

import argparse
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(HERE, "data", "raw")

N_LOW = 100
N_HIGH = 10000
SPAN_MIN_ORDERS = 3.0
ROUNDING_REJECT_SHARE = 0.5


def load_real_country_ids():
    """Same universe as runner.py: real countries only (region.id != 'NA')."""
    with open(os.path.join(RAW_DIR, "wb-countries.json"), "r", encoding="utf-8") as f:
        meta, rows = json.load(f)
    ids = set()
    for row in rows:
        region = row.get("region") or {}
        if region.get("id") != "NA":
            ids.add(row["id"])
    return ids


def main():
    parser = argparse.ArgumentParser(description="Run the codified selection preconditions on a raw snapshot.")
    parser.add_argument("filename", help="raw snapshot filename under data/raw/")
    args = parser.parse_args()

    real_ids = load_real_country_ids()
    with open(os.path.join(RAW_DIR, args.filename), "r", encoding="utf-8") as f:
        meta, rows = json.load(f)

    indicator = rows[0]["indicator"]["id"] if rows else "?"
    values = [
        row["value"] for row in rows
        if row.get("countryiso3code") in real_ids and row.get("value") is not None
    ]

    n = len(values)
    zeros = sum(1 for v in values if v == 0)
    negatives = sum(1 for v in values if v < 0)
    positives = [v for v in values if v > 0]
    span = (math.log10(max(positives)) - math.log10(min(positives))) if positives else 0.0
    rounded_1000 = sum(
        1 for v in values if v == int(v) and int(v) != 0 and int(v) % 1000 == 0
    )
    rounded_share = rounded_1000 / n if n else 0.0

    n_ok = N_LOW <= n <= N_HIGH
    span_ok = span >= SPAN_MIN_ORDERS
    rounding_ok = rounded_share <= ROUNDING_REJECT_SHARE
    verdict = "ACCEPT" if (n_ok and span_ok and rounding_ok) else "REJECT"

    print("indicator: %s  (file: %s)" % (indicator, args.filename))
    print("real-country universe: N=%d  (zeros: %d, negatives: %d)" % (n, zeros, negatives))
    print("precondition 2 -- N in [%d, %d]: %s" % (N_LOW, N_HIGH, "pass" if n_ok else "FAIL"))
    print("precondition 3 -- span %.2f orders (min %.1f): %s" % (span, SPAN_MIN_ORDERS, "pass" if span_ok else "FAIL"))
    print("precondition 4 -- nonzero multiples of 1000: %d/%d = %.1f%% (reject if > %.0f%%): %s" % (
        rounded_1000, n, 100.0 * rounded_share, 100.0 * ROUNDING_REJECT_SHARE,
        "pass" if rounding_ok else "FAIL"))
    print("verdict: %s" % verdict)
    print("(precondition 1, documented provenance, is checked in PROVENANCE.md, not here;")
    print(" no digit test is run by this script)")


if __name__ == "__main__":
    main()
