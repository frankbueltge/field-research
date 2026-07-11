#!/usr/bin/env python3
"""Build data/specimens.json — the fixed specimen registry of "The Split Seal".

Run once at assembly (session 28); the registry is then FROZEN. Selection rules and
provenance are documented in README.md; every entry's bytes are committed under
specimens/ and pinned here by sha256. Deterministic output (sorted keys, stable order).
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = "https://github.com/c2pa-org/public-testfiles/tree/main/legacy/1.4/image/jpeg"
CORPUS_LICENSE = "CC BY-SA 4.0 (c2pa-org/public-testfiles)"

# tier: control-fixture = synthetic conformance artifact (parser-correctness axis)
#       control-camera  = real capture distributed inside the conformance corpus
#       wild            = real media found in circulation (content-truth axis)
SPECIMENS = [
    # -- controls: synthetic fixtures (Adobe 2022, made with make_test_images/c2pa-rs) --
    dict(id="c01", file="adobe-20220124-A.jpg", tier="control-fixture",
         expected="no manifest (corpus 'A' = parent ingredient file, no Content Credentials)",
         source=CORPUS, license=CORPUS_LICENSE),
    dict(id="c02", file="adobe-20220124-C.jpg", tier="control-fixture",
         expected="valid manifest (corpus 'C' = simple claim)",
         source=CORPUS, license=CORPUS_LICENSE),
    dict(id="c03", file="adobe-20220124-E-sig-CA.jpg", tier="control-fixture",
         expected="invalid: signature did not validate (corpus 'E-sig')",
         source=CORPUS, license=CORPUS_LICENSE),
    dict(id="c04", file="adobe-20220124-E-dat-CA.jpg", tier="control-fixture",
         expected="invalid: hard-binding hash mismatch (corpus 'E-dat')",
         source=CORPUS, license=CORPUS_LICENSE),
    dict(id="c05", file="adobe-20220124-E-clm-CAICAI.jpg", tier="control-fixture",
         expected="invalid: referenced claim missing (corpus 'E-clm')",
         source=CORPUS, license=CORPUS_LICENSE),
    dict(id="c06", file="adobe-20220124-E-uri-CA.jpg", tier="control-fixture",
         expected="invalid: assertion tampered, URI hash mismatch (corpus 'E-uri')",
         source=CORPUS, license=CORPUS_LICENSE),
    dict(id="c07", file="adobe-20220124-XCA.jpg", tier="control-fixture",
         expected="incomplete: hash mismatch / off the golden path (corpus 'X')",
         source=CORPUS, license=CORPUS_LICENSE),
    # -- controls: real captures distributed inside the corpus --
    dict(id="c08", file="truepic-20230212-camera.jpg", tier="control-camera",
         expected="valid hardware-signed capture (Truepic Lens SDK)",
         source=CORPUS, license=CORPUS_LICENSE),
    dict(id="c09", file="truepic-20230212-landscape.jpg", tier="control-camera",
         expected="valid hardware-signed capture (Truepic Lens SDK)",
         source=CORPUS, license=CORPUS_LICENSE),
    dict(id="c10", file="nikon-20221019-building.jpeg", tier="control-camera",
         expected="camera capture, invalid: claim signature mismatch (per corpus README)",
         source=CORPUS, license=CORPUS_LICENSE),
    # -- wild: real media found in circulation (Wikimedia Commons originals) --
    dict(id="w01", file="wild-chatgpt-soldering.webp", tier="wild",
         expected="AI image downloaded from a generator, manifest intact?",
         source="https://commons.wikimedia.org/wiki/File:DALL%C2%B7E_2025-02-21_23.58.53_-_A_simple_soldering_iron_with_a_stand._The_soldering_iron_has_a_slim,_ergonomic_handle_with_a_metallic_tip._The_stand_is_a_small_metal_base_with_a_coil.webp",
         license="Public domain (per Commons file page)",
         retrieved="2026-07-11", upload_date="2025-02-22"),
    dict(id="w02", file="wild-chatgpt-imagetitis.webp", tier="wild",
         expected="AI image downloaded from a generator, manifest intact?",
         source="https://commons.wikimedia.org/wiki/File:Imagetitis-affected_editor_by_ChatGPT_4.0_%26_DALL%C2%B7E_3_(2024).webp",
         license="Public domain (per Commons file page)",
         retrieved="2026-07-11", upload_date="2025-02-06"),
    dict(id="w03", file="wild-msdesigner-gato.png", tier="wild",
         expected="AI image from a consumer design tool, manifest intact?",
         source="https://commons.wikimedia.org/wiki/File:Gato_naranja_generado_por_IA.png",
         license="Public domain (per Commons file page)",
         retrieved="2026-07-11", upload_date="2024-02-25"),
    dict(id="w04", file="wild-nomanifest-commons-ai.png", tier="wild",
         expected="community-labelled AI image; machine-readable provenance?",
         source="https://commons.wikimedia.org/wiki/File:Wikimedia_Commons_AI_(2025).png",
         license="CC BY-SA 4.0 (per Commons file page)",
         retrieved="2026-07-11", upload_date="2025-01-24"),
    dict(id="w05", file="wild-human-cat.jpg", tier="wild",
         expected="human photograph (Alvesgaspar, 2010), pre-provenance-era",
         source="https://commons.wikimedia.org/wiki/File:Cat_November_2010-1a.jpg",
         license="CC BY-SA 3.0, author Alvesgaspar (per Commons file page)",
         retrieved="2026-07-11", upload_date="2010-11"),
]


def main() -> None:
    out = []
    for s in SPECIMENS:
        p = ROOT / "specimens" / s["file"]
        s["sha256"] = hashlib.sha256(p.read_bytes()).hexdigest()
        s["bytes"] = p.stat().st_size
        out.append(dict(sorted(s.items())))
    (ROOT / "data" / "specimens.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"registry written: {len(out)} specimens")


if __name__ == "__main__":
    main()
