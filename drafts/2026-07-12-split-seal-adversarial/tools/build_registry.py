#!/usr/bin/env python3
"""Freeze the adversarial-round registry for The Split Seal — round 2 (constructed specimens).

Writes data/specimens.json: for each specimen, its file, tier, sha256 of the committed bytes,
and a short provenance note. Re-running this script MUST be a no-op against the committed
sha256 pins — if a byte changed, the printed hash will differ from the pinned one and the diff
is the alarm. Two specimens only, both constructed by the collective from the pixels of a single
wild specimen of the shipped round (w03), exactly as the round was pre-registered
(open-questions.md, session 29: "a forged-manifest specimen ... and a stripped-manifest twin of
a wild specimen").
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The frozen set. `expected_sha256` is the pin; build_registry re-derives and checks it.
SPECIMENS = [
    {
        "id": "adv1",
        "file": "adv-forge-capture.png",
        "tier": "constructed-forge",
        "expected_sha256": "e1c0465a73b65ccc81d6787d5a705c03a4ff2a960835060f235c80c95bdba37d",
        "provenance": (
            "Constructed by the collective. Base pixels: the decoded pixels of the shipped "
            "round's specimen w03 (wild-msdesigner-gato.png, a synthetic image of a cat, no "
            "person; Wikimedia Commons, licensed; already vetted in works/2026-07-11-split-seal). "
            "The genuine generator manifest was removed and a NEW C2PA manifest was embedded that "
            "asserts a hardware camera capture (digitalSourceType: digitalCapture) — a claim the "
            "pixels contradict. Signed by the collective's own openly-labelled, NON-PRODUCTION "
            "test root ('Split Seal Test Root CA' / O=field-research), which chains to no public "
            "trust list. Read-back verdict: validation_state=Valid, sole status code "
            "signingCredential.untrusted."
        ),
    },
    {
        "id": "adv2",
        "file": "adv-stripped-twin.png",
        "tier": "constructed-stripped",
        "expected_sha256": "1c259af0d3503daf93819a2888e57b8da452cb32b413309e70d8f22360c63ad4",
        "provenance": (
            "Constructed by the collective. Same decoded pixels as adv1 and as shipped w03, with "
            "the genuine generator manifest removed and NO manifest re-added (lossless PNG "
            "re-save drops the C2PA chunk; decoded pixels verified byte-identical to the base). "
            "The 'mark lost / stripped' case: an AI image circulating without any provenance."
        ),
    },
]


def main() -> None:
    out = []
    ok = True
    for s in SPECIMENS:
        raw = (ROOT / "specimens" / s["file"]).read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        match = digest == s["expected_sha256"]
        ok = ok and match
        print(f"{s['id']:5} {s['file']:26} sha256={digest[:16]}… "
              f"{'PIN OK' if match else 'PIN MISMATCH — REGISTRY NOT FROZEN'}")
        out.append({
            "id": s["id"], "file": s["file"], "tier": s["tier"],
            "sha256": digest, "provenance": s["provenance"],
        })
    (ROOT / "data" / "specimens.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("specimens.json written" + ("" if ok else "  [WARNING: a pin mismatched]"))


if __name__ == "__main__":
    main()
