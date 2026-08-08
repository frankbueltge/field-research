"""Scores PREREGISTRATION.md's P1-P4 against observations.json. Writes scored.json."""
import json, collections

B = "/home/user/field-research/drafts/2026-08-08-does-the-date-move"
d = json.load(open(f"{B}/observations.json"))

per_auth = collections.defaultdict(lambda: collections.Counter())
ratios, phantom, silent = [], [], []
cdx_pairs = cdx_diff = 0
coverage = []

for rec in d["urls"]:
    a = rec["authority"]
    cdx_pairs += rec.get("cdx_adjacent_pairs", 0)
    cdx_diff += rec.get("cdx_adjacent_digest_differs", 0)
    obs_ok = sum(1 for o in rec["observations"].values() if "text_sha256" in o)
    coverage.append({"authority": a, "url": rec["url"], "observations": obs_ok,
                     "captures_in_window": rec.get("captures_200_in_window"),
                     "errors": len(rec.get("errors", []))})
    for p in rec.get("pairs", []):
        c = per_auth[a]
        if p["status"] != "SCORED":
            c["dropped"] += 1
            continue
        c["scored"] += 1
        c[p["content"]] += 1
        ratios.append(p["ratio"])
        # V arm
        if p["v"] == "UNSCORABLE":
            c["v_unscorable"] += 1
        else:
            c[f"v_{p['content']}_{p['v']}"] += 1
            if p["content"] == "SUBSTANTIVE" and p["v"] == "STILL":
                silent.append({"authority": a, "url": rec["url"], "from": p["from"], "to": p["to"],
                               "ratio": p["ratio"], "v": p["v_from"]})
            if p["content"] == "IDENTICAL" and p["v"] == "MOVED":
                phantom.append({"authority": a, "url": rec["url"], "from": p["from"], "to": p["to"],
                                "v_from": p["v_from"], "v_to": p["v_to"]})
        # H arm
        if p["h"] == "UNSCORABLE":
            c["h_unscorable"] += 1
        else:
            c[f"h_{p['h']}"] += 1
            c[f"h_{p['content']}_{p['h']}"] += 1

# --- P1: among SUBSTANTIVE pairs scorable for V, does V fail to move in >half, on any authority?
p1 = {}
for a, c in per_auth.items():
    still, moved = c["v_SUBSTANTIVE_STILL"], c["v_SUBSTANTIVE_MOVED"]
    n = still + moved
    p1[a] = {"substantive_scorable_for_v": n, "v_still": still, "v_moved": moved,
             "share_still": (round(still / n, 4) if n else None)}
p1_hit = [a for a, r in p1.items() if r["substantive_scorable_for_v"] > 0 and r["share_still"] > 0.5]

# --- P2: EC pairs scorable for H -> share MOVED
ec = per_auth.get("EC", collections.Counter())
h_n = ec["h_MOVED"] + ec["h_STILL"]
p2 = {"ec_pairs_scorable_for_h": h_n, "h_moved": ec["h_MOVED"],
      "share_moved": (round(ec["h_MOVED"] / h_n, 4) if h_n else None),
      "h_moved_where_text_identical": ec["h_IDENTICAL_MOVED"],
      "text_identical_scorable_for_h": ec["h_IDENTICAL_MOVED"] + ec["h_IDENTICAL_STILL"]}

# --- P3: any IDENTICAL pair where V moved
p3 = {"count": len(phantom), "cases": phantom[:12]}

# --- P4: adjacent CDX digest difference rate over the population
p4 = {"adjacent_pairs": cdx_pairs, "digest_differs": cdx_diff,
      "share": (round(cdx_diff / cdx_pairs, 4) if cdx_pairs else None)}

out = {"instrument": d["instrument"], "run_started_utc": d.get("run_started_utc"),
       "run_finished_utc": d.get("run_finished_utc"),
       "coverage": coverage,
       "per_authority": {a: dict(c) for a, c in per_auth.items()},
       "ratio_distribution": {
           "n": len(ratios),
           "exactly_1.0": sum(1 for r in ratios if r == 1.0),
           "ge_0.98_lt_1.0": sum(1 for r in ratios if 0.98 <= r < 1.0),
           "lt_0.98": sum(1 for r in ratios if r < 0.98),
           "deciles": [round(sorted(ratios)[int(len(ratios) * q / 10)], 4) for q in range(10)] if ratios else []},
       "P1": {"statement": "V fails to move in >50% of SUBSTANTIVE V-scorable pairs on >=1 authority",
              "per_authority": p1, "authorities_meeting_it": p1_hit,
              "verdict": "HELD" if p1_hit else "NOT HELD"},
       "P2": {"statement": "EC: H moves in >=90% of H-scorable pairs", **p2,
              "verdict": (None if not p2["share_moved"] else ("HELD" if p2["share_moved"] >= 0.9 else "NOT HELD"))},
       "P3": {"statement": "at least one IDENTICAL pair where V moved", **p3,
              "verdict": "HELD" if phantom else "NOT HELD"},
       "P4": {"statement": "adjacent CDX digests differ in >=90% of pairs (confirmatory)", **p4,
              "verdict": (None if not p4["share"] else ("HELD" if p4["share"] >= 0.9 else "NOT HELD"))},
       "silent_change_cases": silent[:20], "silent_change_total": len(silent)}

json.dump(out, open(f"{B}/scored.json", "w"), indent=1)
print(json.dumps({k: out[k] for k in ("P1", "P2", "P3", "P4")}, indent=1)[:2600])
print("\nratio dist:", out["ratio_distribution"])
print("silent total:", out["silent_change_total"])
