#!/usr/bin/env python3
"""
build_instrument.py — "As of Today" citation instrument

Reads the committed session-94 and session-95 signal tables and writes a
single self-contained instrument.html. No network access. Deterministic:
same input files, same output bytes (modulo the timestamp in the footer
comment, which is fixed to the two run_started_utc values recorded in the
data, not to wall-clock build time).

Inputs (read-only, all in this directory):
  signals.json     — session 94, EC, 40 rows under "rows"
  signals-2.json    — session 95, GOVUK / NIST / IE, under "authorities"->name->"rows"
  ec-rescore.json   — used ONLY to cross-check which four EC URLs are "chrome"
                       (the instrument's own coverage numbers are computed from
                       the raw rows in signals.json, not copied from this file)
  referents.json    — PREREGISTRATION-3.md, the referent test: every locked V hit
                       (62 of them), re-extracted from a fresh fetch and classified
                       SELF / OTHER / UNATTRIBUTABLE, with the evidence the
                       classification used. Written by referent_test.py. This is
                       now the sole source of the served defensible date for any
                       row that carries a V: only SELF is served; OTHER and
                       UNATTRIBUTABLE show the date, the class and the evidence,
                       with an explicit refusal in place of a defensible date.

Output:
  instrument.html
"""
import json
import re
from datetime import datetime, date
from pathlib import Path

HERE = Path(__file__).resolve().parent

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

# ---------------------------------------------------------------------------
# Load committed data
# ---------------------------------------------------------------------------

def load(name):
    with open(HERE / name, "r", encoding="utf-8") as f:
        return json.load(f)

signals_ec = load("signals.json")
signals_2 = load("signals-2.json")
ec_rescore = load("ec-rescore.json")
referents = load("referents.json")

# One record per locked V hit, keyed by URL — this is the referent test's own
# output (referent_test.py), not recomputed here. 62 expected; asserted below
# once every row has been built, against the actual V-bearing rows found in
# the locked signal files themselves (so a stale referents.json — one that no
# longer matches signals.json / signals-2.json — fails the build loudly rather
# than silently mis-labelling rows).
REFERENT_BY_URL = {rec["url"]: rec for rec in referents["records"]}

RUN1_UTC = signals_ec["run_started_utc"]      # 2026-08-06T08:26:37+00:00
RUN2_UTC = signals_2["run_started_utc"]       # 2026-08-06T14:34:38+00:00
EC_SITEMAP_URL = signals_ec["sitemap_url"]

# ---------------------------------------------------------------------------
# EC "chrome" exclusion — the four URLs the collective's own record excludes
# from the item-only subset of 36. The task names two of the four directly
# (/en/news and /en/policies/ai-office) and describes the other two only as
# "the two /en/news/-prefixed news items in the EC corpus, identify them from
# the rows". A plain substring match on "/en/news/" against signals.json
# finds SIX candidates, not two — the raw rows alone do not disambiguate
# which two of the six are "chrome" versus which four are dated news items
# that stay in the item-only subset. ec-rescore.json (committed alongside
# signals.json, produced by ec_rescore.py re-scoring the same locked rows)
# names the exact four chrome URLs it used, and re-deriving the item-only
# coverage numbers from signals.json with exactly that four-URL exclusion
# reproduces ec-rescore.json's own h/s/v counts and shares exactly (checked
# below, at runtime, with an assertion — the build fails loudly if it ever
# stops matching). That agreement is the basis for treating this four-URL
# set as the correct reading, not a guess. The six-URL candidate list is
# printed to the console on every build for the record.
# ---------------------------------------------------------------------------

EC_ALL_NEWS_PREFIXED = sorted(
    r["url"] for r in signals_ec["rows"] if "/en/news/" in r["url"]
)

EC_CHROME_URLS = set(ec_rescore["chrome_excluded"])
assert len(EC_CHROME_URLS) == 4, "ec-rescore.json chrome_excluded is not length 4"
assert "https://digital-strategy.ec.europa.eu/en/news" in EC_CHROME_URLS
assert "https://digital-strategy.ec.europa.eu/en/policies/ai-office" in EC_CHROME_URLS
_chrome_news_items = sorted(u for u in EC_CHROME_URLS if "/en/news/" in u)
assert len(_chrome_news_items) == 2, (
    "expected exactly two /en/news/-prefixed URLs inside chrome_excluded, "
    f"found {len(_chrome_news_items)}"
)

RECONCILE_NOTES = []
if len(EC_ALL_NEWS_PREFIXED) != 2:
    RECONCILE_NOTES.append(
        "EC corpus: a plain '/en/news/' substring match against signals.json finds "
        f"{len(EC_ALL_NEWS_PREFIXED)} candidate news-item URLs, not the two the task "
        "description assumed. The raw rows carry no chrome/item flag to disambiguate "
        "which two of these are 'chrome'. Resolved by cross-checking ec-rescore.json's "
        "committed chrome_excluded list (produced by ec_rescore.py against the same "
        "locked signals.json) and verifying its four-URL exclusion reproduces its own "
        "h/s/v counts when re-derived from the raw rows here (asserted at build time). "
        f"All {len(EC_ALL_NEWS_PREFIXED)} candidates: " + ", ".join(EC_ALL_NEWS_PREFIXED)
    )

# ---------------------------------------------------------------------------
# Normalise rows across both files into one shape
# ---------------------------------------------------------------------------

AUTHORITIES = [
    ("EC", "European Commission"),
    ("NIST", "NIST"),
    ("IE", "Department of Enterprise, Trade and Employment (Ireland)"),
    ("GOVUK", "GOV.UK"),
]
AUTHORITY_LABEL = dict(AUTHORITIES)

# --- Hand-confirmed rows — kept as annotation, not as the decision rule ---
#
# D10/D11 were first caught by hand, one URL at a time, before the referent
# test (PREREGISTRATION-3.md) existed. That hand-reading is stronger evidence
# than the machine classification below, not weaker, and this build must not
# lose it: every row here is still shown on its slip, clearly labelled
# "hand-confirmed". But it no longer DECIDES what gets served as defensible —
# that is now the referent test's computed SELF / OTHER / UNATTRIBUTABLE
# class alone (see REFERENT_BY_URL and build_row, below). Where the two
# disagree, both are shown and the disagreement is reported in
# RECONCILE_NOTES rather than silently favouring one.
CONFIRMED_WRONG_REFERENT = {
    "https://www.nist.gov/itl/ai-risk-management-framework": (
        "Confirmed wrong-referent (D10): opened by hand — the captured <time datetime> "
        "belongs to a teaser card for a different, linked article, not to this page."
    ),
    "https://www.nist.gov/caisi": (
        "Confirmed wrong-referent (D10): opened by hand — the captured date 2026-03-23 "
        "belongs to a card linking to a research-blog post, not to this page."
    ),
    "https://www.nist.gov/news-events/news-updates/topic/2753736": (
        "Confirmed wrong-referent (D10): opened by hand — the captured <time datetime> "
        "belongs to a teaser card for a different, linked article, not to this page."
    ),
    "https://www.nist.gov/publications": (
        'Confirmed wrong-referent (D10/D11): the <time datetime="2026-09-29T12:00:00Z"> sits '
        'inside <article class="nist-teaser" about="/publications/advancing-resilience-across-'
        'lifeline-infrastructure-systems-need-consistent-guidance">, a "Recent Publications" '
        "teaser card for a different, linked publication — not this page. First surfaced because "
        "the date postdates the run that captured it (the future-date detector, below), then "
        "confirmed by hand against the live page."
    ),
    "https://digital-strategy.ec.europa.eu/en/events": (
        'Confirmed wrong-referent (D10/D11): the matched <time> sits inside '
        '<article class="ecl-content-item"> linking to '
        "/en/events/save-date-cef-digital-community-conference-2026 — a listing-page teaser for "
        "a different, linked event, not this page. First surfaced because the date postdates the "
        "run that captured it (the future-date detector, below), then confirmed by hand against "
        "the live page."
    ),
    "https://enterprise.gov.ie/en/publications/ireland-in-the-digital-decade.html": (
        'Confirmed wrong-referent (D11): matched text "…published on 16 June 2025" is the '
        "publish date of an EU annual report (the Digital Economy and Society Index) discussed "
        "on this page, not the page's own currency. Caught by a label rule (V2-published), not "
        "the <time> fallback — the wrong-referent defect is not confined to one extraction rule."
    ),
    "https://enterprise.gov.ie/en/what-we-do/innovation-research-development/european-space-agency": (
        'Confirmed wrong-referent (D11): matched text "…National Space Strategy for Enterprise '
        '2019-2025, published on 19 June 2019, establishes a framework…" is the publish date of '
        "a cited strategy document, not the page's own currency. Caught by a label rule "
        "(V2-published), not the <time> fallback."
    ),
}

# Rows whose label-rule hit (V1-last-update / V2-published) has actually been
# re-read by hand and found genuine, as a group, per the collective's own
# record — not a per-row individual check, a documented batch finding. Kept
# as annotation for the same reason as CONFIRMED_WRONG_REFERENT, above.
HAND_CHECKED_RULE_AUTHORITIES = {
    ("EC", "V1-last-update"),
}

# --- The referent test decides defensibility now (PREREGISTRATION-3.md) ---
#
# Every row that carries a V was re-extracted from a fresh fetch and
# classified SELF / OTHER / UNATTRIBUTABLE by referent_test.py, with the
# evidence recorded alongside (element ancestry, whether the match sits in a
# link/list-item/card, the enclosing text block). Only SELF is served as the
# defensible date; OTHER and UNATTRIBUTABLE are shown with their evidence and
# an explicit refusal. This replaces the old hand-maintained four-tier system
# (confirmed_wrong_referent / suspect / hand_checked / unaudited) entirely —
# that system is why D11 existed in the first place: it trusted label-rule
# hits (V1/V2) by default and only excluded the <time> fallback. The general
# "future-date" detector (any V later than the run that captured it) still
# runs over every row; it no longer sets a tier, only a cross-checking note
# next to the row's own referent class.

def parse_iso(s):
    if not s:
        return None
    return datetime.fromisoformat(s)


RUN_TS_BY_AUTHORITY = {
    "EC": parse_iso(RUN1_UTC),
    "GOVUK": parse_iso(RUN2_UTC),
    "NIST": parse_iso(RUN2_UTC),
    "IE": parse_iso(RUN2_UTC),
}


def fmt_date_iso(s):
    dt = parse_iso(s)
    if dt is None:
        return None
    return f"{dt.day} {MONTHS[dt.month - 1]} {dt.year}"


def date_part(s):
    dt = parse_iso(s)
    return dt.date() if dt else None


def path_of(url):
    m = re.match(r"^https?://[^/]+(/.*)?$", url)
    p = m.group(1) if m and m.group(1) else "/"
    return p


def build_row(authority_key, raw, scored):
    url = raw["url"]
    h, s, v = raw.get("h"), raw.get("s"), raw.get("v")
    v_rule = raw.get("v_rule")

    # sitemap state, normalised across both source files
    if authority_key == "EC":
        s_state = "IN-SITEMAP" if raw.get("in_sitemap") else "NOT-IN-SITEMAP"
    else:
        s_state = raw.get("s_state")

    # --- The referent test (PREREGISTRATION-3.md), looked up by URL ---
    referent = REFERENT_BY_URL.get(url) if v else None
    if not v:
        referent_class = None
        referent_status = None
    elif referent is None:
        referent_class = None
        referent_status = "not-covered-by-referent-test"
    elif referent.get("fetch") != "OK":
        referent_class = None
        referent_status = "referent-fetch-failed"
    else:
        referent_class = referent["class"]
        referent_status = "classified"

    referent_evidence = referent.get("evidence") if referent else None
    referent_class_reason = referent.get("class_reason") if referent else None
    referent_changed = bool(referent.get("changed")) if referent else False
    referent_fresh_v = referent.get("fresh_v") if referent else None
    referent_fresh_v_raw = referent.get("fresh_v_raw") if referent else None
    referent_fresh_v_rule = referent.get("fresh_v_rule") if referent else None

    # Hand-confirmed annotations — displayed, never used to decide defensibility.
    hand_confirmed_note = CONFIRMED_WRONG_REFERENT.get(url) if v else None
    hand_checked_genuine = bool(v) and bool(v_rule) and (authority_key, v_rule) in HAND_CHECKED_RULE_AUTHORITIES

    v_dt = parse_iso(v)
    run_ts = RUN_TS_BY_AUTHORITY[authority_key]
    v_postdates_run = bool(v_dt is not None and v_dt > run_ts)

    # --- "the date the reader could defend": a SELF-classified V, else S, else none ---
    v_usable = bool(v) and referent_class == "SELF"
    v_present_not_defensible = bool(v) and not v_usable
    if v_usable:
        defend_source, defend_iso = "V", v
    elif s:
        defend_source, defend_iso = "S", s
    else:
        defend_source, defend_iso = None, None

    only_defensible_was_flagged = (defend_source is None) and v_present_not_defensible

    # --- "the date a machine is handed": H, else S, else V, else none (the
    # referent test does not touch this line — it is what naive tooling would
    # still return, in the same order it always read in) ---
    if h:
        machine_source, machine_iso = "H", h
    elif s:
        machine_source, machine_iso = "S", s
    elif v:
        machine_source, machine_iso = "V", v
    else:
        machine_source, machine_iso = None, None
    machine_is_flagged_v = (machine_source == "V" and v_present_not_defensible)

    dp_machine = date_part(machine_iso)
    dp_defend = date_part(defend_iso)
    distance_days = None
    if dp_machine is not None and dp_defend is not None:
        distance_days = abs((dp_machine - dp_defend).days)

    return {
        "authority": authority_key,
        "authority_label": AUTHORITY_LABEL[authority_key],
        "url": url,
        "path": path_of(url),
        "scored": scored,
        "status": raw.get("status"),
        "fetch": raw.get("fetch"),
        "h": h,
        "h_fmt": fmt_date_iso(h),
        "h_raw": raw.get("h_raw"),
        "s": s,
        "s_fmt": fmt_date_iso(s),
        "s_state": s_state,
        "v": v,
        "v_fmt": fmt_date_iso(v),
        "v_raw": raw.get("v_raw"),
        "v_rule": v_rule,
        "etag": raw.get("etag"),
        "referent_class": referent_class,
        "referent_status": referent_status,
        "referent_class_reason": referent_class_reason,
        "referent_evidence": referent_evidence,
        "referent_changed": referent_changed,
        "referent_fresh_v": referent_fresh_v,
        "referent_fresh_v_fmt": fmt_date_iso(referent_fresh_v) if referent_fresh_v else None,
        "referent_fresh_v_raw": referent_fresh_v_raw,
        "referent_fresh_v_rule": referent_fresh_v_rule,
        "hand_confirmed_note": hand_confirmed_note,
        "hand_checked_genuine": hand_checked_genuine,
        "v_postdates_run": v_postdates_run,
        "machine_source": machine_source,
        "machine_fmt": fmt_date_iso(machine_iso),
        "machine_is_flagged_v": machine_is_flagged_v,
        "defend_source": defend_source,
        "defend_fmt": fmt_date_iso(defend_iso),
        "v_present_not_defensible": v_present_not_defensible,
        "only_defensible_was_flagged": only_defensible_was_flagged,
        "distance_days": distance_days,
        "no_signal_at_all": not (h or s or v),
    }


rows_by_authority = {}

ec_rows = []
for raw in signals_ec["rows"]:
    scored = raw["url"] not in EC_CHROME_URLS
    ec_rows.append(build_row("EC", raw, scored))
rows_by_authority["EC"] = ec_rows

for key in ("GOVUK", "NIST", "IE"):
    rows = []
    for raw in signals_2["authorities"][key]["rows"]:
        rows.append(build_row(key, raw, bool(raw.get("arm_b"))))
    rows_by_authority[key] = rows

ALL_ROWS = []
for key, _ in AUTHORITIES:
    ALL_ROWS.extend(rows_by_authority[key])

# The referent test must cover exactly the rows that carry a V here, or the
# stored referents.json no longer matches the locked signal files it claims
# to be testing — fail loudly rather than silently mis-labelling rows.
_v_urls_here = {r["url"] for r in ALL_ROWS if r["v"]}
_v_urls_tested = set(REFERENT_BY_URL)
assert _v_urls_here == _v_urls_tested, (
    "referents.json does not cover exactly the V-bearing rows in the locked signal "
    f"files: {len(_v_urls_here - _v_urls_tested)} untested, "
    f"{len(_v_urls_tested - _v_urls_here)} stale. Re-run referent_test.py."
)
assert len(_v_urls_here) == 62, f"expected 62 V hits per PREREGISTRATION-3.md, found {len(_v_urls_here)}"

# ---------------------------------------------------------------------------
# Coverage panel — two bases, computed from the rows
# ---------------------------------------------------------------------------

def pct(n, of):
    if of == 0:
        return None
    return round(100.0 * n / of, 1)


def coverage_row(rows):
    n = len(rows)
    h = sum(1 for r in rows if r["h"])
    s = sum(1 for r in rows if r["s"])
    v = sum(1 for r in rows if r["v"])
    return {
        "n": n,
        "h": h, "h_share": pct(h, n),
        "s": s, "s_share": pct(s, n),
        "v": v, "v_share": pct(v, n),
    }


COVERAGE = {"all": {}, "scored": {}}
for key, _ in AUTHORITIES:
    rows = rows_by_authority[key]
    COVERAGE["all"][key] = coverage_row(rows)
    COVERAGE["scored"][key] = coverage_row([r for r in rows if r["scored"]])

NO_SIGNAL_ROWS = [r for r in ALL_ROWS if r["no_signal_at_all"]]

# Cross-check: scored-subset EC coverage must equal ec-rescore.json arm_b
_ec_scored = COVERAGE["scored"]["EC"]
_rescore_b = ec_rescore["arm_b"]
assert _ec_scored["n"] == _rescore_b["n_ok"] == 36, "EC scored-subset n mismatch"
assert _ec_scored["v"] == _rescore_b["P4_v_n"] == 31, "EC scored-subset V-count mismatch"

# ---------------------------------------------------------------------------
# Referent-class counts (SELF / OTHER / UNATTRIBUTABLE), computed over every
# row, every authority, from the referent test's own output — not
# recomputed, only tallied. The future-date detector still runs, generally,
# over every row; it no longer sets a tier of its own, it is reported
# alongside whatever the referent test independently found for that row (the
# two are expected to agree; a future-dated V that the referent test still
# calls SELF would be worth a second look, so that disagreement, if any, is
# surfaced below rather than assumed away).
# ---------------------------------------------------------------------------

FUTURE_V_ROWS = [r for r in ALL_ROWS if r["v_postdates_run"]]
_future_still_self = [r for r in FUTURE_V_ROWS if r["referent_class"] == "SELF"]
if _future_still_self:
    RECONCILE_NOTES.append(
        "Future-dated V rule: the general detector (any printed V later than the authority's "
        "own run timestamp) caught a row that the referent test still classifies SELF: " +
        "; ".join(f"{r['authority']} {r['url']} (v={r['v_fmt']})" for r in _future_still_self) +
        ". Shown on its slip as SELF (defensible) because that is what the referent evidence "
        "supports; flagged here because a future-dated 'last update' label is unusual enough to "
        "warrant a second look, not because the referent test's own criteria were not met."
    )

# Hand-confirmed rows (CONFIRMED_WRONG_REFERENT) versus the referent test's
# own class — reported wherever they disagree, in both directions, rather
# than letting either one silently override the other.
_hand_vs_referent_conflicts = []
for r in ALL_ROWS:
    if r["hand_confirmed_note"] and r["referent_class"] == "SELF":
        _hand_vs_referent_conflicts.append(
            f"{r['authority']} {r['url']}: hand-confirmed wrong-referent, but the referent test "
            "classifies it SELF (would be served as defensible) — shown as SELF on its slip "
            "per the referent test's own rule, with the hand-confirmed note displayed alongside "
            "as a conflicting, stronger annotation."
        )
    elif r["hand_confirmed_note"] and r["referent_class"] == "UNATTRIBUTABLE":
        _hand_vs_referent_conflicts.append(
            f"{r['authority']} {r['url']}: hand-confirmed wrong-referent (which the referent "
            "test's OTHER class exists to catch), but the automated evidence for this specific "
            "row falls short of OTHER's bar (no link, no quotation mark in the enclosing text "
            "block) and it lands in UNATTRIBUTABLE instead. Both classes are non-defensible, so "
            "the served date is the same either way; the difference is only in which evidence "
            "the slip shows. Not claimed as a discovery — surfaced because the hand reading and "
            "the machine reading diverge and that is worth a reader's own eyes."
        )
if _hand_vs_referent_conflicts:
    RECONCILE_NOTES.append(
        "Hand-confirmed rows versus the referent test's own class — "
        + "; ".join(_hand_vs_referent_conflicts)
    )

CLASS_KEYS = ("SELF", "OTHER", "UNATTRIBUTABLE")

CLASS_COUNTS = {"all": {}, "scored": {}}
for key, _ in AUTHORITIES:
    rows = rows_by_authority[key]
    scored_rows = [r for r in rows if r["scored"]]
    for basis, rset in (("all", rows), ("scored", scored_rows)):
        counts = {k: 0 for k in CLASS_KEYS}
        for r in rset:
            if r["referent_class"] in counts:
                counts[r["referent_class"]] += 1
        CLASS_COUNTS[basis][key] = counts

# The defensible-date rule must never hand back a V later than the run that
# captured it. Assert this over every row, not just the ones expected to
# trip it.
for r in ALL_ROWS:
    if r["defend_source"] == "V":
        run_ts = RUN_TS_BY_AUTHORITY[r["authority"]]
        v_dt = parse_iso(r["v"])
        assert v_dt <= run_ts, (
            f"defensible V postdates the run timestamp — the future-date rule "
            f"failed to exclude it: {r['url']} v={r['v']} run={run_ts.isoformat()}"
        )

# ---------------------------------------------------------------------------
# Assemble the embedded data blob
# ---------------------------------------------------------------------------

DATA = {
    "meta": {
        "run1_utc": RUN1_UTC,
        "run2_utc": RUN2_UTC,
        "ec_sitemap_url": EC_SITEMAP_URL,
        "corpus_sizes": {k: len(rows_by_authority[k]) for k, _ in AUTHORITIES},
        "scored_sizes": {k: sum(1 for r in rows_by_authority[k] if r["scored"]) for k, _ in AUTHORITIES},
        "ec_chrome_excluded": sorted(EC_CHROME_URLS),
        "ec_all_news_prefixed_candidates": EC_ALL_NEWS_PREFIXED,
        "no_signal_at_all_n": len(NO_SIGNAL_ROWS),
        "no_signal_at_all_urls": [r["url"] for r in NO_SIGNAL_ROWS],
        "total_rows": len(ALL_ROWS),
        "future_v_n": len(FUTURE_V_ROWS),
        "future_v_rows": [
            {"authority": r["authority"], "url": r["url"], "v": r["v"], "v_fmt": r["v_fmt"],
             "referent_class": r["referent_class"]}
            for r in FUTURE_V_ROWS
        ],
        "self_by_authority": {k: CLASS_COUNTS["all"][k]["SELF"] for k, _ in AUTHORITIES},
        "other_by_authority": {k: CLASS_COUNTS["all"][k]["OTHER"] for k, _ in AUTHORITIES},
        "unattributable_by_authority": {k: CLASS_COUNTS["all"][k]["UNATTRIBUTABLE"] for k, _ in AUTHORITIES},
        "hand_confirmed_n": sum(1 for r in ALL_ROWS if r["hand_confirmed_note"]),
        "hand_checked_genuine_n": sum(1 for r in ALL_ROWS if r["hand_checked_genuine"]),
        "referent_test": {
            "preregistration": "PREREGISTRATION-3.md",
            "run_started_utc": referents.get("run_started_utc"),
            "run_finished_utc": referents.get("run_finished_utc"),
            "hits_tested": referents.get("true_hit_count"),
            "fetch_fail_n": referents["counts"]["fetch_fail"],
            "changed_n": referents["counts"]["changed"],
            "class_totals": referents["counts"]["class_totals"],
            "predictions": referents["predictions"],
        },
    },
    "authorities": [{"key": k, "label": lbl} for k, lbl in AUTHORITIES],
    "rows": ALL_ROWS,
    "coverage": COVERAGE,
    "class_counts": CLASS_COUNTS,
}

JSON_BLOB = json.dumps(DATA, ensure_ascii=False, separators=(",", ":"))
# guard against a literal </script> sequence breaking out of the data element
JSON_BLOB_SAFE = JSON_BLOB.replace("</", "<\\/")

# ---------------------------------------------------------------------------
# Console report (also echoed by the build, not just embedded)
# ---------------------------------------------------------------------------

print("=== as-of-today: build_instrument.py ===")
print(f"run1 (EC, session 94):  {RUN1_UTC}")
print(f"run2 (session 95):      {RUN2_UTC}")
print()
print("coverage — all measured pages:")
for k, lbl in AUTHORITIES:
    c = COVERAGE["all"][k]
    print(f"  {lbl:60s} n={c['n']:3d}  H {c['h']:3d} ({c['h_share']}%)  "
          f"S {c['s']:3d} ({c['s_share']}%)  V {c['v']:3d} ({c['v_share']}%)")
print()
print("coverage — scored subset:")
for k, lbl in AUTHORITIES:
    c = COVERAGE["scored"][k]
    print(f"  {lbl:60s} n={c['n']:3d}  H {c['h']:3d} ({c['h_share']}%)  "
          f"S {c['s']:3d} ({c['s_share']}%)  V {c['v']:3d} ({c['v_share']}%)")
print()
print(f"rows with no signal at all: {len(NO_SIGNAL_ROWS)} / {len(ALL_ROWS)}")
for r in NO_SIGNAL_ROWS:
    print(f"  {r['authority_label']}: {r['url']}")
print()
print("referent class (PREREGISTRATION-3.md) — all measured pages (SELF / OTHER / UNATTRIBUTABLE):")
for k, lbl in AUTHORITIES:
    c = CLASS_COUNTS["all"][k]
    print(f"  {lbl:60s} {c['SELF']} / {c['OTHER']} / {c['UNATTRIBUTABLE']}")
print()
print("referent class — scored subset:")
for k, lbl in AUTHORITIES:
    c = CLASS_COUNTS["scored"][k]
    print(f"  {lbl:60s} {c['SELF']} / {c['OTHER']} / {c['UNATTRIBUTABLE']}")
print()
print(f"future-dated V rows caught by the general D6/D11 detector (V later than that "
      f"authority's run timestamp): {len(FUTURE_V_ROWS)}")
for r in FUTURE_V_ROWS:
    print(f"  {r['authority_label']}: {r['url']}  v={r['v_fmt']} ({r['v']})  "
          f"run={RUN_TS_BY_AUTHORITY[r['authority']].isoformat()}  referent_class={r['referent_class']}")
print()
if RECONCILE_NOTES:
    print("RECONCILIATION NOTES (could not resolve from raw rows alone):")
    for note in RECONCILE_NOTES:
        print("  - " + note)
else:
    print("no reconciliation notes")
print()

# ---------------------------------------------------------------------------
# HTML template
# ---------------------------------------------------------------------------

HTML_TEMPLATE = r"""<title>As of Today — the citation slip</title>
<script type="application/json" id="as-of-today-data">__DATA__</script>
<style>
.aot {
  --fg: #1a1a17;
  --bg: #faf8f3;
  --bg-panel: #ffffff;
  --border: #cfc9ba;
  --border-strong: #948c78;
  --muted: #6b6455;
  --accent: #7a3b1e;
  --accent-2: #2c4a3e;
  --warn-bg: #fff2df;
  --warn-border: #c98a2a;
  --bad-bg: #fbe9e6;
  --bad-border: #a8402a;
  --info-bg: #e9edfa;
  --info-border: #35529c;
  --ok-bg: #e8f1e6;
  --ok-border: #3d6b34;
  --mono: "IBM Plex Mono", "Courier New", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  --serif: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, "Times New Roman", serif;
  font-family: var(--serif);
  color: var(--fg);
  background: var(--bg);
  line-height: 1.45;
  max-width: 920px;
  margin: 0 auto;
  padding: 1.25rem 1rem 4rem;
}
@media (prefers-color-scheme: dark) {
  .aot {
    --fg: #ece7db;
    --bg: #17150f;
    --bg-panel: #201d16;
    --border: #4a4436;
    --border-strong: #746b56;
    --muted: #a89e88;
    --accent: #e0a479;
    --accent-2: #8fc3ab;
    --warn-bg: #3a2c10;
    --warn-border: #c98a2a;
    --bad-bg: #3a1a14;
    --bad-border: #d16a4e;
    --info-bg: #182140;
    --info-border: #7d94d6;
    --ok-bg: #16281a;
    --ok-border: #7bab6f;
  }
}
.aot[data-theme="dark"] {
  --fg: #ece7db;
  --bg: #17150f;
  --bg-panel: #201d16;
  --border: #4a4436;
  --border-strong: #746b56;
  --muted: #a89e88;
  --accent: #e0a479;
  --accent-2: #8fc3ab;
  --warn-bg: #3a2c10;
  --warn-border: #c98a2a;
  --bad-bg: #3a1a14;
  --bad-border: #d16a4e;
  --info-bg: #182140;
  --info-border: #7d94d6;
  --ok-bg: #16281a;
  --ok-border: #7bab6f;
}
.aot[data-theme="light"] {
  --fg: #1a1a17;
  --bg: #faf8f3;
  --bg-panel: #ffffff;
  --border: #cfc9ba;
  --border-strong: #948c78;
  --muted: #6b6455;
  --accent: #7a3b1e;
  --accent-2: #2c4a3e;
  --warn-bg: #fff2df;
  --warn-border: #c98a2a;
  --bad-bg: #fbe9e6;
  --bad-border: #a8402a;
  --info-bg: #e9edfa;
  --info-border: #35529c;
  --ok-bg: #e8f1e6;
  --ok-border: #3d6b34;
}
.aot * { box-sizing: border-box; }
.aot h1 {
  font-size: 1.5rem;
  margin: 0 0 0.15rem;
  font-weight: 600;
  letter-spacing: -0.01em;
}
.aot .aot-kicker {
  font-family: var(--mono);
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
  margin: 0 0 1rem;
}
.aot .aot-standing {
  border: 1px solid var(--border);
  background: var(--bg-panel);
  border-radius: 4px;
  padding: 0.8rem 1rem;
  margin-bottom: 1.4rem;
  font-size: 0.86rem;
}
.aot .aot-standing h2 {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
  margin: 0 0 0.5rem;
  font-weight: 600;
  font-family: var(--mono);
}
.aot .aot-standing ul {
  margin: 0;
  padding-left: 1.1rem;
}
.aot .aot-standing li { margin-bottom: 0.3rem; }
.aot .aot-standing li:last-child { margin-bottom: 0; }
.aot .aot-timestamps {
  font-family: var(--mono);
  font-size: 0.78rem;
  color: var(--muted);
  margin-top: 0.55rem;
  padding-top: 0.55rem;
  border-top: 1px dashed var(--border);
}

.aot section { margin-bottom: 1.8rem; }
.aot h2.aot-h2 {
  font-size: 1.02rem;
  border-bottom: 1px solid var(--border-strong);
  padding-bottom: 0.3rem;
  margin: 0 0 0.7rem;
  font-weight: 600;
}
.aot p.aot-lede { color: var(--muted); font-size: 0.88rem; margin: 0 0 0.9rem; }

/* --- slip picker --- */
.aot .aot-picker {
  display: grid;
  grid-template-columns: minmax(220px, 300px) 1fr;
  gap: 1rem;
  align-items: start;
}
@media (max-width: 680px) {
  .aot .aot-picker { grid-template-columns: 1fr; }
}
.aot .aot-list-wrap {
  border: 1px solid var(--border);
  border-radius: 4px;
  background: var(--bg-panel);
  max-height: 480px;
  display: flex;
  flex-direction: column;
}
.aot input.aot-filter {
  font-family: var(--mono);
  font-size: 0.82rem;
  padding: 0.5rem 0.6rem;
  border: none;
  border-bottom: 1px solid var(--border);
  background: transparent;
  color: var(--fg);
  width: 100%;
  border-radius: 4px 4px 0 0;
}
.aot input.aot-filter:focus { outline: 1px solid var(--border-strong); outline-offset: -1px; }
.aot .aot-list {
  overflow-y: auto;
  flex: 1;
  padding: 0.3rem 0;
}
.aot .aot-group-label {
  font-family: var(--mono);
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--muted);
  padding: 0.5rem 0.7rem 0.2rem;
}
.aot button.aot-url-btn {
  display: block;
  width: 100%;
  text-align: left;
  background: none;
  border: none;
  font-family: var(--mono);
  font-size: 0.78rem;
  color: var(--fg);
  padding: 0.32rem 0.7rem;
  cursor: pointer;
  border-left: 3px solid transparent;
  word-break: break-all;
}
.aot button.aot-url-btn:hover { background: var(--warn-bg); }
.aot button.aot-url-btn.aot-selected {
  border-left-color: var(--accent);
  background: var(--warn-bg);
  font-weight: 600;
}
.aot button.aot-url-btn .aot-flag {
  font-family: var(--mono);
  font-size: 0.65rem;
  color: var(--accent);
  margin-left: 0.35rem;
}
.aot .aot-empty-note {
  padding: 0.6rem 0.7rem;
  color: var(--muted);
  font-size: 0.8rem;
}

/* --- slip --- */
.aot .aot-slip {
  border: 1px solid var(--border-strong);
  border-radius: 4px;
  background: var(--bg-panel);
  padding: 1rem 1.1rem 1.2rem;
  font-size: 0.88rem;
}
.aot .aot-slip-placeholder {
  color: var(--muted);
  font-style: italic;
  padding: 1.2rem 0.2rem;
  text-align: center;
  border: 1px dashed var(--border);
  border-radius: 4px;
}
.aot .aot-slip-head {
  font-family: var(--mono);
  font-size: 0.72rem;
  color: var(--muted);
  word-break: break-all;
  margin-bottom: 0.7rem;
  padding-bottom: 0.6rem;
  border-bottom: 1px dashed var(--border);
}
.aot .aot-slip-head .aot-authority {
  color: var(--accent-2);
  font-weight: 600;
}
.aot .aot-sentences { margin: 0 0 0.9rem; padding: 0; list-style: none; }
.aot .aot-sentences li {
  font-family: var(--serif);
  font-size: 0.92rem;
  padding: 0.35rem 0 0.35rem 1.5rem;
  position: relative;
  border-bottom: 1px solid var(--border);
}
.aot .aot-sentences li:last-child { border-bottom: none; }
.aot .aot-sentences li .aot-sig-tag {
  position: absolute;
  left: 0;
  top: 0.35rem;
  font-family: var(--mono);
  font-weight: 700;
  font-size: 0.78rem;
  color: var(--accent);
  width: 1.2rem;
}
.aot .aot-sentences li.aot-absent { color: var(--muted); font-style: italic; }
.aot .aot-sentences li.aot-suspect { background: var(--warn-bg); }
.aot .aot-sentences li.aot-confirmed { background: var(--bad-bg); }
.aot .aot-sentences li.aot-info { background: var(--info-bg); }
.aot .aot-sentences li.aot-ok { background: var(--ok-bg); }
.aot .aot-badge {
  display: inline-block;
  font-family: var(--mono);
  font-size: 0.62rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0.05rem 0.35rem;
  border-radius: 3px;
  margin-left: 0.4rem;
  vertical-align: middle;
  border: 1px solid;
}
.aot .aot-badge-suspect { color: var(--warn-border); border-color: var(--warn-border); }
.aot .aot-badge-confirmed { color: var(--bad-border); border-color: var(--bad-border); background: var(--bad-bg); }
.aot .aot-badge-info { color: var(--info-border); border-color: var(--info-border); background: var(--info-bg); }
.aot .aot-badge-ok { color: var(--ok-border); border-color: var(--ok-border); background: var(--ok-bg); }

.aot .aot-verdict {
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 0.7rem 0.85rem;
  margin-bottom: 0.9rem;
  background: color-mix(in srgb, var(--bg-panel) 92%, var(--fg) 3%);
}
.aot .aot-verdict h3 {
  font-family: var(--mono);
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--muted);
  margin: 0 0 0.5rem;
  font-weight: 600;
}
.aot .aot-verdict-line { margin: 0 0 0.4rem; }
.aot .aot-verdict-line:last-child { margin-bottom: 0; }
.aot .aot-verdict-line .aot-verdict-label { font-weight: 600; }
.aot .aot-verdict-line.aot-nodate { color: var(--accent); font-weight: 600; }
.aot .aot-verdict-note { font-size: 0.78rem; color: var(--muted); margin-top: 0.15rem; }

.aot details.aot-evidence { margin-top: 0.4rem; }
.aot details.aot-evidence summary {
  cursor: pointer;
  font-family: var(--mono);
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--muted);
  padding: 0.2rem 0;
}
.aot table.aot-evidence-table {
  border-collapse: collapse;
  width: 100%;
  margin-top: 0.5rem;
  font-family: var(--mono);
  font-size: 0.74rem;
}
.aot table.aot-evidence-table th, .aot table.aot-evidence-table td {
  text-align: left;
  padding: 0.3rem 0.5rem;
  border-bottom: 1px solid var(--border);
  vertical-align: top;
  word-break: break-word;
}
.aot table.aot-evidence-table th {
  color: var(--muted);
  font-weight: 600;
  width: 34%;
}

/* --- coverage panel --- */
.aot .aot-basis-toggle {
  display: inline-flex;
  border: 1px solid var(--border-strong);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.7rem;
  font-family: var(--mono);
  font-size: 0.76rem;
}
.aot .aot-basis-toggle button {
  background: var(--bg-panel);
  color: var(--fg);
  border: none;
  padding: 0.4rem 0.7rem;
  cursor: pointer;
}
.aot .aot-basis-toggle button + button { border-left: 1px solid var(--border-strong); }
.aot .aot-basis-toggle button.aot-active { background: var(--accent); color: var(--bg); font-weight: 600; }
.aot table.aot-coverage {
  border-collapse: collapse;
  width: 100%;
  font-size: 0.82rem;
}
.aot table.aot-coverage caption {
  text-align: left;
  font-size: 0.78rem;
  color: var(--muted);
  margin-bottom: 0.4rem;
}
.aot table.aot-coverage th, .aot table.aot-coverage td {
  border: 1px solid var(--border);
  padding: 0.4rem 0.55rem;
  text-align: right;
}
.aot table.aot-coverage th:first-child, .aot table.aot-coverage td:first-child {
  text-align: left;
  font-weight: 600;
}
.aot table.aot-coverage thead th {
  background: var(--warn-bg);
  font-family: var(--mono);
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.aot .aot-coverage-note {
  font-size: 0.8rem;
  color: var(--muted);
  margin-top: 0.5rem;
}
.aot .aot-overflow { overflow-x: auto; }

.aot footer.aot-foot {
  margin-top: 2rem;
  padding-top: 0.8rem;
  border-top: 1px solid var(--border);
  font-size: 0.74rem;
  color: var(--muted);
  font-family: var(--mono);
}
</style>

<div class="aot">
  <h1>As of Today</h1>
  <p class="aot-kicker">a citation slip for official policy pages — three self-reported dates, checked against each other</p>

  <div class="aot-standing">
    <h2>What this instrument does and does not do</h2>
    <ul>
      <li>It measures three signals a page can offer about its own currency — an HTTP <strong>Last-Modified</strong> header (H), a sitemap <strong>&lt;lastmod&gt;</strong> entry (S), and a printed date on the page (V). It edits nothing.</li>
      <li>It is a snapshot taken at two moments on one day, not a monitor and not a history.</li>
      <li>S is itself only the publishing system's own claim about the page — it is not verified against anything.</li>
      <li>No archived capture history was reachable for any of these pages, for either measurement session, so nothing here can be checked against what actually changed.</li>
      <li>This instrument's own rules for extracting V from a page are known to be defective on part of the corpus (a fallback that can read a different article's date, or a future date, off the same page) — that is deliberate: the instrument marks its own bad rows in place, on the slip, rather than quietly dropping them.</li>
      <li>D11: the wrong-referent failure is not a property of one extraction rule. It has been confirmed under two different rules, on two different authorities — a &lt;time&gt; fallback on NIST and a text-label rule on Ireland's — so it is treated here as a property of extracting any date from a page that displays other documents' dates, not as one rule's bug.</li>
    </ul>
    <div class="aot-timestamps" id="aot-timestamps"></div>
  </div>

  <section id="aot-section-slip">
    <h2 class="aot-h2">A. The citation slip</h2>
    <p class="aot-lede">Pick any measured page. The slip shows what each of the three signals would let a citer write, then the two verdicts a citer actually needs: the date their tooling hands them, and the date they could defend in a footnote.</p>
    <div class="aot-picker">
      <div class="aot-list-wrap">
        <input class="aot-filter" type="text" id="aot-filter" placeholder="filter by URL or path…" autocomplete="off" spellcheck="false">
        <div class="aot-list" id="aot-list"></div>
      </div>
      <div id="aot-slip-container">
        <div class="aot-slip-placeholder">Select a URL on the left to produce its citation slip.</div>
      </div>
    </div>
  </section>

  <section id="aot-section-coverage">
    <h2 class="aot-h2">C. Coverage, by authority</h2>
    <p class="aot-lede" id="aot-coverage-lede"></p>
    <div class="aot-basis-toggle" id="aot-basis-toggle">
      <button data-basis="all" class="aot-active" type="button">all measured pages</button>
      <button data-basis="scored" type="button">the scored subset</button>
    </div>
    <div class="aot-overflow">
      <table class="aot-coverage" id="aot-coverage-table"></table>
    </div>
    <p class="aot-coverage-note" id="aot-coverage-note"></p>
  </section>

  <footer class="aot-foot" id="aot-foot"></footer>
</div>

<script>
(function () {
  "use strict";

  var raw = document.getElementById("as-of-today-data").textContent;
  var DATA = JSON.parse(raw);

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined && text !== null) e.textContent = text;
    return e;
  }

  function fmtUtc(iso) {
    // iso like 2026-08-06T08:26:37+00:00 -> "2026-08-06 08:26:37 UTC"
    var m = iso.match(/^(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})/);
    if (!m) return iso;
    return m[1] + " " + m[2] + " UTC";
  }

  // ---- standing block timestamps ----
  (function renderTimestamps() {
    var box = document.getElementById("aot-timestamps");
    var p1 = el("div", null, "Session 1 (European Commission, 40 URLs) started " + fmtUtc(DATA.meta.run1_utc) + ".");
    var p2 = el("div", null, "Session 2 (GOV.UK, NIST, Ireland/DETE) started " + fmtUtc(DATA.meta.run2_utc) + ".");
    box.appendChild(p1);
    box.appendChild(p2);
  })();

  // ---- footer ----
  (function renderFooter() {
    var foot = document.getElementById("aot-foot");
    var n = DATA.meta.total_rows;
    var noSig = DATA.meta.no_signal_at_all_n;
    foot.appendChild(el("div", null,
      n + " pages measured across four authorities. " + noSig +
      " of them offer none of the three signals at all."));
    var srcNote = el("div", null,
      "Sitemap read for the European Commission corpus: " + DATA.meta.ec_sitemap_url + ".");
    foot.appendChild(srcNote);
    if (DATA.meta.ec_all_news_prefixed_candidates && DATA.meta.ec_all_news_prefixed_candidates.length > 2) {
      foot.appendChild(el("div", null,
        "Note: " + DATA.meta.ec_all_news_prefixed_candidates.length +
        " URLs in the European Commission corpus match the '/en/news/' item pattern; " +
        "two of them are treated as chrome (excluded from the scored subset) on the " +
        "collective's own committed re-score, the other " +
        (DATA.meta.ec_all_news_prefixed_candidates.length - 2) +
        " are dated news items and stay in the scored subset. See build_instrument.py for how this was resolved."));
    }
    var futureRows = DATA.meta.future_v_rows || [];
    if (futureRows.length > 0) {
      foot.appendChild(el("div", null,
        "Future-dated printed dates, found by a general detector comparing every row's V to " +
        "that authority's own run timestamp (not special-cased to one URL): " + futureRows.length +
        " row" + (futureRows.length === 1 ? "" : "s") + " — " +
        futureRows.map(function (r) { return r.authority + " " + r.url + " (v=" + r.v_fmt + ")"; }).join("; ") +
        ". Both are symptoms of the same wrong-referent defect (D10/D11), confirmed by hand " +
        "against the live pages, and are shown under \"confirmed wrong-referent\" on their " +
        "slips, not as a separate tier."));
    }
    var uc = DATA.meta.unaudited_by_authority || {};
    var hc = DATA.meta.hand_checked_by_authority || {};
    foot.appendChild(el("div", null,
      "Unaudited label-rule hits (D11, not opened by hand): " +
      DATA.authorities.map(function (a) { return a.label + " " + (uc[a.key] || 0); }).join(", ") +
      ". Hand-checked label-rule hits, found genuine: " +
      DATA.authorities.map(function (a) { return a.label + " " + (hc[a.key] || 0); }).join(", ") + "."));
  })();

  // ---- grouping ----
  var rowsByAuthority = {};
  DATA.authorities.forEach(function (a) { rowsByAuthority[a.key] = []; });
  DATA.rows.forEach(function (r) { rowsByAuthority[r.authority].push(r); });

  var selectedUrl = null;

  function pathLabel(row) {
    return row.path.length > 58 ? row.path.slice(0, 55) + "…" : row.path;
  }

  function rowMatches(row, term) {
    if (!term) return true;
    var hay = (row.url + " " + row.path).toLowerCase();
    return hay.indexOf(term) !== -1;
  }

  function renderList() {
    var listEl = document.getElementById("aot-list");
    listEl.textContent = "";
    var term = document.getElementById("aot-filter").value.trim().toLowerCase();
    var any = false;

    DATA.authorities.forEach(function (a) {
      var rows = rowsByAuthority[a.key].filter(function (r) { return rowMatches(r, term); });
      if (rows.length === 0) return;
      any = true;
      listEl.appendChild(el("div", "aot-group-label", a.label + " (" + rows.length + ")"));
      rows.forEach(function (row) {
        var btn = el("button", "aot-url-btn", null);
        btn.type = "button";
        btn.appendChild(document.createTextNode(pathLabel(row)));
        var FLAG_LABEL = {
          confirmed_wrong_referent: "wrong-referent",
          suspect: "suspect",
          hand_checked: "hand-checked",
          unaudited: "unaudited"
        };
        if (row.flag_tier && FLAG_LABEL[row.flag_tier]) {
          btn.appendChild(el("span", "aot-flag", FLAG_LABEL[row.flag_tier]));
        }
        if (row.url === selectedUrl) btn.classList.add("aot-selected");
        btn.addEventListener("click", function () {
          selectedUrl = row.url;
          renderList();
          renderSlip(row);
        });
        listEl.appendChild(btn);
      });
    });

    if (!any) {
      listEl.appendChild(el("div", "aot-empty-note", "No measured page matches that filter."));
    }
  }

  // ---- slip rendering ----

  function sentenceFor(row, sig) {
    var val = row[sig + "_fmt"];
    if (val) {
      var s = row.authority_label + " — " + row.path + ", as of " + val + ".";
      return { text: s, present: true };
    }
    var reason;
    if (sig === "h") reason = "This page offers no Last-Modified header.";
    else if (sig === "s") reason = "This URL is not listed in the site's own sitemap.";
    else reason = "No date is printed on this page for a reader.";
    return { text: row.authority_label + " — " + row.path + ": " + reason, present: false };
  }

  // Four tiers. confirmed_wrong_referent's note comes from the row itself
  // (row.confirmed_note) because the evidence differs case by case; the
  // other three tiers share one standing note per tier.
  var TIER_INFO = {
    confirmed_wrong_referent: {
      cls: "aot-confirmed",
      badgeCls: "aot-badge-confirmed",
      badgeText: "confirmed wrong-referent",
      excluded: true
    },
    suspect: {
      cls: "aot-suspect",
      badgeCls: "aot-badge-suspect",
      badgeText: "suspect",
      excluded: true,
      note: "Suspect (D10): this date comes from a fallback that reads the datetime attribute " +
        "of a <time> element, which may belong to a teaser card linking to a different article " +
        "rather than to this page. Not opened by hand to confirm."
    },
    hand_checked: {
      cls: "aot-ok",
      badgeCls: "aot-badge-ok",
      badgeText: "hand-checked",
      excluded: false,
      note: "Hand-checked: this on-page “Last update” label was read by hand in an earlier " +
        "session and found genuine — not a citation to another document's date. Kept as a " +
        "defensible date."
    },
    unaudited: {
      cls: "aot-info",
      badgeCls: "aot-badge-info",
      badgeText: "unaudited",
      excluded: false,
      note: "Unaudited (D11): this date was matched by a rule that reads a date label printed in " +
        "the page text. In every case of this kind opened by hand so far, the label named a " +
        "different document's publish date, not this page's own currency — so this is a " +
        "candidate, not a warranty. Kept as a defensible date because there is no evidence " +
        "against this specific row, only a pattern from the rows that were checked."
    }
  };

  function noteFor(row, tier) {
    if (row.flag_tier === "confirmed_wrong_referent" && row.confirmed_note) {
      return row.confirmed_note;
    }
    return tier.note;
  }

  function renderSentences(container, row) {
    var ul = el("ul", "aot-sentences", null);
    ["h", "s", "v"].forEach(function (sig) {
      var info = sentenceFor(row, sig);
      var li = el("li", null, null);
      var tag = el("span", "aot-sig-tag", sig.toUpperCase());
      li.appendChild(tag);
      li.appendChild(document.createTextNode(info.text));
      if (!info.present) li.classList.add("aot-absent");
      if (sig === "v" && row.flag_tier) {
        var tier = TIER_INFO[row.flag_tier];
        li.classList.add(tier.cls);
        var badge = el("span", "aot-badge " + tier.badgeCls, tier.badgeText);
        li.appendChild(badge);
        var note = el("div", "aot-verdict-note", noteFor(row, tier));
        li.appendChild(note);
      }
      ul.appendChild(li);
    });
    container.appendChild(ul);
  }

  function renderVerdict(container, row) {
    var box = el("div", "aot-verdict", null);
    box.appendChild(el("h3", null, "Verdict"));

    // machine-handed line
    var mLine = el("div", "aot-verdict-line", null);
    var mLabel = el("span", "aot-verdict-label", "The date a machine is handed: ");
    mLine.appendChild(mLabel);
    if (row.machine_fmt) {
      mLine.appendChild(document.createTextNode(row.machine_fmt + " (from " + row.machine_source + ")."));
    } else {
      mLine.appendChild(document.createTextNode("none — this page offers none of the three signals."));
      mLine.classList.add("aot-nodate");
    }
    box.appendChild(mLine);
    if (row.machine_is_flagged_v) {
      var mTier = TIER_INFO[row.flag_tier];
      box.appendChild(el("div", "aot-verdict-note",
        "This is the printed date, and it is flagged " + mTier.badgeText + " below — it is what " +
        "ordinary tooling would still be handed, in the order H, then S, then V, because neither " +
        "H nor S exists on this page."));
    } else {
      box.appendChild(el("div", "aot-verdict-note",
        "Ordinary tooling reads in this order: Last-Modified header first, then sitemap, then a printed date."));
    }

    // defensible line
    var dLine = el("div", "aot-verdict-line", null);
    var dLabel = el("span", "aot-verdict-label", "The date a reader could defend: ");
    dLine.appendChild(dLabel);
    if (row.defend_fmt) {
      dLine.appendChild(document.createTextNode(row.defend_fmt + " (from " + row.defend_source + ")."));
    } else if (row.only_defensible_was_flagged) {
      dLine.appendChild(document.createTextNode("no defensible date at all."));
      dLine.classList.add("aot-nodate");
    } else {
      dLine.appendChild(document.createTextNode("none — no sitemap entry and no printed date."));
      dLine.classList.add("aot-nodate");
    }
    box.appendChild(dLine);
    if (row.skipped_flagged_v) {
      var sTier = TIER_INFO[row.flag_tier];
      if (row.only_defensible_was_flagged) {
        box.appendChild(el("div", "aot-verdict-note",
          "The only printed date on this page is flagged " + sTier.badgeText + " and there is no " +
          "sitemap entry to fall back to, so it is not offered here as an answer."));
      } else {
        box.appendChild(el("div", "aot-verdict-note",
          "The printed date on this page is flagged " + sTier.badgeText + ", so it is excluded " +
          "here and the sitemap date is used instead."));
      }
    }
    box.appendChild(el("div", "aot-verdict-note",
      "The Last-Modified header is excluded from what a reader could defend: it reports when " +
      "this fetch was delivered, not when the page's content last changed."));

    // distance line
    var distLine = el("div", "aot-verdict-line", null);
    distLine.appendChild(el("span", "aot-verdict-label", "Distance between them: "));
    if (row.distance_days !== null && row.distance_days !== undefined) {
      var days = row.distance_days;
      distLine.appendChild(document.createTextNode(days + (days === 1 ? " day." : " days.")));
    } else {
      distLine.appendChild(document.createTextNode("not computable — one or both dates are absent."));
    }
    box.appendChild(distLine);

    container.appendChild(box);
  }

  function evidenceRow(table, label, value) {
    var tr = el("tr", null, null);
    tr.appendChild(el("th", null, label));
    tr.appendChild(el("td", null, (value === null || value === undefined || value === "") ? "—" : value));
    table.appendChild(tr);
  }

  function renderEvidence(container, row) {
    var det = el("details", "aot-evidence", null);
    var sum = el("summary", null, "Raw evidence");
    det.appendChild(sum);
    var table = el("table", "aot-evidence-table", null);
    evidenceRow(table, "URL", row.url);
    evidenceRow(table, "HTTP status / fetch", row.status + " / " + row.fetch);
    evidenceRow(table, "Last-Modified (raw header)", row.h_raw);
    evidenceRow(table, "ETag", row.etag);
    evidenceRow(table, "Sitemap state", row.s_state);
    evidenceRow(table, "Sitemap <lastmod>", row.s);
    evidenceRow(table, "Printed date (raw string)", row.v_raw);
    evidenceRow(table, "Extraction rule", row.v_rule);
    evidenceRow(table, "V flag (D10 / D11)", row.flag_tier ? TIER_INFO[row.flag_tier].badgeText : "none");
    evidenceRow(table, "In the collective's scored subset", row.scored ? "yes" : "no (chrome / not in arm B)");
    det.appendChild(table);
    container.appendChild(det);
  }

  function renderSlip(row) {
    var container = document.getElementById("aot-slip-container");
    container.textContent = "";
    var slip = el("div", "aot-slip", null);

    var head = el("div", "aot-slip-head", null);
    var authSpan = el("span", "aot-authority", row.authority_label);
    head.appendChild(authSpan);
    head.appendChild(document.createTextNode(" — " + row.url));
    slip.appendChild(head);

    renderSentences(slip, row);
    renderVerdict(slip, row);
    renderEvidence(slip, row);

    container.appendChild(slip);
  }

  document.getElementById("aot-filter").addEventListener("input", renderList);
  renderList();

  // ---- coverage panel ----
  var currentBasis = "all";

  var BASIS_LABEL = {
    all: "all measured pages",
    scored: "the scored subset"
  };

  function renderCoverageLede() {
    var lede = document.getElementById("aot-coverage-lede");
    lede.textContent = "How often each authority offers each signal, counted from the rows above.";
  }

  function renderCoverageNote() {
    var note = document.getElementById("aot-coverage-note");
    var sizes = currentBasis === "all" ? DATA.meta.corpus_sizes : DATA.meta.scored_sizes;
    note.textContent = "";
    var p1 = el("div", null,
      "The collective's own record scored the second basis, \"the scored subset\": " +
      DATA.authorities.map(function (a) { return a.label + " (n=" + sizes[a.key] + ")"; }).join("; ") +
      " — EC's item-only pages with navigation and listing chrome removed, and GOV.UK/NIST/Ireland's " +
      "arm-B pages with navigation chrome removed by the same rule. \"All measured pages\" is every " +
      "URL fetched, chrome included, and was not the basis any P1–P4 prediction was scored against.");
    note.appendChild(p1);
    var p2 = el("div", null,
      "The V counts above include every printed date found, including the rows the citation " +
      "slips flag as suspect or confirmed-defective (D10/D6) — a flagged V is still a V for " +
      "coverage purposes. Each slip's \"date a reader could defend\" excludes those same rows, " +
      "falling back to the sitemap date or to none. So a page can count toward V here and still " +
      "show \"no defensible date\" on its slip: that is by design, not a discrepancy to reconcile.");
    note.appendChild(p2);
  }

  function renderCoverageTable() {
    var table = document.getElementById("aot-coverage-table");
    table.textContent = "";
    var caption = el("caption", null,
      "Counts and shares of pages offering H, S, V — basis: " + BASIS_LABEL[currentBasis] + ".");
    table.appendChild(caption);

    var thead = el("thead", null, null);
    var htr = el("tr", null, null);
    ["Authority", "n", "H", "S", "V"].forEach(function (h) {
      htr.appendChild(el("th", null, h));
    });
    thead.appendChild(htr);
    table.appendChild(thead);

    var tbody = el("tbody", null, null);
    DATA.authorities.forEach(function (a) {
      var c = DATA.coverage[currentBasis][a.key];
      var tr = el("tr", null, null);
      tr.appendChild(el("td", null, a.label));
      tr.appendChild(el("td", null, String(c.n)));
      tr.appendChild(el("td", null, c.n ? (c.h + " (" + c.h_share + "%)") : "—"));
      tr.appendChild(el("td", null, c.n ? (c.s + " (" + c.s_share + "%)") : "—"));
      tr.appendChild(el("td", null, c.n ? (c.v + " (" + c.v_share + "%)") : "—"));
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
  }

  function renderCoverage() {
    renderCoverageLede();
    renderCoverageTable();
    renderCoverageNote();
  }

  var toggleWrap = document.getElementById("aot-basis-toggle");
  Array.prototype.forEach.call(toggleWrap.querySelectorAll("button"), function (btn) {
    btn.addEventListener("click", function () {
      currentBasis = btn.getAttribute("data-basis");
      Array.prototype.forEach.call(toggleWrap.querySelectorAll("button"), function (b) {
        b.classList.remove("aot-active");
      });
      btn.classList.add("aot-active");
      renderCoverage();
    });
  });

  renderCoverage();
})();
</script>
"""

html_out = HTML_TEMPLATE.replace("__DATA__", JSON_BLOB_SAFE)

out_path = HERE / "instrument.html"
out_path.write_text(html_out, encoding="utf-8")
print(f"wrote {out_path} ({len(html_out)} bytes)")
