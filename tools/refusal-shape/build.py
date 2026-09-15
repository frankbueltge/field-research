#!/usr/bin/env python3
"""Apply the pre-registered coding table to the probes and compute every figure the page states.

    python3 tools/refusal-shape/build.py

Inputs:  data/population.json, data/probes.json  (both committed)
Outputs: data/data.json  — every number the artifact states, and nothing it does not
         data/census.csv — one row per unit, human-readable

No figure is computed anywhere but here. The page renders this file; check.py re-derives it.
"""
import csv
import json
import pathlib
import sys
import urllib.parse
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from coding import arm_pattern, code_unit, robots_disallows  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
ART = ROOT / "artifacts/2026-09-15-whose-refusal-is-it"
DATA = ART / "data"
ARMS = ("bare", "urllib", "named")


def clopper_pearson(k, n, alpha=0.05):
    """Exact binomial interval, TWO-SIDED at 95 %, computed by bisection on the binomial CDF
    so this file depends on nothing but the standard library.

    Convention note, so an apparent contradiction of our own record is not read as one: the
    bounds this practice published on 2026-09-14 (0 in 32 permits 8.9 %) are ONE-SIDED 95 %
    upper bounds. The same 0/32 here reads 10.89 %, two-sided. Both are correct; they are not
    the same quantity, and nothing on this page may be compared with those figures directly.
    Verified against a textbook value: 5/10 gives (0.1871, 0.8129)."""
    if n == 0:
        return (0.0, 1.0)

    def binom_cdf(p, k, n):
        # P(X <= k) for X ~ Bin(n, p)
        total, term = 0.0, (1 - p) ** n
        for i in range(0, k + 1):
            if i:
                term *= (n - i + 1) / i * (p / (1 - p)) if p < 1 else 0
            total += term
        return min(1.0, total)

    def solve(target, lo, hi, fn):
        for _ in range(200):
            mid = (lo + hi) / 2
            if fn(mid) > target:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2

    low = 0.0 if k == 0 else solve(1 - alpha / 2, 0.0, 1.0, lambda p: binom_cdf(p, k - 1, n))
    high = 1.0 if k == n else solve(alpha / 2, 0.0, 1.0, lambda p: binom_cdf(p, k, n))
    return (round(low, 4), round(high, 4))


def pct(k, n):
    return round(100.0 * k / n, 2) if n else None


def main():
    probes = json.loads((DATA / "probes.json").read_text())
    pop = json.loads((DATA / "population.json").read_text())
    rows = []

    for u in probes["units"]:
        arms = {a: u["arms"].get(a) for a in ARMS}
        code, label_wrong, reason = code_unit(u, arms)
        pattern = arm_pattern(arms) if u["arms"] else "not-probed"
        # the published ground at the host the identifier actually resolved to (§2.2)
        rh = u.get("resolved_host")
        rb = probes["robots_resolved_hosts"].get(rh) if rh else None
        final = next((arms[a].get("final_url") for a in ARMS if arms[a] and arms[a].get("final_url")), None)
        fp = urllib.parse.urlsplit(final).path if final else ""
        if rb is None:
            # No redirect off the request host (or none recorded): the ground is that host's
            # own robots.txt, which was fetched before probing. Without this fallback every
            # unit that stayed put reads as "no ground known", which would be false.
            rb = probes["robots_request_hosts"].get(u.get("request_host"))
            if rb is not None and not fp:
                fp = urllib.parse.urlsplit(u["url"]).path
        resolved_ground = None
        if rb is not None:
            if not rb.get("served"):
                resolved_ground = "no-robots-served"
            else:
                resolved_ground = "disallowed" if robots_disallows(rb.get("text", ""), fp or "/") else "allowed"
        rows.append({
            "unit_id": u["unit_id"], "stratum": u["stratum"], "url": u["url"],
            "label": u.get("label", ""), "recorded_status": u.get("recorded_status"),
            "recorded_note": u.get("recorded_note"),
            "request_host": u.get("request_host"), "resolved_host": rh,
            "robots_blocked": u.get("robots_blocked"),
            "status_bare": (arms["bare"] or {}).get("status"),
            "status_urllib": (arms["urllib"] or {}).get("status"),
            "status_named": (arms["named"] or {}).get("status"),
            "challenge_seen": any((arms[a] or {}).get("challenge") for a in ARMS),
            "www_authenticate": any((arms[a] or {}).get("www_authenticate") for a in ARMS),
            "code": code, "register_label_wrong": label_wrong, "arm_pattern": pattern,
            "machine_reason": reason, "resolved_host_robots": resolved_ground,
        })

    def share(subset, codes):
        n = len(subset)
        k = sum(1 for r in subset if r["code"] in codes)
        return {"k": k, "n": n, "pct": pct(k, n), "ci95": clopper_pearson(k, n)}

    H = [r for r in rows if r["stratum"] == "H"]
    L = [r for r in rows if r["stratum"] in ("L1", "L2")]
    L1 = [r for r in rows if r["stratum"] == "L1"]
    L2 = [r for r in rows if r["stratum"] == "L2"]
    C = [r for r in rows if r["stratum"] == "C"]
    OURS = ("open", "client-string")

    disagree = [r for r in rows if r["arm_pattern"] not in ("all-agree", "not-probed")]
    named_apart = [r for r in disagree if r["arm_pattern"] == "named-apart"]
    urllib_apart = [r for r in disagree if r["arm_pattern"] == "urllib-apart"]

    HL = H + L
    policy_published = [r for r in HL if r["code"] == "policy-published"]

    # Doors that refuse while their own published policy permits the path.
    refusing = [r for r in HL if r["code"] == "refuses-all"]
    unjustified = [r for r in refusing if r["resolved_host_robots"] == "allowed"]
    no_policy_served = [r for r in refusing if r["resolved_host_robots"] == "no-robots-served"]

    # Hosts that refuse a request for their own rulebook.
    rob_hosts = dict(probes["robots_resolved_hosts"])
    for h, v in probes["robots_request_hosts"].items():
        rob_hosts.setdefault(h, v)
    robots_refused = sorted(h for h, v in rob_hosts.items()
                            if v.get("status") in (401, 403, 429))

    predictions = [
        {"id": "P1",
         "claim": "In stratum H the share coded open+client-string is at least 5 of 13",
         "observed": share(H, OURS),
         "verdict": "confirmed" if share(H, OURS)["k"] >= 5 else "REFUTED"},
        {"id": "P2",
         "claim": "In stratum L that share is lower than in H",
         "observed": {"H": share(H, OURS), "L": share(L, OURS)},
         "verdict": "confirmed" if share(L, OURS)["pct"] < share(H, OURS)["pct"] else "REFUTED"},
        {"id": "P3",
         "claim": "Among units whose arms disagree, more than half are bare=urllib with named apart",
         "observed": {"disagreeing": len(disagree), "named_apart": len(named_apart),
                      "urllib_apart": len(urllib_apart),
                      "other_patterns": len(disagree) - len(named_apart) - len(urllib_apart)},
         "verdict": "confirmed" if len(named_apart) > len(disagree) / 2 else "REFUTED"},
        {"id": "P4",
         "claim": "Fewer than half of H+L units carry a published robots ground (policy-published < 50%)",
         "observed": {"k": len(policy_published), "n": len(HL), "pct": pct(len(policy_published), len(HL))},
         "verdict": "confirmed" if len(policy_published) < len(HL) / 2 else "REFUTED"},
        {"id": "P5",
         "claim": "register_label_wrong is true for at least one H unit",
         "observed": {"k": sum(1 for r in H if r["register_label_wrong"]), "n": len(H),
                      "units": [r["unit_id"] for r in H if r["register_label_wrong"]]},
         "verdict": "confirmed" if any(r["register_label_wrong"] for r in H) else "REFUTED"},
        {"id": "P6",
         "claim": "KILL CONDITION — all 8 control units are coded open",
         "observed": {"codes": dict(Counter(r["code"] for r in C)),
                      "not_open": [{"unit": r["unit_id"], "code": r["code"],
                                    "statuses": [r["status_bare"], r["status_urllib"], r["status_named"]]}
                                   for r in C if r["code"] != "open"]},
         "verdict": "confirmed" if all(r["code"] == "open" for r in C) else "REFUTED"},
    ]

    data = {
        "_note": "Every figure the artifact states. Computed only here, from data/probes.json "
        "under the coding table of PREREGISTRATION.md §2.3. check.py re-derives all of it.",
        "session": 161, "date": "2026-09-15", "practice": "The Field (Meridian)",
        "interval_convention": "Clopper-Pearson, two-sided 95 %. Not comparable with the "
        "one-sided bounds this practice published on 2026-09-14.",
        "probed_utc": probes["probed_utc"],
        "population": {
            "units": len(rows), "seed": pop["seed"],
            "feeds": pop["feeds"], "stratum_sizes": pop["stratum_sizes"],
            "excluded_by_rule": pop["excluded_by_rule"],
        },
        "codes": {
            "all": dict(Counter(r["code"] for r in rows)),
            "H": dict(Counter(r["code"] for r in H)),
            "L1": dict(Counter(r["code"] for r in L1)),
            "L2": dict(Counter(r["code"] for r in L2)),
            "C": dict(Counter(r["code"] for r in C)),
        },
        "headline": {
            "refusal_was_ours_H": share(H, OURS),
            "refusal_was_ours_L": share(L, OURS),
            "refusal_was_ours_L1": share(L1, OURS),
            "refusal_was_ours_L2": share(L2, OURS),
            "refusal_was_theirs_H": share(H, ("refuses-all", "key-declared")),
            "refusal_was_theirs_L": share(L, ("refuses-all", "key-declared")),
            "register_label_wrong_H": {"k": sum(1 for r in H if r["register_label_wrong"]),
                                       "n": len(H)},
        },
        "arm_patterns": {
            "counts": dict(Counter(r["arm_pattern"] for r in rows)),
            "disagreeing_units": len(disagree),
            "named_apart": [r["unit_id"] for r in named_apart],
            "urllib_apart": [r["unit_id"] for r in urllib_apart],
            "per_arm_2xx": {a: sum(1 for r in rows if r[f"status_{a}"] is not None
                                   and 200 <= r[f"status_{a}"] < 300) for a in ARMS},
            "per_arm_refusal": {a: sum(1 for r in rows if r[f"status_{a}"] in (401, 403, 429))
                                for a in ARMS},
            "probed_units": sum(1 for r in rows if r["arm_pattern"] != "not-probed"),
        },
        "published_ground": {
            "policy_published_units": len(policy_published),
            "policy_published_ids": [r["unit_id"] for r in policy_published],
            "refusing_units": len(refusing),
            "refusing_whose_robots_permits_the_path": len(unjustified),
            "refusing_whose_host_serves_no_robots": len(no_policy_served),
            "hosts_refusing_their_own_robots_txt": robots_refused,
            "hosts_refusing_their_own_robots_txt_n": len(robots_refused),
            "distinct_hosts_probed": len({r["resolved_host"] or r["request_host"] for r in rows}),
        },
        "predictions": predictions,
        "rows": rows,
    }

    (DATA / "data.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    cols = ["unit_id", "stratum", "code", "register_label_wrong", "arm_pattern",
            "status_bare", "status_urllib", "status_named", "recorded_status",
            "request_host", "resolved_host", "resolved_host_robots", "robots_blocked",
            "challenge_seen", "www_authenticate", "url"]
    with open(DATA / "census.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    print(f"{len(rows)} units")
    for k, v in data["codes"]["all"].items():
        print(f"  {k:18} {v}")
    for p in predictions:
        print(f"  {p['id']}: {p['verdict']}")


if __name__ == "__main__":
    main()
