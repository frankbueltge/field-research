#!/usr/bin/env python3
"""Round 3 — the trust-list re-validation gate for the Split Seal adversarial round.

The pre-registered ship-or-fold test (PRE-REGISTRATION.md, round-3 section, committed session 34
BEFORE this ran). Question: when a real, published C2PA trust list is loaded, do the shipped round's
genuine production signers (Truepic, Microsoft, an OpenAI-issued credential) validate as *trusted*
while adv1's ad-hoc `field-research` test root stays *untrusted*?

Re-validates the shipped round's six `Valid` manifests (c02, c08, c09, w01, w02, w03) together with
adv1, holding every specimen's bytes frozen, under three configurations:

  - none         : no trust list (reproduces the shipped Layer-1 run exactly)
  - official_TL  : the current official C2PA Trust List (conformance program)
  - ITL          : the Interim Trust List (anchors + allowed) the Verify site uses

Trust files and their provenance/sha256: ../trust/ and ../trust/SOURCES.md. Deterministic given the
committed specimen bytes, the committed trust PEMs, and the pinned library version.

Output: data/layer3-trust.json. Requires: pip install -r requirements.txt (c2pa-python 0.36.0).
"""
import hashlib
import json
from pathlib import Path

import c2pa

DRAFT = Path(__file__).resolve().parent.parent
REPO = DRAFT.parent.parent  # repo root
SHIPPED = REPO / "works" / "2026-07-11-split-seal" / "specimens"

# id -> path (bytes frozen; the six shipped `Valid` manifests + the forge)
SPECIMENS = {
    "c02": SHIPPED / "adobe-20220124-C.jpg",
    "c08": SHIPPED / "truepic-20230212-camera.jpg",
    "c09": SHIPPED / "truepic-20230212-landscape.jpg",
    "w01": SHIPPED / "wild-chatgpt-soldering.webp",
    "w02": SHIPPED / "wild-chatgpt-imagetitis.webp",
    "w03": SHIPPED / "wild-msdesigner-gato.png",
    "adv1": DRAFT / "specimens" / "adv-forge-capture.png",
}

TRUST = DRAFT / "trust"


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
        print(f"{sid:5} {results[sid]['by_config']['none']['signer_issuer'] or '-':26} "
              f"none={r['none']['validation_state']}"
              f"{'/untr' if r['none']['signer_untrusted'] else ''}  "
              f"official={r['official_TL']['validation_state']}"
              f"{'/untr' if r['official_TL']['signer_untrusted'] else ''}  "
              f"ITL={r['ITL']['validation_state']}"
              f"{'/untr' if r['ITL']['signer_untrusted'] else ''}")
    payload = {
        "layer": "manifest trust re-validation (C2PA, round 3)",
        "tool": f"c2pa-python {getattr(c2pa, '__version__', 'unknown')}",
        "run_date": "2026-07-13",
        "configs": {
            "none": "no trust list (reproduces the shipped Layer-1 run)",
            "official_TL": "current official C2PA Trust List (conformance program), trust_anchors",
            "ITL": "Interim Trust List (anchors + allowed) used by the C2PA Verify site",
        },
        "trust_files_sha256": trust_files,
        "results": results,
    }
    (DRAFT / "data" / "layer3-trust.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8")
    print("layer3-trust.json written")


if __name__ == "__main__":
    main()
