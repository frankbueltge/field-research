#!/usr/bin/env python3
"""Integration bundle for "The Split Seal" (added session 30, conformance fix).

The site's integrator copies only a work's TOP-LEVEL files (SITE-API.md: "data inline or
local `./data.json`"), so the three canonical pipeline outputs under data/ are merged into
one derived, top-level data.json. The pipeline outputs stay canonical; this bundle is
machine-derived and drift is checkable: re-running this script must be a no-op.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    bundle = {
        "specimens": json.loads((ROOT / "data" / "specimens.json").read_text()),
        "layer1": json.loads((ROOT / "data" / "layer1.json").read_text()),
        "layer2": json.loads((ROOT / "data" / "layer2.json").read_text()),
    }
    out = ROOT / "data.json"
    out.write_text(json.dumps(bundle, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
                   encoding="utf-8")
    # drift check: the bundle must reparse to exactly the three sources
    reparsed = json.loads(out.read_text())
    for key, src in (("specimens", "specimens.json"), ("layer1", "layer1.json"),
                     ("layer2", "layer2.json")):
        assert reparsed[key] == json.loads((ROOT / "data" / src).read_text()), key
    print("data.json written; equality verified against data/*.json")


if __name__ == "__main__":
    main()
