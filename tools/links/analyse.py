#!/usr/bin/env python3
"""Compute every figure the page shows, from data/papers.csv + urls.csv + probes.csv.
Writes data/summary.json. Nothing on the page is typed by hand; change a definition
here and the page changes with it.

Usage: python3 tools/links/analyse.py <datadir>
"""
import csv, json, math, os, sys
from collections import defaultdict


def wilson(k, n, z=1.96):
    """Wilson score interval for a binomial proportion."""
    if n == 0:
        return [None, None]
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(centre - half, 4), round(centre + half, 4)]


def two_proportion_z(k1, n1, k2, n2):
    if min(n1, n2) == 0:
        return None
    p1, p2 = k1 / n1, k2 / n2
    p = (k1 + k2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    if se == 0:
        return None
    z = (p1 - p2) / se
    # two-sided p from the normal tail
    pval = math.erfc(abs(z) / math.sqrt(2))
    return {"z": round(z, 3), "p": float("%.2g" % pval)}


def fisher_exact_two_sided(a, b, c, d):
    """Two-sided Fisher exact test on the 2x2 table [[a, b], [c, d]] by summing the
    probability of every table at least as extreme as the observed one."""
    from math import comb
    n = a + b + c + d
    row1, col1 = a + b, a + c
    total = comb(n, row1)

    def prob(x):
        return comb(col1, x) * comb(n - col1, row1 - x) / total

    p_obs = prob(a)
    lo = max(0, row1 - (n - col1))
    hi = min(row1, col1)
    p = sum(prob(x) for x in range(lo, hi + 1) if prob(x) <= p_obs * (1 + 1e-9))
    return float("%.2g" % min(p, 1.0))


def host_class(host):
    """Classes of host, not vendor names: the page reports where a link points in kind,
    and data/urls.csv keeps every address itself."""
    h = host.lower()
    if h.endswith("github.com") or h.endswith("gitlab.com") or h.endswith("bitbucket.org"):
        return "code hosting"
    if h.endswith("huggingface.co"):
        return "model and dataset hosting"
    if "anonymous" in h or "openreview" in h:
        return "anonymised review host"
    if h.endswith("github.io") or h.endswith("gitlab.io") or h.startswith("sites.google."):
        return "project page (static hosting)"
    if "youtube" in h or "youtu.be" in h or "vimeo" in h:
        return "video"
    if h.endswith("zenodo.org") or h.endswith("figshare.com") or h.endswith("osf.io"):
        return "archive or repository of record"
    return "other host (own or institutional domain)"


def quarter(datestr):
    y, m = int(datestr[:4]), int(datestr[5:7])
    return "%dQ%d" % (y, (m - 1) // 3 + 1)


def rate(k, n):
    return None if n == 0 else round(k / n, 6)


def main():
    d = sys.argv[1]
    papers = list(csv.DictReader(open(os.path.join(d, "papers.csv"))))
    urls = list(csv.DictReader(open(os.path.join(d, "urls.csv"))))
    probes = {r["url"]: r for r in csv.DictReader(open(os.path.join(d, "probes.csv")))}

    out = {"generated_utc": None, "cohorts": {}, "by_quarter": {}, "by_host": {},
           "hosts_top": {}, "conjecture": {}, "indeterminate": {}}

    # ---------- declaration ----------
    for c in ("A", "B"):
        ps = [p for p in papers if p["cohort"] == c]
        with_url = [p for p in ps if int(p["n_urls"]) > 0]
        out["cohorts"][c] = {
            "papers": len(ps),
            "papers_with_abstract_url": len(with_url),
            "declaration_rate": rate(len(with_url), len(ps)),
            "declaration_ci": wilson(len(with_url), len(ps)),
        }
    out["declaration_diff"] = two_proportion_z(
        out["cohorts"]["A"]["papers_with_abstract_url"], out["cohorts"]["A"]["papers"],
        out["cohorts"]["B"]["papers_with_abstract_url"], out["cohorts"]["B"]["papers"])

    # ---------- resolution (URL level) ----------
    per_cohort_urls = defaultdict(list)
    for u in urls:
        pr = probes.get(u["url"])
        if pr:
            per_cohort_urls[u["cohort"]].append({**u, "outcome": pr["outcome"],
                                                 "method": pr["method"], "note": pr["note"]})
    for c in ("A", "B"):
        us = per_cohort_urls[c]
        reach = sum(1 for u in us if u["outcome"] == "reachable")
        gone = sum(1 for u in us if u["outcome"] == "gone")
        ind = sum(1 for u in us if u["outcome"] == "indeterminate")
        out["cohorts"][c].update({
            "urls": len(us), "reachable": reach, "gone": gone, "indeterminate": ind,
            "resolution_rate": rate(reach, reach + gone),
            "resolution_ci": wilson(reach, reach + gone),
        })
        # paper-level: at least one declared URL that opens
        by_paper = defaultdict(list)
        for u in us:
            by_paper[u["arxiv_id"]].append(u["outcome"])
        decided = {k: v for k, v in by_paper.items() if any(o != "indeterminate" for o in v)}
        ok = sum(1 for v in decided.values() if "reachable" in v)
        out["cohorts"][c].update({
            "papers_decided": len(decided), "papers_any_open": ok,
            "paper_resolution_rate": rate(ok, len(decided)),
            "paper_resolution_ci": wilson(ok, len(decided)),
        })
    A, B = out["cohorts"]["A"], out["cohorts"]["B"]
    out["resolution_diff"] = two_proportion_z(A["reachable"], A["reachable"] + A["gone"],
                                              B["reachable"], B["reachable"] + B["gone"])

    # ---------- by quarter ----------
    for c in ("A", "B"):
        buckets = defaultdict(lambda: {"papers": 0, "with_url": 0, "reachable": 0, "gone": 0,
                                       "indeterminate": 0})
        for p in papers:
            if p["cohort"] != c:
                continue
            q = quarter(p["published"])
            buckets[q]["papers"] += 1
            if int(p["n_urls"]) > 0:
                buckets[q]["with_url"] += 1
        for u in per_cohort_urls[c]:
            buckets[quarter(u["published"])][u["outcome"]] += 1
        out["by_quarter"][c] = {}
        for q in sorted(buckets):
            b = buckets[q]
            out["by_quarter"][c][q] = {**b,
                                       "declaration_rate": rate(b["with_url"], b["papers"]),
                                       "resolution_rate": rate(b["reachable"],
                                                               b["reachable"] + b["gone"])}

    # ---------- how old the links actually are ----------
    import datetime
    probe_day = datetime.date(2026, 8, 31)
    for c in ("A", "B"):
        ages = sorted((probe_day - datetime.date(*map(int, u["published"].split("-")))).days
                      for u in per_cohort_urls[c])
        out["cohorts"][c]["median_link_age_days"] = (ages[len(ages) // 2] if ages else None)
        out["cohorts"][c]["links_older_than_one_year"] = sum(1 for a in ages if a >= 365)

    # ---------- minimum detectable effect on the resolution comparison ----------
    n1, n2 = A["reachable"] + A["gone"], B["reachable"] + B["gone"]
    if min(n1, n2) > 0:
        pp = (A["reachable"] + B["reachable"]) / (n1 + n2)
        out["resolution_mde_points"] = round(
            100 * (1.96 + 0.8416) * math.sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2)), 1)
    else:
        out["resolution_mde_points"] = None
    out["distinct_urls_probed"] = len(probes)
    out["probed_utc"] = sorted(r["probed_utc"] for r in probes.values())[-1] if probes else None
    out["declared_links_total"] = len(urls)

    # ---------- by host class ----------
    for c in ("A", "B"):
        groups = defaultdict(lambda: {"reachable": 0, "gone": 0, "indeterminate": 0})
        hosts = defaultdict(lambda: {"n": 0, "gone": 0})
        for u in per_cohort_urls[c]:
            g = "code" if host_class(u["host"]) == "code hosting" else "other"
            groups[g][u["outcome"]] += 1
            k = host_class(u["host"])
            hosts[k]["n"] += 1
            if u["outcome"] == "gone":
                hosts[k]["gone"] += 1
        out["by_host"][c] = {g: {**v, "resolution_rate": rate(v["reachable"],
                                                              v["reachable"] + v["gone"])}
                             for g, v in groups.items()}
        out["hosts_top"][c] = sorted(({"host": h, **v} for h, v in hosts.items()),
                                     key=lambda r: -r["n"])

    # ---------- composition of cohort A: which phrases carried it ----------
    ph = defaultdict(int)
    for p in papers:
        if p["cohort"] != "A":
            continue
        for one in filter(None, p["phrases"].split("|")):
            ph[one] += 1
    out["phrase_counts"] = dict(sorted(ph.items(), key=lambda kv: -kv[1]))

    # ---------- what the dead links actually are ----------
    dead = []
    for u in urls:
        pr = probes.get(u["url"])
        if pr and pr["outcome"] == "gone":
            dead.append({"cohort": u["cohort"], "published": u["published"],
                         "where": host_class(u["host"]), "note": pr["note"]})
    dead.sort(key=lambda r: r["published"])
    out["dead_links"] = dead
    out["dead_oldest_published"] = dead[0]["published"] if dead else None
    # how do the oldest links in the study behave?
    old = [u for u in urls if u["published"] < "2025-01-01"]
    old_dec = [u for u in old if probes.get(u["url"], {}).get("outcome") in ("reachable", "gone")]
    n_reach_old = sum(1 for u in old_dec if probes[u["url"]]["outcome"] == "reachable")
    fail_rate = (A_gone_total := None)
    out["links_2024"] = {
        "declared": len(old), "decidable": len(old_dec), "reachable": n_reach_old}

    # what chance alone predicts for the oldest links, so their survival is not over-read
    all_dec = [u for u in urls if probes.get(u["url"], {}).get("outcome") in ("reachable", "gone")]
    n_gone = sum(1 for u in all_dec if probes[u["url"]]["outcome"] == "gone")
    if all_dec and out["links_2024"]["decidable"]:
        rate_fail = n_gone / len(all_dec)
        k = out["links_2024"]["decidable"]
        out["links_2024"]["overall_failure_rate"] = round(rate_fail, 4)
        out["links_2024"]["expected_failures"] = round(rate_fail * k, 2)
        out["links_2024"]["p_zero_failures_by_chance"] = round((1 - rate_fail) ** k, 3)

    # ---------- trend with an interval, not a bare slope ----------
    out["trend_test"] = {}
    for c in ("A", "B"):
        us = [u for u in per_cohort_urls[c] if u["outcome"] in ("reachable", "gone")]
        us.sort(key=lambda u: u["published"])
        half = len(us) // 2
        older, newer = us[:half], us[half:]
        k1 = sum(1 for u in older if u["outcome"] == "reachable")
        k2 = sum(1 for u in newer if u["outcome"] == "reachable")
        out["trend_test"][c] = {
            "older_half": "%d/%d" % (k1, len(older)), "newer_half": "%d/%d" % (k2, len(newer)),
            "test": two_proportion_z(k1, len(older), k2, len(newer)),
            "fisher_p": fisher_exact_two_sided(k1, len(older) - k1, k2, len(newer) - k2),
            "split": "by rank at the median; links sharing the median date fall on either side"}

    # ---------- clustering of the control sample in submission time ----------
    out["clustering"] = {}
    for c in ("A", "B"):
        days = defaultdict(int)
        for p in papers:
            if p["cohort"] == c:
                days[p["published"]] += 1
        sizes = list(days.values())
        mbar = sum(sizes) / len(sizes)
        out["clustering"][c] = {"papers": sum(sizes), "distinct_days": len(sizes),
                                "mean_per_day": round(mbar, 2), "max_per_day": max(sizes)}
    # cluster bootstrap of the declaration difference, resampling whole submission days
    import random
    rng = random.Random(20260831)
    by_day = {"A": defaultdict(list), "B": defaultdict(list)}
    for p in papers:
        by_day[p["cohort"]][p["published"]].append(1 if int(p["n_urls"]) > 0 else 0)
    diffs = []
    for _ in range(4000):
        vals = {}
        for c in ("A", "B"):
            days = list(by_day[c])
            draw = [by_day[c][rng.choice(days)] for _ in days]
            flat = [x for grp in draw for x in grp]
            vals[c] = sum(flat) / len(flat)
        diffs.append(vals["A"] - vals["B"])
    diffs.sort()
    out["declaration_cluster_bootstrap"] = {
        "iterations": len(diffs),
        "ci95_points": [round(100 * diffs[int(.025 * len(diffs))], 2),
                        round(100 * diffs[int(.975 * len(diffs))], 2)],
        "share_at_or_below_zero": round(sum(1 for d in diffs if d <= 0) / len(diffs), 4),
        "method": "resampling whole submission days with replacement within each cohort"}

    # ---------- control composition ----------
    prim = defaultdict(int)
    for p in papers:
        if p["cohort"] == "B":
            prim[p["primary_category"]] += 1
    out["control_primary_categories"] = dict(sorted(prim.items(), key=lambda kv: -kv[1])[:6])
    out["control_primary_csai"] = prim.get("cs.AI", 0)

    # ---------- links declared by more than one paper ----------
    seen = defaultdict(int)
    for u in urls:
        seen[u["url"]] += 1
    out["duplicate_declarations"] = sum(1 for v in seen.values() if v > 1)

    # ---------- indeterminate accounting (the honest column) ----------
    notes = defaultdict(int)
    for u in urls:
        pr = probes.get(u["url"])
        if pr and pr["outcome"] == "indeterminate":
            notes[pr["note"].split(":")[0]] += 1
    out["indeterminate"] = {"by_note": dict(sorted(notes.items(), key=lambda kv: -kv[1])),
                            "total": sum(notes.values())}

    # ---------- conjecture verdicts, computed not asserted ----------
    c1 = A["declaration_rate"] > B["declaration_rate"]
    c2 = A["resolution_rate"] is not None and B["resolution_rate"] is not None \
        and A["resolution_rate"] <= B["resolution_rate"]
    qa = [v["resolution_rate"] for q, v in sorted(out["by_quarter"]["A"].items())
          if v["resolution_rate"] is not None]
    qb = [v["resolution_rate"] for q, v in sorted(out["by_quarter"]["B"].items())
          if v["resolution_rate"] is not None]
    def trend(series):
        """Sign of the least-squares slope over the ordered quarters."""
        n = len(series)
        if n < 3:
            return None
        xs = list(range(n))
        mx, my = sum(xs) / n, sum(series) / n
        num = sum((x - mx) * (y - my) for x, y in zip(xs, series))
        den = sum((x - mx) ** 2 for x in xs)
        return round(num / den, 5) if den else None
    out["conjecture"] = {
        "1_declaration_higher_in_A": {"held": bool(c1), "A": A["declaration_rate"],
                                      "B": B["declaration_rate"]},
        "2_resolution_no_better_in_A": {"held": bool(c2), "A": A["resolution_rate"],
                                        "B": B["resolution_rate"]},
        "3_resolution_falls_with_age": {"slope_A_by_quarter": trend(qa),
                                        "slope_B_by_quarter": trend(qb),
                                        "note": "older quarters first; a positive slope means "
                                                "newer papers resolve better"},
    }

    import time
    out["generated_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    harvest = json.load(open(os.path.join(d, "harvest.json")))
    out["harvest"] = harvest
    json.dump(out, open(os.path.join(d, "summary.json"), "w"), indent=2)
    print(json.dumps(out, indent=2)[:4000])


if __name__ == "__main__":
    main()
