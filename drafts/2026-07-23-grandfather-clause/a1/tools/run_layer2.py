#!/usr/bin/env python3
"""A1, Layer 2 — the detector arm, run from the queue with the credential.

WHAT THIS IS. Anchor A1 read the first limb of Article 50(2) of Regulation (EU) 2024/1689
("marked in a machine-readable format") on 2026-08-02 and recorded the second limb
("detectable as artificially generated") as `deferred`, because the detector credential
exists only as a repository secret and a research session is not the kind of run that can
see one (instrument 014, session 09). The access path now exists; this is the arm that
uses it, and it is the collective's own, not the driver's.

THE RULE BY WHICH ITS OUTPUT WILL BE READ WAS COMMITTED BEFORE THIS RAN: `../LAYER2-PROTOCOL.md`
(collective session 81, 2026-08-02). Read it before reading any number this produces.

The measurement is inherited verbatim from instrument 014's `run_layer2.py`: the same single
vendor, the same `genai` model, bytes uploaded (never a URL — 014 dossier §4d), and the raw
`ai_generated` score in [0,1] committed untouched. No thresholding happens here. The frozen
display tiers live in `../LAYER2-PROTOCOL.md` R2 and are applied only at reading time, by
`apply_layer2.py`, so the raw floats stay the record.

THE INTEGRITY STOP (protocol R1). Every specimen's sha256 is re-computed and compared with the
value committed at capture BEFORE anything is uploaded. Scoring happens on another day, on other
hardware, from a checkout of `main`, so "the same bytes" is a claim to be checked, not assumed.
A mismatch aborts having spent nothing.

FAILURE SEMANTICS, AND WHY THEY ARE ASYMMETRIC (protocol R7). A hash mismatch exits non-zero
BEFORE any call: the queue keeps the entry, the job goes red, a human looks, and it costs no
budget to repeat. A PARTIAL interface failure is recorded in the output and the run exits 0:
the file is written, the queue entry is consumed, and the shared budget is spent AT MOST ONCE.
A queued entry is retried daily, so a runner that went red on a partial fault it cannot fix
would spend the practice's shared free tier every night. Errors belong in the record, not in a
retry loop.

BUT A TOTAL FAILURE IS NOT A SUCCESS (Skeptic C4, session 81, blocking — applied). If NOT ONE
specimen scored, this exits non-zero: the entry stays queued and the job goes red. Nothing was
measured, so almost nothing was spent, and the queue driver's honesty rule — green means the
work landed, never that an error was echoed away — must not be defeated by a runner that writes
an empty file and returns 0. As first written, this script did exactly that.

BUDGET (protocol R9). One pass, 17 checks. At the operation cost instrument 014 actually
recorded — `operations_used: 5` on every one of its fifteen checks
(`works/2026-07-11-split-seal/data/layer2.json`) — that is roughly **85 operations**, not 17,
against a free tier of about 2,000 a month (014 dossier §4d). The earlier wording said "17
checks" and invited a five-fold underestimate; the Skeptic caught it. Once, for this anchor. A
re-run would be a new dated event with its own stated reason.

Output: `../layer2.json`. It does NOT touch `a1-results.json`, whose `layer2: "deferred"` is the
true record of what session 80 could reach on the seam and stays as it is (protocol R10).
"""
import hashlib
import json
import os
import sys
import time
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
A1 = HERE.parent
ENDPOINT = "https://api.sightengine.com/1.0/check.json"
SEAM = "2026-08-02"  # the Article 50 application date; A1's capture sits on it exactly

MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
        ".webp": "image/webp"}


def sha256(path: Path) -> str:
    """Never raises: an unreadable specimen must produce the tool's own refusal, not a traceback."""
    try:
        h = hashlib.sha256()
        with path.open("rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError as exc:
        return f"unreadable: {type(exc).__name__}: {exc}"


def total_failure(scored: int, attempted: int) -> bool:
    """Nothing scored at all, out of something attempted — a dead arm, not a partial fault.

    Pulled out as its own function so the decision can be unit-tested without a network call
    (Skeptic C4, session 81). The end-to-end path cannot be tested here: proving it would mean
    calling the live interface with bad credentials, and this practice does not make outbound
    calls to prove a branch.
    """
    return attempted > 0 and scored == 0


def days_between(a: str, b: str) -> int:
    """Whole days from ISO date `a` to ISO date `b`, without importing a calendar library."""
    import datetime
    return (datetime.date.fromisoformat(b) - datetime.date.fromisoformat(a)).days


def main() -> int:
    user = os.environ.get("DETECTOR_IMAGE_API_USER")
    secret = os.environ.get("DETECTOR_IMAGE_API_SECRET")
    if not user or not secret:
        # Same refusal as instrument 014: no credential, no invented numbers.
        sys.exit("detector credentials not present in environment — refusing to fake results")

    specimens = json.loads((A1 / "specimens.json").read_text(encoding="utf-8"))

    # ---- R1, the integrity stop: verify every byte before spending anything -------------
    mismatches = []
    for s in specimens:
        path = A1 / "specimens" / s["file"]
        if not path.is_file():
            mismatches.append(f"{s['id']}: {s['file']} is missing")
            continue
        actual = sha256(path)
        if actual != s["sha256"]:
            mismatches.append(f"{s['id']}: committed {s['sha256']} but found {actual}")
    if mismatches:
        for m in mismatches:
            print(f"HASH MISMATCH  {m}", file=sys.stderr)
        sys.exit(f"{len(mismatches)} specimen(s) do not match the hashes committed at capture — "
                 "refusing to score bytes the anchor did not freeze. Nothing was uploaded.")
    print(f"sha256: all {len(specimens)} specimens match the hashes committed at capture")

    # ---- the pass ----------------------------------------------------------------------
    run_date = time.strftime("%Y-%m-%d")
    results = {}
    scored = 0
    for s in specimens:
        path = A1 / "specimens" / s["file"]
        entry: dict = {"sha256_verified": True}
        try:
            with path.open("rb") as fh:
                resp = requests.post(
                    ENDPOINT,
                    files={"media": (s["file"], fh,
                                     MIME.get(path.suffix.lower(), "application/octet-stream"))},
                    data={"models": "genai", "api_user": user, "api_secret": secret},
                    timeout=60,
                )
            entry["http_status"] = resp.status_code
            body = resp.json()
            entry["api_status"] = body.get("status")
            if body.get("status") == "success":
                entry["ai_generated"] = body.get("type", {}).get("ai_generated")
                entry["operations_used"] = (body.get("request") or {}).get("operations")
                scored += 1
            else:
                entry["error"] = body.get("error")
        except Exception as exc:  # noqa: BLE001 — recorded, never swallowed; see R7
            entry["error"] = {"transport": f"{type(exc).__name__}: {exc}"}
        results[s["id"]] = entry
        print(s["id"], "→", entry.get("ai_generated", entry.get("error")))
        time.sleep(1.5)

    payload = {
        "anchor": "A1",
        "layer": "detector (statistical AI-image classifier)",
        "tool": "the provisioned commercial AI-image detector, `genai` model — the same single "
                "vendor and model as instrument 014, unchanged",
        "reading_rule": "LAYER2-PROTOCOL.md, committed 2026-08-02 (collective session 81) before "
                        "this ran and before any score existed",
        "capture_date": SEAM,
        "days_since_seam_at_capture": 0,
        "layer2_run_date": run_date,
        "days_from_seam_to_layer2_scoring": days_between(SEAM, run_date),
        "specimens_scored": scored,
        "specimens_attempted": len(specimens),
        "operations_used_total": sum(e["operations_used"] for e in results.values()
                                     if isinstance(e.get("operations_used"), int)),
        "sha256_all_verified_before_upload": True,
        "note": ("Raw scores, unthresholded. The detector is a statistical classifier, NOT a "
                 "watermark decoder; this practice holds no independent FPR/FNR benchmark for it, "
                 "and its entire prior calibration here is a single anecdotal true-negative. "
                 "Display tiers are pre-registered in LAYER2-PROTOCOL.md R2 and carry no "
                 "calibration authority. A score is not evidence that a specimen is or is not "
                 "AI-generated (R6). The scoring date is not the capture date (R8)."),
        "results": results,
    }
    (A1 / "layer2.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"layer2.json written — {scored}/{len(specimens)} scored, "
          f"{days_between(SEAM, run_date)} day(s) after the seam")

    if total_failure(scored, len(specimens)):
        # R7, second limb. Nothing scored is not a partial fault, it is a dead arm: the entry
        # stays queued, the job goes red, and it is looked at. Almost no budget was spent
        # precisely because nothing succeeded, so a retry is cheap. The file is left on disk
        # with its errors for whoever looks.
        sys.exit("NOT ONE specimen scored — the detector arm did not run. Entry kept in the "
                 "queue and the job reddened on purpose; layer2.json carries the per-specimen "
                 "errors. This is infrastructure, not a reading.")

    # Exit 0 on PARTIAL failure, on purpose: R7. The record carries the errors.
    return 0


if __name__ == "__main__":
    sys.exit(main())
