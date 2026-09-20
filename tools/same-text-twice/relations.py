#!/usr/bin/env python3
"""The metamorphic relations of session 165, exactly as pre-registered.

Each function takes the source text and returns the follow-up text. Every one of
them is an EQUALITY relation: the claim is that the pinned rule's whole verdict
tuple must be identical on both, because nothing a reader would use to decide what
the document grants, or who grants it, has changed.

M4 is the negative control: it must change nothing.
M9 is declared unscored — it probes a scope the 2026-09-18 rung never claimed.

No function here calls a model. Every transformation is a pure string operation and
is re-derivable from this file.
"""
import re
import textwrap

# ------------------------------------------------------------------ M1
_M1 = re.compile(r"\((c|C)\)")


def m1_marker_case(t: str) -> str:
    """(c) <-> (C). Both spellings are in universal use in copyright notices."""
    return _M1.sub(lambda m: "(C)" if m.group(1) == "c" else "(c)", t)


# ------------------------------------------------------------------ M2
_M2 = re.compile(r"\((?:c|C)\)|©")


def m2_marker_form(t: str) -> str:
    """(c)/(C) -> the symbol, and the symbol -> (c). One simultaneous pass."""
    return _M2.sub(lambda m: "(c)" if m.group(0) == "©" else "©", t)


# ------------------------------------------------------------------ M3
def m3_crlf(t: str) -> str:
    """The same file checked out on a different operating system."""
    return t.replace("\r\n", "\n").replace("\n", "\r\n")


# ------------------------------------------------------------------ M4  (control)
def m4_indent(t: str) -> str:
    """Four spaces before every non-empty line. The pre-registered negative control."""
    return "\n".join(("    " + ln) if ln.strip() else ln for ln in t.split("\n"))


# ------------------------------------------------------------------ M5
def m5_typography(t: str) -> str:
    """Straight quotes to curly, a spaced hyphen to an en dash.

    `fingerprints.normalise()` folds exactly these characters, so it claims this
    blindness in its own docstring.
    """
    t = t.replace("'", "’").replace('"', "”")
    return t.replace(" - ", " – ")


# ------------------------------------------------------------------ M6
def m6_rewrap(t: str) -> str:
    """Every paragraph reflowed to 64 columns; blank lines kept where they were."""
    out, para = [], []

    def flush():
        if para:
            joined = " ".join(x.strip() for x in para)
            out.extend(textwrap.wrap(joined, width=64) or [""])
            para.clear()

    for ln in t.split("\n"):
        if ln.strip():
            para.append(ln)
        else:
            flush()
            out.append("")
    flush()
    return "\n".join(out)


# ------------------------------------------------------------------ M7
def m7_bom(t: str) -> str:
    """A byte-order mark and a blank line, as an editor leaves them."""
    return "﻿\n" + t


# ------------------------------------------------------------------ M8
def m8_trailing(t: str) -> str:
    """Two trailing spaces on every line. Trailing whitespace carries no meaning."""
    return "\n".join(ln + "  " for ln in t.split("\n"))


# ------------------------------------------------------------------ M9  (unscored)
def m9_comment(t: str) -> str:
    """The same licence pasted into a source-file header. Reported as scope, never
    counted as a defect: the 2026-09-18 rung was only applied to licence FILES."""
    return "\n".join(("# " + ln) if ln.strip() else "#" for ln in t.split("\n"))


SCORED = [
    ("M1", "marker case (c) <-> (C)", m1_marker_case),
    ("M2", "marker form (c) <-> ©", m2_marker_form),
    ("M3", "LF -> CRLF", m3_crlf),
    ("M4", "four-space indent (control)", m4_indent),
    ("M5", "typographic punctuation", m5_typography),
    ("M6", "re-wrap to 64 columns", m6_rewrap),
    ("M7", "BOM and a leading blank line", m7_bom),
    ("M8", "trailing whitespace", m8_trailing),
]

UNSCORED = [("M9", "comment-marker decoration", m9_comment)]
ALL = SCORED + UNSCORED
CONTROL = "M4"
