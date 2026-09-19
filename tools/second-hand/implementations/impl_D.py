"""
Text-measurement instrument for software-licence identification and
copyright-attribution scoring.

L1 -- "identified": a hand-written table of short, distinctive operative
phrases, one to four per licence family, each chosen (to the author's best
knowledge of these texts) to appear in no other family's canonical text.
Matching is done against a normalised copy of the input (lowercased, all
runs of whitespace collapsed to a single space, curly quotes folded to
straight quotes) using plain substring containment. A file matching more
than one family's phrases is reported as a multi-family match, never
silently resolved to one.

The BSD 2/3/4-Clause family is a special case: the three variants share a
common textual core (the two "redistributions of source/binary form"
clauses), so a pure inclusion-only phrase table cannot tell them apart --
the phrase that identifies 3-Clause ("neither the name ... nor the names of
its contributors ... endorse or promote") is *also* present verbatim inside
4-Clause. That family is therefore identified with the shared core phrase
plus explicit exclusion logic (presence/absence of the advertising clause
and the endorsement clause), exactly as the specification's own guidance
anticipates for "the BSD clause counts".

L2 -- "attributed": evaluated only for the families whose canonical text
carries the copyright line inside the user-facing grant itself (MIT, ISC,
BSD-2/3/4-Clause, Zlib). For every other family (including Apache-2.0,
whose only copyright line lives in an appendix nobody is expected to edit)
the rung is not applicable and reported as None, never False.

Deciding what counts as a "copyright line" (as opposed to a sentence of
prose that merely mentions the word): the instrument scans the text line by
line and only treats a line as a candidate if it contains a copyright
marker (the word "copyright" as a whole word, case-insensitively, or the
"(c)"/"c"-style, or the "©" symbol) *immediately followed, after only
punctuation/whitespace, by something that occupies the year slot* -- either
an actual four-digit year (optionally a range/list of years) or one of the
well-known unfilled year-placeholder spellings ("<year>", "[year]",
"[yyyy]", "yyyy", "xxxx"). A bare mention of the word "copyright" in running
prose with no year-shaped token right after it (e.g. "this program respects
copyright law") is deliberately not treated as a copyright line at all, and
is not enough by itself to produce any of the four attribution outcomes.
Once a line qualifies, whatever trails the year token is the holder
candidate: empty (after stripping punctuation) means "no_holder"; matching
one of the placeholder patterns (bracket/angle-bracket forms, or well-known
template words like "your name", "copyright holder(s)", "name of copyright
owner", "John Doe", "TODO", and the like) means "placeholder"; anything
else is treated as a real, filled-in holder and reported as "named". If no
line in the whole file qualifies as a copyright line at all, the outcome is
"no_copyright_line". Where a file has several qualifying lines with
different outcomes, "named" wins over "placeholder", which wins over
"no_holder", on the theory that if a genuine holder is named anywhere the
file has, in fact, been attributed.
"""

import re

# ---------------------------------------------------------------------------
# Normalisation (for L1 phrase matching only)
# ---------------------------------------------------------------------------

_WS_RE = re.compile(r"\s+")

_CURLY_QUOTE_MAP = str.maketrans({
    "‘": "'",  # left single quote
    "’": "'",  # right single quote / apostrophe
    "‚": "'",  # single low-9 quote
    "‛": "'",  # single high-reversed-9 quote
    "′": "'",  # prime
    "“": '"',  # left double quote
    "”": '"',  # right double quote
    "„": '"',  # double low-9 quote
    "‟": '"',  # double high-reversed-9 quote
    "″": '"',  # double prime
})


def _normalize(text):
    if not isinstance(text, str):
        text = "" if text is None else str(text)
    t = text.translate(_CURLY_QUOTE_MAP)
    t = t.lower()
    t = _WS_RE.sub(" ", t)
    return t.strip()


# ---------------------------------------------------------------------------
# L1 -- distinctive-phrase table
# ---------------------------------------------------------------------------
# Each phrase below is, to the best of the author's own knowledge of these
# licence texts, a substring that appears in no family other than the one
# it is filed under. BSD-2/3/4-Clause are handled separately below because
# their shared core makes a pure phrase table insufficient on its own.

_SIMPLE_PHRASES = {
    "MIT": [
        'to deal in the software without restriction, including without '
        'limitation the rights to use, copy, modify, merge, publish, '
        'distribute, sublicense',
        'permission is hereby granted, free of charge, to any person '
        'obtaining a copy of this software and associated documentation '
        'files (the "software"), to deal',
    ],
    "ISC": [
        'permission to use, copy, modify, and/or distribute this software '
        'for any purpose with or without fee is hereby granted',
    ],
    "Zlib": [
        'the origin of this software must not be misrepresented',
        'altered source versions must be plainly marked as such, and must '
        'not be misrepresented as being the original software',
    ],
    "Apache-2.0": [
        'apache license version 2.0, january 2004',
        'licensed under the apache license, version 2.0',
        'warranties or conditions of title, non-infringement, '
        'merchantability, or fitness for a particular purpose',
    ],
    "GPL-3.0": [
        'gnu general public license version 3, 29 june 2007',
        'gnu general public license as published by the free software '
        'foundation, either version 3 of the license',
    ],
    "GPL-2.0": [
        'gnu general public license version 2, june 1991',
        'gnu general public license as published by the free software '
        'foundation; either version 2 of the license',
    ],
    "LGPL-3.0": [
        'gnu lesser general public license version 3, 29 june 2007',
        'gnu lesser general public license as published by the free '
        'software foundation, either version 3 of the license',
    ],
    "LGPL-2.1": [
        'gnu lesser general public license version 2.1, february 1999',
        'gnu lesser general public license as published by the free '
        'software foundation; either version 2.1 of the license',
        'gnu library general public license',
    ],
    "AGPL-3.0": [
        'gnu affero general public license version 3, 19 november 2007',
        'gnu affero general public license as published by the free '
        'software foundation, either version 3 of the license',
        'your modified version must prominently offer all users '
        'interacting with it remotely through a computer network',
    ],
    "MPL-2.0": [
        'mozilla public license, v. 2.0',
        'this source code form is subject to the terms of the mozilla '
        'public license',
    ],
    "EPL-2.0": [
        'eclipse public license - v 2.0',
        'is made available under the terms of the eclipse public license 2.0',
        'eclipse public license v. 2.0',
    ],
    "BSL-1.0": [
        'boost software license - version 1.0 - august 17th, 2003',
        'boost software license',
    ],
    "Unlicense": [
        'this is free and unencumbered software released into the public '
        'domain',
    ],
    "CC0-1.0": [
        'creative commons legal code cc0 1.0 universal',
        'has dedicated the work to the public domain by waiving all of his '
        'or her rights to the work',
    ],
    "CC-BY-NC-SA-4.0": [
        'creative commons attribution-noncommercial-sharealike 4.0 '
        'international',
    ],
    "CC-BY-NC-4.0": [
        'creative commons attribution-noncommercial 4.0 international',
    ],
    "CC-BY-SA-4.0": [
        'creative commons attribution-sharealike 4.0 international',
    ],
    "CC-BY-4.0": [
        'creative commons attribution 4.0 international',
    ],
    "WTFPL": [
        'do what the fuck you want to public license',
    ],
    "OpenRAIL": [
        'openrail',
        'open rail license',
        'responsible ai license',
    ],
    "Llama-Community": [
        'llama community license agreement',
        'llama 2 community license agreement',
        'llama 3 community license agreement',
        'llama materials',
    ],
}

# The CC-BY-* phrases above are exclusive of one another by construction:
# normalisation never removes the hyphen that immediately follows
# "attribution" in the -SA / -NC / -NC-SA variants, so e.g. the plain
# "creative commons attribution 4.0 international" phrase (space right
# after "attribution") cannot occur as a substring of
# "creative commons attribution-sharealike 4.0 international" (hyphen right
# after "attribution").

_BSD_CORE_PHRASES = (
    'redistribution and use in source and binary forms',
    'must retain the above copyright notice',
    'must reproduce the above copyright notice',
)
_BSD_ADVERTISING_PHRASE = (
    'all advertising materials mentioning features or use of this software '
    'must display the following acknowledgement'
)
_BSD_ENDORSE_PHRASE = 'endorse or promote products derived from this software'


def _detect_bsd_variant(norm):
    if not all(p in norm for p in _BSD_CORE_PHRASES):
        return None
    has_advertising = _BSD_ADVERTISING_PHRASE in norm
    has_endorse = _BSD_ENDORSE_PHRASE in norm
    if has_advertising:
        return "BSD-4-Clause"
    if has_endorse:
        return "BSD-3-Clause"
    return "BSD-2-Clause"


def _detect_families(norm):
    found = set()
    for family, phrases in _SIMPLE_PHRASES.items():
        for phrase in phrases:
            if phrase in norm:
                found.add(family)
                break
    bsd = _detect_bsd_variant(norm)
    if bsd is not None:
        found.add(bsd)
    return found


# ---------------------------------------------------------------------------
# L2 -- attribution (copyright-line) detection
# ---------------------------------------------------------------------------

_SCORED_FAMILIES = frozenset({
    "MIT", "ISC", "BSD-2-Clause", "BSD-3-Clause", "BSD-4-Clause", "Zlib",
})

_MARKER_RE = re.compile(r'copyright\b|©', re.IGNORECASE)

# Strips an optional "(c)"/"(C)"/"c"/"©" repeat-marker (with optional
# surrounding brackets/punctuation) that often follows the word "copyright"
# itself, e.g. "Copyright (c) 2020 ...".
_CMARK_RE = re.compile(r'^[\s:.\-–—]*[(\[]?\s*(?:c|©)\s*[)\]]?', re.IGNORECASE)

_YEAR_RE = re.compile(
    r'((?:19|20)\d{2})(\s*[-–—/,]\s*(?:(?:19|20)?\d{2}))*'
)

# Unfilled placeholders that occupy the *year* slot itself.
_YEAR_PLACEHOLDER_RE = re.compile(
    r'^[\s:.\-–—]*[<\[]?\s*(?:yyyy|year)\s*[>\]]?',
    re.IGNORECASE,
)
_XXXX_YEAR_RE = re.compile(r'^[\s:.\-–—]*x{4}\b', re.IGNORECASE)

# Unfilled placeholders that occupy the *holder* slot. Deliberately broad
# ("and the like"): any bracketed/angle-bracketed token is treated as a
# template slot, plus the specific well-known spellings the canonical
# licence texts themselves use.
_HOLDER_PLACEHOLDER_PATTERNS = [
    re.compile(r'<[^<>]{0,60}>'),
    re.compile(r'\[[^\[\]]{0,60}\]'),
    re.compile(r'\byour\s+name\b', re.IGNORECASE),
    re.compile(r'\byour\s+(company|organi[sz]ation)\b', re.IGNORECASE),
    re.compile(r'\bcopyright\s+holders?\b', re.IGNORECASE),
    re.compile(r'\bcopyright\s+owners?\b', re.IGNORECASE),
    re.compile(r'\bname\s+of\s+copyright\s+owner\b', re.IGNORECASE),
    re.compile(r'\bfull\s*name\b', re.IGNORECASE),
    re.compile(r"\bauthor'?s?\s+name\b", re.IGNORECASE),
    re.compile(r'\bowner\s+name\b', re.IGNORECASE),
    re.compile(r'\bcompany\s+name\b', re.IGNORECASE),
    re.compile(r'\borgani[sz]ation\s+name\b', re.IGNORECASE),
    re.compile(r'\bjohn\s+doe\b', re.IGNORECASE),
    re.compile(r'\bjane\s+doe\b', re.IGNORECASE),
    re.compile(r'\bexample\s+(inc|corp|company|organi[sz]ation)\b', re.IGNORECASE),
    re.compile(r'\bacme\b', re.IGNORECASE),
    re.compile(r'\btodo\b', re.IGNORECASE),
    re.compile(r'\btbd\b', re.IGNORECASE),
    re.compile(r'\bn/?a\b', re.IGNORECASE),
    re.compile(r'^\s*x{4}\s*$', re.IGNORECASE),
    re.compile(r'\binsert\s+(your\s+)?name\b', re.IGNORECASE),
    re.compile(r'\bfirst\s*last\b', re.IGNORECASE),
]

_STRIP_CHARS = " \t.,;:-–—()[]<>\"'"


def _looks_like_placeholder_holder(candidate):
    stripped = candidate.strip()
    if not stripped:
        return False
    for pattern in _HOLDER_PLACEHOLDER_PATTERNS:
        if pattern.search(stripped):
            return True
    return False


def _detect_attribution(text):
    outcomes = set()
    for line in text.split('\n'):
        marker = _MARKER_RE.search(line)
        if not marker:
            continue
        tail = line[marker.end():]
        stripped_tail = _CMARK_RE.sub('', tail, count=1)
        if stripped_tail == tail:
            # no (c)/© repeat-marker found right after; still fine, just
            # move on to the year slot directly.
            pass
        tail = stripped_tail.lstrip()

        if _YEAR_PLACEHOLDER_RE.match(tail) or _XXXX_YEAR_RE.match(tail):
            outcomes.add("placeholder")
            continue

        year_match = _YEAR_RE.search(tail)
        if not year_match:
            # No year and no recognised year-placeholder: this line does
            # not match the "copyright + year + holder" shape at all, so
            # it is not treated as a copyright line (e.g. prose that
            # merely uses the word "copyright").
            continue

        holder_candidate = tail[year_match.end():]
        holder_candidate = holder_candidate.strip(_STRIP_CHARS)

        if not holder_candidate:
            outcomes.add("no_holder")
        elif _looks_like_placeholder_holder(holder_candidate):
            outcomes.add("placeholder")
        else:
            outcomes.add("named")

    if "named" in outcomes:
        return "named"
    if "placeholder" in outcomes:
        return "placeholder"
    if "no_holder" in outcomes:
        return "no_holder"
    return "no_copyright_line"


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def score(text: str) -> dict:
    """Returns {"families": [...], "attribution": <str or None>}"""
    try:
        if not isinstance(text, str):
            text = "" if text is None else str(text)

        norm = _normalize(text)
        families = _detect_families(norm)

        if families & _SCORED_FAMILIES:
            attribution = _detect_attribution(text)
        else:
            attribution = None

        return {"families": sorted(families), "attribution": attribution}
    except Exception:
        return {"families": [], "attribution": None}
