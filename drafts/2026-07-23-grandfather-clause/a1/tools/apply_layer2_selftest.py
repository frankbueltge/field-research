#!/usr/bin/env python3
"""Prove the Layer-2 reading rule executes, before the data it will read exists.

Committed collective session 81, 2026-08-02, alongside `apply_layer2.py` and
`../LAYER2-PROTOCOL.md` — and before the detector job was queued. A rule that has never been
run is a rule nobody has checked; this runs it.

EVERYTHING HERE IS A CONSTRUCTED FIXTURE. No fixture is a specimen, no number in this file is
a measurement, and nothing this file prints is a finding about anything in the world. Its only
subject is `apply_layer2.py`. Fixtures are written to a temporary directory and the real `a1/`
is never touched — asserted, not assumed, at the end of the run.

    python3 apply_layer2_selftest.py        # 22 assertions, exit 0 on pass
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
A1 = HERE.parent
SCRIPT = HERE / "apply_layer2.py"

PASSED = 0
FAILED: list[str] = []


def check(name: str, cond: bool) -> None:
    global PASSED
    if cond:
        PASSED += 1
        print(f"  ok    {name}")
    else:
        FAILED.append(name)
        print(f"  FAIL  {name}")


def specimen(sid, stratum, state, in_rule=True, provider="Fixture Provider") -> dict:
    return {"id": sid, "stratum": stratum, "state": state, "in_decision_rule": in_rule,
            "provider": provider, "file": f"{sid}.png", "sha256": "0" * 64,
            "days_since_seam": 0, "captured": "2026-08-02"}


def build(tmp: Path, specimens: list[dict], scores: dict, *, l2_extra: dict | None = None) -> Path:
    """Lay out a fake `a1/` — tools/ plus the two input files — and return its root."""
    a1 = tmp / "a1"
    (a1 / "tools").mkdir(parents=True, exist_ok=True)
    shutil.copy(SCRIPT, a1 / "tools" / "apply_layer2.py")
    (a1 / "a1-results.json").write_text(json.dumps({
        "anchor": "A1", "date": "2026-08-02", "days_since_seam": 0,
        "layer2": "deferred", "specimens": specimens}), encoding="utf-8")
    payload = {"anchor": "A1", "layer2_run_date": "2026-08-09",
               "days_from_seam_to_layer2_scoring": 7,
               "sha256_all_verified_before_upload": True,
               "specimens_attempted": len(specimens),
               "specimens_scored": sum(1 for v in scores.values() if "ai_generated" in v),
               "results": scores}
    payload.update(l2_extra or {})
    (a1 / "layer2.json").write_text(json.dumps(payload), encoding="utf-8")
    return a1


def run(a1: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(a1 / "tools" / "apply_layer2.py")],
                          capture_output=True, text=True)


def main() -> int:
    a1_before = sorted(p.name for p in A1.iterdir())

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)

        # --- case 1: the A1 shape itself — every no-manifest row indeterminate ----------
        # This is the shape the real anchor is in, so protocol R3's pre-registered null is
        # exercised here rather than merely asserted in prose.
        specimens = [specimen("s01", "S-signatory", "indeterminate-at-capture"),
                     specimen("s04", "S-signatory", "machine-readable-marked"),
                     specimen("n01", "N-nonsignatory", "indeterminate-at-capture"),
                     specimen("c01", "C-camera-control", "manifest-not-synthetic"),
                     specimen("x01", "X-observation-only", "indeterminate-at-capture", False)]
        scores = {"s01": {"ai_generated": 0.99}, "s04": {"ai_generated": 0.95},
                  "n01": {"ai_generated": 0.97}, "c01": {"ai_generated": 0.01},
                  "x01": {"ai_generated": 0.93}}
        a1 = build(tmp / "c1", specimens, scores)
        r = run(a1)
        out = json.loads((a1 / "a1-layer2-reading.json").read_text())
        check("case 1 exits 0", r.returncode == 0)
        check("case 1: no row is eligible for the flagged state — every no-manifest row is "
              "indeterminate (R3)", out["unmarked_but_detector_flagged"]["eligible_rows"] == 0)
        check("case 1: the state is empty even though three indeterminate rows score >= 0.90",
              out["unmarked_but_detector_flagged"]["count"] == 0)
        check("case 1: tiers applied at the inherited boundaries",
              [x["tier"] for x in out["specimens"]] ==
              ["flagged AI — high", "flagged AI — high", "flagged AI — high",
               "flagged human — high", "flagged AI — high"])
        check("case 1: the scoring date is carried separately from the capture date (R8)",
              out["days_since_seam_at_capture"] == 0
              and out["days_from_seam_to_layer2_scoring"] == 7)
        check("case 1: a1-results.json is not written to (R10)",
              json.loads((a1 / "a1-results.json").read_text())["layer2"] == "deferred")
        check("case 1: the refusals are on the face of the output",
              len(out["refusals"]) == 4
              and any("accuracy" in x for x in out["refusals"])
              and any("directional" in x for x in out["refusals"]))
        check("case 1: rows outside the decision rule are carried, not silently dropped",
              any(x["id"] == "x01" and x["in_decision_rule"] is False
                  for x in out["specimens"]))

        # --- case 2: an eligible row exists and is flagged / not flagged ----------------
        # A shape A1 does not have, so the rule's live limb is exercised for A2's sake.
        specimens = [specimen("u01", "S-signatory", "unmarked-at-capture"),
                     specimen("u02", "S-signatory", "unmarked-at-capture"),
                     specimen("u03", "N-nonsignatory", "unmarked-at-capture")]
        scores = {"u01": {"ai_generated": 0.90}, "u02": {"ai_generated": 0.8999},
                  "u03": {"ai_generated": 0.42}}
        a1 = build(tmp / "c2", specimens, scores)
        r = run(a1)
        out = json.loads((a1 / "a1-layer2-reading.json").read_text())
        check("case 2 exits 0", r.returncode == 0)
        check("case 2: all three rows are eligible",
              out["unmarked_but_detector_flagged"]["eligible_rows"] == 3)
        check("case 2: the threshold is inclusive at exactly 0.90 and excludes 0.8999",
              out["unmarked_but_detector_flagged"]["flagged_ids"] == ["u01"])

        # --- case 3: a specimen the detector could not score ----------------------------
        specimens = [specimen("e01", "S-signatory", "unmarked-at-capture")]
        scores = {"e01": {"error": {"type": "usage_limit", "message": "fixture"}}}
        a1 = build(tmp / "c3", specimens, scores)
        r = run(a1)
        out = json.loads((a1 / "a1-layer2-reading.json").read_text())
        check("case 3 exits 0 — an unscored specimen is recorded, not fatal (R7)",
              r.returncode == 0)
        check("case 3: it is listed as unscored and carries its error",
              out["unscored_specimens"] == ["e01"]
              and out["specimens"][0]["detector_error"]["type"] == "usage_limit")
        check("case 3: an eligible row with no score is not counted as flagged",
              out["unmarked_but_detector_flagged"]["eligible_rows"] == 1
              and out["unmarked_but_detector_flagged"]["count"] == 0)

        # --- case 4: the two files disagree about which specimens exist -----------------
        specimens = [specimen("a01", "S-signatory", "unmarked-at-capture"),
                     specimen("a02", "S-signatory", "unmarked-at-capture")]
        a1 = build(tmp / "c4", specimens, {"a01": {"ai_generated": 0.5}})
        r = run(a1)
        check("case 4 refuses to read across mismatched specimen sets",
              r.returncode != 0 and "a02" in r.stderr
              and not (a1 / "a1-layer2-reading.json").exists())

        # --- case 5: the job has not run yet -------------------------------------------
        a1 = build(tmp / "c5", [specimen("z01", "S-signatory", "unmarked-at-capture")], {})
        (a1 / "layer2.json").unlink()
        r = run(a1)
        check("case 5: a missing layer2.json is a clear stop, not a traceback",
              r.returncode != 0 and "has not run" in r.stderr
              and "Traceback" not in r.stderr)

        # --- case 6: the R6 guard, which makes the no-accuracy prohibition checkable ----
        # The Skeptic's objection (C6, session 81) was that R6 was a comment, not a barrier:
        # `strata_descriptive` already holds a stratum-by-tier cross-tabulation, so one added
        # division would produce the forbidden rate. The guard's invariant is that every value
        # under it is a whole count or a mapping of whole counts. Exercised directly.
        import importlib.util
        spec = importlib.util.spec_from_file_location("al2", SCRIPT)
        al2 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(al2)

        def guard_rejects(strata) -> bool:
            try:
                al2.assert_no_derived_rate(strata)
            except SystemExit:
                return True
            return False

        check("R6 guard: passes a clean stratum of counts",
              not guard_rejects({"S": {"n": 5, "scored": 5,
                                       "tiers": {"flagged AI — high": 3},
                                       "layer1_states": {"indeterminate-at-capture": 5}}}))
        check("R6 guard: rejects a derived rate over stratum x tier — the exact forbidden move",
              guard_rejects({"S": {"n": 5, "scored": 5, "flagged_rate": 0.6}}))
        check("R6 guard: rejects a float hidden inside the tier mapping",
              guard_rejects({"S": {"n": 5, "tiers": {"flagged AI — high": 0.6}}}))
        check("R6 guard: rejects a non-count value that is neither int nor mapping of ints",
              guard_rejects({"S": {"n": 5, "note": "AI-leaning dominates"}}))
        check("R6 guard: the real output passed it — case 1 wrote its file",
              (tmp / "c1" / "a1" / "a1-layer2-reading.json").is_file())

    check("the real a1/ directory was not touched", sorted(p.name for p in A1.iterdir()) == a1_before)

    print(f"\n{PASSED} passed, {len(FAILED)} failed")
    for f in FAILED:
        print(f"  FAILED: {f}")
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
