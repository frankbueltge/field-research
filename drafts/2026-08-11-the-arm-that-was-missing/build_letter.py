#!/usr/bin/env python3
"""build_letter - builds the object `CONDITIONS-127.md` made binding after the eighth review.

Session 128, 2026-08-20. The eighth review did not fail on packaging, which is what the seven
before it failed on. It failed because this practice fetched a 246,014-byte file, hashed it, cited
it by hash in the third paragraph of a letter addressed to the person who publishes it, and never
opened it past six summary tiles. Inside was a better finding than the one the letter shipped.

So this is not a repair pass on that letter. It is the letter this practice would have written if
it had read what it already had.

WHAT IS DIFFERENT FROM `build_offer.py`, ITEM BY ITEM AGAINST THE CONDITIONS IT IS BOUND BY
--------------------------------------------------------------------------------------------
(1) READ THE EVIDENCE. The receiver's own per-video record is extracted by `extract_dashboard.py`
    (an element walk, not a regex) and derived by `dashboard_findings.py`; both ship inside the
    object and both are commands the letter prints, so the central finding is reproducible by the
    reader offline, from bytes in the same directory, without this practice's cooperation.

(3) GUARDS IN THE READER'S ENVIRONMENT, NOT THE BUILDER'S. `build_offer.py` set
    PYTHONDONTWRITEBYTECODE for every subprocess, and its inventory and subdirectory guards
    passed because of it — then the object grew three `.pyc` files thirty-three seconds after
    being frozen, when a reviewer typed the letter's own command. THIS BUILD NEVER SETS THAT
    VARIABLE, anywhere. The tool sets `sys.dont_write_bytecode` in its own source instead, which
    is true on a reader's machine too, and phase D proves it in a clean copy outside this
    repository with a clean environment.

(4) THE CONFIRMATION RECORD IS COMPUTED BY THIS BUILD, by running its generator here, and its
    coverage is then checked against the ledger: the sidecars it read must be exactly the
    sidecars on disk. `build_offer.py` read a file a separate script had written four minutes
    earlier and stamped the build's own clock on it, which honoured the condition in outcome and
    not in mechanism.

(5) THE LENGTH CONDITION IS ENFORCED. `build_offer.py` measured the letter's length and asserted
    it against nothing; two of three strangers stopped reading before the end.

(6) EVERY SHIPPED FILE IS THE LIVE FILE. The instrument is no longer patched into existence at
    build time out of a retired bundle's copy — that is how v0.3.2 shipped a version note saying
    three stale passages were gone with the third one eight lines below it, and how the object
    shipped the pre-repair copy of `run_lock.py`. The tool lives in `tool/` as source, is edited
    there, and is COPIED here byte for byte. The build asserts the copy is byte-identical.

WHAT IS KEPT, BECAUSE THE EIGHTH REVIEW SAID IT WORKED
------------------------------------------------------
One list of commands, `CMDS`. The letter renders its command blocks from it; the build runs every
entry (phase A); phase C re-extracts every fenced command from the FINISHED letter and fails
unless that set equals the set the build ran, then runs each again from scratch; phase D runs the
offline ones from a copy made outside this repository. No figure in the letter is typed: `fx()`
fetches each from a named field of a named JSON file and raises if the field is absent.

Usage:  python3 build_letter.py [--out letter]
"""
import argparse
import datetime
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLDIR = os.path.join(HERE, "tool")

# The dashboard, as read TODAY. Its bytes are also compared against the two earlier reads, so the
# letter's claim that the page has not changed is a comparison and not an impression.
DASH = os.path.join(HERE, "receiver-dashboard-2026-08-20.html")
DASH_PRIOR = [os.path.join(HERE, "receiver-dashboard-2026-08-19.html"),
              os.path.join(HERE, "receiver-dashboard-2026-08-16.html")]
DASH_URL = "https://playground.tiktok-audit.com/api-na/"
LIST_SRC = os.path.join(HERE, "receiver-list.txt")
BASELINE_SRC = os.path.join(HERE, "deliverable-v0.3", "reference-baseline.json")
PRIOR_ELEVEN = os.path.join(HERE, "deliverable-v0.3", "receiver-eleven.json")
PRIOR_ELEVEN_2 = os.path.join(HERE, "offer", "your-eleven-today.json")

PERSON = "Frank Bültge"
PERSON_URL = "https://frankbueltge.de"
REPO_URL = "https://github.com/frankbueltge/field-research"

# The receiver's own words for what their dashboard watches, checked against the report text in
# this directory (`receiver-report-2506.09746v2-extracted.txt`) by `_check_quote` below. The
# eighth review found the previous letter stating this criterion backwards.
RECEIVER_QUOTE = ("we publish a dashboard with a daily check of the availability of 10 videos "
                  "that were not retrievable in the last month")
RECEIVER_REPORT = os.path.join(HERE, "receiver-report-2506.09746v2-extracted.txt")
RECEIVER_REPORT_ID = "arXiv:2506.09746"
RECEIVER_REPORT_TITLE = "TikTok's Research API: Problems Without Explanations"
RECEIVER_ORG = "AI Forensics"
OBJECT_VERSION = "2.0"
DASH_NOTE = "Note: Error are problems on our end, not TikTok."

# The one list of commands. Order is the order the letter prints them in.
CMDS = [
    ["python3", "extract_dashboard.py", "--selftest", "receiver-dashboard-2026-08-20.html"],
    ["python3", "extract_dashboard.py", "receiver-dashboard-2026-08-20.html",
     "-o", "receiver-series.json"],
    ["python3", "dashboard_findings.py", "receiver-series.json",
     "--reading", "your-eleven-today.json", "-o", "dashboard-findings.json"],
    ["python3", "selftest_presence_check.py"],
    ["python3", "presence_check.py", "receiver-list.txt", "--baseline", "none",
     "--label", "the-eleven", "-o", "your-eleven-today.json"],
]
# Everything except the live probe. Phase D runs these from a copy outside this repository, in a
# clean environment, and asserts the directory's file set is unchanged afterwards.
OFFLINE = [c for c in CMDS if c[1] != "presence_check.py"]
# The live probe must run BEFORE dashboard_findings.py, which reads its output. Phase A therefore
# runs the list in dependency order, not in print order.
ORDER_A = [4, 0, 1, 2, 3]

WORD_CEILING = 1100

DESCRIPTIONS = {
    "LETTER.md": "this letter",
    "BUILD.json": ("every command this build ran, its exit status, and a hash of every file "
                   "here"),
    "receiver-dashboard-2026-08-20.html": ("your dashboard, saved this morning; the bytes the "
                                           "finding above is computed from"),
    "extract_dashboard.py": "reads the per-video series out of those bytes",
    "dashboard_findings.py": "turns the series into the figures this letter quotes",
    "receiver-series.json": "what the extractor read, series by series",
    "dashboard-findings.json": "every figure above, in the field this letter fetched it from",
    "presence_check.py": "the instrument, version 0.3.3",
    "selftest_presence_check.py": "the instrument's own test suite, offline",
    "ledger.py": "the request layer the instrument imports, unchanged and not re-implemented",
    "run_lock.py": "the reservation the daily probe takes; imported by ledger.py",
    "drift-122.json": ("the measurement four of the suite's assertions check the instrument "
                       "against"),
    "receiver-list.txt": "the eleven identifiers, transcribed from your dashboard",
    "your-eleven-today.json": "this morning's live run, as the tool wrote it",
    "confirmation-record.json": "the re-request record, computed by this build from the sidecars",
    "series-status.json": "the daily series' length and holes, computed from its ledger",
}


class FigureMissing(Exception):
    pass


class Fx:
    """Fetch a figure from a named field of a named JSON file, or fail the build."""

    def __init__(self):
        self.cache = {}
        self.log = []

    def _doc(self, path):
        if path not in self.cache:
            self.cache[path] = json.load(open(path, encoding="utf-8"))
        return self.cache[path]

    def __call__(self, path, *keys, fmt=None):
        node = self._doc(path)
        trail = []
        for k in keys:
            trail.append(str(k))
            try:
                node = node[k]
            except (KeyError, IndexError, TypeError):
                raise FigureMissing(
                    "%s has no field %s - the field was renamed or the file is not the one this "
                    "build expects. No figure is guessed and no default is substituted."
                    % (os.path.basename(path), ".".join(trail)))
        value = fmt(node) if fmt else node
        self.log.append({"file": os.path.basename(path), "field": ".".join(str(k) for k in keys),
                         "raw": node, "rendered": str(value)})
        return value


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def snapshot(d):
    """Every file under d, relative, sorted - membership, not contents."""
    out = []
    for root, dirs, files in os.walk(d):
        for f in files:
            out.append(os.path.relpath(os.path.join(root, f), d))
    return sorted(out)


def run(cmd, cwd, why, log, env=None):
    """Run a command. NOTHING here sets PYTHONDONTWRITEBYTECODE - see the module docstring."""
    t0 = time.time()
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       env=env if env is not None else dict(os.environ))
    rec = {"cmd": " ".join(cmd), "why": why, "returncode": p.returncode,
           "seconds": round(time.time() - t0, 1),
           "stdout_tail": p.stdout[-600:], "stderr_tail": p.stderr[-600:]}
    log.append(rec)
    if p.returncode != 0:
        raise SystemExit("BUILD FAILED: %s exited %d\n%s\n%s"
                         % (" ".join(cmd), p.returncode, p.stdout[-2000:], p.stderr[-2000:]))
    return p


def _refuse_if_a_probe_is_in_flight(log):
    """Deviation D25's standing rule, made a mechanism instead of a sentence.

    Session 127 wrote it down after its validation builds put a second client of this practice on
    the same endpoint while the day's panel probe was running: *a live build of the delivery
    object is not run while a panel probe is in flight.* Session 128 then broke that rule sixteen
    times in ninety minutes (D26), because a rule in a markdown file does not stop a build.

    So the build asks the ledger, not the builder, and there is deliberately NO override flag —
    an escape hatch is how the rule became advisory in the first place. `window_status.py` already
    distinguishes a partial being written by a live reservation from one that was abandoned, and
    it is the file both the letter and this check read.
    """
    d = tempfile.mkdtemp(prefix="inflight-")
    tmp = os.path.join(d, "scan.json")
    try:
        p = subprocess.run(["python3", "window_status.py", tmp], cwd=HERE,
                           capture_output=True, text=True)
        if p.returncode != 0 or not os.path.exists(tmp):
            raise SystemExit("BUILD REFUSED: could not read the ledger's in-flight state, and a "
                             "build that cannot tell whether a probe is running does not run "
                             "the live command.\n" + p.stderr[-800:])
        scan = json.load(open(tmp, encoding="utf-8"))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    if scan.get("n_in_flight"):
        raise SystemExit(
            "BUILD REFUSED: a panel probe is in flight (%s). This build runs the receiver-list "
            "command live, twice, and would put a second client of this practice on the same "
            "endpoint from the same vantage while the day is being measured. Deviation D25 set "
            "that rule and D26 records this build breaking it sixteen times before it became a "
            "check. There is no override; wait for the run file to close."
            % ", ".join(f["file"] for f in scan.get("in_flight", [])))
    log.append({"check": "no panel probe in flight (D25's rule, enforced by the ledger)",
                "n_in_flight": 0, "ok": True})


def _check_quote(log):
    """The receiver's own words, checked against the report text before they are printed.

    The eighth review's most serious single finding was that the letter stated this receiver's
    selection criterion backwards. A quotation of a named third party in a document addressed to
    them is checked mechanically here, against the extracted report in this directory, with
    whitespace normalised because the extraction is from a PDF.
    """
    text = " ".join(open(RECEIVER_REPORT, encoding="utf-8").read().split())
    want = " ".join(RECEIVER_QUOTE.split())
    if want not in text:
        raise FigureMissing(
            "the receiver's own words this letter quotes are not in the extracted report text. "
            "The quotation is not printed on this practice's memory of it.")
    log.append({"check": "receiver quotation found verbatim in " + os.path.basename(
        RECEIVER_REPORT), "ok": True})
    # and their own dashboard's note, likewise
    dash = open(DASH, encoding="utf-8").read()
    if " ".join(DASH_NOTE.split()) not in " ".join(dash.split()):
        raise FigureMissing("the dashboard note this letter quotes is not in the saved bytes.")
    log.append({"check": "dashboard note found verbatim in " + os.path.basename(DASH),
                "ok": True})


def _confirmation_record(out, log):
    """Item 4: computed here, from the sidecars, and its coverage checked against the ledger."""
    dst = os.path.join(out, "confirmation-record.json")
    run(["python3", "confirmation_record_121.py", "-o", dst], HERE,
        "item 4: the confirmation record is computed by this build, not read from a file whose "
        "date the build never checks", log)
    rec = json.load(open(dst, encoding="utf-8"))
    read = sorted(os.path.basename(p) for p in rec["sources"]["sidecars"])
    on_disk = sorted(os.path.basename(p)
                     for p in glob.glob(os.path.join(HERE, "ledger",
                                                     "transition-confirm-*.json")))
    if read != on_disk:
        raise FigureMissing(
            "the confirmation record covers %d sidecars and the ledger holds %d. Missing from "
            "the record: %s. A record that silently omits a day is the defect this check "
            "exists for." % (len(read), len(on_disk), sorted(set(on_disk) - set(read))))
    log.append({"check": "confirmation record coverage", "sidecars_read": len(read),
                "sidecars_on_disk": len(on_disk), "ok": True,
                "newest_sidecar": on_disk[-1]})
    return dst


def _readings_history(today_path):
    """Every dated reading this practice has taken of these eleven identifiers, compared.

    Three now. One morning is one morning; three mornings across eight days are three mornings.
    """
    readings = []
    prior = json.load(open(PRIOR_ELEVEN, encoding="utf-8"))
    r0 = prior["readings"][0]
    day = r0["started_utc"][:10]
    readings.append({"started_utc": r0["started_utc"], "vantage_asn": r0["vantage_asn"],
                     "states": {u["vid"]: u["states"][day] for u in prior["units"]},
                     "source": os.path.relpath(PRIOR_ELEVEN, HERE)})
    for p in (PRIOR_ELEVEN_2, today_path):
        d = json.load(open(p, encoding="utf-8"))
        readings.append({"started_utc": d["started_utc"], "vantage_asn": d["vantage"]["asn"],
                         "states": {o["vid"]: o["state"] for o in d["observations"]},
                         "source": os.path.relpath(p, HERE)})
    readings.sort(key=lambda r: r["started_utc"])
    ids = sorted(set().union(*[set(r["states"]) for r in readings]))
    changed = []
    for v in ids:
        seq = [r["states"].get(v) for r in readings]
        if len(set(seq)) > 1:
            changed.append({"vid": v, "sequence": seq})
    always_absent = [v for v in ids
                     if all(r["states"].get(v) == "NOT-RETRIEVABLE" for r in readings)]
    return {
        "n_readings": len(readings),
        "dates": [r["started_utc"] for r in readings],
        "vantages": sorted(set(r["vantage_asn"] for r in readings)),
        "n_identifiers": len(ids),
        "n_changed_state_across_readings": len(changed),
        "changed": changed,
        "not_retrievable_on_every_reading": always_absent,
        "what_this_is_not": ("three readings are three readings. They do not establish a rate, a "
                             "trend, or that anything is permanently gone."),
        "readings": [{"started_utc": r["started_utc"], "vantage_asn": r["vantage_asn"],
                      "source": r["source"]} for r in readings],
    }


def _rewrap(text, width=94):
    """Re-wrap prose so the raw file reads evenly; fences, tables, headings pass through."""
    out, fence = [], False
    for para in text.split("\n\n"):
        if para.strip().startswith("```") or fence:
            out.append(para)
            fence = fence != (para.count("```") % 2 == 1)
            continue
        lines = para.split("\n")
        if any(l.lstrip().startswith(("|", "#", ">", "-", "*")) for l in lines):
            out.append(para)
            continue
        words, cur, buf = " ".join(para.split()).split(" "), 0, []
        line = []
        for w in words:
            if cur + len(w) + (1 if line else 0) > width and line:
                buf.append(" ".join(line))
                line, cur = [w], len(w)
            else:
                line.append(w)
                cur += len(w) + (1 if len(line) > 1 else 0)
        if line:
            buf.append(" ".join(line))
        out.append("\n".join(buf))
    return "\n\n".join(out)


def words(text):
    """Prose words a reader reads: fenced blocks and table rows excluded, counted not typed."""
    n, fence = 0, False
    for line in text.split("\n"):
        if line.strip().startswith("```"):
            fence = not fence
            continue
        if fence or line.strip().startswith("|"):
            continue
        n += len(line.split())
    return n


def cmd_block(i):
    return "```sh\n" + " ".join(CMDS[i]) + "\n```"


def fenced_commands(text):
    out, fence, buf = [], False, []
    for line in text.split("\n"):
        if line.strip().startswith("```"):
            if fence:
                out.append(" ".join(" ".join(buf).split()))
                buf = []
            fence = not fence
            continue
        if fence:
            buf.append(line)
    return out


def render(fx, out, F, C, S, R, hist, dash_hashes):
    """The letter. Every number comes through fx(); none is typed."""
    n = fx(F, "record", "n_videos")
    flip = fx(F, "simultaneous_flip", "date")
    n_flip = fx(F, "simultaneous_flip", "n_series_whose_last_change_is_that_date")
    from_na = fx(F, "simultaneous_flip", "states_they_came_from", "Not Available")
    from_av = fx(F, "simultaneous_flip", "states_they_came_from", "Available")
    went_to = fx(F, "simultaneous_flip", "state_they_went_to", 0)
    last_date = fx(F, "record", "last_date")
    first_date = fx(F, "record", "first_date")
    gap_days = fx(F, "simultaneous_flip", "days_from_flip_to_record_end")
    since = fx(F, "record", "days_from_record_end_to_our_reading")
    since_flip = fx(F, "simultaneous_flip", "days_from_flip_to_our_reading")
    n_gaps = fx(F, "record", "gaps_in_the_record", fmt=len)
    outlier = fx(F, "the_one_that_is_not_like_the_others", "video_id")
    outlier_av = fx(F, "the_one_that_is_not_like_the_others", "available_days")
    outlier_n = fx(F, "the_one_that_is_not_like_the_others", "n_recorded_days")
    err_final = fx(F, "record", "final_status_counts", "Error")

    n_retr = fx(F, "against_our_own_reading", "n_retrievable_in_our_reading")
    read_utc = fx(C, "started_utc")
    asn = fx(C, "vantage", "asn")
    endpoint = fx(C, "probe", "endpoint")
    passes = fx(C, "confirmation", "passes")
    n_unconf = fx(C, "n_unconfirmed_absent")
    # Every bucket the run produced, not the two the letter expects: the dry run of this build
    # returned one INDETERMINATE and the sentence silently dropped it, so 9 + 1 did not make 11.
    buckets = fx(C, "counts")
    GLOSS = {"RETRIEVABLE": "publicly retrievable",
             "NOT-RETRIEVABLE": "not retrievable, and still not after %d re-requests" % passes,
             "INDETERMINATE": ("indeterminate - a transport failure, which is evidence of "
                               "nothing either way"),
             "UNCONFIRMED-ABSENT": ("refused once and not on re-request, so excluded from both "
                                    "parts of the rate")}
    if sum(buckets.values()) + n_unconf != n and sum(buckets.values()) != n:
        raise FigureMissing("the run's buckets sum to %d over %d identifiers; the letter would "
                            "print arithmetic that does not close."
                            % (sum(buckets.values()), n))
    rest = "; ".join("%d %s" % (v, GLOSS[k]) for k, v in sorted(buckets.items())
                     if k != "RETRIEVABLE" and v)

    day_lo = fx(F, "scoring_the_handed_over_breakdown", "day_range_found", 0)
    day_hi = fx(F, "scoring_the_handed_over_breakdown", "day_range_found", 1)
    n_group = fx(F, "scoring_the_handed_over_breakdown", "n_videos_found")
    n_group_retr = fx(F, "scoring_the_handed_over_breakdown",
                      "n_retrievable_now_in_that_group")
    n_cmp = fx(F, "extraction_checked_against_the_pages_own_aggregate_chart", "n_comparisons")
    n_dis = fx(F, "extraction_checked_against_the_pages_own_aggregate_chart", "n_disagreements")

    ret_conf = fx(R, "genuine_transitions_only", "NOT-RETRIEVABLE->RETRIEVABLE", "confirmed")
    ret_n = fx(R, "genuine_transitions_only", "NOT-RETRIEVABLE->RETRIEVABLE", "n")
    los_conf = fx(R, "genuine_transitions_only", "RETRIEVABLE->NOT-RETRIEVABLE", "confirmed")
    los_n = fx(R, "genuine_transitions_only", "RETRIEVABLE->NOT-RETRIEVABLE", "n")

    days_measured = fx(S, "n_measurement_days")
    holes = fx(S, "n_holes")
    # the calendar span is not a field, so it is DERIVED from fetched fields rather than typed
    d0 = fx(S, "measurement_days", 0, "start_utc")
    d1 = fx(S, "measurement_days", days_measured - 1, "start_utc")
    days_cal = (datetime.date.fromisoformat(d1[:10])
                - datetime.date.fromisoformat(d0[:10])).days + 1

    n_readings = hist["n_readings"]
    n_changed = hist["n_changed_state_across_readings"]

    t = []
    A = t.append

    A("# All %d series on your dashboard changed to %s on %s, and it has recorded nothing "
      "since %s" % (n_flip, went_to, flip, last_date))
    A("")
    A("*A machine research practice measured and wrote this; %s publishes it and answers for "
      "it. Nobody has been contacted and it has not been sent. Full note at the end.*"
      % PERSON)
    A("")
    A("## What your own dashboard's data says")
    A("")
    A("*%s*, published by %s (%s), says: *\"%s.\"* The dashboard it points to now tracks %d, "
      "and we read it this morning at `%s`. Its bytes are identical to the copies we saved on "
      "two earlier days, so nothing below turns on a stale capture."
      % (RECEIVER_REPORT_TITLE, RECEIVER_ORG, RECEIVER_REPORT_ID, RECEIVER_QUOTE, n, DASH_URL))
    A("")
    A("The page carries %d per-video timelines that its summary tiles do not show. Read out of "
      "those bytes, they say this:" % n)
    A("")
    A("- **Every one of the %d series changes state for the last time on %s** - %d from *Not "
      "Available* and %d from *Available*, all to *%s*, and none of them changes again."
      % (n_flip, flip, from_na, from_av, went_to))
    A("- **The record stops %d days later, on %s**, and has not moved in the %d days since."
      % (gap_days, last_date, since))
    A("- The tiles a visitor sees - %d with errors, none available - therefore describe **%s**, "
      "not today. Your page does print `Dashboard generated on: %s`, in its footer; the tiles "
      "themselves carry no date." % (err_final, last_date, last_date))
    A("- One of the %d, `%s`, had been recorded *Available* on %d of its %d days. The %s flip "
      "took that one too." % (n, outlier, outlier_av, outlier_n, flip))
    A("")
    A("**This is your record, not our reading of it**: the page draws its own summary chart "
      "from a separate payload, and summing the %d timelines reproduces that chart "
      "exactly - %d comparisons, %d disagreements." % (n, n_cmp, n_dis))
    A("")
    A("Independently checked videos do not all change state on one day. That is the signature "
      "of the thing doing the checking, and your own page already says so in its own words: "
      "*\"%s\"* **What is new here is the date.**" % DASH_NOTE)
    A("")
    A("We have not seen the code behind it and are not saying what broke - only that whatever "
      "it was, it happened on %s." % flip)
    A("")
    A("## What we measured ourselves, this morning")
    A("")
    A("The command below ran at **%s**, from autonomous system **%s**, through the platform's "
      "public oEmbed endpoint (`%s`) - no account, no research credential, one request per "
      "identifier and **%d immediate re-requests of every refusal** before believing it:"
      % (read_utc, asn, endpoint, passes))
    A("")
    A("> **%d of your %d were publicly retrievable.** The rest: %s."
      % (buckets.get("RETRIEVABLE", 0), n, rest if rest else "nothing else"))
    A("")
    A("Your record has %d of the %d as *Not Available* on between %d and %d of their recorded "
      "days - **and %d of those %d answered a public request this morning.** This is the third "
      "dated reading we "
      "have taken of these identifiers (%s); %d of the %d changed state across the three."
      % (n_group, n, day_lo, day_hi, n_group_retr, n_group,
         ", ".join(d[:10] for d in hist["dates"]), n_changed, n))
    A("")
    A("## What this cannot tell you")
    A("")
    A("- **A reading in August does not characterise a state recorded in January.** The %d days "
      "between are not assumed to be quiet: over its own short life our daily series has seen "
      "%d of %d apparent returns from absence survive re-requesting, and %d of %d apparent "
      "losses. Retrievability moves in both directions, and this letter reads one morning."
      % (since_flip, ret_conf, ret_n, los_conf, los_n))
    A("- **It cannot show that your errors are not a real gap in the research interface.** A "
      "video can be publicly fetchable *and* genuinely absent from that interface. Our "
      "measurement cannot separate a broken checking path from a genuine gap, and therefore "
      "cannot attribute your failures away from one.")
    A("- **It cannot tell you a video was deleted.** The endpoint answers every kind of absence "
      "with one opaque code; an identifier that never existed returns the same one. *Not "
      "retrievable* means only that, from this vantage, at that moment.")
    A("- **Your %d were not chosen by us**, and they are not a sample of anything." % n)
    A("")
    A("## Check all of it yourself")
    A("")
    A("**Everything the headline rests on is in this directory** - your dashboard's bytes, the "
      "extractor, the derivation - and no step needs our cooperation. Every command below was "
      "run by this letter's own build, here; the %d that need no network were run again from a "
      "copy made outside our repository, in a clean environment. If any had failed, this "
      "letter would not exist. **Two figures are not reproducible "
      "here**: the re-request counts and our series' length come from a daily ledger that is "
      "not in this directory. Both files name their sources, and that ledger is public in the "
      "repository named below." % len(OFFLINE))
    A("")
    A("The first three read your dashboard's own bytes and need no network:")
    A("")
    A(cmd_block(0))
    A(cmd_block(1))
    A(cmd_block(2))
    A("")
    A("The third of them reads the measurement shipped here; run the last command below and it "
      "writes your own in its place. Those last two are the instrument and its measurement, "
      "and the second makes requests:")
    A("")
    A(cmd_block(3))
    A(cmd_block(4))
    A("")
    A("Point the probe at your own list by replacing `receiver-list.txt` with one identifier "
      "per line. It sends no credential and keeps no identifier of yours - but **as printed it "
      "does disclose this machine's IP address** to a third-party lookup service, because "
      "`--vantage` defaults to recording which network the reading was taken from. "
      "`--vantage none` turns that off and the tool prints what it did either way.")
    A("")
    A("## The instrument this comes from")
    A("")
    A("A credential-free probe of a fixed panel, aimed at the same hour every day and reported "
      "from its own ledger: **%d measurement days across %d calendar days**, with **%d** day "
      "started and abandoned and therefore not counted. A started run is not a run, and "
      "`consecutive_daily` is **false** in our own status file." % (days_measured, days_cal,
                                                                   holes))
    A("")
    A("## Terms, and who answers for this")
    A("")
    A("Written and measured by **Meridian**, an autonomous research practice: a machine did "
      "the measuring, the writing and the checking. **%s - %s - publishes it and carries "
      "responsibility for it.** The "
      "whole record, including every review this object and its predecessors failed, is public "
      "at `%s`. Nobody named here has been contacted; whether this is ever sent is his "
      "decision, not this practice's." % (PERSON, PERSON_URL, REPO_URL))
    A("")
    A("**Version %s of this object, built %s.** If you use a figure from here, please carry "
      "the sentence it depends on - that is a request, not a condition on you, and the full "
      "set is `memory/downstream-commitments.md` in the repository above. Corrections and "
      "disputes have a route: open an issue there - a correction becomes a new dated entry, "
      "never a silent edit. Data CC0 1.0, code Apache 2.0, text CC BY 4.0."
      % (OBJECT_VERSION, read_utc))
    A("")
    A("## What is in this directory")
    A("")
    A("| file | what it is |")
    A("|---|---|")
    for name in sorted(os.listdir(out)):
        if name not in DESCRIPTIONS:
            raise FigureMissing("%s is in the object and has no entry in DESCRIPTIONS; the "
                                "inventory would be false as printed." % name)
        A("| `%s` | %s |" % (name, DESCRIPTIONS[name]))
    missing = sorted(set(DESCRIPTIONS) - set(os.listdir(out)) - {"LETTER.md", "BUILD.json"})
    if missing:
        raise FigureMissing("DESCRIPTIONS names files that are not in the object: %s" % missing)
    return _rewrap("\n".join(t))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="letter")
    a = ap.parse_args(argv)
    out = os.path.join(HERE, a.out)
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    log = []
    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    _refuse_if_a_probe_is_in_flight(log)
    _check_quote(log)

    # --- the object's files, copied, and the copies asserted byte-identical -------------------
    copied = {}
    for src, name in ([(os.path.join(TOOLDIR, f), f) for f in
                       ("presence_check.py", "selftest_presence_check.py", "ledger.py",
                        "run_lock.py", "drift-122.json")]
                      + [(DASH, os.path.basename(DASH)),
                         (LIST_SRC, "receiver-list.txt"),
                         (os.path.join(HERE, "extract_dashboard.py"), "extract_dashboard.py"),
                         (os.path.join(HERE, "dashboard_findings.py"),
                          "dashboard_findings.py")]):
        dst = os.path.join(out, name)
        shutil.copy(src, dst)
        if sha256(src) != sha256(dst):
            raise SystemExit("copy of %s is not byte-identical to its source" % name)
        copied[name] = {"from": os.path.relpath(src, HERE), "sha256": sha256(dst),
                        "is_the_live_file": True}
    log.append({"check": "every shipped file is byte-identical to its live source",
                "n_files": len(copied), "ok": True})

    # the daily series' own status, computed from the ledger
    run(["python3", "window_status.py", os.path.join(out, "series-status.json")], HERE,
        "the series' length and holes, computed from the ledger rather than described", log)

    # item 4
    rec_path = _confirmation_record(out, log)

    # --- phase A: run every command, in dependency order --------------------------------------
    for i in ORDER_A:
        run(CMDS[i], out, "phase A: produce the figures the letter quotes", log)

    F = os.path.join(out, "dashboard-findings.json")
    C = os.path.join(out, "your-eleven-today.json")
    S = os.path.join(out, "series-status.json")

    hist = _readings_history(C)
    dash_hashes = {os.path.basename(p): sha256(p) for p in [DASH] + DASH_PRIOR}
    if len(set(dash_hashes.values())) != 1:
        raise FigureMissing("the three saved reads of the dashboard are not byte-identical; the "
                            "letter's sentence about that is false and must be rewritten: %s"
                            % dash_hashes)
    log.append({"check": "three dated reads of the dashboard are byte-identical",
                "sha256": sorted(set(dash_hashes.values()))[0], "reads": sorted(dash_hashes),
                "ok": True})

    fx = Fx()
    text = render(fx, out, F, C, S, rec_path, hist, dash_hashes)

    # --- phase E: the length condition, enforced ----------------------------------------------
    n_words = words(text)
    if n_words > WORD_CEILING:
        raise SystemExit("BUILD FAILED: the letter is %d prose words against a ceiling of %d. "
                         "The previous object measured this and asserted it against nothing, "
                         "and two of three strangers stopped reading before the end."
                         % (n_words, WORD_CEILING))
    log.append({"check": "letter length", "prose_words": n_words, "ceiling": WORD_CEILING,
                "ok": True})

    open(os.path.join(out, "LETTER.md"), "w", encoding="utf-8").write(text + "\n")

    # --- phase C: the letter's own commands, re-extracted and re-run --------------------------
    printed = fenced_commands(open(os.path.join(out, "LETTER.md"), encoding="utf-8").read())
    declared = [" ".join(c) for c in CMDS]
    if sorted(printed) != sorted(declared):
        raise SystemExit("BUILD FAILED: the letter prints commands this build did not run, or "
                         "omits ones it did.\nprinted:  %s\ndeclared: %s" % (printed, declared))
    log.append({"check": "the set of commands the letter prints equals the set the build ran",
                "n": len(printed), "ok": True})
    phase_c = tempfile.mkdtemp(prefix="phaseC-")
    try:
        for f in os.listdir(out):
            shutil.copy(os.path.join(out, f), phase_c)
        for c in printed:
            run(c.split(), phase_c, "phase C: run what the letter prints, as printed, from "
                "scratch", log)
    finally:
        shutil.rmtree(phase_c)

    # --- phase D: from a copy outside this repository, in a clean environment ------------------
    parent = tempfile.mkdtemp(prefix="phaseD-")
    d = os.path.join(parent, "letter")
    try:
        shutil.copytree(out, d)
        before = snapshot(d)
        env = {k: v for k, v in os.environ.items() if k != "PYTHONDONTWRITEBYTECODE"}
        for c in OFFLINE:
            run(c, d, "phase D: the offline commands, from a copy outside this repository, "
                "with PYTHONDONTWRITEBYTECODE removed from the environment", log, env=env)
        after = snapshot(d)
        added = sorted(set(after) - set(before))
        if added:
            raise SystemExit(
                "BUILD FAILED: running this object's own instructions in a clean copy ADDED "
                "files to it: %s. This is erratum E23. A guard that passes only because the "
                "build sets PYTHONDONTWRITEBYTECODE is true of the builder's machine and false "
                "of the reader's." % added)
        log.append({"check": "a reader's copy is unchanged in membership after running the "
                             "printed offline commands, with no bytecode variable set",
                    "files_before": len(before), "files_after": len(after), "ok": True})
    finally:
        shutil.rmtree(parent)

    # --- BUILD.json ----------------------------------------------------------------------------
    files = sorted(os.listdir(out))
    build = {
        "schema": "field-research/letter-build/1",
        "built_by": "build_letter.py, session 128, 2026-08-20",
        "object_version": OBJECT_VERSION,
        "started_utc": started,
        "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "conditions_this_build_is_bound_by": "CONDITIONS-127.md, items 1-7",
        "never_sets_pythondontwritebytecode": True,
        "prose_words": n_words,
        "word_ceiling": WORD_CEILING,
        "commands": [" ".join(c) for c in CMDS],
        "log": log,
        "figures_fetched": fx.log,
        "shipped_files_are_live_copies": copied,
        "dashboard_reads": dash_hashes,
        "dashboard_url": DASH_URL,
        "readings_history": hist,
        "files": [{"name": f, "sha256": sha256(os.path.join(out, f)),
                   "bytes": os.path.getsize(os.path.join(out, f))}
                  for f in files if f != "BUILD.json"],
    }
    with open(os.path.join(out, "BUILD.json"), "w", encoding="utf-8") as f:
        json.dump(build, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("built %s: %d files, %d prose words (ceiling %d), %d commands run %d times"
          % (a.out, len(os.listdir(out)), n_words, WORD_CEILING, len(CMDS),
             len([r for r in log if "cmd" in r])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
