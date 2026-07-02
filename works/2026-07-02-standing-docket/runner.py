"""
runner.py -- Instrument 009, "The Standing Docket"

Reads the committed World Bank raw snapshots, runs one trial (two synthetic
controls scored first, then the real series), appends the trial to
ledger.json (creating it if absent), recomputes the cumulative conviction
record, and writes data.json (the same object the Astro work renders).

Usage:
    python3 runner.py --date 2026-07-02

Deterministic: synthetic_benford uses random.Random(42), synthetic_human
uses random.Random(43). Both seeds are fixed in this file and disclosed in
the ledger's seed_disclosure field and in README.md.
"""

import argparse
import json
import os
import random
import sys

import digit_tests as dt

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(HERE, "data", "raw")
LEDGER_PATH = os.path.join(HERE, "ledger.json")
DATA_PATH = os.path.join(HERE, "data.json")

DETECTOR_VERSION = "digit-tests-v1"

SEED_SYNTHETIC_BENFORD = 42
SEED_SYNTHETIC_HUMAN = 43
SYNTHETIC_N = 200

CHI2_TEST_NAMES = ["first_digit_chi2", "second_digit_chi2", "last_digit_chi2"]
ALL_TEST_NAMES = ["first_digit_chi2", "first_digit_mad", "second_digit_chi2", "last_digit_chi2"]


# ---------------------------------------------------------------------
# Real data loading
# ---------------------------------------------------------------------

def load_real_country_ids():
    """Country ids (ISO3) for the 217 real countries: region.id != 'NA'."""
    with open(os.path.join(RAW_DIR, "wb-countries.json"), "r", encoding="utf-8") as f:
        meta, rows = json.load(f)
    ids = set()
    for row in rows:
        region = row.get("region") or {}
        if region.get("id") != "NA":
            ids.add(row["id"])
    return ids


def load_indicator_values(filename, real_ids):
    """Load an indicator snapshot, filtered to real countries with non-null values."""
    with open(os.path.join(RAW_DIR, filename), "r", encoding="utf-8") as f:
        meta, rows = json.load(f)
    values = []
    for row in rows:
        iso3 = row.get("countryiso3code")
        val = row.get("value")
        if iso3 in real_ids and val is not None:
            values.append(val)
    indicator_id = rows[0]["indicator"]["id"] if rows else None
    indicator_label = rows[0]["indicator"]["value"] if rows else None
    lastupdated = meta.get("lastupdated")
    return values, indicator_id, indicator_label, lastupdated


# ---------------------------------------------------------------------
# Synthetic controls
# ---------------------------------------------------------------------

def generate_synthetic_benford(seed=SEED_SYNTHETIC_BENFORD, n=SYNTHETIC_N):
    """
    Values distributed per Benford's Law by construction: v = 10**uniform(2,7).
    This is a multiplicative span covering five orders of magnitude (100 to
    10,000,000), which is exactly the condition under which Benford's Law
    holds. First digits follow Benford's Law by construction; last digits of
    the integer part are close to uniform because the fractional exponent is
    continuously distributed.
    """
    rng = random.Random(seed)
    return [10 ** rng.uniform(2, 7) for _ in range(n)]


def generate_synthetic_human(seed=SEED_SYNTHETIC_HUMAN, n=SYNTHETIC_N):
    """
    A modeled CARICATURE of human-fabricated numbers, not real fraud data.
    Two documented human tendencies are caricatured:
      - first digits over-weighted toward 5-9 (people fabricating numbers
        tend to avoid "suspiciously small" leading digits and prefer digits
        in the middle-to-upper range);
      - last digits under-represent 0 and 5, in the direction documented by
        Beber & Scacco (2012) doi:10.1093/pan/mps003 for real election-form
        fabrication (they found humans avoid certain "round" terminal
        digits when inventing numbers by hand).
    This is a synthetic caricature built to have a KNOWN, injected
    digit-bias -- it is not drawn from, or claimed to resemble in detail,
    any actual fraud dataset.
    """
    rng = random.Random(seed)
    first_digit_pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    first_digit_weights = [1, 1, 1, 1, 3, 3, 3, 3, 3]  # over-weights 5-9
    last_digit_pool = [1, 2, 3, 4, 6, 7, 8, 9]  # excludes 0 and 5

    values = []
    for _ in range(n):
        num_digits = rng.randint(3, 8)
        first = rng.choices(first_digit_pool, weights=first_digit_weights, k=1)[0]
        middle = [rng.randint(0, 9) for _ in range(max(0, num_digits - 2))]
        last = rng.choice(last_digit_pool) if num_digits >= 2 else first
        digit_str = "".join(str(d) for d in [first] + middle + ([last] if num_digits >= 2 else []))
        values.append(int(digit_str))
    return values


# ---------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------

def score_series(values):
    n, n_gate, tests, chi2_mad_disagree = dt.run_all_tests(values)
    return n, n_gate, tests, chi2_mad_disagree


def any_chi2_flagged(tests):
    return any(tests[name]["flagged"] for name in CHI2_TEST_NAMES)


def score_control(name, values, expect_clean):
    n, n_gate, tests, chi2_mad_disagree = score_series(values)
    convicted = any_chi2_flagged(tests)
    # expect_clean=True  -> synthetic_benford should NOT be convicted
    # expect_clean=False -> synthetic_human SHOULD be convicted
    behaved_as_expected = (not convicted) if expect_clean else convicted
    return {
        "name": name,
        "n": n,
        "n_gate": n_gate,
        "tests": tests,
        "chi2_mad_disagree": chi2_mad_disagree,
        "convicted": convicted,
        "behaved_as_expected": behaved_as_expected,
    }


def score_real_series(source, indicator_id, indicator_label, indicator_date, snapshot_date, values):
    n, n_gate, tests, chi2_mad_disagree = score_series(values)
    convicted = any_chi2_flagged(tests)
    return {
        "source": source,
        "indicator": indicator_id,
        "indicator_label": indicator_label,
        "indicator_date": indicator_date,
        "snapshot_date": snapshot_date,
        "n": n,
        "n_gate": n_gate,
        "tests": tests,
        "chi2_mad_disagree": chi2_mad_disagree,
        "convicted": convicted,
    }


# ---------------------------------------------------------------------
# Trial construction
# ---------------------------------------------------------------------

def build_trial(trial_id, date, snapshot_date):
    real_ids = load_real_country_ids()

    pop_values, pop_id, pop_label, pop_lastupdated = load_indicator_values("wb-pop-2023.json", real_ids)
    gdp_values, gdp_id, gdp_label, gdp_lastupdated = load_indicator_values("wb-gdp-2023.json", real_ids)

    synthetic_benford_values = generate_synthetic_benford()
    synthetic_human_values = generate_synthetic_human()

    controls = [
        score_control("synthetic_benford", synthetic_benford_values, expect_clean=True),
        score_control("synthetic_human", synthetic_human_values, expect_clean=False),
    ]

    series = [
        score_real_series(
            "World Bank", pop_id, pop_label, "2023", snapshot_date, pop_values
        ),
        score_real_series(
            "World Bank", gdp_id, gdp_label, "2023", snapshot_date, gdp_values
        ),
    ]

    clean_real_series_flagged = [s["indicator"] for s in series if s["convicted"]]
    tests_disagreeing = [s["indicator"] for s in series if s["chi2_mad_disagree"]]

    trial = {
        "trial_id": trial_id,
        "date": date,
        "seed_disclosure": {
            "synthetic_benford": SEED_SYNTHETIC_BENFORD,
            "synthetic_human": SEED_SYNTHETIC_HUMAN,
            "generator": "random.Random(seed) -- Python stdlib Mersenne Twister",
        },
        "detector_version": DETECTOR_VERSION,
        "controls": controls,
        "series": series,
        "verdict": {
            "clean_real_series_flagged": clean_real_series_flagged,
            "tests_disagreeing": tests_disagreeing,
        },
    }
    return trial


# ---------------------------------------------------------------------
# Cumulative block
# ---------------------------------------------------------------------

def compute_cumulative(trials):
    trial_count = len(trials)

    clean_real_series_tested = 0
    clean_real_series_convicted = 0
    per_test_conviction_counts_clean = {name: 0 for name in ALL_TEST_NAMES}

    synthetic_human_total = 0
    synthetic_human_detected = 0
    synthetic_benford_total = 0
    synthetic_benford_cleared = 0

    chi2_mad_conflicts = 0
    chi2_mad_observations = 0

    for trial in trials:
        for s in trial["series"]:
            clean_real_series_tested += 1
            if s["convicted"]:
                clean_real_series_convicted += 1
            for name in ALL_TEST_NAMES:
                if s["tests"][name]["flagged"]:
                    per_test_conviction_counts_clean[name] += 1
            chi2_mad_observations += 1
            if s["chi2_mad_disagree"]:
                chi2_mad_conflicts += 1

        for c in trial["controls"]:
            chi2_mad_observations += 1
            if c["chi2_mad_disagree"]:
                chi2_mad_conflicts += 1
            if c["name"] == "synthetic_human":
                synthetic_human_total += 1
                if c["convicted"]:
                    synthetic_human_detected += 1
            elif c["name"] == "synthetic_benford":
                synthetic_benford_total += 1
                if not c["convicted"]:
                    synthetic_benford_cleared += 1

    false_conviction_rate = (
        clean_real_series_convicted / clean_real_series_tested
        if clean_real_series_tested else None
    )
    detection_rate_on_synthetic_fraud = (
        synthetic_human_detected / synthetic_human_total
        if synthetic_human_total else None
    )
    clear_rate_on_synthetic_benford = (
        synthetic_benford_cleared / synthetic_benford_total
        if synthetic_benford_total else None
    )
    chi2_mad_conflict_rate = (
        chi2_mad_conflicts / chi2_mad_observations
        if chi2_mad_observations else None
    )

    alpha = dt.ALPHA
    expected_familywise_rate_by_chance = 1 - (1 - alpha) ** 4

    return {
        "trial_count": trial_count,
        "clean_real_series_tested": clean_real_series_tested,
        "clean_real_series_convicted": clean_real_series_convicted,
        "false_conviction_rate_on_clean_real_data": false_conviction_rate,
        "per_test_conviction_counts_on_clean_data": per_test_conviction_counts_clean,
        "detection_rate_on_synthetic_fraud": detection_rate_on_synthetic_fraud,
        "clear_rate_on_synthetic_benford": clear_rate_on_synthetic_benford,
        "chi2_mad_conflict_rate": chi2_mad_conflict_rate,
        "expected_false_conviction_rate_by_chance_alpha": {
            name: alpha for name in CHI2_TEST_NAMES
        },
        "expected_familywise_rate_by_chance": expected_familywise_rate_by_chance,
        "note": (
            "expected_false_conviction_rate_by_chance_alpha is the per-test "
            "significance threshold (alpha=0.05), i.e. the false-positive rate "
            "expected on truly clean data from that single test alone by chance. "
            "But each series here is put through 4 tests (3 chi2 tests + 1 MAD "
            "check), so the chance that AT LEAST ONE test flags a truly clean "
            "series is higher than 0.05: assuming independence, "
            "1-(1-0.05)^4 = %.6f (stored as expected_familywise_rate_by_chance). "
            "This is arithmetic, not an empirical claim -- it is the theoretical "
            "baseline the observed false_conviction_rate_on_clean_real_data "
            "should be compared against, not zero."
        ) % expected_familywise_rate_by_chance,
    }


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Run a Standing Docket trial and append to the ledger.")
    parser.add_argument("--date", required=True, help="Trial date, YYYY-MM-DD")
    parser.add_argument(
        "--snapshot-date",
        default=None,
        help="Snapshot date of the underlying raw data (defaults to --date)",
    )
    args = parser.parse_args()

    snapshot_date = args.snapshot_date or args.date

    if os.path.exists(LEDGER_PATH):
        with open(LEDGER_PATH, "r", encoding="utf-8") as f:
            ledger = json.load(f)
        trials = ledger.get("trials", [])
    else:
        trials = []

    next_trial_id = len(trials) + 1
    trial = build_trial(next_trial_id, args.date, snapshot_date)
    trials.append(trial)

    cumulative = compute_cumulative(trials)

    ledger = {
        "instrument": "009-standing-docket",
        "detector_version": DETECTOR_VERSION,
        "trials": trials,
        "cumulative": cumulative,
    }

    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2)
        f.write("\n")

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2)
        f.write("\n")

    print("Trial %d recorded for %s. Ledger now has %d trial(s)." % (
        next_trial_id, args.date, len(trials)
    ))
    print(json.dumps(cumulative, indent=2))


if __name__ == "__main__":
    main()
