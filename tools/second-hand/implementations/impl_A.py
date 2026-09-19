"""
License-text measurement instrument.

L1 ("identified"): a hand-written table of short, distinctive operative
phrases per licence family. A phrase only goes in the table if it is a
sentence (or clause) that appears, verbatim, in that family's own canonical
text and in no other family's canonical text. Where two families share a
long common preamble (the BSD family) or a common notice skeleton (the
GPL/LGPL/AGPL family), plain substring membership is not enough to tell them
apart on its own, so those two family groups are resolved with a small,
explicit combination of inclusion/exclusion checks built only from phrases
that are themselves each unique to the clause they signal (the advertising
clause, the endorsement clause, the "Lesser"/"Affero" qualifiers, the
version-2/2.1/3 wording). Every other family is a flat substring test.

L2 ("attributed"): evaluated only for the families whose canonical text asks
the *user* to fill in a copyright line inside the operative grant: MIT, ISC,
BSD-2/3/4-Clause and Zlib. For every other identified family the rung is not
applicable and the result is None (never False) -- this includes eventual
Apache-2.0 identifications, whose own appendix boilerplate
"Copyright [yyyy] [name of copyright owner]" is explicitly excluded from
scoring by the specification's amendment.

A "copyright line" is deliberately defined narrowly: a physical line whose
content, once any leading comment syntax (#, //, /*, *, ;, <!--, --, etc.)
is stripped, *begins* with the word "Copyright" (or "Copr." or the "(c)"/"©"
copyright mark) followed by a year or year range and then a holder. This is
meant to exclude ordinary prose that merely mentions the word "copyright"
in passing (e.g. "This copyright policy explains ..."), which would satisfy
a bare substring search for the word but is not what the specification means
by "a line".
"""

import re

# ---------------------------------------------------------------------------
# L1: normalisation
# ---------------------------------------------------------------------------

_CURLY_QUOTES_TABLE = str.maketrans({
    "‘": "'", "’": "'", "‚": "'", "′": "'",
    "“": '"', "”": '"', "„": '"', "″": '"',
})

_WS_RE = re.compile(r"\s+")


def _normalize(text):
    t = text.translate(_CURLY_QUOTES_TABLE)
    t = t.lower()
    t = _WS_RE.sub(" ", t)
    return t.strip()


# ---------------------------------------------------------------------------
# L1: phrase table
# ---------------------------------------------------------------------------

# BSD family: the first two clauses are shared verbatim across the 2/3/4
# clause variants, so family membership within "BSD" is decided by which
# additional clauses are present, not by the shared preamble alone.
_BSD_BASE_1 = (
    "redistribution and use in source and binary forms, with or without "
    "modification, are permitted provided that the following conditions "
    "are met"
)
_BSD_BASE_2 = "redistributions in binary form must reproduce the above copyright notice"
_BSD_ADV = (
    "all advertising materials mentioning features or use of this software "
    "must display the following acknowledgement"
)
_BSD_ENDORSE = (
    "may be used to endorse or promote products derived from this software "
    "without specific prior written permission"
)

_PHRASES = {
    "MIT": [
        "to deal in the software without restriction, including without "
        "limitation the rights to use, copy, modify, merge, publish, "
        "distribute, sublicense, and/or sell copies of the software",
        "permission is hereby granted, free of charge, to any person "
        "obtaining a copy of this software and associated documentation files",
    ],
    "ISC": [
        "permission to use, copy, modify, and/or distribute this software "
        "for any purpose with or without fee is hereby granted",
    ],
    "Zlib": [
        "the origin of this software must not be misrepresented; you must "
        "not claim that you wrote the original software",
        "altered source versions must be plainly marked as such, and must "
        "not be misrepresented as being the original software",
    ],
    "Apache-2.0": [
        'licensed under the apache license, version 2.0 (the "license"); '
        "you may not use this file except in compliance with the license.",
        'distributed under the license is distributed on an "as is" basis, '
        "without warranties or conditions of any kind, either express or implied.",
    ],
    "GPL-3.0": [
        "gnu general public license as published by the free software "
        "foundation, either version 3 of the license, or (at your option) "
        "any later version",
        "gnu general public license version 3, 29 june 2007",
    ],
    "GPL-2.0": [
        "gnu general public license as published by the free software "
        "foundation; either version 2 of the license, or (at your option) "
        "any later version",
        "gnu general public license version 2, june 1991",
    ],
    "LGPL-3.0": [
        "gnu lesser general public license as published by the free "
        "software foundation; either version 3 of the license, or (at your "
        "option) any later version",
        "gnu lesser general public license as published by the free "
        "software foundation, either version 3 of the license, or (at your "
        "option) any later version",
        "gnu lesser general public license version 3, 29 june 2007",
    ],
    "LGPL-2.1": [
        "gnu lesser general public license as published by the free "
        "software foundation; either version 2.1 of the license, or (at "
        "your option) any later version",
        "gnu lesser general public license version 2.1, february 1999",
    ],
    "AGPL-3.0": [
        "gnu affero general public license as published by the free "
        "software foundation, either version 3 of the license, or (at your "
        "option) any later version",
        "gnu affero general public license version 3, 19 november 2007",
    ],
    "MPL-2.0": [
        "this source code form is subject to the terms of the mozilla "
        "public license, v. 2.0.",
        "if a copy of the mpl was not distributed with this file, you can "
        "obtain one at http://mozilla.org/mpl/2.0/",
    ],
    "EPL-2.0": [
        "eclipse public license - v 2.0",
        "eclipse public license 2.0 which is available at "
        "http://www.eclipse.org/legal/epl-2.0",
        "eclipse public license 2.0 which is available at "
        "https://www.eclipse.org/legal/epl-2.0",
    ],
    "BSL-1.0": [
        "boost software license - version 1.0 - august 17th, 2003",
        "obtaining a copy of the software and accompanying documentation "
        "covered by this license",
    ],
    "Unlicense": [
        "this is free and unencumbered software released into the public domain",
        "in jurisdictions that recognize copyright laws, the author or "
        "authors of this software dedicate any and all copyright interest "
        "in the software to the public domain",
    ],
    "CC0-1.0": [
        "cc0 1.0 universal",
        "the person who associated a work with this deed has dedicated the "
        "work to the public domain by waiving all of his or her rights to "
        "the work worldwide under copyright law",
        "creativecommons.org/publicdomain/zero/1.0",
    ],
    # The Creative Commons 4.0 family names are mutually exclusive as plain
    # substrings once hyphenation is taken into account: "Attribution 4.0
    # International" never occurs inside "Attribution-ShareAlike 4.0
    # International" etc., because the character immediately after
    # "attribution" differs (a space vs. a hyphen).
    "CC-BY-NC-SA-4.0": [
        "attribution-noncommercial-sharealike 4.0 international",
    ],
    "CC-BY-NC-4.0": [
        "attribution-noncommercial 4.0 international",
    ],
    "CC-BY-SA-4.0": [
        "attribution-sharealike 4.0 international",
    ],
    "CC-BY-4.0": [
        "attribution 4.0 international",
    ],
    "WTFPL": [
        "do what the fuck you want to public license",
    ],
    "OpenRAIL": [
        "creativeml open rail-m license",
        "bigscience rail license",
        "open rail++-m license",
        "responsible ai license",
    ],
    "Llama-Community": [
        '"llama materials" means, collectively',
        "llama 2 community license agreement",
        "llama 3 community license agreement",
        "meta llama 3 community license agreement",
    ],
}

SCORED_FAMILIES = {"MIT", "ISC", "BSD-2-Clause", "BSD-3-Clause", "BSD-4-Clause", "Zlib"}


def _identify_bsd(norm):
    fams = set()
    if _BSD_BASE_1 in norm and _BSD_BASE_2 in norm:
        if _BSD_ADV in norm:
            fams.add("BSD-4-Clause")
        elif _BSD_ENDORSE in norm:
            fams.add("BSD-3-Clause")
        else:
            fams.add("BSD-2-Clause")
    return fams


def _identify_families(norm):
    fams = set()
    for fam, phrases in _PHRASES.items():
        for p in phrases:
            if p in norm:
                fams.add(fam)
                break
    fams |= _identify_bsd(norm)
    return fams


# ---------------------------------------------------------------------------
# L2: copyright-line detection
# ---------------------------------------------------------------------------

# Strip common leading comment syntax so that "// Copyright ..." or
# " * Copyright ..." or "<!-- Copyright ..." still counts as *beginning*
# with the copyright marker once comment decoration is discounted.
_LEADING_COMMENT_RE = re.compile(r"^[\s#*/<>!;\-]+")

_COPYRIGHT_LINE_RE = re.compile(
    r"(?i)^(?:copyright|copr\.?|©)\s*(?:\(\s*c\s*\)|©)?\s*"
    r"(?:(?P<yearph>[<\[]?\s*(?:yyyy|xxxx|year)\s*[>\]]?)"
    r"|(?P<yearnum>\d{4}(?:\s*[-–—/]\s*\d{2,4})?"
    r"(?:\s*(?:,|and)\s*\d{4}(?:\s*[-–—/]\s*\d{2,4})?)*))"
    r"\s*[,.\-:]?\s*"
    r"(?P<holder>.*)$"
)

_TRAILING_RIGHTS_RE = re.compile(r"(?i)all rights reserved\.?\s*$")
_TRAILING_COMMENT_RE = re.compile(r'(\*/|-->|"""|\'\'\')\s*$')

# Placeholder holder patterns: bracketed forms (<year>, [fullname], <OWNER>,
# ...) are caught generically by the "contains a bracket character" check in
# _classify_line; these cover the un-bracketed, word-based placeholders that
# canonical texts and common templates use ("xxxx", "your name", "TBD", the
# literal words "owner"/"author"/"name" left standing alone, and the like).
_HOLDER_PLACEHOLDER_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"copyright\s*holders?",
        r"full\s*name",
        r"name of copyright owner",
        r"\byour\s*name\b",
        r"\bname\b\s*$",
        r"\bowner\b\s*$",
        r"\bauthor\b\s*$",
        r"\bcompany name\b",
        r"\borgani[sz]ation\b\s*$",
        r"john doe",
        r"jane doe",
        r"insert\s*(?:your\s*)?name(\s*here)?",
        r"\btbd\b",
        r"\bfixme\b",
        r"\btodo\b",
        r"\bxxxx?\b",
        r"placeholder",
        r"\bexample\b\s*$",
    ]
]


def _clean_holder(holder):
    h = holder.strip()
    h = _TRAILING_RIGHTS_RE.sub("", h).strip()
    h = _TRAILING_COMMENT_RE.sub("", h).strip()
    h = h.strip(" \t.,;:*\"'-")
    return h


def _classify_line(line):
    stripped = _LEADING_COMMENT_RE.sub("", line).strip()
    m = _COPYRIGHT_LINE_RE.match(stripped)
    if not m:
        return None
    if m.group("yearph") is not None:
        return "placeholder"
    holder = _clean_holder(m.group("holder") or "")
    if not holder:
        return "no_holder"
    if any(ch in holder for ch in "<>[]{}"):
        return "placeholder"
    for pat in _HOLDER_PLACEHOLDER_PATTERNS:
        if pat.search(holder):
            return "placeholder"
    return "named"


def _evaluate_attribution(original_text):
    results = set()
    for line in original_text.splitlines():
        cls = _classify_line(line)
        if cls is not None:
            results.add(cls)
    if not results:
        return "no_copyright_line"
    if "named" in results:
        return "named"
    if "placeholder" in results:
        return "placeholder"
    if "no_holder" in results:
        return "no_holder"
    return "no_copyright_line"


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def score(text: str) -> dict:
    """Returns {"families": [...], "attribution": <str or None>}"""
    try:
        if not isinstance(text, str):
            return {"families": [], "attribution": None}
        norm = _normalize(text)
        fams = _identify_families(norm)
        families_list = sorted(fams)
        if fams & SCORED_FAMILIES:
            attribution = _evaluate_attribution(text)
        else:
            attribution = None
        return {"families": families_list, "attribution": attribution}
    except Exception:
        return {"families": [], "attribution": None}
