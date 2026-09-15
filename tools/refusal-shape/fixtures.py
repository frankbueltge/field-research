#!/usr/bin/env python3
"""Test the tests, before the data exists (PREREGISTRATION.md §4).

Every mechanical rule this study's verdicts rest on is run here against hand-made cases:
for each rule, a case it MUST produce and at least one near-miss it MUST NOT. The near-miss
is the half that matters — the three defects this practice shipped in its last four sessions
were all rules that fired on something adjacent to their target.

    python3 tools/refusal-shape/fixtures.py          # write data/fixture-check.json
    python3 tools/refusal-shape/fixtures.py --check  # re-run and fail on any difference

Run and committed BEFORE the first probe request.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from coding import arm_pattern, code_unit, parse_robots, robots_disallows  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA = ROOT / "artifacts/2026-09-15-whose-refusal-is-it/data"


def arm(status, auth=False, error=None):
    return {"status": status, "www_authenticate": auth, "error": error}


def three(b, u, n):
    return {"bare": b, "urllib": u, "named": n}


# (name, unit, arms, expected_code, expected_label_wrong, what this case is for)
CODE_CASES = [
    # --- policy-published ----------------------------------------------------
    ("policy fires when robots disallows",
     {"robots_blocked": True}, three(None, None, None), "policy-published", False,
     "MUST fire: a published rule is a published rule even with no probe"),
    ("policy does NOT fire on a refusal with no robots rule",
     {"robots_blocked": False}, three(arm(403), arm(403), arm(403)), "refuses-all", False,
     "MUST NOT fire: silence in robots.txt is not a published ground"),

    # --- key-declared --------------------------------------------------------
    ("key-declared fires on 401 with WWW-Authenticate",
     {}, three(arm(401, True), arm(401, True), arm(401, True)), "key-declared", False,
     "MUST fire: the server published the machine-readable ground"),
    ("key-declared does NOT fire on 401 without the header",
     {}, three(arm(401), arm(401), arm(401)), "refuses-all", False,
     "MUST NOT fire: a bare 401 asserts nothing a client can act on"),
    ("key-declared does NOT fire on 403 with the header elsewhere",
     {}, three(arm(403, True), arm(403), arm(403)), "refuses-all", False,
     "MUST NOT fire: 403 is not a challenge, whatever headers ride along"),

    # --- open ----------------------------------------------------------------
    ("open fires when every arm is 2xx",
     {}, three(arm(200), arm(200), arm(204)), "open", False,
     "MUST fire: 204 is 2xx; the door opened"),
    ("open does NOT fire when one arm failed to get a status",
     {}, three(arm(200), arm(None, error="timeout"), arm(200)), "other", False,
     "MUST NOT fire: an unanswered arm is not an open door"),

    # --- client-string (the load-bearing cell) -------------------------------
    ("client-string fires when named opens what urllib is refused",
     {}, three(arm(403), arm(403), arm(200)), "client-string", False,
     "MUST fire: this is the 2026-09-11 event, as a code"),
    ("client-string fires in the other direction too",
     {}, three(arm(200), arm(200), arm(429)), "client-string", False,
     "MUST fire: the rule is about disagreement, not about named winning"),
    ("client-string does NOT fire on 200 beside a 500",
     {}, three(arm(200), arm(500), arm(200)), "other", False,
     "MUST NOT fire: a server fault is not a refusal"),
    ("client-string does NOT fire on 200 beside a 404",
     {}, three(arm(200), arm(404), arm(200)), "other", False,
     "MUST NOT fire: absence is not refusal — the distinction this practice has "
     "insisted on since the retrievability series"),

    # --- register_label_wrong ------------------------------------------------
    ("label_wrong fires when the register claims a key and the door opens",
     {"recorded_note": "Zugang erfordert Anmeldung oder Schlüssel (HTTP 403)"},
     three(arm(403), arm(403), arm(200)), "client-string", True,
     "MUST fire: the note's claim is contradicted by the door"),
    ("label_wrong does NOT fire when a key really is declared",
     {"recorded_note": "Zugang erfordert Anmeldung oder Schlüssel (HTTP 401)"},
     three(arm(401, True), arm(401, True), arm(401, True)), "key-declared", False,
     "MUST NOT fire: the register is right about this one"),
    ("label_wrong does NOT fire when the door refuses everyone",
     {"recorded_note": "Zugang erfordert Anmeldung oder Schlüssel (HTTP 403)"},
     three(arm(403), arm(403), arm(403)), "refuses-all", False,
     "MUST NOT fire: the note may be imprecise, but nothing here contradicts it"),
    ("label_wrong does NOT fire when the register claimed nothing",
     {"recorded_note": "Identifier antwortet mit HTTP 403"},
     three(arm(403), arm(403), arm(200)), "client-string", False,
     "MUST NOT fire: this note states the status and claims no ground — "
     "the near-miss that separates a wrong label from a bare one"),
]

ROBOTS_CASES = [
    ("plain disallow fires", "User-agent: *\nDisallow: /ops/\n", "/ops/x", True),
    ("plain disallow spares another path", "User-agent: *\nDisallow: /ops/\n", "/articles/1", False),
    ("empty disallow forbids nothing", "User-agent: *\nDisallow:\n", "/anything", False),
    ("a rule for another agent is not ours",
     "User-agent: 007ac9\nDisallow: /\n\nUser-agent: *\nDisallow: /ops/\n", "/articles/1", False),
    ("a rule for another agent does not leak the block",
     "User-agent: Turnitin\nDisallow: /\n", "/articles/1", False),
    ("longer Allow beats shorter Disallow",
     "User-agent: *\nDisallow: /a/\nAllow: /a/open/\n", "/a/open/1", False),
    ("shorter Allow loses to longer Disallow",
     "User-agent: *\nAllow: /a/\nDisallow: /a/closed/\n", "/a/closed/1", True),
    # Added 2026-09-15 after mutants.py M5 survived the original set: every Allow/Disallow
    # case here had unequal pattern lengths, so the tie-break was never exercised. Found
    # before the first probe ran; the gap and its closing are both in data/mutation-check.json.
    ("Allow wins an equal-length tie",
     "User-agent: *\nDisallow: /a/b/\nAllow: /a/b/\n", "/a/b/c", False),
    ("wildcard in the middle matches",
     "User-agent: *\nDisallow: /*/private\n", "/x/private", True),
    ("end anchor respected", "User-agent: *\nDisallow: /x$\n", "/x/y", False),
    ("comments and blank lines ignored",
     "# hello\n\nUser-agent: *   # star\nDisallow: /ops/\n", "/ops/", True),
    ("an unreachable robots.txt publishes nothing", "", "/anything", False),
    ("an HTML error page is not a rule",
     "<!DOCTYPE html><html><head><title>403</title></head></html>", "/anything", False),
]

PATTERN_CASES = [
    ("named apart", three(arm(403), arm(403), arm(200)), "named-apart"),
    ("all agree", three(arm(403), arm(403), arm(403)), "all-agree"),
    ("urllib apart", three(arm(200), arm(403), arm(200)), "urllib-apart"),
    ("bare apart", three(arm(403), arm(200), arm(200)), "bare-apart"),
    ("all differ", three(arm(403), arm(429), arm(200)), "all-differ"),
]

CRAWL_DELAY_CASES = [
    ("crawl-delay read from the star group", "User-agent: *\nCrawl-delay: 2\n", 2.0),
    ("crawl-delay of another agent not taken",
     "User-agent: Turnitin\nCrawl-delay: 10\n\nUser-agent: *\nDisallow:\n", None),
    ("nonsense crawl-delay ignored", "User-agent: *\nCrawl-delay: soon\n", None),
]


def run():
    results, failures = [], 0
    for name, unit, arms, want_code, want_wrong, why in CODE_CASES:
        code, wrong, reason = code_unit(unit, arms)
        ok = code == want_code and wrong == want_wrong
        failures += not ok
        results.append({"rule": "code_unit", "case": name, "purpose": why, "expected":
                        [want_code, want_wrong], "got": [code, wrong], "pass": ok,
                        "machine_reason": reason})
    for name, text, path, want in ROBOTS_CASES:
        got = robots_disallows(text, path)
        ok = got == want
        failures += not ok
        results.append({"rule": "robots_disallows", "case": name, "expected": want,
                        "got": got, "pass": ok})
    for name, arms, want in PATTERN_CASES:
        got = arm_pattern(arms)
        ok = got == want
        failures += not ok
        results.append({"rule": "arm_pattern", "case": name, "expected": want, "got": got,
                        "pass": ok})
    for name, text, want in CRAWL_DELAY_CASES:
        got = parse_robots(text)[1]
        ok = got == want
        failures += not ok
        results.append({"rule": "parse_robots.crawl_delay", "case": name, "expected": want,
                        "got": got, "pass": ok})
    return results, failures


def main():
    results, failures = run()
    must_fire = sum(1 for r in results if r["rule"] == "code_unit" and "MUST fire" in r.get("purpose", ""))
    must_not = sum(1 for r in results if r["rule"] == "code_unit" and "MUST NOT" in r.get("purpose", ""))
    out = {
        "_note": "PREREGISTRATION.md §4 — every mechanical rule run against hand-made cases "
        "before the first probe request. The near-misses are the point.",
        "cases": len(results),
        "failures": failures,
        "code_unit_must_fire": must_fire,
        "code_unit_must_not_fire": must_not,
        "results": results,
    }
    if "--check" in sys.argv:
        old = json.loads((DATA / "fixture-check.json").read_text())
        same = old["results"] == results and old["failures"] == failures
        print("fixture-check reproduces" if same else "FIXTURE CHECK DRIFTED")
        sys.exit(0 if same and failures == 0 else 1)
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "fixture-check.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(f"{len(results)} fixture cases, {failures} failing "
          f"({must_fire} must-fire / {must_not} must-not-fire on the coding table)")
    for r in results:
        if not r["pass"]:
            print("  FAIL:", r["case"], r["expected"], "->", r["got"])
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
