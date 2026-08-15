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
import calendar
import json
import os
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import presence_check as pc  # noqa: E402

PASS, FAIL = [], []


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

# --------------------------------------------------------------------------------- report
print(f"selftest_presence_check — presence_check {pc.VERSION}")
print(f"  {len(PASS)} assertion(s) passed")
if FAIL:
    print(f"  {len(FAIL)} FAILED:")
    for f in FAIL:
        print("    - " + f)
    sys.exit(1)
print("  0 failed")
sys.exit(0)
