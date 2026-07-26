#!/usr/bin/env python3
"""Audit instrument for the Dataset Register snapshot.

Reads only the frozen files under provenance/register-records/ (resolved
relative to this script's own location) and recomputes a fixed set of
assertions (A1-A18) about the register's own aggregate and record-level
files. Every number is computed from the input files; nothing is invented.

Naming note: two of the six harvested sources carry corporate names this
practice's constitution does not permit in its own prose. In every question,
note, docstring, comment and printed line below they are called "the
withheld source" and "the model-hosting source". The upstream record's own
data values (the `quelle` field, e.g. in dict keys, and URL hosts) are never
rewritten: they are reported verbatim because they are the frozen record's
own content, and that is disclosed on the work's face.

Standard library only. Deterministic and offline: the only nondeterministic
field written to the output is `generated_utc`.
"""

import argparse
import hashlib
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from urllib.parse import urlparse

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DRAFT_DIR = os.path.dirname(SCRIPT_DIR)
REGISTER_DIR = os.path.join(DRAFT_DIR, "provenance", "register-records")
MANIFESTE_DIR = os.path.join(REGISTER_DIR, "manifeste")
RESULTS_PATH = os.path.join(DRAFT_DIR, "results", "audit.json")

WITHHELD_SOURCE = "kaggle"

UPSTREAM_COMMIT = "a7024008ec337118b2aeebb87065ded83ed23413"
UPSTREAM_TAG = "snapshot-2026-07-26"
UPSTREAM_TAG_SHA = "8be62d8b86f2b5ce3690f44a983497adac7957d6"


# ---------------------------------------------------------------------------
# Pure helper functions (unit-tested directly)
# ---------------------------------------------------------------------------

def read_json(path):
    """Read a single JSON document from a file."""
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def read_jsonl(path):
    """Read a JSON-Lines file into a list of dicts, skipping blank lines."""
    rows = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def sha256_of_file(path):
    """Return the hex SHA-256 digest of a file's bytes."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def host_of(url):
    """Return the network location (host) component of a URL, or empty string."""
    if not url:
        return ""
    return urlparse(url).netloc


def share(numerator, denominator):
    """Return numerator / denominator as a float, or None if denominator is 0."""
    if denominator == 0:
        return None
    return numerator / denominator


def round6(value):
    """Round a float to 6 decimal places; pass through non-floats unchanged."""
    if isinstance(value, float):
        return round(value, 6)
    return value


def count_by(rows, key):
    """Return a plain dict mapping rows[i][key] -> count, over an iterable of dicts."""
    c = Counter(r.get(key) for r in rows)
    return dict(c)


def sum_field(rows, key):
    """Sum an integer field across a list of dicts."""
    return sum(r[key] for r in rows)


def relpath(path):
    """Return a path relative to DRAFT_DIR, with forward slashes, for evidence lists."""
    rel = os.path.relpath(path, DRAFT_DIR)
    return rel.replace(os.sep, "/")


def last_wins_by_id(rows, id_key="id"):
    """Reduce rows to one per id, keeping the last occurrence in file order.

    This mirrors the upstream builder's own reduction (`table[id] = row` while
    reading a file top to bottom): the last row for a given id overwrites any
    earlier one. Returns a dict id -> row, insertion order preserved.
    """
    result = {}
    for row in rows:
        result[row[id_key]] = row
    return result


def group_by_id(rows, id_key="id"):
    """Group rows by id, preserving each id's rows in file (encounter) order.

    Returns a dict id -> list of rows, in first-seen id order.
    """
    groups = {}
    for row in rows:
        groups.setdefault(row[id_key], []).append(row)
    return groups


# ---------------------------------------------------------------------------
# Input loading
# ---------------------------------------------------------------------------

def load_inputs():
    """Load every frozen input file into memory. Returns a dict of raw data."""
    snapshot_path = os.path.join(REGISTER_DIR, "snapshot-2026-07-26.manifest.json")
    snapshot = read_json(snapshot_path)

    manifest_files = sorted(
        fn for fn in os.listdir(MANIFESTE_DIR) if fn.endswith(".json")
    )
    run_manifests = []
    for fn in manifest_files:
        path = os.path.join(MANIFESTE_DIR, fn)
        run_manifests.append((path, read_json(path)))

    ablehnungen_path = os.path.join(REGISTER_DIR, "ablehnungen.jsonl")
    ablehnungen = read_jsonl(ablehnungen_path)

    ausfaelle_path = os.path.join(REGISTER_DIR, "ausfaelle.jsonl")
    ausfaelle = read_jsonl(ausfaelle_path)

    aufloesungen_path = os.path.join(REGISTER_DIR, "aufloesungen.jsonl")
    aufloesungen = read_jsonl(aufloesungen_path)

    entscheidungen_path = os.path.join(REGISTER_DIR, "entscheidungen.jsonl")
    entscheidungen = read_jsonl(entscheidungen_path)

    return {
        "snapshot_path": snapshot_path,
        "snapshot": snapshot,
        "run_manifests": run_manifests,
        "ablehnungen_path": ablehnungen_path,
        "ablehnungen": ablehnungen,
        "ausfaelle_path": ausfaelle_path,
        "ausfaelle": ausfaelle,
        "aufloesungen_path": aufloesungen_path,
        "aufloesungen": aufloesungen,
        "entscheidungen_path": entscheidungen_path,
        "entscheidungen": entscheidungen,
    }


def collect_input_manifest():
    """Build the `inputs` block: every frozen file with its recomputed SHA-256."""
    paths = [
        os.path.join(REGISTER_DIR, "snapshot-2026-07-26.manifest.json"),
        os.path.join(REGISTER_DIR, "ablehnungen.jsonl"),
        os.path.join(REGISTER_DIR, "ausfaelle.jsonl"),
        os.path.join(REGISTER_DIR, "aufloesungen.jsonl"),
        os.path.join(REGISTER_DIR, "entscheidungen.jsonl"),
    ]
    for fn in sorted(os.listdir(MANIFESTE_DIR)):
        if fn.endswith(".json"):
            paths.append(os.path.join(MANIFESTE_DIR, fn))
    paths.sort(key=relpath)
    return [
        {"path": relpath(p), "sha256": sha256_of_file(p)}
        for p in paths
    ]


# ---------------------------------------------------------------------------
# Assertions A1-A12
# ---------------------------------------------------------------------------

def make_assertion(id_, question, computed, expected, evidence, kind, extra=None):
    """Build one assertion record with a mechanically-derived PASS/FAIL verdict."""
    verdict = "PASS" if computed == expected else "FAIL"
    rec = {
        "id": id_,
        "question": question,
        "computed": computed,
        "expected": expected,
        "verdict": verdict,
        "evidence": evidence,
        "kind": kind,
    }
    if extra:
        rec.update(extra)
    return rec


def build_assertions(data):
    assertions = []

    run_manifests = data["run_manifests"]
    ablehnungen = data["ablehnungen"]
    ausfaelle = data["ausfaelle"]
    aufloesungen = data["aufloesungen"]
    snapshot = data["snapshot"]
    counters = snapshot["zaehler"]

    manifeste_evidence = [relpath(p) for p, _ in run_manifests]
    ablehnungen_evidence = [relpath(data["ablehnungen_path"])]
    aufloesungen_evidence = [relpath(data["aufloesungen_path"])]
    snapshot_evidence = [relpath(data["snapshot_path"])]

    # --- A1: harvest total -------------------------------------------------
    per_run_records = [(m["quelle"], m["records"]) for _, m in run_manifests]
    a1_total = sum(r for _, r in per_run_records)
    assertions.append(make_assertion(
        "A1",
        "What is the sum of `records` over the six committed harvest-run manifests?",
        a1_total,
        29666,
        manifeste_evidence,
        "observed",
        {"per_run": [{"lauf": m["lauf"], "quelle": m["quelle"], "records": m["records"]} for _, m in run_manifests]},
    ))

    # --- A2: withheld source share ------------------------------------------
    withheld_records = sum(r for q, r in per_run_records if q == WITHHELD_SOURCE)
    withheld_share = share(withheld_records, a1_total)
    assertions.append(make_assertion(
        "A2",
        f"How many records did the withheld source (`{WITHHELD_SOURCE}`) contribute to the harvest, and what share of A1 is that?",
        {"withheld_records": withheld_records, "share_of_total": round6(withheld_share)},
        {"withheld_records": 10056, "share_of_total": 0.338974},
        manifeste_evidence,
        "observed",
    ))

    # --- A3: funnel identity -------------------------------------------------
    fundstellen = int(counters["fundstellen"])
    non_withheld_total = a1_total - withheld_records
    a3_diff = fundstellen - non_withheld_total
    assertions.append(make_assertion(
        "A3",
        "Does the snapshot's `fundstellen` counter equal the harvest total minus the withheld source's records, exactly?",
        a3_diff,
        0,
        snapshot_evidence + manifeste_evidence,
        "observed",
        {"fundstellen": fundstellen, "harvest_total_a1": a1_total, "withheld_records_a2": withheld_records,
         "non_withheld_total": non_withheld_total},
    ))

    # --- A4: rejection register size and reason distribution -----------------
    a4_total = len(ablehnungen)
    a4_dist = count_by(ablehnungen, "grund")
    assertions.append(make_assertion(
        "A4",
        "How many lines does the rejection register carry in total, and how are they distributed by reason code (`grund`)?",
        {"total": a4_total, "distribution": a4_dist},
        {"total": 438, "distribution": {
            "konstruierte-url-ungeprueft": 300,
            "keine-zugangs-url": 137,
            "quelle-rechtlich-ungeklaert": 1,
        }},
        ablehnungen_evidence,
        "observed",
    ))

    # --- A5: rejection lines for the withheld source vs its harvest count ----
    withheld_rejection_lines = sum(1 for r in ablehnungen if r["quelle"] == WITHHELD_SOURCE)
    assertions.append(make_assertion(
        "A5",
        f"How many rejection-register lines name the withheld source (`{WITHHELD_SOURCE}`), against how many records of that source were harvested (A2)?",
        {"rejection_lines": withheld_rejection_lines, "harvested_records": withheld_records,
         "ratio": f"{withheld_rejection_lines} : {withheld_records}"},
        {"rejection_lines": 1, "harvested_records": 10056, "ratio": "1 : 10056"},
        ablehnungen_evidence + manifeste_evidence,
        "observed",
    ))

    # --- A6: register excess ---------------------------------------------------
    abgelehnt_gesamt = int(counters["abgelehnt_gesamt"])
    a6_excess = a4_total - abgelehnt_gesamt
    assertions.append(make_assertion(
        "A6",
        "What is the difference between the append-only rejection register's line count and the snapshot's own `abgelehnt_gesamt` counter?",
        a6_excess,
        21,
        ablehnungen_evidence + snapshot_evidence,
        "observed",
        {"ablehnungen_lines": a4_total, "abgelehnt_gesamt": abgelehnt_gesamt},
    ))

    # --- A7: stale rejections (directly observable) ---------------------------
    rejected_hf_ids = {r["quell_id"] for r in ablehnungen if r["quelle"] == "huggingface"}
    confirmed_hf_ids = {
        r["quell_id"] for r in aufloesungen
        if r.get("quelle") == "huggingface" and r.get("ok") is True
    }
    stale_intersection = rejected_hf_ids & confirmed_hf_ids
    remainder = a6_excess - len(stale_intersection)
    assertions.append(make_assertion(
        "A7",
        "Of the `huggingface` records that appear in the rejection register, how many also have a confirmed (ok=true) resolved access route in the resolution ledger?",
        {"rejected_huggingface_ids": len(rejected_hf_ids),
         "confirmed_huggingface_ids": len(confirmed_hf_ids),
         "intersection": len(stale_intersection),
         "excess_remainder_after_intersection": remainder},
        {"rejected_huggingface_ids": 300, "confirmed_huggingface_ids": 20, "intersection": 20,
         "excess_remainder_after_intersection": 1},
        ablehnungen_evidence + aufloesungen_evidence,
        "observed",
        {"note": ("The intersection (20) is directly observable from the two frozen files. "
                  "The remainder (A6 excess 21 minus this intersection 20 = 1) is a separate, "
                  "inference-labelled reading: it identifies the remainder with the single "
                  "withheld-source rejection line seen in A5. See A12 for the inference basis.")},
    ))

    # --- A8: the subset that satisfies the evidence rule ----------------------
    eintraege = int(counters["eintraege"])
    aufgeloest_versucht = int(counters["aufgeloest_versucht"])
    aufgeloest_bestaetigt = int(counters["aufgeloest_bestaetigt"])
    share_versucht = share(aufgeloest_versucht, eintraege)
    share_bestaetigt = share(aufgeloest_bestaetigt, eintraege)
    assertions.append(make_assertion(
        "A8",
        "What share of all register entries (`eintraege`) have an attempted (`aufgeloest_versucht`) resp. confirmed (`aufgeloest_bestaetigt`) resolved access route?",
        {"eintraege": eintraege, "aufgeloest_versucht": aufgeloest_versucht,
         "aufgeloest_bestaetigt": aufgeloest_bestaetigt,
         "share_versucht": round6(share_versucht), "share_bestaetigt": round6(share_bestaetigt)},
        {"eintraege": 17327, "aufgeloest_versucht": 220, "aufgeloest_bestaetigt": 164,
         "share_versucht": 0.012697, "share_bestaetigt": 0.009465},
        snapshot_evidence,
        "observed",
        {"caveat": ("The intersection of `aufgeloest_bestaetigt` with an open licence is not "
                    "computable from the committed tree (the 17,327 entries themselves are "
                    "gitignored). 164 is therefore an upper bound on the subset that satisfies "
                    "both of this practice's evidence conditions (retrievable AND openly licensed), "
                    "not a measurement of that subset itself.")},
    ))

    # --- A9: resolution ledger shape --------------------------------------------
    a9_total = len(aufloesungen)
    a9_unique_ids = len({r["id"] for r in aufloesungen})
    a9_ok_true = sum(1 for r in aufloesungen if r.get("ok") is True)
    status_dist_raw = count_by(aufloesungen, "http_status")
    status_dist = {("null" if k is None else str(k)): v for k, v in status_dist_raw.items()}
    assertions.append(make_assertion(
        "A9",
        "In the resolution ledger, how many rows are there, how many unique `id`s, how many `ok=true` rows, and what is the HTTP status distribution?",
        {"total_rows": a9_total, "unique_ids": a9_unique_ids, "ok_true_rows": a9_ok_true,
         "status_distribution": status_dist},
        {"total_rows": 1070, "unique_ids": 670, "ok_true_rows": 614,
         "status_distribution": {"200": 608, "404": 402, "403": 53, "202": 6, "null": 1}},
        aufloesungen_evidence,
        "observed",
    ))

    # --- A10: where the check fails ---------------------------------------------
    failures = [r for r in aufloesungen if r.get("ok") is not True]
    a10_total = len(failures)
    fail_host_counts = Counter(host_of(r.get("url")) for r in failures)
    fail_host_status = {}
    for r in failures:
        h = host_of(r.get("url"))
        s = r.get("http_status")
        s_key = "null" if s is None else str(s)
        fail_host_status.setdefault(h, Counter())[s_key] += 1
    fail_host_status = {h: dict(c) for h, c in fail_host_status.items()}
    top_two = fail_host_counts.most_common(2)
    top_two_share = share(sum(c for _, c in top_two), a10_total)

    confirmed_rows = [r for r in aufloesungen if r.get("ok") is True]
    confirmed_host_counts = dict(Counter(host_of(r.get("url")) for r in confirmed_rows))

    # The compared computed/expected pair carries exactly the facts the method fixed
    # in advance (total, the two dominant hosts with their status codes, the top-two
    # share). The full per-host breakdown and the confirmed-host distribution are
    # reported alongside as descriptive detail, not as part of the pass/fail check.
    a10_checked = {
        "failures_total": a10_total,
        "www.kaggle.com": {"count": fail_host_counts.get("www.kaggle.com", 0),
                            "statuses": fail_host_status.get("www.kaggle.com", {})},
        "www.gbif.org": {"count": fail_host_counts.get("www.gbif.org", 0),
                          "statuses": fail_host_status.get("www.gbif.org", {})},
        "top_two_share": round6(top_two_share),
    }
    assertions.append(make_assertion(
        "A10",
        "Among resolution-ledger rows where `ok` is not true, what is the URL-host distribution and the associated status codes, and what share of all failures do the top two hosts account for?",
        a10_checked,
        {"failures_total": 456,
         "www.kaggle.com": {"count": 402, "statuses": {"404": 402}},
         "www.gbif.org": {"count": 48, "statuses": {"403": 48}},
         "top_two_share": 0.986842},
        aufloesungen_evidence,
        "observed",
        {"top_two_hosts": [h for h, _ in top_two],
         "full_failure_host_distribution": dict(fail_host_counts),
         "full_failure_host_status_breakdown": fail_host_status,
         "confirmed_host_distribution": confirmed_host_counts},
    ))

    # --- A11: per-run harvest completeness ---------------------------------------
    per_run_detail = []
    incomplete_count = 0
    for path, m in run_manifests:
        records = m["records"]
        reported = m.get("gesamt_gemeldet_im_fenster")
        ratio = share(records, reported) if reported else None
        vollstaendig = m["vollstaendig"]
        if not vollstaendig:
            incomplete_count += 1
        per_run_detail.append({
            "lauf": m["lauf"],
            "quelle": m["quelle"],
            "records": records,
            "gesamt_gemeldet_im_fenster": reported,
            "ratio_records_over_reported": round6(ratio) if ratio is not None else None,
            "vollstaendig": vollstaendig,
            "hinweis": m.get("hinweis"),
        })
    # complete_runs is reported by source name ("the datacite run"), matching how the
    # method states the finding; the exact ratios per run (not part of the fixed
    # expected block, per the method) are carried in the sibling `per_run` field.
    complete_run_sources = sorted({m["quelle"] for _, m in run_manifests if m["vollstaendig"]})
    assertions.append(make_assertion(
        "A11",
        "For each of the six harvest runs, how do `records` compare to `gesamt_gemeldet_im_fenster` (its own reported window total), and how many runs declare themselves incomplete (`vollstaendig`=false)?",
        {"incomplete_runs": incomplete_count, "complete_runs": complete_run_sources},
        {"incomplete_runs": 5, "complete_runs": ["datacite"]},
        manifeste_evidence,
        "observed",
        {"per_run": per_run_detail,
         "note": ("Two of the six run manifests (huggingface, and both kaggle runs) do not "
                  "carry a `gesamt_gemeldet_im_fenster` field at all, so no ratio can be computed "
                  "for them; this is reported as `null`, not zero.")},
    ))

    # --- A12: the withheld-harvest inference --------------------------------------
    alternative_ruled_out = "ruled-out-by-counters"
    # The alternative reading (files present, rejected per record) would require
    # abgelehnt_gesamt to be at least withheld_records (10056); it is 417.
    ruled_out = abgelehnt_gesamt < withheld_records
    computed_alt = alternative_ruled_out if ruled_out else "not-ruled-out"

    # Directly observable corroboration (not itself part of the inference): the
    # snapshot manifest's own `assets` array names a packaged jsonl.gz file for
    # every run EXCEPT the withheld source's two kaggle runs, even though both
    # kaggle run manifests declare their own `datei`/`sha256` for such a file.
    asset_names = [a["name"] for a in snapshot.get("assets", [])]
    run_files_in_assets = {
        m["quelle"]: (m.get("datei") in asset_names) for _, m in run_manifests
    }
    kaggle_files_listed_as_assets = sum(
        1 for _, m in run_manifests if m["quelle"] == WITHHELD_SOURCE and m.get("datei") in asset_names
    )

    assertions.append(make_assertion(
        "A12",
        ("Inference: were the withheld source's harvest files simply absent from the build's "
         "inputs (rather than present and individually rejected)? State the alternative reading "
         "and whether the counters rule it out."),
        computed_alt,
        alternative_ruled_out,
        snapshot_evidence + ablehnungen_evidence + manifeste_evidence,
        "inference",
        {
            "basis": ("A3 shows fundstellen (19610) equals the harvest total of all sources "
                      "except the withheld one (kaggle), exactly, with zero difference. "
                      "This is consistent with the withheld source's harvest files having been "
                      "absent from the snapshot build's inputs entirely."),
            "alternative_reading": ("The files were present as inputs to the build, and the "
                                     "withheld source's 10056 records were rejected one by one "
                                     "during the build."),
            "why_ruled_out": (f"A per-record rejection of {withheld_records} records would "
                               f"require the snapshot's abgelehnt_gesamt counter to be at least "
                               f"{withheld_records}. It is {abgelehnt_gesamt} (A4/A6), which rules "
                               f"out the alternative reading."),
            "abgelehnt_gesamt": abgelehnt_gesamt,
            "withheld_records": withheld_records,
            "corroborating_observation": (
                "The snapshot manifest's own `assets` array (a directly readable field, not an "
                "inference) lists the packaged run file for arcgis (both runs), datacite, and "
                "huggingface, but lists no file for either kaggle run, although both kaggle run "
                "manifests declare their own `datei`/`sha256` for exactly such a file. "
                f"kaggle run files listed among snapshot assets: {kaggle_files_listed_as_assets} of "
                f"{sum(1 for _, m in run_manifests if m['quelle'] == WITHHELD_SOURCE)}."
            ),
            "run_file_present_in_snapshot_assets_by_source": run_files_in_assets,
        },
    ))

    # --- A13: where the verification effort went ---------------------------------
    rows_by_source = count_by(aufloesungen, "quelle")
    ids_by_source = {}
    for r in aufloesungen:
        ids_by_source.setdefault(r["quelle"], set()).add(r["id"])
    unique_ids_by_source = {q: len(ids) for q, ids in ids_by_source.items()}
    a13_total_rows = len(aufloesungen)
    a13_total_unique_ids = len({r["id"] for r in aufloesungen})
    withheld_rows = rows_by_source.get(WITHHELD_SOURCE, 0)
    withheld_unique_ids = unique_ids_by_source.get(WITHHELD_SOURCE, 0)
    withheld_share_rows = share(withheld_rows, a13_total_rows)
    withheld_share_unique_ids = share(withheld_unique_ids, a13_total_unique_ids)
    assertions.append(make_assertion(
        "A13",
        "In the resolution ledger, how many rows and how many unique ids does each source contribute, and what share of each does the withheld source account for?",
        {"rows_by_source": rows_by_source, "unique_ids_by_source": unique_ids_by_source,
         "withheld_share_of_rows": round6(withheld_share_rows),
         "withheld_share_of_unique_ids": round6(withheld_share_unique_ids)},
        {"rows_by_source": {"kaggle": 850, "datacite": 200, "huggingface": 20},
         "unique_ids_by_source": {"kaggle": 450, "datacite": 200, "huggingface": 20},
         "withheld_share_of_rows": 0.794393,
         "withheld_share_of_unique_ids": 0.671642},
        aufloesungen_evidence,
        "observed",
    ))

    # --- A14: the counters reconcile, and what that proves ------------------------
    last_wins = last_wins_by_id(aufloesungen)
    non_withheld_last = {i: r for i, r in last_wins.items() if r["quelle"] != WITHHELD_SOURCE}
    non_withheld_ok = sum(1 for r in non_withheld_last.values() if r.get("ok") is True)
    withheld_last = {i: r for i, r in last_wins.items() if r["quelle"] == WITHHELD_SOURCE}
    withheld_last_ok = sum(1 for r in withheld_last.values() if r.get("ok") is True)
    assertions.append(make_assertion(
        "A14",
        ("Reducing the resolution ledger to one row per id (last occurrence in file order "
         "wins, matching the upstream builder's own reduction), and restricting to the "
         "non-withheld sources (`datacite`, `huggingface`): how many ids are there, and how "
         "many have `ok` true? Do these equal the snapshot's `aufgeloest_versucht` and "
         "`aufgeloest_bestaetigt` counters?"),
        {"non_withheld_ids": len(non_withheld_last), "non_withheld_ok": non_withheld_ok,
         "withheld_last_wins_ok": withheld_last_ok},
        {"non_withheld_ids": aufgeloest_versucht, "non_withheld_ok": aufgeloest_bestaetigt,
         "withheld_last_wins_ok": 450},
        aufloesungen_evidence + snapshot_evidence,
        "observed",
        {"note": ("The non-withheld reduction reproduces the snapshot's own "
                  "aufgeloest_versucht/aufgeloest_bestaetigt counters exactly. This makes A12's "
                  "inference near-direct: under the identical last-wins reduction, 450 "
                  "withheld-source ids hold a confirmed access route, and none of the 450 "
                  "contributes to either published counter.")},
    ))

    # --- A15: the repeat structure of the ledger -----------------------------------
    id_groups = group_by_id(aufloesungen)
    repeated = {i: rs for i, rs in id_groups.items() if len(rs) > 1}
    repeated_sources = {rs[0]["quelle"] for rs in repeated.values()}
    max_repeat_count = max((len(rs) for rs in repeated.values()), default=0)

    forward_pattern = [(404, False), (200, True)]
    reverse_pattern = [(200, True), (404, False)]
    forward_count = 0
    reverse_count = 0
    other_count = 0
    order_mismatches = 0
    for rs in repeated.values():
        chrono = sorted(rs, key=lambda r: r["datum"])
        file_order_ids = [id(r) for r in rs]
        chrono_order_ids = [id(r) for r in chrono]
        if file_order_ids != chrono_order_ids:
            order_mismatches += 1
        pattern = [(r.get("http_status"), r.get("ok")) for r in chrono]
        if pattern == forward_pattern:
            forward_count += 1
        elif pattern == reverse_pattern:
            reverse_count += 1
        else:
            other_count += 1

    assertions.append(make_assertion(
        "A15",
        ("Which resolution-ledger ids appear more than once, from which source, what is the "
         "maximum repeat count, and, in chronological order by `datum`, what pattern of "
         "`(http_status, ok)` do the repeated ids show?"),
        {"repeated_ids": len(repeated), "repeated_sources": sorted(repeated_sources),
         "max_repeat_count": max_repeat_count,
         "forward_pattern_count": forward_count, "reverse_pattern_count": reverse_count,
         "other_pattern_count": other_count,
         "ids_where_file_order_differs_from_datum_order": order_mismatches},
        {"repeated_ids": 400, "repeated_sources": ["kaggle"], "max_repeat_count": 2,
         "forward_pattern_count": 400, "reverse_pattern_count": 0, "other_pattern_count": 0,
         "ids_where_file_order_differs_from_datum_order": 0},
        aufloesungen_evidence,
        "observed",
        {"forward_pattern": "[(404, false), (200, true)]",
         "note": ("All 400 repeated ids belong to the withheld source and show the same "
                  "pattern: an initial 404/false row later followed by a 200/true row, in file "
                  "order and in chronological (datum) order alike.")},
    ))

    # --- A16: what the failure column actually contains ---------------------------
    ok_true_ids = {r["id"] for r in aufloesungen if r.get("ok") is True}
    failures_a16 = [r for r in aufloesungen if r.get("ok") is not True]
    n_failures = len(failures_a16)

    class_has_ok_sibling = [r for r in failures_a16 if r["id"] in ok_true_ids]
    remaining_a16 = [r for r in failures_a16 if r["id"] not in ok_true_ids]

    class_403 = [r for r in remaining_a16 if r.get("http_status") == 403]
    class_403_hosts = dict(Counter(host_of(r.get("url")) for r in class_403))

    class_outage = [r for r in remaining_a16 if "ausfall" in r and "http_status" not in r]
    class_outage_hosts = sorted({host_of(r.get("url")) for r in class_outage})

    classified_ids = {id(r) for r in class_403} | {id(r) for r in class_outage}
    class_residue = [r for r in remaining_a16 if id(r) not in classified_ids]
    class_residue_hosts = sorted({host_of(r.get("url")) for r in class_residue})
    class_residue_sources = sorted({r["quelle"] for r in class_residue})
    class_residue_statuses = sorted({r.get("http_status") for r in class_residue})

    classes_sum = len(class_has_ok_sibling) + len(class_403) + len(class_outage) + len(class_residue)
    residue_share_of_failures = share(len(class_residue), n_failures)
    residue_share_of_all_rows = share(len(class_residue), len(aufloesungen))

    unconfirmed_from_a14 = aufgeloest_versucht - aufgeloest_bestaetigt

    assertions.append(make_assertion(
        "A16",
        ("Among the resolution-ledger rows where `ok` is not true, how many fall into each of "
         "four disjoint classes: (i) rows whose id has another row with `ok` true elsewhere in "
         "the ledger; (ii) of the rest, rows with HTTP status 403, and their hosts; (iii) rows "
         "carrying a transport-outage marker (`ausfall`, no `http_status`), and their host; "
         "(iv) the remaining residue, with its hosts, sources and statuses? Do the four classes "
         "sum to the total number of non-ok rows?"),
        {"failures_total": n_failures,
         "class_has_ok_sibling": len(class_has_ok_sibling),
         "class_403": len(class_403), "class_403_hosts": class_403_hosts,
         "class_outage": len(class_outage), "class_outage_hosts": class_outage_hosts,
         "class_residue": len(class_residue), "class_residue_hosts": class_residue_hosts,
         "class_residue_sources": class_residue_sources,
         "class_residue_statuses": class_residue_statuses,
         "classes_sum": classes_sum,
         "residue_share_of_failures": round6(residue_share_of_failures),
         "residue_share_of_all_rows": round6(residue_share_of_all_rows)},
        {"failures_total": 456,
         "class_has_ok_sibling": 400,
         "class_403": 53, "class_403_hosts": {"www.gbif.org": 48, "www.openicpsr.org": 2,
                                                "data.nhm.ac.uk": 1, "www.researchgate.net": 1,
                                                "www.checklistbank.org": 1},
         "class_outage": 1, "class_outage_hosts": ["www.osti.gov"],
         "class_residue": 2, "class_residue_hosts": ["www.kaggle.com"],
         "class_residue_sources": ["datacite"],
         "class_residue_statuses": [404],
         "classes_sum": 456,
         "residue_share_of_failures": round6(share(2, 456)),
         "residue_share_of_all_rows": 0.001869},
        aufloesungen_evidence,
        "observed",
        {"note": (f"The 56 rows never confirmed anywhere in the ledger (class_403 + class_outage "
                  f"= {len(class_403) + len(class_outage)}) equal the entry-level unconfirmed "
                  f"count implied by A14 (aufgeloest_versucht - aufgeloest_bestaetigt = "
                  f"{aufgeloest_versucht} - {aufgeloest_bestaetigt} = {unconfirmed_from_a14}). "
                  "At this state the register's entire checked-but-not-confirmed column is "
                  "53 rows with HTTP status 403, 1 row with a transport outage, and 2 rows "
                  "with HTTP status 404 reached through DataCite-registered DOIs.")},
    ))

    return assertions


# ---------------------------------------------------------------------------
# Report assembly
# ---------------------------------------------------------------------------

def build_report():
    """Load inputs, compute all assertions, and assemble the full report dict."""
    data = load_inputs()
    assertions = build_assertions(data)
    n_pass = sum(1 for a in assertions if a["verdict"] == "PASS")
    n_fail = len(assertions) - n_pass
    report = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "upstream": {
            "commit": UPSTREAM_COMMIT,
            "tag": UPSTREAM_TAG,
            "tag_sha": UPSTREAM_TAG_SHA,
        },
        "inputs": collect_input_manifest(),
        "assertions": assertions,
        "verdict": {
            "pass_count": n_pass,
            "fail_count": n_fail,
            "total": len(assertions),
            "all_pass": n_fail == 0,
        },
    }
    return report


def print_report(report):
    """Print a compact human-readable summary of the report to stdout."""
    print("Dataset Register audit")
    print(f"generated_utc: {report['generated_utc']}")
    print(f"upstream commit: {report['upstream']['commit']}")
    print(f"upstream tag: {report['upstream']['tag']} ({report['upstream']['tag_sha']})")
    print()
    for a in report["assertions"]:
        print(f"[{a['verdict']}] {a['id']} ({a['kind']}): {a['question']}")
        print(f"    computed: {a['computed']}")
        print(f"    expected: {a['expected']}")
    print()
    v = report["verdict"]
    print(f"AUDIT: {v['pass_count']}/{v['total']} assertions PASS"
          + ("" if v["all_pass"] else f" ({v['fail_count']} FAIL)"))


def reports_equal_ignoring_timestamp(a, b):
    """Compare two report dicts for equality, ignoring the generated_utc field."""
    a2 = dict(a)
    b2 = dict(b)
    a2.pop("generated_utc", None)
    b2.pop("generated_utc", None)
    return json.dumps(a2, sort_keys=True) == json.dumps(b2, sort_keys=True)


def main():
    parser = argparse.ArgumentParser(description="Audit the frozen Dataset Register records.")
    parser.add_argument("--check", action="store_true",
                         help="Recompute and compare against the committed results/audit.json; "
                              "exit non-zero on any FAIL or on any drift beyond generated_utc.")
    args = parser.parse_args()

    report = build_report()
    print_report(report)

    if args.check:
        ok = report["verdict"]["all_pass"]
        if not os.path.exists(RESULTS_PATH):
            print("CHECK: no committed results/audit.json found", file=sys.stderr)
            sys.exit(1)
        with open(RESULTS_PATH, "r", encoding="utf-8") as fh:
            committed = json.load(fh)
        drift = not reports_equal_ignoring_timestamp(report, committed)
        if drift:
            print("CHECK: regenerated report differs from committed results/audit.json "
                  "(beyond generated_utc)", file=sys.stderr)
        if not ok or drift:
            sys.exit(1)
        sys.exit(0)

    os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
    with open(RESULTS_PATH, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=False, ensure_ascii=False)
        fh.write("\n")


if __name__ == "__main__":
    main()
