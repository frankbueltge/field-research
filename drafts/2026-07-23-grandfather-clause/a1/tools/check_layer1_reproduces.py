#!/usr/bin/env python3
"""A1 — does the inherited Layer 1 instrument still say what it said when it shipped?

The pre-registration inherits Layer 1 "verbatim from instrument 014" — the same
`run_layer1.py`, the same pinned library (`c2pa-python==0.36.0`). An inherited
instrument is only inherited if it still produces the same reading; otherwise A1 would
be comparing new specimens against an instrument that has quietly moved.

So before A1 scores anything, this runs the shipped script against the shipped work's
own 15 frozen, sha256-pinned specimens and diffs the result against the `layer1.json`
committed with that work on 2026-07-11. Any difference is a finding about the
instrument, not about the specimens, and must be reported before any A1 row is read.

Nothing in `works/` is written to: the specimens and the script are copied to a
temporary tree and the script writes there.

Exit 0 = identical. Exit 1 = drift (and the differing fields are printed).
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
WORK = REPO / "works" / "2026-07-11-split-seal"


def main() -> int:
    shipped = json.loads((WORK / "data" / "layer1.json").read_text())
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        shutil.copytree(WORK / "specimens", tmp / "specimens")
        (tmp / "data").mkdir()
        (tmp / "tools").mkdir()
        shutil.copy(WORK / "data" / "specimens.json", tmp / "data" / "specimens.json")
        shutil.copy(WORK / "tools" / "run_layer1.py", tmp / "tools" / "run_layer1.py")
        proc = subprocess.run([sys.executable, str(tmp / "tools" / "run_layer1.py")],
                              cwd=tmp, capture_output=True, text=True)
        if proc.returncode != 0:
            print("run_layer1.py failed:\n" + proc.stderr)
            return 1
        rerun = json.loads((tmp / "data" / "layer1.json").read_text())

    a, b = rerun["results"], shipped["results"]
    print(f"tool line — re-run: {rerun['tool']} | shipped: {shipped['tool']}")
    if set(a) != set(b):
        print(f"specimen sets differ: only-rerun={sorted(set(a)-set(b))} "
              f"only-shipped={sorted(set(b)-set(a))}")
        return 1
    diffs = [k for k in sorted(a) if a[k] != b[k]]
    if not diffs:
        print(f"IDENTICAL — all {len(a)} specimens reproduce the 2026-07-11 reading.")
        return 0
    for k in diffs:
        for f in sorted(set(a[k]) | set(b[k])):
            if a[k].get(f) != b[k].get(f):
                print(f"  {k}.{f}\n     re-run : {json.dumps(a[k].get(f))[:400]}"
                      f"\n     shipped: {json.dumps(b[k].get(f))[:400]}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
