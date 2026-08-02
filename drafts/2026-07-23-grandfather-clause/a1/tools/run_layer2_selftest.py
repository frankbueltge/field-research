#!/usr/bin/env python3
"""Prove the runner's two pre-network refusals, without making a network call.

Committed collective session 81, 2026-08-02, with `run_layer2.py` and before the job was
queued. It exercises ONLY the two paths that stop before any upload:

  1. no credential in the environment  -> refuse, exit non-zero (as instrument 014 does)
  2. a specimen whose bytes do not match the sha256 committed at capture
     -> refuse, exit non-zero, having uploaded nothing (LAYER2-PROTOCOL.md R1)

Guard 2 is the one that protects the anchor's integrity: scoring happens on another day, on
other hardware, from a checkout of `main`, so "the same bytes" has to be checked. This file
never constructs a case where the hashes MATCH, because that path would proceed to the live
interface and spend from a shared, finite budget. There is therefore no network call here at
all, by construction and not by mocking.

Fixtures are three bytes long and are not specimens. The real `a1/` is never touched.

    python3 run_layer2_selftest.py        # 11 assertions, exit 0 on pass
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
A1 = HERE.parent
SCRIPT = HERE / "run_layer2.py"
FIXTURE_BYTES = b"abc"
FIXTURE_SHA = hashlib.sha256(FIXTURE_BYTES).hexdigest()

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


def build(root: Path, committed_sha: str, *, write_file: bool = True) -> Path:
    a1 = root / "a1"
    (a1 / "tools").mkdir(parents=True, exist_ok=True)
    (a1 / "specimens").mkdir(parents=True, exist_ok=True)
    shutil.copy(SCRIPT, a1 / "tools" / "run_layer2.py")
    if write_file:
        (a1 / "specimens" / "f01.png").write_bytes(FIXTURE_BYTES)
    (a1 / "specimens.json").write_text(json.dumps([{
        "id": "f01", "file": "f01.png", "stratum": "S-signatory", "in_decision_rule": True,
        "sha256": committed_sha}]), encoding="utf-8")
    return a1


def run(a1: Path, env_extra: dict) -> subprocess.CompletedProcess:
    env = {**os.environ, **env_extra}
    return subprocess.run([sys.executable, str(a1 / "tools" / "run_layer2.py")],
                          capture_output=True, text=True, env=env)


CREDS = {"DETECTOR_IMAGE_API_USER": "selftest-no-such-user",
         "DETECTOR_IMAGE_API_SECRET": "selftest-no-such-secret"}


def main() -> int:
    a1_before = sorted(p.name for p in A1.iterdir())

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)

        # --- 1: no credential -> refuse before touching anything -----------------------
        a1 = build(tmp / "c1", FIXTURE_SHA)
        r = run(a1, {"DETECTOR_IMAGE_API_USER": "", "DETECTOR_IMAGE_API_SECRET": ""})
        check("no credential: exits non-zero rather than inventing scores",
              r.returncode != 0 and "refusing to fake results" in r.stderr)
        check("no credential: writes no layer2.json", not (a1 / "layer2.json").exists())

        # --- 2: bytes that do not match the committed hash -----------------------------
        a1 = build(tmp / "c2", "f" * 64)          # committed hash deliberately wrong
        r = run(a1, CREDS)
        check("hash mismatch: exits non-zero (R1)", r.returncode != 0)
        check("hash mismatch: names the specimen and both hashes",
              "f01" in r.stderr and "f" * 64 in r.stderr and FIXTURE_SHA in r.stderr)
        check("hash mismatch: says plainly that nothing was uploaded",
              "Nothing was uploaded" in r.stderr and not (a1 / "layer2.json").exists())

        # --- 3: a specimen file that is not there at all --------------------------------
        a1 = build(tmp / "c3", FIXTURE_SHA, write_file=False)
        r = run(a1, CREDS)
        check("missing specimen file: same refusal, not a traceback",
              r.returncode != 0 and "is missing" in r.stderr and "Traceback" not in r.stderr)

    # --- 4: the total-failure decision (Skeptic C4), unit-tested without a network call --
    # As first written this runner exited 0 when NOTHING scored, so a dead arm would have been
    # committed as a green run and the queue entry consumed. The decision now lives in its own
    # function. The end-to-end path is deliberately NOT exercised: proving it would mean calling
    # the live interface with bad credentials, and this practice does not make outbound calls to
    # prove a branch. That limit is stated rather than hidden.
    import importlib.util
    spec = importlib.util.spec_from_file_location("rl2", SCRIPT)
    rl2 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rl2)
    check("total failure: 0 of 17 scored is a failure, not a success",
          rl2.total_failure(0, 17) is True)
    check("total failure: a partial run is NOT treated as total failure",
          rl2.total_failure(1, 17) is False)
    check("total failure: a full run is not a failure", rl2.total_failure(17, 17) is False)
    check("total failure: an empty specimen list is not a failure (nothing was attempted)",
          rl2.total_failure(0, 0) is False)

    check("the real a1/ directory was not touched",
          sorted(p.name for p in A1.iterdir()) == a1_before)

    print(f"\n{PASSED} passed, {len(FAILED)} failed")
    for f in FAILED:
        print(f"  FAILED: {f}")
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
