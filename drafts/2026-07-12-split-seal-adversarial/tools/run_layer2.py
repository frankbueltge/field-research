#!/usr/bin/env python3
"""Layer 2 — the detector arm of the Split Seal adversarial round.

Uploads each committed specimen's BYTES (not a URL — the shipped round found some hosts reject
URL fetch) to the provisioned statistical AI-image detector and records the raw, unthresholded
`ai_generated` score. One run = 2 checks. Secrets are Actions-only (session-09 finding), so this
runs from the manual-dispatch workflow, never interactively.

Pre-registration note: `PRE-REGISTRATION.md` was committed BEFORE this script's output for
adv1/adv2 exists. The prediction (both ≈ 0.99, the shipped w03 pixels) and the meaning of each
outcome are fixed there. This script only records; it interprets nothing.

Output: data/layer2.json.
"""
import json
import os
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.sightengine.com/1.0/check.json"


def score(path: Path, user: str, secret: str) -> dict:
    with path.open("rb") as fh:
        resp = requests.post(
            API,
            files={"media": fh},
            data={"models": "genai", "api_user": user, "api_secret": secret},
            timeout=60,
        )
    j = resp.json()
    return {
        "ai_generated": (j.get("type") or {}).get("ai_generated"),
        "api_status": (j.get("status")),
        "http_status": resp.status_code,
        "operations_used": (j.get("operations") or {}).get("used")
        if isinstance(j.get("operations"), dict) else None,
        "raw_status": j.get("status"),
    }


def main() -> None:
    user = os.environ["DETECTOR_IMAGE_API_USER"]
    secret = os.environ["DETECTOR_IMAGE_API_SECRET"]
    specimens = json.loads((ROOT / "data" / "specimens.json").read_text())
    results = {}
    for s in specimens:
        results[s["id"]] = score(ROOT / "specimens" / s["file"], user, secret)
        print(s["id"], "→", results[s["id"]].get("ai_generated"))
    payload = {
        "layer": "detector (statistical AI-image classifier)",
        "note": "Raw scores, unthresholded. Statistical classifier, NOT a watermark decoder; no "
                "independent FPR/FNR benchmark; display tiers carry no calibration authority "
                "(see PRE-REGISTRATION.md).",
        "run_date": None,  # stamped by the workflow commit
        "results": results,
    }
    (ROOT / "data" / "layer2.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8")
    print("layer2.json written")


if __name__ == "__main__":
    main()
