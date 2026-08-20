#!/usr/bin/env python3
"""selftest_presence_check — run this before you trust the tool, and it needs no network.

Session 121, 2026-08-15. Ships beside `presence_check.py` v0.2 so that a stranger can check the
four repairs v0.2 claims, rather than take this practice's word for them. Every assertion below
either reproduces a defect that v0.1 actually had (and shows it is gone) or pins a piece of
arithmetic the tool's headline depends on.

    python3 selftest_presence_check.py

The probe is stubbed: no request leaves the machine, and `time.sleep` is replaced, so the whole
suite runs in well under a second. That is deliberate — a test that needs the network cannot be
run by someone deciding whether to run the tool at all.

Exit 0 = every assertion held. Exit 1 = at least one did not, and the failure is printed.
"""
import sys

# Before importing the tool: erratum E23. See the note at the top of presence_check.py — running
# this suite inside the directory that ships it must not add files to that directory.
sys.dont_write_bytecode = True

import calendar
import json
import os
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import presence_check as pc  # noqa: E402

PASS, FAIL, SKIPPED = [], [], []


def check(name, got, want):
    if got == want:
        PASS.append(name)
    else:
        FAIL.append(f"{name}\n      got:  {got!r}\n      want: {want!r}")


def check_true(name, cond, detail=""):
    if cond:
        PASS.append(name)
    else:
        FAIL.append(f"{name}  {detail}")


# ---------------------------------------------------------------- 1. parse_line (condition I4)
# The four lines below are the ones the session-120 adversary actually ran through v0.1. Each is
# recorded here with what v0.1 returned, so the test documents the defect and not only the fix.
for line, v01_returned in [
    ("2026-08-15", "2026"),
    ("tiktok 2024 roundup", "2024"),
    ("https://www.youtube.com/watch?v=4", "4"),
    ("https://vm.tiktok.com/ZMabcdef/", None),
]:
    vid, handle, reason = pc.parse_line(line)
    check(f"I4 refuses {line!r} (v0.1 measured {v01_returned!r})", vid, None)
    check_true(f"I4 gives a reason for {line!r}", bool(reason), f"reason={reason!r}")

check("accepts a full URL",
      pc.parse_line("https://www.tiktok.com/@someuser/video/7123456789012345678")[:2],
      ("7123456789012345678", "someuser"))
check("accepts a URL with a query string",
      pc.parse_line("https://www.tiktok.com/@u/video/7123456789012345678?is_from_webapp=1")[0],
      "7123456789012345678")
check("accepts a bare identifier",
      pc.parse_line("7123456789012345678")[:2], ("7123456789012345678", "x"))
check("accepts 'id,handle'",
      pc.parse_line("7123456789012345678,someuser")[:2], ("7123456789012345678", "someuser"))
check("accepts 'id, @handle' with spacing",
      pc.parse_line("7123456789012345678, @someuser")[:2], ("7123456789012345678", "someuser"))
# The legacy short identifier stays measurable. Session 110's control (D12) established that
# `12345` returns a full body; a stricter rule that discarded it would discard real data, and
# the session-120 adversary confirmed it answers HTTP 200 in all four window runs.
check("keeps the legacy short identifier 12345", pc.parse_line("12345")[0], "12345")
check("ignores a comment line", pc.parse_line("# a list of videos")[0], None)
check("ignores a blank line", pc.parse_line("   ")[0], None)
check("a refused blank line carries no reason", pc.parse_line("   ")[2], None)

# ---------------------------------------------------------------------------- 2. dating rule
check("19-digit id dates", pc.dated("7123456789012345678", 2_000_000_000)[1] is not None, True)
check("non-19-digit id is undatable", pc.dated("12345", 2_000_000_000)[1], None)
check_true("non-19-digit id says why", "not-19-digit" in (pc.dated("12345", 2_000_000_000)[2] or ""))
# A creation time at or after the reference time is refused rather than returned as a negative
# age. This is the check the session-120 errata (E3) found the bundle claiming and not doing.
future = ("7123456789012345678", int("7123456789012345678") >> 32)
check("age is refused when creation is not before the reference time",
      pc.dated(future[0], future[1])[1], None)
check("band_of maps 0.5y", pc.band_of(0.5), "0-1y")
check("band_of maps 7y to the open band", pc.band_of(7.0), "5y+")

# ------------------------------------------------------------------ 3. baseline failure (I6)
missing, why = pc.load_baseline("/nonexistent/presence-baseline.json")
check("a missing baseline returns None", missing, None)
check_true("a missing baseline names the path", "/nonexistent/" in (why or ""), why)
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
    json.dump({"schema": "something/else/1"}, fh)
    wrong_schema_path = fh.name
b, why2 = pc.load_baseline(wrong_schema_path)
check("a wrong-schema baseline returns None", b, None)
check_true("a wrong-schema baseline names both schemas",
           "something/else/1" in (why2 or "") and "public-presence-null" in (why2 or ""), why2)
os.unlink(wrong_schema_path)

# ---------------------------------------------------------------- 4. confirmation logic (I3)
class StubProbe:
    """Returns a scripted sequence of HTTP results per identifier, and counts requests."""

    def __init__(self, script):
        self.script = {k: list(v) for k, v in script.items()}
        self.calls = []

    def __call__(self, vid, handle):
        self.calls.append(vid)
        seq = self.script[vid]
        code = seq.pop(0) if len(seq) > 1 else seq[0]
        if code == 200:
            return {"http": 200, "bytes": 500, "author_unique_id": handle, "title_len": 12}
        return {"http": code, "bytes": 60, "body_code": code}


T_REF = 2_000_000_000
LIVE = "7123456789012345678"     # answers 200 always
GONE = "7123456789012345679"     # answers 400 always
FLAKY = "7123456789012345680"    # answers 400 once, then 200 — the artefact this arc has seen


def run(items, confirm, confirm_what, script):
    stub = StubProbe(script)
    rows = pc.measure(items, T_REF, confirm, confirm_what,
                      probe=stub, sleep=lambda _s: None)
    return rows, stub


script = {LIVE: [200], GONE: [400], FLAKY: [400, 200]}
items = [(LIVE, "a"), (GONE, "b"), (FLAKY, "c")]

rows, stub = run(items, 5, "absent", script)
states = {r["vid"]: r["state"] for r in rows}
check("a live reading stays RETRIEVABLE", states[LIVE], "RETRIEVABLE")
check("a refusal that survives 5 passes is NOT-RETRIEVABLE", states[GONE], "NOT-RETRIEVABLE")
check("I3 a refusal that does not reproduce becomes UNCONFIRMED-ABSENT",
      states[FLAKY], "UNCONFIRMED-ABSENT")
check("the first-pass reading is kept beside the verdict",
      [r["first_pass_state"] for r in rows if r["vid"] == FLAKY], ["NOT-RETRIEVABLE"])
check("confirmation requests = 2 absent readings x 5 passes",
      len([c for c in stub.calls]) - 3, 10)
check("a RETRIEVABLE reading is not re-requested by default",
      stub.calls.count(LIVE), 1)

counts, det, rate = pc.tally(rows)
check("UNCONFIRMED-ABSENT is excluded from the denominator", det, 2)
check("the absence rate counts only confirmed absence", rate, 0.5)
check("the unconfirmed reading is still reported", counts.get("UNCONFIRMED-ABSENT"), 1)

rows0, stub0 = run(items, 0, "absent", script)
check("--confirm 0 makes one request per identifier", len(stub0.calls), 3)
check("--confirm 0 reports the single reading as absence",
      {r["vid"]: r["state"] for r in rows0}[FLAKY], "NOT-RETRIEVABLE")
check("--confirm 0 records no confirmation block",
      [r["confirmation"] for r in rows0], [None, None, None])

rows_all, stub_all = run(items, 5, "all", {LIVE: [200], GONE: [400], FLAKY: [400, 200]})
check("--confirm-what all re-requests every determinate reading",
      len(stub_all.calls) - 3, 15)
check("--confirm-what all leaves a stable live reading alone",
      {r["vid"]: r["state"] for r in rows_all}[LIVE], "RETRIEVABLE")

# A first-pass RETRIEVABLE that does not reproduce is INDETERMINATE, never absence: the tool
# must not convert a failure to reproduce presence into evidence of absence.
rows_fp, _ = run([(FLAKY, "c")], 5, "all", {FLAKY: [200, 400]})
check("an unreproduced presence becomes INDETERMINATE, not absence",
      rows_fp[0]["state"], "INDETERMINATE")

# A transport failure is never confirmed away: it is not evidence either way, so it is not a
# target of confirmation and stays INDETERMINATE.
rows_t, stub_t = run([(GONE, "b")], 5, "absent", {GONE: [503]})
check("an unexpected status is INDETERMINATE", rows_t[0]["state"], "INDETERMINATE")
check("an INDETERMINATE reading is not re-requested", len(stub_t.calls), 1)

# ------------------------------- 4b. v0.2.1: noise in the confirmation burst is not disagreement
# The adversary of v0.2 wrote this assertion's absence as its blocking charge: the 65-assertion
# suite tested INDETERMINATE only as a FIRST-pass outcome, which is never a confirmation target,
# so nothing exercised an INDETERMINATE pass DURING a confirmation. v0.2 treated it as
# disagreement and discarded a genuinely absent unit from both numerator and denominator. At this
# arc's own measured transport-failure rate (1.24 %, PREREGISTRATION-112.md §P2) that is 6.05 %
# of absent units.
NOISY = "7123456789012345681"

rows_n, _ = run([(NOISY, "d")], 5, "absent", {NOISY: [400, 400, 503, 400, 400, 400]})
c = rows_n[0]["confirmation"]
check("v0.2.1 one noisy pass does not refute an absence", rows_n[0]["state"], "NOT-RETRIEVABLE")
check("v0.2.1 the noisy pass is counted as noise, not disagreement", c["n_noise"], 1)
check("v0.2.1 no pass reversed the reading", c["n_reversing"], 0)
check("v0.2.1 four passes agreed", c["n_agreeing"], 4)
check("v0.2.1 the confirmation is marked partial", c["partial"], True)
check_true("v0.2.1 the partial confirmation says so in words", "4 of 5" in (c.get("note") or ""),
           c.get("note"))
counts_n, det_n, rate_n = pc.tally(rows_n)
check("v0.2.1 a partially confirmed absence stays in the denominator", det_n, 1)
check("v0.2.1 and in the numerator", rate_n, 1.0)

# A determinate pass that disagrees still refutes, exactly as before — the repair must not have
# turned the confirmation step off.
rows_r, _ = run([(NOISY, "d")], 5, "absent", {NOISY: [400, 503, 200, 400, 400, 400]})
check("v0.2.1 a real reversal still refutes even with noise present",
      rows_r[0]["state"], "UNCONFIRMED-ABSENT")
check("v0.2.1 the reversal is counted", rows_r[0]["confirmation"]["n_reversing"], 1)

# Every pass noise: the confirmation did not run, and the tool says so rather than confirming.
rows_z, _ = run([(NOISY, "d")], 3, "absent", {NOISY: [400, 503]})
check("v0.2.1 an all-noise confirmation reports INDETERMINATE", rows_z[0]["state"],
      "INDETERMINATE")
check_true("v0.2.1 an all-noise confirmation says the confirmation did not run",
           "did not run" in (rows_z[0]["confirmation"].get("note") or ""),
           rows_z[0]["confirmation"].get("note"))

# ------------------------------- 4c. v0.2.1: the URL rule checks the host, not only the path
# v0.2 accepted /video/<digits> on ANY domain and measured it against this platform's endpoint.
for other in ["https://www.youtube.com/video/7123456789012345678",
              "https://example.com/video/7123456789012345678/watch",
              "https://vimeo.com/video/7123456789012345678",
              "https://www.instagram.com/reel/video/9999999999",
              "https://tiktok.com.evil.example/video/7123456789012345678"]:
    vid_o, _h, reason_o = pc.parse_line(other)
    check(f"v0.2.1 refuses another host: {other[:44]}", vid_o, None)
    check_true(f"v0.2.1 names the host it refused: {other[:44]}",
               "not this platform" in (reason_o or ""), reason_o)

check("v0.2.1 accepts the platform's own /v/<id> share path",
      pc.parse_line("https://m.tiktok.com/v/7123456789012345678.html")[0],
      "7123456789012345678")
_v, _h, _r = pc.parse_line("https://vm.tiktok.com/ZMabcdef/")
check("v0.2.1 still refuses an unresolved share link", _v, None)
check_true("v0.2.1 gives the share link the RIGHT reason, not 'another platform'",
           "does not follow redirects" in (_r or "") and "not this platform" not in (_r or ""), _r)

# ------------------------------- 4d. v0.2.1: ordinary spreadsheet separators are accepted
for sep_line, label in [("7123456789012345678\tsomeuser", "tab"),
                        ("7123456789012345678;someuser", "semicolon"),
                        ("7123456789012345678 someuser", "space"),
                        ("7123456789012345678,someuser", "comma")]:
    check(f"v0.2.1 accepts a {label}-separated id and handle",
          pc.parse_line(sep_line)[:2], ("7123456789012345678", "someuser"))

# ------------------------------------------------------------------ 5. vantage modes (I7)
FAKE_VANTAGE = {"ip": "203.0.113.7", "city": "Somewhere", "region": "R", "country": "US",
                "loc": "1.0,2.0", "timezone": "UTC", "asn": "AS396982",
                "source": "https://example.invalid/json", "fetched_utc": "2026-08-15T20:00:00Z"}
asn_mode = pc.read_vantage("asn", probe=lambda: dict(FAKE_VANTAGE))
check("I7 asn mode keeps the autonomous system", asn_mode["asn"], "AS396982")
for personal in ("ip", "city", "region", "loc", "timezone"):
    check(f"I7 asn mode drops {personal}", personal in asn_mode, False)
check_true("I7 asn mode says the lookup still disclosed the IP",
           "IP address" in asn_mode["note"], asn_mode["note"])
full_mode = pc.read_vantage("full", probe=lambda: dict(FAKE_VANTAGE))
check("I7 full mode keeps the IP", full_mode["ip"], "203.0.113.7")
check_true("I7 full mode carries a disclosure", "disclosure" in full_mode)
called = []
none_mode = pc.read_vantage("none", probe=lambda: called.append(1) or dict(FAKE_VANTAGE))
check("I7 none mode makes no call", called, [])
check("I7 none mode records no autonomous system", none_mode["asn"], None)

# ------------------------------------------------------------------------- 6. expectation
BASE = {"schema": "field-research/public-presence-null/1",
        "by_age_band": {"0-1y": {"n": 100, "absent_rate": 0.10, "absent_ci": [0.05, 0.15]},
                        "5y+": {"n": 50, "absent_rate": 0.30, "absent_ci": [0.20, 0.40]}},
        "pooled": {"n": 150},
        "source_run": {"file": "f.json", "run_id": "r", "vantage_asn": "AS1"}}
exp = pc.expectation([{"band": "0-1y"}, {"band": "0-1y"}, {"band": "5y+"}, {"band": None}], BASE)
check("expectation weights by the caller's own histogram",
      round(exp["expected_absent_rate"], 10), round((2 / 3) * 0.10 + (1 / 3) * 0.30, 10))
check("expectation counts only dated rows", exp["n_dated"], 3)
check("expectation carries its reference population", exp["reference_population"]["n"], 150)
check("expectation is None without a baseline", pc.expectation([{"band": "0-1y"}], None), None)
check("expectation is None when nothing is dated", pc.expectation([{"band": None}], BASE), None)

# ------------------------------------------------------------------- 7. baseline currency
DATED = dict(BASE, t_ref_utc="2026-08-14T03:43:47Z")
# a measurement reference exactly one day after the baseline's declared one
one_day_later = calendar.timegm(time.strptime("2026-08-15T03:43:47Z", "%Y-%m-%dT%H:%M:%SZ"))
cur = pc.baseline_currency(DATED, one_day_later)
check("baseline currency computes the gap in days", cur["age_days_at_measurement"], 1.0)
check_true("baseline currency states the declaration is unverified",
           "NOT verified" in cur["status"], cur["status"])
check("baseline currency is None without a baseline", pc.baseline_currency(None, 0), None)
check("a baseline with no reference time is named as such",
      pc.baseline_currency(BASE, 0)["age_days_at_measurement"], None)
check("an unreadable reference time is named as such",
      pc.baseline_currency(dict(BASE, t_ref_utc="whenever"), 0)["age_days_at_measurement"], None)

# ---------------------------------------------- 8. the frozen-reference drift (V1, V2; s122)
# The whole point of these assertions is that the drift is computed on the CALLER'S list, offline,
# with no network and no reference to this arc's own panel. Identifiers are constructed so their
# decoded creation time is exact: the platform's modern scheme is unix-seconds << 32.
def _vid_created_at(stamp):
    """A 19-digit identifier whose dating rule decodes to exactly `stamp`."""
    t = calendar.timegm(time.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ"))
    v = str(t << 32)
    assert len(v) == 19, (stamp, v)
    return v


# A video created 4 years and 11 months before the reference time: in 4-5y at the reference
# time, and in 5y+ once the clock has moved two months on.
V_NEAR_EDGE = _vid_created_at("2021-09-14T03:43:47Z")
DRIFTY = {"schema": "field-research/public-presence-null/1",
          "t_ref_utc": "2026-08-14T03:43:47Z",
          "by_age_band": {"4-5y": {"n": 100, "absent_rate": 0.10, "absent_ci": [0.05, 0.15]},
                          "5y+": {"n": 100, "absent_rate": 0.30, "absent_ci": [0.20, 0.40]}},
          "pooled": {"n": 200},
          "source_run": {"file": "f.json", "run_id": "r", "vantage_asn": "AS1"}}

t_at_ref = calendar.timegm(time.strptime("2026-08-14T03:43:47Z", "%Y-%m-%dT%H:%M:%SZ"))
rows_now = [{"vid": V_NEAR_EDGE, "band": pc.band_of(
    (t_at_ref + 120 * 86400 - (int(V_NEAR_EDGE) >> 32)) / pc.YEAR_S)}]
d = pc.drift(rows_now, DRIFTY, t_at_ref + 120 * 86400)
check("drift reports the gap between the two clocks", d["days_between_the_two_clocks"], 120.0)
check("drift ages the list at the reference time into the band it was in then",
      d["age_histogram_at_the_reference_time"], {"4-5y": 1})
check("drift ages the list at now into the band it has moved to",
      d["age_histogram_at_now"], {"5y+": 1})
check("the reference-time expectation is the table's reference-time cell",
      round(d["expected_with_the_list_aged_at_the_reference_time"], 10), 0.10)
check("the now-aged expectation is the table's later cell",
      round(d["expected_with_the_list_aged_at_now"], 10), 0.30)
check("the drift is reported in percentage points, signed",
      round(d["drift_pp"], 10), 20.0)
check_true("the drift says in as many words that it is not a forecast",
           "not a forecast" in d["the_drift_is_not_a_forecast"]
           or "no part of this figure says retrievability itself changed"
           in d["the_drift_is_not_a_forecast"], d["the_drift_is_not_a_forecast"])
check_true("the drift names the reference-time figure as the defensible one",
           d["which_one_is_defensible"].lower().startswith("the reference-time one"),
           d["which_one_is_defensible"][:60])

# A tool run on the reference day itself must report exactly zero drift — the defect and its
# measurement have to agree that there is nothing to see when the two clocks coincide.
rows_same = [{"vid": V_NEAR_EDGE, "band": pc.band_of(
    (t_at_ref - (int(V_NEAR_EDGE) >> 32)) / pc.YEAR_S)}]
d0 = pc.drift(rows_same, DRIFTY, t_at_ref)
check("drift is exactly zero on the reference day", d0["drift_pp"], 0.0)
check("drift is None without a baseline", pc.drift(rows_same, None, t_at_ref), None)
check("drift is None when the baseline declares no reference time",
      pc.drift(rows_same, BASE, t_at_ref), None)
check("drift is None when the declared reference time is unreadable",
      pc.drift(rows_same, dict(DRIFTY, t_ref_utc="whenever"), t_at_ref), None)
check("an undatable identifier contributes no band at either clock",
      pc.rebanded([{"vid": "12345"}], t_at_ref), [{"band": None}])
# --- v0.3.1: the comparand, asserted against the measurement rather than against a literal ---
# Verifier 122 finding 6 and Interlocutor 14 finding 5 both caught the v0.3.0 version of this
# assertion: it read `pc.STALE_AFTER_DAYS == 26`, which passes identically whether 26 was
# computed or typed, inside a repair whose whole subject is numbers that quietly stop matching
# their source. It now recomputes the comparand from the measurement file. AND — session 119's
# lesson, which the old version also broke — a check that cannot find its subject must SAY SO,
# never pass quietly: if the measurement file is not beside the bundle, that is reported as a
# skipped assertion with a reason, not as a pass.
_HERE = os.path.dirname(os.path.abspath(__file__))
# session 127: beside this script first (the short object ships it), then the
# retired bundle's layout, so this file runs unchanged in either place.
_MEAS = os.path.join(_HERE, "drift-122.json")
if not os.path.exists(_MEAS):
    _MEAS = os.path.join(_HERE, "..", "..", "drift-122.json")
if os.path.exists(_MEAS):
    _m = json.load(open(_MEAS))
    _fam = _m["half_two_caller_side_drift"]["when_the_design_half_overtakes_the_bookkeeping_half"]
    _moved = _m["half_one_bookkeeping"]["bands_that_move"]
    _worst = max(abs(100 * r["delta_rate"]) for r in _moved if r.get("delta_rate") is not None)
    check("the measurement's worst band-rate delta is the 0.1826 pp v0.3.0 warned off",
          round(_worst, 4), 0.1826)
    check("and that comparand yields the 26 days v0.3.0 hard-coded", _fam["days"], 26)
    check_true("the comparand v0.3.1 actually uses is SMALLER than the withdrawn one — the "
               "strictest member of the family, not the most forgiving",
               pc.BOOKKEEPING_COMPARAND_PP < _worst,
               (pc.BOOKKEEPING_COMPARAND_PP, _worst))
    check_true("the withdrawn constant is gone from the module",
               not hasattr(pc, "STALE_AFTER_DAYS"), "STALE_AFTER_DAYS still present")
else:
    SKIPPED.append("drift-122.json not beside the bundle: the comparand could NOT be checked "
                   "against its measurement, and this line is here so that absence is visible")

# --- v0.3.1: the two cases v0.3.0 got wrong, both reproduced from the adversary's report -----
_DR = {"schema": "field-research/public-presence-null/1",
       "t_ref_utc": "2026-08-14T03:43:47Z",
       "by_age_band": {"0-1y": {"n": 100, "absent_rate": 0.05, "absent_ci": [0.02, 0.10]},
                       "4-5y": {"n": 100, "absent_rate": 0.10, "absent_ci": [0.05, 0.15]},
                       "5y+": {"n": 100, "absent_rate": 0.30, "absent_ci": [0.20, 0.40]}},
       "pooled": {"n": 300},
       "source_run": {"file": "f.json", "run_id": "r", "vantage_asn": "AS1"}}
_td = calendar.timegm(time.strptime("2026-08-14T03:43:47Z", "%Y-%m-%dT%H:%M:%SZ"))
_mk = lambda d: str((int(_td - d * 86400) << 32) | 1)     # created d days BEFORE t_ref
_now = _td + 400 * 86400


def _rows(vids, at):
    return [{"vid": v, "band": pc.band_of((at - (int(v) >> 32)) / pc.YEAR_S)} for v in vids]


# Case A — every identifier postdates the table. v0.3.0 returned None here and the printer
# silently fell through to the today-aged figure, unlabelled.
_a = pc.drift(_rows([_mk(-50 - i * 10) for i in range(5)], _now), _DR, _now)
check_true("a list that entirely postdates the table still returns a drift record", _a is not None)
check("...with no reference-time reading, because those videos did not exist then",
      _a["expected_with_the_list_aged_at_the_reference_time"], None)
check("...with the drift refused rather than invented", _a["drift_pp"], None)
check("...and marked not comparable", _a["comparable"], False)
check_true("...and the refusal states its reason",
           "created AFTER" in _a["why_the_drift_is_not_reported"],
           _a["why_the_drift_is_not_reported"])
check("...while the today-aged reading is still computed and counted",
      _a["n_dated_at_now"], 5)

# Case B — a mixed list. v0.3.0 printed the difference between two DIFFERENT denominators as
# drift; on the adversary's five-old/five-new list that was -4.8752 pp of which none was drift.
_b = pc.drift(_rows([_mk(2000 + i * 100) for i in range(5)]
                    + [_mk(-50 - i * 10) for i in range(5)], _now), _DR, _now)
check("a mixed list is datable at the reference time for the old half only",
      _b["n_dated_at_the_reference_time"], 5)
check("...and for the whole list at today", _b["n_dated_at_now"], 10)
check("...so the drift is refused", _b["drift_pp"], None)
check_true("...and the refusal names the two denominators",
           "5 identifier(s) are datable" in _b["why_the_drift_is_not_reported"]
           and "10 at today" in _b["why_the_drift_is_not_reported"],
           _b["why_the_drift_is_not_reported"])

# Case C — a comparable list still reports a drift, with both intervals and both denominators.
_c = pc.drift(_rows([_mk(1700)], _now), _DR, _now)
check("a comparable list is marked comparable", _c["comparable"], True)
check("...its two denominators agree",
      (_c["n_dated_at_the_reference_time"], _c["n_dated_at_now"]), (1, 1))
check_true("...and both readings carry their interval, not just the disowned one",
           None not in (_c["expected_at_the_reference_time_lo"],
                        _c["expected_at_the_reference_time_hi"],
                        _c["expected_at_now_lo"], _c["expected_at_now_hi"]))

# --- v0.3.1: the tool can now tell a table that lies about its own clock -------------------
_ok = pc.baseline_currency(dict(_DR, ages_computed_at_utc="2026-08-14T03:43:47Z"), _td)
check_true("a table whose two clocks agree is reported as AGREE",
           _ok["clock_check"].startswith("AGREE"), _ok["clock_check"])
_bad = pc.baseline_currency(dict(_DR, ages_computed_at_utc="2026-08-11T11:24:06Z"), _td)
check_true("a table with V1's own defect is reported as DISAGREE",
           _bad["clock_check"].startswith("DISAGREE"), _bad["clock_check"])
check("...and the disagreement is measured, at V1's own 2.6803 days",
      round(_bad["declared_minus_computed_days"], 4), 2.6803)
check_true("a table that states only one clock is UNCHECKABLE, never AGREE",
           pc.baseline_currency(_DR, _td)["clock_check"].startswith("UNCHECKABLE"),
           pc.baseline_currency(_DR, _td)["clock_check"])

# --------------------------------------------------------------------------------- report
print(f"selftest_presence_check — presence_check {pc.VERSION}")
print(f"  {len(PASS)} assertion(s) passed")
for sk in SKIPPED:
    print(f"  SKIPPED (said out loud, never counted as a pass): {sk}")
if FAIL:
    print(f"  {len(FAIL)} FAILED:")
    for f in FAIL:
        print("    - " + f)
    sys.exit(1)
print("  0 failed")
sys.exit(0)
