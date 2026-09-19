#!/usr/bin/env python3
"""The two arms of the corpus. Session 164, 2026-09-19.

Arm C is the SPDX canonical text as published. Arm F is the same text with the
literal substitution table of PREREGISTRATION.md §6 applied, case-sensitively, in
the order written there. The table is an INPUT TRANSFORMATION, not a measuring
rule: it is published in full and it overlaps this practice's own placeholder
table, which is disclosed rather than hidden.
"""

# (token, replacement) — order is the pre-registered order and matters.
FILL = [
    ("<year>", "2019"),
    ("<years>", "2019-2021"),
    ("<yyyy>", "2019"),
    ("[year]", "2019"),
    ("[years]", "2019-2021"),
    ("[yyyy]", "2019"),
    ("<YEAR>", "2019"),
    ("[YEAR]", "2019"),
    ("<copyright holders>", "Aurora Instruments GmbH"),
    ("<copyright holder>", "Aurora Instruments GmbH"),
    ("[copyright holder]", "Aurora Instruments GmbH"),
    ("[copyright holders]", "Aurora Instruments GmbH"),
    ("<copyright-holder>", "Aurora Instruments GmbH"),
    ("[name of copyright owner]", "Aurora Instruments GmbH"),
    ("<name of copyright owner>", "Aurora Instruments GmbH"),
    ("<OWNER>", "Aurora Instruments GmbH"),
    ("[OWNER]", "Aurora Instruments GmbH"),
    ("<owner>", "Aurora Instruments GmbH"),
    ("[owner]", "Aurora Instruments GmbH"),
    ("[fullname]", "Wilhelmine Kessler"),
    ("[full name]", "Wilhelmine Kessler"),
    ("<fullname>", "Wilhelmine Kessler"),
    ("<full name>", "Wilhelmine Kessler"),
    ("[name]", "Wilhelmine Kessler"),
    ("<name>", "Wilhelmine Kessler"),
    ("<name of author>", "Wilhelmine Kessler"),
    ("[name of author]", "Wilhelmine Kessler"),
    ("<author>", "Wilhelmine Kessler"),
    ("[author]", "Wilhelmine Kessler"),
    ("[organization]", "Aurora Instruments GmbH"),
    ("<organization>", "Aurora Instruments GmbH"),
]

FILL_TOKENS = [t for t, _ in FILL]


def fill(text: str) -> str:
    for token, repl in FILL:
        text = text.replace(token, repl)
    return text
