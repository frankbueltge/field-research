#!/usr/bin/env python3
"""Break each rule on purpose and see whether the hand-made cases notice.

Session 163, 2026-09-18, run before any repository blob was read. A mutation that no
case catches is a hole in the case list, not a harmless one. Run:
    python3 mutants.py [out.json]

The boundary, demonstrated on 09-15 and 09-16 and asserted no further here: this
catches a rule that does not compute what its author said. It cannot catch an author
who wrote the wrong sentence, and on both those nights that is exactly what happened.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rules
import fingerprints as fp
import fixtures

ORIG = {k: getattr(rules, k) for k in
        ("is_licence_shaped", "l0_nonempty", "l1_families", "l2_attribution",
         "l3_voices", "file_delivers", "apache_appendix_unfilled",
         "normalise", "has_placeholder", "holder_of", "copyright_lines",
         "SCORED_FAMILIES", "LICENCE_BASENAME_RE")}


def restore():
    for k, v in ORIG.items():
        setattr(rules, k, v)


def _mut_shape_always():
    rules.is_licence_shaped = lambda p: True


def _mut_shape_no_suffix():
    rx = re.compile(r"^(licen[cs]e|copying|unlicense|copyright)$", re.I)
    rules.is_licence_shaped = lambda p: bool(rx.match(p.rsplit("/", 1)[-1]))


def _mut_shape_case_sensitive():
    rx = re.compile(r"^(licen[cs]e|copying|unlicense|copyright)([.\-_].*)?$")
    rules.is_licence_shaped = lambda p: bool(rx.match(p.rsplit("/", 1)[-1]))


def _mut_l0_whitespace_counts():
    rules.l0_nonempty = lambda raw: raw is not None


def _mut_norm_no_collapse():
    rules.normalise = lambda t: t.lower()


def _mut_norm_no_lower():
    rules.normalise = lambda t: re.sub(r"\s+", " ", t).strip()


def _mut_norm_no_quote_fold():
    """Fold everything EXCEPT the curly quotes. Expected to survive: see below."""
    quotes = "\u2018\u2019\u201a\u201b\u201c\u201d\u201e\u201f"
    def f(t):
        for a, b in fp._QUOTES.items():
            if a in quotes:
                continue
            t = t.replace(a, b)
        return re.sub(r"\s+", " ", t.lower()).strip()
    rules.normalise = f


def _mut_norm_no_dash_fold():
    def f(t):
        for a, b in fp._QUOTES.items():
            if a in "\u2013\u2014\u2212":
                continue
            t = t.replace(a, b)
        return re.sub(r"\s+", " ", t.lower()).strip()
    rules.normalise = f


def _mut_norm_no_nbsp_fold():
    def f(t):
        for a, b in fp._QUOTES.items():
            if a == "\u00a0":
                continue
            t = t.replace(a, b)
        return re.sub(r"[ \t\r\n]+", " ", t.lower()).strip()
    rules.normalise = f


def _mut_l1_ignore_none_of():
    def f(raw):
        if not rules.l0_nonempty(raw):
            return []
        n = rules.normalise(raw)
        out = []
        for name, spec in fp.FAMILIES:
            if any(p in n for p in spec["any_of"]) and all(
                    p in n for p in spec.get("requires_all", [])):
                out.append(name)
        return out
    rules.l1_families = f


def _mut_l1_ignore_requires_all():
    def f(raw):
        if not rules.l0_nonempty(raw):
            return []
        n = rules.normalise(raw)
        out = []
        for name, spec in fp.FAMILIES:
            if any(p in n for p in spec["any_of"]) and not any(
                    p in n for p in spec.get("none_of", [])):
                out.append(name)
        return out
    rules.l1_families = f


def _mut_l1_prefix_match():
    def f(raw):
        if not rules.l0_nonempty(raw):
            return []
        n = rules.normalise(raw)
        return [name for name, spec in fp.FAMILIES
                if any(p[:12] in n for p in spec["any_of"])]
    rules.l1_families = f


def _mut_l1_skips_empty_check():
    def f(raw):
        n = rules.normalise(raw or "")
        return [name for name, spec in fp.FAMILIES if any(p in n for p in spec["any_of"])] or ["MIT"]
    rules.l1_families = f


def _mut_placeholder_never():
    rules.has_placeholder = lambda line: False


def _mut_placeholder_bare_substring():
    def f(line):
        low = line.lower()
        return any(p in low for p in fp.PLACEHOLDERS) or any(
            w in low for w in fp.PLACEHOLDER_WORDS)
    rules.has_placeholder = f


def _mut_placeholder_always():
    rules.has_placeholder = lambda line: True


def _mut_holder_keeps_years():
    def f(line):
        s = re.sub(r"(?i)^[\s#*/;%!<>\-=_|\.]*(copyright\b|\(c\)|©)*[\s,\.:\-]*", "", line)
        return s.strip(" \t,.:;-()[]<>*#/")
    rules.holder_of = f


def _mut_holder_whole_line():
    rules.holder_of = lambda line: line.strip()


def _mut_l2_named_if_any_line():
    def f(raw, families):
        if not any(x in rules.SCORED_FAMILIES for x in families):
            return None
        return "named" if rules.copyright_lines(raw or "") else "no_copyright_line"
    rules.l2_attribution = f


def _mut_l2_scores_every_family():
    def f(raw, families):
        lines = rules.copyright_lines(raw or "")
        if not lines:
            return "no_copyright_line"
        for ln in lines:
            if not rules.has_placeholder(ln) and rules.holder_of(ln):
                return "named"
        return "placeholder"
    rules.l2_attribution = f


def _mut_l2_placeholder_wins():
    def f(raw, families):
        if not any(x in rules.SCORED_FAMILIES for x in families):
            return None
        lines = rules.copyright_lines(raw or "")
        if not lines:
            return "no_copyright_line"
        vs = ["placeholder" if rules.has_placeholder(l) else
              ("named" if rules.holder_of(l) else "no_holder") for l in lines]
        if "placeholder" in vs:
            return "placeholder"
        return "named" if "named" in vs else "no_holder"
    rules.l2_attribution = f


def _mut_l3_first_file_only():
    rules.l3_voices = lambda per_file: list(per_file[0]) if per_file else []


def _mut_delivers_ignores_l2():
    def f(raw):
        if not rules.l0_nonempty(raw):
            return False, "empty"
        return (True, "identified") if rules.l1_families(raw) else (False, "not_identified")
    rules.file_delivers = f


def _mut_delivers_ignores_l1():
    def f(raw):
        return (True, "nonempty") if rules.l0_nonempty(raw) else (False, "empty")
    rules.file_delivers = f


def _mut_apache_drops_family_check():
    rules.apache_appendix_unfilled = lambda raw, fams: any(
        rules.has_placeholder(l) for l in rules.copyright_lines(raw or ""))


# One mutation is expected to survive, and the reason is checked rather than asserted:
# no phrase in the table carries a quote character, so folding curly quotes cannot
# change an L1 verdict. Fixture TABLE/no-phrase-carries-a-quote holds that reason to
# account. The fold stays in the code because the table may gain a quoted phrase.
EXPECTED_SURVIVORS = {"norm/no-quote-fold"}

MUTANTS = [
    ("shape/always-true", _mut_shape_always),
    ("shape/no-suffix-group", _mut_shape_no_suffix),
    ("shape/case-sensitive", _mut_shape_case_sensitive),
    ("L0/whitespace-counts", _mut_l0_whitespace_counts),
    ("norm/no-whitespace-collapse", _mut_norm_no_collapse),
    ("norm/no-lowercase", _mut_norm_no_lower),
    ("norm/no-quote-fold", _mut_norm_no_quote_fold),
    ("norm/no-dash-fold", _mut_norm_no_dash_fold),
    ("norm/no-nbsp-fold", _mut_norm_no_nbsp_fold),
    ("L1/ignore-none-of", _mut_l1_ignore_none_of),
    ("L1/ignore-requires-all", _mut_l1_ignore_requires_all),
    ("L1/prefix-match-only", _mut_l1_prefix_match),
    ("L1/no-empty-check", _mut_l1_skips_empty_check),
    ("placeholder/never-fires", _mut_placeholder_never),
    ("placeholder/bare-word-substring", _mut_placeholder_bare_substring),
    ("placeholder/always-fires", _mut_placeholder_always),
    ("holder/keeps-years", _mut_holder_keeps_years),
    ("holder/whole-line", _mut_holder_whole_line),
    ("L2/named-if-any-copyright-line", _mut_l2_named_if_any_line),
    ("L2/scores-every-family", _mut_l2_scores_every_family),
    ("L2/placeholder-beats-named", _mut_l2_placeholder_wins),
    ("L3/first-file-only", _mut_l3_first_file_only),
    ("HEAD/ignores-L2", _mut_delivers_ignores_l2),
    ("HEAD/ignores-L1", _mut_delivers_ignores_l1),
    ("APX/drops-family-check", _mut_apache_drops_family_check),
]


def main():
    baseline = fixtures.run()
    base_fail = [r["id"] for r in baseline if not r["pass"]]
    rows = []
    for name, apply_fn in MUTANTS:
        restore()
        apply_fn()
        try:
            res = fixtures.run()
            caught = [r["id"] for r in res if not r["pass"]]
        finally:
            restore()
        rows.append({"mutant": name, "n_caught": len(caught), "caught_by": caught[:6],
                     "survived": len(caught) == 0,
                     "expected_to_survive": name in EXPECTED_SURVIVORS})
    restore()
    survivors = [r for r in rows if r["survived"]]
    unexpected = [r for r in survivors if not r["expected_to_survive"]]
    missing = [r for r in rows if r["expected_to_survive"] and not r["survived"]]
    out = {
        "note": "Each rule broken on purpose; a mutation no hand-made case notices is a "
                "hole in the case list. Run before any repository blob was read.",
        "baseline_failures": base_fail,
        "n_mutants": len(rows), "n_survived": len(survivors),
        "expected_survivors": sorted(EXPECTED_SURVIVORS),
        "unexpected_survivors": [r["mutant"] for r in unexpected],
        "expected_survivors_that_were_caught": [r["mutant"] for r in missing],
        "mutants": rows,
    }
    txt = json.dumps(out, indent=1)
    if len(sys.argv) > 1:
        open(sys.argv[1], "w").write(txt + "\n")
    print(f"baseline failures: {len(base_fail)}; {len(rows)} mutants, "
          f"{len(survivors)} survived ({len(unexpected)} unexpectedly)")
    for s in unexpected:
        print("  SURVIVED UNEXPECTEDLY", s["mutant"])
    for s in missing:
        print("  EXPECTED TO SURVIVE BUT WAS CAUGHT", s["mutant"])
    return 1 if (unexpected or missing or base_fail) else 0


if __name__ == "__main__":
    sys.exit(main())
