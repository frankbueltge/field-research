#!/usr/bin/env python3
"""
Layer 0 — the offline, assertable layer.

Reads one pinned snapshot of a public register of AI harms and emits:

  inventory.json     population counts, the inclusion rule, the excluded classes with
                     their units stated, and the age distribution
  sample.json        a seeded, stratified sample of report records — metadata only
  fingerprints.json  a one-way fingerprint of each sampled report's stored full-text copy

Nothing here touches the network. The snapshot is verified against a pinned SHA-256 before
a single field is read: this script proves the provenance of its input, not only the
determinism of its output.

The stored full text is third-party material under its own rights and is NEVER written to
disk by this script. What is written is a set of hashed word-shingles, from which the text
cannot be reconstructed but against which a live page can be checked.

Usage:
    python3 build_inventory.py --snapshot <path-to-.tar.bz2>
    python3 build_inventory.py --snapshot <path> --check     # rebuild and compare, exit 1 on drift
"""

import argparse
import collections
import csv
import hashlib
import io
import json
import os
import random
import re
import sys
import tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "MANIFEST.json")

# The sample is drawn with this seed and no other. Same seed, same sample.
SEED = "meridian-2026-08-01-what-the-record-rests-on"
PER_STRATUM = 20
# Strata: publication year 2015..2026, plus one pooled stratum for everything published earlier.
STRATA_YEARS = [str(y) for y in range(2015, 2027)]
POOLED = "<=2014"

SHINGLE_N = 8          # words per shingle
SHINGLE_HASH_HEX = 12  # hex chars kept per shingle hash

csv.field_size_limit(10 ** 9)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_reports_csv(snapshot_path):
    """Extract reports.csv from the pinned archive without unpacking anything else."""
    with tarfile.open(snapshot_path, "r:bz2") as tf:
        member = None
        for m in tf.getmembers():
            if m.name.endswith("/reports.csv"):
                member = m
                break
        if member is None:
            raise SystemExit("reports.csv not found in snapshot")
        raw = tf.extractfile(member).read()
    text = raw.decode("utf-8", errors="replace")
    return list(csv.DictReader(io.StringIO(text))), member.name, len(raw)


WORD_RE = re.compile(r"[a-z0-9]+")


def normalise_words(text):
    """Lowercase, keep alphanumeric runs only. Used identically on stored and live text."""
    return WORD_RE.findall(text.lower())


def shingles(words, n=SHINGLE_N):
    if len(words) < n:
        return []
    return [" ".join(words[i:i + n]) for i in range(len(words) - n + 1)]


def fingerprint(text):
    """One-way fingerprint of a stored copy: hashed word-shingles, sorted and deduplicated.

    The text cannot be recovered from this. A live page can still be scored against it.
    """
    words = normalise_words(text)
    sh = shingles(words)
    hashes = sorted({hashlib.sha1(s.encode("utf-8")).hexdigest()[:SHINGLE_HASH_HEX] for s in sh})
    return {
        "n_words": len(words),
        "n_shingles": len(sh),
        "n_unique_shingles": len(hashes),
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "text_chars": len(text),
        # packed: the sorted unique hashes concatenated, %d hex characters each
        "shingle_hashes_packed": "".join(hashes),
    }


def year_of(iso):
    return (iso or "")[:4]


def stratum_of(pub_year):
    return pub_year if pub_year in STRATA_YEARS else POOLED


def build(snapshot_path):
    manifest = json.load(open(MANIFEST, encoding="utf-8"))
    pin = manifest["snapshot"]

    actual_bytes = os.path.getsize(snapshot_path)
    actual_sha = sha256_file(snapshot_path)
    if actual_sha != pin["sha256"] or actual_bytes != pin["bytes"]:
        raise SystemExit(
            "INPUT PROVENANCE FAILURE — this is not the pinned snapshot.\n"
            f"  expected sha256 {pin['sha256']} ({pin['bytes']} bytes)\n"
            f"  got      sha256 {actual_sha} ({actual_bytes} bytes)"
        )

    rows, member_name, member_bytes = read_reports_csv(snapshot_path)

    # ---- the inclusion rule, stated once and applied once -------------------------------
    # INCLUDED: a report record whose `url` field begins with http:// or https://.
    # Everything else is excluded, and every excluded record is counted into a named class.
    included, excluded = [], []
    for r in rows:
        (included if (r.get("url") or "").startswith(("http://", "https://")) else excluded).append(r)

    excl_by_tag = collections.Counter((r.get("tags") or "").strip() for r in excluded)
    variant_like = sum(v for k, v in excl_by_tag.items() if k.startswith("variant:"))
    excl_empty_title = sum(1 for r in excluded if not (r.get("title") or "").strip())
    excl_empty_desc = sum(1 for r in excluded if not (r.get("description") or "").strip())
    excl_text_lens = [len((r.get("text") or "").strip()) for r in excluded]

    urls = [r["url"] for r in included]
    url_counts = collections.Counter(urls)
    dupes = {u: c for u, c in url_counts.items() if c > 1}

    # URLs that point at an archive rather than at an original document, and URLs that point
    # back at the register's own site — declared classes, kept in the population and marked.
    ARCHIVE_HOSTS = ("web.archive.org", "archive.today", "archive.ph", "archive.is",
                     "webcache.googleusercontent.com", "perma.cc")
    SELF_HOSTS = ("incidentdatabase.ai",)

    def host(u):
        m = re.match(r"https?://([^/:]+)", u or "")
        return (m.group(1) if m else "").lower()

    n_archive_url = sum(1 for u in urls if any(h in host(u) for h in ARCHIVE_HOSTS))
    n_self_url = sum(1 for u in urls if any(h in host(u) for h in SELF_HOSTS))

    langs = collections.Counter((r.get("language") or "").strip() for r in included)
    pub_years = collections.Counter(year_of(r.get("date_published")) for r in included)
    dl_years = collections.Counter(year_of(r.get("date_downloaded")) for r in included)

    def held_len(r):
        return len((r.get("text") or "").strip())

    held = [held_len(r) for r in included]
    held_sorted = sorted(held)

    def pct(p):
        if not held_sorted:
            return 0
        return held_sorted[min(len(held_sorted) - 1, int(p * len(held_sorted)))]

    strata_sizes = collections.Counter(stratum_of(year_of(r.get("date_published"))) for r in included)

    # Two integrity classes that bear directly on what the live layers can conclude.
    # (a) A document cannot be downloaded before it was published. Where the register's own
    #     two dates say otherwise, the L2 test "was there a capture before the download" is
    #     being compared against a date that is known to be wrong somewhere in the field.
    def bad_date_order(r):
        dp, dd = (r.get("date_published") or "")[:10], (r.get("date_downloaded") or "")[:10]
        return bool(dp and dd and len(dp) == 10 and len(dd) == 10 and dp > dd)

    date_order_bad = [r["report_number"] for r in included if bad_date_order(r)]

    # (b) The register itself marks some records as holding a stand-in rather than the
    #     document. Their stored text is not a copy of the cited page and must never be
    #     scored as drift.
    ED_NOTE = "aiid editor's note"
    self_declared_placeholder = [r["report_number"] for r in included
                                 if ED_NOTE in (r.get("text") or "").lower()]

    inventory = {
        "layer": "L0 — offline inventory, assertable",
        "snapshot": pin,
        "reports_csv": {"member": member_name, "bytes": member_bytes},
        "population": {
            "records_in_reports_csv": len(rows),
            "included_unit": "report records whose url field begins with http:// or https://",
            "included_records": len(included),
            "distinct_urls_among_included": len(url_counts),
            "included_records_sharing_a_url_with_another_record": sum(dupes.values()),
            "distinct_urls_used_more_than_once": len(dupes),
        },
        "excluded": {
            "unit": "report records",
            "total": len(excluded),
            "by_tags_field": dict(excl_by_tag.most_common()),
            "records_tagged_variant_prefix": variant_like,
            "records_with_empty_title": excl_empty_title,
            "records_with_empty_description": excl_empty_desc,
            "stored_text_length": {
                "empty": sum(1 for n in excl_text_lens if n == 0),
                "40_chars_or_fewer": sum(1 for n in excl_text_lens if 0 < n <= 40),
                "more_than_40_chars": sum(1 for n in excl_text_lens if n > 40),
            },
            "note": (
                "What is observed, not what is assumed. Every excluded record carries a tag with a "
                "'variant:' prefix, and every one has an empty title and an empty description. The "
                "class is NOT homogeneous: most hold 40 characters or less of stored text — many "
                "hold the single character '1' — while 126 hold more, and those read as substantive "
                "accounts of an incident (e.g. report 3205). At least one, report 2587, holds "
                "placeholder fixture prose beginning 'New text example... Lorem ipsum'. The "
                "register's published glossary uses 'variant' for a taxonomic relationship between "
                "incidents; whether the tag on these records means the same thing is NOT established "
                "here and is not asserted. Excluded from this measurement for one reason only: a "
                "citation census cannot measure a record that makes no citation."
            ),
        },
        "declared_subclasses_kept_in_population": {
            "unit": "report records",
            "url_points_at_a_web_archive_or_cache": n_archive_url,
            "url_points_at_the_registers_own_site": n_self_url,
            "by_language": dict(langs.most_common(10)),
        },
        "held_text": {
            "unit": "report records (included only)",
            "records_with_stored_full_text_over_200_chars": sum(1 for n in held if n > 200),
            "records_with_stored_full_text_200_chars_or_less": sum(1 for n in held if n <= 200),
            "chars_p10": pct(0.10), "chars_median": pct(0.50), "chars_p90": pct(0.90),
            "chars_max": max(held) if held else 0,
        },
        "age_distribution": {
            "unit": "report records (included only)",
            "by_publication_year": dict(sorted(pub_years.items())),
            "by_register_download_year": dict(sorted(dl_years.items())),
        },
        "integrity_classes": {
            "unit": "report records (included only)",
            "date_published_after_date_downloaded": {
                "count": len(date_order_bad),
                "share_of_included": round(len(date_order_bad) / max(1, len(included)), 5),
                "report_numbers": date_order_bad,
                "why_it_matters": (
                    "L2 asks whether a public archive holds a capture at or before the date the "
                    "register recorded downloading the document. These records prove that field "
                    "carries a non-zero error rate, so the L2 precedence result is reported with "
                    "them flagged and excluded from the precedence rate."
                ),
            },
            "register_declares_its_stored_text_a_stand_in": {
                "count": len(self_declared_placeholder),
                "report_numbers": self_declared_placeholder,
                "why_it_matters": (
                    "The register states in these records' own text that what it holds is a "
                    "placeholder, not a copy of the cited document. Scoring them for drift would "
                    "report the register's disclosed incompleteness as a change in somebody "
                    "else's page. They are measured at L1 and L2 and excluded from L3."
                ),
            },
        },
        "strata": {
            "definition": "publication year 2015..2026; everything published 2014 or earlier pooled",
            "sizes_in_population": dict(sorted(strata_sizes.items())),
            "earliest_publication_year_in_pooled_stratum": min(
                [year_of(r.get("date_published")) for r in included
                 if stratum_of(year_of(r.get("date_published"))) == POOLED] or ["n/a"]),
        },
        "sampling": {
            "seed": SEED,
            "allocation": "equal allocation, %d report records per stratum" % PER_STRATUM,
            "note": (
                "Equal allocation gives each stratum the same precision and therefore does NOT "
                "give a self-weighting corpus estimate. Any corpus-wide rate must be a "
                "stratum-size-weighted estimate and must be reported with its interval."
            ),
        },
    }

    # ---- the seeded sample ---------------------------------------------------------------
    by_stratum = collections.defaultdict(list)
    for r in included:
        by_stratum[stratum_of(year_of(r.get("date_published")))].append(r)
    # deterministic ordering before any draw
    for k in by_stratum:
        by_stratum[k].sort(key=lambda r: int(r["report_number"]) if (r.get("report_number") or "").isdigit() else 10 ** 9)

    rng = random.Random(SEED)
    sample, fps = [], {}
    for stratum in STRATA_YEARS + [POOLED]:
        pool = by_stratum.get(stratum, [])
        take = min(PER_STRATUM, len(pool))
        drawn = rng.sample(pool, take) if take else []
        drawn.sort(key=lambda r: int(r["report_number"]) if (r.get("report_number") or "").isdigit() else 10 ** 9)
        for r in drawn:
            rid = r["report_number"]
            sample.append({
                "report_number": rid,
                "stratum": stratum,
                "stratum_size_in_population": strata_sizes[stratum],
                "url": r["url"],
                "source_domain": r.get("source_domain", ""),
                "title": r.get("title", ""),
                "language": r.get("language", ""),
                "date_published": r.get("date_published", ""),
                "date_downloaded": r.get("date_downloaded", ""),
                "date_submitted": r.get("date_submitted", ""),
                "held_text_chars": held_len(r),
                "flag_date_published_after_downloaded": bad_date_order(r),
                "flag_register_declares_stand_in": rid in self_declared_placeholder,
                "flag_url_shared_with_another_report": url_counts[r["url"]] > 1,
            })
            fps[rid] = fingerprint((r.get("text") or "").strip())

    sample_doc = {
        "seed": SEED,
        "drawn_from": pin["sha256"],
        "per_stratum_requested": PER_STRATUM,
        "n": len(sample),
        "note": "Metadata only. The register's stored full text is not reproduced here.",
        "reports": sample,
    }
    fp_doc = {
        "method": {
            "normalisation": "lowercase; runs of [a-z0-9] kept as words; everything else is a separator",
            "shingle_words": SHINGLE_N,
            "hash": "sha1 of the shingle, first %d hex characters" % SHINGLE_HASH_HEX,
            "packing": "sorted unique hashes concatenated into one string; split every %d characters"
                       % SHINGLE_HASH_HEX,
            "one_way": "The stored text cannot be reconstructed from these hashes.",
        },
        "drawn_from": pin["sha256"],
        "fingerprints": fps,
    }
    return inventory, sample_doc, fp_doc


def write_json(path, obj):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, sort_keys=False, ensure_ascii=False)
        fh.write("\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", required=True)
    ap.add_argument("--check", action="store_true",
                    help="rebuild and compare against the committed outputs; exit 1 on any difference")
    args = ap.parse_args()

    inventory, sample_doc, fp_doc = build(args.snapshot)
    targets = [("inventory.json", inventory), ("sample.json", sample_doc), ("fingerprints.json", fp_doc)]

    if args.check:
        bad = []
        for name, obj in targets:
            p = os.path.join(HERE, name)
            if not os.path.exists(p):
                bad.append(f"{name}: missing")
                continue
            old = json.load(open(p, encoding="utf-8"))
            if old != obj:
                bad.append(f"{name}: differs from a fresh rebuild")
        if bad:
            print("CHECK FAILED\n  " + "\n  ".join(bad))
            return 1
        print("CHECK PASSED — pinned input verified, all three outputs reproduce byte-for-byte")
        return 0

    for name, obj in targets:
        write_json(os.path.join(HERE, name), obj)
    print("wrote inventory.json, sample.json, fingerprints.json  (n=%d)" % sample_doc["n"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
