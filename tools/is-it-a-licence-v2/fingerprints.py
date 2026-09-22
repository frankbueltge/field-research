#!/usr/bin/env python3
"""The phrase table, the placeholder table and the normalisation.

Session 163, 2026-09-18. Written by hand before any repository blob was read.

Every phrase below is a short quotation from the licence text it identifies, chosen
because it appears in that family and, as far as the author could tell, in no other.
No phrase is longer than it has to be; none is a whole clause where half a sentence
discriminates. `none_of` carries the phrases that rule a family out, which is how
BSD-2 is told from BSD-3 and CC-BY from CC-BY-NC.

No rule in this file calls a model. Identification is exact substring matching on a
normalised string, so a reader can re-derive every verdict from the committed text.
"""
import re

# ---------------------------------------------------------------- normalisation

_QUOTES = {
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "“": '"', "”": '"', "„": '"', "‟": '"',
    "–": "-", "—": "-", "−": "-", " ": " ",
    "﻿": "", "­": "",
}


def normalise(text: str) -> str:
    """Lowercase, fold quotes and dashes, collapse every run of whitespace to one space.

    Deliberately does NOT strip punctuation: the phrases below rely on commas.
    """
    for a, b in _QUOTES.items():
        text = text.replace(a, b)
    return re.sub(r"\s+", " ", text.lower()).strip()


# ---------------------------------------------------------------- the families
#
# any_of : at least one must be present (after normalisation)
# none_of: none may be present
# scored : True  -> the copyright line is inside the operative grant, so L2 applies
#          False -> the canonical text ships a template appendix or carries no
#                   copyright line at all, so L2 is null (amendment 1)

FAMILIES = [
    ("MIT", {
        "any_of": ["permission is hereby granted, free of charge, to any person obtaining a copy "
                   "of this software and associated documentation files"],
        "none_of": [],
        "scored": True,
    }),
    ("ISC", {
        "any_of": ["permission to use, copy, modify, and/or distribute this software for any "
                   "purpose with or without fee is hereby granted"],
        "none_of": [],
        "scored": True,
    }),
    ("BSD-4-Clause", {
        "any_of": ["redistribution and use in source and binary forms, with or without "
                   "modification, are permitted provided that the following conditions are met"],
        "none_of": [],
        "requires_all": ["all advertising materials mentioning features or use of this software "
                         "must display the following acknowledge"],
        "scored": True,
    }),
    ("BSD-3-Clause", {
        "any_of": ["redistribution and use in source and binary forms, with or without "
                   "modification, are permitted provided that the following conditions are met"],
        "requires_all": ["may be used to endorse or promote products derived from this software"],
        "none_of": ["all advertising materials mentioning features or use of this software "
                    "must display the following acknowledge"],
        "scored": True,
    }),
    ("BSD-2-Clause", {
        "any_of": ["redistribution and use in source and binary forms, with or without "
                   "modification, are permitted provided that the following conditions are met"],
        "none_of": ["may be used to endorse or promote products derived from this software",
                    "all advertising materials mentioning features or use of this software "
                    "must display the following acknowledge"],
        "scored": True,
    }),
    ("Zlib", {
        "any_of": ["altered source versions must be plainly marked as such, and must not be "
                   "misrepresented as being the original software"],
        "none_of": [],
        "scored": True,
    }),
    ("Apache-2.0", {
        "any_of": ["terms and conditions for use, reproduction, and distribution",
                   "licensed under the apache license, version 2.0"],
        "none_of": [],
        "scored": False,
    }),
    ("GPL-3.0", {
        "any_of": ["gnu general public license version 3, 29 june 2007"],
        # K1 fired on the first control run: the canonical GPLv3 text NAMES the Affero
        # licence in section 13, so excluding a family by a mere mention of another
        # excluded the canon from itself. Discriminate by the other family's TITLE LINE.
        "none_of": ["gnu lesser general public license version 3, 29 june 2007",
                    "gnu affero general public license version 3, 19 november 2007"],
        "scored": False,
    }),
    ("GPL-2.0", {
        "any_of": ["gnu general public license version 2, june 1991"],
        # Same defect: the canonical GPLv2 text names the Library GPL in its preamble.
        "none_of": ["gnu lesser general public license version 2.1, february 1999",
                    "gnu library general public license version 2, june 1991"],
        "scored": False,
    }),
    ("LGPL-3.0", {
        "any_of": ["gnu lesser general public license version 3, 29 june 2007"],
        "none_of": [],
        "scored": False,
    }),
    ("LGPL-2.1", {
        "any_of": ["gnu lesser general public license version 2.1, february 1999"],
        "none_of": [],
        "scored": False,
    }),
    ("AGPL-3.0", {
        "any_of": ["gnu affero general public license version 3, 19 november 2007"],
        "none_of": [],
        "scored": False,
    }),
    ("MPL-2.0", {
        "any_of": ["mozilla public license version 2.0"],
        "none_of": [],
        "scored": False,
    }),
    ("EPL-2.0", {
        "any_of": ["eclipse public license - v 2.0"],
        "none_of": [],
        "scored": False,
    }),
    ("BSL-1.0", {
        "any_of": ["boost software license - version 1.0"],
        "none_of": [],
        "scored": False,
    }),
    ("Unlicense", {
        "any_of": ["this is free and unencumbered software released into the public domain"],
        "none_of": [],
        "scored": False,
    }),
    ("CC0-1.0", {
        "any_of": ["creative commons legal code cc0 1.0 universal", "cc0 1.0 universal"],
        "none_of": [],
        "scored": False,
    }),
    ("CC-BY-NC-SA-4.0", {
        "any_of": ["attribution-noncommercial-sharealike 4.0 international public license"],
        "none_of": [],
        "scored": False,
    }),
    ("CC-BY-NC-4.0", {
        "any_of": ["attribution-noncommercial 4.0 international public license"],
        "none_of": ["attribution-noncommercial-sharealike 4.0 international public license"],
        "scored": False,
    }),
    ("CC-BY-SA-4.0", {
        "any_of": ["attribution-sharealike 4.0 international public license"],
        "none_of": ["attribution-noncommercial-sharealike 4.0 international public license"],
        "scored": False,
    }),
    ("CC-BY-4.0", {
        "any_of": ["attribution 4.0 international public license"],
        "none_of": ["attribution-noncommercial 4.0 international public license",
                    "attribution-sharealike 4.0 international public license",
                    "attribution-noncommercial-sharealike 4.0 international public license"],
        "scored": False,
    }),
    ("WTFPL", {
        "any_of": ["do what the fuck you want to public license"],
        "none_of": [],
        "scored": False,
    }),
    ("OpenRAIL", {
        "any_of": ["openrail", "responsible ai license"],
        "none_of": [],
        "scored": False,
    }),
    ("Llama-Community", {
        "any_of": ["llama 2 community license agreement", "llama 3 community license agreement",
                   "llama 3.1 community license agreement", "llama 3.2 community license agreement"],
        "none_of": [],
        "scored": False,
    }),
]

FAMILY_NAMES = [n for n, _ in FAMILIES]
SCORED_FAMILIES = {n for n, spec in FAMILIES if spec["scored"]}

# The SPDX identifier whose canonical text each family must be identified from,
# used only by the K1/K3 control. Families with no single SPDX text are absent.
SPDX_CONTROL = {
    "MIT": "MIT", "ISC": "ISC", "BSD-4-Clause": "BSD-4-Clause",
    "BSD-3-Clause": "BSD-3-Clause", "BSD-2-Clause": "BSD-2-Clause", "Zlib": "Zlib",
    "Apache-2.0": "Apache-2.0", "GPL-3.0": "GPL-3.0-only", "GPL-2.0": "GPL-2.0-only",
    "LGPL-3.0": "LGPL-3.0-only", "LGPL-2.1": "LGPL-2.1-only", "AGPL-3.0": "AGPL-3.0-only",
    "MPL-2.0": "MPL-2.0", "EPL-2.0": "EPL-2.0", "BSL-1.0": "BSL-1.0",
    "Unlicense": "Unlicense", "CC0-1.0": "CC0-1.0",
    "CC-BY-NC-SA-4.0": "CC-BY-NC-SA-4.0", "CC-BY-NC-4.0": "CC-BY-NC-4.0",
    "CC-BY-SA-4.0": "CC-BY-SA-4.0", "CC-BY-4.0": "CC-BY-4.0", "WTFPL": "WTFPL",
}

# ---------------------------------------------------------------- placeholders
#
# Matched case-insensitively as substrings, and ONLY inside a line that already
# carries the word "copyright". Every form below is taken from a canonical or
# widely distributed licence template, not invented.

PLACEHOLDERS = [
    "<year>", "<years>", "<yyyy>", "[year]", "[years]", "[yyyy]", "{year}", "{{year}}",
    "<copyright holders>", "<copyright holder>", "[copyright holder]", "[copyright holders]",
    "<copyright-holder>", "[name of copyright owner]", "<name of copyright owner>",
    "[fullname]", "[full name]", "{fullname}", "<fullname>", "<full name>",
    "[name]", "<name>", "[your name]", "<your name>", "your name here",
    "[author]", "<author>", "<name of author>", "[name of author]",
    "[owner]", "<owner>", "[organization]", "<organization>", "[organisation]",
    "<insert", "[insert", "{{", "<>", "[]",
]

# Bare words that are placeholders only as whole words: a holder whose name
# happens to contain 'yyyy' must not fire. Found while writing the fixtures,
# before any repository data existed.
PLACEHOLDER_WORDS = ["yyyy", "xxxx", "yyy", "nnnn"]
_WORD_RE = re.compile(r"(?i)(?<![a-z0-9])(" + "|".join(PLACEHOLDER_WORDS) + r")(?![a-z0-9])")

_COPYRIGHT_LINE = re.compile(r"(?i)\bcopyright\b")
# A NOTICE, not a sentence that happens to contain the word. Added 2026-09-18 after the
# first build run: MIT's own boilerplate — "The above copyright notice and this permission
# notice shall be included in all copies" — was being read as a copyright line with a
# holder, so every MIT file scored 'named' whether or not its real notice was filled in.
# 78 fixtures and 25 mutants passed over that defect; what caught it was disbelieving a
# result of 67 out of 67. A notice's word must begin the line, after comment marks.
_PREFIX = r"[\s#*/;%!<>\-=_|\.'\"\[\u2018\u2019\u201c\u201d]*"
# The word form: Copyright / Copr. — a notice continues with (c), the symbol, a year,
# a bracket or a capital; prose continues with a lowercase word. (Second defect, found
# by hand-reading: Apache-2.0 wraps a sentence so a line BEGINS "copyright notice that
# is included in or attached to the work".)
_NOTICE_WORD = re.compile(_PREFIX + r"(copyright\b|copr\.)", re.I)
_TAIL_WORD = re.compile(r"^[\s,\.:\-]*(\([cC]\)|\u00a9|&copy;|(19|20)\d{2}|[\[<{]|[A-Z0-9])")
# The symbol form. "\u00a9" and "&copy;" take the same tail. The ASCII "(c)" does NOT:
# it is also an enumerated list marker, and Apache-2.0 section 4(c) begins
# "(c) You must retain, in the Source form of any Derivative Works ...", which the rule
# above read as a notice held by "You must retain, in the Source form ...". Third defect
# in this one rule, found the same way as the other two: by disbelieving an output.
# So a bare "(c)" is a notice only when a year or a bracketed template follows it.
_NOTICE_SYM = re.compile(_PREFIX + r"(\u00a9|&copy;)")
_NOTICE_PAREN = re.compile(_PREFIX + r"\(c\)", re.I)
_TAIL_PAREN = re.compile(r"^[\s,\.:\-]*((19|20)\d{2}|[\[<{])")
# Leading matter stripped from a copyright line before asking whether a holder is left.
_STRIP = re.compile(
    r"(?i)^[\s#*/;%!<>\-=_|\.]*"          # comment and rule characters
    r"(copyright\b|\(c\)|\(C\)|©|&copy;|\bc\b)*"
    r"[\s,\.:\-]*"
)
_YEARS = re.compile(r"(?i)\b(19|20)\d{2}\b(\s*[-–,]\s*((19|20)\d{2}|present|now))*")
_TAIL = re.compile(r"(?i)\ball rights reserved\b\.?")


def is_copyright_notice(line: str) -> bool:
    """True for a copyright NOTICE, false for prose or a list item."""
    t = line.strip()
    for head, tail in ((_NOTICE_WORD, _TAIL_WORD), (_NOTICE_SYM, _TAIL_WORD),
                       (_NOTICE_PAREN, _TAIL_PAREN)):
        m = head.match(t)
        if m and tail.match(t[m.end():]):
            return True
    return False


def mentions_copyright(line: str) -> bool:
    """True for any line carrying the word. Kept for the record; not used by L2."""
    return bool(_COPYRIGHT_LINE.search(line))


def copyright_lines(raw_text: str):
    """Every copyright NOTICE in the file, in file order."""
    return [ln.strip() for ln in raw_text.splitlines() if is_copyright_notice(ln)]


def holder_of(line: str) -> str:
    """What is left of a copyright line once the word, the symbol and the years are gone."""
    s = line
    for _ in range(3):                    # 'Copyright (c) Copyright' does occur
        s = _STRIP.sub("", s, count=1)
    s = _YEARS.sub(" ", s)
    s = _TAIL.sub(" ", s)
    s = re.sub(r"(?i)^[\s,\.:\-\(\)]*(c\)|\(c\)|©)?[\s,\.:\-]*", "", s)
    return re.sub(r"\s+", " ", s).strip(" \t,.:;-()[]<>*#/")


def has_placeholder(line: str) -> bool:
    """True if a copyright line carries an unfilled template placeholder."""
    low = line.lower()
    if any(p in low for p in PLACEHOLDERS):
        return True
    return bool(_WORD_RE.search(low))


# ======================================================================== session 167
# Appended by tools/a-repair-is-a-new-rule/variants.py. Nothing above this line is
# edited. With _R1 / _R6 / _R7 all False this block reproduces the shipped rule.

_R1 = False
_R6 = True
_R7 = False

_R1_EVIDENCE = re.compile(r"(?i)\((?:c|C)\)|©|&copy;|\b(?:19|20)\d{2}\b")
_R6_FILLER = re.compile(r"^[\s#*/;%!<>\-=_|\.]*$")
_R7_CUT = re.compile(r"(?i)(?=copyright\b|copr\.|\(c\)|©|&copy;)")
_R7_BLOCK = re.compile(r"\n[ \t]*\n")

_notice_base = is_copyright_notice


def is_copyright_notice(line):                                          # noqa: F811
    """The shipped test, and under R1 a required piece of notice evidence."""
    if not _notice_base(line):
        return False
    if not _R1:
        return True
    return bool(_R1_EVIDENCE.search(line)) or has_placeholder(line)


def _units_physical(raw_text):
    """The shipped scope: one unit per physical line, stripped."""
    return [ln.strip() for ln in raw_text.splitlines()]


def _units_logical(raw_text):
    """R7's scope: each block's lines joined, then cut before every notice marker."""
    out = []
    for block in _R7_BLOCK.split(raw_text):
        joined = " ".join(ln.strip() for ln in block.splitlines() if ln.strip())
        if not joined:
            continue
        for seg in _R7_CUT.split(joined):
            seg = seg.strip()
            if seg:
                out.append(seg)
    return out


def copyright_lines(raw_text):                                          # noqa: F811
    """Every copyright notice in the file, in file order, under this variant's flags."""
    raw_text = raw_text or ""
    units = _units_logical(raw_text) if _R7 else _units_physical(raw_text)
    out = []
    for i, unit in enumerate(units):
        if not is_copyright_notice(unit):
            continue
        found = unit.strip()
        if _R6 and holder_of(found) == "":
            parts = [found]
            for nxt in units[i + 1:i + 4]:
                if not nxt.strip() or _R6_FILLER.match(nxt) or is_copyright_notice(nxt):
                    break
                parts.append(nxt.strip())
                if holder_of(" ".join(parts)):
                    break
            joined = " ".join(parts)
            if holder_of(joined):
                found = joined
        out.append(found)
    return out
