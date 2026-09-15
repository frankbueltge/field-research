#!/usr/bin/env python3
"""Draw the pre-registered population for the refusal-shape study, mechanically.

Two house feeds are read live and never mirrored:
  https://frankbueltge.de/datasets/register.json   the sources this ecology's pipelines call
  https://frankbueltge.de/papers/register.json     the papers this ecology has examined

Strata (all rules fixed here, before any probe runs):

  H   every datasets-register entry whose reachability probe recorded 401 or 403,
      or which the register marks zugang_gesperrt. Taken whole, no sampling.
  L1  entry-weighted: a seeded simple random sample of 24 from every papers-register
      entry whose identifier check recorded 401, 403 or 429. Estimand: the share of
      THIS REGISTER'S RECORDED REFUSALS that are not the publisher's policy.
  L2  registrant-weighted: 24 DOI prefixes drawn by seed from the prefixes not already
      represented in L1, one entry per prefix. Estimand: the share of PUBLISHERS.
  C   positive control: 5 papers-register entries recorded 200 and 3 datasets-register
      entries recorded 200, seeded draw. The instrument must reach these.

Excluded from L by rule, with the ground stated: pruef_status 202 (50 entries). Session
157 recorded one 202-with-empty-body as a bot-block, but 202 is not a refusal status and
coding it would mix a judgement into a population definition.

    python3 tools/refusal-shape/population.py            # write data/population.json
    python3 tools/refusal-shape/population.py --check    # fail if the draw is not reproducible
"""
import hashlib
import json
import pathlib
import random
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
ART = ROOT / "artifacts/2026-09-15-whose-refusal-is-it"
DATA = ART / "data"

SEED = 20260915
DATASETS_URL = "https://frankbueltge.de/datasets/register.json"
PAPERS_URL = "https://frankbueltge.de/papers/register.json"

REFUSAL_STATUS = (401, 403, 429)
UA = "Meridian/1.0 (field research reachability probe; +https://frankbueltge.de/field)"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read()
    return json.loads(raw), hashlib.sha256(raw).hexdigest()


def draw():
    ds, ds_digest = fetch(DATASETS_URL)
    pa, pa_digest = fetch(PAPERS_URL)

    # --- H -------------------------------------------------------------------
    H = []
    for x in ds["entries"]:
        if x.get("pruef_status") in (401, 403) or x.get("zugang_gesperrt"):
            H.append(
                {
                    "unit_id": "H:" + x["id"],
                    "stratum": "H",
                    "url": x.get("zugriff_url") or x["adressen"][0],
                    "label": x["titel"],
                    "recorded_status": x.get("pruef_status"),
                    "recorded_note": x.get("pruef_vermerk"),
                    "register_says_blocked": bool(x.get("zugang_gesperrt")),
                }
            )
    H.sort(key=lambda r: r["unit_id"])

    # --- L -------------------------------------------------------------------
    pool = [
        x
        for x in pa["entries"]
        if x.get("pruef_status") in REFUSAL_STATUS and x.get("url")
    ]
    pool.sort(key=lambda x: x["id"])

    rng = random.Random(SEED)
    l1_idx = rng.sample(range(len(pool)), 24)
    L1 = [pool[i] for i in sorted(l1_idx)]
    used_prefix = {(x.get("kennung") or "?/").split("/")[0] for x in L1}

    by_prefix = {}
    for x in pool:
        p = (x.get("kennung") or "?/").split("/")[0]
        by_prefix.setdefault(p, []).append(x)
    free = sorted(p for p in by_prefix if p not in used_prefix)
    rng2 = random.Random(SEED + 1)
    pick = rng2.sample(free, min(24, len(free)))
    L2 = []
    for p in sorted(pick):
        rows = by_prefix[p]
        L2.append(rows[random.Random(SEED + 2 + int(p.split(".")[-1])).randrange(len(rows))])

    def paper_unit(x, stratum):
        return {
            "unit_id": f"{stratum}:{x['id']}",
            "stratum": stratum,
            "url": x["url"],
            "label": x["titel"][:90],
            "doi_prefix": (x.get("kennung") or "?/").split("/")[0],
            "recorded_status": x.get("pruef_status"),
            "recorded_note": x.get("pruef_vermerk"),
            "register_says_open": bool(x.get("frei_zugaenglich")),
        }

    # --- C -------------------------------------------------------------------
    ok_pa = sorted(
        [x for x in pa["entries"] if x.get("pruef_status") == 200 and x.get("url")],
        key=lambda x: x["id"],
    )
    ok_ds = sorted(
        [x for x in ds["entries"] if x.get("pruef_status") == 200 and (x.get("zugriff_url") or x.get("adressen"))],
        key=lambda x: x["id"],
    )
    rng3 = random.Random(SEED + 7)
    C = [paper_unit(x, "C") for x in rng3.sample(ok_pa, 5)]
    for x in rng3.sample(ok_ds, 3):
        C.append(
            {
                "unit_id": "C:" + x["id"],
                "stratum": "C",
                "url": x.get("zugriff_url") or x["adressen"][0],
                "label": x["titel"],
                "recorded_status": 200,
                "recorded_note": x.get("pruef_vermerk"),
            }
        )

    units = H + [paper_unit(x, "L1") for x in L1] + [paper_unit(x, "L2") for x in L2] + C
    # A URL probed twice would be two requests to one door for one fact.
    seen, dedup = set(), []
    for u in units:
        if u["url"] in seen:
            u["duplicate_of_url"] = True
            continue
        seen.add(u["url"])
        dedup.append(u)

    return {
        "_note": "Pre-registered population for artifacts/2026-09-15-whose-refusal-is-it. "
        "Drawn before any probe ran. Rules in tools/refusal-shape/population.py and "
        "PREREGISTRATION.md; nothing here was chosen by hand.",
        "seed": SEED,
        "drawn_utc": None,
        "feeds": {
            "datasets_register": {"url": DATASETS_URL, "sha256": ds_digest, "count": ds["count"]},
            "papers_register": {"url": PAPERS_URL, "sha256": pa_digest, "count": pa["count"]},
        },
        "stratum_sizes": {
            "H_population": len(H),
            "H_drawn": len(H),
            "L_population": len(pool),
            "L1_drawn": 24,
            "L2_drawn": len(L2),
            "L2_prefixes_available": len(free),
            "L_distinct_prefixes": len(by_prefix),
            "C_drawn": len(C),
        },
        "excluded_by_rule": {
            "pruef_status_202": sum(1 for x in pa["entries"] if x.get("pruef_status") == 202),
            "ground": "202 is not a refusal status; session 157 coded one 202 as a bot-block "
            "by hand, and a judgement does not belong in a population rule.",
        },
        "units": dedup,
    }


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    out = DATA / "population.json"
    fresh = draw()
    if "--check" in sys.argv:
        old = json.loads(out.read_text())
        a = [u["url"] for u in old["units"]]
        b = [u["url"] for u in fresh["units"]]
        if a != b:
            print(f"DRAW NOT REPRODUCIBLE: {len(a)} committed vs {len(b)} redrawn")
            sys.exit(1)
        print(f"draw reproducible: {len(a)} units")
        return
    import datetime

    fresh["drawn_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    out.write_text(json.dumps(fresh, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {out} — {len(fresh['units'])} units")
    for s in ("H", "L1", "L2", "C"):
        print(f"  {s}: {sum(1 for u in fresh['units'] if u['stratum'] == s)}")


if __name__ == "__main__":
    main()
