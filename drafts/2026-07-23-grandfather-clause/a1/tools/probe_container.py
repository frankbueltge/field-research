#!/usr/bin/env python3
"""A1 — container evidence, so `indeterminate-at-capture` is a measurement, not a hunch.

WHY THIS EXISTS (written and committed BEFORE any A1 specimen was scored)
-------------------------------------------------------------------------
The pre-registration (session 55) states the guard but not the test:

    "Provenance-stripping guard: capture from the least-stripping available source ...
     A manifest absent because the host stripped it on upload is recorded as
     `indeterminate-at-capture`, never as 'provider did not mark' — a false-negative
     mode that must not be allowed to masquerade as a finding."

It never says how a session decides that the host stripped it. Left there, the decision
is the scorer's taste, and taste applied after seeing the result is exactly what a
pre-registration exists to prevent. So the rule is fixed here, in advance:

RULE A1-S (operational refinement of the pre-registered stripping guard)
    A specimen with NO C2PA manifest is classified `indeterminate-at-capture` — not
    `unmarked` — if EITHER of these holds:

    (S1) TRANSPORT EVIDENCE. The bytes were served from an image-transformation path:
         the URL contains an image-resizing/reformatting marker (`/_next/image`,
         `cdn-cgi/image`, `/image/upload/`, or a `w=`/`width=`/`format=`/`quality=`
         query parameter), or the served format differs from the format the source
         markup names for that asset.

    (S2) CONTAINER EVIDENCE. The file carries NO ancillary metadata whatsoever — no
         XMP packet, no EXIF, and (for PNG) no textual chunk. A generator's own output
         file essentially always carries at least one of these; a re-encoded delivery
         variant characteristically carries none. Absence of all three is evidence that
         the container was rebuilt in transport.

    A specimen with no manifest that triggers NEITHER S1 nor S2 is recorded as
    `unmarked-at-capture` — the only state from which the pre-registered
    `machine-readable-marked` proportion may take a denominator.

    S2 is deliberately CONSERVATIVE IN ONE DIRECTION ONLY: it can misclassify a genuine
    bare unmarked output as indeterminate, shrinking effective N. It cannot manufacture
    a marked specimen. Given that the pre-registration's stated fear is a false negative
    masquerading as a finding, erring toward indeterminate is the correct direction, and
    the cost — a smaller effective N, printed on the row — is visible to any reader.

This script only REPORTS the evidence; the classification is applied by `score_a1.py`.
Deterministic given the committed bytes.
"""
import json
import re
import sys
from pathlib import Path

TRANSFORM_MARKERS = ("/_next/image", "cdn-cgi/image", "/image/upload/", "/imgproxy/")
TRANSFORM_PARAMS = re.compile(r"[?&](w|width|format|quality|q|fm|auto|dpr)=", re.I)

MAGIC = [
    (b"\x89PNG\r\n\x1a\n", "png"),
    (b"\xff\xd8\xff", "jpeg"),
    (b"RIFF", "webp-riff"),
    (b"\x00\x00\x00 ftypavif", "avif"),
    (b"GIF8", "gif"),
]


def sniff(head: bytes) -> str:
    for sig, name in MAGIC:
        if head.startswith(sig):
            if name == "webp-riff":
                return "webp" if head[8:12] == b"WEBP" else "riff-other"
            return name
    if head[4:12] == b"ftypavif":
        return "avif"
    if head[4:8] == b"ftyp":
        return "isobmff(" + head[8:12].decode("latin-1", "replace") + ")"
    return "unknown"


def png_text_chunks(data: bytes) -> list:
    out, i = [], 8
    while i + 8 <= len(data):
        length = int.from_bytes(data[i:i + 4], "big")
        ctype = data[i + 4:i + 8].decode("latin-1", "replace")
        if ctype in ("tEXt", "iTXt", "zTXt", "eXIf"):
            out.append(ctype)
        if ctype == "IEND":
            break
        i += 12 + length
        if length > len(data):
            break
    return out


def probe(path: Path, source_url: str) -> dict:
    data = path.read_bytes()
    fmt = sniff(data[:16])
    # C2PA lives in a JUMBF box; the box type string is the reliable byte marker.
    has_jumbf = b"jumb" in data[:2_000_000] or b"jumb" in data[-2_000_000:]
    has_c2pa_ns = b"c2pa" in data[:2_000_000] or b"c2pa" in data[-2_000_000:]
    has_xmp = b"<x:xmpmeta" in data or b"W5M0MpCehiHzreSzNTczkc9d" in data
    has_exif = b"Exif\x00\x00" in data[:4_000_000] or b"eXIf" in data[:200_000]
    chunks = png_text_chunks(data) if fmt == "png" else []
    s1 = bool(any(m in source_url for m in TRANSFORM_MARKERS)
              or TRANSFORM_PARAMS.search(source_url))
    s2 = not (has_xmp or has_exif or chunks)
    return {
        "file": path.name,
        "bytes": len(data),
        "format_from_magic": fmt,
        "magic_hex": data[:16].hex(),
        "jumbf_box_marker": has_jumbf,
        "c2pa_string_marker": has_c2pa_ns,
        "xmp_packet": has_xmp,
        "exif": has_exif,
        "png_text_chunks": chunks,
        "S1_transport_evidence": s1,
        "S2_no_ancillary_metadata": s2,
        "stripping_evidence": s1 or s2,
    }


def main(manifest_path: str) -> int:
    reg = json.loads(Path(manifest_path).read_text())
    root = Path(manifest_path).resolve().parent
    out = []
    for s in reg:
        out.append({"id": s["id"], **probe(root / "specimens" / s["file"], s["source_url"])})
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
