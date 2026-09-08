#!/usr/bin/env python3
"""Hollow — a model-free detector for disguised missing data in a catalogue's free text.

Session 155, cycle 003, question "Missing Data Art". Rules frozen by
artifacts/cycle-003/2026-09-08-complete-and-empty/PREREGISTRATION.md, committed before any
held-out number existed.

No model is called anywhere in this file. Standard library only. Every random draw is seeded.

Usage:
    python3 tools/hollow/hollow.py --fetch      # fetch the three house feeds, measure, write data
    python3 tools/hollow/hollow.py              # measure from a cached fetch in --cache
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import re
import sys
import urllib.request
from collections import Counter, defaultdict

FEEDS = {
    "atlas": "https://frankbueltge.de/atlas/werke.json",
    "papers": "https://frankbueltge.de/papers/index.json",
    "datasets": "https://frankbueltge.de/datasets/register.json",
}

# ---------------------------------------------------------------------------
# The frozen rule material. Nothing below this line may be extended after a
# held-out number has been seen (PREREGISTRATION.md §2).
# ---------------------------------------------------------------------------

CHROME_MARKERS = [
    r"\bedit\b",
    r"\binception:",
    r"\battributed to:",
    r"description description",
    r"&quot;",
    r"&amp;",
    r"&nbsp;",
    r"&#\d+;",
    r"retrieved from",
    r"jump to navigation",
    r"\bmain page\b",
    r"this page was last",
    r"read more",
    r"click here",
]
CHROME_RE = [(m, re.compile(m, re.IGNORECASE)) for m in CHROME_MARKERS]

TERMINAL = set(".!?…\"”’')")

OPENERS = {
    "and", "but", "or", "which", "that", "who", "whose", "whom", "while",
    "whereas", "although", "though", "because", "since", "when", "where",
    "however", "thus", "therefore", "also", "both", "such", "these", "those",
    "its", "their", "his", "her",
}

# Provenance families, first match wins. Frozen with the rules.
PROVENANCE = [
    ("Rhizome ArtBase", re.compile(r"rhizome", re.I)),
    ("dataphys.org", re.compile(r"dataphys", re.I)),
    ("S+T+ARTS / Ars Electronica", re.compile(r"S\+T\+ARTS|STARTS", re.I)),
    ("Ars Electronica (other)", re.compile(r"ars electronica|prix", re.I)),
]

SPLIT_FIELD = "title"  # sha256(title) % 2 -> 0 development, 1 held out


# ---------------------------------------------------------------------------
# Rules
# ---------------------------------------------------------------------------

def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def r1_chrome(text: str) -> list[str]:
    """Scrape-residue markers. Returns the markers that fired."""
    return [m for m, rx in CHROME_RE if rx.search(text)]


def r2_truncated_tail(text: str) -> bool:
    t = norm(text)
    return bool(t) and t[-1] not in TERMINAL


def r3_truncated_head(text: str) -> bool:
    t = norm(text)
    if not t:
        return False
    first = t[0]
    if first.isalpha() and first.islower():
        return True
    tok = re.split(r"[^\w']+", t, maxsplit=1)[0].lower()
    return tok in OPENERS


def duplicate_keys(texts: list[str]) -> set[str]:
    c = Counter(norm(t).casefold() for t in texts)
    return {k for k, n in c.items() if n > 1 and k}


def classify(text: str, dupes: set[str]) -> dict:
    t = norm(text)
    chrome = r1_chrome(t)
    r1 = bool(chrome)
    r2 = r2_truncated_tail(t)
    r3 = r3_truncated_head(t)
    r4 = t.casefold() in dupes
    return {
        "r1_chrome": r1,
        "r1_markers": chrome,
        "r2_truncated_tail": r2,
        "r3_truncated_head": r3,
        "r4_duplicate": r4,
        "hollow_strict": r1 or r4,
        "hollow_broad": r1 or r2 or r3 or r4,
    }


def provenance(venue: str) -> str:
    for name, rx in PROVENANCE:
        if rx.search(venue or ""):
            return name
    return "other"


def half(entry: dict) -> int:
    key = (entry.get(SPLIT_FIELD) or "").encode("utf-8")
    return int(hashlib.sha256(key).hexdigest(), 16) % 2


# ---------------------------------------------------------------------------
# Statistics, standard library only
# ---------------------------------------------------------------------------

def chi2_stat(table: list[list[int]]) -> float:
    rows = len(table)
    cols = len(table[0])
    n = sum(sum(r) for r in table)
    if n == 0:
        return 0.0
    rt = [sum(r) for r in table]
    ct = [sum(table[i][j] for i in range(rows)) for j in range(cols)]
    s = 0.0
    for i in range(rows):
        for j in range(cols):
            e = rt[i] * ct[j] / n
            if e > 0:
                s += (table[i][j] - e) ** 2 / e
    return s


def _gamma_q(a: float, x: float) -> float:
    """Regularised upper incomplete gamma Q(a,x) = 1 - P(a,x). Numerical Recipes form."""
    if x < 0 or a <= 0:
        raise ValueError("domain")
    if x == 0:
        return 1.0
    if x < a + 1.0:  # series for P, then complement
        ap, s, term = a, 1.0 / a, 1.0 / a
        for _ in range(1000):
            ap += 1.0
            term *= x / ap
            s += term
            if abs(term) < abs(s) * 1e-15:
                break
        return 1.0 - s * math.exp(-x + a * math.log(x) - math.lgamma(a))
    # continued fraction for Q
    tiny = 1e-300
    b, c, d = x + 1.0 - a, 1.0 / tiny, 1.0 / (x + 1.0 - a)
    h = d
    for i in range(1, 1000):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < tiny:
            d = tiny
        c = b + an / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-15:
            break
    return math.exp(-x + a * math.log(x) - math.lgamma(a)) * h


def chi2_sf(stat: float, df: int) -> float:
    """Upper tail of the chi-square distribution. Asymptotic; sparse tables are noted on the page."""
    if df <= 0:
        return 1.0
    if stat <= 0:
        return 1.0
    return _gamma_q(df / 2.0, stat / 2.0)


def perm_pvalue(labels: list[int], groups: list[str], reps: int, seed: int) -> tuple[float, float]:
    """Permutation p-value for the chi-square statistic of labels x groups."""
    keys = sorted(set(groups))
    idx = {k: i for i, k in enumerate(keys)}

    def table_of(lab):
        t = [[0] * len(keys) for _ in range(2)]
        for l, g in zip(lab, groups):
            t[l][idx[g]] += 1
        return t

    obs = chi2_stat(table_of(labels))
    rng = random.Random(seed)
    shuffled = list(labels)
    ge = 0
    for _ in range(reps):
        rng.shuffle(shuffled)
        if chi2_stat(table_of(shuffled)) >= obs - 1e-12:
            ge += 1
    return obs, (ge + 1) / (reps + 1)


def fisher_2x2(a: int, b: int, c: int, d: int) -> float:
    """Two-sided Fisher exact p-value for [[a,b],[c,d]]."""
    n = a + b + c + d
    r1, r2 = a + b, c + d
    c1 = a + c

    def prob(x):
        return (math.comb(r1, x) * math.comb(r2, c1 - x)) / math.comb(n, c1)

    lo = max(0, c1 - r2)
    hi = min(r1, c1)
    p_obs = prob(a)
    return min(1.0, sum(prob(x) for x in range(lo, hi + 1) if prob(x) <= p_obs + 1e-12))


def benjamini_hochberg(pvals: list[float], q: float) -> list[bool]:
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    keep = [False] * m
    kmax = -1
    for rank, i in enumerate(order, start=1):
        if pvals[i] <= q * rank / m:
            kmax = rank
    for rank, i in enumerate(order, start=1):
        if rank <= kmax:
            keep[i] = True
    return keep


def cohen_kappa(a: list[int], b: list[int]) -> float:
    n = len(a)
    agree = sum(1 for x, y in zip(a, b) if x == y) / n
    pa1 = sum(a) / n
    pb1 = sum(b) / n
    chance = pa1 * pb1 + (1 - pa1) * (1 - pb1)
    return (agree - chance) / (1 - chance) if chance < 1 else 0.0


def wilson(k: int, n: int, z: float = 1.959963985) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


# ---------------------------------------------------------------------------
# Feeds
# ---------------------------------------------------------------------------

def fetch(url: str, cache: str, name: str, do_fetch: bool) -> tuple[dict, str, int]:
    path = os.path.join(cache, name + ".json")
    if do_fetch:
        os.makedirs(cache, exist_ok=True)
        req = urllib.request.Request(url, headers={"User-Agent": "field-research/hollow"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read()
        with open(path, "wb") as fh:
            fh.write(raw)
    else:
        with open(path, "rb") as fh:
            raw = fh.read()
    return json.loads(raw), hashlib.sha256(raw).hexdigest(), len(raw)


def declared_missing(entries: list[dict]) -> dict:
    def empty(v):
        if v is None:
            return True
        if isinstance(v, str) and v.strip() == "":
            return True
        if isinstance(v, (list, dict)) and len(v) == 0:
            return True
        return False

    fields = sorted({k for e in entries for k in e})
    cells = miss = 0
    per = {}
    for f in fields:
        n = sum(1 for e in entries if f in e)
        m = sum(1 for e in entries if f in e and empty(e[f]))
        cells += n
        miss += m
        if m:
            per[f] = {"missing": m, "of": n}
    return {"cells": cells, "declared_missing": miss,
            "completeness_pct": round(100 * (cells - miss) / cells, 2) if cells else None,
            "per_field": per}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true", help="fetch the feeds instead of using the cache")
    ap.add_argument("--cache", default=".hollow-cache")
    ap.add_argument("--out", default="artifacts/cycle-003/2026-09-08-complete-and-empty/data")
    ap.add_argument("--reps", type=int, default=10000)
    ap.add_argument("--null-reps", type=int, default=2000)
    ap.add_argument("--audit-n", type=int, default=60)
    ap.add_argument("--seed", type=int, default=20260908)
    args = ap.parse_args()

    feeds = {}
    for name, url in FEEDS.items():
        try:
            doc, digest, nbytes = fetch(url, args.cache, name, args.fetch)
        except Exception as exc:  # a feed that cannot be read is a fact about the session
            print(f"FEED UNREACHABLE {name}: {exc}", file=sys.stderr)
            feeds[name] = {"unreachable": str(exc)}
            continue
        feeds[name] = {"url": url, "sha256": digest, "bytes": nbytes,
                       "count": len(doc.get("entries", [])), "doc": doc}

    atlas = feeds["atlas"]["doc"]["entries"]

    # --- declared missingness, all three registers -------------------------
    declared = {}
    for name in FEEDS:
        if "doc" in feeds.get(name, {}):
            declared[name] = declared_missing(feeds[name]["doc"]["entries"])

    # --- the detector on the atlas ----------------------------------------
    dupes = duplicate_keys([e["decisive_move"] for e in atlas])
    rows = []
    for e in atlas:
        flags = classify(e["decisive_move"], dupes)
        rows.append({
            "title": e["title"],
            "artist": e["artist"],
            "year": e["year"],
            "half": "held" if half(e) else "dev",
            "provenance": provenance(e["venue_prize"]),
            "verify_status": e["verify_status"],
            "medium_class": e["medium_class"],
            "form": e["form"],
            "axis_pole": e["axis_pole"],
            "decade": (e["year"][:3] + "0s") if re.match(r"^\d{4}", str(e["year"] or "")) else "unknown",
            "chars": len(norm(e["decisive_move"])),
            "source_url": e["source_url"],
            **flags,
        })

    def rate(subset, key):
        k = sum(1 for r in subset if r[key])
        n = len(subset)
        lo, hi = wilson(k, n)
        return {"k": k, "n": n, "pct": round(100 * k / n, 2) if n else None,
                "ci95": [round(100 * lo, 2), round(100 * hi, 2)]}

    dev = [r for r in rows if r["half"] == "dev"]
    held = [r for r in rows if r["half"] == "held"]

    headline = {
        "all": {k: rate(rows, k) for k in ("hollow_strict", "hollow_broad",
                                           "r1_chrome", "r2_truncated_tail",
                                           "r3_truncated_head", "r4_duplicate")},
        "dev": {k: rate(dev, k) for k in ("hollow_strict", "hollow_broad")},
        "held": {k: rate(held, k) for k in ("hollow_strict", "hollow_broad")},
    }

    # --- the twelve pre-registered association tests -----------------------
    covariates = ["verify_status", "provenance", "medium_class", "form", "axis_pole", "decade"]
    tests = []
    for label in ("hollow_broad", "hollow_strict"):
        for cov in covariates:
            groups = [r[cov] for r in held]
            labels = [1 if r[label] else 0 for r in held]
            stat, p = perm_pvalue(labels, groups, args.reps, args.seed + len(tests))
            df = (2 - 1) * (len(set(groups)) - 1)
            tab = defaultdict(lambda: [0, 0])
            for l, g in zip(labels, groups):
                tab[g][l] += 1
            tests.append({
                "label": label, "covariate": cov, "chi2": round(stat, 3), "df": df,
                "p_perm": round(p, 5), "p_chi2": chi2_sf(stat, df), "levels": len(set(groups)),
                "table": {g: {"not": v[0], "hollow": v[1]} for g, v in sorted(tab.items())},
            })
    keep = benjamini_hochberg([t["p_perm"] for t in tests], 0.05)
    keep_chi2 = benjamini_hochberg([t["p_chi2"] for t in tests], 0.05)
    for t, k, k2 in zip(tests, keep, keep_chi2):
        t["bh_survivor"] = bool(k)
        t["bh_survivor_chi2"] = bool(k2)

    # --- null world: permute each label vector, rerun the whole test set ----
    # The asymptotic p-value family is used on both sides so the comparison is like for like;
    # a permutation p-value with a floor of 1/(reps+1) could not clear the BH threshold of
    # 0.05/12 in an affordable number of inner replicates, which would bias the null to zero.
    rng = random.Random(args.seed + 999)
    group_vectors = {cov: [r[cov] for r in held] for cov in covariates}
    null_counts = []
    for _ in range(args.null_reps):
        ps = []
        for label in ("hollow_broad", "hollow_strict"):
            perm = [1 if r[label] else 0 for r in held]
            rng.shuffle(perm)
            for cov in covariates:
                g = group_vectors[cov]
                keys = sorted(set(g))
                idx = {k: i for i, k in enumerate(keys)}
                t = [[0] * len(keys) for _ in range(2)]
                for l, gg in zip(perm, g):
                    t[l][idx[gg]] += 1
                ps.append(chi2_sf(chi2_stat(t), len(keys) - 1))
        null_counts.append(sum(benjamini_hochberg(ps, 0.05)))
    null_summary = {
        "replicates": args.null_reps,
        "p_family": "asymptotic chi-square, both observed and null",
        "observed_survivors_chi2_family": sum(1 for t in tests if t["bh_survivor_chi2"]),
        "mean_survivors": round(sum(null_counts) / len(null_counts), 3),
        "distribution": dict(sorted(Counter(null_counts).items())),
    }

    # --- P3, the 2x2 on verify_status, Fisher exact ------------------------
    a = sum(1 for r in held if r["verify_status"] == "toVerify" and r["hollow_broad"])
    b = sum(1 for r in held if r["verify_status"] == "toVerify" and not r["hollow_broad"])
    c = sum(1 for r in held if r["verify_status"] == "verified" and r["hollow_broad"])
    d = sum(1 for r in held if r["verify_status"] == "verified" and not r["hollow_broad"])
    p3 = {
        "toVerify": {"hollow": a, "not": b, "pct": round(100 * a / (a + b), 2) if a + b else None},
        "verified": {"hollow": c, "not": d, "pct": round(100 * c / (c + d), 2) if c + d else None},
        "fisher_p": round(fisher_2x2(a, b, c, d), 6),
    }
    p3["points_difference"] = round((p3["toVerify"]["pct"] or 0) - (p3["verified"]["pct"] or 0), 2)

    # --- P5, the datasets register's free text -----------------------------
    p5 = {}
    if "doc" in feeds.get("datasets", {}):
        ds = feeds["datasets"]["doc"]["entries"]
        for field in ("relevanz", "pruef_vermerk", "aufnahmegrund"):
            texts = [str(e.get(field) or "") for e in ds]
            nonempty = [t for t in texts if norm(t)]
            dd = duplicate_keys(nonempty)
            flags = [classify(t, dd) for t in nonempty]
            p5[field] = {
                "n_nonempty": len(nonempty), "n_entries": len(ds),
                "hollow_strict": sum(1 for f in flags if f["hollow_strict"]),
                "hollow_broad": sum(1 for f in flags if f["hollow_broad"]),
                "strict_pct": round(100 * sum(1 for f in flags if f["hollow_strict"]) / len(nonempty), 2) if nonempty else None,
            }

    # --- the audit sample, drawn now, labelled by hand afterwards ----------
    rng2 = random.Random(args.seed)
    sample = rng2.sample(sorted(held, key=lambda r: r["title"]), min(args.audit_n, len(held)))
    audit_stub = [{"title": r["title"], "artist": r["artist"], "provenance": r["provenance"],
                   "hollow_broad": r["hollow_broad"], "hollow_strict": r["hollow_strict"],
                   "chars": r["chars"]} for r in sample]

    # --- the second reading: what the catalogue is missing ------------------
    prov_counts = Counter(r["provenance"] for r in rows)
    decade_counts = Counter(r["decade"] for r in rows)
    prov_hollow = {}
    for g in prov_counts:
        sub = [r for r in rows if r["provenance"] == g]
        prov_hollow[g] = {"n": len(sub),
                          "hollow_broad_pct": round(100 * sum(1 for r in sub if r["hollow_broad"]) / len(sub), 2),
                          "hollow_strict_pct": round(100 * sum(1 for r in sub if r["hollow_strict"]) / len(sub), 2)}

    out = {
        "generated_by": "tools/hollow/hollow.py",
        "date": "2026-09-08",
        "session": 155,
        "cycle": 3,
        "question": "Missing Data Art",
        "feeds": {k: {kk: vv for kk, vv in v.items() if kk != "doc"} for k, v in feeds.items()},
        "declared_missing": declared,
        "split": {"rule": "sha256(title) mod 2", "dev": len(dev), "held": len(held)},
        "headline": headline,
        "tests": tests,
        "null_world": null_summary,
        "p3_verify_status": p3,
        "p5_datasets_register": p5,
        "provenance_counts": dict(prov_counts.most_common()),
        "provenance_hollow": prov_hollow,
        "decade_counts": dict(sorted(decade_counts.items())),
        "params": {"reps": args.reps, "null_reps": args.null_reps, "seed": args.seed,
                   "audit_n": args.audit_n},
    }

    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "results.json"), "w") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False, sort_keys=False)
    with open(os.path.join(args.out, "entries.json"), "w") as fh:
        json.dump(rows, fh, indent=1, ensure_ascii=False)
    stub_path = os.path.join(args.out, "audit-sample.json")
    if not os.path.exists(stub_path):
        with open(stub_path, "w") as fh:
            json.dump(audit_stub, fh, indent=1, ensure_ascii=False)

    print(json.dumps({"headline": headline, "p3": p3, "null": null_summary,
                      "survivors": sum(1 for t in tests if t["bh_survivor"]),
                      "p5": p5}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
