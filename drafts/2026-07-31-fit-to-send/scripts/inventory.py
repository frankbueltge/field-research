#!/usr/bin/env python3
"""Layer 0 — offline inventory of every outbound identifier in `works/`.

Governed by drafts/2026-07-31-fit-to-send/PREREGISTRATION.md, section 2. This script makes
**no network request**. It walks the pinned tree, extracts identifiers of four pre-registered
classes (U1 absolute URL, U2 scheme-less locator, U3 DOI, U4 arXiv id), assigns each a tier
and a role, records a SHA-256 per scanned file, and writes a deterministic
`results/inventory.json`. It also computes the three Layer-0 assertions (L0-1, L0-2, L0-3).

Usage:
    python3 scripts/inventory.py            # (re)write results/inventory.json + INVENTORY.md
    python3 scripts/inventory.py --check    # determinism check; exits non-zero on any diff
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Fixed, pre-registered constants. Committed inside the script per the task's
# instruction for the U2 TLD list; the same treatment is extended to the
# other fixed lists below so every non-obvious cutoff is visible in one place.
# ---------------------------------------------------------------------------

SCRIPT_PATH = Path(__file__).resolve()
DRAFT_ROOT = SCRIPT_PATH.parents[1]          # drafts/2026-07-31-fit-to-send
REPO_ROOT = SCRIPT_PATH.parents[3]           # repository root
WORKS_DIR = REPO_ROOT / "works"
RESULTS_DIR = DRAFT_ROOT / "results"
INVENTORY_JSON = RESULTS_DIR / "inventory.json"
INVENTORY_MD = RESULTS_DIR / "INVENTORY.md"

# Given, not derived: the pin the preregistration names. Not read from git.
PINNED_COMMIT = "0138e79d0bd95aa4797fb617949d07d947fb338f"

# §2.1 U2: "host.tld/path where the TLD is in a fixed list committed with the script."
U2_TLDS = [
    "com", "org", "net", "edu", "gov", "int", "eu", "de",
    "io", "ai", "info", "uk", "ch", "at", "press", "law",
]

# Text-bearing extensions swept (§ task item 1). Everything else is skipped as binary,
# including extensions that might carry text (e.g. .jsonl, .pem) — not in the pre-registered
# list, so not widened in. See report, "Implementation decisions".
ALLOWED_EXTENSIONS = {".md", ".astro", ".html", ".json", ".txt", ".py", ".csv"}

# §2.2 tier "site": exactly these top-level filenames.
SITE_FILENAMES = {"work.astro", "work.html", "meta.json", "data.json"}

# Role rule, bullet 1: filename-based correction-record triggers.
CORRECTIONS_FILENAME = "CORRECTIONS.md"
RECOVERY_SUBSTRING = "RECOVERY"

# Role rule, bullet 1: heading-text substrings (case-insensitive), applied only within
# markdown (.md) files — see "Implementation decisions" for why .md-only.
CORRECTION_HEADING_SUBSTRINGS = (
    "corrected", "withdrawn", "was wrong", "superseded", "discarded",
)

# Role rule, bullet 2: frozen third-party data the works STUDY, not cite — named explicitly
# by the task, relative to repo root.
FROZEN_OBJECT_DATA_FILES = {
    "works/2026-07-20-coverage-not-custody/sample.json",
    "works/2026-07-20-coverage-not-custody/results.json",
    "works/2026-07-20-coverage-not-custody/results-subtest.json",
    "works/2026-07-20-coverage-not-custody/results-x-subtest.json",
}

# §4 / Layer 2b: key-name whitelist used to recognise a "quotation/identifier-valued field"
# structurally. See "Implementation decisions" for why a bare "id" key is excluded.
TOKEN_FIELD_KEYWORDS = (
    "quote", "verbatim", "phrase", "token", "identifier", "excerpt", "snippet", "claim",
)

# Characters that terminate a raw identifier match: whitespace, markup delimiters, and the
# markdown inline-code backtick (not part of the pre-registered strip set, but a match
# *boundary* — see "Implementation decisions").
_STOP_CHARS = r'\s<>"\'`'

TRAILING_STRIP_CHARS = ".,;:)]}\"'"


# ---------------------------------------------------------------------------
# Identifier extraction
# ---------------------------------------------------------------------------

U1_RE = re.compile(r"https?://[^" + _STOP_CHARS + r"]+")

_TLD_ALT = "|".join(re.escape(t) for t in U2_TLDS)
U2_RE = re.compile(
    r"(?<![\w./@])([a-zA-Z0-9][a-zA-Z0-9-]*(?:\.[a-zA-Z0-9-]+)*\.(?:"
    + _TLD_ALT
    + r")/[^" + _STOP_CHARS + r"]+)"
)

# with or without a `doi:` / `https://doi.org/` prefix (§2.1 U3). The https://doi.org/ case
# is already consumed as U1 before this pattern runs (see extract_identifiers).
U3_RE = re.compile(r"(?:[Dd][Oo][Ii]:\s*)?(10\.\d{4,9}/[^" + _STOP_CHARS + r"]+)")

U4_RE = re.compile(r"[Aa][Rr][Xx][Ii][Vv]:\s?(\d{4}\.\d{4,5}(?:[Vv]\d+)?)")


def strip_trailing(s: str) -> str:
    """Strip trailing `.,;:)]}` and any trailing `"` or `'` — repeatedly, per §2, item 4."""
    while s and s[-1] in TRAILING_STRIP_CHARS:
        s = s[:-1]
    return s


def _mask(text: str, spans: list[tuple[int, int]]) -> str:
    chars = list(text)
    for s, e in spans:
        for i in range(s, e):
            chars[i] = " "
    return "".join(chars)


def extract_identifiers(text: str) -> list[dict]:
    """Return a list of {cls, raw, start} for one file's text, in class-priority order
    (U1 first, then U2, U3, U4), each pass run against a copy of the text with the previously
    matched spans masked out so the same substring is never claimed by two classes."""
    found = []
    spans: list[tuple[int, int]] = []

    working = text
    for m in U1_RE.finditer(working):
        found.append({"cls": "U1", "raw": m.group(0), "start": m.start()})
        spans.append((m.start(), m.end()))
    working = _mask(text, spans)

    new_spans = []
    for m in U2_RE.finditer(working):
        found.append({"cls": "U2", "raw": m.group(1), "start": m.start(1)})
        new_spans.append((m.start(1), m.end(1)))
    spans.extend(new_spans)
    working = _mask(text, spans)

    new_spans = []
    for m in U3_RE.finditer(working):
        found.append({"cls": "U3", "raw": m.group(0), "start": m.start(0)})
        new_spans.append((m.start(0), m.end(0)))
    spans.extend(new_spans)
    working = _mask(text, spans)

    new_spans = []
    for m in U4_RE.finditer(working):
        found.append({"cls": "U4", "raw": m.group(0), "start": m.start(0)})
        new_spans.append((m.start(0), m.end(0)))
    spans.extend(new_spans)

    return found


def normalize(cls: str, raw: str) -> str:
    """§2, item 4: normalise to a fetchable URL."""
    if cls == "U1":
        return strip_trailing(raw)
    if cls == "U2":
        return "https://" + strip_trailing(raw)
    if cls == "U3":
        # raw may carry a leading "doi:" / "DOI:" marker; the DOI proper starts at "10.".
        m = re.search(r"10\.\d{4,9}/.*", raw)
        doi = m.group(0) if m else raw
        return "https://doi.org/" + strip_trailing(doi)
    if cls == "U4":
        m = re.search(r"\d{4}\.\d{4,5}(?:[Vv]\d+)?", raw)
        arxiv_id = m.group(0) if m else raw
        return "https://arxiv.org/abs/" + strip_trailing(arxiv_id)
    raise ValueError(cls)


# ---------------------------------------------------------------------------
# Markdown heading tracking (correction-record by heading, §2 role rule bullet 1)
# ---------------------------------------------------------------------------

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")


def correction_heading_lines(text: str) -> set[int]:
    """Return the set of 0-indexed line numbers that fall under a markdown heading whose
    text contains one of CORRECTION_HEADING_SUBSTRINGS (case-insensitive), including nested
    subheadings of that section. .md files only (see "Implementation decisions")."""
    lines = text.split("\n")
    flagged: set[int] = set()
    active_level: int | None = None
    for i, line in enumerate(lines):
        m = _HEADING_RE.match(line)
        if m:
            level = len(m.group(1))
            heading_text = m.group(2).lower()
            is_match = any(p in heading_text for p in CORRECTION_HEADING_SUBSTRINGS)
            if is_match:
                active_level = level
                flagged.add(i)
                continue
            if active_level is not None and level <= active_level:
                active_level = None
            continue
        if active_level is not None:
            flagged.add(i)
    return flagged


def line_of_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1  # 1-indexed


# ---------------------------------------------------------------------------
# Tier / role assignment
# ---------------------------------------------------------------------------

def compute_tier(rel_path: str) -> str:
    """rel_path is relative to WORKS_DIR, e.g. '2026-07-01-fairness-trap/work.astro'."""
    parts = rel_path.split("/")
    if len(parts) == 2 and parts[1] in SITE_FILENAMES:
        return "site"
    if len(parts) == 2:
        return "repo"
    return "sub"


def compute_role(rel_path: str, tier: str, under_correction_heading: bool) -> str:
    """rel_path relative to WORKS_DIR. Ordered rules, first match wins — matches the ordering
    of the bullets in the task specification exactly."""
    filename = rel_path.split("/")[-1]
    repo_rel = "works/" + rel_path

    if filename == CORRECTIONS_FILENAME:
        return "correction-record"
    if RECOVERY_SUBSTRING in filename.upper():
        return "correction-record"
    if under_correction_heading:
        return "correction-record"

    if tier == "sub":
        return "object-data"
    if repo_rel in FROZEN_OBJECT_DATA_FILES:
        return "object-data"

    return "evidence"


# ---------------------------------------------------------------------------
# Layer 2b — structural token bindings
# ---------------------------------------------------------------------------

_URL_IN_VALUE_RE = re.compile(r"https?://[^\s<>\"'`;]+")


def find_urls_in_value(v: str) -> list[str]:
    return [strip_trailing(u) for u in _URL_IN_VALUE_RE.findall(v)]


def is_token_key(k: str) -> bool:
    kl = k.lower()
    return any(kw in kl for kw in TOKEN_FIELD_KEYWORDS)


def is_excluded_numeric_token(v: str) -> bool:
    """§4 / Layer 2b: 'Numeric tokens shorter than 4 digits are excluded.'"""
    stripped = v.strip()
    return stripped.isdigit() and len(stripped) < 4


def scan_json_for_token_bindings(rel_path: str, data) -> list[dict]:
    bindings = []

    def walk(obj, json_path):
        if isinstance(obj, dict):
            url_pairs = []
            for k, v in obj.items():
                if isinstance(v, str):
                    for u in find_urls_in_value(v):
                        url_pairs.append((k, u))
            token_pairs = []
            for k, v in obj.items():
                if isinstance(v, str) and is_token_key(k):
                    if not is_excluded_numeric_token(v):
                        token_pairs.append((k, v))
            if url_pairs and token_pairs:
                for _uk, u in url_pairs:
                    for _tk, t in token_pairs:
                        bindings.append({
                            "file": "works/" + rel_path,
                            "json_path": json_path or "/",
                            "url": u,
                            "token": t,
                        })
            for k, v in obj.items():
                walk(v, json_path + "/" + k)
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                walk(v, json_path + f"[{i}]")

    walk(data, "")
    return bindings


# ---------------------------------------------------------------------------
# File walking
# ---------------------------------------------------------------------------

def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def iter_work_dirs():
    for entry in sorted(WORKS_DIR.iterdir()):
        if entry.is_dir():
            yield entry.name


def iter_scanned_files(work_name: str):
    """Yield (rel_path_within_works, abs_path) for text-bearing files, deterministically
    ordered (sorted walk)."""
    work_dir = WORKS_DIR / work_name
    for root, dirs, files in os.walk(work_dir):
        dirs.sort()
        for fn in sorted(files):
            ext = Path(fn).suffix.lower()
            if ext not in ALLOWED_EXTENSIONS:
                continue
            abs_path = Path(root) / fn
            rel_path = str(abs_path.relative_to(WORKS_DIR)).replace(os.sep, "/")
            yield rel_path, abs_path


# ---------------------------------------------------------------------------
# Build the inventory
# ---------------------------------------------------------------------------

def build_inventory() -> dict:
    files_record = []
    identifiers_record = []
    token_bindings_record = []

    works = list(iter_work_dirs())
    assert len(works) == 20, f"expected 20 work directories, found {len(works)}"

    for work_name in works:
        for rel_path, abs_path in iter_scanned_files(work_name):
            repo_rel = "works/" + rel_path
            files_record.append({
                "path": repo_rel,
                "sha256": sha256_of_file(abs_path),
            })

            raw_bytes = abs_path.read_bytes()
            try:
                text = raw_bytes.decode("utf-8")
            except UnicodeDecodeError:
                text = raw_bytes.decode("utf-8", errors="replace")

            tier = compute_tier(rel_path)
            is_md = abs_path.suffix.lower() == ".md"
            heading_lines = correction_heading_lines(text) if is_md else set()

            for ident in extract_identifiers(text):
                line_no = line_of_offset(text, ident["start"])
                under_heading = (line_no - 1) in heading_lines
                role = compute_role(rel_path, tier, under_heading)
                normalized_url = normalize(ident["cls"], ident["raw"])
                identifiers_record.append({
                    "work": work_name,
                    "path": repo_rel,
                    "tier": tier,
                    "class": ident["cls"],
                    "role": role,
                    "raw": ident["raw"],
                    "normalized_url": normalized_url,
                    "line": line_no,
                })

            if abs_path.suffix.lower() == ".json":
                try:
                    data = json.loads(text)
                except json.JSONDecodeError:
                    data = None
                if data is not None:
                    token_bindings_record.extend(
                        scan_json_for_token_bindings(rel_path, data)
                    )

    files_record.sort(key=lambda r: r["path"])
    identifiers_record.sort(key=lambda r: (
        r["work"], r["path"], r["class"], r["line"], r["raw"], r["role"],
    ))
    token_bindings_record.sort(key=lambda r: (
        r["file"], r["json_path"], r["url"], r["token"],
    ))

    assertions = compute_assertions(works, identifiers_record)

    inventory = {
        "pinned_commit": PINNED_COMMIT,
        "object": "the 20 work directories under works/ at the pinned commit",
        "works": works,
        "u2_tld_list": list(U2_TLDS),
        "allowed_extensions": sorted(ALLOWED_EXTENSIONS),
        "files": files_record,
        "identifiers": identifiers_record,
        "token_bindings": token_bindings_record,
        "assertions": assertions,
    }
    return inventory


def compute_assertions(works: list[str], identifiers: list[dict]) -> dict:
    # L0-1: per work, per tier, per class, per role: identifier counts.
    counts: dict[tuple, int] = {}
    for ident in identifiers:
        key = (ident["work"], ident["tier"], ident["class"], ident["role"])
        counts[key] = counts.get(key, 0) + 1
    l0_1 = [
        {"work": w, "tier": t, "class": c, "role": r, "count": n}
        for (w, t, c, r), n in sorted(counts.items())
    ]

    # L0-2: works whose evidence-role inventory is empty in every class -> UNAUDITABLE.
    evidence_by_work: dict[str, int] = {w: 0 for w in works}
    for ident in identifiers:
        if ident["role"] == "evidence":
            evidence_by_work[ident["work"]] += 1
    uninauditable = sorted(w for w, n in evidence_by_work.items() if n == 0)

    # L0-3: per work, does the rendered `site` tier carry any evidence identifier at all.
    site_evidence_by_work: dict[str, int] = {w: 0 for w in works}
    for ident in identifiers:
        if ident["role"] == "evidence" and ident["tier"] == "site":
            site_evidence_by_work[ident["work"]] += 1
    l0_3 = [
        {"work": w, "site_tier_has_evidence": site_evidence_by_work[w] > 0}
        for w in sorted(works)
    ]
    no_site_evidence = sorted(w for w, n in site_evidence_by_work.items() if n == 0)

    return {
        "L0_1_counts": l0_1,
        "L0_2_UNAUDITABLE": uninauditable,
        "L0_3_site_tier_evidence": l0_3,
        "L0_3_works_with_no_site_evidence": no_site_evidence,
    }


# ---------------------------------------------------------------------------
# Human-readable summary
# ---------------------------------------------------------------------------

def write_inventory_md(inventory: dict, path: Path) -> None:
    works = inventory["works"]
    counts = inventory["assertions"]["L0_1_counts"]
    uninauditable = inventory["assertions"]["L0_2_UNAUDITABLE"]
    no_site_evidence = inventory["assertions"]["L0_3_works_with_no_site_evidence"]
    identifiers = inventory["identifiers"]

    # evidence counts per work per tier
    per_work_tier: dict[tuple, int] = {}
    for row in counts:
        if row["role"] != "evidence":
            continue
        key = (row["work"], row["tier"])
        per_work_tier[key] = per_work_tier.get(key, 0) + row["count"]

    lines = []
    lines.append("# Inventory — Layer 0 summary")
    lines.append("")
    lines.append(f"Pinned commit: `{inventory['pinned_commit']}`. Offline, deterministic, no network request made.")
    lines.append("")
    lines.append("Counts below are of role `evidence` identifiers only (all classes combined), by tier.")
    lines.append("")
    lines.append("| work | site | repo | sub | UNAUDITABLE (L0-2) | site has no evidence (L0-3) |")
    lines.append("|---|---|---|---|---|---|")
    for w in works:
        site = per_work_tier.get((w, "site"), 0)
        repo = per_work_tier.get((w, "repo"), 0)
        sub = per_work_tier.get((w, "sub"), 0)
        flag_uninaud = "UNAUDITABLE" if w in uninauditable else ""
        flag_site = "yes" if w in no_site_evidence else ""
        lines.append(f"| {w} | {site} | {repo} | {sub} | {flag_uninaud} | {flag_site} |")
    lines.append("")

    lines.append("## L0-2 — UNAUDITABLE (evidence-role inventory empty in every class)")
    lines.append("")
    if uninauditable:
        for w in uninauditable:
            lines.append(f"- {w}")
    else:
        lines.append("(none)")
    lines.append("")

    lines.append("## L0-3 — works whose rendered `site` tier carries no `evidence` identifier at all")
    lines.append("")
    if no_site_evidence:
        for w in no_site_evidence:
            lines.append(f"- {w}")
    else:
        lines.append("(none)")
    lines.append("")

    n_unique_evidence = len({
        i["normalized_url"] for i in identifiers
        if i["role"] == "evidence" and i["tier"] in ("site", "repo")
    })
    n_identifier_occurrences = len(identifiers)
    lines.append(
        f"Total unique normalised `evidence` URLs (tiers site+repo — what Layer 1 would probe): "
        f"**{n_unique_evidence}**."
    )
    lines.append(f"Total identifier occurrences recorded (all tiers, all roles): **{n_identifier_occurrences}**.")
    lines.append(f"Structural token bindings found (Layer 2b candidates): **{len(inventory['token_bindings'])}**.")
    lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------

def canonical_json(obj: dict) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true",
                         help="re-run extraction and exit non-zero if results/inventory.json "
                              "on disk differs from a fresh run (determinism check).")
    args = parser.parse_args()

    inventory = build_inventory()
    fresh_text = canonical_json(inventory)

    if args.check:
        if not INVENTORY_JSON.exists():
            print(f"CHECK FAILED: {INVENTORY_JSON} does not exist", file=sys.stderr)
            sys.exit(1)
        on_disk_text = INVENTORY_JSON.read_text(encoding="utf-8")
        if on_disk_text != fresh_text:
            print("CHECK FAILED: results/inventory.json differs from a fresh run", file=sys.stderr)
            sys.exit(1)
        print("CHECK OK: results/inventory.json is reproducible from the pinned tree.")
        sys.exit(0)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    INVENTORY_JSON.write_text(fresh_text, encoding="utf-8")
    write_inventory_md(inventory, INVENTORY_MD)
    print(f"Wrote {INVENTORY_JSON}")
    print(f"Wrote {INVENTORY_MD}")


if __name__ == "__main__":
    main()
