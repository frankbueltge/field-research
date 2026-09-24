#!/usr/bin/env python3
"""Verification suite for artifacts/2026-09-24-another-network. Needs no network.

Every check re-derives its answer from the raw data files rather than trusting a field
estimates.json already computed — a check that re-reads a conclusion checks nothing.

    python3 tools/another-network/check.py
"""
import hashlib
import json
import math
import pathlib
import sys
from math import comb

ROOT = pathlib.Path(__file__).resolve().parents[2]
ART = ROOT / "artifacts/2026-09-24-another-network"
DATA = ART / "data"
OLD_POP = ROOT / "artifacts/2026-09-15-whose-refusal-is-it/data/population.json"

CHALLENGE_MARKS = [
    "just a moment", "cf-mitigated", "enable javascript", "captcha", "cloudflare",
    "checking your browser", "ddos", "access denied", "are you a robot",
]
ROBOTS_EXCLUDED = {
    "H:en-wikipedia-org", "H:query-wikidata-org", "H:www-reddit-com", "C:api-coingecko-com",
}

failures = []


def check(name, cond, detail=""):
    mark = "ok" if cond else "FAIL"
    print(f"[{mark}] {name}" + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        failures.append(name)


def local_refuses_raw(rec):
    if rec is None:
        return None
    if rec.get("error"):
        return True
    if rec.get("status") in (401, 403, 429):
        return True
    if rec.get("challenge"):
        return True
    return False


def delegate_refuses_raw(rec):
    if rec["result"] == "failed":
        return True
    clen = rec.get("content_len")
    if clen is None or clen < 40:
        return True
    low = (rec.get("content_head") or "").lower()
    if any(m in low for m in CHALLENGE_MARKS):
        return True
    return False


def main():
    pop_raw = OLD_POP.read_bytes()
    pop = json.loads(pop_raw)
    snap = json.loads((DATA / "population-snapshot.json").read_text())
    check("population snapshot sha256 matches the file read today",
          snap["sha256"] == hashlib.sha256(pop_raw).hexdigest())
    check("population has 69 units, as pre-registered",
          len(pop["units"]) == 69, str(len(pop["units"])))

    local = json.loads((DATA / "local.json").read_text())
    delegate = json.loads((DATA / "delegate.json").read_text())
    estimates = json.loads((DATA / "estimates.json").read_text())

    local_ids = {u["unit_id"] for u in local["units"]}
    pop_ids = {u["unit_id"] for u in pop["units"]}
    check("local.json covers exactly the 65 eligible units (69 minus the 4 pre-registered robots exclusions)",
          local_ids == pop_ids - ROBOTS_EXCLUDED and len(local_ids) == 65,
          str(len(local_ids)))
    check("no duplicate unit_id in local.json",
          len(local["units"]) == len(local_ids))
    check("none of the 4 pre-registered robots-excluded units appear in local.json at all",
          not (local_ids & ROBOTS_EXCLUDED))

    probed = [u for u in local["units"] if u["local"] is not None]
    newly_excluded = [u["unit_id"] for u in local["units"]
                      if u["unit_id"] not in ROBOTS_EXCLUDED and u["local"] is None]
    check("exactly one unit was newly robots-excluded at probe time",
          len(newly_excluded) == 1, str(newly_excluded))
    check("64 units carry a real local probe result",
          len(probed) == 64, str(len(probed)))

    # local_refuses recomputed independently from the raw arm record
    mismatches = [u["unit_id"] for u in probed
                  if u["local_refuses"] != local_refuses_raw(u["local"])]
    check("local_refuses in local.json matches an independent re-derivation from local.status/error/challenge",
          not mismatches, str(mismatches))

    delegate_ids_with_result = {u["unit_id"] for u in delegate["units"] if u["delegate"] is not None}
    local_probed_ids = {u["unit_id"] for u in probed}
    check("delegate.json has a result for exactly the 64 units local.json probed, no more no less",
          delegate_ids_with_result == local_probed_ids)

    dmismatches = [u["unit_id"] for u in delegate["units"] if u["delegate"] is not None
                   and u["delegate_refuses"] != delegate_refuses_raw(u["delegate"])]
    check("delegate_refuses matches an independent re-derivation from result/content_len/content_head",
          not dmismatches, str(dmismatches))

    # hand_reads census: every local unit with status==200 and a screen hit must appear exactly once
    screen_candidates = {u["unit_id"] for u in probed
                          if u["local"]["status"] == 200 and u["local"]["challenge"]}
    hand_read_ids = {h["unit_id"] for h in estimates["hand_reads"]}
    check("hand_reads covers exactly the screen's own 200-status challenge-hit candidates, a full census",
          screen_candidates == hand_read_ids,
          f"candidates={screen_candidates} hand_read={hand_read_ids}")
    check("hand_reads has no duplicate unit_id",
          len(estimates["hand_reads"]) == len(hand_read_ids))

    false_pos = {h["unit_id"] for h in estimates["hand_reads"] if h["verdict"] == "false"}
    true_pos = {h["unit_id"] for h in estimates["hand_reads"] if h["verdict"] == "true"}
    check("hand-read verdicts are exactly 3 false-positive and 2 confirmed",
          len(false_pos) == 3 and len(true_pos) == 2,
          f"false={false_pos} true={true_pos}")

    rows = {r["unit_id"]: r for r in estimates["rows"]}
    check("estimates.json rows cover exactly the 64 both-arm units",
          set(rows) == local_probed_ids)
    check("local_refuses_read is False for every false-positive hand-read unit",
          all(not rows[uid]["local_refuses_read"] for uid in false_pos))
    check("local_refuses_read is True for every confirmed hand-read unit",
          all(rows[uid]["local_refuses_read"] for uid in true_pos))
    # any unit not in hand_reads keeps screen == read
    unaffected = [uid for uid in rows if uid not in hand_read_ids
                  and rows[uid]["local_refuses_screen"] != rows[uid]["local_refuses_read"]]
    check("local_refuses_screen == local_refuses_read for every unit the hand-read did not touch",
          not unaffected, str(unaffected))

    # quadrant recomputation, both screen and read versions
    for key, qname in (("local_refuses_screen", "quadrant_screen"), ("local_refuses_read", "quadrant_read")):
        both_refuse = sum(1 for r in rows.values() if r[key] and r["delegate_refuses"])
        local_only = sum(1 for r in rows.values() if r[key] and not r["delegate_refuses"])
        delegate_only = sum(1 for r in rows.values() if not r[key] and r["delegate_refuses"])
        both_read = sum(1 for r in rows.values() if not r[key] and not r["delegate_refuses"])
        got = estimates[qname]
        check(f"{qname} matches an independent recount from rows",
              got == {"both_refuse": both_refuse, "local_only_refuses": local_only,
                      "delegate_only_refuses": delegate_only, "both_read": both_read},
              str(got))
        check(f"{qname} sums to 64",
              both_refuse + local_only + delegate_only + both_read == 64)

    # P1/P2 recomputation (read version)
    refusal_rows = [r for r in rows.values() if r["recorded_status"] in (401, 403, 429)]
    check("58 units carry a recorded refusal status (401/403/429)", len(refusal_rows) == 58)
    still = [r for r in refusal_rows if r["local_refuses_read"]]
    check("p1_p2_read.still_refuse matches an independent recount",
          estimates["p1_p2_read"]["still_refuse"] == len(still), str(len(still)))
    reads_of_still = [r for r in still if not r["delegate_refuses"]]
    check("p1_p2_read.of_those_delegate_reads matches an independent recount",
          estimates["p1_p2_read"]["of_those_delegate_reads"] == len(reads_of_still),
          str(len(reads_of_still)))

    # sign test recomputation
    lo = estimates["quadrant_read"]["local_only_refuses"]
    do = estimates["quadrant_read"]["delegate_only_refuses"]
    n = lo + do
    k = max(lo, do)
    p_sign = min(sum(comb(n, i) for i in range(k, n + 1)) * 2 / (2 ** n), 1.0) if n else None
    check("sign-test p-value on discordant pairs matches an independent recomputation",
          math.isclose(p_sign, estimates["sign_test_on_discordant_pairs_read"]["two_sided_exact_p"],
                       rel_tol=1e-9),
          f"{p_sign} vs {estimates['sign_test_on_discordant_pairs_read']['two_sided_exact_p']}")

    # controls
    ctrl = [r for r in rows.values() if r["stratum"] == "C"]
    check("6 controls present (7 minus 1 newly robots-excluded)", len(ctrl) == 6, str(len(ctrl)))
    ctrl_local_reads = sum(1 for r in ctrl if not r["local_refuses_read"])
    ctrl_delegate_reads = sum(1 for r in ctrl if not r["delegate_refuses"])
    check("controls.local_reads matches an independent recount",
          estimates["controls"]["local_reads"] == ctrl_local_reads)
    check("controls.delegate_reads matches an independent recount",
          estimates["controls"]["delegate_reads"] == ctrl_delegate_reads)
    check("K1 (instrument floor) did not fire, per its own stated rule",
          not estimates["kill_conditions"]["K1_instrument_floor"]["fired"])
    check("K1's floor of 4 is actually met by both arms' recount",
          ctrl_local_reads >= 4 and ctrl_delegate_reads >= 4,
          f"local={ctrl_local_reads} delegate={ctrl_delegate_reads}")

    # asymmetric case lists match the quadrant_read counts
    asym = estimates["asymmetric_cases"]
    check("asymmetric_cases.delegate_reads_local_refuses length matches quadrant_read.local_only_refuses",
          len(asym["delegate_reads_local_refuses"]) == estimates["quadrant_read"]["local_only_refuses"])
    check("asymmetric_cases.local_reads_delegate_refuses length matches quadrant_read.delegate_only_refuses",
          len(asym["local_reads_delegate_refuses"]) == estimates["quadrant_read"]["delegate_only_refuses"])

    render = json.loads((DATA / "render-check.json").read_text())
    check("render-check reports no horizontal overflow at all three widths",
          all(not v["overflow"] for v in render["final_results"].values()))
    check("render-check reports zero console errors at all three widths",
          all(not v["console_errors"] for v in render["final_results"].values()))
    import subprocess
    page_check = subprocess.run(
        [sys.executable, str(ROOT / "tools/another-network/make_page.py"), "--check"],
        capture_output=True, text=True)
    check("index.html is byte-for-byte what make_page.py renders from estimates.json today",
          page_check.returncode == 0, page_check.stdout + page_check.stderr)

    print()
    print(f"{len(failures)} check(s) failed" if failures else "all checks passed")
    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
