"""
Text-measurement instrument for open-source / open-content licence texts.

Implements two independent "rungs":

  L1 -- identified:    does the file's normalised text contain a distinctive
                        operative phrase of a known licence family?
  L2 -- attributed:     for the families whose canonical text carries a
                        copyright line inside the operative grant (MIT, ISC,
                        BSD-2/3/4-Clause, Zlib), does the file carry an
                        actual, non-placeholder copyright notice?

Pure standard library, no I/O, no network, deterministic, side-effect-free
at import time.
"""

import re

# ---------------------------------------------------------------------------
# Shared text normalisation helpers
# ---------------------------------------------------------------------------

_CURLY_QUOTES = {
    "‘": "'", "’": "'", "‚": "'", "‛": "'", "′": "'",
    "“": '"', "”": '"', "„": '"', "‟": '"', "″": '"',
}
_QUOTE_TABLE = str.maketrans(_CURLY_QUOTES)

_WS_RE = re.compile(r"\s+")


def _fold_quotes(s: str) -> str:
    return s.translate(_QUOTE_TABLE)


def _normalize_l1(text: str) -> str:
    """Lowercase, fold curly quotes to straight, collapse all whitespace
    (including newlines) to a single space."""
    s = _fold_quotes(text)
    s = s.lower()
    s = _WS_RE.sub(" ", s)
    return s.strip()


def _has(t: str, phrase: str) -> bool:
    return phrase in t


# ---------------------------------------------------------------------------
# L1 -- per-family detectors
#
# Each detector receives the L1-normalised (lowercase, quote-folded,
# whitespace-collapsed) text and returns True/False. Where a family's
# canonical text is a near-superset of a sibling family's (the BSD clause
# count, the CC-BY variants, the GPL/LGPL/AGPL/version family), inclusion
# phrases are combined with exclusion conditions so that the *combination*
# -- not any single fragment -- is unique to that family, per the
# specification's explicit allowance for this.
# ---------------------------------------------------------------------------

def _det_mit(t: str) -> bool:
    # Boost uses near-identical "permission is hereby granted, free of
    # charge" language but for "any person or organization ... accompanying
    # documentation covered by this license" -- exclude that wording so a
    # Boost text is never also counted as MIT.
    if _has(t, "any person or organization obtaining a copy of the software "
                "and accompanying documentation covered by this license"):
        return False
    return (
        _has(t, "to deal in the software without restriction, including "
                 "without limitation the rights to use, copy, modify, merge, "
                 "publish, distribute, sublicense, and/or sell copies of the "
                 "software")
        or _has(t, "permission is hereby granted, free of charge, to any "
                    "person obtaining a copy of this software and associated "
                    "documentation files")
    )


def _det_zlib(t: str) -> bool:
    return _has(t, "the origin of this software must not be misrepresented")


def _det_isc(t: str) -> bool:
    if _det_zlib(t):
        return False
    return _has(t, "distribute this software for any purpose with or "
                    "without fee is hereby granted")


_BSD_CORE = ("redistribution and use in source and binary forms, with or "
             "without modification, are permitted provided that the "
             "following conditions are met")


def _bsd_core(t: str) -> bool:
    return _has(t, _BSD_CORE)


def _bsd_advertising(t: str) -> bool:
    return (
        _has(t, "all advertising materials mentioning features or use of "
                 "this software must display the following acknowledgement")
        or _has(t, "all advertising materials mentioning features or use of "
                    "this software must display the following acknowledgment")
    )


def _bsd_endorsement(t: str) -> bool:
    return _has(t, "may be used to endorse or promote products derived from "
                     "this software without specific prior written permission")


def _det_bsd4(t: str) -> bool:
    return _bsd_core(t) and _bsd_advertising(t)


def _det_bsd3(t: str) -> bool:
    return _bsd_core(t) and _bsd_endorsement(t) and not _bsd_advertising(t)


def _det_bsd2(t: str) -> bool:
    return _bsd_core(t) and not _bsd_endorsement(t) and not _bsd_advertising(t)


def _det_apache(t: str) -> bool:
    return (
        (_has(t, "apache license") and _has(t, "version 2.0"))
        or _has(t, "www.apache.org/licenses/license-2.0")
    )


def _is_lesser(t: str) -> bool:
    return _has(t, "lesser general public license") or _has(
        t, "library general public license"
    )


def _is_affero(t: str) -> bool:
    return _has(t, "affero general public license")


def _has_gpl_name(t: str) -> bool:
    return _has(t, "general public license")


def _det_agpl3(t: str) -> bool:
    if not _is_affero(t):
        return False
    return (
        (_has_gpl_name(t) and _has(t, "version 3"))
        or _has(t, "specifically designed to ensure cooperation with the "
                    "community in the case of network server software")
    )


def _det_lgpl3(t: str) -> bool:
    if not _is_lesser(t) or _is_affero(t):
        return False
    return (
        (_has_gpl_name(t) and _has(t, "version 3"))
        or _has(t, "incorporates the terms and conditions of version 3 of "
                    "the gnu general public license")
    )


def _det_lgpl21(t: str) -> bool:
    if not _is_lesser(t) or _is_affero(t):
        return False
    return _has_gpl_name(t) and _has(t, "version 2.1")


def _det_gpl3(t: str) -> bool:
    if _is_lesser(t) or _is_affero(t):
        return False
    return (
        (_has_gpl_name(t) and _has(t, "version 3"))
        or _has(t, "the gnu general public license is a free, copyleft "
                    "license for software")
    )


def _det_gpl2(t: str) -> bool:
    if _is_lesser(t) or _is_affero(t):
        return False
    return _has_gpl_name(t) and _has(t, "version 2") and not _has(t, "version 2.1")


def _det_mpl2(t: str) -> bool:
    return (
        _has(t, "this source code form is subject to the terms of the "
                 "mozilla public license, v. 2.0")
        or (_has(t, "mozilla public license") and _has(t, "incompatible with "
                                                            "secondary licenses"))
    )


def _det_epl2(t: str) -> bool:
    has_epl = _has(t, "eclipse public license")
    has_v2 = (
        _has(t, "v. 2.0") or _has(t, "v2.0") or _has(t, "version 2.0")
        or _has(t, "v 2.0")
    )
    return has_epl and has_v2


def _det_bsl1(t: str) -> bool:
    return (
        _has(t, "any person or organization obtaining a copy of the "
                 "software and accompanying documentation covered by this "
                 "license")
        or _has(t, "boost software license")
    )


def _det_unlicense(t: str) -> bool:
    return _has(t, "this is free and unencumbered software released into "
                    "the public domain")


def _det_cc0(t: str) -> bool:
    return (
        (_has(t, "cc0 1.0 universal") and _has(t, "public domain dedication"))
        or _has(t, "without fear of later claims of infringement build "
                    "upon, modify, incorporate in other works, reuse and "
                    "redistribute")
    )


def _det_cc_by_nc_sa4(t: str) -> bool:
    return (
        _has(t, "creative commons attribution-noncommercial-sharealike 4.0 "
                 "international")
        or _has(t, "cc by-nc-sa 4.0")
        or _has(t, "licensed under a creative commons "
                    "attribution-noncommercial-sharealike 4.0 international "
                    "license")
    )


def _det_cc_by_nc4(t: str) -> bool:
    return (
        _has(t, "creative commons attribution-noncommercial 4.0 international")
        or _has(t, "cc by-nc 4.0")
        or _has(t, "licensed under a creative commons attribution-noncommercial "
                    "4.0 international license")
    )


def _det_cc_by_sa4(t: str) -> bool:
    return (
        _has(t, "creative commons attribution-sharealike 4.0 international")
        or _has(t, "cc by-sa 4.0")
        or _has(t, "licensed under a creative commons attribution-sharealike "
                    "4.0 international license")
    )


def _det_cc_by4(t: str) -> bool:
    return (
        _has(t, "creative commons attribution 4.0 international")
        or _has(t, "cc by 4.0")
        or _has(t, "licensed under a creative commons attribution 4.0 "
                    "international license")
    )


def _det_wtfpl(t: str) -> bool:
    return (
        _has(t, "do what the fuck you want to public license")
        or _has(t, "you just do what the fuck you want to")
    )


def _det_openrail(t: str) -> bool:
    if not (_has(t, "openrail") or _has(t, "open rail")):
        return False
    return (
        _has(t, "responsible ai license")
        or _has(t, "use-based restriction")
        or _has(t, "use based restriction")
        or _has(t, "rail license")
        or _has(t, "bigscience")
    )


def _det_llama(t: str) -> bool:
    if not _has(t, "llama"):
        return False
    return (
        _has(t, "community license")
        or _has(t, "you will not use the llama materials to improve any "
                    "other large language model")
        or (_has(t, "llama materials") and _has(t, "meta") and
            _has(t, "license agreement"))
    )


_FAMILY_DETECTORS = {
    "MIT": _det_mit,
    "ISC": _det_isc,
    "BSD-4-Clause": _det_bsd4,
    "BSD-3-Clause": _det_bsd3,
    "BSD-2-Clause": _det_bsd2,
    "Zlib": _det_zlib,
    "Apache-2.0": _det_apache,
    "GPL-3.0": _det_gpl3,
    "GPL-2.0": _det_gpl2,
    "LGPL-3.0": _det_lgpl3,
    "LGPL-2.1": _det_lgpl21,
    "AGPL-3.0": _det_agpl3,
    "MPL-2.0": _det_mpl2,
    "EPL-2.0": _det_epl2,
    "BSL-1.0": _det_bsl1,
    "Unlicense": _det_unlicense,
    "CC0-1.0": _det_cc0,
    "CC-BY-NC-SA-4.0": _det_cc_by_nc_sa4,
    "CC-BY-NC-4.0": _det_cc_by_nc4,
    "CC-BY-SA-4.0": _det_cc_by_sa4,
    "CC-BY-4.0": _det_cc_by4,
    "WTFPL": _det_wtfpl,
    "OpenRAIL": _det_openrail,
    "Llama-Community": _det_llama,
}


def _safe_call(fn, t: str) -> bool:
    try:
        return bool(fn(t))
    except Exception:
        return False


def _detect_families(normalized_text: str):
    return [name for name, fn in _FAMILY_DETECTORS.items()
            if _safe_call(fn, normalized_text)]


# ---------------------------------------------------------------------------
# L2 -- attribution
#
# Evaluated only for the families whose copyright line sits inside the
# operative grant and whose canonical text's placeholder is meant to be
# filled in by the user: MIT, ISC, BSD-2/3/4-Clause, Zlib. Everything else
# (including the Apache-2.0 appendix, GPL-family, MPL-2.0, CC0, Unlicense,
# the CC-BY-* family, WTFPL, OpenRAIL, Llama-Community) is not applicable.
# ---------------------------------------------------------------------------

_L2_SCORED_FAMILIES = {
    "MIT", "ISC", "BSD-2-Clause", "BSD-3-Clause", "BSD-4-Clause", "Zlib",
}

_MARKER_RE = re.compile(r"copyright|©", re.IGNORECASE)

# A run of one or more 4-digit years, possibly a range/list.
_YEAR_DIGIT_RE = re.compile(r"\d{4}(?:\s*[-–—,]\s*\d{4})*")

# Unfilled template year tokens: <year>, [year], <yyyy>, [yyyy], bare yyyy/xxxx.
_YEAR_PLACEHOLDER_RE = re.compile(
    r"<\s*(?:year|yyyy)\s*>|\[\s*(?:year|yyyy)\s*\]|\byyyy\b|\bxxxx\b",
    re.IGNORECASE,
)

_LEADING_STRIP_RE = re.compile(r"^[\s,.:;\-–—]+")
_LEADING_C_RE = re.compile(r"^\(c\)\s*", re.IGNORECASE)
_LEADING_BY_RE = re.compile(r"^by\s+", re.IGNORECASE)

# A holder string that consists entirely of one or more bracketed groups,
# e.g. "<copyright holders>", "[fullname]", "[yyyy] [name of copyright owner]".
_BRACKET_WHOLE_RE = re.compile(r"^(?:[<\[{][^<>\[\]{}]*[>\]}][\s,]*)+$")

_PLACEHOLDER_EXACT = {
    "copyright holder", "copyright holders", "the copyright holder",
    "the copyright holders", "copyright owner", "copyright owners",
    "the copyright owner", "the copyright owners",
    "owner", "holder", "author", "authors", "name", "fullname", "full name",
    "your name", "your name here", "insert name here", "insert your name",
    "insert your name here", "name of author", "author name", "authors name",
    "name of copyright owner", "name of copyright holder",
    "your company", "company name", "your organization", "organization name",
    "example company", "acme", "acme inc", "acme, inc.", "acme corp",
    "acme corporation", "john doe", "jane doe", "tbd", "todo", "fixme",
    "n/a", "na", "xxxx", "xxx", "nobody", "unknown", "anonymous",
    "first last", "firstname lastname",
}

_PLACEHOLDER_SUBSTR = (
    "copyright holder", "copyright owner", "name of copyright owner",
    "name of copyright holder", "your name", "insert name",
    "insert your name", "full name here", "company name here",
    "your company name", "name of author", "author name here",
)


def _clean_holder(raw: str) -> str:
    h = raw
    for _ in range(4):
        h2 = _LEADING_STRIP_RE.sub("", h)
        h2 = _LEADING_C_RE.sub("", h2)
        h2 = _LEADING_BY_RE.sub("", h2)
        if h2 == h:
            break
        h = h2
    return h.strip()


def _looks_like_placeholder_holder(holder: str) -> bool:
    h = holder.strip()
    h = h.rstrip(".").strip()
    if not h:
        return False
    low = h.lower()
    if _BRACKET_WHOLE_RE.match(h):
        return True
    if low in _PLACEHOLDER_EXACT:
        return True
    for kw in _PLACEHOLDER_SUBSTR:
        if kw in low:
            return True
    return False


def _classify_copyright(text: str) -> str:
    """Scans the *original* text (not the L1 single-line normalisation,
    since a copyright "line" is a line-structured notion) for copyright
    lines and classifies the strongest one found."""
    results = []
    for raw_line in text.splitlines():
        line = _fold_quotes(raw_line)
        line = re.sub(r"[ \t]+", " ", line).strip()
        if not line:
            continue
        markers = list(_MARKER_RE.finditer(line))
        if not markers:
            continue
        for mk in markers:
            # Extend to end of line rather than cutting at the next marker:
            # a placeholder holder like "<copyright holders>" contains the
            # word "copyright" itself, which would otherwise be treated as
            # a second marker and wrongly truncate the segment.
            seg_start = mk.end()
            segment = line[seg_start:]

            md = _YEAR_DIGIT_RE.search(segment)
            if md:
                holder_raw = segment[md.end():]
                holder = _clean_holder(holder_raw)
                if not holder:
                    results.append("no_holder")
                elif _looks_like_placeholder_holder(holder):
                    results.append("placeholder")
                else:
                    results.append("named")
                continue

            mp = _YEAR_PLACEHOLDER_RE.search(segment)
            if mp:
                results.append("placeholder")
                continue

            # Marker present but nothing resembling a year in its segment:
            # not a qualifying copyright line; keep scanning other markers.

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

        normalized = _normalize_l1(text)
        families = _detect_families(normalized)

        applicable = any(f in _L2_SCORED_FAMILIES for f in families)
        attribution = _classify_copyright(text) if applicable else None

        return {"families": families, "attribution": attribution}
    except Exception:
        return {"families": [], "attribution": None}
