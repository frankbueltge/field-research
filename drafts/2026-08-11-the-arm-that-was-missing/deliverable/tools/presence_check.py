#!/usr/bin/env python3
"""presence_check - measure whether named videos are publicly retrievable, on a named day.

VERSION 0.3.0, session 122, 2026-08-16.

    python3 presence_check.py LISTFILE [-o OUT.json] [--baseline presence-baseline.json]
                              [--confirm N] [--confirm-what absent|all]
                              [--vantage asn|full|none] [--label NAME]

Version 0.1 of this file was part of a bundle that was **withheld** at the gauntlet of
2026-08-15 (`deliverable/GAUNTLET-2026-08-15.md`). Four of the defects that stopped it live in
this file, and this version exists to answer them. The v0.1 text is not deleted and not edited
in place: it is retrievable at commit `9157f731` of this repository, sha256
`ae8fc947e6b7e7a12d646c282e49991cc6433640a0256acefdd0fa1eff6caa1d`, so the two reviewers'
reports stay checkable against the state they were run on.

WHAT 0.3.0 CHANGED, AND IT IS ONE DEFECT AND NOTHING ELSE
---------------------------------------------------------
**The frozen-reference drift — V1 and V2 of the session-120 gauntlet**, carried unrepaired across
two sessions and made binding on session 122 by `CONDITIONS-121.md`. A reviewer's words for it:
the defect that would *"quietly move somebody else's number"*. It has two halves.

*The bookkeeping half* was in the table, not in this file: `reference-baseline.json` declared one
reference time and had its age columns computed against another, **2.6803 days** earlier. Twenty-
four units sit in a different band under the two clocks; **no absent count moves and the pooled
rate is identical to the last digit**, but every published age-band cell does move, and so does
the age gradient's own test (3.69× → 3.64×, p 6.447e-10 → 7.656e-10; the conclusion is unchanged).
Repaired in `build_deliverable.py` and published as dated corrected files beside the originals.

*The design half is in this file.* It ages the caller's identifiers at the moment the caller runs
it and looks them up in a table fixed on a past day, so the printed expectation walks away from
what was measured by exactly the shelf-life of the tool — silently, keeping the same decimals.
0.2.1 disclosed the table's age. Disclosure is not a size. **0.3.0 prints the size, computed on
the caller's own list**: the same list aged at the table's reference time and aged at today, both
figures, the gap between them named as arithmetic drift and not as a change in the world. The
reference-time figure leads, because it is the only one whose ages and table agree.

The staleness threshold is measured rather than picked: **26 days**, the day on which this drift
first exceeds the largest band-rate error the bookkeeping half ever caused. Full measurement:
`drift-122.json`, `DRIFT-122.md`.

**Nothing else in this file changed at 0.3.0**, deliberately: session 121 spent itself on this
tool and was told by its own adversary that the tool had got harder to fool rather than more
correct. This version answers one carried defect and stops.

WHAT 0.2.1 REPAIRED, AFTER ITS OWN GAUNTLET
-------------------------------------------
**VERSION 0.2.1 (same session, after its own gauntlet).** The two reviewers of v0.2 returned a
Verifier FAIL and an Interlocutor verdict of *survives, narrowed*, with four defects in this file.
All four are repaired here and none of the repairs carries a verdict — the reviewers read v0.2,
retrievable at commit `ffebcf56`. What changed: an INDETERMINATE confirmation pass is no longer
treated as disagreement (it discarded roughly one genuinely absent unit in seventeen); the URL
rule now checks the host, because v0.2 accepted `/video/<digits>` on ANY domain; tab-, semicolon-
and space-separated lists are accepted; and the direction of the bias the design creates is
stated in the output. Full account: `CHANGELOG-v0.2.md`, section "What v0.2.1 repaired".

WHAT CHANGED IN 0.2, AND WHICH OBJECTION EACH ANSWERS
-----------------------------------------------------
1. **Readings are confirmed (I3, the objection that stopped the ship).** v0.1 took one pass and
   reported it. Every reading *this practice* trusts survives five immediate re-requests, and
   v0.1 did not do that, while the bundle offered this practice's own reproducibility as the
   reason to trust it. Now: `--confirm N` (default 5) re-requests every reading that carries the
   claim, and a reading that does not survive is reported as UNCONFIRMED, not as absence.
2. **A line that is not an identifier is refused (I4).** v0.1 read `2026-08-15` as the video
   `2026`, `tiktok 2024 roundup` as `2024`, and a different platform's URL as `4`. It now
   requires a `/video/<digits>` or `/v/<digits>` path **on this platform's host** or a field
   that is entirely digits, and prints what it refused and why. (v0.2 checked the path and not
   the host, so another site's `/video/<digits>` was accepted; 0.2.1 checks the host.)
3. **A failed baseline fails where a human sees it (I6).** v0.1 recorded the failure in one JSON
   field and printed a full run as if nothing had happened. It now prints on both streams and
   exits 3.
4. **The third-party geolocation call is disclosed and optional (I7).** v0.1 called a commercial
   IP-geolocation service and wrote the caller's IP, city, region, coordinates and timezone into
   the output file they might share, and nothing in the bundle said so. The default now keeps
   only the autonomous-system number and the country; `--vantage none` makes no call at all; and
   whichever mode is chosen is announced before the request goes out.

WHAT A RESULT MEANS, and this is the sentence most easily lost:

    RETRIEVABLE        the endpoint returned a usable public record for this identifier,
                       from this vantage, at this moment.
    NOT-RETRIEVABLE    the endpoint refused, and the refusal survived every confirmation pass.
                       The refusal is a single opaque HTTP 400 and is SEMANTICALLY EMPTY:
                       session 109's three-arm control with twenty synthetic identifiers showed
                       that a video which never existed returns exactly the same code, and that
                       no 404 is ever returned. It therefore means "not publicly retrievable
                       from here, now". IT DOES NOT MEAN DELETED, removed, banned, or private,
                       and this tool will not say so.
    UNCONFIRMED-ABSENT the first pass refused and at least one confirmation pass did not. This
                       is an instrument artefact by this arc's own criterion (K4,
                       `PREREGISTRATION-112.md` §4) and is EXCLUDED from the absence rate.
    INDETERMINATE      a transport failure or an unexpected status. Not evidence either way.

WHY CONFIRMATION IS NOT OPTIONAL BY DEFAULT, stated with the record behind it. This arc has
re-requested eight readings that looked like changes. Of the three genuine disappearances, ONE
survived and TWO did not. Of the three genuine returns, three survived. Computed from the raw
sidecars by `confirmation_record_121.py` -> `confirmation-record-121.json`; the same file counts
the raw readings including two of this arc's own artefact echoes (5 of 5 returns, 1 of 3
disappearances). Six events is not a rate and this tool will not turn it into one. What it does
establish is that a single refusal from this endpoint is not a fact yet, and a tool that reports
one as absence reports something its own maker does not believe.

THE ASYMMETRY IN THIS DESIGN, STATED RATHER THAN HIDDEN. By default only NOT-RETRIEVABLE
readings are confirmed, because those are the readings that carry a claim. A RETRIEVABLE reading
is therefore taken on one pass, and this tool CANNOT detect a false reading of presence. This
arc has never observed one — and has never looked, which is not the same thing. `--confirm-what
all` re-requests every reading and closes the gap at roughly six times the requests.

HOW THIS DIFFERS FROM THIS PRACTICE'S OWN DAILY LEDGER, which is a difference and not a defect.
The daily ledger takes ONE pass per identifier per day and applies confirmation to the
*transitions* between two days. A stranger measuring one list on one day has no previous day and
therefore no transitions, so the only confirmation available is of the readings themselves. The
two instruments are not the same and a figure from one is not a row of the other.

The probe is imported from ledger.py rather than re-implemented, so a list measured with this
tool is measured at the same rate, with the same classifier, as every row of this practice's own
ledger.

Offered under the conditions in memory/downstream-commitments.md. Those are conditions this
practice asks a reuser to honour, not obligations imposed on anybody.
"""

import argparse
import calendar
import json
import re
import sys
import time

import ledger

VERSION = "0.3.0"
YEAR_S = 365.25 * 86400.0
DEFAULT_CONFIRM = 5
# Session 122, 2026-08-16. Measured, not chosen: the day on which the drift caused by a frozen
# reference first exceeds 0.1826 pp — the largest single band-rate error the reference table's
# own bookkeeping defect (V1) ever produced. `drift-122.json`, key
# half_two_caller_side_drift.when_the_design_half_overtakes_the_bookkeeping_half.
STALE_AFTER_DAYS = 26

# CORRECTED session 121, condition I4 of INTERLOCUTOR-12.md. The v0.1 rule was a bare
# `(\d{1,25})` search anywhere in the line, which turned any line containing a digit into an
# identifier: `2026-08-15` measured the video `2026`, and a URL from a different platform
# measured `4`. The floor of one digit is KEPT — this arc's own legacy-identifier control
# (session 110, D12) established that `12345` is a real video returning a full body, so a rule
# that discards short identifiers discards real data. What is added is that the identifier must
# be the WHOLE field, or the digits of a `/video/` path. Everything else is refused out loud.
#
# v0.2.1, session 121: the adversary found that v0.2's repair was domain-blind — it matched
# `/video/<digits>` anywhere in any URL, so `https://www.youtube.com/video/7123…` and
# `https://example.com/video/7123…/watch` were ACCEPTED and measured against this platform's
# endpoint. That is I4's own failure through the accepted path instead of the refused one. The
# host is now checked, and the platform's `/v/<digits>` share path is accepted because it is the
# same platform and names the identifier plainly.
VIDEO_PATH_RE = re.compile(r"/(?:video|v)/(\d{1,25})(?:[./?#]|$)")
ALL_DIGITS_RE = re.compile(r"^(\d{1,25})$")
HANDLE_RE = re.compile(r"@([A-Za-z0-9._-]+)")
URL_HOST_RE = re.compile(r"^[a-z][a-z0-9+.-]*://([^/?#]+)", re.I)
PLATFORM_HOST_RE = re.compile(r"(?:^|\.)tiktok\.com$", re.I)
# Tab, semicolon, comma or run of spaces — the separators an ordinary spreadsheet export uses.
# v0.2 accepted only the comma and refused the rest, which is a tool refusing real lists.
FIELD_SPLIT_RE = re.compile(r"[,;\t]|\s{1,}")
AGE_BANDS = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 99)]

STATE_RETRIEVABLE = "RETRIEVABLE"
STATE_ABSENT = "NOT-RETRIEVABLE"
STATE_UNCONFIRMED = "UNCONFIRMED-ABSENT"
STATE_INDETERMINATE = "INDETERMINATE"


def band_label(lo, hi):
    return f"{lo}-{hi}y" if hi < 99 else f"{lo}y+"


def band_of(age_y):
    for lo, hi in AGE_BANDS:
        if lo <= age_y < hi:
            return band_label(lo, hi)
    return None


def parse_line(line):
    """Return (vid, handle, reason). vid is None when the line is refused.

    Accepted, and nothing else:
        https://www.tiktok.com/@someuser/video/7123456789012345678   (any /video/<digits> URL)
        7123456789012345678                                          (the whole field is digits)
        7123456789012345678,someuser                                 ('id,handle')

    Refused, with the reason returned so the caller can print it: a date, a sentence containing
    a year, a short link that has to be resolved before it names anything, a URL from another
    platform. v0.1 measured all four of these as videos.
    """
    line = line.strip()
    if not line or line.startswith("#"):
        return None, None, None
    handle = None
    m = HANDLE_RE.search(line)
    if m:
        handle = m.group(1)
    field = line
    if not URL_HOST_RE.match(line):
        parts = [p.strip() for p in FIELD_SPLIT_RE.split(line) if p.strip()]
        if len(parts) >= 2 and parts[1]:
            handle = parts[1].lstrip("@")
        if parts:
            field = parts[0]

    host_m = URL_HOST_RE.match(field)
    if host_m:
        host = host_m.group(1).split("@")[-1].split(":")[0]
        if not PLATFORM_HOST_RE.search(host):
            return None, None, (f"a URL on {host!r}, which is not this platform — this tool "
                                "measures one platform's endpoint and will not treat another "
                                "host's path as an identifier of it")
        m = VIDEO_PATH_RE.search(field)
        if m:
            return m.group(1), (handle or "x"), None
        return None, None, ("a URL on this platform with no /video/<digits> or /v/<digits> path "
                            "— a share link of the vm./vt. kind names no identifier until it is "
                            "resolved, and this tool does not follow redirects")

    m = VIDEO_PATH_RE.search(field)
    if m:
        return m.group(1), (handle or "x"), None
    m = ALL_DIGITS_RE.match(field)
    if m:
        return m.group(1), (handle or "x"), None
    return None, None, ("not an identifier — the field must be a /video/<digits> URL on this "
                        "platform or digits only; a date, a year inside a sentence or a title "
                        "is refused")


def dated(vid, t_ref):
    """This arc's dating rule, WITH its measured breakpoint honoured.

    id >> 32 is unix seconds ONLY inside the platform's modern 19-digit scheme. Session 110
    measured the rule breaking outside it (194951213564514304 is live and decodes to 1971),
    so anything that is not 19 digits is returned undatable rather than silently dated.
    """
    if len(vid) != 19:
        return None, None, "not-19-digit: dating rule does not hold outside the modern scheme"
    created = int(vid) >> 32
    age_s = t_ref - created
    if age_s <= 0:
        return created, None, "creation timestamp is not before the reference time"
    return created, age_s / YEAR_S, None


def load_baseline(path):
    try:
        b = json.load(open(path))
    except Exception as e:
        return None, f"baseline not loaded from {path!r} ({type(e).__name__})"
    if b.get("schema") != "field-research/public-presence-null/1":
        return None, (f"baseline at {path!r} has schema {b.get('schema')!r}, expected "
                      "'field-research/public-presence-null/1'")
    return b, None


def baseline_currency(baseline, t_ref):
    """How old is the yardstick, according to the yardstick?

    A reference table is a measurement of one population on one day. Used months later it is
    still arithmetic, and still wrong in a direction nobody can see from the output. This tool
    cannot verify the reference time — it can only report what the file declares and how far
    the measurement now stands from it, which is the difference between a stale yardstick a
    reader can notice and one they cannot.

    The declared time is a claim the file makes about itself. This arc's own shipped reference
    table was found at the session-120 gauntlet to declare one reference time while its ages had
    been computed against another, three days earlier (errata E6) — which is exactly why the
    declaration is reported as a declaration and never as a fact.
    """
    if not baseline:
        return None
    declared = baseline.get("t_ref_utc")
    out = {"declared_t_ref_utc": declared,
           "status": "declared by the baseline file; NOT verified by this tool",
           "age_days_at_measurement": None}
    if not declared:
        out["status"] = "the baseline declares no reference time at all"
        return out
    try:
        parsed = calendar.timegm(time.strptime(declared, "%Y-%m-%dT%H:%M:%SZ"))
    except Exception:
        out["status"] = f"the baseline's reference time {declared!r} is not readable"
        return out
    out["age_days_at_measurement"] = round((t_ref - parsed) / 86400.0, 3)
    return out


def band_hist(rows, key="band"):
    h = {}
    for r in rows:
        if r.get(key):
            h[r[key]] = h.get(r[key], 0) + 1
    return h


def rebanded(rows, t_target):
    """The caller's own rows, re-aged at another clock. Used for one thing only: to show the
    caller what the reference table's own reference time would have said about their list."""
    out = []
    for r in rows:
        vid = str(r["vid"])
        b = None
        if len(vid) == 19:
            age = (t_target - (int(vid) >> 32)) / YEAR_S
            b = band_of(age) if age > 0 else None
        out.append({"band": b})
    return out


def drift(rows, baseline, t_now):
    """THE FROZEN-REFERENCE DRIFT, measured on the caller's own list rather than described.

    V1 and V2 of the session-120 gauntlet; repaired and measured at session 122, 2026-08-16.
    The full measurement on this arc's own panel is `drift-122.json` / `DRIFT-122.md`.

    The problem this exists to make visible: the reference table is a measurement of one
    population on ONE DAY. This tool ages the caller's identifiers at the moment the caller
    runs it and then looks those ages up in that fixed table. So the two clocks diverge by
    exactly the time the tool has sat unused, and the printed expectation walks away from
    anything that was ever observed while keeping the same name and the same decimals.

    On this arc's own panel the walk is +0.0035 pp after a day, +0.2264 pp after a month,
    +2.4225 pp after a year, +4.1649 pp after two — and after 26 days it exceeds the largest
    error the reference table's own bookkeeping defect ever caused. It is not a forecast of
    retrievability: nothing was re-measured at any of those horizons. It is how far the
    ARITHMETIC moves.

    So: both numbers, always, with the reference-time one named as the defensible one. The
    caller does not have to trust this docstring — the gap is computed on their list.
    """
    if not baseline:
        return None
    declared = baseline.get("t_ref_utc")
    if not declared:
        return None
    try:
        t_decl = calendar.timegm(time.strptime(declared, "%Y-%m-%dT%H:%M:%SZ"))
    except Exception:
        return None
    at_now = expectation(rows, baseline)
    at_ref = expectation(rebanded(rows, t_decl), baseline)
    if not at_now or not at_ref:
        return None
    gap_d = (t_now - t_decl) / 86400.0
    return {
        "days_between_the_two_clocks": round(gap_d, 3),
        "expected_with_the_list_aged_at_the_reference_time": at_ref["expected_absent_rate"],
        "expected_with_the_list_aged_at_now": at_now["expected_absent_rate"],
        "drift_pp": 100 * (at_now["expected_absent_rate"] - at_ref["expected_absent_rate"]),
        "age_histogram_at_the_reference_time": band_hist(rebanded(rows, t_decl)),
        "age_histogram_at_now": band_hist(rows),
        "which_one_is_defensible": (
            "the reference-time one. It is the only reading in which the ages and the table's "
            "clock agree, and it says what it can honestly say: for a list with this age "
            "profile, the reference population showed this much public absence ON THE "
            "REFERENCE DAY. The now-aged one extrapolates a single cross-section forward as "
            "though it were a hazard, which this arc has explicitly withdrawn as a claim — a "
            "single cross-section cannot separate the age of a video from the cohort it was "
            "created in, and this arc's own forum arm reverses the sign of the age gradient "
            "when first-citation year is held fixed (underpowered, p = 0.69)."),
        "the_drift_is_not_a_forecast": (
            "no part of this figure says retrievability itself changed. It says how far this "
            "tool's own arithmetic has moved from the day the table was measured."),
    }


def expectation(rows, baseline):
    """What public absence would be EXPECTED for a list with this age profile.

    This is the transfer function of presence-baseline.json applied to the caller's OWN age
    histogram. It is a comparison against ONE reference population - videos cited in an
    encyclopedia and posted to one technology forum, measured from one vantage on one day.
    A list drawn from somewhere else may legitimately sit far outside it, and doing so is
    NOT by itself evidence of anything. This number is a yardstick, not a verdict.
    """
    if not baseline:
        return None
    table = baseline["by_age_band"]
    hist = {}
    for r in rows:
        if r.get("band"):
            hist[r["band"]] = hist.get(r["band"], 0) + 1
    if not hist:
        return None
    tot = sum(hist.values())
    point = lo = hi = 0.0
    for b, w in hist.items():
        c = table.get(b)
        if not c or not c["n"]:
            continue
        point += (w / tot) * c["absent_rate"]
        lo += (w / tot) * c["absent_ci"][0]
        hi += (w / tot) * c["absent_ci"][1]
    return {"age_histogram": hist, "n_dated": tot,
            "expected_absent_rate": point, "expected_lo": lo, "expected_hi": hi,
            "reference_population": {
                "source": baseline["source_run"]["file"],
                "run_id": baseline["source_run"]["run_id"],
                "n": baseline["pooled"]["n"],
                "what_it_is": ("videos cited across MediaWiki language editions and posted to "
                               "one public technology forum, measured from "
                               f"{baseline['source_run']['vantage_asn']} on one day"),
            }}


def read_vantage(mode, probe=None):
    """Record where the measurement stands — under the caller's disclosure choice.

    CONDITION I7. v0.1 called a commercial IP-geolocation service unconditionally and wrote the
    caller's IP address, city, region, coordinates and timezone into the output file, and no
    document in the bundle mentioned it. The vantage is genuinely load-bearing — a figure from
    one network location is not a figure from another — but the AS number is the whole of what
    any figure here uses.
    """
    if mode == "none":
        return {"mode": "none", "asn": None, "country": None,
                "note": ("no third-party call was made, so no vantage was recorded. Figures "
                         "from an unrecorded vantage cannot be compared with figures from a "
                         "recorded one, which is the reason this is not the default.")}
    van = (probe or ledger.vantage)()
    if mode == "full":
        van = dict(van)
        van["mode"] = "full"
        van["disclosure"] = ("this record contains the caller's own IP address and approximate "
                             "location, obtained from a third-party service. Do not publish or "
                             "forward this file without reading this field.")
        return van
    return {"mode": "asn",
            "asn": van.get("asn"), "country": van.get("country"),
            "source": van.get("source"), "fetched_utc": van.get("fetched_utc"),
            "note": ("only the autonomous system and country are kept. The lookup itself "
                     "disclosed this machine's IP address to the service named in `source`; "
                     "that cannot be undone by discarding the answer, and --vantage none "
                     "avoids the call entirely.")}


def measure(items, t_ref, confirm, confirm_what, probe=None, sleep=None, log=None):
    """One pass over every identifier, then the confirmation passes that carry the claim.

    `probe` and `sleep` are injected so the logic is testable without the network; in
    production they are ledger.probe_one and time.sleep.
    """
    probe = probe or ledger.probe_one
    sleep = sleep if sleep is not None else time.sleep
    log = log or (lambda *_: None)
    rows = []
    for i, (vid, handle) in enumerate(items):
        rec = probe(vid, handle)
        rec["vid"] = vid
        rec["handle_sent"] = handle
        first = ledger.classify(rec)
        rec["first_pass_state"] = first
        rec["state"] = first
        created, age_y, why = dated(vid, t_ref)
        rec["created_utc"] = (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(created))
                              if created else None)
        rec["age_y"] = age_y
        rec["band"] = band_of(age_y) if age_y is not None else None
        if why:
            rec["dating_note"] = why
        rows.append(rec)
        if i + 1 < len(items):
            sleep(ledger.DELAY)

    if confirm <= 0:
        for r in rows:
            r["confirmation"] = None
        return rows

    if confirm_what == "all":
        targets = [r for r in rows if r["first_pass_state"] in (STATE_RETRIEVABLE, STATE_ABSENT)]
    else:
        targets = [r for r in rows if r["first_pass_state"] == STATE_ABSENT]
    log(f"confirmation: {len(targets)} reading(s) x {confirm} pass(es) = "
        f"{len(targets) * confirm} further request(s)")
    for r in rows:
        r["confirmation"] = None
    for r in targets:
        states = []
        for _ in range(confirm):
            sleep(ledger.DELAY)
            rec = probe(r["vid"], r["handle_sent"])
            states.append(ledger.classify(rec))
        # v0.2.1, session 121, the adversary's blocking charge 1. v0.2 asked `all(s == first)`,
        # which treated a pass that TIMED OUT exactly like a pass that came back with the
        # opposite state. At this arc's own measured transport-failure rate of 1.24 %
        # (PREREGISTRATION-112.md §P2) the chance that at least one of five passes is noise is
        # 6.05 %, so roughly one genuinely absent unit in seventeen was being thrown out of both
        # numerator and denominator — pushing the reported absence rate DOWN, and worst exactly
        # when the endpoint is under the load the confirmation step itself adds.
        #
        # A pass is now one of three things and they are not merged:
        #   agreeing     — determinate and equal to the first-pass reading
        #   reversing    — determinate and opposite: this is what refutes a reading
        #   noise        — INDETERMINATE: it says nothing, and is counted as nothing
        reversing = [s for s in states
                     if s in (STATE_RETRIEVABLE, STATE_ABSENT) and s != r["first_pass_state"]]
        agreeing = [s for s in states if s == r["first_pass_state"]]
        noise = [s for s in states if s == STATE_INDETERMINATE]
        conf = {"passes": confirm, "states": states,
                "n_agreeing": len(agreeing), "n_reversing": len(reversing),
                "n_noise": len(noise),
                "partial": bool(noise) and not reversing,
                "agreed": not reversing and bool(agreeing),
                "rule": ("a reading is refuted only by a determinate pass that disagrees with "
                         "it. An INDETERMINATE pass is noise and is counted as nothing — never "
                         "as disagreement.")}
        r["confirmation"] = conf
        if reversing:
            if r["first_pass_state"] == STATE_ABSENT:
                r["state"] = STATE_UNCONFIRMED
            else:
                r["state"] = STATE_INDETERMINATE
                conf["note"] = ("a first-pass RETRIEVABLE reading that a determinate pass "
                                "contradicted is not evidence either way")
        elif not agreeing:
            # Every pass was noise. The confirmation did not run, and pretending it confirmed
            # anything would be worse than reporting that nothing was learned.
            r["state"] = STATE_INDETERMINATE
            conf["note"] = (f"all {confirm} confirmation passes were INDETERMINATE: the "
                            "confirmation did not run, so this reading is reported as "
                            "INDETERMINATE rather than as a confirmed or a refuted absence")
        elif noise:
            conf["note"] = (f"confirmed on {len(agreeing)} of {confirm} passes; "
                            f"{len(noise)} pass(es) were transport noise and counted as nothing. "
                            "A consumer wanting full-strength confirmations only should filter "
                            "on confirmation.partial == false.")
    return rows


def tally(rows):
    counts = {}
    for r in rows:
        counts[r["state"]] = counts.get(r["state"], 0) + 1
    det = counts.get(STATE_RETRIEVABLE, 0) + counts.get(STATE_ABSENT, 0)
    rate = (counts.get(STATE_ABSENT, 0) / det) if det else None
    return counts, det, rate


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("listfile")
    ap.add_argument("-o", "--out", default=None)
    ap.add_argument("--baseline", default="presence-baseline.json")
    ap.add_argument("--label", default=None, help="a name for this list, recorded as given")
    ap.add_argument("--confirm", type=int, default=DEFAULT_CONFIRM,
                    help=(f"re-request each claim-carrying reading N times (default "
                          f"{DEFAULT_CONFIRM}, matching this practice's own confirmation step). "
                          "--confirm 0 reports single readings and says so in the output."))
    ap.add_argument("--confirm-what", choices=("absent", "all"), default="absent",
                    help=("which readings to confirm. 'absent' (default) confirms only the "
                          "readings that carry a claim; 'all' also re-requests RETRIEVABLE "
                          "readings, at roughly six times the requests."))
    ap.add_argument("--vantage", choices=("asn", "full", "none"), default="asn",
                    help=("what to record about where you are standing. 'asn' (default) keeps "
                          "the autonomous system and country; 'full' also writes your IP, city, "
                          "region, coordinates and timezone into the output; 'none' makes no "
                          "third-party call at all."))
    a = ap.parse_args(argv)

    items, bad = [], []
    for raw in open(a.listfile, encoding="utf-8"):
        vid, handle, reason = parse_line(raw)
        if vid:
            items.append((vid, handle))
        elif reason:
            bad.append({"line": raw.strip()[:120], "reason": reason})
    if not items:
        print("no identifiers found in", a.listfile, file=sys.stderr)
        for x in bad:
            print(f"  refused: {x['line']}\n           {x['reason']}", file=sys.stderr)
        return 2
    # Condition 3 of session 113, kept: a dropped line is announced where a human will see it,
    # on both streams, never only in a field of the output file. What is new in 0.2 is that the
    # reason is printed too, because "dropped" without a reason invites the reader to assume a
    # typo when the tool has in fact refused a whole class of input.
    if bad:
        print(f"WARNING: {len(bad)} line(s) in {a.listfile} were REFUSED and NOT measured:")
        for x in bad:
            print(f"  refused: {x['line']}")
            print(f"           {x['reason']}")
        print(f"WARNING: {len(bad)} line(s) refused in {a.listfile}; see stdout for the list "
              f"and the reasons", file=sys.stderr)

    baseline, bwhy = load_baseline(a.baseline)
    # CONDITION I6. In v0.1 this failure was a single field in the output file, and the run
    # printed a complete-looking report without the comparison it advertises. It is now loud on
    # both streams and it changes the exit status, so a script that checks one cannot miss it.
    if bwhy:
        bar = "!" * 78
        print(f"\n{bar}\nWARNING: NO EXPECTATION WILL BE COMPUTED.\n  {bwhy}\n"
              f"  The measurement below is unaffected and stands on its own; what is missing is\n"
              f"  the comparison against the reference population. Exit status will be 3.\n"
              f"{bar}\n")
        print(f"WARNING: baseline not loaded — {bwhy}; expectation omitted, exiting 3",
              file=sys.stderr)

    # The cost is printed before the first request, because how many requests this will make
    # depends on how many readings turn out to carry a claim and a caller cannot work that out
    # from the list. The ceiling is stated; the actual number is printed when it is known.
    worst = len(items) * max(a.confirm, 0)
    print(f"presence_check {VERSION}: {len(items)} identifier(s) from {a.listfile}")
    print(f"  confirmation: {a.confirm} pass(es) per {a.confirm_what}-reading "
          f"({'OFF — single readings' if a.confirm <= 0 else 'on'}); "
          f"first pass is {len(items)} request(s), confirmation adds at most {worst} "
          f"(one per {a.confirm_what} reading x {max(a.confirm, 0)}), "
          f"~{(len(items) + worst) * ledger.DELAY / 60:.0f} min at this instrument's rate")
    print(f"  vantage mode: {a.vantage}" + {
        "asn": " — autonomous system and country only; the lookup still discloses this "
               "machine's IP to the service",
        "full": " — YOUR IP, CITY, REGION, COORDINATES AND TIMEZONE WILL BE WRITTEN INTO THE "
                "OUTPUT FILE",
        "none": " — no third-party call; no vantage recorded, and figures are then not "
                "comparable across locations",
    }[a.vantage])

    # The vantage is read BEFORE the first measurement request, never after. Every figure
    # this instrument produces is conditional on where it was standing.
    van = read_vantage(a.vantage)
    t0 = time.time()
    t_ref = calendar.timegm(time.gmtime(t0))
    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0))

    rows = measure(items, t_ref, a.confirm, a.confirm_what, log=lambda m: print("  " + m))
    counts, det, rate = tally(rows)
    n_unconfirmed = counts.get(STATE_UNCONFIRMED, 0)

    out = {
        "schema": "field-research/presence-check/2",
        "tool": "presence_check.py",
        "tool_version": VERSION,
        "list": {"file": a.listfile, "label": a.label,
                 "n_items": len(items), "refused_lines": bad},
        "started_utc": started,
        "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "seconds": round(time.time() - t0, 1),
        "vantage": van,
        "probe": {"endpoint": ledger.ENDPOINT, "user_agent": ledger.UA,
                  "delay_s": ledger.DELAY, "timeout_s": ledger.TIMEOUT,
                  "imported_from": "ledger.py (not re-implemented)"},
        "confirmation": {
            "passes": a.confirm,
            "applied_to": a.confirm_what,
            "enabled": a.confirm > 0,
            "rule": ("a reading is kept only if every confirmation pass agrees with it. A "
                     "first-pass refusal that does not survive is reported as "
                     "UNCONFIRMED-ABSENT and excluded from the absence rate — this arc's K4 "
                     "criterion, PREREGISTRATION-112.md §4."),
            "record_behind_the_default": (
                "of this arc's three genuine disappearance readings, one survived five "
                "re-requests and two did not; of its three genuine return readings, three "
                "survived. Six events, computed in confirmation-record-121.json. Not a rate."),
            "warning_if_disabled": (None if a.confirm > 0 else
                                    "CONFIRMATION WAS DISABLED. Every NOT-RETRIEVABLE below is "
                                    "a single reading from an endpoint whose refusal this "
                                    "practice has watched fail to reproduce."),
            "asymmetry": ("with --confirm-what absent (the default) a RETRIEVABLE reading is "
                          "taken on one pass; this tool cannot detect a false reading of "
                          "presence and has never looked for one."),
            "direction_of_the_bias_this_creates": (
                "stated because the code forces it, not because it was measured. A refuted "
                "absence is DISCARDED (UNCONFIRMED-ABSENT, out of numerator and denominator) "
                "rather than reclassified to RETRIEVABLE, while a false presence is never "
                "tested at all and stays in the denominator on the retrievable side. Both "
                "effects push the reported absence rate DOWN relative to a symmetric regime. "
                "The size is unknown. --confirm-what all removes the second effect and not the "
                "first."),
            "what_five_passes_is_and_is_not": (
                "five is the number this arc pre-registered at session 112, and this practice's "
                "own record declines to certify it: PREREGISTRATION-119-overlay-use.md says in "
                "as many words that K4's five re-requests are 'not claimed' to be the right "
                "test, only the pre-registered one. Nothing here has measured what a sixth pass "
                "or a pass at an hour's delay would add. Treat --confirm 5 as a precedent this "
                "tool follows, never as a threshold anyone validated."),
        },
        "counts": counts,
        "determinate": det,
        "public_absence_rate": rate,
        "absence_rate_denominator": ("RETRIEVABLE + NOT-RETRIEVABLE; UNCONFIRMED-ABSENT and "
                                     "INDETERMINATE are excluded from both parts"),
        "n_unconfirmed_absent": n_unconfirmed,
        "expectation_for_this_age_profile": expectation(rows, baseline),
        "frozen_reference_drift": drift(rows, baseline, t_ref),
        "baseline_currency": baseline_currency(baseline, t_ref),
        "baseline_note": bwhy,
        "what_not_retrievable_means": (
            "not publicly retrievable from this vantage at this time, on a first pass and every "
            "confirmation pass. The endpoint's refusal is a single opaque HTTP 400 that a "
            "never-existing identifier also returns (session 109 three-arm control, 20 "
            "synthetic identifiers). NOT DELETED."),
        "observations": rows,
    }

    dest = a.out or f"presence-check-{time.strftime('%Y-%m-%dT%H%MZ', time.gmtime(t0))}.json"
    json.dump(out, open(dest, "w"), indent=1)

    print(f"{a.label or a.listfile}: {len(items)} identifiers, {out['seconds']} s, "
          f"vantage {van.get('asn')} ({van.get('country')})")
    for r in rows:
        age = f"{r['age_y']:.2f}y" if r["age_y"] is not None else "undated"
        conf = ""
        if r.get("confirmation"):
            conf = f" conf={'+' if r['confirmation']['agreed'] else 'FAILED'}"
        print(f"  {r['vid']}  {r['state']:<18} http={str(r.get('http')):<5} {age}{conf}")
    print(f"counts {counts}")
    if n_unconfirmed:
        print(f"NOTE: {n_unconfirmed} refusal(s) did not survive confirmation and are NOT "
              f"counted as absence")
    if rate is not None:
        print(f"observed public absence {rate:.4f} ({counts.get(STATE_ABSENT, 0)}/{det})")
    if a.confirm <= 0:
        print("NOTE: confirmation was disabled; every absence above is a single reading")
    cur = out["baseline_currency"]
    if cur and cur.get("age_days_at_measurement") is not None:
        age_d = cur["age_days_at_measurement"]
        print(f"reference table declares {cur['declared_t_ref_utc']} — {age_d:.1f} day(s) "
              f"before this measurement (declared, not verified by this tool)")
        # Session 122: the threshold is measured, not chosen. STALE_AFTER_DAYS is the day on
        # which the drift this staleness causes first exceeds the largest single error the
        # reference table's own bookkeeping defect ever produced (0.1826 pp). Before that day
        # the staleness is smaller than a defect this practice published a public erratum for;
        # after it, it is larger. `drift-122.json` -> when_the_design_half_overtakes...
        if age_d > STALE_AFTER_DAYS:
            print(f"WARNING: the reference table is {age_d:.0f} days old, past the {STALE_AFTER_DAYS}-day "
                  f"mark at which staleness outweighs the worst bookkeeping error this table "
                  f"has ever carried. An expectation from a stale yardstick is arithmetic, not "
                  f"a comparison.")
            print(f"WARNING: reference table {age_d:.0f} days old (stale after {STALE_AFTER_DAYS})",
                  file=sys.stderr)
    exp = out["expectation_for_this_age_profile"]
    dr = out["frozen_reference_drift"]
    if exp:
        # The reference-time figure leads, because it is the one whose ages and table agree.
        if dr:
            print(f"expected for this age profile, AT THE REFERENCE TIME "
                  f"{dr['expected_with_the_list_aged_at_the_reference_time']:.4f} "
                  f"— a yardstick from a different population, not a verdict")
            print(f"  the same list aged at today instead: "
                  f"{dr['expected_with_the_list_aged_at_now']:.4f} "
                  f"({dr['drift_pp']:+.4f} pp over {dr['days_between_the_two_clocks']:.1f} day(s) "
                  f"of frozen reference). This gap is arithmetic drift, NOT a measurement that "
                  f"retrievability changed.")
        else:
            print(f"expected for this age profile {exp['expected_absent_rate']:.4f} "
                  f"[{exp['expected_lo']:.4f}, {exp['expected_hi']:.4f}] "
                  f"— a yardstick from a different population, not a verdict")
    print("written", dest)
    return 3 if bwhy else 0


if __name__ == "__main__":
    sys.exit(main())
