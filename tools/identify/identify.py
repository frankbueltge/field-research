#!/usr/bin/env python3
"""Identify — does a description, stripped of its own title, pick its record out of its catalogue?

Session 158, cycle 003, question "Missing Data Art". Everything here is fixed by
artifacts/cycle-003/2026-09-12-what-a-description-is-for/PREREGISTRATION.md, committed before this
file fetched anything.

Two instruments:

  1. narrowing  — model-free, deterministic, census. How many records does a masked value narrow
                  its own catalogue to? (PREREGISTRATION §2.2)
  2. the sheet  — a 5-way identification task for a blind reader, sampled from the held-out half.
                  This file writes the sheet; it never writes a label. (§2.3)

The hollowness screen is IMPORTED from tools/hollow/hollow.py, rules untouched. R5 is re-declared
here exactly as tools/travel/travel.py declared it on 2026-09-11, with the same disclosure.

No model is called anywhere in this file. Standard library only. Every random draw is seeded.
No third-party corpus is written into the repository (protocol §7): the harvest goes to --cache.

Usage:
    python3 tools/identify/identify.py --fetch --cache /path/to/cache
    python3 tools/identify/identify.py --cache /path/to/cache          # measure from cache
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import re
import sys
import time
import unicodedata
import urllib.request
from collections import Counter, defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "hollow"))
import hollow  # noqa: E402

OUT = "artifacts/cycle-003/2026-09-12-what-a-description-is-for/data"

UA = "field-research/identify (Meridian; research; contact via frankbueltge.de)"

# --- Parameters, fixed by the pre-registration. Not tuned after a number was seen. -------------
SEED = 20260912
N_SAMPLE = 60
N_CANDIDATES = 5
COMMON_DF_FRACTION = 0.10   # §2.2 step 2
N_RAREST = 3                # §2.2 step 3
SHEET_CAP_CHARS = 1200      # §2.3
MASK = "▮"

TOKEN_RE = re.compile(r"[^\W_]{3,}", re.UNICODE)

ARMS = {
    "atlas": {
        "label": "Atlas of Data Art (home arm)",
        "endpoint": "https://frankbueltge.de/atlas/werke.json",
        "field": "decisive_move",
        "stratum_field": "venue_prize (provenance families, frozen 2026-09-08)",
    },
    "uk": {
        "label": "data.gov.uk",
        "endpoint": "https://ckan.publishing.service.gov.uk/api/3/action/package_search",
        "field": "notes",
        "stratum_field": "organization",
    },
}


# ---------------------------------------------------------------------------
# R5, re-declared byte-identically to tools/travel/travel.py (2026-09-11).
# Origin disclosed there and again in this session's pre-registration §1.3:
# it was suggested by a record inside the population and is NOT on the footing of R1-R4.
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


# ---------------------------------------------------------------------------
# Harvest
# ---------------------------------------------------------------------------

def get(url: str, timeout: int = 120, tries: int = 4) -> bytes:
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except Exception as exc:  # noqa: BLE001 - an unreachable feed is a fact about the session
            last = exc
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"{url}: {last}")


def s(v) -> str:
    return v if isinstance(v, str) else ("" if v is None else str(v))


def harvest_atlas(cache: str) -> dict:
    url = ARMS["atlas"]["endpoint"]
    t0 = time.time()
    raw = get(url)
    doc = json.loads(raw)
    rows = doc["entries"] if isinstance(doc, dict) and "entries" in doc else doc
    path = os.path.join(cache, "atlas.jsonl")
    with open(path, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps({
                "id": s(r.get("id") or r.get("slug") or r.get("title")),
                "title": s(r.get("title")),
                "text": s(r.get("decisive_move")),
                "stratum": hollow.provenance(s(r.get("venue_prize"))),
            }, ensure_ascii=False) + "\n")
    return {"catalogue": "atlas", "api_total": len(rows), "harvested": len(rows),
            "endpoint": url, "field": "decisive_move",
            "stratum_field": ARMS["atlas"]["stratum_field"],
            "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
            "seconds": round(time.time() - t0, 1),
            "fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "ok": True}


def harvest_uk(cache: str) -> dict:
    base = ARMS["uk"]["endpoint"]
    t0 = time.time()
    first = json.loads(get(f"{base}?rows=0"))
    total = int(first["result"]["count"])
    path = os.path.join(cache, "uk.jsonl")
    kept, pages, start = 0, 0, 0
    with open(path, "w", encoding="utf-8") as fh:
        while start < total:
            doc = json.loads(get(f"{base}?rows=1000&start={start}"))
            rows = doc["result"]["results"]
            if not rows:
                break
            for r in rows:
                org = r.get("organization") or {}
                fh.write(json.dumps({
                    "id": s(r.get("id")),
                    "title": s(r.get("title")),
                    "text": s(r.get("notes")),
                    "stratum": s(org.get("title") or org.get("name")),
                }, ensure_ascii=False) + "\n")
                kept += 1
            pages += 1
            start += len(rows)
            print(f"  uk {kept}/{total}", file=sys.stderr)
            time.sleep(0.3)
    return {"catalogue": "uk", "api_total": total, "harvested": kept, "pages": pages,
            "endpoint": base, "field": "notes", "stratum_field": "organization",
            "seconds": round(time.time() - t0, 1),
            "fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "ok": True}


def load(cache: str, name: str) -> list[dict]:
    with open(os.path.join(cache, name + ".jsonl"), encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


# ---------------------------------------------------------------------------
# Masking (PREREGISTRATION §2.1)
# ---------------------------------------------------------------------------

def nfkc(text: str) -> str:
    return unicodedata.normalize("NFKC", text or "")


def tokens(text: str) -> list[str]:
    return [m.group(0).casefold() for m in TOKEN_RE.finditer(nfkc(text))]


def mask(text: str, title: str) -> str:
    """Replace every whole token of the description that the title already contains."""
    title_set = set(tokens(title))
    if not title_set:
        return hollow.norm(nfkc(text))
    out = TOKEN_RE.sub(lambda m: MASK if m.group(0).casefold() in title_set else m.group(0),
                       nfkc(text))
    return hollow.norm(out)


# ---------------------------------------------------------------------------
# Instrument 1 — narrowing (PREREGISTRATION §2.2)
# ---------------------------------------------------------------------------

def narrowing(masked: list[str]) -> list[dict]:
    """For each masked value, how many records does it narrow the catalogue to?"""
    n = len(masked)
    toks = [set(tokens(m)) for m in masked]
    df = Counter()
    for ts in toks:
        df.update(ts)
    postings = defaultdict(set)
    for i, ts in enumerate(toks):
        for t in ts:
            postings[t].add(i)

    cutoff = COMMON_DF_FRACTION * n
    out = []
    for i, ts in enumerate(toks):
        usable = [t for t in ts if df[t] <= cutoff]
        if not usable:
            out.append({"narrowing_set_size": n, "identifies_nothing": True,
                        "identifies_uniquely": False, "keys": [], "usable_tokens": 0})
            continue
        # deterministic: rarest first, ties broken by the token's own sort order
        usable.sort(key=lambda t: (df[t], t))
        keys = usable[:N_RAREST]
        acc = set(postings[keys[0]])
        for k in keys[1:]:
            acc &= postings[k]
        out.append({"narrowing_set_size": len(acc), "identifies_nothing": False,
                    "identifies_uniquely": len(acc) == 1, "keys": keys,
                    "usable_tokens": len(usable)})
    return out


# ---------------------------------------------------------------------------
# Screen + build the per-record table
# ---------------------------------------------------------------------------

def build_arm(name: str, rows: list[dict]) -> dict:
    field = ARMS[name]["field"]
    present = [r for r in rows if hollow.norm(r["text"])]
    n_all, n_present = len(rows), len(present)

    dupes = hollow.duplicate_keys([r["text"] for r in present])
    recs = []
    for r in present:
        c = hollow.classify(r["text"], dupes)
        m = mask(r["text"], r["title"])
        recs.append({
            "id": r["id"], "title": r["title"], "text": r["text"], "masked": m,
            "stratum": r["stratum"] or "(none)",
            "half": hollow.half({"title": r["title"]}),
            "masked_token_count": len(tokens(m)),
            "r1_chrome": c["r1_chrome"], "r2_truncated_tail": c["r2_truncated_tail"],
            "r3_truncated_head": c["r3_truncated_head"], "r4_duplicate": c["r4_duplicate"],
            "r5_title_echo": r5_title_echo(r["text"], r["title"]),
            "hollow_strict": c["hollow_strict"], "hollow_broad": c["hollow_broad"],
        })
    for rec, nr in zip(recs, narrowing([x["masked"] for x in recs])):
        rec.update(nr)

    def pct(k, d):
        return round(100.0 * k / d, 2) if d else None

    not_unique = sum(1 for r in recs if not r["identifies_uniquely"])
    nothing = sum(1 for r in recs if r["identifies_nothing"])
    lo, hi = hollow.wilson(not_unique, n_present)
    return {
        "catalogue": name, "label": ARMS[name]["label"], "field": field,
        "records": n_all, "present": n_present,
        "declared_completeness_pct": pct(n_present, n_all),
        "narrowing": {
            "not_unique": not_unique, "not_unique_pct": pct(not_unique, n_present),
            "not_unique_ci": [round(100 * lo, 2), round(100 * hi, 2)],
            "identifies_nothing": nothing, "identifies_nothing_pct": pct(nothing, n_present),
            "median_set_size": sorted(r["narrowing_set_size"] for r in recs)[n_present // 2]
                               if n_present else None,
            "mean_masked_tokens": round(sum(r["masked_token_count"] for r in recs) / n_present, 2)
                                  if n_present else None,
            "under_3_masked_tokens": sum(1 for r in recs if r["masked_token_count"] < 3),
            "under_3_masked_tokens_pct": pct(sum(1 for r in recs if r["masked_token_count"] < 3),
                                             n_present),
        },
        "screen": {k: {"n": sum(1 for r in recs if r[k]), "pct": pct(sum(1 for r in recs if r[k]),
                                                                     n_present)}
                   for k in ("r1_chrome", "r2_truncated_tail", "r3_truncated_head",
                             "r4_duplicate", "r5_title_echo", "hollow_strict", "hollow_broad")},
        "_recs": recs,
    }


# ---------------------------------------------------------------------------
# Instrument 2 — the sheet (PREREGISTRATION §2.3). This writes no label.
# ---------------------------------------------------------------------------

def make_sheet(name: str, recs: list[dict], masked_arm: bool, seed_offset: int) -> tuple[dict, dict]:
    held = [r for r in recs if r["half"] == 1]
    rng = random.Random(SEED + seed_offset)
    titles = [r["title"] for r in held]
    picked = rng.sample(held, min(N_SAMPLE, len(held)))

    items, trunc = [], []
    for i, r in enumerate(picked):
        pool = [t for t in titles if t != r["title"]]
        distract = random.Random(SEED + seed_offset + 1000 + i).sample(pool, N_CANDIDATES - 1)
        cands = distract + [r["title"]]
        random.Random(SEED + seed_offset + 2000 + i).shuffle(cands)
        value = r["masked"] if masked_arm else hollow.norm(nfkc(r["text"]))
        truncated = len(value) > SHEET_CAP_CHARS
        if truncated:
            trunc.append({"item": i + 1, "id": r["id"], "full_chars": len(value),
                          "shown_chars": SHEET_CAP_CHARS})
            value = value[:SHEET_CAP_CHARS]
        items.append({
            "item": i + 1, "value": value, "truncated": truncated,
            "candidates": [{"index": j + 1, "title": t} for j, t in enumerate(cands)],
        })
    key = [{"item": i + 1,
            "id": r["id"],
            "correct_index": next(c["index"] for c in items[i]["candidates"]
                                  if c["title"] == r["title"])}
           for i, r in enumerate(picked)]

    sheet = {
        "_instruction": (
            "For each item: one descriptive value from a catalogue, and five candidate titles. "
            "Exactly one candidate is the title of the record this value belongs to. Choose it. "
            "Answer with the candidate's index (1-5), or the string \"cannot_tell\" if the value "
            "gives you nothing to go on. There is no partial credit and guessing is expected where "
            "the value is uninformative; a wrong guess and a \"cannot_tell\" are treated "
            "differently in the record, so do not use \"cannot_tell\" to avoid committing."
        ),
        "_mask_note": ("A filled block character stands where a word of the record's own title was "
                       "removed." if masked_arm else
                       "Values are shown as the catalogue holds them, unmodified."),
        "_arm": name, "_masked": masked_arm, "_n": len(items),
        "_truncation": ("Values longer than 1200 characters are cut at 1200 and marked "
                        "truncated:true. The full lengths are in data/sheet-truncation.json."),
        "items": items,
    }
    return sheet, {"key": key, "sampled_ids": [r["id"] for r in picked], "truncation": trunc}


# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--cache", required=True)
    args = ap.parse_args()

    os.makedirs(args.cache, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)

    manifest_path = os.path.join(OUT, "manifest.json")
    if args.fetch:
        manifest = {"atlas": harvest_atlas(args.cache), "uk": harvest_uk(args.cache)}
        json.dump(manifest, open(manifest_path, "w"), indent=2, ensure_ascii=False)
    else:
        manifest = json.load(open(manifest_path))

    arms = {n: build_arm(n, load(args.cache, n)) for n in ARMS}

    # The sheets. Written before any label exists.
    sheets = {
        "atlas-masked": make_sheet("atlas", arms["atlas"]["_recs"], True, 0),
        "atlas-unmasked": make_sheet("atlas", arms["atlas"]["_recs"], False, 0),
        "uk-masked": make_sheet("uk", arms["uk"]["_recs"], True, 7),
    }
    # atlas-masked and atlas-unmasked must be the SAME 60 items in the SAME order (§2.3).
    a_ids = sheets["atlas-masked"][1]["sampled_ids"]
    b_ids = sheets["atlas-unmasked"][1]["sampled_ids"]
    if a_ids != b_ids:
        print("HOME ARMS DIVERGED: masked and unmasked sheets are not the same items", file=sys.stderr)
        return 2

    keys, truncs = {}, {}
    for label, (sheet, aux) in sheets.items():
        json.dump(sheet, open(os.path.join(OUT, f"sheet-{label}.json"), "w"),
                  indent=2, ensure_ascii=False)
        keys[label] = aux["key"]
        truncs[label] = aux["truncation"]
    json.dump(keys, open(os.path.join(OUT, "sheet-key.json"), "w"), indent=2, ensure_ascii=False)
    json.dump(truncs, open(os.path.join(OUT, "sheet-truncation.json"), "w"),
              indent=2, ensure_ascii=False)

    census = {n: {k: v for k, v in a.items() if k != "_recs"} for n, a in arms.items()}
    json.dump({"generated_by": "tools/identify/identify.py", "date": "2026-09-12", "session": 158,
               "params": {"seed": SEED, "n_sample": N_SAMPLE, "n_candidates": N_CANDIDATES,
                          "common_df_fraction": COMMON_DF_FRACTION, "n_rarest": N_RAREST,
                          "sheet_cap_chars": SHEET_CAP_CHARS},
               "manifest": manifest, "census": census},
              open(os.path.join(OUT, "census.json"), "w"), indent=2, ensure_ascii=False)

    # the per-record table stays out of the repository (third-party text, protocol §7)
    for n, a in arms.items():
        with open(os.path.join(args.cache, f"{n}-recs.jsonl"), "w", encoding="utf-8") as fh:
            for r in a["_recs"]:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    for n, c in census.items():
        print(f"{n}: {c['present']}/{c['records']} present ({c['declared_completeness_pct']} %), "
              f"not-unique {c['narrowing']['not_unique_pct']} %, "
              f"identifies-nothing {c['narrowing']['identifies_nothing_pct']} %, "
              f"broad {c['screen']['hollow_broad']['pct']} %")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
