#!/usr/bin/env python3
"""Layer 3 — trust re-validation of the six shipped `Valid` manifests (the round-3 fold).

Folded into instrument 014 in collective session 37 (2026-07-14) after the Split Seal
adversarial round's round-3 gate resolved (journal 2026-07-13, session 36; trust/SOURCES.md).
The shipped Layer-1 run (run_layer1.py) loaded no trust list, so every `validation_state: Valid`
also carried `signingCredential.untrusted` — "Valid" there means the signature is cryptographically
intact, NOT that the signer is trust-anchored. This script re-validates the six shipped `Valid`
manifests (c02, c08, c09, w01, w02, w03), bytes frozen, under three configurations:

  - none         : no trust list (reproduces the shipped Layer-1 run exactly)
  - official_TL  : the current official C2PA Trust List (conformance program), CA anchors
  - ITL          : the Interim Trust List (anchors + allowed) the C2PA Verify site uses

adv1 — the forged `Valid + untrusted` manifest built for the adversarial follow-on round — is NOT
a specimen of this work (its bytes live only in that round's sha256-pinned registry). Its result,
carried in the caveat below, is that it stays `untrusted` under EVERY configuration (it chains to
nothing); source: drafts/2026-07-12-split-seal-adversarial/data/layer3-trust.json, journal
2026-07-13. This work's frozen 15-specimen set is unchanged.

Trust files and their provenance/sha256: ../trust/ and ../trust/SOURCES.md. Deterministic given the
committed specimen bytes, the committed trust PEMs, and the pinned library version.

Output: data/layer3-trust.json. Requires: pip install -r requirements.txt (c2pa-python 0.36.0).
"""
import hashlib
import json
from pathlib import Path

import c2pa

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "specimens"
TRUST = ROOT / "trust"

# id -> path (bytes frozen; the six shipped `Valid` manifests only — adv1 is not a specimen here)
SPECIMENS = {
    "c02": SPEC / "adobe-20220124-C.jpg",
    "c08": SPEC / "truepic-20230212-camera.jpg",
    "c09": SPEC / "truepic-20230212-landscape.jpg",
    "w01": SPEC / "wild-chatgpt-soldering.webp",
    "w02": SPEC / "wild-chatgpt-imagetitis.webp",
    "w03": SPEC / "wild-msdesigner-gato.png",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_configs() -> dict:
    official = (TRUST / "C2PA-TRUST-LIST.pem").read_text()
    itl_anchors = (TRUST / "ITL-anchors.pem").read_text()
    itl_allowed = (TRUST / "ITL-allowed.pem").read_text()
    return {
        # None => read with no trust configuration (matches the shipped Layer-1 run)
        "none": None,
        "official_TL": {
            "trust": {"trust_anchors": official},
            "verify": {"verify_trust": True},
        },
        "ITL": {
            "trust": {"trust_anchors": itl_anchors, "allowed_list": itl_allowed},
            "verify": {"verify_trust": True},
        },
    }


def read(path: Path, settings: dict | None) -> dict:
    if settings is None:
        with c2pa.Reader(str(path)) as reader:
            m = json.loads(reader.json())
    else:
        s = c2pa.Settings.from_json(json.dumps(settings))
        ctx = c2pa.ContextBuilder().with_settings(s).build()
        with c2pa.Reader(str(path), context=ctx) as reader:
            m = json.loads(reader.json())
    active = (m.get("manifests") or {}).get(m.get("active_manifest"), {})
    sig = active.get("signature_info") or {}
    codes = [x.get("code") for x in (m.get("validation_status") or [])]
    return {
        "validation_state": m.get("validation_state"),
        "signer_untrusted": "signingCredential.untrusted" in codes,
        "status_codes": codes,
        "signer_issuer": sig.get("issuer"),
        "signer_common_name": sig.get("common_name"),
    }


def main() -> None:
    configs = build_configs()
    trust_files = {p.name: sha256(p) for p in sorted(TRUST.glob("*.pem"))}
    results = {}
    for sid, path in SPECIMENS.items():
        results[sid] = {
            "specimen_sha256": sha256(path),
            "by_config": {name: read(path, cfg) for name, cfg in configs.items()},
        }
        r = results[sid]["by_config"]
        print(f"{sid:5} {r['none']['signer_issuer'] or '-':26} "
              f"none={r['none']['validation_state']}"
              f"{'/untr' if r['none']['signer_untrusted'] else ''}  "
              f"official={r['official_TL']['validation_state']}"
              f"{'/untr' if r['official_TL']['signer_untrusted'] else ''}  "
              f"ITL={r['ITL']['validation_state']}"
              f"{'/untr' if r['ITL']['signer_untrusted'] else ''}")
    payload = {
        "layer": "manifest trust re-validation (C2PA) — the six shipped Valid manifests",
        "tool": f"c2pa-python {getattr(c2pa, '__version__', 'unknown')}",
        "run_date": "2026-07-14",
        "source": "folds the Split Seal adversarial round's round-3 gate (journal 2026-07-13, "
                  "session 36) into instrument 014; adv1 (the forge) stays untrusted under every "
                  "list — see drafts/2026-07-12-split-seal-adversarial/data/layer3-trust.json",
        "configs": {
            "none": "no trust list (reproduces the shipped Layer-1 run)",
            "official_TL": "current official C2PA Trust List (conformance program), trust_anchors",
            "ITL": "Interim Trust List (anchors + allowed) used by the C2PA Verify site",
        },
        "trust_files_sha256": trust_files,
        "results": results,
    }
    (ROOT / "data" / "layer3-trust.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8")
    print("layer3-trust.json written")


if __name__ == "__main__":
    main()
