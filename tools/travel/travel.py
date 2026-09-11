#!/usr/bin/env python3
"""Travel — carry the frozen hollowness screen to catalogues this practice did not build.

Session 157, cycle 003, question "Missing Data Art". Every population, rule, split, statistic,
prediction and kill condition is fixed by
artifacts/cycle-003/2026-09-11-does-it-travel/PREREGISTRATION.md, committed before the first
record was fetched.

R1-R4 are imported from tools/hollow/hollow.py and are NOT re-implemented here, so that the
screen carried abroad is byte-for-byte the screen used at home on 2026-09-08. R5 is defined in
this file and is reported separately everywhere, because it was added after the frozen set
(PREREGISTRATION.md §1.3).

No model is called anywhere in this file. Standard library only. Every random draw is seeded.

Usage:
    python3 tools/travel/travel.py --cache <dir> --out <dir> [--stage measure|join]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "hollow"))
import hollow  # noqa: E402  the frozen rules, imported and not copied

SEED = 20260911
MIN_STRATUM = 20          # pooling floor, PREREGISTRATION.md §3.4
PERM_REPS = 10000
AUDIT_PER_CATALOGUE = 30

CATALOGUE_LABEL = {
    "atlas": "Atlas of Data Art (home arm)",
    "cma": "Cleveland Museum of Art",
    "uk": "data.gov.uk",
    "govdata": "govdata.de",
    "aic": "Art Institute of Chicago",
}


# ---------------------------------------------------------------------------
# R5 — title echo. Added 2026-09-11, origin disclosed in the pre-registration.
# ---------------------------------------------------------------------------

def r5_title_echo(text: str, title: str) -> bool:
    t = hollow.norm(text).casefold().rstrip(" .;:,-–—")
    ti = hollow.norm(title).casefold().rstrip(" .;:,-–—")
    if not t or not ti:
        return False
    if t == ti:
        return True
    if t in ti:
        return True
    if ti in t and len(t) <= 1.25 * len(ti):
        return True
    return False


# R3's two limbs, counted separately for P5. The rule itself is untouched.
def r3_limbs(text: str) -> tuple[bool, bool]:
    t = hollow.norm(text)
    if not t:
        return (False, False)
    lower = bool(t[0].isalpha() and t[0].islower())
    tok = re.split(r"[^\w']+", t, maxsplit=1)[0].lower()
    opener = tok in hollow.OPENERS
    return (lower, opener)


def half_of(rec_id: str) -> int:
    return int(hashlib.sha256(rec_id.encode("utf-8")).hexdigest(), 16) % 2


def load(cache: str, name: str) -> list[dict]:
    path = os.path.join(cache, f"{name}.jsonl")
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


# ---------------------------------------------------------------------------
# Permutation test: shuffle the stratum vector, take the first K as flagged.
# ---------------------------------------------------------------------------

def perm_test(labels: list[int], groups: list[str], reps: int, seed: int) -> dict:
    keys = sorted(set(groups))
    idx = {k: i for i, k in enumerate(keys)}
    gvec = [idx[g] for g in groups]
    sizes = [0] * len(keys)
    for gi in gvec:
        sizes[gi] += 1
    K = sum(labels)
    n = len(labels)

    def chi2_from_counts(cnt: list[int]) -> float:
        if K == 0 or K == n:
            return 0.0
        s = 0.0
        for gi, ng in enumerate(sizes):
            if ng == 0:
                continue
            e1 = ng * K / n
            e0 = ng - e1
            o1 = cnt[gi]
            o0 = ng - o1
            if e1 > 0:
                s += (o1 - e1) ** 2 / e1
            if e0 > 0:
                s += (o0 - e0) ** 2 / e0
        return s

    obs_cnt = [0] * len(keys)
    for l, gi in zip(labels, gvec):
        obs_cnt[gi] += l
    obs = chi2_from_counts(obs_cnt)

    # A permutation of the label vector is the same thing as a uniform choice of which K of the
    # n records carry the label, so each replicate draws that subset directly. Identical null,
    # and it does not walk the whole vector once per replicate.
    rng = random.Random(seed)
    nk = len(keys)
    ge = 0
    for _ in range(reps):
        tally = Counter(rng.sample(gvec, K))
        cnt = [tally.get(i, 0) for i in range(nk)]
        if chi2_from_counts(cnt) >= obs - 1e-9:
            ge += 1
    df = len(keys) - 1
    return {"chi2": round(obs, 3), "df": df, "levels": len(keys),
            "p_perm": (ge + 1) / (reps + 1), "p_chi2": hollow.chi2_sf(obs, df),
            "reps": reps, "flagged": K, "n": n}


def pooled_strata(rows: list[dict], floor: int) -> dict[str, str]:
    counts = Counter(r["stratum"] or "(none)" for r in rows)
    return {k: (k if v >= floor else "(small strata)") for k, v in counts.items()}


# ---------------------------------------------------------------------------
# Per-catalogue measurement
# ---------------------------------------------------------------------------

def measure(name: str, recs: list[dict], atlas_provenance: bool = False) -> dict:
    n_records = len(recs)
    present = [r for r in recs if hollow.norm(r.get("text", ""))]
    n_present = len(present)
    fill = 100 * n_present / n_records if n_records else 0.0

    res = {
        "catalogue": name,
        "label": CATALOGUE_LABEL.get(name, name),
        "records": n_records,
        "present": n_present,
        "declared_completeness_pct": round(fill, 2),
        "k1_fired": fill < 20.0,
    }
    if res["k1_fired"]:
        res["note"] = "K1: descriptive field non-empty on under 20 % of records; no screen run."
        return res

    dupes = hollow.duplicate_keys([r["text"] for r in present])
    rows = []
    for r in present:
        f = hollow.classify(r["text"], dupes)
        lower, opener = r3_limbs(r["text"])
        stratum = r["stratum"] or "(none)"
        if atlas_provenance:
            stratum = hollow.provenance(stratum)
        rows.append({
            "id": r["id"], "title": r.get("title", ""), "url": r.get("url", ""),
            "stratum": stratum, "half": "held" if half_of(r["id"]) else "dev",
            "chars": len(hollow.norm(r["text"])),
            "r5_title_echo": r5_title_echo(r["text"], r.get("title", "")),
            "r3_lower": lower, "r3_opener": opener,
            **f,
        })
    for r in rows:
        r["hollow_broad5"] = r["hollow_broad"] or r["r5_title_echo"]

    held = [r for r in rows if r["half"] == "held"]
    dev = [r for r in rows if r["half"] == "dev"]

    def rate(subset, key):
        k = sum(1 for r in subset if r[key])
        n = len(subset)
        lo, hi = hollow.wilson(k, n)
        return {"k": k, "n": n, "pct": round(100 * k / n, 2) if n else None,
                "ci95": [round(100 * lo, 2), round(100 * hi, 2)]}

    keys = ("r1_chrome", "r2_truncated_tail", "r3_truncated_head", "r4_duplicate",
            "r5_title_echo", "r3_lower", "r3_opener", "hollow_strict", "hollow_broad",
            "hollow_broad5")
    res["held"] = {k: rate(held, k) for k in keys}
    res["dev"] = {k: rate(dev, k) for k in keys}
    res["all"] = {k: rate(rows, k) for k in keys}
    res["split"] = {"dev": len(dev), "held": len(held), "rule": "sha256(id) mod 2"}

    # P3 — how much of the broad aggregate is R2 alone
    agree = sum(1 for r in held if r["hollow_broad"] == r["r2_truncated_tail"])
    res["p3_broad_is_r2"] = {
        "agree": agree, "n": len(held),
        "pct": round(100 * agree / len(held), 2) if held else None,
    }
    # P6 — what R5 adds beyond the frozen four
    add = [r for r in held if r["r5_title_echo"] and not r["hollow_broad"]]
    res["p6_r5_increment"] = {"r5_only": len(add), "r5_total": sum(1 for r in held if r["r5_title_echo"]),
                              "n": len(held)}

    # P2 — the primary association test, held-out half only
    pool = pooled_strata(held, MIN_STRATUM)
    groups = [pool[r["stratum"]] for r in held]
    big = sorted({g for g in groups if g != "(small strata)"})
    res["k2_fired"] = len(big) < 2
    if not res["k2_fired"]:
        labels = [1 if r["hollow_broad"] else 0 for r in held]
        res["association"] = perm_test(labels, groups, PERM_REPS, SEED)
        tab = defaultdict(lambda: [0, 0])
        for l, g in zip(labels, groups):
            tab[g][l] += 1
        res["association"]["table"] = {
            g: {"records": v[0] + v[1], "flagged": v[1],
                "pct": round(100 * v[1] / (v[0] + v[1]), 2)}
            for g, v in sorted(tab.items(), key=lambda kv: -(kv[1][1]))
        }
        total_flag = sum(labels)
        top = max(res["association"]["table"].items(), key=lambda kv: kv[1]["flagged"])
        # Exploratory, and labelled exploratory on the page: the pre-registered concentration
        # ratio is not scale-free — with many strata and a high base rate no single stratum can
        # reach twice its record share. These are descriptive and decide nothing.
        tb = res["association"]["table"]
        rates = sorted(v["pct"] for v in tb.values())
        top5 = sum(v["flagged"] for v in list(tb.values())[:5])
        res["exploratory_spread"] = {
            "strata": len(tb),
            "strata_above_90pct": sum(1 for v in tb.values() if v["pct"] > 90),
            "strata_below_10pct": sum(1 for v in tb.values() if v["pct"] < 10),
            "min_rate_pct": rates[0], "max_rate_pct": rates[-1],
            "median_rate_pct": rates[len(rates) // 2],
            "top5_flag_share_pct": round(100 * top5 / total_flag, 2) if total_flag else None,
        }
        res["concentration"] = {
            "top_stratum": top[0],
            "flag_share_pct": round(100 * top[1]["flagged"] / total_flag, 2) if total_flag else None,
            "record_share_pct": round(100 * top[1]["records"] / len(held), 2),
            "ratio": round((top[1]["flagged"] / total_flag) / (top[1]["records"] / len(held)), 3)
            if total_flag else None,
            "strata_total": len(set(groups)),
        }
    else:
        res["note_k2"] = "K2: fewer than two strata with 20 or more held-out records."

    res["_rows"] = rows
    return res


# ---------------------------------------------------------------------------
# Audit sheet — opaque id and value text only (PREREGISTRATION.md §3.3)
# ---------------------------------------------------------------------------

def build_audit_sheet(measures: dict, cache: str, out: str) -> None:
    sheet_path = os.path.join(out, "audit-sheet.json")
    if os.path.exists(sheet_path):
        return
    rng = random.Random(SEED)
    sheet = []
    for name in ("cma", "uk"):
        if "_rows" not in measures.get(name, {}):
            return
        recs = {r["id"]: r for r in load(cache, name)}
        held = [r for r in measures[name]["_rows"] if r["half"] == "held"]
        pick = rng.sample(sorted(held, key=lambda r: r["id"]), AUDIT_PER_CATALOGUE)
        for r in pick:
            raw = recs[r["id"]]["text"]
            sheet.append({
                "aid": hashlib.sha1(f"{name}:{r['id']}:{SEED}".encode()).hexdigest()[:10],
                "value": hollow.norm(raw)[:1200],
            })
    rng.shuffle(sheet)
    with open(sheet_path, "w", encoding="utf-8") as fh:
        json.dump(sheet, fh, indent=1, ensure_ascii=False)
    print(f"wrote {sheet_path} ({len(sheet)} values, no flags, no titles)", file=sys.stderr)

    # A second sheet, declared post-hoc on the page. It carries one fact the blind sheet cannot:
    # how many records in the same catalogue carry this identical value. R4 is a property of a
    # value's relation to the rest of the catalogue, and a reader of one value in isolation
    # cannot see it — so the blind pass cannot validate R4 even in principle.
    counts = {}
    for name in ("cma", "uk"):
        recs = {r["id"]: r for r in load(cache, name)}
        cc = Counter(hollow.norm(r["text"]).casefold() for r in recs.values()
                     if hollow.norm(r["text"]))
        for r in measures[name]["_rows"]:
            aid = hashlib.sha1(f"{name}:{r['id']}:{SEED}".encode()).hexdigest()[:10]
            counts[aid] = cc[hollow.norm(recs[r["id"]]["text"]).casefold()]
    informed = [{"aid": s["aid"], "value": s["value"],
                 "identical_value_on_records": counts.get(s["aid"])} for s in sheet]
    with open(os.path.join(out, "audit-sheet-informed.json"), "w", encoding="utf-8") as fh:
        json.dump(informed, fh, indent=1, ensure_ascii=False)


def join_audit(measures: dict, out: str) -> dict | None:
    labels_path = os.path.join(out, "audit-labels.json")
    if not os.path.exists(labels_path):
        return None
    labels = {x["aid"]: x["label"] for x in json.load(open(labels_path, encoding="utf-8"))}
    inf_path = os.path.join(out, "audit-labels-informed.json")
    informed = ({x["aid"]: x["label"] for x in json.load(open(inf_path, encoding="utf-8"))}
                if os.path.exists(inf_path) else {})
    key = {}
    for name in ("cma", "uk"):
        for r in measures.get(name, {}).get("_rows", []):
            aid = hashlib.sha1(f"{name}:{r['id']}:{SEED}".encode()).hexdigest()[:10]
            key[aid] = (name, r)
    joined, undecidable = [], 0
    for aid, lab in labels.items():
        if aid not in key:
            continue
        name, r = key[aid]
        if lab == "cannot tell":
            undecidable += 1
            continue
        joined.append({"aid": aid, "catalogue": name,
                       "reader_hollow": 1 if lab == "says nothing" else 0,
                       "screen_broad": 1 if r["hollow_broad"] else 0,
                       "screen_broad5": 1 if r["hollow_broad5"] else 0,
                       "screen_strict": 1 if r["hollow_strict"] else 0})
    a = [j["reader_hollow"] for j in joined]
    b = [j["screen_broad"] for j in joined]
    b5 = [j["screen_broad5"] for j in joined]
    tp = sum(1 for j in joined if j["screen_broad"] and j["reader_hollow"])
    fp = sum(1 for j in joined if j["screen_broad"] and not j["reader_hollow"])
    fn = sum(1 for j in joined if not j["screen_broad"] and j["reader_hollow"])
    tn = sum(1 for j in joined if not j["screen_broad"] and not j["reader_hollow"])
    agree = sum(1 for x, y in zip(a, b) if x == y)
    out_d = {
        "labelled": len(labels), "joined": len(joined), "cannot_tell": undecidable,
        "reader_says_nothing": sum(a), "screen_flags": sum(b),
        "agreement_pct": round(100 * agree / len(joined), 2) if joined else None,
        "kappa": round(hollow.cohen_kappa(a, b), 4) if joined else None,
        "kappa_broad5": round(hollow.cohen_kappa(a, b5), 4) if joined else None,
        "confusion": {"tp": tp, "fp": fp, "fn": fn, "tn": tn},
        "precision": round(tp / (tp + fp), 4) if tp + fp else None,
        "recall": round(tp / (tp + fn), 4) if tp + fn else None,
    }
    if informed:
        pairs = [(informed[aid], key[aid][1]) for aid in informed if aid in key
                 and informed[aid] != "cannot tell"]
        ai = [1 if lab == "says nothing" else 0 for lab, _ in pairs]
        bi = [1 if r["hollow_broad"] else 0 for _, r in pairs]
        out_d["informed_pass"] = {
            "_note": "Post-hoc, declared: a second labelling of the same 60 values in which the "
                     "reader was told how many records carry the identical value, and nothing "
                     "else. R4 is a relation between values; a reader of one value alone cannot "
                     "see it, so the blind pass cannot validate R4 even in principle.",
            "joined": len(pairs), "reader_says_nothing": sum(ai), "screen_flags": sum(bi),
            "agreement_pct": round(100 * sum(1 for x, y in zip(ai, bi) if x == y) / len(pairs), 2)
            if pairs else None,
            "kappa": round(hollow.cohen_kappa(ai, bi), 4) if pairs else None,
        }
    for name in ("cma", "uk"):
        sub = [j for j in joined if j["catalogue"] == name]
        if sub:
            aa = [j["reader_hollow"] for j in sub]
            bb = [j["screen_broad"] for j in sub]
            out_d[name] = {
                "n": len(sub), "reader_says_nothing": sum(aa), "screen_flags": sum(bb),
                "agreement_pct": round(100 * sum(1 for x, y in zip(aa, bb) if x == y) / len(sub), 2),
                "kappa": round(hollow.cohen_kappa(aa, bb), 4),
            }
    return out_d


# ---------------------------------------------------------------------------
# Quoted evidence — short values with their record URL
# ---------------------------------------------------------------------------

def quotes(measures: dict, cache: str, per: int = 4) -> list[dict]:
    rng = random.Random(SEED + 7)
    out = []
    for name in ("cma", "uk", "govdata"):
        m = measures.get(name)
        if not m or "_rows" not in m:
            continue
        recs = {r["id"]: r for r in load(cache, name)}
        held = [r for r in m["_rows"] if r["half"] == "held" and r["hollow_broad5"]]
        if not held:
            continue
        pick = rng.sample(sorted(held, key=lambda r: r["id"]), min(per, len(held)))
        for r in pick:
            txt = hollow.norm(recs[r["id"]]["text"])
            out.append({
                "catalogue": name, "title": r["title"][:120],
                "value": txt[:180] + ("…" if len(txt) > 180 else ""),
                "chars": len(txt), "url": r["url"],
                "rules": [k for k in ("r1_chrome", "r2_truncated_tail", "r3_truncated_head",
                                      "r4_duplicate", "r5_title_echo") if r[k]],
            })
    return out


# ---------------------------------------------------------------------------
# The seven predictions of PREREGISTRATION.md §5, evaluated mechanically.
# Each returns per-arm detail and a single verdict string, so that check.py can
# recompute every verdict from the same numbers without reading this function.
# ---------------------------------------------------------------------------

SCORED = ("cma", "uk", "govdata")


def evaluate_predictions(m: dict, audit: dict | None) -> dict:
    p = {}

    # P1 — completeness >= 95 % and broad flag rate >= 5 %, in each scored catalogue
    arms = {}
    for c in SCORED:
        d = m.get(c, {})
        comp = d.get("declared_completeness_pct")
        flag = d.get("held", {}).get("hollow_broad", {}).get("pct")
        arms[c] = {"completeness_pct": comp, "held_broad_pct": flag,
                   "pass": bool(comp is not None and flag is not None
                                and comp >= 95.0 and flag >= 5.0)}
    p["P1"] = {"statement": "declared completeness >= 95 % and broad flag rate >= 5 % on the "
                            "held-out half, in each of C1-C3",
               "arms": arms,
               "verdict": "confirmed" if all(a["pass"] for a in arms.values()) else "refuted"}

    # P2 — association survives BH at q=0.05 AND top-stratum concentration ratio >= 2
    arms = {}
    for c in SCORED:
        d = m.get(c, {})
        a = d.get("association")
        conc = d.get("concentration")
        if not a or not conc:
            arms[c] = {"pass": False, "reason": "no association test (kill condition)"}
            continue
        arms[c] = {"p_perm": a["p_perm"], "bh_survivor": a.get("bh_survivor"),
                   "ratio": conc["ratio"], "top_stratum": conc["top_stratum"],
                   "flag_share_pct": conc["flag_share_pct"],
                   "record_share_pct": conc["record_share_pct"],
                   "pass": bool(a.get("bh_survivor") and conc["ratio"] is not None
                                and conc["ratio"] >= 2.0)}
    p["P2"] = {"statement": "hollowness concentrates by provenance stratum: BH survivor at "
                            "q = 0.05 and top-stratum flag share at least 2x its record share",
               "arms": arms,
               "verdict": "confirmed" if all(a["pass"] for a in arms.values())
               else ("refuted" if not any(a["pass"] for a in arms.values()) else "split")}

    # P3 — broad == R2 on >= 95 % of held-out values
    arms = {c: {"pct": m.get(c, {}).get("p3_broad_is_r2", {}).get("pct"),
                "pass": bool((m.get(c, {}).get("p3_broad_is_r2", {}).get("pct") or 0) >= 95.0)}
            for c in SCORED}
    p["P3"] = {"statement": "the broad aggregate and R2 alone agree on at least 95 % of held-out "
                            "values in each scored catalogue",
               "arms": arms,
               "verdict": "confirmed" if all(a["pass"] for a in arms.values())
               else ("refuted" if not any(a["pass"] for a in arms.values()) else "split")}

    # P4 — blind audit: agreement >= 75 % and kappa >= 0.42
    if audit:
        ok = bool(audit["agreement_pct"] is not None and audit["kappa"] is not None
                  and audit["agreement_pct"] >= 75.0 and audit["kappa"] >= 0.42)
        p["P4"] = {"statement": "against a blind reader on 60 held-out values: agreement >= 75 % "
                                "and Cohen's kappa >= 0.42",
                   "agreement_pct": audit["agreement_pct"], "kappa": audit["kappa"],
                   "verdict": "confirmed" if ok else "refuted"}
    else:
        p["P4"] = {"statement": "against a blind reader on 60 held-out values", "verdict": "pending"}

    # P5 — R3's opener limb: < 1 % on German, >= 1 % on English
    de = m.get("govdata", {}).get("held", {}).get("r3_opener", {}).get("pct")
    en = m.get("uk", {}).get("held", {}).get("r3_opener", {}).get("pct")
    p["P5"] = {"statement": "R3's English opener limb fires on under 1 % of German held-out values "
                            "and on 1 % or more of English ones",
               "govdata_pct": de, "uk_pct": en,
               "verdict": "confirmed" if (de is not None and en is not None and de < 1.0 and en >= 1.0)
               else "refuted"}

    # P6 — R5 fires on >= 1 % somewhere AND adds >= 20 held-out values beyond the frozen four
    arms = {c: {"pct": m.get(c, {}).get("held", {}).get("r5_title_echo", {}).get("pct"),
                "r5_only": m.get(c, {}).get("p6_r5_increment", {}).get("r5_only")}
            for c in SCORED}
    hit = any((a["pct"] or 0) >= 1.0 and (a["r5_only"] or 0) >= 20 for a in arms.values())
    p["P6"] = {"statement": "R5 fires on at least 1 % of held-out values in at least one catalogue "
                            "and flags at least 20 values no frozen rule flags",
               "arms": arms, "verdict": "confirmed" if hit else "refuted"}

    # P7 — the home arm reproduces 2026-09-08 exactly
    atlas = m.get("atlas", {})
    got = {"entries": atlas.get("present"), "records": atlas.get("records"),
           "all_broad_pct": atlas.get("all", {}).get("hollow_broad", {}).get("pct"),
           "held_broad_pct": atlas.get("held", {}).get("hollow_broad", {}).get("pct"),
           "r4_held_k": atlas.get("held", {}).get("r4_duplicate", {}).get("k"),
           "broad_is_r2_held_agree": atlas.get("p3_broad_is_r2", {}).get("agree"),
           "held_n": atlas.get("split", {}).get("held")}
    want = {"records": 521, "all_broad_pct": 40.5, "held_broad_pct": 44.05, "r4_held_k": 0,
            "broad_is_r2_held_agree": 249, "held_n": 252}
    p["P7"] = {"statement": "the home arm reproduces the published figures of 2026-09-08",
               "published_2026_09_08": want, "measured_today": got,
               "verdict": "confirmed" if all(got.get(k) == v for k, v in want.items()) else "refuted"}
    p["K4_fired"] = p["P7"]["verdict"] != "confirmed"
    return p


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True)
    ap.add_argument("--out", default="artifacts/cycle-003/2026-09-11-does-it-travel/data")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    manifest = json.load(open(os.path.join(args.cache, "manifest.json"), encoding="utf-8"))

    measures = {}
    for name in ("atlas", "cma", "uk", "govdata", "aic"):
        if not manifest.get(name, {}).get("ok"):
            measures[name] = {"catalogue": name, "unreachable": manifest.get(name, {}).get("error")}
            continue
        recs = load(args.cache, name)
        measures[name] = measure(name, recs, atlas_provenance=(name == "atlas"))
        # K5 — census completeness
        api_total = manifest[name].get("api_total")
        got = manifest[name].get("harvested")
        if name != "aic" and api_total:
            frac = got / api_total
            measures[name]["k5_fired"] = frac < 0.95
            measures[name]["harvest_fraction"] = round(frac, 4)

    # Exploratory, declared as such on the page: Cleveland carries a second descriptive field.
    if "_rows" in measures.get("cma", {}):
        cma_raw = load(args.cache, "cma")
        measures["cma"]["exploratory_second_field"] = {
            "field": "did_you_know",
            "records_with_it": sum(1 for r in cma_raw if r.get("has_didyouknow")),
            "records": len(cma_raw),
            "records_with_neither": sum(1 for r in cma_raw
                                        if not r.get("has_didyouknow")
                                        and not hollow.norm(r.get("text", ""))),
        }

    # C4: the fill rates that are the whole point of including it
    if "unreachable" not in measures["aic"]:
        aic = load(args.cache, "aic")
        measures["aic"]["fill_rates"] = {
            f: {"filled": sum(1 for r in aic if hollow.norm(r.get(f, ""))), "of": len(aic)}
            for f in ("text", "short_description", "provenance_text", "credit_line")
        }

    build_audit_sheet(measures, args.cache, args.out)
    audit = join_audit(measures, args.out)

    # BH across the three primary association tests
    fam = [(n, measures[n]["association"]["p_perm"]) for n in ("cma", "uk", "govdata")
           if "association" in measures.get(n, {})]
    if fam:
        keep = hollow.benjamini_hochberg([p for _, p in fam], 0.05)
        for (n, _), k in zip(fam, keep):
            measures[n]["association"]["bh_survivor"] = bool(k)

    predictions = evaluate_predictions(measures, audit)

    out = {
        "generated_by": "tools/travel/travel.py",
        "predictions": predictions,
        "date": "2026-09-11", "session": 157, "cycle": 3, "question": "Missing Data Art",
        "preregistration": "artifacts/cycle-003/2026-09-11-does-it-travel/PREREGISTRATION.md",
        "manifest": manifest,
        "catalogues": {k: {kk: vv for kk, vv in v.items() if kk != "_rows"}
                       for k, v in measures.items()},
        "audit": audit,
        "quotes": quotes(measures, args.cache),
        "params": {"seed": SEED, "perm_reps": PERM_REPS, "min_stratum": MIN_STRATUM,
                   "audit_per_catalogue": AUDIT_PER_CATALOGUE},
    }
    with open(os.path.join(args.out, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    print(json.dumps({k: {kk: v.get(kk) for kk in
                          ("records", "present", "declared_completeness_pct", "k1_fired")}
                      for k, v in out["catalogues"].items()}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
