#!/usr/bin/env python3
"""discharge_121 — recompute every reviewer figure with this practice's own code first.

Session 121, 2026-08-15. The rule this arc has kept since session 115: a reviewer's number is
not printed in a disposition until this practice has recomputed it and can say whether it agrees.
Where it disagrees, both are published.

    python3 discharge_121.py [-o discharge-121.json]

Everything here is offline except `--time-vantage`, which issues exactly one request to the
geolocation service in order to measure what a reviewer said this session had misattributed.
"""
import argparse
import datetime as dt
import json
import subprocess
import sys
import time

OUT = {}


def utc(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)


def hhmm(delta):
    tot = int(delta.total_seconds())
    return f"{tot // 3600} h {tot % 3600 // 60} m {tot % 60} s"


# --- V7: the re-confirmation gap, and the claim that is temporally impossible ----------------
ft = json.load(open("functional-test-121.json"))
day5_run_close = utc("2026-08-15T05:31:27Z")          # DAY5-2026-08-15.md, run close
sidecar = json.load(open("ledger/transition-confirm-2026-08-15.json"))
last_pass = max(p["utc"] for r in sidecar["results"]
                if r["vid"] == "7234106298021727515" for p in r["passes"])
commit_utc = subprocess.run(["git", "log", "-s", "--format=%cI", "-1", "ffebcf56"],
                            capture_output=True, text=True).stdout.strip()

OUT["V7_reconfirmation_gap"] = {
    "claimed_in_INCREMENT-11_and_README": {"time": "20:29 UTC", "gap": "14 h 58 m"},
    "true_functional_run_started_utc": ft["started_utc"],
    "true_functional_run_finished_utc": ft["finished_utc"],
    "anchor_a_day5_run_close_utc": "2026-08-15T05:31:27Z",
    "anchor_b_day5_last_confirmation_pass_utc": last_pass,
    "gap_from_anchor_a_to_run_finish": hhmm(utc(ft["finished_utc"]) - day5_run_close),
    "gap_from_anchor_b_to_run_start": hhmm(utc(ft["started_utc"]) - utc(last_pass)),
    "commit_that_published_the_claim": {"sha": "ffebcf56", "committed_utc": commit_utc},
    "verdict": ("FALSE AND TEMPORALLY IMPOSSIBLE. No run happened at 20:29 UTC. The commit "
                "asserting it in the past tense was made at " + commit_utc + ", before the "
                "moment it describes. The figure 14 h 58 m was derived from the invented time "
                "and is not a rounding error. This practice found it independently at 20:47 UTC "
                "while the reviewers were running, and held it rather than edit a state under "
                "review; the Verifier found it too and its finding is the one published."),
}

# --- V8: the vantage-cost comparison ----------------------------------------------------------
i6_seconds = 0.7   # from the session's own I6 run: 1 item, --confirm 0, --vantage none
OUT["V8_vantage_cost"] = {
    "claimed_in_INCREMENT-11": "--vantage none made no third-party call (0.7 s against 10.7 s)",
    "run_A": {"seconds": i6_seconds, "n_items": 1, "confirm": 0, "vantage": "none",
              "purpose": "it was the I6 missing-baseline test, not a vantage test"},
    "run_B": {"seconds": ft["seconds"], "n_items": ft["list"]["n_items"],
              "confirm": ft["confirmation"]["passes"], "vantage": ft["vantage"]["mode"]},
    "confound": ("three variables differ at once: item count, confirmation passes, vantage mode. "
                 "run_B's own sleeps alone are (3-1) + 5 = 7 s at ledger.DELAY = 1.0 s."),
    "verdict": ("MISLEADING AS STATED. The two runs are not a controlled comparison and almost "
                "none of the 10 s difference is the vantage call. The reviewer is right."),
}

# --- Interlocutor charge 1: the probability a confirmation burst hits transport noise ----------
def burst_noise(p, n=5):
    return 1.0 - (1.0 - p) ** n


OUT["I1_noise_in_the_confirmation_burst"] = {
    "arc_own_transport_failure_rates": {
        "session_109_census": 0.0033, "session_110_run": 0.0124,
        "preregistered_ceiling_P2": 0.020,
        "source": "PREREGISTRATION-112.md §P2 and lines 119, 144"},
    "p_at_least_one_noisy_pass_in_5": {
        "at_0.33_pct": round(burst_noise(0.0033), 6),
        "at_1.24_pct": round(burst_noise(0.0124), 6),
        "at_2.0_pct": round(burst_noise(0.020), 6)},
    "reviewer_figure": "roughly 1-(1-0.012)^5 = 5.8 %",
    "our_recomputation_at_1.24_pct_the_arc_own_measured_rate": round(burst_noise(0.0124) * 100, 2),
    "verdict": ("AGREED, and at this arc's own measured 1.24 % the figure is 6.05 %, slightly "
                "above the reviewer's 5.8 % (which used 1.2 %). The defect is real: v0.2 treated "
                "an INDETERMINATE confirmation pass as disagreement, so a genuinely absent unit "
                "was discarded from BOTH numerator and denominator on one transport blip."),
}

# --- V9: the condition accounting -------------------------------------------------------------
OUT["V9_condition_accounting"] = {
    "total_dispositioned_at_session_120": 32,
    "discharged_at_session_120": ["I16"],
    "carried": 31,
    "touched_by_v0.2": {"I3": "confirmation", "I4": "strict parsing (partially — see I6 below)",
                        "I6": "loud baseline failure + exit 3", "I7": "vantage modes",
                        "V14": "the README addendum rewords 'unmodified since it was written'"},
    "n_touched": 5,
    "untouched": 31 - 5,
    "verdict": ("The published '26' is arithmetically right and was not shown. 31 carried minus "
                "5 touched = 26. V14 is the fifth and the increment never said so."),
}

# --- Interlocutor charge 2: the README sentence -------------------------------------------------
# CORRECTED WHILE THIS SCRIPT WAS BEING RUN, and recorded rather than quietly fixed. The first
# version of this check searched line by line for "same instrument" and returned NOTHING, while
# the verdict below already said "CONFIRMED" — a verdict written before its own check ran, which
# is the exact failure sessions 87, 88 and 90 were caught on. The phrase is split across a line
# break in the source ("the same" / "instrument,"), so the check must read the whole text with
# whitespace collapsed. It does now, and the sentence is there.
import re  # noqa: E402

readme_raw = open("deliverable/README.md", encoding="utf-8").read()
readme_flat = re.sub(r"\s+", " ", readme_raw)
sentence = "It is the same instrument, so your reading and ours are comparable."
lines = readme_raw.splitlines()
line_hits = [i + 1 for i, l in enumerate(lines) if "instrument, so your reading" in l]
OUT["I2_readme_same_instrument"] = {
    "searched": "whole file, whitespace collapsed (a line-by-line search misses it — see note)",
    "sentence_present": sentence in readme_flat,
    "line_carrying_the_second_half": line_hits,
    "tool_docstring_says": ("The two instruments are not the same and a figure from one is not a "
                            "row of the other."),
    "verdict": ("CONFIRMED. The sentence the previous adversary quoted as the falsehood at the "
                "centre of its objection is still live in the bundle, in the same commit that "
                "wrote its correction into the tool one file over."),
}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default="discharge-121.json")
    ap.add_argument("--time-vantage", action="store_true",
                    help="issue ONE request to the geolocation service and time it")
    a = ap.parse_args(argv)
    if a.time_vantage:
        sys.path.insert(0, "deliverable/tools")
        import ledger
        t = time.time()
        ledger.vantage()
        OUT["V8_vantage_cost"]["measured_isolated_cost_seconds"] = round(time.time() - t, 3)
        OUT["V8_vantage_cost"]["measured_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                                               time.gmtime())
    json.dump(OUT, open(a.out, "w"), indent=1)
    print(json.dumps(OUT, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
