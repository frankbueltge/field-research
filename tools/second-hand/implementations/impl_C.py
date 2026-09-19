"""
Text-measurement instrument for open-source / open-content licence identification (L1)
and copyright-attribution scoring (L2).

Implements the specification given to the author verbatim:

  L1 - identified: normalise the text (lowercase, collapse whitespace, fold curly
       quotes to straight) and test for the presence of a small, hand-written table
       of short, distinctive operative phrases, each chosen so that it appears in the
       canonical text of exactly one licence family and no other family represented
       here. Multiple hits are reported as multiple families ("multi-family"), never
       silently resolved to one. Failure to match anything is "not identified by this
       instrument", not evidence of absence of a licence -- so this module never
       tries to be clever/fuzzy about L1; it only ever grows more phrases.

  L2 - attributed: for the families whose canonical text embeds the copyright line
       inside the operative grant (MIT, ISC, BSD-2/3/4-Clause, Zlib) -- and ONLADY
       for those -- look for a line of the shape `copyright <year(s)> <holder>` and
       classify the holder as a real name ("named"), an unfilled template
       ("placeholder"), missing entirely ("no_holder"), or report that no such line
       exists at all ("no_copyright_line"). For every other family the rung is not
       applicable and the result is None, never False.

Pure standard library, no side effects at import time, never raises.
"""

from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# L1: normalisation
# ---------------------------------------------------------------------------

_QUOTE_MAP = str.maketrans({
    "‘": "'",  # left single quote
    "’": "'",  # right single quote / apostrophe
    "‚": "'",  # single low-9 quote
    "‛": "'",  # single high-reversed-9 quote
    "′": "'",  # prime
    "“": '"',  # left double quote
    "”": '"',  # right double quote
    "„": '"',  # double low-9 quote
    "‟": '"',  # double high-reversed-9 quote
    "«": '"',  # left guillemet
    "»": '"',  # right guillemet
    "″": '"',  # double prime
})

_WS_RE = re.compile(r"\s+")


def _normalize(text: str) -> str:
    """lowercase, fold curly quotes to straight, collapse all whitespace runs to one space"""
    if not text:
        return ""
    t = text.lower()
    t = t.translate(_QUOTE_MAP)
    t = _WS_RE.sub(" ", t)
    return t.strip()


# ---------------------------------------------------------------------------
# L1: phrase table
# ---------------------------------------------------------------------------
# Each family maps to a list of 1-4 phrases. A family is "identified" if ANY of
# its phrases is an exact substring of the normalised text. Phrases are written
# from memory of each licence's own canonical text and picked specifically to
# avoid appearing in any *other* family kept in this table.

_MIT_PHRASES = [
    'permission is hereby granted, free of charge, to any person obtaining a copy '
    'of this software and associated documentation files (the "software"), to deal '
    'in the software without restriction, including without limitation the rights '
    'to use, copy, modify, merge, publish, distribute, sublicense, and/or sell '
    'copies of the software',
]

_ISC_PHRASES = [
    'permission to use, copy, modify, and/or distribute this software for any '
    'purpose with or without fee is hereby granted, provided that the above '
    'copyright notice and this permission notice appear in all copies',
]

_ZLIB_PHRASES = [
    'permission is granted to anyone to use this software for any purpose, '
    'including commercial applications, and to alter it and redistribute it '
    'freely, subject to the following restrictions',
    'the origin of this software must not be misrepresented; you must not claim '
    'that you wrote the original software',
]

_BSD_COND1 = 'redistributions of source code must retain the above copyright notice'
_BSD_COND2 = ('redistributions in binary form must reproduce the above copyright '
              'notice')
_BSD_ADVERTISING = [
    'all advertising materials mentioning features or use of this software must '
    'display the following acknowledgement',
    'all advertising materials mentioning features or use of this software must '
    'display the following acknowledgment',
]
_BSD_ENDORSE = [
    'may not be used to endorse or promote products derived from this software '
    'without specific prior written permission',
    'may not be used to endorse or promote products derived from this software '
    'without the specific prior written permission',
]

_APACHE2_PHRASES = [
    'licensed under the apache license, version 2.0 (the "license"); you may not '
    'use this file except in compliance with the license',
    'unless required by applicable law or agreed to in writing, software '
    'distributed under the license is distributed on an "as is" basis, without '
    'warranties or conditions of any kind, either express or implied',
]

_GPL2_PHRASES = [
    'gnu general public license as published by the free software foundation; '
    'either version 2 of the license, or (at your option) any later version',
]

_GPL3_PHRASES = [
    'gnu general public license as published by the free software foundation, '
    'either version 3 of the license, or (at your option) any later version',
]

_LGPL21_PHRASES = [
    'gnu lesser general public license as published by the free software '
    'foundation; either version 2.1 of the license, or (at your option) any '
    'later version',
    'this license, the lesser general public license, applies to some specific '
    'designated software packages',
]

_LGPL3_PHRASES = [
    'gnu lesser general public license as published by the free software '
    'foundation, either version 3 of the license, or (at your option) any later '
    'version',
    'incorporates the terms and conditions of version 3 of the gnu general '
    'public license, supplemented by the additional permissions listed',
]

_AGPL3_PHRASES = [
    'gnu affero general public license as published by the free software '
    'foundation, either version 3 of the license, or (at your option) any later '
    'version',
    'remote network interaction; use with the gnu general public license',
]

_MPL2_PHRASES = [
    'this source code form is subject to the terms of the mozilla public '
    'license, v. 2.0. if a copy of the mpl was not distributed with this file, '
    'you can obtain one at http://mozilla.org/mpl/2.0/',
]

_EPL2_PHRASES = [
    'this program and the accompanying materials are made available under the '
    'terms of the eclipse public license 2.0 which is available at '
    'http://www.eclipse.org/legal/epl-2.0',
    'eclipse public license - v 2.0',
]

_BSL1_PHRASES = [
    'boost software license - version 1.0 - august 17th, 2003',
    'permission is hereby granted, free of charge, to any person or organization '
    'obtaining a copy of the software and accompanying documentation covered by '
    'this license',
]

_UNLICENSE_PHRASES = [
    'this is free and unencumbered software released into the public domain',
    'in jurisdictions that recognize copyright laws, the author or authors of '
    'this software dedicate any and all copyright interest in the software to '
    'the public domain',
]

_CC0_PHRASES = [
    'has waived all copyright and related or neighboring rights',
    'dedicated the work to the public domain by waiving all of his or her '
    'rights to the work worldwide under copyright law',
    'creativecommons.org/publicdomain/zero/1.0',
]

_WTFPL_PHRASES = [
    'do what the fuck you want to public license',
    '0. you just do what the fuck you want to',
]

_CC_BY_4_PHRASES = [
    'creative commons attribution 4.0 international public license',
    'creative commons attribution 4.0 international license',
    'creativecommons.org/licenses/by/4.0',
]

_CC_BY_SA_4_PHRASES = [
    'creative commons attribution-sharealike 4.0 international public license',
    'creative commons attribution-sharealike 4.0 international license',
    'creativecommons.org/licenses/by-sa/4.0',
]

_CC_BY_NC_4_PHRASES = [
    'creative commons attribution-noncommercial 4.0 international public license',
    'creative commons attribution-noncommercial 4.0 international license',
    'creativecommons.org/licenses/by-nc/4.0',
]

_CC_BY_NC_SA_4_PHRASES = [
    'creative commons attribution-noncommercial-sharealike 4.0 international '
    'public license',
    'creative commons attribution-noncommercial-sharealike 4.0 international '
    'license',
    'creativecommons.org/licenses/by-nc-sa/4.0',
]

_LLAMA_PHRASES = [
    'llama 2 community license agreement',
    'llama 3 community license agreement',
    'llama 3.1 community license agreement',
    'llama 3.2 community license agreement',
]

# Families detected by a plain "any phrase is a substring" rule.
_SIMPLE_PHRASE_TABLE = {
    "MIT": _MIT_PHRASES,
    "ISC": _ISC_PHRASES,
    "Zlib": _ZLIB_PHRASES,
    "Apache-2.0": _APACHE2_PHRASES,
    "GPL-2.0": _GPL2_PHRASES,
    "GPL-3.0": _GPL3_PHRASES,
    "LGPL-2.1": _LGPL21_PHRASES,
    "LGPL-3.0": _LGPL3_PHRASES,
    "AGPL-3.0": _AGPL3_PHRASES,
    "MPL-2.0": _MPL2_PHRASES,
    "EPL-2.0": _EPL2_PHRASES,
    "BSL-1.0": _BSL1_PHRASES,
    "Unlicense": _UNLICENSE_PHRASES,
    "CC0-1.0": _CC0_PHRASES,
    "WTFPL": _WTFPL_PHRASES,
    "CC-BY-4.0": _CC_BY_4_PHRASES,
    "CC-BY-SA-4.0": _CC_BY_SA_4_PHRASES,
    "CC-BY-NC-4.0": _CC_BY_NC_4_PHRASES,
    "CC-BY-NC-SA-4.0": _CC_BY_NC_SA_4_PHRASES,
    "Llama-Community": _LLAMA_PHRASES,
}


def _any_phrase(norm: str, phrases) -> bool:
    return any(p in norm for p in phrases)


def _detect_bsd(norm: str, families: set) -> None:
    """BSD-2/3/4-Clause share their opening two conditions; they are distinguished
    by the presence/absence of the advertising clause and the endorse clause."""
    if _BSD_COND1 not in norm or _BSD_COND2 not in norm:
        return
    has_ad = _any_phrase(norm, _BSD_ADVERTISING)
    has_endorse = _any_phrase(norm, _BSD_ENDORSE)
    if has_ad:
        families.add("BSD-4-Clause")
    elif has_endorse:
        families.add("BSD-3-Clause")
    else:
        families.add("BSD-2-Clause")


def _detect_openrail(norm: str, families: set) -> None:
    if "creativeml open rail" in norm or "bigscience openrail" in norm or \
       "open rail-m" in norm:
        families.add("OpenRAIL")
        return
    if "responsible ai license" in norm and "attachment a" in norm:
        families.add("OpenRAIL")


def _detect_families(norm: str) -> set:
    families = set()
    for name, phrases in _SIMPLE_PHRASE_TABLE.items():
        if _any_phrase(norm, phrases):
            families.add(name)
    _detect_bsd(norm, families)
    _detect_openrail(norm, families)
    return families


# ---------------------------------------------------------------------------
# L2: copyright-line attribution
# ---------------------------------------------------------------------------
# Only evaluated for the families whose canonical text has the copyright line
# sitting inside the fill-in-the-blank operative grant.

_SCORED_FOR_L2 = {"MIT", "ISC", "BSD-2-Clause", "BSD-3-Clause", "BSD-4-Clause", "Zlib"}

_COMMENT_PREFIX_RE = re.compile(r"^(?:[#*;>]+|//+|--+|/\*+|\*+)\s*")

_YEAR_TOKEN = (
    r"(?:\d{4}(?:\s*[-–—,]\s*\d{2,4})*"   # 2020, 2020-2023, 2020, 2021
    r"|\[\s*(?:year|yyyy)\s*\]"                     # [year] / [yyyy]
    r"|<\s*(?:year|yyyy)\s*>"                       # <year> / <yyyy>
    r"|yyyy|xxxx)"
)

_COPYRIGHT_LINE_RE = re.compile(
    r"(?i)^(?:©|\(c\)|copyright|copr\.?)\s*(?:©|\(c\))?\s*"
    r"(?P<year>" + _YEAR_TOKEN + r")\s*(?P<holder>.*)$"
)

_TRAILING_CLOSE_RE = re.compile(r"(?:\*/|-->)\s*$")
_TRAILING_RIGHTS_RE = re.compile(r"(?i)[.,;:\s]*all rights reserved\.?\s*$")


def _strip_comment_prefix(line: str) -> str:
    s = line.strip()
    s = _COMMENT_PREFIX_RE.sub("", s)
    return s.strip()


def _clean_holder(h: str) -> str:
    h = h.strip()
    h = _TRAILING_CLOSE_RE.sub("", h).strip()
    h = _TRAILING_RIGHTS_RE.sub("", h).strip()
    h = h.strip(" \t.,;:")
    return h


def _find_copyright_holders(text: str):
    """Scan raw text line-by-line for lines that, once a leading comment marker is
    stripped, START with 'copyright' (or (c)/(c)) immediately followed by a year
    or a year-placeholder token. This is deliberately narrower than "contains the
    word copyright anywhere" so that prose sentences such as '...the above
    copyright notice...' embedded mid-paragraph in a licence body are not mistaken
    for a copyright notice line."""
    holders = []
    if not text:
        return holders
    for raw_line in text.splitlines():
        line = _strip_comment_prefix(raw_line)
        if not line:
            continue
        m = _COPYRIGHT_LINE_RE.match(line)
        if not m:
            continue
        holders.append(_clean_holder(m.group("holder")))
    return holders


# Placeholder holder patterns: bracketed template forms the canonical texts
# themselves use, plus common by-hand fill-in-the-blank words ("and the like").
_PLACEHOLDER_PATTERNS = [
    re.compile(r"\byour\s*name\b"),
    re.compile(r"\byour\s*organi[sz]ation\b"),
    re.compile(r"\borgani[sz]ation\s*name\b"),
    re.compile(r"\bcompany\s*name\b"),
    re.compile(r"\bcopyright\s*holders?\b"),
    re.compile(r"\bname\s*of\s*copyright\s*owner\b"),
    re.compile(r"\bname\s*of\s*author\b"),
    re.compile(r"\bauthor'?s?\s*name\b"),
    re.compile(r"\bfull\s*name\b"),
    re.compile(r"\bowner\s*name\b"),
    re.compile(r"\byyyy\b"),
    re.compile(r"\bxxxx\b"),
    re.compile(r"^\s*name\s*$"),
    re.compile(r"^\s*owner\s*$"),
    re.compile(r"^\s*author\s*$"),
    re.compile(r"^\s*holder\s*$"),
    re.compile(r"\btodo\b"),
    re.compile(r"\btbd\b"),
    re.compile(r"\bplaceholder\b"),
    re.compile(r"\binsert\b.*\bname\b"),
    re.compile(r"\bfill\s*in\b"),
    re.compile(r"example\.(?:com|org|net)"),
    re.compile(r"^\.\.\.$"),
    re.compile(r"^_+$"),
    re.compile(r"^-+$"),
]


def _is_placeholder_holder(holder: str) -> bool:
    h = holder.strip()
    if not h:
        return False
    h_stripped = h.rstrip(" .,;:")
    if (h_stripped.startswith("<") and h_stripped.endswith(">")) or \
       (h_stripped.startswith("[") and h_stripped.endswith("]")):
        return True
    hl = h.lower()
    return any(p.search(hl) for p in _PLACEHOLDER_PATTERNS)


def _attribution_for(text: str) -> str:
    holders = _find_copyright_holders(text)
    if not holders:
        return "no_copyright_line"
    classifications = []
    for h in holders:
        if not h:
            classifications.append("no_holder")
        elif _is_placeholder_holder(h):
            classifications.append("placeholder")
        else:
            classifications.append("named")
    if "named" in classifications:
        return "named"
    if "placeholder" in classifications:
        return "placeholder"
    return "no_holder"


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def score(text: str) -> dict:
    """Returns {"families": [...], "attribution": <str or None>}"""
    try:
        if text is None:
            text = ""
        if not isinstance(text, str):
            text = str(text)
    except Exception:
        text = ""

    try:
        norm = _normalize(text)
    except Exception:
        norm = ""

    families = set()
    try:
        families = _detect_families(norm)
    except Exception:
        families = set()

    attribution = None
    try:
        if families & _SCORED_FOR_L2:
            attribution = _attribution_for(text)
    except Exception:
        attribution = None

    return {"families": sorted(families), "attribution": attribution}
