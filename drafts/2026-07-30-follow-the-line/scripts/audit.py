#!/usr/bin/env python3
"""Back-reference audit of the ecology's Paper Catalogue against this repository.

The catalogue's distinguishing promise is line-level provenance: every entry carries the
repository and file where the citation was found. That promise is checkable in exactly one
place by exactly one party — the entries whose evidence is asserted to sit in `field-research/`.
This script performs that check, and the complementary one in the other direction: which
identifier-shaped strings this repository actually contains, and what a sieve does to them.

Every assertion is OFFLINE and DETERMINISTIC. The two inputs are:
  * the frozen catalogue extract  (sources/history/a7879398.json, hashed in
    sources/history/MANIFEST.json and in SOURCES.md)
  * this repository at a pinned commit (default 58d9c4c), read via `git show`, never the
    working tree — so the audit does not measure whatever happens to be checked out.

Live network observations are NOT assertions here. One was made this session and is fenced
off in the work's own record; nothing in this file depends on it.

Both runs first verify the frozen input against the hash pinned for it in MANIFEST.json and
refuse to proceed if it has drifted (added in gauntlet round four; `--check` on its own proves
only that a fresh run reproduces the committed output, not that the input is still the
documented one).

Usage:
  python3 scripts/audit.py            # write results/audit.json
  python3 scripts/audit.py --check    # recompute and fail if it differs from the committed file
"""
import argparse
import collections
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE,
                      capture_output=True, text=True, check=True).stdout.strip()
FROZEN = os.path.join(HERE, "sources", "history", "a7879398.json")
MANIFEST = os.path.join(HERE, "sources", "history", "MANIFEST.json")
OUT = os.path.join(HERE, "results", "audit.json")

PIN = "58d9c4c"

# The catalogue side, pinned to upstream commits. Established 2026-07-28 after this practice's
# published claim that the upstream history was unreadable was tested and found false; carried
# into this file on 2026-07-30 (see the `corrections` block in the output's `pin`).
UPSTREAM_COMMIT = "a7879398326d0b6e546cbeab8b7216ca31700f5e"   # the state audited, 01:41:37+02:00
SEED_STATE_COMMIT = "6a032edb16f645d56eab9af2a913050eb3de57e4"   # the state the seed described

# The catalogue names citers with short labels; their evidence paths carry repository
# prefixes. This is the mapping the audit tests, not a mapping it assumes.
LABEL_TO_PREFIX = {
    "field": {"field-research"},
    "meridian": {"meridian-runtime", "docs"},
    "atelier": {"ulysses"},
    "studio": {"studio"},
}

VENDORED = "works/2026-07-26-one-line-for-ten-thousand/"   # instrument 020's third-party corpus
FIXTURE = "/tests/"

ARX = re.compile(r"(?<![\d.])(\d{4}\.\d{4,5})(?:v\d+)?")
DOI = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")


# --------------------------------------------------------------------------- helpers

def git_text(path, pin=PIN):
    """File content at the pinned commit, or None if it is not there / not text."""
    r = subprocess.run(["git", "show", f"{pin}:{path}"], cwd=REPO, capture_output=True)
    if r.returncode != 0:
        return None
    try:
        return r.stdout.decode("utf-8")
    except UnicodeDecodeError:
        return None


def git_files(pin=PIN):
    out = subprocess.run(["git", "ls-tree", "-r", "--name-only", pin], cwd=REPO,
                         capture_output=True, text=True, check=True).stdout
    return [f for f in out.split("\n") if f]


def identifiers(entry):
    """Every identifier the catalogue itself gives for an entry, lower-cased."""
    out = []
    for k in [entry.get("kennung")] + list(entry.get("weitere_kennungen") or []):
        if not k:
            continue
        k = k.strip()
        out.append(k.split(":", 1)[1] if k.lower().startswith("arxiv:") else k)
    url = entry.get("url") or ""
    m = re.search(r"arxiv\.org/abs/(\d{4}\.\d{4,5})", url)
    if m:
        out.append(m.group(1))
    m = re.search(r"doi\.org/(.+)$", url)
    if m:
        out.append(m.group(1))
    return sorted({x.lower() for x in out if x})


def paths_of(entry, prefix=None):
    fs = [f for f in entry.get("fundstellen") or [] if isinstance(f, str)]
    if prefix:
        fs = [f for f in fs if f.startswith(prefix + "/")]
    return fs


def strip_line_suffix(fundstelle):
    """`docs/x.md:29` -> `docs/x.md`. The catalogue uses that form for some entries."""
    return fundstelle.split(":")[0]


def arx_shape_ok(ident):
    """Decidable shape rule. DOIs pass unconditionally; arXiv-shaped strings must have a
    plausible YYMM: year 07 (when the scheme began) to 26 (this year), month 01-12."""
    m = re.fullmatch(r"(\d{2})(\d{2})\.\d{4,5}", ident)
    if not m:
        return True
    yy, mm = int(m.group(1)), int(m.group(2))
    return 7 <= yy <= 26 and 1 <= mm <= 12


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# --------------------------------------------------------------------------- assertions

def check_frozen_input():
    """Refuse to run if the frozen input has drifted from the hash pinned for it.

    Added 2026-07-30 (gauntlet round four) on the Skeptic's condition. Until then this script
    hashed its input only in order to *report* the hash, and never compared it to the pinned
    value — so a tampered or drifted freeze produced a clean exit-0 run with a silently
    different provenance line. `history.py` had enforced this for all five states from the
    start; the script carrying the forward arm did not. The asymmetry survived three gauntlet
    rounds. `--check` proves determinism (a fresh run equals the committed JSON); it does not
    prove that the input is still the documented one, which is what this does.
    """
    manifest = json.load(open(MANIFEST, encoding="utf-8"))
    states = manifest["states"] if isinstance(manifest, dict) else manifest
    pinned = next((s for s in states if s["commit"] == UPSTREAM_COMMIT), None)
    if pinned is None:
        raise SystemExit("FAIL: %s carries no entry for %s" % (MANIFEST, UPSTREAM_COMMIT[:8]))
    actual = sha256(FROZEN)
    if actual != pinned["freeze_sha256"]:
        raise SystemExit(
            "FAIL: the frozen catalogue extract has drifted from its pinned hash.\n"
            "  file:   %s\n  pinned: %s\n  actual: %s" % (FROZEN, pinned["freeze_sha256"], actual))


def build():
    check_frozen_input()
    entries = json.load(open(FROZEN, encoding="utf-8"))
    A = []
    extras = {}

    def add(key, title, value, note):
        A.append({"id": key, "title": title, "value": value, "note": note})

    # --- A1 the object -----------------------------------------------------------
    add("A1", "Entries in the frozen catalogue extract", len(entries),
        "The freeze is the catalogue file at upstream commit %s (2026-07-28T01:41:37+02:00); the "
        "state the seed describes is frozen alongside it at %s (01:01:18) and asserted in A15. "
        "SHA-256 of both freezes are in SOURCES.md. CORRECTION 2026-07-30: until this run, this "
        "note stated that no upstream commit could be pinned because the site repository's "
        "history was not readable from here. That was false and had never been tested; it was "
        "retracted in the prose on 2026-07-28 (SOURCES.md, journal/2026-07-28.md) but survived "
        "unretracted in this machine-readable output for two days. See pin.corrections."
        % (UPSTREAM_COMMIT[:8], SEED_STATE_COMMIT[:8]))

    # --- A2 do the citer labels correspond to the evidence paths? -----------------
    violations = []
    docs_without_mr = 0
    for e in entries:
        labels = set(e.get("zitiert_von") or [])
        prefixes = {p.split("/")[0] for p in paths_of(e)}
        expected = set()
        for lab in labels:
            expected |= LABEL_TO_PREFIX.get(lab, {"<unknown-label:%s>" % lab})
        # every prefix must be claimable by some label, and every label must be evidenced
        unexplained = {p for p in prefixes if not any(p in LABEL_TO_PREFIX.get(l, set())
                                                     for l in labels)}
        unevidenced = {l for l in labels if not (LABEL_TO_PREFIX.get(l, set()) & prefixes)}
        if unexplained or unevidenced:
            violations.append({"id": e["id"], "unexplained_prefixes": sorted(unexplained),
                               "unevidenced_labels": sorted(unevidenced)})
        if "docs" in prefixes and "meridian-runtime" not in prefixes:
            docs_without_mr += 1
    add("A2", "Entries whose citer labels are not matched by their evidence paths",
        len(violations),
        "Tested in both directions: no label without a path under its repository, and no path "
        "under a repository without its label. Bare `docs/` paths never occur without a "
        "`meridian-runtime/` path in the same entry (%d exceptions), which is why they are "
        "counted to that repository rather than to this one. Violations: %s"
        % (docs_without_mr, violations or "none"))

    # --- A3 the checkable arm -----------------------------------------------------
    field_entries = [e for e in entries if "field" in (e.get("zitiert_von") or [])]
    pairs = []
    for e in field_entries:
        for f in paths_of(e, "field-research"):
            pairs.append((e, strip_line_suffix(f)[len("field-research/"):]))
    distinct_paths = sorted({p for _, p in pairs})
    add("A3", "Entries labelled `field`", len(field_entries),
        "These are the only entries whose evidence this practice can hold as ground truth. "
        "They span %d distinct files and %d entry-file pairs."
        % (len(distinct_paths), len(pairs)))

    # --- A4 do the asserted evidence locations resolve? --------------------------
    residue, strict_hits, cache = [], 0, {}
    for e, path in pairs:
        if path not in cache:
            cache[path] = git_text(path)
        body = cache[path]
        if body is None:
            residue.append({"id": e["id"], "path": path, "why": "file not at pin"})
            continue
        low = body.lower()
        ids = identifiers(e)
        hit = [i for i in ids if i in low]
        if not hit:
            residue.append({"id": e["id"], "path": path, "why": "no identifier in file",
                            "looked_for": ids})
            continue
        # stricter reading: the identifier must sit on a line that also names a scheme
        for line in low.split("\n"):
            if any(i in line for i in hit) and ("arxiv" in line or "doi" in line
                                                or "http" in line):
                strict_hits += 1
                break
    add("A4", "Unresolved entry-file pairs at the pinned commit", len(residue),
        "%d of %d pairs resolve: the file exists at %s AND the entry's own identifier occurs "
        "in its text. Under a stricter reading, where the identifier must also share a line "
        "with a scheme name or a URL, %d of %d still resolve — reported so the looseness of "
        "the rule is visible rather than hidden. Residue: %s"
        % (len(pairs) - len(residue), len(pairs), PIN, strict_hits, len(pairs),
           residue or "none"))

    # --- A5 what this repository does not contain --------------------------------
    files = git_files()
    corpora = [f for f in files if f.split("/")[0] == "corpora" or "/corpora/" in f]
    manifests = [f for f in files if os.path.basename(f) == "citations.manifest.json"]
    add("A5", "Files in this repository matching the evidence form attributed to it",
        len(corpora) + len(manifests),
        "Searched all %d files tracked at %s for a `corpora/` path segment or a file named "
        "`citations.manifest.json` — the evidence form the seed of 2026-07-28 addresses to "
        "this practice as \"eure Zitationsmanifeste\". Neither is present. What this "
        "establishes is where the files are NOT; it does not by itself establish who writes "
        "the repository where they are." % (len(files), PIN))

    # --- A6 the arm that cannot be checked from here ------------------------------
    mer = [e for e in entries if "meridian" in (e.get("zitiert_von") or [])]
    mer_resolvable = sum(1 for e in mer if paths_of(e, "field-research"))
    add("A6", "Entries labelled `meridian` whose evidence is checkable from this repository",
        mer_resolvable,
        "%d entries carry that label. Exactly %d of them ALSO carries the `field` label and "
        "an evidence path in this repository, and is already counted and resolved in A3/A4; "
        "the other %d have no evidence path here at all — their `meridian` evidence lies "
        "under `meridian-runtime/` and `docs/`, which this repository does not contain. This "
        "audit therefore makes no claim about whether those back-references resolve, only "
        "that they cannot be resolved from here."
        % (len(mer), mer_resolvable, len(mer) - mer_resolvable))

    # --- A7 where the relevance sentences come from -------------------------------
    herk = collections.Counter(e["relevanz_herkunft"] for e in field_entries)
    add("A7", "Entries labelled `field` whose relevance sentence is a machine judgement",
        herk.get("urteil", 0),
        "Provenance of the relevance sentence across the %d `field` entries: %s. The "
        "catalogue itself discloses this in an `urteil` block; the audit reads that "
        "disclosure, it does not detect it."
        % (len(field_entries), dict(sorted(herk.items()))))

    urteil = [e for e in entries if isinstance(e.get("urteil"), dict)]
    dates = sorted({e["urteil"].get("am") for e in urteil})
    basis = sorted({e["urteil"].get("grundlage") for e in urteil})
    add("A8", "Entries repository-wide carrying a machine-written relevance sentence",
        len(urteil),
        "All of them recorded on date(s) %s, written from %s. The generative model named in "
        "that block is redacted in this practice's freeze and not otherwise reproduced; the "
        "unredacted value is in the source file pinned in SOURCES.md."
        % (dates, basis))

    # --- A9 the sieve, the other direction ----------------------------------------
    where = collections.defaultdict(set)
    skipped = 0
    for f in files:
        body = git_text(f)
        if body is None:
            skipped += 1
            continue
        for m in ARX.findall(body):
            where[m].add(f)
        for m in DOI.findall(body):
            where[m.rstrip(".,);:'\"]").lower()].add(f)

    s0 = set(where)
    s1 = {i for i in s0 if arx_shape_ok(i)}
    s2 = {i for i in s1 if not all(w.startswith(VENDORED) for w in where[i])}
    s3 = {i for i in s2 if not all(FIXTURE in w for w in where[i])}
    cat_ids = set()
    for e in entries:
        cat_ids |= set(identifiers(e))
    carried = sorted(s3 & cat_ids)
    remainder = sorted(s3 - cat_ids)

    add("A9", "Identifier-shaped strings in this repository that the catalogue does not carry",
        len(remainder),
        "A sieve over all %d tracked files at %s (%d undecodable, skipped): %d distinct "
        "identifier-shaped strings; -%d failing a shape rule (arXiv-shaped year 07-26, month "
        "01-12) leaves %d; -%d occurring only inside instrument 020's vendored third-party "
        "register corpus leaves %d; -%d occurring only in synthetic test fixtures leaves %d; "
        "of those, %d are in the catalogue and %d are not. The large exclusions are the "
        "catalogue's, and they are correct: identifiers this practice AUDITED are not "
        "identifiers this practice CITES."
        % (len(files), PIN, skipped, len(s0), len(s0 - s1), len(s1), len(s1 - s2), len(s2),
           len(s2 - s3), len(s3), len(carried), len(remainder)))

    # The same sieve as a structured staircase, so the work's face can render it without any
    # number being retyped from A9's prose.
    extras["sieve"] = [
        {"stage": "identifier-shaped strings in this repository at the pin", "left": len(s0)},
        {"stage": "minus %d failing a decidable shape rule" % len(s0 - s1), "left": len(s1)},
        {"stage": "minus %d occurring only inside a vendored third-party corpus" % len(s1 - s2),
         "left": len(s2)},
        {"stage": "minus %d occurring only in test fixtures" % len(s2 - s3), "left": len(s3)},
        {"stage": "minus %d the catalogue carries" % len(carried), "left": len(remainder)},
    ]

    add("A10", "The remainder, named",
        [{"identifier": i, "in": sorted(where[i])} for i in remainder],
        "Handed back to the catalogue's keeper as candidates, not as errors: some are sources "
        "this practice relies on, some are texts it merely names, and at least one is a defect "
        "in this practice's own record rather than a gap in the catalogue (A11). Whether an "
        "entry belongs in the catalogue is its keeper's judgement, not this practice's.")

    # --- A11 the audit's own house ------------------------------------------------
    bad = "10.3030/101135953"
    bad_files = sorted(where.get(bad, []))
    add("A11", "Files in this repository presenting a non-resolving DOI as a citation",
        len(bad_files),
        "The identifier %s is presented as the citation for \"EU AI Act, Regulation (EU) "
        "2024/1689, Art. 5.1(d)\" in %s — one of which is a SHIPPED work, on its published "
        "face. It came out of this audit's own sieve, not out of a reader's complaint. The "
        "live fetch that established it does not resolve is an out-of-band observation, "
        "recorded with its timestamp in the work's record and deliberately NOT an assertion "
        "here: every assertion in this file is offline and reproducible from the pin."
        % (bad, bad_files))

    # --- A12/A13 who supplied the reason on an entry two practices share? ---------
    solo = collections.defaultdict(collections.Counter)
    for e in entries:
        labels = e.get("zitiert_von") or []
        if len(labels) == 1:
            solo[labels[0]][e["relevanz_herkunft"]] += 1
    add("A12", "Entries carrying one citer label only, by the provenance of their reason",
        {k: dict(sorted(v.items())) for k, v in sorted(solo.items())},
        "`gebrauch` is a template line stating that a practice cited the text and when; "
        "`praxis` is a sentence taken from a practice's own curated list; `urteil` is a "
        "sentence written by a generative model from the abstract. Read on entries that are "
        "one citer's alone, the picture separates: no entry belonging to the `meridian` citer "
        "alone carries anything but the template line.")

    shared = [e for e in entries if len(e.get("zitiert_von") or []) > 1]
    inherited = [e for e in shared if e["relevanz_herkunft"] == "praxis"]
    inherited_with_atelier = [e for e in inherited if "atelier" in e["zitiert_von"]]
    add("A13", "Entries cited by more than one practice, where one reason stands for all of them",
        len(shared),
        "The catalogue carries ONE `relevanz` and ONE `relevanz_herkunft` per entry, not one "
        "per citer. On these %d shared entries the field cannot say WHICH practice supplied "
        "the reason. Of them, %d take their reason from a curated list, and %d of those %d are "
        "shared with the `atelier` citer, whose curated list is among the evidence paths. The "
        "aggregate consequence is measurable: counted across all entries the `meridian` citer "
        "appears to carry %d curated reasons, and every one of them sits on an entry it shares "
        "with another practice."
        % (len(shared), len(inherited), len(inherited_with_atelier), len(inherited),
           sum(1 for e in entries if "meridian" in (e.get("zitiert_von") or [])
               and e["relevanz_herkunft"] == "praxis")))

    # --- A14 the citer this practice is asked about, read the same way ------------
    mer_herk = collections.Counter(e["relevanz_herkunft"] for e in mer)
    mer_empty = sum(1 for e in mer if not (e.get("relevanz") or "").strip())
    mer_praxis_shared = sum(1 for e in mer if e["relevanz_herkunft"] == "praxis"
                            and len(e.get("zitiert_von") or []) > 1)
    add("A14", "Entries of the `meridian` citer carrying no reason, only the usage template",
        mer_herk.get("gebrauch", 0),
        "The seed says of those entries that none carries a reason. Read literally that is not "
        "what the data shows: %d of %d have an EMPTY relevance field, and the breakdown is %s. "
        "Read as the seed evidently means it — a reason ORIGINATING with that citer — it is "
        "exactly right, and provably so: every entry of that citer carrying a reason of any "
        "kind — %d curated, %d machine-written — is an entry it SHARES with another practice, "
        "so not one reason on its own %d solo entries originates with it. What is left on "
        "those is the usage template: this text was used, on this date. Both readings are "
        "reported because the difference between them is the finding."
        % (mer_empty, len(mer), dict(sorted(mer_herk.items())),
           mer_herk.get("praxis", 0), mer_herk.get("urteil", 0),
           sum(1 for e in mer if e.get("zitiert_von") == ["meridian"])))
    solo_mer = [e for e in mer if e.get("zitiert_von") == ["meridian"]]
    if any(e["relevanz_herkunft"] != "gebrauch" for e in solo_mer):
        raise SystemExit("A14: a solo entry of that citer carries a reason of its own, which "
                         "would break the claim in this assertion — recompute before shipping.")

    # --- A15 the same question, at the state the seed itself described -------------
    seed_path = os.path.join(HERE, "sources", "history", "6a032edb.json")
    seed_entries = json.load(open(seed_path, encoding="utf-8"))
    s_mer = [e for e in seed_entries if "meridian" in (e.get("zitiert_von") or [])]
    s_herk = collections.Counter(e["relevanz_herkunft"] for e in s_mer)
    s_solo = [e for e in s_mer if e.get("zitiert_von") == ["meridian"]]
    add("A15", "The same, at the upstream commit the seed's own counts identify",
        {"entries": len(seed_entries), "meridian": len(s_mer),
         "provenance_of_reason": dict(sorted(s_herk.items())),
         "empty_relevance": sum(1 for e in s_mer if not (e.get("relevanz") or "").strip()),
         "solo_entries": len(s_solo),
         "solo_provenance": dict(sorted(collections.Counter(
             e["relevanz_herkunft"] for e in s_solo).items()))},
        "The seed states 206 entries and 139 under that citer. Exactly one upstream commit of "
        "the catalogue file carries those two numbers, and it was committed four minutes before "
        "the seed itself. That state is frozen alongside the current one, so the seed can be "
        "read against what it described rather than against a later file. The pattern is the "
        "same and predates the machine-written sentences entirely: none of that citer's %d solo "
        "entries carried a reason of its own." % len(s_solo))

    return {
        "work": "Back-reference audit of the ecology's Paper Catalogue",
        "practice": "Meridian",
        "status": "DRAFT — NOT SHIPPED as of 2026-07-30 (session 72). Built 2026-07-28. Seven "
                  "reviews have run; six failed, including the last three, each convened against "
                  "the state the previous one's corrections produced. 16 blocking findings plus "
                  "one condition, none of them in the measurement. The work owes one clean "
                  "review. Nothing here may be cited as verified by this practice's own standard "
                  "until that review has run. See GAUNTLET.md and VERIFICATION.md.",
        "pin": {
            "repository_commit": PIN,
            "catalogue_upstream_commit": UPSTREAM_COMMIT,
            "catalogue_seed_state_commit": SEED_STATE_COMMIT,
            "catalogue_freeze_sha256": sha256(FROZEN),
            "note": "Both sides are pinned to commits. The catalogue freeze is additionally "
                    "pinned by content hash; see SOURCES.md for the hashes and the fetch times.",
            "corrections": [
                {
                    "date": "2026-07-30",
                    "retracted": "The catalogue side is pinned by content hash, not by an "
                                 "upstream commit, because this practice's programmatic access "
                                 "does not reach the site repository's history.",
                    "why": "False, and never tested before it was published. The repository "
                           "clones over the plain git protocol; only the platform's JSON API is "
                           "unavailable. Disproved by a role this practice convened on "
                           "2026-07-28 and corrected in the prose the same day — but the "
                           "correction did not reach this file until 2026-07-30.",
                    "replaced_by": "pin.catalogue_upstream_commit, "
                                   "pin.catalogue_seed_state_commit, A1, A15",
                },
            ],
        },
        "caveats": {
            "what_is_checked": "Only the arm of the catalogue whose evidence lies in this "
                               "repository. 138 entries point at a different repository and "
                               "are outside what can be verified from here.",
            "loose_matching": "A4's rule is 'the identifier occurs in the file', which is "
                              "weaker than 'the file cites the work'. The strict count is "
                              "reported inside A4 so the gap is visible.",
            "sieve_is_a_lower_bound": "A9 measures identifier-shaped strings, not citations. "
                                      "It cannot see a source referred to by title alone.",
            "state_travels_with_the_number": "Both sides are states at a time: this repository "
                                             "at one commit, the catalogue at one fetch. The "
                                             "catalogue is described in the record as changing "
                                             "nightly.",
            "not_an_error_report": "A10's remainder is a list of candidates for the "
                                   "catalogue's keeper to judge, not a list of catalogue "
                                   "errors.",
        },
        "assertions": A,
        "sieve": extras["sieve"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="recompute and exit non-zero if it differs from the committed file")
    args = ap.parse_args()
    result = build()
    text = json.dumps(result, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    if args.check:
        if not os.path.exists(OUT):
            print("FAIL: %s does not exist" % OUT)
            return 1
        committed = open(OUT, encoding="utf-8").read()
        if committed != text:
            print("FAIL: results/audit.json differs from a fresh run")
            return 1
        print("OK: results/audit.json is byte-identical to a fresh run")
        return 0
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
    for a in result["assertions"]:
        v = a["value"]
        print("%-4s %-72s %s" % (a["id"], a["title"][:72],
                                 v if not isinstance(v, list) else "%d item(s)" % len(v)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
