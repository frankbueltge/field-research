#!/usr/bin/env python3
"""Hand-made cases, run before any repository blob is read. Session 163.

Each case says what a rule MUST produce and what it MUST NOT. The cases are written
from the licence texts and from the shapes a licence file takes in the wild, not from
anything in the population. Run: python3 fixtures.py  ->  data/fixture-check.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rules
import fingerprints as fp

MIT_HEAD = ('MIT License\n\nCopyright (c) 2023 Jane Doe\n\n'
            'Permission is hereby granted, free of charge, to any person obtaining a copy\n'
            'of this software and associated documentation files (the "Software"), to deal\n'
            'in the Software without restriction.\n')
BSD_COMMON = ('Redistribution and use in source and binary forms, with or without\n'
              'modification, are permitted provided that the following conditions are met:\n'
              '1. Redistributions of source code must retain the above copyright notice.\n')
BSD3_CLAUSE = ('3. Neither the name of the copyright holder nor the names of its contributors\n'
               '   may be used to endorse or promote products derived from this software\n'
               '   without specific prior written permission.\n')
BSD4_CLAUSE = ('3. All advertising materials mentioning features or use of this software\n'
               '   must display the following acknowledgement: This product includes software.\n')

# (id, kind, callable -> value, value)
#   kind "must"     : the rule MUST return `value`
#   kind "must-not" : the rule MUST NOT return `value` — a FORBIDDEN value, not a target
#
# The two readings were conflated in the first draft of this file, which is why one
# case failed before any data existed. Recorded here rather than quietly repaired.
CASES = [
    # ---- the net (session 162's own rule, reproduced) -------------------
    ("shape/LICENSE", "must", lambda: rules.is_licence_shaped("LICENSE"), True),
    ("shape/LICENSE.md", "must", lambda: rules.is_licence_shaped("a/b/LICENSE.md"), True),
    ("shape/LICENCE.txt", "must", lambda: rules.is_licence_shaped("LICENCE.txt"), True),
    ("shape/COPYING", "must", lambda: rules.is_licence_shaped("COPYING"), True),
    ("shape/LICENSE-MIT", "must", lambda: rules.is_licence_shaped("LICENSE-MIT"), True),
    ("shape/license-risk-scan.md", "must", lambda: rules.is_licence_shaped("docs/license-risk-scan.md"), True),
    ("shape/licenses-dir-name", "must-not", lambda: rules.is_licence_shaped("licenses"), True),
    ("shape/licensing.py", "must-not", lambda: rules.is_licence_shaped("src/licensing.py"), True),
    ("shape/README", "must-not", lambda: rules.is_licence_shaped("README.md"), True),
    ("shape/relicense.md", "must-not", lambda: rules.is_licence_shaped("relicense.md"), True),

    # ---- L0 -------------------------------------------------------------
    ("L0/empty", "must-not", lambda: rules.l0_nonempty(""), True),
    ("L0/whitespace", "must-not", lambda: rules.l0_nonempty("\n\n   \t\n"), True),
    ("L0/one-char", "must", lambda: rules.l0_nonempty("x"), True),

    # ---- L1 identification ---------------------------------------------
    ("L1/mit", "must", lambda: rules.l1_families(MIT_HEAD), ["MIT"]),
    ("L1/mit-crlf", "must", lambda: rules.l1_families(MIT_HEAD.replace("\n", "\r\n")), ["MIT"]),
    ("L1/mit-curly-quotes", "must",
     lambda: rules.l1_families(MIT_HEAD.replace('"Software"', "“Software”")), ["MIT"]),
    ("L1/mit-hard-wrapped", "must",
     lambda: rules.l1_families("Permission is hereby granted, free of charge,\nto any person\nobtaining a copy of this\nsoftware and associated documentation files (the Software)"),
     ["MIT"]),
    # Added after the mutation run below found that NO phrase in the table contains a
    # quote character, so quote folding could not change any verdict and the curly-quote
    # case above was not testing what its name said. These three exercise the folds that
    # a phrase really does depend on.
    ("L1/bsl-en-dash", "must", lambda: rules.l1_families(
        "Boost Software License \u2013 Version 1.0 \u2013 August 17th, 2003\n"), ["BSL-1.0"]),
    ("L1/epl-em-dash", "must", lambda: rules.l1_families(
        "Eclipse Public License \u2014 v 2.0\n"), ["EPL-2.0"]),
    ("L1/mit-nbsp", "must", lambda: rules.l1_families(
        MIT_HEAD.replace("to any person", "to\u00a0any\u00a0person")), ["MIT"]),
    ("TABLE/no-phrase-carries-a-quote", "must", lambda: any(
        ch in ph for _, spec in fp.FAMILIES
        for key in ("any_of", "requires_all", "none_of") for ph in spec.get(key, [])
        for ch in '"\u2018\u2019\u201c\u201d'), False),
    ("TABLE/every-phrase-is-normalised", "must", lambda: all(
        ph == fp.normalise(ph) for _, spec in fp.FAMILIES
        for key in ("any_of", "requires_all", "none_of") for ph in spec.get(key, [])), True),
    ("L1/isc", "must", lambda: rules.l1_families(
        "Copyright (c) 2019 Someone\n\nPermission to use, copy, modify, and/or distribute this software for any\n"
        "purpose with or without fee is hereby granted."), ["ISC"]),
    ("L1/bsd2", "must", lambda: rules.l1_families("Copyright 2020 A\n" + BSD_COMMON), ["BSD-2-Clause"]),
    ("L1/bsd3", "must", lambda: rules.l1_families("Copyright 2020 A\n" + BSD_COMMON + BSD3_CLAUSE), ["BSD-3-Clause"]),
    ("L1/bsd4", "must", lambda: rules.l1_families("Copyright 1995 A\n" + BSD_COMMON + BSD4_CLAUSE), ["BSD-4-Clause"]),
    ("L1/bsd3-is-not-bsd2", "must-not",
     lambda: "BSD-2-Clause" in rules.l1_families("Copyright 2020 A\n" + BSD_COMMON + BSD3_CLAUSE), True),
    ("L1/apache-full", "must", lambda: rules.l1_families(
        "Apache License\nVersion 2.0, January 2004\n\nTERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION\n"),
     ["Apache-2.0"]),
    ("L1/apache-header", "must", lambda: rules.l1_families(
        "Licensed under the Apache License, Version 2.0 (the \"License\");"), ["Apache-2.0"]),
    ("L1/gpl3", "must", lambda: rules.l1_families(
        "                    GNU GENERAL PUBLIC LICENSE\n                       Version 3, 29 June 2007\n"), ["GPL-3.0"]),
    ("L1/gpl2", "must", lambda: rules.l1_families(
        "                    GNU GENERAL PUBLIC LICENSE\n                       Version 2, June 1991\n"), ["GPL-2.0"]),
    ("L1/agpl3-not-gpl3", "must-not", lambda: "GPL-3.0" in rules.l1_families(
        "GNU AFFERO GENERAL PUBLIC LICENSE\nVersion 3, 19 November 2007\n\n"
        "This licence is a modified version of the GNU General Public License.\n"), True),
    # Added after K1 fired on the first control run: the canonical GPLv3 text names the
    # Affero licence in section 13 and the canonical GPLv2 names the Library GPL in its
    # preamble. A family must not be excluded by a mere mention of another.
    ("L1/gpl3-naming-agpl-is-still-gpl3", "must", lambda: rules.l1_families(
        "GNU GENERAL PUBLIC LICENSE\nVersion 3, 29 June 2007\n\n"
        "13. Use with the GNU Affero General Public License.\n"
        "Notwithstanding any other provision of this License, you have permission to\n"
        "link or combine any covered work with a work licensed under version 3 of the\n"
        "GNU Affero General Public License into a single combined work.\n"), ["GPL-3.0"]),
    ("L1/gpl2-naming-library-gpl-is-still-gpl2", "must", lambda: rules.l1_families(
        "GNU GENERAL PUBLIC LICENSE\nVersion 2, June 1991\n\n"
        "If your program is a subroutine library, you may consider it more useful to\n"
        "permit linking proprietary applications with the library. If this is what you\n"
        "want to do, use the GNU Library General Public License instead of this License.\n"),
     ["GPL-2.0"]),
    ("L1/lgpl21", "must", lambda: rules.l1_families(
        "GNU LESSER GENERAL PUBLIC LICENSE\nVersion 2.1, February 1999\n"), ["LGPL-2.1"]),
    ("L1/mpl2", "must", lambda: rules.l1_families("Mozilla Public License Version 2.0\n"), ["MPL-2.0"]),
    ("L1/unlicense", "must", lambda: rules.l1_families(
        "This is free and unencumbered software released into the public domain.\n"), ["Unlicense"]),
    ("L1/cc0", "must", lambda: rules.l1_families("Creative Commons Legal Code\n\nCC0 1.0 Universal\n"), ["CC0-1.0"]),
    ("L1/ccby4", "must", lambda: rules.l1_families(
        "Creative Commons Attribution 4.0 International Public License\n"), ["CC-BY-4.0"]),
    ("L1/ccbync4-not-ccby4", "must-not", lambda: "CC-BY-4.0" in rules.l1_families(
        "Creative Commons Attribution-NonCommercial 4.0 International Public License\n"), True),
    ("L1/ccbyncsa4", "must", lambda: rules.l1_families(
        "Attribution-NonCommercial-ShareAlike 4.0 International Public License\n"), ["CC-BY-NC-SA-4.0"]),
    ("L1/zlib", "must", lambda: rules.l1_families(
        "Altered source versions must be plainly marked as such, and must not be\n"
        "misrepresented as being the original software.\n"), ["Zlib"]),
    ("L1/dual-mit-apache", "must", lambda: sorted(rules.l1_families(
        MIT_HEAD + "\n\nTERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION\n")),
     ["Apache-2.0", "MIT"]),

    # ---- L1 must NOT identify -------------------------------------------
    ("L1/pointer-only", "must-not", lambda: bool(rules.l1_families(
        "This project is licensed under the MIT License. See the LICENSE file for details.\n")), True),
    ("L1/spdx-tag-only", "must-not", lambda: bool(rules.l1_families("SPDX-License-Identifier: MIT\n")), True),
    ("L1/empty", "must-not", lambda: bool(rules.l1_families("")), True),
    ("L1/copyright-only", "must-not", lambda: bool(rules.l1_families(
        "Copyright (c) 2024 Acme Corp. All rights reserved.\n")), True),
    ("L1/all-rights-reserved", "must-not", lambda: bool(rules.l1_families(
        "Copyright 2025 Acme. All rights reserved. No permission is granted to anyone.\n")), True),
    ("L1/risk-scan-report", "must-not", lambda: bool(rules.l1_families(
        "# License risk scan\n\n| package | license | risk |\n|---|---|---|\n| numpy | BSD-3-Clause | low |\n")), True),
    ("L1/prose-about-licences", "must-not", lambda: bool(rules.l1_families(
        "We evaluated whether each repository carries a license file and found that most do.\n")), True),

    # ---- L2 attribution --------------------------------------------------
    ("L2/mit-named", "must", lambda: rules.l2_attribution(MIT_HEAD, ["MIT"]), "named"),
    ("L2/mit-placeholder-angle", "must", lambda: rules.l2_attribution(
        MIT_HEAD.replace("2023 Jane Doe", "<year> <copyright holders>"), ["MIT"]), "placeholder"),
    ("L2/mit-placeholder-square", "must", lambda: rules.l2_attribution(
        MIT_HEAD.replace("2023 Jane Doe", "[year] [fullname]"), ["MIT"]), "placeholder"),
    ("L2/mit-placeholder-brace", "must", lambda: rules.l2_attribution(
        MIT_HEAD.replace("2023 Jane Doe", "{year} {fullname}"), ["MIT"]), "placeholder"),
    ("L2/mit-yyyy-word", "must", lambda: rules.l2_attribution(
        MIT_HEAD.replace("2023 Jane Doe", "yyyy Name Of Author"), ["MIT"]), "placeholder"),
    ("L2/holder-containing-yyyy-is-not-placeholder", "must-not", lambda: rules.l2_attribution(
        MIT_HEAD.replace("Jane Doe", "Yyyylmaz Labs"), ["MIT"]), "placeholder"),
    ("L2/year-only-no-holder", "must", lambda: rules.l2_attribution(
        MIT_HEAD.replace("2023 Jane Doe", "2023"), ["MIT"]), "no_holder"),
    ("L2/no-copyright-line", "must", lambda: rules.l2_attribution(
        MIT_HEAD.replace("Copyright (c) 2023 Jane Doe\n", ""), ["MIT"]), "no_copyright_line"),
    ("L2/one-filled-among-many-wins", "must", lambda: rules.l2_attribution(
        "Copyright (c) [year] [fullname]\nCopyright (c) 2024 Real Person\n" + MIT_HEAD.split("Copyright")[0]
        + "Permission is hereby granted, free of charge, to any person obtaining a copy of this "
          "software and associated documentation files", ["MIT"]), "named"),
    ("L2/comment-prefixed-line", "must", lambda: rules.l2_attribution(
        "# Copyright 2020 Acme Inc.\n" + MIT_HEAD.replace("Copyright (c) 2023 Jane Doe\n", ""), ["MIT"]), "named"),
    ("L2/range-of-years", "must", lambda: rules.l2_attribution(
        MIT_HEAD.replace("2023 Jane Doe", "2019-2024 Acme Inc."), ["MIT"]), "named"),
    ("L2/not-applicable-gpl", "must", lambda: rules.l2_attribution("x", ["GPL-3.0"]), None),
    ("L2/not-applicable-apache", "must", lambda: rules.l2_attribution("x", ["Apache-2.0"]), None),
    ("L2/not-applicable-unidentified", "must", lambda: rules.l2_attribution("x", []), None),
    ("L2/scored-wins-in-mixed", "must", lambda: rules.l2_attribution(
        "Copyright (c) 2024 Real Person\n", ["Apache-2.0", "MIT"]), "named"),

    # ---- the headline ----------------------------------------------------
    ("HEAD/mit-filled-delivers", "must", lambda: rules.file_delivers(MIT_HEAD)[0], True),
    ("HEAD/mit-template-does-not", "must-not", lambda: rules.file_delivers(
        MIT_HEAD.replace("2023 Jane Doe", "[year] [fullname]"))[0], True),
    ("HEAD/gpl-delivers-without-holder", "must", lambda: rules.file_delivers(
        "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007")[0], True),
    ("HEAD/empty-does-not", "must-not", lambda: rules.file_delivers("")[0], True),
    ("HEAD/pointer-does-not", "must-not", lambda: rules.file_delivers(
        "See LICENSE for the MIT terms.")[0], True),
    ("HEAD/reason-empty", "must", lambda: rules.file_delivers("")[1], "empty"),
    ("HEAD/reason-not-identified", "must", lambda: rules.file_delivers("nothing here")[1], "not_identified"),

    # ---- L3 --------------------------------------------------------------
    ("L3/one-voice", "must", lambda: rules.l3_voices([["MIT"], ["MIT"]]), ["MIT"]),
    ("L3/two-voices", "must", lambda: rules.l3_voices([["MIT"], ["Apache-2.0"]]), ["MIT", "Apache-2.0"]),
    ("L3/unidentified-is-not-a-voice", "must", lambda: rules.l3_voices([["MIT"], []]), ["MIT"]),

    # ---- Apache appendix, reported never scored --------------------------
    ("APX/unfilled", "must", lambda: rules.apache_appendix_unfilled(
        "TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION\n"
        "Copyright [yyyy] [name of copyright owner]\n", ["Apache-2.0"]), True),
    ("APX/filled", "must-not", lambda: rules.apache_appendix_unfilled(
        "TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION\nCopyright 2024 Acme\n",
        ["Apache-2.0"]), True),
    ("APX/not-apache", "must-not", lambda: rules.apache_appendix_unfilled(
        "Copyright [yyyy] [name of copyright owner]", ["MIT"]), True),
]


def run():
    results = []
    for cid, kind, fn, expected in CASES:
        try:
            got = fn()
            ok = (got == expected) if kind == "must" else (got != expected)
            err = None
        except Exception as exc:                        # a rule that raises is a failure
            got, ok, err = None, False, f"{type(exc).__name__}: {exc}"
        results.append({"id": cid, "kind": kind,
                        ("forbidden" if kind == "must-not" else "expected"): expected, "got": got,
                        "pass": ok, "error": err})
    return results


if __name__ == "__main__":
    res = run()
    failed = [r for r in res if not r["pass"]]
    out = {
        "note": "Hand-made cases for every rule of session 163, run before any repository "
                "blob was read. A fixture checks that a rule computes what its author says, "
                "never that the author wrote the right sentence.",
        "n_cases": len(res), "n_pass": len(res) - len(failed), "n_fail": len(failed),
        "cases": res,
    }
    dest = sys.argv[1] if len(sys.argv) > 1 else None
    txt = json.dumps(out, indent=1, default=str)
    if dest:
        open(dest, "w").write(txt + "\n")
    print(f"{len(res)} cases, {len(failed)} failed")
    for f in failed:
        print("  FAIL", f["id"], f["kind"], repr(f.get("expected", f.get("forbidden"))), "got", repr(f["got"]), f["error"] or "")
    sys.exit(1 if failed else 0)
