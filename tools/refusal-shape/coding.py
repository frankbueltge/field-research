#!/usr/bin/env python3
"""The coding table of PREREGISTRATION.md §2.3, and the robots rule of §2.2.

This module holds every mechanical rule the study's verdicts rest on. `fixtures.py` and
`build.py` both import from here, so the rules the fixtures test are the rules that run.
A fixture that tested a copy of a rule would test nothing.
"""
import re

REFUSAL = (401, 403, 429)


def parse_robots(text):
    """Return (rules_for_star, crawl_delay) from a robots.txt body.

    rules_for_star is a list of (kind, path) with kind in {"allow", "disallow"}, in file
    order, for the `*` group only — the group that governs a client with no special name.
    A malformed or empty file yields no rules, which means: nothing is published.
    """
    rules, delay, in_star, groups_seen = [], None, False, False
    for raw in (text or "").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        field, _, value = line.partition(":")
        field = field.strip().lower()
        value = value.strip()
        if field == "user-agent":
            if groups_seen and not in_star:
                pass
            in_star = value == "*"
            groups_seen = True
            continue
        if not in_star:
            continue
        if field == "disallow":
            rules.append(("disallow", value))
        elif field == "allow":
            rules.append(("allow", value))
        elif field == "crawl-delay":
            try:
                delay = float(value)
            except ValueError:
                pass
    return rules, delay


def _match_len(pattern, path):
    """Length of `pattern` if it matches `path` under the robots wildcard convention, else -1."""
    if pattern == "":
        return -1  # an empty Disallow forbids nothing
    anchored_end = pattern.endswith("$")
    p = pattern[:-1] if anchored_end else pattern
    rx = "".join(".*" if ch == "*" else re.escape(ch) for ch in p)
    rx = "^" + rx + ("$" if anchored_end else "")
    return len(pattern) if re.search(rx, path) else -1


def robots_disallows(text, path):
    """True if robots.txt `text` disallows `path` for `*`. Longest match wins; Allow beats
    Disallow at equal length, which is the convention the major crawlers publish."""
    rules, _ = parse_robots(text)
    best_kind, best_len = None, -1
    for kind, pattern in rules:
        n = _match_len(pattern, path)
        if n > best_len or (n == best_len and n >= 0 and kind == "allow"):
            if n >= 0:
                best_kind, best_len = kind, n
    return best_kind == "disallow"


def code_unit(unit, arms):
    """Apply PREREGISTRATION.md §2.3. `arms` maps arm name -> arm record.

    An arm record carries: status (int or None), www_authenticate (bool), error (str or None).
    A unit carries: robots_blocked (bool), recorded_note (str or None), register_says_blocked.
    Returns (code, register_label_wrong, reason).
    """
    if unit.get("robots_blocked"):
        return "policy-published", False, "robots.txt disallows this path for *; not probed"

    probed = [a for a in arms.values() if a is not None]
    statuses = [a.get("status") for a in probed]
    if not probed or all(s is None for s in statuses):
        return "other", False, "no HTTP status from any arm"

    auth_seen = any(a.get("www_authenticate") for a in probed)
    ok = [s for s in statuses if s is not None and 200 <= s < 300]
    refused = [s for s in statuses if s in REFUSAL]

    if statuses and all(s == 401 for s in statuses) and auth_seen:
        code, reason = "key-declared", "every arm 401 and a WWW-Authenticate header was served"
    elif len(ok) == len(statuses) and None not in statuses:
        code, reason = "open", "every probed arm returned 2xx"
    elif ok and refused:
        code, reason = "client-string", "at least one arm 2xx and at least one arm 401/403/429"
    elif refused and len(refused) == len(statuses):
        code, reason = "refuses-all", "every arm 401/403/429, no WWW-Authenticate anywhere"
    else:
        code, reason = "other", "mixed non-refusal outcome (5xx, 404, or transport failure)"

    claims_key = bool(
        unit.get("register_says_blocked")
        or re.search(r"Anmeldung|Schl[uü]ssel|login|key", unit.get("recorded_note") or "", re.I)
    )
    label_wrong = bool(claims_key and code in ("open", "client-string") and not auth_seen)
    return code, label_wrong, reason


def arm_pattern(arms):
    """For P3: does `named` stand apart from the two unnamed clients?

    Returns one of "named-apart", "bare-apart", "urllib-apart", "all-agree", "all-differ".
    Two arms 'agree' when their status codes are equal.
    """
    s = {k: (arms.get(k) or {}).get("status") for k in ("bare", "urllib", "named")}
    b, u, n = s["bare"], s["urllib"], s["named"]
    if b == u == n:
        return "all-agree"
    if b == u and n != b:
        return "named-apart"
    if b == n and u != b:
        return "urllib-apart"
    if u == n and b != u:
        return "bare-apart"
    return "all-differ"
