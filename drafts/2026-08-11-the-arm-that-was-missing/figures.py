#!/usr/bin/env python3
"""figures - a figure in prose, carrying the field it came from.

Session 123, 2026-08-16.

WHY THIS EXISTS
---------------
Three consecutive gauntlets failed (sessions 120, 121, 122) and **not one of them failed on a
measurement**. Every blocking finding was a number this practice typed or carried by hand into
its own prose: a self-audit count carried from a run that predated the paragraph, a
re-confirmation time typed instead of read, a speed comparison moving three variables at once.

Session 120 wrote the right rule for the bundle - *no figure in the bundle is typed by a human* -
and enforced it by generating `FIGURES.md` from JSON. It was never extended to the prose AROUND
the bundle, which is where all three failures lived.

`prose_vs_json.py` (session 116) is the existing guard. It asks: does this number occur ANYWHERE
in the draft's machine-written JSON? It says so itself that it cannot catch "a number that is
right for the wrong reason, nor one copied correctly from the wrong row." Both of those have
since happened.

WHAT THIS ADDS
--------------
A figure is never written into prose as a literal. It is fetched:

    fx = Figures()
    fx.n("deliverable-v0.3/reference-baseline.json", "pooled.n")

which reads that field, formats it, and RECORDS the pairing (rendered text -> file + JSON path).
The prose is assembled from the returned strings. `fx.provenance()` then emits, for every figure
that appears in the prose, the exact file and field it was read from.

That turns "is this number in the data?" into "which field is this number, and is that the field
the sentence is about?" - a question a reviewer can check mechanically against the provenance
table, and one a human writing quickly cannot answer wrong without the table saying so.

WHAT IT STILL CANNOT DO, STATED PLAINLY
---------------------------------------
It cannot know whether the SENTENCE around a correctly-fetched figure describes that field
correctly. A figure read from `pooled.n` and introduced as "the number of absent units" is wrong
prose with right provenance. The provenance table makes that checkable by a reviewer in one pass;
it does not make it impossible. Nothing here removes the need for the gauntlet.
"""
import json
import math
import os
import re


class MissingField(Exception):
    """A prose figure asked for a field that is not in the file. Never falls back to a literal."""


def dig(obj, path):
    """`a.b[0].c` -> the value. Raises MissingField rather than returning a default, because a
    default is exactly the silent wrong number this module exists to prevent."""
    cur = obj
    for seg in re.findall(r"[^.\[\]]+|\[\d+\]", path):
        if seg.startswith("["):
            i = int(seg[1:-1])
            if not isinstance(cur, list) or i >= len(cur):
                raise MissingField(f"{path}: no index {i}")
            cur = cur[i]
        else:
            if not isinstance(cur, dict) or seg not in cur:
                raise MissingField(f"{path}: no key {seg!r}")
            cur = cur[seg]
    return cur


class Figures:
    def __init__(self, relative_to=None):
        """`relative_to`: a directory. Provenance records paths relative to it, so the table a
        receiver reads names files the way they sit in the bundle, and two builds of the same
        bundle into different directories produce the same provenance."""
        self._cache = {}
        self._prov = []
        self._rel = relative_to

    def _load(self, path):
        if path not in self._cache:
            self._cache[path] = json.load(open(path))
        return self._cache[path]

    def _record(self, rendered, file, jpath, note):
        shown = file
        if self._rel and file != "(literal)":
            shown = os.path.relpath(file, self._rel)
        self._prov.append({"rendered": rendered, "file": shown, "json_path": jpath,
                           "note": note})
        return rendered

    # -- renderers. Each one reads, formats, records, and returns a string. ----------------
    def raw(self, file, jpath, note=""):
        """A value rendered exactly as it sits in the file (strings, dates, identifiers)."""
        return self._record(str(dig(self._load(file), jpath)), file, jpath, note)

    def n(self, file, jpath, note=""):
        """An integer count, thousands-separated."""
        v = dig(self._load(file), jpath)
        if not isinstance(v, int):
            raise MissingField(f"{jpath}: expected an integer, found {type(v).__name__}")
        return self._record(f"{v:,}", file, jpath, note)

    def pct(self, file, jpath, dp=2, note=""):
        """A proportion in [0,1] rendered as a percentage."""
        v = dig(self._load(file), jpath)
        if v is None:
            raise MissingField(f"{jpath}: null, and a null has no percentage")
        return self._record(f"{100.0 * v:.{dp}f} %", file, jpath, note)

    def num(self, file, jpath, dp=4, note=""):
        v = dig(self._load(file), jpath)
        if v is None:
            raise MissingField(f"{jpath}: null")
        return self._record(f"{v:.{dp}f}", file, jpath, note)

    def sci(self, file, jpath, dp=4, note=""):
        """A p-value or other small number in scientific notation, written the way this arc
        writes them: 7.6558 x 10^-10."""
        v = dig(self._load(file), jpath)
        if v is None:
            raise MissingField(f"{jpath}: null")
        if v == 0:
            return self._record("0", file, jpath, note)
        e = int(math.floor(math.log10(abs(v))))
        m = v / (10 ** e)
        return self._record(f"{m:.{dp}f} × 10<sup>{e}</sup>", file, jpath, note)

    def ci(self, file, jpath, dp=2, note=""):
        """A [lo, hi] interval rendered as percentages."""
        v = dig(self._load(file), jpath)
        if not (isinstance(v, list) and len(v) == 2) or v[0] is None:
            raise MissingField(f"{jpath}: not a two-element interval")
        return self._record(f"{100.0 * v[0]:.{dp}f} %–{100.0 * v[1]:.{dp}f} %",
                            file, jpath, note)

    def count(self, file, jpath, note=""):
        """len() of a list or dict in the file - a count the file implies rather than states."""
        v = dig(self._load(file), jpath)
        if not isinstance(v, (list, dict)):
            raise MissingField(f"{jpath}: not a list or dict, cannot be counted")
        return self._record(f"{len(v):,}", file, jpath, note + " (len)")

    def key(self, file, parent_jpath, key_name, note=""):
        """A dict KEY used as a label in prose - a measurement-day label, an age-band label.

        These are data: they name which run or which band a row is. Rendering them with `lit`
        would file them as human-typed constants, which is the opposite of true. This verifies
        the key is actually present under `parent_jpath` and records where it was read.
        """
        parent = dig(self._load(file), parent_jpath)
        if not isinstance(parent, dict) or key_name not in parent:
            raise MissingField(f"{parent_jpath}: no key {key_name!r}")
        return self._record(str(key_name), file, f"{parent_jpath}.<key>", note)

    def lit(self, text, why):
        """A number that is deliberately NOT read from a file - a date in a sentence, a section
        number, a figure quoted from an outside source. Recorded with the reason, so the audit
        can tell a declared literal from an undeclared one."""
        return self._record(str(text), "(literal)", "-", why)

    def provenance(self):
        return {
            "schema": "field-research/figure-provenance/1",
            "written_by": "figures.py, session 123",
            "what_this_is": ("every figure that appears in the generated prose of this bundle, "
                             "with the file and JSON field it was read from. A figure not in "
                             "this table was typed by a human and is a defect."),
            "n_figures": len(self._prov),
            "figures": self._prov,
        }

    def write(self, path):
        json.dump(self.provenance(), open(path, "w"), indent=1)


# -- the auditor -------------------------------------------------------------------------
# A number as a CLAIM. The trailing group requires digits after the point, so the sentence-final
# period of "...version 0.1." is not swallowed into the token (which made the first run of this
# auditor report `16.` as an unmatched figure - a defect in the auditor, not in the prose).
NUM = re.compile(r"(?<![A-Za-z0-9])\d[\d,]*(?:\.\d+)?")
ISO = re.compile(r"\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}Z)?")

# Markdown structure that is made of digits but asserts nothing: heading numbers, ordered-list
# markers, section cross-references. Removed before scanning, and named here so "what the audit
# does not look at" is a stated list rather than a silence.
STRUCTURE = [
    (re.compile(r"^#{1,6}\s+\d+\.", re.M), "heading number"),
    (re.compile(r"^\s*\d+\.\s", re.M), "ordered-list marker"),
    (re.compile(r"§+\s*\d+(?:\s*(?:,|and)\s*\d+)*"), "section cross-reference"),
    (re.compile(r"^\|[\s\-|:]+\|$", re.M), "table rule"),
]


def audit_prose(prose_paths, provenance_path, allow_substrings=()):
    """Every number in the generated prose must be a rendered figure from the provenance table.

    A number survives the audit only if it was produced by `Figures` - either fetched from a JSON
    field, or declared a literal through `.lit()` with a stated reason. Skipped, because they are
    addresses and not claims: fenced code, inline code (paths, field names), URLs, markdown
    structure (see STRUCTURE), and digits inside a word (`sha256`, `AS396982`).

    Returns a report dict; the caller decides what to do with a non-zero count.
    """
    prov = json.load(open(provenance_path))
    rendered = set()
    for f in prov["figures"]:
        r = f["rendered"]
        rendered.add(r)
        for m in ISO.findall(r):
            rendered.add(m)
            rendered.update(NUM.findall(m))
        for m in NUM.findall(r):
            rendered.add(m)
            rendered.add(m.replace(",", ""))

    report = {"schema": "field-research/prose-figure-audit/2",
              "provenance": provenance_path,
              "n_rendered_tokens": len(rendered),
              "not_scanned": [why for _, why in STRUCTURE] + ["fenced code", "inline code",
                                                              "URLs", "digits inside a word"],
              "files": [], "n_unmatched_total": 0}
    for p in prose_paths:
        text = open(p).read()
        text = re.sub(r"```.*?```", " ", text, flags=re.S)     # code blocks are not claims
        text = re.sub(r"`[^`]*`", " ", text)                    # inline code: paths, fields
        text = re.sub(r"https?://\S+", " ", text)               # URLs are addresses
        for rx, _ in STRUCTURE:
            text = rx.sub(" ", text)
        unmatched = []
        for m in ISO.finditer(text):                            # whole dates, checked as wholes
            if m.group(0) not in rendered:
                ctx = text[max(0, m.start() - 60):m.end() + 60].replace("\n", " ")
                unmatched.append({"token": m.group(0), "kind": "date", "context": ctx})
        text = ISO.sub(" ", text)                               # then out of the way
        for m in NUM.finditer(text):
            tok = m.group(0)
            if tok in rendered or tok.replace(",", "") in rendered:
                continue
            if any(s in tok for s in allow_substrings):
                continue
            ctx = text[max(0, m.start() - 60):m.end() + 60].replace("\n", " ")
            unmatched.append({"token": tok, "kind": "number", "context": ctx})
        report["files"].append({"file": p, "n_unmatched": len(unmatched),
                                "unmatched": unmatched})
        report["n_unmatched_total"] += len(unmatched)
    return report
