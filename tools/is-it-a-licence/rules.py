#!/usr/bin/env python3
"""The four rungs. Session 163, 2026-09-18.

L0 present and non-empty · L1 identified · L2 attributed · L3 single-voiced.
No rule calls a model. Every verdict is re-derivable from the committed text.
"""
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fingerprints import (FAMILIES, SCORED_FAMILIES, PLACEHOLDERS, normalise,
                          copyright_lines, holder_of, has_placeholder)

# Session 162's own net, reproduced unchanged so the same files are looked at.
LICENCE_BASENAME_RE = re.compile(r"^(licen[cs]e|copying|unlicense|copyright)([.\-_].*)?$", re.I)


def is_licence_shaped(path: str) -> bool:
    """Session 162's rung R3, applied to one path. Reads the name, never the file."""
    return bool(LICENCE_BASENAME_RE.match(path.rsplit("/", 1)[-1]))


# ------------------------------------------------------------------- L0

def l0_nonempty(raw: str) -> bool:
    """The blob holds at least one non-whitespace character."""
    return raw is not None and raw.strip() != ""


# ------------------------------------------------------------------- L1

def l1_families(raw: str):
    """Every family whose phrase test the text passes, in table order.

    A family matches when at least one of its `any_of` phrases is present, all of
    its `requires_all` phrases are present, and none of its `none_of` phrases is.
    """
    if not l0_nonempty(raw):
        return []
    norm = normalise(raw)
    out = []
    for name, spec in FAMILIES:
        if not any(p in norm for p in spec["any_of"]):
            continue
        if any(p not in norm for p in spec.get("requires_all", [])):
            continue
        if any(p in norm for p in spec.get("none_of", [])):
            continue
        out.append(name)
    return out


# ------------------------------------------------------------------- L2

def l2_attribution(raw: str, families):
    """Whether the file names a licensor, for the families where that is scored.

    Returns one of: 'named', 'placeholder', 'no_holder', 'no_copyright_line',
    or None when no identified family is scored (amendment 1).
    """
    if not any(f in SCORED_FAMILIES for f in families):
        return None
    lines = copyright_lines(raw or "")
    if not lines:
        return "no_copyright_line"
    # A file may carry several copyright lines. One filled line is enough.
    verdicts = []
    for ln in lines:
        if has_placeholder(ln):
            verdicts.append("placeholder")
        elif holder_of(ln):
            verdicts.append("named")
        else:
            verdicts.append("no_holder")
    if "named" in verdicts:
        return "named"
    if "placeholder" in verdicts:
        return "placeholder"
    return "no_holder"


def apache_appendix_unfilled(raw: str, families) -> bool:
    """Reported, never scored: an Apache-2.0 text whose appendix is left as shipped.

    Amendment 1: shipping the appendix unedited is the normal way to apply the
    licence. This is published as a description of practice, not as a defect.
    """
    if "Apache-2.0" not in families:
        return False
    return any(has_placeholder(ln) for ln in copyright_lines(raw or ""))


# ------------------------------------------------------------------- L3

def l3_voices(per_file_families):
    """Distinct identified families across one repository's licence-shaped files."""
    seen = []
    for fams in per_file_families:
        for f in fams:
            if f not in seen:
                seen.append(f)
    return seen


# ------------------------------------------------------------------- headline

def file_delivers(raw: str):
    """L0 and L1 and (L2 where applicable). Returns (bool, reason)."""
    if not l0_nonempty(raw):
        return False, "empty"
    fams = l1_families(raw)
    if not fams:
        return False, "not_identified"
    att = l2_attribution(raw, fams)
    if att is None:
        return True, "identified_attribution_not_applicable"
    if att == "named":
        return True, "identified_and_attributed"
    return False, att
