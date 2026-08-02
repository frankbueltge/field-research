#!/usr/bin/env python3
"""A1 — apply the pre-registered states and arithmetic to the captured specimens.

Reads `specimens.json` (the committed sample list, frozen with sha256s before any layer
ran), runs the inherited Layer 1 reading, applies Rule A1-S from `probe_container.py`,
and emits `a1-results.json`.

THE PRE-REGISTERED STATES (README §"Scoring", §"Decision rule"), applied here verbatim:

  machine-readable-marked   manifest present AND parses AND asserts a synthetic
                            digitalSourceType (trainedAlgorithmicMedia /
                            compositeWithTrainedAlgorithmicMedia)
  manifest-not-synthetic    manifest present and parses, no synthetic digitalSourceType
  manifest-invalid          manifest present, does not validate
  indeterminate-at-capture  no manifest AND Rule A1-S stripping evidence — EXCLUDED from
                            both numerator and denominator
  unmarked-at-capture       no manifest AND no stripping evidence — denominator only

  effective N = specimens in the stratum minus indeterminate-at-capture
  proportion   = machine-readable-marked / effective N, with a Wilson 95% interval
  capture-inconclusive when indeterminate / N > 0.40

NO DIRECTIONAL LABEL IS PRODUCED HERE. The pre-registration makes the load-bearing
comparison the fresh-capture pair A1 -> A2 (A2 not before 2026-12-02); A1 alone can
carry no adoption-shift, reversal or led-the-timeline label, and this script does not
compute one. `led-the-timeline` is explicitly deferred: it requires an A1 rate whose
interval excludes zero, which is a reading this collective takes only once the A1 row
has been through its own review.

Layer 2 is `deferred` at this anchor: it runs only via the repository's Actions-only
credential path (instrument 014, session 09), which is not reachable from a session
container. The pre-registered `unmarked-but-detector-flagged` state is therefore
UNAVAILABLE for A1, and the row says so.
"""
import json
import math
import subprocess
import sys
from pathlib import Path

import c2pa

HERE = Path(__file__).resolve().parent
A1 = HERE.parent
SYNTHETIC = {"trainedAlgorithmicMedia", "compositeWithTrainedAlgorithmicMedia",
             "http://cv.iptc.org/newscodes/digitalsourcetype/trainedAlgorithmicMedia",
             "http://cv.iptc.org/newscodes/digitalsourcetype/compositeWithTrainedAlgorithmicMedia"}


def read_manifest(path: Path) -> dict:
    """Identical logic to instrument 014's run_layer1.py read_manifest()."""
    try:
        with c2pa.Reader(str(path)) as reader:
            m = json.loads(reader.json())
    except Exception as exc:
        return {"manifest_present": False, "error": f"{type(exc).__name__}: {exc}"}
    active = m.get("active_manifest")
    manifest = (m.get("manifests") or {}).get(active, {})
    source_types = []
    for assertion in manifest.get("assertions", []):
        data = assertion.get("data") or {}
        for action in (data.get("actions", []) if isinstance(data, dict) else []):
            dst = action.get("digitalSourceType")
            if dst:
                source_types.append({"action": action.get("action"), "digitalSourceType": dst})
    sig = manifest.get("signature_info") or {}
    return {
        "manifest_present": True,
        "validation_state": m.get("validation_state"),
        "validation_status": [{"code": s.get("code"), "explanation": s.get("explanation")}
                              for s in (m.get("validation_status") or [])],
        "claim_generator": manifest.get("claim_generator"),
        "signer_issuer": sig.get("issuer"),
        "signer_common_name": sig.get("common_name"),
        "digital_source_types": source_types,
        "assertion_labels": [a.get("label") for a in manifest.get("assertions", [])],
    }


def wilson(k: int, n: int, z: float = 1.959963984540054):
    """Wilson score interval, 95%. Returns (lo, hi) or None when n == 0."""
    if n == 0:
        return None
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(max(0.0, centre - half), 4), round(min(1.0, centre + half), 4))


def classify(layer1: dict, container: dict) -> str:
    if layer1.get("manifest_present"):
        if str(layer1.get("validation_state")).lower() != "valid":
            return "manifest-invalid"
        types = {t["digitalSourceType"] for t in layer1.get("digital_source_types", [])}
        types |= {t.rsplit("/", 1)[-1] for t in types}
        return "machine-readable-marked" if types & SYNTHETIC else "manifest-not-synthetic"
    return "indeterminate-at-capture" if container["stripping_evidence"] else "unmarked-at-capture"


def main() -> int:
    reg = json.loads((A1 / "specimens.json").read_text())
    containers = {c["id"]: c for c in json.loads(subprocess.run(
        [sys.executable, str(HERE / "probe_container.py"), str(A1 / "specimens.json")],
        capture_output=True, text=True, check=True).stdout)}

    rows = []
    for s in reg:
        l1 = read_manifest(A1 / "specimens" / s["file"])
        rows.append({**s, "layer1": l1, "container": containers[s["id"]],
                     "state": classify(l1, containers[s["id"]]),
                     "layer2": "deferred"})

    strata = {}
    for r in rows:
        st = strata.setdefault(r["stratum"], {"n": 0, "indeterminate": 0, "marked": 0,
                                              "states": {},
                                              "in_decision_rule": r["in_decision_rule"]})
        st["n"] += 1
        st["states"][r["state"]] = st["states"].get(r["state"], 0) + 1
        if r["state"] == "indeterminate-at-capture":
            st["indeterminate"] += 1
        if r["state"] == "machine-readable-marked":
            st["marked"] += 1
    for name, st in strata.items():
        # AMENDMENT, made after the capture and before scoring, and said so in
        # CAPTURE-NOTES.md: the registry carries one group that is NOT one of the three
        # pre-registered strata (`X-observation-only`). It is recorded and probed
        # because what it shows is worth showing, but it supplies no numerator, no
        # denominator and no interval to anything. The guard is structural — it turns on
        # a flag written into the registry, not on any result — and it can only remove
        # numbers from the record, never add them.
        if not st["in_decision_rule"]:
            st["effective_n"] = None
            st["indeterminate_rate"] = None
            st["capture_inconclusive"] = None
            st["marked_proportion"] = None
            st["wilson_95"] = None
            st["directional_label"] = ("outside the pre-registered strata — observation "
                                       "only, supplies no numerator to any label")
            continue
        st["effective_n"] = st["n"] - st["indeterminate"]
        st["indeterminate_rate"] = round(st["indeterminate"] / st["n"], 4) if st["n"] else None
        st["capture_inconclusive"] = bool(st["n"] and st["indeterminate"] / st["n"] > 0.40)
        st["marked_proportion"] = (round(st["marked"] / st["effective_n"], 4)
                                   if st["effective_n"] else None)
        st["wilson_95"] = wilson(st["marked"], st["effective_n"])
        st["directional_label"] = ("not computable at a single anchor — the pre-registered "
                                   "load-bearing comparison is A1 -> A2")

    out = {"anchor": "A1", "date": "2026-08-02", "seam": "2026-08-02",
           "days_since_seam": 0,
           "layer1_tool": "c2pa-python 0.36.0 (pinned, as instrument 014)",
           "layer2": "deferred — Actions-only credential path unreachable; the "
                     "pre-registered unmarked-but-detector-flagged state is unavailable "
                     "for this anchor",
           "strata": strata, "specimens": rows}
    (A1 / "a1-results.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    for name, st in sorted(strata.items()):
        print(f"{name}: n={st['n']} indeterminate={st['indeterminate']} "
              f"effN={st['effective_n']} marked={st['marked']} "
              f"p={st['marked_proportion']} wilson={st['wilson_95']} "
              f"{'CAPTURE-INCONCLUSIVE' if st['capture_inconclusive'] else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
