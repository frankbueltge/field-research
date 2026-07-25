"""
scripts/filter_corpus.py — PREREGISTRATION.md §2 corpus rules, applied to raw OAI-PMH
ListRecords chunks (harvest.py output). Stdlib only (xml.etree, gzip, json, hashlib).

Input layout expected (as produced by harvest.py): `--raw-dir/<set>/*.xml.gz`, one gzip
member per OAI-PMH HTTP response, for sets "cs" and "math".

Rules applied per record (§2):
  - Deleted records (header status="deleted") are skipped.
  - Stratum membership: primary category (first whitespace-separated token of
    `<categories>`) is exactly one of cs.CL, cs.CV, math.NT. Mutually exclusive by
    construction.
  - Dating: `<created>` (first-version submission date) in 2015-01-01..2026-06-30
    inclusive.
  - Records are deduplicated by arXiv id across input files/sets (a record can appear
    in both the "cs" and "math" OAI sets if cross-listed; first occurrence wins — the
    metadata content for a given id is identical regardless of which set surfaced it).
  - Tokenizer: scripts/tokenizer.py, fixed. Abstracts with fewer than 50 tokens are
    excluded ("excluded_short") and counted per (stratum, unit) cell.
  - Unit: calendar half-year of `<created>`, e.g. "2015H1", "2015H2".

Outputs, all under --outdir:
  - `<stratum>.jsonl`: one line per kept record, {id, created, datestamp, unit, abstract}.
    (datestamp is the OAI header's <datestamp> -- last metadata touch -- kept ONLY to
    compute the §2 contamination ceiling below; it never enters any metric.)
  - `counts.json`: {"cells": per stratum x unit {kept, excluded_short},
    "contamination_ceiling": per stratum, the §2 bounding statistic -- among this
    stratum's KEPT records with created < 2023-01-01, the share whose datestamp is
    >= 2023-01-01 (metadata touched post-launch, for any reason). This is the harvest's
    free upper bound on pre-2023 envelope contamination by post-launch-revised text.
  - `manifest.json`: sha256 of every input raw chunk and every output file this run
    produced.
"""
import argparse
import gzip
import hashlib
import json
import os
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tokenizer import tokenize  # noqa: E402

OAI_NS = "http://www.openarchives.org/OAI/2.0/"
ARXIV_NS = "http://arxiv.org/OAI/arXiv/"

TARGET_STRATA = ("cs.CL", "cs.CV", "math.NT")
MIN_TOKENS = 50
DATE_MIN = "2015-01-01"
DATE_MAX = "2026-06-30"


def half_year_unit(created):
    """created: 'YYYY-MM-DD' -> 'YYYYH1' or 'YYYYH2'."""
    year = created[0:4]
    month = int(created[5:7])
    half = "H1" if month <= 6 else "H2"
    return f"{year}{half}"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def iter_raw_files(raw_dir, sets):
    for set_name in sets:
        set_dir = os.path.join(raw_dir, set_name)
        if not os.path.isdir(set_dir):
            continue
        for name in sorted(os.listdir(set_dir)):
            if name.endswith(".xml.gz"):
                yield set_name, os.path.join(set_dir, name)


def parse_records(gz_path):
    """Yield dicts {id, categories, created, datestamp, abstract} for each <record> in
    the gzipped OAI-PMH response at gz_path. `datestamp` is the OAI header's
    <datestamp> (last metadata touch), captured for the §2 contamination ceiling."""
    with gzip.open(gz_path, "rb") as f:
        data = f.read()
    root = ET.fromstring(data)
    list_records = root.find(f"{{{OAI_NS}}}ListRecords")
    if list_records is None:
        return
    for record in list_records.findall(f"{{{OAI_NS}}}record"):
        header = record.find(f"{{{OAI_NS}}}header")
        if header is not None and header.get("status") == "deleted":
            continue
        datestamp_el = header.find(f"{{{OAI_NS}}}datestamp") if header is not None else None
        metadata = record.find(f"{{{OAI_NS}}}metadata")
        if metadata is None:
            continue
        arxiv = metadata.find(f"{{{ARXIV_NS}}}arXiv")
        if arxiv is None:
            continue
        id_el = arxiv.find(f"{{{ARXIV_NS}}}id")
        created_el = arxiv.find(f"{{{ARXIV_NS}}}created")
        categories_el = arxiv.find(f"{{{ARXIV_NS}}}categories")
        abstract_el = arxiv.find(f"{{{ARXIV_NS}}}abstract")
        if id_el is None or created_el is None or categories_el is None or abstract_el is None:
            continue
        yield {
            "id": (id_el.text or "").strip(),
            "categories": (categories_el.text or "").strip(),
            "created": (created_el.text or "").strip(),
            "datestamp": (datestamp_el.text or "").strip() if datestamp_el is not None else "",
            "abstract": (abstract_el.text or "").strip(),
        }


def primary_category(categories):
    if not categories:
        return None
    return categories.split()[0]


def in_date_range(created):
    return DATE_MIN <= created <= DATE_MAX


CONTAMINATION_CUTOFF = "2023-01-01"


def contamination_ceiling(rows):
    """§2 bounding statistic: among KEPT rows with created < 2023-01-01, the share
    whose datestamp is >= 2023-01-01 (metadata touched post-launch, for any reason).
    Returns a dict; share is None if there are no pre-2023 kept rows."""
    pre2023 = [r for r in rows if r["created"] < CONTAMINATION_CUTOFF]
    touched_post_launch = [r for r in pre2023 if r["datestamp"] >= CONTAMINATION_CUTOFF]
    n_pre2023 = len(pre2023)
    n_touched = len(touched_post_launch)
    share = (n_touched / n_pre2023) if n_pre2023 > 0 else None
    return {
        "pre2023_kept_count": n_pre2023,
        "pre2023_datestamp_post2023_count": n_touched,
        "share": share,
    }


def filter_corpus(raw_dir, outdir, sets=("cs", "math")):
    os.makedirs(outdir, exist_ok=True)

    input_hashes = {}
    seen_ids = set()
    kept_by_stratum = {s: [] for s in TARGET_STRATA}
    counts = {s: {} for s in TARGET_STRATA}  # stratum -> unit -> {kept, excluded_short}

    def bump(stratum, unit, key):
        cell = counts[stratum].setdefault(unit, {"kept": 0, "excluded_short": 0})
        cell[key] += 1

    for set_name, path in iter_raw_files(raw_dir, sets):
        rel = os.path.relpath(path, raw_dir)
        input_hashes[rel] = sha256_file(path)
        for rec in parse_records(path):
            rid = rec["id"]
            if not rid or rid in seen_ids:
                continue
            primary = primary_category(rec["categories"])
            if primary not in TARGET_STRATA:
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
    for stratum in TARGET_STRATA:
        # Deterministic order: sort by (unit, id).
        rows = sorted(kept_by_stratum[stratum], key=lambda r: (r["unit"], r["id"]))
        contamination[stratum] = contamination_ceiling(rows)
        out_path = os.path.join(outdir, f"{stratum}.jsonl")
        with open(out_path, "w", encoding="utf-8") as f:
            for row in rows:
                # datestamp is provenance-only: never enters any metric downstream.
                f.write(json.dumps(row, sort_keys=True) + "\n")
        output_hashes[f"{stratum}.jsonl"] = sha256_file(out_path)

    counts_path = os.path.join(outdir, "counts.json")
    with open(counts_path, "w", encoding="utf-8") as f:
        json.dump({"cells": counts, "contamination_ceiling": contamination}, f, indent=2, sort_keys=True)
    output_hashes["counts.json"] = sha256_file(counts_path)

    manifest = {
        "raw_dir": os.path.abspath(raw_dir),
        "outdir": os.path.abspath(outdir),
        "min_tokens": MIN_TOKENS,
        "date_range": [DATE_MIN, DATE_MAX],
        "target_strata": list(TARGET_STRATA),
        "input_sha256": input_hashes,
        "output_sha256": output_hashes,
    }
    manifest_path = os.path.join(outdir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)

    return counts


def main(argv=None):
    parser = argparse.ArgumentParser(description="Apply PREREGISTRATION.md §2 corpus rules to raw OAI-PMH chunks.")
    parser.add_argument("--raw-dir", required=True, help="Directory with <set>/*.xml.gz (harvest.py output).")
    parser.add_argument("--outdir", required=True, help="Directory to write per-stratum JSONL + counts + manifest.")
    parser.add_argument("--sets", nargs="+", default=["cs", "math"], help="Set subdirectories to read.")
    args = parser.parse_args(argv)

    counts = filter_corpus(args.raw_dir, args.outdir, tuple(args.sets))
    total_kept = sum(cell["kept"] for stratum in counts for cell in counts[stratum].values())
    print(f"kept {total_kept} records across {len(counts)} strata; wrote to {args.outdir}")


if __name__ == "__main__":
    main()
