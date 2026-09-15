#!/usr/bin/env python3
"""Do the fixtures have teeth? Break each rule on purpose and see whether they notice.

35 fixtures that all pass on the first run prove nothing: the same hand wrote the rules and
the cases, so agreement may only mean the hand is consistent. This script damages the rules
one at a time — each mutation a plausible slip, not nonsense — and records which fixtures
catch it. **A mutation no fixture catches is a hole in the fixture set**, and it is reported
as one rather than quietly patched.

    python3 tools/refusal-shape/mutants.py          # write data/mutation-check.json
    python3 tools/refusal-shape/mutants.py --check  # re-run and fail on any difference

Run and committed BEFORE the first probe request.
"""
import json
import pathlib
import sys
import types

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATA = ROOT / "artifacts/2026-09-15-whose-refusal-is-it/data"
sys.path.insert(0, str(HERE))
import fixtures as F  # noqa: E402

SRC = (HERE / "coding.py").read_text()

# (id, what the slip would be, exact text, replacement)
MUTATIONS = [
    ("M1", "the robots rule is never consulted",
     'if unit.get("robots_blocked"):', 'if False:'),
    ("M2", "key-declared stops requiring the WWW-Authenticate header",
     'if statuses and all(s == 401 for s in statuses) and auth_seen:',
     'if statuses and all(s == 401 for s in statuses):'),
    ("M3", "client-string counts any non-2xx as a refusal (404 and 500 included)",
     'elif ok and refused:', 'elif ok and len(ok) < len(statuses):'),
    ("M4", "register_label_wrong also fires where the door refused everyone",
     'label_wrong = bool(claims_key and code in ("open", "client-string") and not auth_seen)',
     'label_wrong = bool(claims_key and code in ("open", "client-string", "refuses-all") and not auth_seen)'),
    ("M5", "a longer Allow no longer beats a shorter Disallow",
     'if n > best_len or (n == best_len and n >= 0 and kind == "allow"):',
     'if n > best_len:'),
    ("M6", "an empty Disallow is read as forbidding everything",
     '        return -1  # an empty Disallow forbids nothing',
     '        return 0  # an empty Disallow forbids nothing'),
    ("M7", "rules written for a named crawler are applied to us",
     'in_star = value == "*"', 'in_star = True'),
    ("M8", "open accepts an arm that never answered",
     'elif len(ok) == len(statuses) and None not in statuses:',
     'elif len(ok) == len([s for s in statuses if s is not None]):'),
    ("M9", "the named/unnamed split is read off the wrong pair",
     'if b == u and n != b:\n        return "named-apart"',
     'if b == n and u != b:\n        return "named-apart"'),
    ("M10", "the refusal set silently loses 429",
     'REFUSAL = (401, 403, 429)', 'REFUSAL = (401, 403)'),
]


def load(src):
    mod = types.ModuleType("coding_mutant")
    mod.__dict__["__file__"] = "coding_mutant"
    exec(compile(src, "coding_mutant", "exec"), mod.__dict__)
    return mod


def run_with(mod):
    """Re-run every fixture case against `mod`, returning the names that fail."""
    failed = []
    for name, unit, arms, want_code, want_wrong, _why in F.CODE_CASES:
        try:
            code, wrong, _ = mod.code_unit(unit, arms)
        except Exception as exc:  # a rule that crashes is a rule that failed
            failed.append(f"code_unit/{name} (raised {type(exc).__name__})")
            continue
        if code != want_code or wrong != want_wrong:
            failed.append(f"code_unit/{name}")
    for name, text, path, want in F.ROBOTS_CASES:
        try:
            got = mod.robots_disallows(text, path)
        except Exception as exc:
            failed.append(f"robots/{name} (raised {type(exc).__name__})")
            continue
        if got != want:
            failed.append(f"robots/{name}")
    for name, arms, want in F.PATTERN_CASES:
        if mod.arm_pattern(arms) != want:
            failed.append(f"arm_pattern/{name}")
    for name, text, want in F.CRAWL_DELAY_CASES:
        if mod.parse_robots(text)[1] != want:
            failed.append(f"crawl_delay/{name}")
    return failed


def main():
    base = load(SRC)
    baseline = run_with(base)
    rows, missed = [], 0
    for mid, story, old, new in MUTATIONS:
        if SRC.count(old) != 1:
            rows.append({"id": mid, "slip": story, "applied": False,
                         "note": f"anchor text occurs {SRC.count(old)} times; mutation not applied"})
            missed += 1
            continue
        caught = run_with(load(SRC.replace(old, new, 1)))
        rows.append({"id": mid, "slip": story, "applied": True,
                     "fixtures_that_caught_it": len(caught), "caught_by": caught[:6],
                     "survived": len(caught) == 0})
        missed += len(caught) == 0
    out = {
        "_note": "Mutation test of the fixture set (PREREGISTRATION.md §4). Each row damages one "
        "mechanical rule and reports which fixtures noticed. A surviving mutation is a hole in "
        "the fixtures and is reported, not patched away.",
        "baseline_failures": baseline,
        "mutations": len(MUTATIONS),
        "survived": missed,
        "history": [
            {
                "utc": "2026-09-15",
                "event": "On its first run, before any probe request, M5 survived: every "
                "Allow/Disallow fixture had unequal pattern lengths, so the tie-break rule was "
                "never exercised and a mutation that broke it changed no outcome. One fixture "
                "('Allow wins an equal-length tie') was added and M5 is caught. Recorded rather "
                "than quietly repaired: the fixture set as first written had a hole, and the "
                "mutation test is the only thing that found it.",
            }
        ],
        "results": rows,
    }
    if "--check" in sys.argv:
        old = json.loads((DATA / "mutation-check.json").read_text())
        same = old["results"] == rows and old["baseline_failures"] == baseline
        print("mutation-check reproduces" if same else "MUTATION CHECK DRIFTED")
        sys.exit(0 if same and not baseline and missed == 0 else 1)
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "mutation-check.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(f"baseline failures: {len(baseline)}")
    print(f"{len(MUTATIONS)} mutations, {missed} survived uncaught")
    for r in rows:
        if r.get("survived") or not r.get("applied", True):
            print("  SURVIVED:", r["id"], r["slip"])
    sys.exit(1 if baseline or missed else 0)


if __name__ == "__main__":
    main()
