#!/usr/bin/env python3
"""The Correction That Arrives Too Late — first move on joint inquiry ji-2026-001.

Offline, deterministic, no network, no clock. Implements RULE.md exactly; every
threshold and word list below is the one committed in RULE.md before any number
existed. Run from the repository root:

    python3 drafts/2026-08-03-the-correction-that-arrives-too-late/measure.py

Writes results.json next to this file and prints a summary. Exits non-zero if the
pinned commit cannot be confirmed.
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
REGISTER = os.path.join(ROOT, "memory", "discarded.md")
JOURNAL_DIR = os.path.join(ROOT, "journal")
SELF_DIR = os.path.relpath(HERE, ROOT)

# ---------------------------------------------------------------- RULE.md §3.1
LEDGER_VERBS = ["ledger", "ledgered", "logged", "recorded", "added", "entered",
                "row", "rows", "entry", "entries", "dated"]
NEGATIONS = ["owed", "to be", "not yet", "will be", "should be", "no row",
             "without a row", "never"]

# ---------------------------------------------------------------- RULE.md §4.3
# DEVIATION D5 (RULE.md §7): the pre-registered keyword list did not cover this
# register's own wording for the 2026-07-21 event — its rows say "lost in the
# 2026-07-21 history purge" and contain none of the five listed keywords. Checked by
# hand before the list was widened: journal/2026-07-22.md:38–42 records that the purge
# WAS the removal of names from git history, i.e. the same rights-sensitive event.
# "purge"/"purged" are therefore added to the exclusion list.
RIGHTS_EXCLUSIONS = ["redact", "redaction", "redacted", "legal-hygiene redaction",
                     "name removed", "purge", "purged"]

# ---------------------------------------------------------------- RULE.md §4.6
MARKERS = ["withdraw", "withdrawn", "retract", "erratum", "errata", "superseded",
           "supersedes", "discarded", "correction", "corrected", "rejected",
           "no longer", "not a claim", "in error", "was wrong", "struck"]

# DEVIATION D6 (RULE.md §7): `.svg` added — this archive has shipped verbatim quoted
# text inside SVG, so the pre-registered set had a blind spot by construction.
SURFACE_EXT = {".md", ".json", ".astro", ".py", ".html", ".txt", ".csv", ".svg"}

# A surface's class, for the breakdown required by pre-read finding 7: journal prose
# narrating a correction almost always carries marker vocabulary, so pooling it with
# shipped surfaces would flatter the archive.
def surface_class(path):
    if path.startswith("journal/"):
        return "journal"
    if path.startswith("works/") or path.startswith("deliveries/"):
        return "shipped"
    if path.startswith("memory/"):
        return "curated-memory"
    if path.startswith("drafts/"):
        return "drafts"
    if path.startswith("archive/"):
        return "archive"
    return "other"


MIN_KEY_CHARS = 30
MIN_KEY_WORDS = 4
NEIGHBOURHOOD = 10

# DEVIATION D7 (RULE.md §7): number words extended one–twenty; the pre-registered list
# stopped at twelve and would have silently skipped a larger stated count.
NUMBER_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
                "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
                "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
                "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
                "twenty": 20}

STOPWORDS = {"the", "and", "that", "this", "with", "from", "which", "were", "been",
             "have", "into", "than", "then", "they", "them", "their", "there",
             "those", "these", "session", "sessions", "discarded", "ledgered",
             "logged", "recorded", "added", "entered", "rows", "entry", "entries",
             "memory", "journal", "collective", "because", "before", "after"}


def git(*args):
    return subprocess.run(["git", "-C", ROOT] + list(args),
                          capture_output=True, text=True, check=True).stdout


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


# ============================================================ the register
def sessions_in(text):
    """Every session number named in a string (RULE.md §3.3, §3.2)."""
    out = []
    for m in re.finditer(r"sessions?\s*[-‑]?\s*(\d{1,3})\s*(?:[–—-]\s*(\d{1,3}))?",
                         text, re.I):
        a = int(m.group(1))
        out.append(a)
        if m.group(2):
            b = int(m.group(2))
            if b > a and b - a < 30:
                out.extend(range(a + 1, b + 1))
    return out


def parse_register(text):
    """Register entries: table rows (RULE.md §4.1) and dated-section bullets."""
    entries = []
    lines = text.split("\n")
    section = None
    bullet = None

    def flush_bullet():
        nonlocal bullet
        if bullet is not None:
            body = "\n".join(bullet["lines"]).strip()
            if body:
                entries.append({"kind": "bullet", "section": bullet["section"],
                                "line": bullet["line"], "text": body,
                                "date_cell": bullet["section"] or ""})
            bullet = None

    for i, line in enumerate(lines, start=1):
        if line.startswith("#"):
            flush_bullet()
            section = line.lstrip("#").strip() if re.search(r"session", line, re.I) else None
            continue
        if line.startswith("|"):
            flush_bullet()
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not cells or set(line) <= set("|-: "):
                continue
            if cells[0].lower() in ("what", "where it lived", "claim", "what was said"):
                continue
            date_cell = cells[-1]
            entries.append({"kind": "row", "section": section, "line": i,
                            "text": " | ".join(cells), "date_cell": date_cell})
            continue
        if section and re.match(r"^-\s+\S", line):
            flush_bullet()
            bullet = {"section": section, "line": i, "lines": [line]}
            continue
        if bullet is not None:
            if line.strip() == "" and bullet["lines"][-1].strip() == "":
                flush_bullet()
            else:
                bullet["lines"].append(line)
    flush_bullet()

    for e in entries:
        e["sessions"] = sessions_in(e["date_cell"]) or sessions_in(e["section"] or "")
        e["primary"] = e["sessions"][0] if e["sessions"] else None
    return entries


# ============================================================ limb A
def journal_sessions(lines):
    """Map line index -> session number of the nearest preceding session heading.

    DEVIATION D2 (see RULE.md §7): the rule said `# Session NN`. Only 20 of the 31
    journal files use that heading; the rest write `# Journal — DATE (collective
    session NN)`, `# Collective session NN` or `# Session — DATE (collective session
    NN)`. Any level-1 heading naming a session now attributes, taking the last
    session number on the heading line.
    """
    out = []
    cur = None
    for line in lines:
        if line.startswith("# "):
            nums = re.findall(r"session\s*[-‑]?\s*(\d{1,3})", line, re.I)
            if nums:
                cur = int(nums[-1])
        out.append(cur)
    return out


def count_claim(line):
    """A stated quantity of register rows/entries on an announcement line (§3.5).

    DEVIATION D3 (see RULE.md §7): the pre-registered pattern read the NN of
    "the session-33 journal entry stands as minutes" as a claim of 33 rows. A number
    immediately preceded by "session"/"session-" is an identifier, not a quantity,
    and is now skipped.
    """
    pat = (r"(?<!session )(?<!session-)\b(\d{1,2}|" + "|".join(NUMBER_WORDS) + r")\b"
           r"(?:[^.;]{0,40}?)\b(rows?|entries|entry)\b")
    m = re.search(pat, line, re.I)
    if not m:
        return None
    tok = m.group(1).lower()
    return int(tok) if tok.isdigit() else NUMBER_WORDS[tok]


def tokens(text):
    """Distinctive lowercase tokens of a line, for the corroboration signal (D8)."""
    words = re.findall(r"[A-Za-z][A-Za-z0-9'’\-]{5,}", text.lower())
    return {w for w in words if w not in STOPWORDS}


def limb_a(register_sessions, register_by_session, register_text_by_session):
    announcements = []
    for name in sorted(os.listdir(JOURNAL_DIR)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(JOURNAL_DIR, name)
        lines = read(path).split("\n")
        heads = journal_sessions(lines)
        for i, line in enumerate(lines):
            if "discarded.md" not in line:
                continue
            low = line.lower()
            if not any(re.search(r"\b" + v + r"\b", low) for v in LEDGER_VERBS):
                continue
            if any(n in low for n in NEGATIONS):
                announcements.append({"file": name, "line": i + 1, "text": line.strip(),
                                      "verdict": "EXCLUDED-BY-NEGATION",
                                      "sessions": [], "attribution": None})
                continue
            named = sessions_in(line)
            attribution = "on-line" if named else "heading"
            sess = named or ([heads[i]] if heads[i] is not None else [])
            own = heads[i]
            # DEVIATION D3 (RULE.md §7), pre-read finding 2: a line inside session X's
            # minutes that names session Y is that session's *commentary on another
            # session*, not its own announcement. It is tagged and excluded from the
            # counted set instead of being merged into session Y's record.
            retrospective = bool(named) and own is not None and own not in named
            if not sess:
                verdict = "UNATTRIBUTABLE"
            elif retrospective:
                verdict = "RETROSPECTIVE-COMMENTARY"
            else:
                missing = [s for s in sess if s not in register_sessions]
                verdict = "REACHED" if not missing else "NOT-REACHED"
            rec = {"file": name, "line": i + 1, "text": line.strip(),
                   "sessions": sess, "attribution": attribution,
                   "own_session": own, "verdict": verdict}
            if verdict == "NOT-REACHED":
                rec["missing"] = [s for s in sess if s not in register_sessions]
            # DEVIATION D8 (RULE.md §7), pre-read finding 12: a disclosed secondary
            # signal that narrows the session-granularity ceiling of §3.5 — do any
            # distinctive words of the announcement recur in the register rows filed
            # under that session? Reported, never used to overturn the verdict above.
            if verdict in ("REACHED", "NOT-REACHED"):
                atoks = tokens(line)
                rtoks = set()
                for s in sess:
                    rtoks |= tokens(register_text_by_session.get(s, ""))
                shared = sorted(atoks & rtoks)
                rec["corroboration"] = {"shared_tokens": len(shared),
                                        "sample": shared[:8],
                                        "signal": "CORROBORATED" if len(shared) >= 2
                                        else "NOT-CORROBORATED"}
            n = count_claim(line)
            if n is not None and len(sess) == 1 and sess[0] is not None:
                actual = len(register_by_session.get(sess[0], []))
                rec["count_claim"] = {"claimed": n, "actual_rows_for_session": actual,
                                      "verdict": "COUNT-MATCH" if n == actual else "COUNT-MISMATCH"}
            announcements.append(rec)
    return announcements


# ============================================================ limb B
QUOTE_PATTERNS = [r"“([^“”]+)”", r"\"([^\"]+)\"", r"`([^`]+)`"]
FILEISH = re.compile(r"\S+\.(md|py|json|astro|html|txt|csv|sh)\b")


def key_strings(text):
    keys = []
    for pat in QUOTE_PATTERNS:
        for m in re.finditer(pat, text):
            s = m.group(1).strip()
            if len(s) < MIN_KEY_CHARS:
                continue
            if len(s.split()) < MIN_KEY_WORDS:
                continue
            if "http" in s or FILEISH.search(s):
                continue
            if any(mk in s.lower() for mk in MARKERS):
                continue
            keys.append(s)
    return sorted(set(keys))


def surfaces():
    files = git("ls-files").strip().split("\n")
    out = []
    for f in files:
        if os.path.splitext(f)[1] not in SURFACE_EXT:
            continue
        if f == "memory/discarded.md":
            continue
        if f.startswith(SELF_DIR + os.sep) or f.startswith(SELF_DIR + "/"):
            continue
        out.append(f)
    return sorted(out)


def scan(keys, files):
    """Exact, case-sensitive substring search; classify each occurrence (§4.5–4.6).

    DEVIATION D4 (RULE.md §7), pre-read finding 4: occurrences are deduplicated by
    (file, line, character offset), not by (key, file). Where two key strings overlap
    at the same location — which this register produces, because successive rounds
    re-quote overlapping spans of one sentence — the location counts **once**, and
    every key that matched it is listed on that one occurrence.
    """
    occ = {}          # (file, line, offset) -> occurrence record
    for f in files:
        try:
            text = read(os.path.join(ROOT, f))
        except (UnicodeDecodeError, OSError):
            continue
        lines = None
        lowered = None
        for k in keys:
            if k not in text:
                continue
            if lines is None:
                lines = text.split("\n")
                lowered = [ln.lower() for ln in lines]
            for i, ln in enumerate(lines):
                start = ln.find(k)
                while start != -1:
                    ident = (f, i + 1, start)
                    rec = occ.get(ident)
                    if rec is None:
                        lo = max(0, i - NEIGHBOURHOOD)
                        hi = min(len(lines), i + NEIGHBOURHOOD + 1)
                        nb = "\n".join(lowered[lo:hi])
                        marked = sorted({mk for mk in MARKERS if mk in nb})
                        rec = {"file": f, "line": i + 1, "offset": start,
                               "surface_class": surface_class(f),
                               "marked_in_place": bool(marked),
                               "markers": marked, "keys": []}
                        occ[ident] = rec
                    if k not in rec["keys"]:
                        rec["keys"].append(k)
                    start = ln.find(k, start + 1)
    return sorted(occ.values(), key=lambda r: (r["file"], r["line"], r["offset"]))


# ============================================================ main
def main():
    head = git("rev-parse", "HEAD").strip()
    dirty = git("status", "--porcelain").strip()

    register_text = read(REGISTER)
    entries = parse_register(register_text)

    register_sessions = set()
    register_by_session = {}
    register_text_by_session = {}
    for e in entries:
        for s in e["sessions"]:
            register_sessions.add(s)
            register_text_by_session[s] = register_text_by_session.get(s, "") + " " + e["text"]
        if e["primary"] is not None:
            register_by_session.setdefault(e["primary"], []).append(e["line"])
    for m in re.finditer(r"^#{2,3}\s+.*$", register_text, re.M):
        for s in sessions_in(m.group(0)):
            register_sessions.add(s)

    announcements = limb_a(register_sessions, register_by_session, register_text_by_session)

    excluded_rights = [e for e in entries
                       if any(x in e["text"].lower() for x in RIGHTS_EXCLUSIONS)]
    checkable = [e for e in entries if e not in excluded_rights]

    keys = {}
    for e in checkable:
        for k in key_strings(e["text"]):
            keys.setdefault(k, []).append({"line": e["line"], "kind": e["kind"],
                                           "sessions": e["sessions"]})
    files = surfaces()
    occurrences = scan(sorted(keys), files)

    # DEVIATION D9 (RULE.md §7), pre-read finding 5: the headline unit is pre-committed
    # here as WITHDRAWAL-level — how many register entries have at least one occurrence
    # that is unmarked in its own document — with the occurrence count as detail only.
    by_key = {}
    for o in occurrences:
        for k in o["keys"]:
            by_key.setdefault(k, []).append(o)
    entry_lines = {}      # register entry line -> set of its key strings
    for k, srcs in keys.items():
        for s in srcs:
            entry_lines.setdefault(s["line"], set()).add(k)
    entries_unmarked, entries_with_any_occurrence = [], []
    for line, ks in sorted(entry_lines.items()):
        occs = [o for k in ks for o in by_key.get(k, [])]
        if occs:
            entries_with_any_occurrence.append(line)
        if any(not o["marked_in_place"] for o in occs):
            entries_unmarked.append(line)

    by_class = {}
    for o in occurrences:
        c = by_class.setdefault(o["surface_class"], {"total": 0, "unmarked": 0})
        c["total"] += 1
        if not o["marked_in_place"]:
            c["unmarked"] += 1

    unmarked = {}
    for k, occs in by_key.items():
        u = [o for o in occs if not o["marked_in_place"]]
        if u:
            unmarked[k] = u
    entries_with_keys = len(entry_lines)

    counted = [a for a in announcements
               if a["verdict"] in ("REACHED", "NOT-REACHED")]
    results = {
        "pinned_commit": head,
        "working_tree_clean": dirty == "",
        "rule": "drafts/2026-08-03-the-correction-that-arrives-too-late/RULE.md",
        "register": {
            "path": "memory/discarded.md",
            "entries_parsed": len(entries),
            "rows": sum(1 for e in entries if e["kind"] == "row"),
            "bullets": sum(1 for e in entries if e["kind"] == "bullet"),
            "entries_with_no_session_attribution":
                sum(1 for e in entries if not e["sessions"]),
            "sessions_present": sorted(register_sessions),
            "entries_excluded_by_rights_rule": len(excluded_rights),
        },
        "limb_a": {
            "announcements_found": len(announcements),
            "excluded_by_negation": sum(1 for a in announcements
                                        if a["verdict"] == "EXCLUDED-BY-NEGATION"),
            "excluded_as_retrospective_commentary":
                sum(1 for a in announcements
                    if a["verdict"] == "RETROSPECTIVE-COMMENTARY"),
            "unattributable": sum(1 for a in announcements
                                  if a["verdict"] == "UNATTRIBUTABLE"),
            "counted": len(counted),
            "reached": sum(1 for a in counted if a["verdict"] == "REACHED"),
            "not_reached": sum(1 for a in counted if a["verdict"] == "NOT-REACHED"),
            "count_claims": sum(1 for a in announcements if "count_claim" in a),
            "count_mismatch": sum(1 for a in announcements
                                  if a.get("count_claim", {}).get("verdict") == "COUNT-MISMATCH"),
            "corroboration_not_corroborated":
                sum(1 for a in announcements
                    if a.get("corroboration", {}).get("signal") == "NOT-CORROBORATED"),
            "records": announcements,
        },
        "limb_b": {
            "headline_unit": "register entries with at least one occurrence unmarked "
                             "in its own document (RULE.md §7, deviation D9)",
            "entries_checkable": len(checkable),
            "entries_yielding_a_key_string": entries_with_keys,
            "entries_with_any_occurrence": len(entries_with_any_occurrence),
            "entries_with_an_unmarked_occurrence": len(entries_unmarked),
            "entry_lines_with_an_unmarked_occurrence": entries_unmarked,
            "key_strings": len(keys),
            "surfaces_searched": len(files),
            "occurrences": len(occurrences),
            "occurrences_marked_in_place": sum(1 for o in occurrences if o["marked_in_place"]),
            "occurrences_unmarked": sum(1 for o in occurrences if not o["marked_in_place"]),
            "by_surface_class": by_class,
            "keys_with_unmarked_occurrences": len(unmarked),
            "keys_with_no_occurrence_anywhere": sum(1 for k in keys if k not in by_key),
            "unmarked_detail": {k: unmarked[k] for k in sorted(unmarked)},
            "all_occurrences": occurrences,
        },
    }

    out = os.path.join(HERE, "results.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False, sort_keys=False)
        fh.write("\n")

    r = results
    print(f"pinned commit      : {head}  (working tree clean: {r['working_tree_clean']})")
    print(f"register entries   : {r['register']['entries_parsed']} "
          f"({r['register']['rows']} rows + {r['register']['bullets']} bullets); "
          f"rights-excluded {r['register']['entries_excluded_by_rights_rule']}")
    a = r["limb_a"]
    print(f"limb A             : {a['counted']} announcements counted — "
          f"{a['reached']} reached, {a['not_reached']} NOT reached "
          f"({a['excluded_by_negation']} excluded by negation, "
          f"{a['excluded_as_retrospective_commentary']} retrospective commentary, "
          f"{a['unattributable']} unattributable)")
    print(f"limb A count claims: {a['count_claims']} stated, {a['count_mismatch']} mismatched; "
          f"{a['corroboration_not_corroborated']} of {a['counted']} not corroborated by content")
    b = r["limb_b"]
    print(f"limb B             : {b['key_strings']} key strings from "
          f"{b['entries_yielding_a_key_string']} of {b['entries_checkable']} entries; "
          f"{b['surfaces_searched']} surfaces")
    print(f"limb B HEADLINE    : {b['entries_with_an_unmarked_occurrence']} of "
          f"{b['entries_with_any_occurrence']} register entries with any occurrence have at "
          f"least one occurrence unmarked in its own document")
    print(f"limb B occurrences : {b['occurrences']} deduplicated "
          f"({b['occurrences_marked_in_place']} marked in place, "
          f"{b['occurrences_unmarked']} unmarked) — by surface class: "
          + ", ".join(f"{k} {v['unmarked']}/{v['total']}"
                      for k, v in sorted(b['by_surface_class'].items())))
    print(f"wrote {os.path.relpath(out, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
