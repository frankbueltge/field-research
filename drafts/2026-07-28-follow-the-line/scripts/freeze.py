#!/usr/bin/env python3
"""Freeze the fetched Paper Catalogue into the reduced, redacted extract this audit runs on.

Two reductions are applied, both deliberate and both disclosed on the work's face:

1. `zusammenfassung` (the abstract of each catalogued text) is DROPPED. Those abstracts are
   third-party material under publisher copyright; this practice's legal hygiene admits own,
   licensed, CC or public-domain material, or a genuine short quotation with source — not 208
   full abstracts vendored into its own repository. No assertion in this audit reads that field.

2. Inside the `urteil` block, the `modell` value is replaced by a fixed redaction token. The
   catalogue records there which generative model authored an entry's `relevanz` sentence. This
   practice's constitution forbids naming AI products or their vendors anywhere in its record,
   so the value is redacted while the FACT that the field exists, and its date, basis and
   session, are kept — those are what the audit's assertions read. The unredacted value is
   retrievable by anyone from the source URL, which is pinned by SHA-256 in ../SOURCES.md.

Usage:  python3 scripts/freeze.py <raw-papers.json> <out.json>

The output is written with sorted keys and a fixed separator so that the same input always
produces the same bytes.
"""
import json
import sys

REDACTION = "[redacted by the auditing practice: a generative-model identifier; " \
            "this practice's constitution forbids naming AI products or vendors in its " \
            "record. The unredacted value is in the source file pinned in SOURCES.md.]"

DROPPED_FIELD = "zusammenfassung"


def freeze(entries):
    out = []
    for e in entries:
        f = {k: v for k, v in e.items() if k != DROPPED_FIELD}
        if isinstance(f.get("urteil"), dict) and "modell" in f["urteil"]:
            f["urteil"] = dict(f["urteil"])
            f["urteil"]["modell"] = REDACTION
        out.append(f)
    return out


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    raw = json.load(open(sys.argv[1], encoding="utf-8"))
    if not isinstance(raw, list):
        raise SystemExit("expected a JSON array of catalogue entries")
    with open(sys.argv[2], "w", encoding="utf-8") as fh:
        json.dump(freeze(raw), fh, ensure_ascii=False, sort_keys=True,
                  indent=1, separators=(",", ": "))
        fh.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
