#!/usr/bin/env python3
"""A1 — the alternative reading under Rule A1-S′, computed AFTER the governing one.

READ THIS BEFORE READING ITS NUMBERS. This script does NOT produce the anchor's
governing reading. `a1-results.json`, produced by `score_a1.py` under Rule A1-S as that
rule stood committed before any specimen was scored, is the governing reading, and it
stays the governing reading. What is below is post-hoc, is labelled post-hoc everywhere
it appears, and supplies no directional label to anything.

WHY IT EXISTS. Rule A1-S classified a no-manifest specimen as `indeterminate-at-capture`
if it carried no ancillary metadata at all (limb S2), on the stated premise that a
generator's own output file essentially always carries XMP, EXIF or a PNG text chunk, so
carrying none is evidence the container was rebuilt in transport. Specimen s04 falsifies
that premise on the S-stratum delivery path: it carries a valid C2PA manifest asserting
a synthetic digitalSourceType and it carries no XMP, no EXIF and no PNG text chunk
either. So "no ancillary metadata" does not imply "container rebuilt", and — more to the
point — a manifest demonstrably survives that exact delivery path, because one did.

RULE A1-S′, PRE-REGISTERED HERE FOR ANCHOR A2 AND ANY LATER ANCHOR:

    Limb S2 is replaced by a PATH-LEVEL POSITIVE CONTROL. If any specimen captured from
    the same delivery path at the same anchor carries a parsing C2PA manifest, that path
    is non-stripping at that anchor, and its no-manifest specimens are recorded
    `unmarked-at-capture`, not `indeterminate-at-capture`. Where no such positive control
    exists on a path, the old S2 test stands as the fallback, because then nothing has
    shown the path preserves manifests. Limb S1 (transport evidence in the URL) is
    unchanged and still sufficient on its own.

Note what A1-S′ does NOT do, which is the test of whether it was written to fit the
result: it does not rescue the N stratum. No Stability AI specimen carries a manifest,
so that path has no positive control, the S2 fallback applies unchanged, and the stratum
stays `capture-inconclusive` under both rules. The same holds for the Google observation
group. The corrected rule changes exactly one stratum, in the direction the evidence
points, and leaves the two it cannot speak to alone.

"Delivery path" is keyed on the URL host plus the first path segment — the granularity at
which a transformation service is configured.
"""
import json
import math
from pathlib import Path
from urllib.parse import urlsplit

A1 = Path(__file__).resolve().parent.parent


def path_key(url: str) -> str:
    parts = urlsplit(url)
    first = parts.path.lstrip("/").split("/")[0] if parts.path.strip("/") else ""
    return f"{parts.netloc}/{first}"


def wilson(k: int, n: int, z: float = 1.959963984540054):
    if n == 0:
        return None
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(max(0.0, centre - half), 4), round(min(1.0, centre + half), 4))


def main() -> int:
    res = json.loads((A1 / "a1-results.json").read_text())
    rows = res["specimens"]

    non_stripping = {path_key(r["source_url"]) for r in rows
                     if r["layer1"].get("manifest_present")}

    out = {"reading": "POST-HOC, NON-GOVERNING — Rule A1-S′",
           "governing_reading": "a1-results.json (Rule A1-S)",
           "non_stripping_paths_by_positive_control": sorted(non_stripping),
           "strata": {}}

    for r in rows:
        if not r["in_decision_rule"]:
            continue
        st = out["strata"].setdefault(r["stratum"], {"n": 0, "indeterminate": 0,
                                                     "marked": 0, "states": {}})
        state = r["state"]
        if state == "indeterminate-at-capture" and not r["container"]["S1_transport_evidence"] \
                and path_key(r["source_url"]) in non_stripping:
            state = "unmarked-at-capture"
        st["n"] += 1
        st["states"][state] = st["states"].get(state, 0) + 1
        st["indeterminate"] += state == "indeterminate-at-capture"
        st["marked"] += state == "machine-readable-marked"

    for name, st in out["strata"].items():
        st["effective_n"] = st["n"] - st["indeterminate"]
        st["capture_inconclusive"] = st["indeterminate"] / st["n"] > 0.40
        st["marked_proportion"] = (round(st["marked"] / st["effective_n"], 4)
                                   if st["effective_n"] else None)
        st["wilson_95"] = wilson(st["marked"], st["effective_n"])
        st["directional_label"] = ("none — a single anchor cannot carry one, and this "
                                   "reading is post-hoc besides")

    (A1 / "a1-alt-reading.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print("paths with a positive control:", sorted(non_stripping))
    for name, st in sorted(out["strata"].items()):
        print(f"{name}: n={st['n']} indet={st['indeterminate']} effN={st['effective_n']} "
              f"marked={st['marked']} p={st['marked_proportion']} wilson={st['wilson_95']} "
              f"{'CAPTURE-INCONCLUSIVE' if st['capture_inconclusive'] else ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
