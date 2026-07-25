"""
scripts/filter_corpus_api.py — PREREGISTRATION.md §2 corpus rules, applied to raw
query-API Atom chunks (harvest_api.py output), per §10 deviation D1. Stdlib only
(xml.etree, gzip, json, hashlib, re).

D1's field mapping (fixed there, reused verbatim here):
  - id: the arXiv id extracted from the entry's <id> URL, version suffix stripped
    (e.g. "http://arxiv.org/abs/2501.01234v2" -> "2501.01234"); old-style ids
    (e.g. "math/0501001") keep their slash form -- only the trailing "vN" is
    stripped, regardless of id style.
  - created: the date part of <published> (both OAI's <created> and Atom's
    <published> are the first-version submission date).
  - datestamp: the date part of <updated> (D1's redefinition -- narrower than the
    OAI route's header datestamp: paper-version updates, not any metadata touch).
  - primary category: the explicit `arxiv:primary_category` attribute (stronger
    than the OAI-PMH route's first-`<category>`-wins convention).
  - abstract: the entry's <summary> text.

Everything downstream of that mapping is UNCHANGED from filter_corpus.py (the OAI
route's script, left untouched per the round-3 instruction) and several small pure
helpers are imported from it directly rather than re-implemented, so the two routes'
corpus rules cannot silently drift apart: TARGET_STRATA, MIN_TOKENS, DATE_MIN,
DATE_MAX, half_year_unit(), in_date_range(), sha256_file(), contamination_ceiling()
(D1: "share of pre-2023-created records whose latest version date is >= 2023-01-01" --
arithmetically identical to the OAI version's contamination_ceiling(), only the
`datestamp` field's PROVENANCE differs, which this module supplies).

Input layout expected (as produced by harvest_api.py): `--raw-dir/<stratum>/<unit>/*.xml.gz`.
Note `cat:` matched any-listing when harvesting (like OAI's `set=` did) -- the
directory a raw chunk lives under is NOT authoritative for stratum membership; the
per-entry `arxiv:primary_category` is, exactly as it was for OAI's `<categories>`
first-entry. A chunk fetched under the cs.CV query can (and does) legitimately
contain zero cs.CV-primary entries if every hit was actually cross-listed with a
different primary category.

§10 amendment D1a (deep-paging split): a (stratum, unit) whose own totalResults
exceeded harvest_api.py's monthly-split threshold was re-fetched as 6 calendar-month
queries, chunked as `<YYYYMM>-<page:05d>.xml.gz` instead of the plain `<page:05d>.xml.gz`
naming unsplit units use. This module's file discovery (iter_raw_files, below) globs
every `*.xml.gz` under a unit directory regardless of which naming pattern produced it
-- it never inspects or relies on the chunk filename's shape, only its content -- so
BOTH naming schemes are read identically and no adjustment was needed here. (A single
unit directory will only ever contain one naming scheme in practice, since D1a discards
the unit-level probe page entirely on a split rather than mixing it with monthly
chunks -- but nothing below assumes that either.) D1a is explicit that unit assignment
always comes from each record's own `<published>` date, never from the query window
(unit-level or monthly) that happened to fetch it -- this module already worked that
way for D1's unit-level-only case, so D1a requires no change to the filtering logic,
only to file discovery's tolerance of the new filename shape (confirmed above).

Dedup: by id, across ALL raw files (any stratum, any unit, any page) -- a
cross-listed paper can appear under more than one stratum's query. First occurrence
wins; traversal order is fully sorted (stratum name, then unit label, then filename)
so "first occurrence" is a deterministic function of the input files' content, not of
OS directory-listing order.

Outputs, all under --outdir (same shape as filter_corpus.py's, so metrics.py and
envelope.py run unmodified against either route's corpus):
  - `<stratum>.jsonl`: one line per kept record, {id, created, datestamp, unit, abstract}.
  - `counts.json`: {"cells": per stratum x unit {kept, excluded_short},
    "contamination_ceiling": per stratum, the D1 bounding statistic}.
  - `manifest.json`: sha256 of every input raw chunk and every output file this run
    produced.
"""
import argparse
import gzip
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tokenizer import tokenize  # noqa: E402
from filter_corpus import (  # noqa: E402
    TARGET_STRATA,
    MIN_TOKENS,
    DATE_MIN,
    DATE_MAX,
    half_year_unit,
    in_date_range,
    sha256_file,
    contamination_ceiling,
)

ATOM_NS = "http://www.w3.org/2005/Atom"
ARXIV_ATOM_NS = "http://arxiv.org/schemas/atom"

_ID_URL_RE = re.compile(r"arxiv\.org/abs/(.+)$")
_VERSION_SUFFIX_RE = re.compile(r"v\d+$")


def extract_id(id_url):
    """'http://arxiv.org/abs/2501.01234v2' -> '2501.01234'.
    'http://arxiv.org/abs/math/0501001v1' -> 'math/0501001' (old-style ids keep the
    slash form; only the trailing version suffix is stripped)."""
    m = _ID_URL_RE.search(id_url or "")
    if not m:
        return None
    id_part = m.group(1)
    return _VERSION_SUFFIX_RE.sub("", id_part)


def iter_raw_files(raw_dir, strata=TARGET_STRATA):
    """Sorted traversal: stratum dir, then unit dir, then page filename -- this
    fixed order is what makes dedup's "first occurrence wins" deterministic."""
    for stratum in sorted(strata):
        stratum_dir = os.path.join(raw_dir, stratum)
        if not os.path.isdir(stratum_dir):
            continue
        for unit in sorted(os.listdir(stratum_dir)):
            unit_dir = os.path.join(stratum_dir, unit)
            if not os.path.isdir(unit_dir):
                continue
            for name in sorted(os.listdir(unit_dir)):
                if name.endswith(".xml.gz"):
                    yield stratum, unit, os.path.join(unit_dir, name)


def parse_entries(gz_path):
    """Yield dicts {id, created, datestamp, primary_category, abstract} for each
    <entry> in the gzipped Atom response at gz_path. Entries missing any required
    field, or whose <id> doesn't parse to a usable arXiv id, are skipped."""
    with gzip.open(gz_path, "rb") as f:
        data = f.read()
    root = ET.fromstring(data)
    for entry in root.findall(f"{{{ATOM_NS}}}entry"):
        id_el = entry.find(f"{{{ATOM_NS}}}id")
        published_el = entry.find(f"{{{ATOM_NS}}}published")
        updated_el = entry.find(f"{{{ATOM_NS}}}updated")
        summary_el = entry.find(f"{{{ATOM_NS}}}summary")
        primary_el = entry.find(f"{{{ARXIV_ATOM_NS}}}primary_category")
        if id_el is None or published_el is None or updated_el is None or summary_el is None or primary_el is None:
            continue
        id_clean = extract_id((id_el.text or "").strip())
        if not id_clean:
            continue
        published = (published_el.text or "").strip()
        updated = (updated_el.text or "").strip()
        if len(published) < 10 or len(updated) < 10:
            continue
        yield {
            "id": id_clean,
            "created": published[:10],
            "datestamp": updated[:10],
            "primary_category": (primary_el.get("term") or "").strip(),
            "abstract": (summary_el.text or "").strip(),
        }


def filter_corpus_api(raw_dir, outdir, strata=TARGET_STRATA):
    os.makedirs(outdir, exist_ok=True)

    input_hashes = {}
    seen_ids = set()
    kept_by_stratum = {s: [] for s in strata}
    counts = {s: {} for s in strata}  # stratum -> unit -> {kept, excluded_short}

    def bump(stratum, unit, key):
        cell = counts[stratum].setdefault(unit, {"kept": 0, "excluded_short": 0})
        cell[key] += 1

    for _query_stratum, _query_unit, path in iter_raw_files(raw_dir, strata):
        rel = os.path.relpath(path, raw_dir)
        input_hashes[rel] = sha256_file(path)
        for rec in parse_entries(path):
            rid = rec["id"]
            if not rid or rid in seen_ids:
                continue
            primary = rec["primary_category"]
            if primary not in strata:
                continue
            created = rec["created"]
            if not created or not in_date_range(created):
                continue
            seen_ids.add(rid)
            unit = half_year_unit(created)
            tokens = tokenize(rec["abstract"])
            if len(tokens) < MIN_TOKENS:
                bump(primary, unit, "excluded_short")
                continue
            bump(primary, unit, "kept")
            kept_by_stratum[primary].append({
                "id": rid,
                "created": created,
                "datestamp": rec["datestamp"],
                "unit": unit,
                "abstract": rec["abstract"],
            })

    output_hashes = {}
    contamination = {}
    for stratum in strata:
        rows = sorted(kept_by_stratum[stratum], key=lambda r: (r["unit"], r["id"]))
        contamination[stratum] = contamination_ceiling(rows)
        out_path = os.path.join(outdir, f"{stratum}.jsonl")
        with open(out_path, "w", encoding="utf-8") as f:
            for row in rows:
                f.write(json.dumps(row, sort_keys=True) + "\n")
        output_hashes[f"{stratum}.jsonl"] = sha256_file(out_path)

    counts_path = os.path.join(outdir, "counts.json")
    with open(counts_path, "w", encoding="utf-8") as f:
        json.dump({"cells": counts, "contamination_ceiling": contamination}, f, indent=2, sort_keys=True)
    output_hashes["counts.json"] = sha256_file(counts_path)

    manifest = {
        "raw_dir": os.path.abspath(raw_dir),
        "outdir": os.path.abspath(outdir),
        "route": "query-api (PREREGISTRATION.md §10 deviation D1)",
        "min_tokens": MIN_TOKENS,
        "date_range": [DATE_MIN, DATE_MAX],
        "target_strata": list(strata),
        "input_sha256": input_hashes,
        "output_sha256": output_hashes,
    }
    manifest_path = os.path.join(outdir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)

    return counts


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Apply PREREGISTRATION.md §2 corpus rules (D1 query-API route) to raw Atom chunks."
    )
    parser.add_argument("--raw-dir", required=True, help="Directory with <stratum>/<unit>/*.xml.gz (harvest_api.py output).")
    parser.add_argument("--outdir", required=True, help="Directory to write per-stratum JSONL + counts + manifest.")
    args = parser.parse_args(argv)

    counts = filter_corpus_api(args.raw_dir, args.outdir)
    total_kept = sum(cell["kept"] for stratum in counts for cell in counts[stratum].values())
    print(f"kept {total_kept} records across {len(counts)} strata; wrote to {args.outdir}")


if __name__ == "__main__":
    main()
