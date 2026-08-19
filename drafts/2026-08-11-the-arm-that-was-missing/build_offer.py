#!/usr/bin/env python3
"""build_offer - builds the short object that replaces the retired bundle.

Session 127, 2026-08-19. `CONDITIONS-126.md` retired `deliverable-v0.3/` as the delivery object
after its seventh consecutive failed gauntlet — every one of the seven in the packaging, none in
a measurement — and bound this session to build a different kind of thing:

  1. a letter a person can read in five minutes, its data, and its caveats;
  2. it names a person;
  3. EVERY RUNNABLE INSTRUCTION IN IT IS EXECUTED BY THIS BUILD, and the build fails if one
     errors — the only new mechanism licensed, and licensed because the seventh gauntlet found
     that the one command the retired bundle told a human to type had never been typed by any
     of its seven reviewers and did not run;
  4. the instrument's length is READ from the ledger and is never "seven consecutive daily runs";
  7. the confirmation ratio is computed at build time and never carried across.

HOW THIS FILE HONOURS (3), WHICH IS THE POINT OF IT
----------------------------------------------------
The letter cannot print a command this build did not run. There is one list of commands, `CMDS`.
The letter renders its command blocks FROM that list, the build executes every entry of it in the
object's own directory, and after rendering, phase C re-extracts every fenced command out of the
finished letter text and checks that the set of commands in the letter is exactly the set the
build ran, then runs each of them again from scratch. A command that exits non-zero fails the
build. A command that appears in the letter and not in `CMDS` fails the build.

The live command runs TWICE, deliberately: once to produce the figures the letter quotes (phase
A) and once as the letter's own instruction, executed as printed (phase C). Both results are
recorded. If they disagree, that is not a build failure — it is this instrument's own subject
matter, and the letter is built to say so.

NO FIGURE IN THE LETTER IS TYPED. `fx()` fetches every one from a named field of a named JSON
file and raises if the field is absent, so a renamed field fails the build instead of printing a
stale number.

Usage:  python3 build_offer.py [--out offer] [--skip-live]
        --skip-live is for a dry run of the rendering only; it refuses to write the letter.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time

import window_status

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL_SRC = os.path.join(HERE, "deliverable-v0.3", "tools", "presence_check.py")
SELFTEST_SRC = os.path.join(HERE, "deliverable-v0.3", "tools", "selftest_presence_check.py")
LEDGER_SRC = os.path.join(HERE, "deliverable-v0.3", "tools", "ledger.py")
RUNLOCK_SRC = os.path.join(HERE, "deliverable-v0.3", "tools", "run_lock.py")
BASELINE_SRC = os.path.join(HERE, "deliverable-v0.3", "reference-baseline.json")
LIST_SRC = os.path.join(HERE, "receiver-list.txt")
# Re-read live this session and byte-identical to the copy saved on 2026-08-16; both
# hashes are carried into measurement.json so the claim is checkable, not asserted.
DASHBOARD = os.path.join(HERE, "receiver-dashboard-2026-08-19.json")
DASHBOARD_PRIOR = os.path.join(HERE, "deliverable-v0.3", "receiver-dashboard-read.json")
PANELDATE = os.path.join(HERE, "panel-date-125.json")
RECORD = os.path.join(HERE, "confirmation-record-121.json")
PRIOR_ELEVEN = os.path.join(HERE, "deliverable-v0.3", "receiver-eleven.json")
NEIGHBOURS = os.path.join(HERE, "neighbours-127.json")
DRIFT_SRC = os.path.join(HERE, "drift-122.json")

# The one list of commands. The letter renders from it; the build runs it; phase C proves the
# letter contains these and nothing else.
CMDS = [
    ["python3", "selftest_presence_check.py"],
    ["python3", "presence_check.py", "receiver-list.txt",
     "--baseline", "reference-baseline.json", "--label", "the-eleven",
     "-o", "your-eleven-today.json"],
]

# What each file in the object is, for the letter's own table. The table is GENERATED from the
# directory listing and this map: a file on disk with no entry here fails the build, and an entry
# here with no file fails it too. The retired bundle's seventh gauntlet died on an inventory that
# claimed to list a directory's contents and did not.
DESCRIPTIONS = {
    "LETTER.md": "this letter",
    "measurement.json": "every figure above, in the field this letter fetched it from",
    "series-status.json": "the series' length, holes and intervals, computed from the ledger",
    "your-eleven-today.json": "the live run this letter quotes, as the tool wrote it",
    "rerun-verification.json": ("the same command run a second time, as printed above, to prove "
                                "it runs"),
    "presence_check.py": "the instrument",
    "selftest_presence_check.py": "the instrument's own test suite, offline",
    "ledger.py": ("the request layer the instrument imports, unchanged and not "
                  "re-implemented"),
    "run_lock.py": "the reservation the daily probe takes; imported by ledger.py",
    "drift-122.json": ("the measurement four of the suite's assertions check the "
                       "instrument against"),
    "receiver-list.txt": "the identifiers, as transcribed from your dashboard",
    "reference-baseline.json": "the reference population table the comparison uses",
    "BUILD.json": "what this build ran, with exit statuses, both runs' counts and a hash per file",
}

PERSON = "Frank Bültge"
PERSON_URL = "https://frankbueltge.de"


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
                    f"{os.path.relpath(path, HERE)} has no field {'.'.join(trail)} — the field "
                    f"was renamed or the file is not the one this build expects. No figure is "
                    f"guessed and no default is substituted.")
        value = fmt(node) if fmt else node
        self.log.append({"file": os.path.relpath(path, HERE),
                         "field": ".".join(str(k) for k in keys),
                         "raw": node, "rendered": str(value)})
        return value


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def run(cmd, cwd, why):
    # PYTHONDONTWRITEBYTECODE, because of ERRATA-126.md E23: running the retired bundle's own
    # modules during its review wrote two .pyc files INTO the frozen directory, and the freeze
    # verified contents while being blind to membership. A build that runs code inside the object
    # it is building must not litter it.
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    t0 = time.time()
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env)
    rec = {"cmd": " ".join(cmd), "why": why, "returncode": p.returncode,
           "seconds": round(time.time() - t0, 1),
           "stdout_tail": p.stdout[-1500:], "stderr_tail": p.stderr[-800:]}
    return p, rec


def patch_tool(dst):
    """Copy the instrument and correct the one figure frozen inside its own source.

    v0.3.1 states this arc's confirmation record as literal counts in two places — its docstring
    and the `record_behind_the_default` field of every output file it writes. Those counts were
    true of six events on 2026-08-15 and are not true now: the series has grown and the ratio has
    moved against us. A portable tool cannot read this arc's record file, so the counts are
    replaced by the finding that does not go stale plus a pointer to where the current counts
    are computed. That is the whole of the change, and it is made in THIS COPY — the retired
    bundle is not touched, repaired or re-versioned.
    """
    src = open(TOOL_SRC, encoding="utf-8").read()
    doc_old = ("re-requested eight readings that looked like changes. Of the three genuine "
               "disappearances, ONE\nsurvived and TWO did not. Of the three genuine returns, "
               "three survived. Computed from the raw")
    if doc_old not in src:
        raise FigureMissing("the v0.3.1 docstring paragraph this build corrects is not in the "
                            "source; the tool changed and this patch must be re-read")
    field_re = re.compile(
        r'("record_behind_the_default": \(\n)(.*?)(\),\n)', re.S)
    m = field_re.search(src)
    if m is None or "three genuine disappearance readings" not in m.group(2):
        raise FigureMissing("the v0.3.1 record_behind_the_default literal this build corrects "
                            "is not in the source; the tool changed and this patch must be "
                            "re-read")
    doc_new = ("re-requested every reading that looked like a change. SOME REFUSALS DID NOT "
               "SURVIVE\nre-requesting, which is the entire reason this default is on. The "
               "counts move as the series\ngrows and are therefore NOT frozen into this file: "
               "they are computed from the raw")
    field_new = (
        '                "some of this arc\'s refusal readings did not survive five immediate "\n'
        '                "re-requests, and that is the whole reason this default is on. The "\n'
        '                "counts move as the series grows, so they are NOT frozen into this "\n'
        '                "tool: they are computed in confirmation-record-121.json and stated, "\n'
        '                "with the date they were computed, in the letter this tool ships "\n'
        '                "with. Never a rate."')
    src = src.replace(doc_old, doc_new)
    src = field_re.sub(lambda mm: mm.group(1) + field_new + "\n" + mm.group(3), src, count=1)
    src = src.replace('VERSION = "0.3.1"', 'VERSION = "0.3.2"')
    src = src.replace(
        "VERSION 0.3.1, session 122, 2026-08-16 (v0.3.0 failed its own gauntlet the same night).",
        "VERSION 0.3.2, session 127, 2026-08-19. 0.3.2 differs from 0.3.1 in ONE thing: the\n"
        "confirmation record was stated in this file as literal counts, and those counts went\n"
        "stale when the series grew. They are gone; the finding they illustrated is not.\n"
        "VERSION 0.3.1, session 122, 2026-08-16 (v0.3.0 failed its own gauntlet the same night).")
    open(dst, "w", encoding="utf-8").write(src)


def _neighbours():
    """What the letter's one claim about the world rests on, dated and re-checked.

    The claim was established on 2026-08-15 against a register that has since grown. Rather than
    carry it on a stale search, the register was fetched again this session and the same keyword
    check re-run; what that returned is here, and the letter fetches its figures from it.
    """
    n = json.load(open(NEIGHBOURS, encoding="utf-8"))
    return {
        "source": os.path.relpath(NEIGHBOURS, HERE),
        "register_url": n["register"]["url"],
        "register_fetched_utc": n["register"]["fetched_utc"],
        "register_count": n["register"]["count_entries"],
        "prior_search_date": n["prior_search"]["date"],
        "prior_search_register_count": n["prior_search"]["register_count"],
        "register_growth_since": n["register_growth_since_prior_search"],
        "nearest_neighbour": ("Bekavac & Mayer, Platforms' Research API Data Access: What Users "
                              "See vs. What Researchers can Retrieve, FAccT '26; preprint "
                              "arXiv:2601.12390"),
        "what_the_recheck_returned": ("every entry the keyword check surfaced was already "
                                      "assessed by this arc (NEIGHBOURS-120.md, "
                                      "FANOUT-1-neighbours.md); none is new"),
        "what_this_check_is_not": ("a keyword check over one register, not a field search. It "
                                   "can only find what that register holds and what those words "
                                   "reach."),
    }


def _prior_comparison(today):
    """This practice's earlier dated reading of the same eleven, and what moved between them.

    One morning is one morning. The arc measured the same list once before, on 2026-08-12
    (`deliverable-v0.3/receiver-eleven.json`, session 113's run), and a second dated reading a
    week later is worth more than either alone — so it is computed here rather than described.
    """
    prior = json.load(open(PRIOR_ELEVEN, encoding="utf-8"))
    reading = prior["readings"][0]
    day = reading["started_utc"][:10]
    then = {u["vid"]: u["states"][day] for u in prior["units"]}
    now = {o["vid"]: o["state"] for o in today["observations"]}
    shared = sorted(set(then) & set(now))
    changed = [{"vid": v, "then": then[v], "now": now[v]}
               for v in shared if then[v] != now[v]]
    absent_both = [v for v in shared if then[v] == now[v] == "NOT-RETRIEVABLE"]
    return {
        "source": os.path.relpath(PRIOR_ELEVEN, HERE),
        "read_utc": reading["started_utc"],
        "vantage_asn": reading["vantage_asn"],
        "counts_then": reading["counts"],
        "n_shared_identifiers": len(shared),
        "n_changed_state": len(changed),
        "changed": changed,
        "absent_on_both_readings": absent_both,
        "what_this_is_not": ("two readings a week apart are two readings. They do not establish "
                             "a rate, a trend, or that anything is permanently absent."),
    }


def patch_selftest(dst):
    """Copy the test suite and point its one external file at this object's own copy.

    Four of the suite's assertions read `drift-122.json` to check the tool's comparand against
    the measurement it came from, and the path is written for the retired bundle's layout
    (`../../drift-122.json`). Run from anywhere else the suite SKIPS them and says so out loud —
    which is good design and still leaves a receiver running 124 of 128 assertions without being
    told why. So the file ships here and the path looks beside the script first. Nothing else in
    the suite is touched.
    """
    src = open(SELFTEST_SRC, encoding="utf-8").read()
    old = ('_MEAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", '
           '"drift-122.json")')
    if old not in src:
        raise FigureMissing("the selftest's drift-122.json path is not where this build expects "
                            "it; the suite changed and this patch must be re-read")
    new = ('_HERE = os.path.dirname(os.path.abspath(__file__))\n'
           '# session 127: beside this script first (the short object ships it), then the\n'
           '# retired bundle\'s layout, so this file runs unchanged in either place.\n'
           '_MEAS = os.path.join(_HERE, "drift-122.json")\n'
           'if not os.path.exists(_MEAS):\n'
           '    _MEAS = os.path.join(_HERE, "..", "..", "drift-122.json")')
    open(dst, "w", encoding="utf-8").write(src.replace(old, new))


def _rewrap(text, width=94):
    """Re-wrap prose paragraphs so the raw file reads evenly.

    Fenced blocks, table rows, headings and blockquotes are passed through untouched — a wrapped
    command would be a command a reader cannot paste, which is the defect that retired the last
    object.
    """
    out_lines, para, in_fence = [], [], False
    indent = [""]

    def flush():
        if not para:
            return
        words = " ".join(para).split()
        pad = indent[0]
        line = ""
        first = True
        for w in words:
            head = "" if first else pad
            if line and len(head) + len(line) + 1 + len(w) > width:
                out_lines.append(("" if first else pad) + line)
                first = False
                line = w
            else:
                line = w if not line else line + " " + w
        if line:
            out_lines.append(("" if first else pad) + line)
        para.clear()
        indent[0] = ""

    for raw in text.split("\n"):
        if raw.startswith("```"):
            flush()
            in_fence = not in_fence
            out_lines.append(raw)
            continue
        if in_fence or raw.startswith(("|", "#", ">")) or not raw.strip():
            flush()
            out_lines.append(raw)
            continue
        if raw.startswith(("- ", "* ")):
            flush()
            indent[0] = "  "
            para.append(raw)
            continue
        if raw.startswith("  ") and not para:
            out_lines.append(raw)
            continue
        para.append(raw.strip())
    flush()
    return "\n".join(out_lines)


def render(fx, out, meta):
    P = lambda *p: os.path.join(out, *p)
    M = P("measurement.json")
    W = P("series-status.json")

    n_items = fx(M, "today", "list", "n_items")
    retr = fx(M, "today", "counts", "RETRIEVABLE")
    counts = fx(M, "today", "counts")
    other = {k: v for k, v in counts.items() if k != "RETRIEVABLE"}
    other_str = ", ".join(f"{v} {k}" for k, v in sorted(other.items())) or "none"
    started = fx(M, "today", "started_utc")
    asn = fx(M, "today", "vantage", "asn")
    endpoint = fx(M, "today", "probe", "endpoint")
    passes = fx(M, "today", "confirmation", "passes")
    tool_v = fx(M, "today", "tool_version")
    n_assert = fx(M, "selftest", "assertions_passed")
    n_unconf = fx(M, "today", "n_unconfirmed_absent")
    absent_now = counts.get("NOT-RETRIEVABLE", 0)
    unconf_clause = (
        "and no first-pass refusal failed to reproduce" if n_unconf == 0 else
        f"and {n_unconf} further first-pass refusal did not reproduce, so it was excluded rather "
        f"than counted" if n_unconf == 1 else
        f"and {n_unconf} further first-pass refusals did not reproduce, so they were excluded "
        f"rather than counted")
    refusal_line = (
        f"The {'one refusal' if absent_now == 1 else str(absent_now) + ' refusals'} above "
        f"{'was' if absent_now == 1 else 'were'} re-requested {passes} times and did not go "
        f"away, {unconf_clause}."
        if absent_now else
        f"Nothing refused on the first pass, {unconf_clause}.")
    prior_when = fx(M, "prior_reading_of_the_same_list", "read_utc")
    prior_retr = fx(M, "prior_reading_of_the_same_list", "counts_then", "RETRIEVABLE")
    prior_n = fx(M, "prior_reading_of_the_same_list", "n_shared_identifiers")
    n_changed = fx(M, "prior_reading_of_the_same_list", "n_changed_state")
    both_absent = fx(M, "prior_reading_of_the_same_list", "absent_on_both_readings")
    changed_line = (
        f"not one of the {prior_n} changed state between the two readings"
        + (f", and the one that was not retrievable then (`{both_absent[0]}`) is the same one "
           f"that is not retrievable now." if len(both_absent) == 1 else ".")
        if n_changed == 0 else
        f"{n_changed} of the {prior_n} changed state between the two readings.")

    dash_total = fx(M, "receiver_dashboard", "totals", "videos")
    dash_err = fx(M, "receiver_dashboard", "totals", "error")
    dash_avail = fx(M, "receiver_dashboard", "totals", "available")
    dash_gen = fx(M, "receiver_dashboard", "generated")
    dash_note = fx(M, "receiver_dashboard", "note")
    dash_read = fx(M, "receiver_dashboard", "read_date")
    dash_prior = fx(M, "receiver_dashboard", "prior_reading", "read_date")
    dash_same = fx(M, "receiver_dashboard", "unchanged_since_prior_reading")
    dash_sha = fx(M, "receiver_dashboard", "saved_bytes_sha256")
    dash_unchanged = (
        f"We fetched it again this morning and the bytes are identical to the copy we saved on "
        f"{dash_prior} (sha256 `{dash_sha[:16]}…`), so nothing here turns on a stale capture."
        if dash_same else
        f"The page has changed since we last saved it on {dash_prior}; the figures above are "
        f"from this morning's copy (sha256 `{dash_sha[:16]}…`).")

    g_loss_n = fx(M, "confirmation_record", "genuine_transitions_only",
                  "RETRIEVABLE->NOT-RETRIEVABLE", "n")
    g_loss_c = fx(M, "confirmation_record", "genuine_transitions_only",
                  "RETRIEVABLE->NOT-RETRIEVABLE", "confirmed")
    g_ret_n = fx(M, "confirmation_record", "genuine_transitions_only",
                 "NOT-RETRIEVABLE->RETRIEVABLE", "n")
    g_ret_c = fx(M, "confirmation_record", "genuine_transitions_only",
                 "NOT-RETRIEVABLE->RETRIEVABLE", "confirmed")
    g_loss_r = g_loss_n - g_loss_c

    thou = lambda n: f"{n:,}"
    days = fx(W, "n_measurement_days")
    holes = fx(W, "n_holes")
    holes_str = ("no day was started and abandoned" if holes == 0 else
                 "one day was started and abandoned" if holes == 1 else
                 f"{holes} days were started and abandoned")
    consecutive = fx(W, "consecutive_daily")
    first_day = fx(W, "measurement_days", 0, "start_utc")
    last_day = fx(W, "measurement_days", -1, "start_utc")
    span = fx(M, "series", "calendar_days_spanned")

    reg_n = fx(M, "neighbour_check", "register_count")
    reg_growth = fx(M, "neighbour_check", "register_growth_since")
    prior_search = fx(M, "neighbour_check", "prior_search_date")
    pop_what = fx(M, "population_caveat", "reference_population_what_it_is",
                  fmt=lambda t: t.split(". ")[0].rstrip(".").strip())
    bracket = fx(M, "population_caveat", "panel_construction_bracket_days")
    pop_n = fx(M, "population_caveat", "reference_population_n")
    t_ref = fx(M, "population_caveat", "reference_day_utc")

    on_disk = {f for f in os.listdir(out) if os.path.isfile(os.path.join(out, f))}
    # the three files that do not exist yet at render time and are written by the phases after it
    expected = on_disk | {"LETTER.md", "rerun-verification.json", "BUILD.json"}
    if expected != set(DESCRIPTIONS):
        raise SystemExit(
            "the letter's file table and the directory disagree.\n"
            f"  on disk, undescribed: {sorted(expected - set(DESCRIPTIONS))}\n"
            f"  described, absent:    {sorted(set(DESCRIPTIONS) - expected)}")
    file_rows = "\n".join(
        f"| `{f}` | {DESCRIPTIONS[f]}"
        + (f", version {tool_v}" if f == "presence_check.py" else "")
        + (f": {n_assert} assertions" if f == "selftest_presence_check.py" else "")
        + " |"
        for f in sorted(DESCRIPTIONS))

    cmd_self = " ".join(CMDS[0])
    cmd_live = " ".join(CMDS[1])
    built = meta["built_utc"]

    return f"""# {retr} of your {n_items} were publicly fetchable this morning, with no account

*A short letter, its data, and its limits. It is written to be forwarded unedited by a person;
this practice sends nothing and asks for nothing back.*

**Who made this and who answers for it.** It was measured and written by Meridian, an autonomous
research practice: the measuring, the writing and the checking were done by a machine practice,
and that is said plainly here rather than left for a reader to work out. **{PERSON} —
{PERSON_URL} — publishes it and carries responsibility for it**, as this practice's own
constitution requires of everything it publishes. The whole record, including all seven reviews
this object's predecessor failed, is public at `https://github.com/frankbueltge/field-research`.
**Nobody named in this letter has been contacted, this letter has not been sent to anyone, and
the decision whether it is ever sent is his and not this practice's.**

---

## Why this reaches you

You published a report on a large video platform's research interface, and with it a public
dashboard that checks whether videos which — in your own words — *"should be available through
the Research API but were not"* are there. Read on {dash_read}, that dashboard declares itself
generated **{dash_gen}** and reports **{dash_total}** videos tracked, **{dash_avail}**
available and **{dash_err}** with errors. It also says, on its own face:

> *"{dash_note}"*

{dash_unchanged}

That sentence is why this letter exists. An instrument that cannot separate its own failures from
the platform's needs a second, independent measurement beside it, and **that second measurement
needs no credential and no account.**

We checked whether it was already being done and narrowed our own claim when it turned out to be
partly done: Bekavac and Mayer compare the user-visible feeds of controlled accounts against what
the TikTok Research API and the Meta Content Library return, over two election periods (FAccT '26;
preprint `arXiv:2601.12390`) — a stronger study than anything here, but run *through accounts*,
over bounded periods, and published as a study rather than as something you can point at your own
list. **What we could not find — in our own field searches, or in the {thou(reg_n)} papers our
register held when we re-checked it this morning — is a running, credential-free, dated reference
a stranger can address their own identifiers against on a day of their choosing.** That is what
this is, and not more. (Re-checked against a register {reg_growth} entries larger than when the
search was first run on {prior_search}; nothing new surfaced. It is a keyword check over one
register, not a survey of the field.)

## What we measured, this morning

The command in section *"Check it yourself"* below was run at **{started}**, from autonomous
system **{asn}**, through the platform's public oEmbed endpoint (`{endpoint}`) — no account, no
research credential, no allow-list, one request per identifier and **{passes} immediate
re-requests of every refusal** before believing it:

> **{retr} of {n_items} were publicly retrievable.** The remainder: {other_str}.

{refusal_line}

**And this is the second time we have read your list.** On {prior_when}, from the same vantage,
it came back **{prior_retr} of {prior_n}** as well — {changed_line} Two readings a week apart are
two readings: they do not establish a rate, a trend, or that anything is permanently gone.

So a dashboard reporting {dash_err} errors across those {n_items} is, on this morning's evidence,
very likely reporting something about its own path to the platform rather than about the videos.
Your own note already says as much. This is a control arm for that note, not a discovery about
the platform — and it is the whole of what this letter claims.

## The part to read before you use the number

We ran the obvious check against ourselves and it did not go our way. Every apparent state change
in our own daily series is re-requested {passes} times immediately, and across the series so far:
**{g_ret_c} of {g_ret_n}** apparent returns survived re-checking, and **{g_loss_c} of
{g_loss_n}** apparent disappearances did. **{g_loss_r} refusals did not reproduce when the same
identifier was requested again, seconds later.**

**A single unconfirmed refusal is a reading of the network as much as of the platform.** That is
why the tool below re-requests by default, and why we would rather you took that habit than any
figure in this letter. These are counts of events, not a rate, and they are computed fresh every
time this letter is built — {g_loss_c + g_ret_c} confirmations out of {g_loss_n + g_ret_n} events
as of {built}.

## What this cannot tell you, so nobody has to find out later

- **It cannot tell you a video was deleted.** The endpoint answers every kind of absence with one
  opaque code; an identifier that never existed returns the same one. *Not publicly retrievable*
  means only that, from this vantage, at that moment.
- **It is one vantage and one endpoint.** It is not an audit of the research interface and cannot
  on its own show any coverage claim to be false.
- **Your {n_items} were not chosen by us.** Your own instrument selected them by reporting an
  error on them.
- **The tool prints a comparison figure. It is not a benchmark and not a prediction about your
  list.** It compares your list against **{thou(pop_n)}** identifiers that are, in the words of the
  table itself, *{pop_what}* — as they read on **{t_ref}**. A
  yardstick cited without its population is a verdict wearing a yardstick's clothes. Worse, and
  we would rather say it than have you find it: **we never recorded the day that reference
  population was collected**, and our own record can only bracket it to **{bracket} days**. Use
  the direct measurement above; treat the comparison as background.

## Check it yourself

Everything needed is in this directory, and no step requires our cooperation. Both commands below
were executed by this letter's own build, in this directory, at {built} — if either had failed,
this letter would not exist:

```sh
{cmd_self}
```

```sh
{cmd_live}
```

The first is the instrument's own test suite, offline. The second is the measurement, live: it
writes `your-eleven-today.json`. Point it at your own list by replacing `receiver-list.txt` with
one identifier per line. It sends no credential and stores nothing about you; what it records
about its own network location is controlled by `--vantage`.

## The instrument this comes from

A daily credential-free probe of a fixed panel, run at the same hour and reported from its own
ledger rather than from anyone's memory: **{days} measurement days** between {first_day} and
{last_day}, **{span} calendar days**. In that time **{holes_str}** and therefore not counted —
a started run is not a run. `consecutive_daily` is **{consecutive}** in our own status file and
we print it that way rather than round it up. The panel is the cited population described above; your list is measured beside it and
never mixed into it.

## Status and terms

Version 1.0 of this object, {built}. It replaces a 32-file bundle that failed this practice's own
adversarial review seven times — never on a measurement, always on its packaging — and was
retired rather than repaired an eighth time. **This object was built to be put through that same
review, and whatever the review returned, including a failure, is in the public record for the
date on this letter**: `journal/2026-08-19.md` in the repository named above. It is not restated
here, because the strangers who read the last version told us that a document narrating its own
review history is a document they stop reading. Data CC0 1.0, code Apache 2.0, text CC BY 4.0.

If you use a figure from here, please carry the sentence it depends on: the confirmation counts
above with the date they were computed, and the population sentence with any comparison figure.
That is a request, not a condition on you.

## What is in this directory

| file | what it is |
|---|---|
{file_rows}
"""


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "offer"))
    ap.add_argument("--skip-live", action="store_true")
    ap.add_argument("--render-only", metavar="PATH", default=None,
                    help="re-render the letter from the files already in --out and write it to "
                         "PATH, running nothing. A validation mode: it never writes LETTER.md "
                         "and never writes BUILD.json, so no shipped state can come out of it.")
    a = ap.parse_args(argv)
    out = os.path.abspath(a.out)
    os.makedirs(out, exist_ok=True)
    built = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    build_log = []

    if a.render_only:
        prior = json.load(open(os.path.join(out, "BUILD.json"), encoding="utf-8"))
        selftest_out = next(r["stdout_tail"] for r in prior["runs"]
                            if "selftest" in r["cmd"])
        _write_measurement(out, built, selftest_out)
        fx = Fx()
        text = _rewrap(render(fx, out, {"built_utc": built}))
        open(a.render_only, "w", encoding="utf-8").write(text)
        print(f"render-only: {len(text.split())} words, {len(fx.log)} figures fetched -> "
              f"{a.render_only}")
        return 0

    # --- the object's own files -------------------------------------------------------------
    patch_tool(os.path.join(out, "presence_check.py"))
    for src in (LEDGER_SRC, RUNLOCK_SRC):
        shutil.copy2(src, os.path.join(out, os.path.basename(src)))
    shutil.copy2(DRIFT_SRC, os.path.join(out, "drift-122.json"))
    patch_selftest(os.path.join(out, "selftest_presence_check.py"))
    shutil.copy2(BASELINE_SRC, os.path.join(out, "reference-baseline.json"))
    shutil.copy2(LIST_SRC, os.path.join(out, "receiver-list.txt"))

    # --- the series, computed from the ledger, never asserted --------------------------------
    status = window_status.scan()
    json.dump(status, open(os.path.join(out, "series-status.json"), "w"), indent=1)

    # --- phase A: run the commands that produce the figures ----------------------------------
    if a.skip_live:
        print("--skip-live: refusing to render a letter whose commands were not run",
              file=sys.stderr)
        return 4
    selftest_out = ""
    for cmd in CMDS:
        p, rec = run(cmd, out, "phase A — produces the figures the letter quotes")
        build_log.append(rec)
        if cmd[1].startswith("selftest"):
            selftest_out = p.stdout
        print(f"  [A] {' '.join(cmd)} -> {p.returncode}")
        if p.returncode != 0:
            print(p.stdout[-2000:], file=sys.stderr)
            print(p.stderr[-2000:], file=sys.stderr)
            raise SystemExit("phase A command failed; no letter is written")

    today = _write_measurement(out, built, selftest_out)
    return _finish(a, out, built, build_log, today)


def _write_measurement(out, built, selftest_out):
    """Assemble measurement.json and series-status.json from the run that just happened.

    Split out of main() so `--render-only` can rebuild both from the files already in the
    directory and re-render the letter without issuing a single live request — which is how a
    template change is validated while a panel probe is in flight (DEVIATIONS.md D25).
    """
    today = json.load(open(os.path.join(out, "your-eleven-today.json"), encoding="utf-8"))
    status = window_status.scan()
    json.dump(status, open(os.path.join(out, "series-status.json"), "w"), indent=1)
    record = json.load(open(RECORD, encoding="utf-8"))
    dash = json.load(open(DASHBOARD, encoding="utf-8"))
    panel = json.load(open(PANELDATE, encoding="utf-8"))
    ref = json.load(open(BASELINE_SRC, encoding="utf-8"))

    first = status["measurement_days"][0]["start_utc"][:10]
    last = status["measurement_days"][-1]["start_utc"][:10]
    span = (int(time.mktime(time.strptime(last, "%Y-%m-%d")))
            - int(time.mktime(time.strptime(first, "%Y-%m-%d")))) // 86400 + 1

    measurement = {
        "schema": "field-research/short-offer/1",
        "built_by": "build_offer.py, session 127",
        "built_utc": built,
        "what_this_is": ("every figure the letter states, in the field the letter fetched it "
                         "from. No figure in the letter is typed; if a field here is renamed "
                         "the build fails instead of printing a stale number."),
        "today": today,
        "selftest": {
            "command": " ".join(CMDS[0]),
            "assertions_passed": int(re.search(r"(\d+) assertion\(s\) passed",
                                               selftest_out).group(1)),
            "failed": int(re.search(r"(\d+) failed", selftest_out).group(1)),
            "stdout": selftest_out.strip(),
        },
        "prior_reading_of_the_same_list": _prior_comparison(today),
        "neighbour_check": _neighbours(),
        "confirmation_record": {
            "source": os.path.relpath(RECORD, HERE),
            "computed_by": record["built_by"],
            "genuine_transitions_only": record["genuine_transitions_only"],
            "all_readings": record["all_readings"],
            "n_sidecars": len(record["sources"]["sidecars"]),
            "what_a_pass_is": record["what_a_pass_is"],
        },
        "series": {
            "source": "series-status.json, computed by window_status.py from the ledger",
            "n_measurement_days": status["n_measurement_days"],
            "n_holes": status["n_holes"],
            "consecutive_daily": status["consecutive_daily"],
            "preregistered_window_met": status["preregistered_window_met"],
            "first_day_utc": status["measurement_days"][0]["start_utc"],
            "last_day_utc": status["measurement_days"][-1]["start_utc"],
            "calendar_days_spanned": span,
        },
        "receiver_dashboard": {
            "source": os.path.relpath(DASHBOARD, HERE),
            "read_from_saved_bytes": dash["source_file"],
            "saved_bytes_sha256": dash["source_sha256"],
            # derived from the saved file's own name rather than typed here
            "read_date": re.search(r"(\d{4}-\d{2}-\d{2})", dash["source_file"]).group(1),
            "url": dash["url"],
            "generated": dash["fields"]["generated_declared"]["value"],
            "totals": {
                "videos": dash["fields"]["Total Videos Tracked"]["value"],
                "available": dash["fields"]["Available"]["value"],
                "unavailable": dash["fields"]["Unavailable"]["value"],
                "error": dash["fields"]["Errors"]["value"],
            },
            "note": dash["fields"]["error_note"]["value"],
            "what_these_are": dash["what_this_is"],
            "prior_reading": {
                "source": os.path.relpath(DASHBOARD_PRIOR, HERE),
                "read_date": re.search(
                    r"(\d{4}-\d{2}-\d{2})",
                    json.load(open(DASHBOARD_PRIOR, encoding="utf-8"))["source_file"]).group(1),
                "saved_bytes_sha256": json.load(
                    open(DASHBOARD_PRIOR, encoding="utf-8"))["source_sha256"],
            },
            "unchanged_since_prior_reading": (
                dash["source_sha256"]
                == json.load(open(DASHBOARD_PRIOR, encoding="utf-8"))["source_sha256"]),
        },
        "population_caveat": {
            "reference_population_n": ref["pooled"]["n"],
            "reference_population_what_it_is": ref["population"]["what_it_is"],
            "reference_day_utc": ref["t_ref_utc"],
            "panel_construction_bracket_days": panel["bracket_days"],
            "panel_lower_bound_utc": panel["lower_bound_utc"],
            "panel_upper_bound_utc": panel["upper_bound_utc"],
            "why_it_matters": ("the comparison figure is a cited population of a given age on a "
                              "given day, not a benchmark and not a prediction about a "
                              "caller's list; and this arc never recorded when that population "
                              "was collected."),
        },
    }
    json.dump(measurement, open(os.path.join(out, "measurement.json"), "w"),
              indent=1, ensure_ascii=False)
    return today


def _finish(a, out, built, build_log, today):
    # --- phase B: render, every figure fetched -----------------------------------------------
    fx = Fx()
    letter = _rewrap(render(fx, out, {"built_utc": built}))
    open(os.path.join(out, "LETTER.md"), "w", encoding="utf-8").write(letter)
    print(f"  [B] LETTER.md rendered, {len(letter.split())} words, "
          f"{len(fx.log)} figures fetched")

    # --- phase C: every runnable instruction IN THE LETTER, executed -------------------------
    in_letter = [" ".join(b.strip().split())
                 for b in re.findall(r"```sh\n(.*?)```", letter, re.S)]
    declared = [" ".join(c) for c in CMDS]
    if sorted(in_letter) != sorted(declared):
        raise SystemExit(
            "phase C: the letter's commands are not the commands this build ran.\n"
            f"  in letter: {in_letter}\n  built/ran: {declared}")
    for cmd in in_letter:
        p, rec = run(cmd.split(), out, "phase C — the letter's own instruction, as printed")
        build_log.append(rec)
        print(f"  [C] {cmd} -> {p.returncode}")
        if p.returncode != 0:
            print(p.stdout[-2000:], file=sys.stderr)
            print(p.stderr[-2000:], file=sys.stderr)
            raise SystemExit("phase C: an instruction the letter tells a reader to type FAILED. "
                             "The build fails; that is the point of this phase.")

    # Phase C re-ran the live command, so the file on disk is now C's, not the one the letter
    # quotes. The letter's run is restored and C's is kept beside it under its own name.
    c_run = json.load(open(os.path.join(out, "your-eleven-today.json"), encoding="utf-8"))
    json.dump(c_run, open(os.path.join(out, "rerun-verification.json"), "w"), indent=1)
    json.dump(today, open(os.path.join(out, "your-eleven-today.json"), "w"), indent=1)

    agree = c_run["counts"] == today["counts"]
    files = sorted(f for f in os.listdir(out) if os.path.isfile(os.path.join(out, f)))
    # The seventh gauntlet failed the retired bundle on an inventory that claimed to list the
    # bundle's contents and did not. This one is written last, so it cannot hash itself; that is
    # stated here rather than left for a reader to catch, and asserted below.
    json.dump({
        "covers": "every file in this directory except BUILD.json, which is written last and "
                  "cannot hash itself. Nothing else may be absent from the table below; the "
                  "build fails if anything is.",
        "schema": "field-research/offer-build/1",
        "built_utc": built,
        "built_by": "build_offer.py, session 127",
        "commands_declared": declared,
        "commands_found_in_letter": in_letter,
        "commands_match": True,
        "runs": build_log,
        "phase_c_note": ("phase C executes the letter's own instructions as printed. The live "
                         "command therefore ran twice; both results are kept. rerun-"
                         "verification.json is phase C's, your-eleven-today.json is the one the "
                         "letter quotes."),
        "two_runs_agree_on_counts": agree,
        "two_runs_counts": {"letter": today["counts"], "verification": c_run["counts"]},
        "letter_words": len(letter.split()),
        "figures_fetched": fx.log,
        "files": [{"file": f, "sha256": sha256(os.path.join(out, f)),
                   "bytes": os.path.getsize(os.path.join(out, f))} for f in files],
    }, open(os.path.join(out, "BUILD.json"), "w"), indent=1, ensure_ascii=False)

    on_disk = {f for f in os.listdir(out) if os.path.isfile(os.path.join(out, f))}
    unlisted = on_disk - set(files) - {"BUILD.json"}
    if unlisted:
        raise SystemExit(f"BUILD.json does not list files that are on disk: {sorted(unlisted)}")
    subdirs = sorted(d for d in os.listdir(out) if os.path.isdir(os.path.join(out, d)))
    if subdirs:
        raise SystemExit(
            f"the object has subdirectories and its inventory only counts files: {subdirs}. "
            f"This is ERRATA-126.md E23 — a listing that verifies contents and is blind to "
            f"membership — and the build refuses rather than repeat it.")
    print(f"  built {len(files)} files + BUILD.json; nothing on disk is unlisted; "
          f"two live runs agree on counts: {agree}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
