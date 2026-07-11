#!/usr/bin/env python3
"""Layer 1 — the manifest arm of "The Split Seal".

Reads every specimen in data/specimens.json with c2pa-python and records, per specimen:
manifest presence, validation state, validation status codes, claim generator, signer
issuer, and every digitalSourceType asserted anywhere in the active manifest's actions.

Deterministic given the committed specimen bytes and the pinned library version.
Output: data/layer1.json. Requires: pip install -r requirements.txt (c2pa-python==0.36.0).
"""
import json
from pathlib import Path

import c2pa

ROOT = Path(__file__).resolve().parent.parent


def read_manifest(path: Path) -> dict:
    try:
        with c2pa.Reader(str(path)) as reader:
            m = json.loads(reader.json())
    except Exception as exc:  # ManifestNotFound and kin — the honest "no seal" case
        return {
            "manifest_present": False,
            "error": f"{type(exc).__name__}: {exc}",
        }
    active_label = m.get("active_manifest")
    manifest = (m.get("manifests") or {}).get(active_label, {})
    source_types = []
    for assertion in manifest.get("assertions", []):
        data = assertion.get("data") or {}
        for action in data.get("actions", []) if isinstance(data, dict) else []:
            dst = action.get("digitalSourceType")
            if dst:
                source_types.append({"action": action.get("action"), "digitalSourceType": dst})
    signature = manifest.get("signature_info") or {}
    return {
        "manifest_present": True,
        "validation_state": m.get("validation_state"),
        "validation_status": [
            {"code": s.get("code"), "url": s.get("url"), "explanation": s.get("explanation")}
            for s in (m.get("validation_status") or [])
        ],
        "claim_generator": manifest.get("claim_generator"),
        "title": manifest.get("title"),
        "signer_issuer": signature.get("issuer"),
        "signer_common_name": signature.get("common_name"),
        "cert_serial": signature.get("cert_serial_number"),
        "digital_source_types": source_types,
        "assertion_labels": [a.get("label") for a in manifest.get("assertions", [])],
    }


def main() -> None:
    specimens = json.loads((ROOT / "data" / "specimens.json").read_text())
    results = {}
    for s in specimens:
        results[s["id"]] = read_manifest(ROOT / "specimens" / s["file"])
        print(s["id"], "→",
              "manifest" if results[s["id"]].get("manifest_present") else "no manifest",
              results[s["id"]].get("validation_state", ""))
    payload = {
        "layer": "manifest (C2PA)",
        "tool": f"c2pa-python {getattr(c2pa, '__version__', 'unknown')}",
        "run_date": "2026-07-11",
        "results": results,
    }
    (ROOT / "data" / "layer1.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8")
    print("layer1.json written")


if __name__ == "__main__":
    main()
