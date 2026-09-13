#!/usr/bin/env python3
"""Room — does "identifying power depends on the room" hold on a corpus we did not build?

Session 159, cycle 003, question "Missing Data Art". Governed by
presentations/cycle-003/PREREGISTRATION.md §3, committed before this file fetched anything.

On 2026-09-12 this practice measured, on data.gov.uk alone, that the share of descriptions failing
to pick out their own record rises from 16.51 % at 521 records to 62.17 % at 67,205 with nothing
about the descriptions changed. One corpus. This file runs the identical ladder on govdata.de — a
CKAN portal this house did not build, in a different language, about twice the size.

Nothing here is re-tuned. Both instruments are IMPORTED, not copied:

  * tools/identify/identify.py — the model-free narrowing instrument, frozen 2026-09-12
    (COMMON_DF_FRACTION = 0.10, N_RAREST = 3, the same tokeniser, the same title-masking step);
  * tools/hollow/hollow.py     — the hollowness screen's rules R1-R4, frozen 2026-09-08.

If these instruments are wrong for German text, they are wrong here in exactly the way they were
wrong at home. That is the point of importing rather than copying.

No model is called anywhere in this file. Standard library only. Every draw is seeded. No
third-party corpus is written into this repository (protocol §7): the harvest goes to --cache,
outside the working tree, and only aggregates are committed.

Usage:
    python3 tools/room/room.py --fetch --cache /path/to/cache
    python3 tools/room/room.py --cache /path/to/cache        # measure from an existing cache
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import statistics
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "identify"))
sys.path.insert(0, os.path.join(HERE, "..", "hollow"))

import hollow  # noqa: E402
import identify  # noqa: E402

OUT = "presentations/cycle-003/data"

UA = "field-research/room (Meridian; research; contact via frankbueltge.de)"
ENDPOINT = "https://www.govdata.de/ckan/api/3/action/package_search"
FIELD = "notes"

# Fixed by the pre-registration. Not tuned after a number was seen.
SEED = 20260913
LADDER = [521, 1000, 2000, 4000, 8000, 16000, 32000, 64000]
REPEATS = 5

# Reference values, quoted from the artifact that made them. Used for ratios on the page, never
# as a bar unless a prediction in the pre-registration says so.
UK_NOT_UNIQUE_521 = 16.51
UK_NOT_UNIQUE_FULL = 62.17
UK_RATIO = 3.77
UK_R4_RATIO = 6.39
ATLAS_NOT_UNIQUE_521 = 0.96

# Observed before the pre-registration was written, and declared there (§0.2).
PROBE_COUNT_2026_09_13 = 156003
CENSUS_COUNT_2026_09_11 = 146492


def get(url: str, timeout: int = 120, tries: int = 4) -> bytes:
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except Exception as exc:  # noqa: BLE001 - a shut door is a fact about the session
            last = exc
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"{url}: {last}")


def harvest(cache: str) -> dict:
    """Census of govdata.de. K3 of the pre-registration: a refusal is reported, not worked around."""
    t0 = time.time()
    try:
        first = json.loads(get(f"{ENDPOINT}?rows=0"))
    except RuntimeError as exc:
        return {"ok": False, "error": str(exc)[:400], "endpoint": ENDPOINT,
                "fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    total = int(first["result"]["count"])
    path = os.path.join(cache, "govdata.jsonl")
    kept, pages, start = 0, 0, 0
    digest = hashlib.sha256()
    with open(path, "w", encoding="utf-8") as fh:
        while start < total:
            try:
                raw = get(f"{ENDPOINT}?rows=1000&start={start}")
            except RuntimeError as exc:
                print(f"  govdata: stopped at {start}: {exc}", file=sys.stderr)
                break
            digest.update(raw)
            rows = json.loads(raw)["result"]["results"]
            if not rows:
                break
            for r in rows:
                org = r.get("organization") or {}
                fh.write(json.dumps({
                    "id": identify.s(r.get("id")),
                    "title": identify.s(r.get("title")),
                    "text": identify.s(r.get(FIELD)),
                    "stratum": identify.s(org.get("title") or org.get("name")),
                }, ensure_ascii=False) + "\n")
                kept += 1
            pages += 1
            start += len(rows)
            if pages % 10 == 0:
                print(f"  govdata {kept}/{total}", file=sys.stderr)
            time.sleep(0.3)
    return {"ok": True, "catalogue": "govdata", "api_total": total, "harvested": kept,
            "pages": pages, "endpoint": ENDPOINT, "field": FIELD,
            "stratum_field": "organization", "pages_sha256": digest.hexdigest(),
            "seconds": round(time.time() - t0, 1),
            "fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}


def load(cache: str) -> list[dict]:
    rows = []
    with open(os.path.join(cache, "govdata.jsonl"), encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def prepare(rows: list[dict]) -> tuple[list[dict], dict]:
    """Mask each value with its own title and pre-compute the three single-value rules.

    R1-R3 are properties of one string and are computed once. R4 is a relation to the catalogue and
    must be recomputed inside every subsample — which is the whole question.
    """
    present = [r for r in rows if (r.get("text") or "").strip()]
    prepared = []
    for r in present:
        text = r["text"]
        m = identify.mask(text, r.get("title") or "")
        prepared.append({
            "text": text,
            "masked": m,
            "masked_tokens": len(identify.tokens(m)),
            "r1": bool(hollow.r1_chrome(text)),
            "r2": bool(hollow.r2_truncated_tail(text)),
            "r3": bool(hollow.r3_truncated_head(text)),
        })
    stats = {
        "records": len(rows),
        "present": len(present),
        "declared_completeness_pct": round(100.0 * len(present) / len(rows), 2) if rows else 0.0,
        "mean_masked_tokens": round(
            statistics.fmean(p["masked_tokens"] for p in prepared), 2) if prepared else 0.0,
        "under_3_masked_tokens": sum(1 for p in prepared if p["masked_tokens"] < 3),
    }
    stats["under_3_masked_tokens_pct"] = round(
        100.0 * stats["under_3_masked_tokens"] / len(prepared), 2) if prepared else 0.0
    return prepared, stats


def rung(sub: list[dict]) -> dict:
    """Every rate on one rung, all instruments recomputed INSIDE the subsample."""
    n = len(sub)
    narrow = identify.narrowing([p["masked"] for p in sub])
    not_unique = sum(1 for x in narrow if not x["identifies_uniquely"])
    nothing = sum(1 for x in narrow if x["identifies_nothing"])
    dupes = hollow.duplicate_keys([p["text"] for p in sub])
    r4 = sum(1 for p in sub if hollow.norm(p["text"]).casefold() in dupes)
    broad = sum(1 for p in sub
                if p["r1"] or p["r2"] or p["r3"] or hollow.norm(p["text"]).casefold() in dupes)
    return {
        "not_unique_pct": round(100.0 * not_unique / n, 2),
        "identifies_nothing_pct": round(100.0 * nothing / n, 2),
        "r1_chrome_pct": round(100.0 * sum(1 for p in sub if p["r1"]) / n, 3),
        "r2_truncated_tail_pct": round(100.0 * sum(1 for p in sub if p["r2"]) / n, 3),
        "r3_truncated_head_pct": round(100.0 * sum(1 for p in sub if p["r3"]) / n, 3),
        "r4_duplicate_pct": round(100.0 * r4 / n, 2),
        "hollow_broad_pct": round(100.0 * broad / n, 2),
    }


def ladder(prepared: list[dict]) -> list[dict]:
    rng = random.Random(SEED)
    n_full = len(prepared)
    out = []
    for size in LADDER + [n_full]:
        if size > n_full:
            continue
        reps = 1 if size == n_full else REPEATS
        runs = []
        for i in range(reps):
            sub = prepared if size == n_full else rng.sample(prepared, size)
            runs.append(rung(sub))
            print(f"  rung n={size} rep {i + 1}/{reps}", file=sys.stderr)
        agg = {"n": size, "repeats": reps}
        for k in runs[0]:
            vals = [r[k] for r in runs]
            agg[k] = round(statistics.fmean(vals), 2 if "pct" in k else 3)
            agg[k + "_sd"] = round(statistics.stdev(vals), 3) if reps > 1 else None
        out.append(agg)
    return out


def score(rungs: list[dict], stats: dict, man: dict) -> dict:
    """The six pre-registered predictions, and the four kill conditions."""
    by_n = {r["n"]: r for r in rungs}
    bottom = by_n.get(521)
    top = rungs[-1] if rungs else None
    k = {}

    k["K1"] = {"condition": "notes non-empty on < 80 % of harvested records",
               "value_pct": stats["declared_completeness_pct"],
               "fired": stats["declared_completeness_pct"] < 80.0}
    harvested_share = (100.0 * man.get("harvested", 0) / man["api_total"]) if man.get("api_total") else 0.0
    k["K2"] = {"condition": "fewer than 90 % of the API's reported count harvested",
               "value_pct": round(harvested_share, 2), "fired": harvested_share < 90.0}
    k["K3"] = {"condition": "the endpoint refuses past the retry budget",
               "fired": not man.get("ok", False)}
    k["K4"] = {"condition": ">= 25 % of masked values retain fewer than 3 tokens",
               "value_pct": stats["under_3_masked_tokens_pct"],
               "fired": stats["under_3_masked_tokens_pct"] >= 25.0}

    scored = not (k["K1"]["fired"] or k["K3"]["fired"] or k["K4"]["fired"])
    p = {}
    if not rungs:
        return {"kill_conditions": k, "predictions": {}, "scored": False}

    # P1 - monotone rise
    worst_drop, worst_at = 0.0, None
    for a, b in zip(rungs, rungs[1:]):
        drop = a["not_unique_pct"] - b["not_unique_pct"]
        if drop > worst_drop:
            worst_drop, worst_at = drop, (a["n"], b["n"])
    p["P1"] = {"statement": "not_unique_pct is monotonically non-decreasing; refuted by any drop > 1.0 point",
               "largest_drop_points": round(worst_drop, 2), "between": worst_at,
               "verdict": "confirmed" if worst_drop <= 1.0 else "refuted"}

    # P2 - at the atlas's own size, govdata still fails far more often
    p["P2"] = {"statement": "at n = 521 the govdata rate is at least 5 points above the atlas's 0.96 %",
               "value_pct": bottom["not_unique_pct"] if bottom else None,
               "atlas_pct": ATLAS_NOT_UNIQUE_521,
               "gap_points": round(bottom["not_unique_pct"] - ATLAS_NOT_UNIQUE_521, 2) if bottom else None,
               "verdict": ("confirmed" if bottom and bottom["not_unique_pct"] - ATLAS_NOT_UNIQUE_521 >= 5.0
                           else "refuted")}

    ratio = round(top["not_unique_pct"] / bottom["not_unique_pct"], 2) if bottom and bottom["not_unique_pct"] else None
    p["P3"] = {"statement": "the full/521 narrowing ratio is within a factor of 2 of data.gov.uk's 3.77",
               "ratio": ratio, "uk_ratio": UK_RATIO, "band": [1.88, 7.54],
               "verdict": ("confirmed" if ratio is not None and 1.88 <= ratio <= 7.54 else "refuted")}

    r4_ratio = round(top["r4_duplicate_pct"] / bottom["r4_duplicate_pct"], 2) if bottom and bottom["r4_duplicate_pct"] else None
    p["P4"] = {"statement": "R4's full/521 ratio is above 2.0",
               "ratio": r4_ratio, "r4_at_521": bottom["r4_duplicate_pct"] if bottom else None,
               "r4_at_full": top["r4_duplicate_pct"],
               "verdict": ("confirmed" if r4_ratio is not None and r4_ratio > 2.0 else "refuted")}

    p["P5"] = {"statement": "R4's ratio exceeds the narrowing instrument's ratio, as on data.gov.uk (6.39 > 3.77)",
               "r4_ratio": r4_ratio, "narrowing_ratio": ratio,
               "verdict": ("confirmed" if (r4_ratio is not None and ratio is not None and r4_ratio > ratio)
                           else "refuted")}

    moves = {}
    for key in ("r1_chrome_pct", "r2_truncated_tail_pct", "r3_truncated_head_pct"):
        moves[key] = round(abs(top[key] - rungs[0][key]), 3)
    p["P6"] = {"statement": "R1-R3 are properties of one value and cannot move with catalogue size; "
                            "refuted by any move > 0.05 points (a control on our own code)",
               "moves_points": moves, "largest": max(moves.values()),
               "verdict": "confirmed" if max(moves.values()) <= 0.05 else "refuted"}

    if not scored:
        for v in p.values():
            v["verdict"] = "not scored (kill condition fired)"

    tally = {"total": len(p),
             "confirmed": sum(1 for v in p.values() if v["verdict"] == "confirmed"),
             "refuted": sum(1 for v in p.values() if v["verdict"] == "refuted")}
    return {"kill_conditions": k, "predictions": p, "_tally": tally, "scored": scored}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True)
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--out", default=OUT)
    args = ap.parse_args()
    os.makedirs(args.cache, exist_ok=True)
    os.makedirs(args.out, exist_ok=True)

    man_path = os.path.join(args.cache, "govdata-manifest.json")
    if args.fetch:
        man = harvest(args.cache)
        with open(man_path, "w", encoding="utf-8") as fh:
            json.dump(man, fh, indent=1)
    else:
        with open(man_path, encoding="utf-8") as fh:
            man = json.load(fh)

    out = {
        "_status": "PRE-REGISTERED. presentations/cycle-003/PREREGISTRATION.md §3, committed "
                   "before this file fetched anything. Instruments imported unchanged from "
                   "tools/identify/identify.py (frozen 2026-09-12) and tools/hollow/hollow.py "
                   "(frozen 2026-09-08). No model is called. Standard library only.",
        "generated_by": "tools/room/room.py",
        "date": "2026-09-13",
        "session": 159,
        "cycle": 3,
        "question": "Missing Data Art",
        "params": {"seed": SEED, "ladder": LADDER, "repeats_per_size": REPEATS,
                   "common_df_fraction": identify.COMMON_DF_FRACTION,
                   "n_rarest": identify.N_RAREST},
        "reference": {
            "_note": "Quoted from artifacts/cycle-003/2026-09-12-what-a-description-is-for/"
                     "data/size-curve.json and .../results.json. Not re-measured here.",
            "uk_not_unique_pct_at_521": UK_NOT_UNIQUE_521,
            "uk_not_unique_pct_at_full": UK_NOT_UNIQUE_FULL,
            "uk_narrowing_ratio": UK_RATIO,
            "uk_r4_ratio": UK_R4_RATIO,
            "atlas_not_unique_pct_at_521": ATLAS_NOT_UNIQUE_521,
        },
        "growth": {
            "_note": "Observed by a one-request probe BEFORE the pre-registration was written and "
                     "declared there (§0.2). An observation, never a prediction.",
            "count_2026_09_11": CENSUS_COUNT_2026_09_11,
            "count_probe_2026_09_13": PROBE_COUNT_2026_09_13,
            "delta": PROBE_COUNT_2026_09_13 - CENSUS_COUNT_2026_09_11,
        },
        "manifest": man,
    }

    if not man.get("ok"):
        out["ladder"] = []
        out["population"] = {}
        out.update(score([], {"declared_completeness_pct": 0.0, "under_3_masked_tokens_pct": 0.0}, man))
        with open(os.path.join(args.out, "room-ladder.json"), "w", encoding="utf-8") as fh:
            json.dump(out, fh, indent=1, ensure_ascii=False)
        print("endpoint refused; K3 fired; nothing measured", file=sys.stderr)
        return 0

    rows = load(args.cache)
    prepared, stats = prepare(rows)
    out["population"] = stats
    rungs = ladder(prepared) if stats["declared_completeness_pct"] >= 80.0 else []
    out["ladder"] = rungs
    out.update(score(rungs, stats, man))

    with open(os.path.join(args.out, "room-ladder.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print(json.dumps(out.get("_tally", {}), indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
