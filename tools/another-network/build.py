#!/usr/bin/env python3
"""Combine local.json + delegate.json, apply the hand-read adjudication of the borderline
CHALLENGE_MARKS hits (read one by one, all of them — a census, not a sample, since there are
only 5), and write data/estimates.json and data/hand-reads.json.

    python3 tools/another-network/build.py
"""
import json
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
ART = ROOT / "artifacts/2026-09-24-another-network"
DATA = ART / "data"

# Every local unit whose status was 200 AND whose CHALLENGE_MARKS screen fired. Read by hand,
# all 5 (a census of the screen's own candidates on this population), reason quoted from the
# body excerpt in local.json.
HAND_READS = [
    {"unit_id": "H:datacenters-microsoft-com", "screen_mark": "cloudflare",
     "verdict": "false", "reason": "hit is a <script> tag loading a Cloudflare-hosted CDN "
     "library (cdnjs.cloudflare.com/.../gsap.min.js); the page is not behind Cloudflare, it "
     "merely imports a script from it."},
    {"unit_id": "H:wikimedia-org", "screen_mark": "captcha",
     "verdict": "false", "reason": "hit is the MediaWiki config key "
     "`wgConfirmEditCaptchaNeededForGenericEdit` inside embedded page JSON, naming a feature "
     "flag, not a captcha being shown to this request."},
    {"unit_id": "H:www-wikidata-org", "screen_mark": "captcha",
     "verdict": "false", "reason": "same MediaWiki config key as above, same verdict."},
    {"unit_id": "C:unbekannt-defining-the-observed-significance-level-of-a-test-a-simple-example-us",
     "screen_mark": "enable javascript", "verdict": "true",
     "reason": "link.springer.com serves a client-rendered shell whose only body text is "
     "'Please enable JavaScript to proceed.' — no article content reaches a non-JS client."},
    {"unit_id": "C:bijan-davvaz-groups", "screen_mark": "enable javascript", "verdict": "true",
     "reason": "same Springer JS-only shell as above, different DOI, same publisher."},
]
FALSE_POSITIVES = {h["unit_id"] for h in HAND_READS if h["verdict"] == "false"}


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None, None)
    p = k / n
    denom = 1 + z * z / n
    centre = p + z * z / (2 * n)
    spread = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (p, (centre - spread) / denom, (centre + spread) / denom)


def corrected_local_refuses(unit_id, raw_refuses):
    if unit_id in FALSE_POSITIVES:
        return False
    return raw_refuses


def main():
    local = json.loads((DATA / "local.json").read_text())
    delegate = json.loads((DATA / "delegate.json").read_text())
    lmap = {u["unit_id"]: u for u in local["units"]}
    dmap = {u["unit_id"]: u for u in delegate["units"]}

    both = [uid for uid in lmap if lmap[uid].get("local") is not None
            and dmap.get(uid, {}).get("delegate") is not None]
    both.sort()
    assert len(both) == 64, len(both)

    rows = []
    for uid in both:
        lu, du = lmap[uid], dmap[uid]
        raw_local_refuses = lu["local_refuses"]
        cor_local_refuses = corrected_local_refuses(uid, raw_local_refuses)
        rows.append({
            "unit_id": uid, "stratum": lu["stratum"], "url": lu["url"],
            "recorded_status": lu["recorded_status"],
            "local_status": lu["local"]["status"], "local_error": lu["local"]["error"],
            "local_refuses_screen": raw_local_refuses,
            "local_refuses_read": cor_local_refuses,
            "delegate_result": du["delegate"]["result"], "delegate_error": du["delegate"]["error"],
            "delegate_refuses": du["delegate_refuses"],
        })

    def quad(refuse_key):
        both_refuse = sum(1 for r in rows if r[refuse_key] and r["delegate_refuses"])
        local_only = sum(1 for r in rows if r[refuse_key] and not r["delegate_refuses"])
        delegate_only = sum(1 for r in rows if not r[refuse_key] and r["delegate_refuses"])
        both_read = sum(1 for r in rows if not r[refuse_key] and not r["delegate_refuses"])
        return {"both_refuse": both_refuse, "local_only_refuses": local_only,
                "delegate_only_refuses": delegate_only, "both_read": both_read}

    q_screen = quad("local_refuses_screen")
    q_read = quad("local_refuses_read")

    # P1 / P2 over the pre-registered refusal stratum (H+L1+L2, recorded 401/403/429)
    refusal_rows = [r for r in rows if r["recorded_status"] in (401, 403, 429)]
    n_refusal = len(refusal_rows)

    def p1p2(refuse_key):
        still = [r for r in refusal_rows if r[refuse_key]]
        p1 = wilson(len(still), n_refusal)
        reads_of_still = [r for r in still if not r["delegate_refuses"]]
        p2 = wilson(len(reads_of_still), len(still)) if still else (None, None, None)
        return {"n_refusal_units": n_refusal, "still_refuse": len(still),
                "p1_point_lo_hi": p1, "of_those_delegate_reads": len(reads_of_still),
                "p2_point_lo_hi": p2}

    p_screen = p1p2("local_refuses_screen")
    p_read = p1p2("local_refuses_read")

    # controls
    ctrl = [r for r in rows if r["stratum"] == "C"]
    ctrl_local_reads = sum(1 for r in ctrl if not r["local_refuses_read"])
    ctrl_delegate_reads = sum(1 for r in ctrl if not r["delegate_refuses"])

    # sign test on discordant pairs (read-corrected), exact binomial, two-sided
    disc_local_only = q_read["local_only_refuses"]
    disc_delegate_only = q_read["delegate_only_refuses"]
    n_disc = disc_local_only + disc_delegate_only
    from math import comb
    if n_disc:
        k = max(disc_local_only, disc_delegate_only)
        p_sign = sum(comb(n_disc, i) for i in range(k, n_disc + 1)) * 2 / (2 ** n_disc)
        p_sign = min(p_sign, 1.0)
    else:
        p_sign = None

    kill_conditions = {
        "K1_instrument_floor": {
            "rule": "fewer than 4 of the (here) 6 positive controls read under an arm",
            "local_reads": ctrl_local_reads, "delegate_reads": ctrl_delegate_reads,
            "n_controls": len(ctrl),
            "fired": ctrl_local_reads < 4 or ctrl_delegate_reads < 4,
        },
        "K2_local_arm_dead": {
            "rule": "local reads zero of 64 units",
            "local_reads_total": sum(1 for r in rows if not r["local_refuses_read"]),
            "fired": sum(1 for r in rows if not r["local_refuses_read"]) == 0,
        },
        "K3_delegate_tool_dead": {
            "rule": "delegate tool errors on the whole batch rather than per-URL",
            "fired": False,
            "note": "all five tavily_extract calls returned per-URL results/failed_results; "
            "none raised a transport/auth error.",
        },
    }

    out = {
        "_note": "Built by tools/another-network/build.py from local.json + delegate.json + "
        "the hand-read adjudication in this file. 'screen' = the mechanical, pre-registered "
        "CHALLENGE_MARKS rule applied without correction; 'read' = the same rule after the "
        "5-case hand adjudication of HAND_READS below, all 5 of the screen's own 200-status "
        "candidates on this population (a census, not a sample).",
        "n_units_both_arms": len(rows),
        "quadrant_screen": q_screen,
        "quadrant_read": q_read,
        "sign_test_on_discordant_pairs_read": {
            "local_only_refuses": disc_local_only, "delegate_only_refuses": disc_delegate_only,
            "n_discordant": n_disc, "two_sided_exact_p": p_sign,
        },
        "p1_p2_screen": p_screen,
        "p1_p2_read": p_read,
        "controls": {"n": len(ctrl), "local_reads": ctrl_local_reads,
                     "delegate_reads": ctrl_delegate_reads,
                     "both_fail": [r["unit_id"] for r in ctrl
                                   if r["local_refuses_read"] and r["delegate_refuses"]]},
        "kill_conditions": kill_conditions,
        "hand_reads": HAND_READS,
        "asymmetric_cases": {
            "delegate_reads_local_refuses": sorted(
                r["unit_id"] for r in rows if r["local_refuses_read"] and not r["delegate_refuses"]),
            "local_reads_delegate_refuses": sorted(
                r["unit_id"] for r in rows if not r["local_refuses_read"] and r["delegate_refuses"]),
        },
        "rows": rows,
    }
    (DATA / "estimates.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print("wrote", DATA / "estimates.json")
    print(json.dumps({"quadrant_read": q_read, "p1_p2_read": p_read,
                       "sign_test_p": p_sign, "kill_conditions": {
                           k: v["fired"] for k, v in kill_conditions.items()}}, indent=1))


if __name__ == "__main__":
    main()
