#!/usr/bin/env python3
"""Layer 2 — the detector arm of "The Split Seal".

Runs each committed specimen ONCE through the provisioned commercial AI-image detector
(Sightengine, model `genai`) by uploading the bytes (never by URL — see dossier §4d),
and records the raw `type.ai_generated` score in [0,1] untouched. No thresholding
happens here: the pre-registered display tiers live in README.md and are applied only
at render time, so the raw floats stay the record.

Runs in GitHub Actions (workflow_dispatch) — the API credentials exist only as
repository secrets (DETECTOR_IMAGE_API_USER / DETECTOR_IMAGE_API_SECRET), a finding
recorded in session 09. Budget note: one run = 15 checks; the free tier sustains
~2,000 operations/month (dossier §4d) — do not re-run casually.

Output: data/layer2.json.
"""
import json
import os
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
ENDPOINT = "https://api.sightengine.com/1.0/check.json"

MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
        ".webp": "image/webp"}


def main() -> None:
    user = os.environ.get("DETECTOR_IMAGE_API_USER")
    secret = os.environ.get("DETECTOR_IMAGE_API_SECRET")
    if not user or not secret:
        sys.exit("detector credentials not present in environment — refusing to fake results")

    specimens = json.loads((ROOT / "data" / "specimens.json").read_text())
    results = {}
    for s in specimens:
        path = ROOT / "specimens" / s["file"]
        with path.open("rb") as fh:
            resp = requests.post(
                ENDPOINT,
                files={"media": (s["file"], fh, MIME.get(path.suffix.lower(), "application/octet-stream"))},
                data={"models": "genai", "api_user": user, "api_secret": secret},
                timeout=60,
            )
        body = resp.json()
        entry = {"http_status": resp.status_code, "api_status": body.get("status")}
        if body.get("status") == "success":
            entry["ai_generated"] = body.get("type", {}).get("ai_generated")
            entry["operations_used"] = (body.get("request") or {}).get("operations")
        else:
            entry["error"] = body.get("error")
        results[s["id"]] = entry
        print(s["id"], "→", entry.get("ai_generated", entry.get("error")))
        time.sleep(1.5)

    payload = {
        "layer": "detector (statistical AI-image classifier)",
        "tool": "Sightengine `genai` model (commercial API)",
        "run_date": time.strftime("%Y-%m-%d"),
        "note": ("Raw scores, unthresholded. The detector is a statistical classifier, "
                 "NOT a watermark decoder; the collective holds no independent FPR/FNR "
                 "benchmark for it — display tiers are pre-registered in README.md and "
                 "carry no calibration authority."),
        "results": results,
    }
    (ROOT / "data" / "layer2.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8")
    print("layer2.json written")


if __name__ == "__main__":
    main()
