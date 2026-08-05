#!/usr/bin/env python3
"""score.py — the metrics RULE.md §6 fixed, the peek check §7 fixed, and the band §8 fixed.

Nothing here is chosen after the readers ran. Every threshold, every pairing and every
band condition is transcribed from RULE.md, which is committed strictly before either
reader's file exists (`git log --diff-filter=A -- RULE.md reader-R1.json`).

One thing RULE.md did NOT fix, and this script therefore refuses to decide: whether a
reader's UNDECIDABLE case sits inside or outside that reader's population when the
in-population tables are recomputed. Both are computed and both are reported. Logged in
DEVIATIONS.md as a gap in the pre-registration, resolved the only way a gap found after
the fact honestly can be — by reporting every branch rather than picking one.

Offline, stdlib only, deterministic.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
WORK = ROOT / "works" / "2026-08-03-where-the-reader-declines" / "data.json"

RELATIONS = ("supports", "contradicts", "qualifies", "contextualizes", "undecidable")

# RULE.md §7
PEEK_CASE_MAX = 0.60
PEEK_MEAN_MAX = 0.35

# RULE.md §8
BAND_B_RATIO = 1.5
BAND_C_N_DELTA = 5

STOP = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from", "in", "into",
    "is", "it", "its", "no", "not", "of", "on", "or", "so", "than", "that", "the", "their",
    "them", "there", "these", "this", "to", "was", "were", "which", "with", "without",
}


def words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", (text or "").lower()) if w not in STOP and len(w) > 2}


# --------------------------------------------------------------------------- load

def load() -> tuple[dict, dict, dict]:
    cases = {c["case_id"]: c for c in json.loads(WORK.read_text())["cases"]}
    readers = {}
    for name in ("R1", "R2"):
        raw = json.loads((HERE / f"reader-{name}.json").read_text())
        readers[name] = {c["case_id"]: c for c in raw["cases"]}
    return cases, readers["R1"], readers["R2"]


def validate(cases: dict, reader: dict, name: str) -> list[str]:
    """Every way this reader's file is unusable. Not the first — all of them."""
    out: list[str] = []
    if len(reader) != 60:
        out.append(f"{name}: {len(reader)} cases, expected 60")
    missing = set(cases) - set(reader)
    extra = set(reader) - set(cases)
    if missing:
        out.append(f"{name}: {len(missing)} case_ids missing, e.g. {sorted(missing)[:3]}")
    if extra:
        out.append(f"{name}: {len(extra)} unknown case_ids, e.g. {sorted(extra)[:3]}")
    for cid, r in reader.items():
        if r.get("verdict") not in ("IN", "OUT", "UNDECIDABLE"):
            out.append(f"{name}/{cid}: verdict {r.get('verdict')!r}")
        src = cid in cases and (cases[cid]["title"] + "\n" + cases[cid]["excerpt"])
        q = (r.get("deciding_quote") or "").strip()
        if src and q and q not in src:
            out.append(f"{name}/{cid}: deciding_quote not verbatim in title+excerpt: {q[:60]!r}")
        if not (r.get("reason") or "").strip():
            out.append(f"{name}/{cid}: empty reason")
    return out


# ------------------------------------------------------------------- §7 peek check

def peek(cases: dict, reader: dict, name: str) -> dict:
    """Overlap on words the reader could only have got from the original's own text.

    Words present in the case's title or excerpt are removed from both sides first: both
    readers are quoting the same source, so shared source vocabulary is innocent and must
    not be allowed to look like contamination. What remains on the original's side is its
    own wording. Jaccard on that residue.
    """
    per: list[tuple[str, float]] = []
    for cid, c in cases.items():
        src = words(c["title"]) | words(c["excerpt"])
        orig = words(c.get("population_reason") or c.get("exclusion_reason") or "") - src
        mine = words(reader.get(cid, {}).get("reason", "")) - src
        union = orig | mine
        per.append((cid, len(orig & mine) / len(union) if union else 0.0))
    per.sort(key=lambda t: -t[1])
    mean = sum(v for _, v in per) / len(per) if per else 0.0
    return {
        "reader": name,
        "mean": round(mean, 4),
        "max_case": per[0][0] if per else None,
        "max": round(per[0][1], 4) if per else 0.0,
        "top5": [(cid, round(v, 4)) for cid, v in per[:5]],
        "compromised": bool(per and (per[0][1] >= PEEK_CASE_MAX or mean > PEEK_MEAN_MAX)),
    }


# ---------------------------------------------------------------------- §6 metrics

def binary(v) -> bool | None:
    if v is True or v == "IN":
        return True
    if v is False or v == "OUT":
        return False
    return None


def kappa(pairs: list[tuple[bool, bool]]) -> float | None:
    n = len(pairs)
    if not n:
        return None
    po = sum(1 for a, b in pairs if a == b) / n
    pa = sum(a for a, b in pairs) / n
    pb = sum(b for a, b in pairs) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return None if pe == 1 else round((po - pe) / (1 - pe), 4)


def compare(cases: dict, left: dict, right: dict, lname: str, rname: str) -> dict:
    """left/right map case_id -> IN|OUT|UNDECIDABLE. UNDECIDABLE disagrees with any binary."""
    agree = und = 0
    both: list[tuple[bool, bool]] = []
    moved_in_out = moved_out_in = 0
    disputes: list[dict] = []
    for cid in cases:
        lv, rv = left[cid], right[cid]
        lb, rb = binary(lv), binary(rv)
        if lv == rv:
            agree += 1
        if lb is None or rb is None:
            und += 1
        else:
            both.append((lb, rb))
            if lb and not rb:
                moved_in_out += 1
            elif rb and not lb:
                moved_out_in += 1
        if lv != rv:
            disputes.append({"case_id": cid, lname: lv, rname: rv})
    return {
        "pairing": f"{lname} x {rname}",
        "n": len(cases),
        "agree": agree,
        "agreement_pct": round(100 * agree / len(cases), 1),
        "undecidable_involved": und,
        "kappa_on_binary": kappa(both),
        "kappa_n": len(both),
        f"{lname}_IN_to_{rname}_OUT": moved_in_out,
        f"{lname}_OUT_to_{rname}_IN": moved_out_in,
        "disputes": disputes,
    }


# ----------------------------------------------------------- recomputed in-pop tables

def table(cases: dict, member: set[str]) -> dict:
    sel = [cases[c] for c in cases if c in member]
    def dist(key):
        c = Counter((x[key]["relation"] or "undecidable") for x in sel)
        return {r: c.get(r, 0) for r in RELATIONS}
    g, m = dist("gold"), dist("machine")
    n = len(sel)
    ratio = (m["contextualizes"] / g["contextualizes"]) if g["contextualizes"] else None
    return {
        "n": n,
        "gold": g,
        "machine": m,
        "machine_contextualizes_pct": round(100 * m["contextualizes"] / n, 1) if n else None,
        "gold_contextualizes_pct": round(100 * g["contextualizes"] / n, 1) if n else None,
        "ratio_machine_over_gold_contextualizes": round(ratio, 3) if ratio else None,
    }


def membership(reader: dict, undecidable_in: bool) -> set[str]:
    return {c for c, r in reader.items()
            if r == "IN" or (undecidable_in and r == "UNDECIDABLE")}


def band(cases: dict, orig: dict, splits: dict) -> dict:
    """RULE.md §8, evaluated mechanically. splits: label -> set of in-population case_ids."""
    supports_case = next(
        (c for c, x in cases.items()
         if x["in_population"] and x["gold"]["relation"] == "supports"), None)
    orig_member = {c for c, v in orig.items() if v == "IN"}
    reasons: list[str] = []
    band_b_ok = True
    for label, member in splits.items():
        t = table(cases, member)
        ratio = t["ratio_machine_over_gold_contextualizes"]
        m_und = t["machine"]["undecidable"]
        g_und = t["gold"]["undecidable"]
        if ratio is None or ratio < BAND_B_RATIO:
            band_b_ok = False
            reasons.append(f"{label}: contextualizes ratio {ratio} < {BAND_B_RATIO}")
        if not (m_und == 0 and g_und >= 1):
            band_b_ok = False
            reasons.append(f"{label}: machine undecidable {m_und}, blind reader {g_und}")
        if abs(t["n"] - len(orig_member)) > BAND_C_N_DELTA:
            reasons.append(f"{label}: n {t['n']} vs {len(orig_member)}, moves by more than {BAND_C_N_DELTA}")
        if supports_case and supports_case not in member:
            reasons.append(f"{label}: the single `supports` case {supports_case} leaves the population")
    exact = all(member == orig_member for member in splits.values())
    if exact:
        return {"band": "A", "reasons": ["both readers reproduce the original split exactly"]}
    band_c = [r for r in reasons if "moves by more than" in r or "leaves the population" in r]
    if not band_b_ok or band_c:
        return {"band": "C", "reasons": reasons}
    return {"band": "B", "reasons": reasons or ["disagreement present; headline conditions hold"]}


# ------------------------------------------------------------------------------ main

def main() -> None:
    cases, r1, r2 = load()
    errors = validate(cases, r1, "R1") + validate(cases, r2, "R2")

    orig = {c: ("IN" if cases[c]["in_population"] else "OUT") for c in cases}
    v1 = {c: r1[c]["verdict"] for c in cases}
    v2 = {c: r2[c]["verdict"] for c in cases}

    peeks = [peek(cases, r1, "R1"), peek(cases, r2, "R2")]

    splits_excl = {"R1": membership(v1, False), "R2": membership(v2, False)}
    splits_incl = {"R1": membership(v1, True), "R2": membership(v2, True)}

    out = {
        "_note": (
            "Every metric and threshold below is transcribed from RULE.md, committed before "
            "either reader ran. Produced by scripts/score.py; offline and deterministic."
        ),
        "validation_errors": errors,
        "counts": {
            "original": dict(Counter(orig.values())),
            "R1": dict(Counter(v1.values())),
            "R2": dict(Counter(v2.values())),
        },
        "peek_check": peeks,
        "pairings": [
            compare(cases, orig, v1, "original", "R1"),
            compare(cases, orig, v2, "original", "R2"),
            compare(cases, v1, v2, "R1", "R2"),
        ],
        "tables": {
            "as_published_original_split": table(cases, {c for c in cases if cases[c]["in_population"]}),
            "undecidable_outside_population": {k: table(cases, v) for k, v in splits_excl.items()},
            "undecidable_inside_population": {k: table(cases, v) for k, v in splits_incl.items()},
        },
        "band_undecidable_outside": band(cases, orig, splits_excl),
        "band_undecidable_inside": band(cases, orig, splits_incl),
    }
    (HERE / "results.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")

    print("validation errors:", len(errors))
    for e in errors[:10]:
        print("  ", e)
    for p in peeks:
        print(f"peek {p['reader']}: mean {p['mean']} max {p['max']} ({p['max_case']}) "
              f"compromised={p['compromised']}")
    for p in out["pairings"]:
        print(f"{p['pairing']}: agree {p['agree']}/60 = {p['agreement_pct']}%  "
              f"kappa {p['kappa_on_binary']} (n={p['kappa_n']})")
    print("n as published:", out["tables"]["as_published_original_split"]["n"])
    for k, v in out["tables"]["undecidable_outside_population"].items():
        print(f"  {k} n={v['n']} machine ctx {v['machine']['contextualizes']} "
              f"({v['machine_contextualizes_pct']}%) ratio {v['ratio_machine_over_gold_contextualizes']}")
    print("BAND (undecidable outside):", out["band_undecidable_outside"]["band"])
    print("BAND (undecidable inside):", out["band_undecidable_inside"]["band"])


if __name__ == "__main__":
    main()
