#!/usr/bin/env python3
"""run_lock - the probe refuses to start when a run for the same day is already happening.

Session 124, 2026-08-16. Deviation D23, BOOKKEEPING ONLY: no request of the probe changes, and
nothing here runs after the first measurement request has gone out.

WHY THIS EXISTS
---------------
On 2026-08-16 **two complete probes ran over the same manifest at the same hour**. Session 122
scheduled day 6 for 03:37:40Z and held a background job; session 123 opened a minute before that
second, could not see the held job, and launched the same probe. Both started at 03:37:40Z and
both finished. For 109 minutes the endpoint took **twice** this instrument's one-request-per-
second discipline from this house - about 7,738 requests where the pre-registration provides
3,869 (`DOUBLE-PROBE-122.md`).

Session 122's own landing note wrote the remedy and did not build it:

    *What is owed is a lock, not a note* - the probe must refuse to start when a run for the
    same manifest and UTC day is in flight.

A note was written. This is the lock. It is built one session later, before day 7, and the delay
is part of the record rather than an omission from it.

The accident also had a second cost nobody had noticed until tonight: the bundle builder
discovered both runs as separate *measurement days* with the same label, so `MANIFEST.json`
claimed seven measurement days over six days of measurement and one day's cells came from
whichever run was processed last. That half is fixed in `build_deliverable.py`. This half stops
the second run from happening at all.

WHAT COUNTS AS "ALREADY HAPPENING"
-----------------------------------
Three signals, checked against the same manifest fingerprint and the same UTC day. Any one of
them refuses the start:

1. **A live lock file** whose holding process still exists.
2. **A fresh `.partial` checkpoint** for that day. This is the signal that matters most, because
   it is the one the handover between sessions actively teaches a reader to ignore: *a partial
   file is never a run*. That is true of a partial as EVIDENCE and false of it as a SIGN OF LIFE,
   and the difference cost 3,869 requests.
3. **A complete run file** for that day. A day already measured is not measured again by
   accident.

WHAT IT CANNOT DO, STATED PLAINLY
----------------------------------
It is a lock on one filesystem. Two probes launched against two separate checkouts of this
repository cannot see each other, and this lock would not have stopped that. It stopped the case
that actually happened - both day-6 probes ran against this working tree - and it makes no claim
beyond that. Process liveness is checked with signal 0, which answers "does a process with this
pid exist", not "is it this probe"; on a machine that has recycled the pid the lock reads as live
and refuses, which is the safe direction.

And it can be overridden, because a deliberate replicate is a legitimate measurement: pass
`--replicate` AND write to a path carrying `-second-probe`. Both are required, so a replicate is
something a session declares in two places rather than something it falls into.

Two limits, stated because a guard whose gaps are a silence is worse than a smaller guard named
honestly:

- **One filesystem only.** Two probes launched against two separate checkouts of this repository
  cannot see each other's lock and this would not stop them. It stops the case that happened —
  both day-6 probes ran against this one working tree — and claims nothing past that.
- **Same-filesystem simultaneity is closed, not by check-then-write, but by an atomic create.**
  The lock is created with `O_CREAT | O_EXCL`, so of N processes racing to start the same
  manifest+day with no prior lock, exactly one create succeeds and the rest are refused. The
  earlier version of this note said this race was *not* closed; that was written before the atomic
  create existed and is corrected here. `selftest_run_lock.py` runs six real processes through a
  barrier and asserts exactly one wins. The reservation mechanism (`reserve()`, taken before a
  scheduled run holds) additionally removes the race for the scheduled case, by making the lock
  live through the whole hold rather than only from fire-time.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time

# The lock file is named for the manifest and the UTC day it guards, so two DIFFERENT manifests
# (or the same manifest on two days) get two different lock files and never contend for one path.
# A single shared lock name would make an atomic `O_EXCL` create collide across manifests, which
# is a correctness bug, not just an inconvenience — a run of manifest B would be refused because
# manifest A holds the one lock. `LOCK_NAME` is retained as the pattern prefix for discovery.
LOCK_NAME = ".run-lock.json"
LOCK_PREFIX = ".run-lock-"
REPLICATE_MARK = "-second-probe"


def _lock_path(ledger_dir, fp, day):
    return os.path.join(ledger_dir, f"{LOCK_PREFIX}{fp}-{day}.json")
# A `.partial` is written every 100 units, which at 1.0 s per unit is about every 100 seconds.
# Fifteen minutes is generous against that cadence and short enough that a checkpoint left by a
# run killed yesterday does not block today's.
PARTIAL_FRESH_S = 900


class RunRefused(Exception):
    """The probe must not start. Carries the reason, which is written into the record."""


def manifest_fingerprint(manifest_path):
    h = hashlib.sha256()
    with open(manifest_path, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()[:16]


def _alive(pid):
    try:
        os.kill(pid, 0)
    except (OSError, TypeError):
        return False
    return True


def _utc_day(t=None):
    return time.strftime("%Y-%m-%d", time.gmtime(t))


def _partial_own_day(path, d):
    """The day a checkpoint says IT belongs to, read from the run, not from the filesystem.

    Session 125, 2026-08-17, defect L1. The first real use of this lock refused a legitimate
    run because it read the day off `os.path.getmtime`. Every session of this practice starts
    from a fresh clone, the checkpoints are tracked files, and a checkout stamps them with the
    checkout time — so day 6's finished checkpoint presented as a run in flight for day 7,
    thirty-seven seconds old, minutes before day 7 was due. A run's day is a property of the
    run. `run_id` and `run_utc_start` are written by the probe; the filename is the next best
    witness; mtime is the last resort and is now only reached when the file says nothing.
    """
    for key in ("run_utc_start", "run_id"):
        v = d.get(key)
        if isinstance(v, str) and len(v) >= 10 and v[4] == "-" and v[7] == "-":
            return v[:10], key
    base = os.path.basename(path)
    if base.startswith("run-") and len(base) > 14 and base[8] == "-" and base[11] == "-":
        return base[4:14], "filename"
    return _utc_day(os.path.getmtime(path)), "mtime"


def _is_committed_state(path):
    """True when this file is byte-identical to the state the repository has committed.

    Session 125, defect L2, the other half of the same refusal. A tracked `.partial` restored
    by a checkout is fresh by mtime and was written by nobody. A checkout is not a probe. If
    git cannot answer — no repository, no git — this returns False, so the file keeps counting
    as a sign of life and the lock stays on its safe side.
    """
    try:
        r = subprocess.run(["git", "status", "--porcelain", "--", os.path.abspath(path)],
                           cwd=os.path.dirname(os.path.abspath(path)) or ".",
                           capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.SubprocessError):
        return False
    if r.returncode != 0:
        return False
    if r.stdout.strip():
        return False                      # modified or untracked: a process has touched it
    r2 = subprocess.run(["git", "ls-files", "--error-unmatch", "--", os.path.abspath(path)],
                        cwd=os.path.dirname(os.path.abspath(path)) or ".",
                        capture_output=True, text=True, timeout=15)
    return r2.returncode == 0             # clean AND tracked == exactly the committed bytes


def _scan_day(ledger_dir, day, fingerprint):
    """Complete runs and fresh partials for this day, over this manifest."""
    complete, fresh_partial = [], []
    if not os.path.isdir(ledger_dir):
        return complete, fresh_partial
    now = time.time()
    for n in sorted(os.listdir(ledger_dir)):
        p = os.path.join(ledger_dir, n)
        if n.endswith(".partial"):
            try:
                d = json.load(open(p))
            except (OSError, ValueError):
                continue
            own_day, day_source = _partial_own_day(p, d)
            # Three reasons a checkpoint is not a run in flight, each sufficient on its own and
            # each of which alone would have prevented session 125's false refusal:
            #   L1 the checkpoint says it belongs to another day;
            #   L3 the run it checkpoints has a completed file beside it — it finished;
            #   L2 the bytes are the committed ones, so a checkout wrote them, not a probe.
            if own_day != day:
                continue
            if os.path.exists(p[:-len(".partial")]):
                continue
            if now - os.path.getmtime(p) >= PARTIAL_FRESH_S:
                continue
            if _is_committed_state(p):
                continue
            fresh_partial.append({"file": p, "age_s": round(now - os.path.getmtime(p), 1),
                                  "requested": d.get("requested"),
                                  "day_read_from": day_source})
            continue
        if not n.endswith(".json"):
            continue
        try:
            d = json.load(open(p))
        except (OSError, ValueError):
            continue
        start = d.get("run_utc_start")
        if isinstance(start, str) and start[:10] == day and not d.get("partial"):
            complete.append({"file": p, "run_utc_start": start,
                             "requested": d.get("requested")})
    return complete, fresh_partial


def acquire(manifest_path, out_path, ledger_dir="ledger", replicate=False, now=None):
    """Refuse, or take the lock and return the record of what it saw.

    The returned dict is written into the run file, so a run always carries the state of the day
    it started into - including a stale lock it took over.
    """
    day = _utc_day(now)
    fp = manifest_fingerprint(manifest_path)
    lock_path = _lock_path(ledger_dir, fp, day)
    os.makedirs(ledger_dir, exist_ok=True)

    declared_replicate = replicate and REPLICATE_MARK in os.path.basename(out_path)
    if replicate and not declared_replicate:
        raise RunRefused(
            f"--replicate was given but the output path does not carry {REPLICATE_MARK!r}. "
            f"A deliberate second pass is declared in two places or it is not deliberate: "
            f"{out_path}")

    saw = {"utc_day": day, "manifest_fingerprint": fp, "declared_replicate": declared_replicate}

    # 1. a live lock
    held = None
    if os.path.exists(lock_path):
        try:
            held = json.load(open(lock_path))
        except (OSError, ValueError):
            held = {"unreadable": True}
        # Our OWN reservation. A window probe reserves the day before it sleeps to its hour, then
        # `exec`s into the measurement in the same process — same pid across the exec — so the
        # lock it wrote is the one it now finds. This is the case the 2026-08-16 accident needed
        # and did not have: the reservation is live through the whole hold, so a second session
        # opening during the hold sees a live lock and refuses. We take over our own reservation
        # rather than refuse it.
        if held.get("pid") == os.getpid() and held.get("manifest_fingerprint") == fp:
            saw["took_over_own_reservation"] = held
            held = None
        elif (held.get("utc_day") == day and held.get("manifest_fingerprint") == fp
                and _alive(held.get("pid"))):
            saw["blocked_by"] = {"kind": "live lock", "lock": held}
            if not declared_replicate:
                raise RunRefused(
                    f"a run over this manifest is already in flight for {day}: pid "
                    f"{held.get('pid')} started {held.get('started_utc')} writing "
                    f"{held.get('out_path')}. Two probes ran on 2026-08-16 because nothing said "
                    f"this; see DOUBLE-PROBE-122.md. If a second pass is intended, declare it: "
                    f"--replicate and an output path carrying {REPLICATE_MARK!r}.")
        elif held.get("utc_day") == day and held.get("manifest_fingerprint") == fp:
            saw["stale_lock_taken_over"] = held      # holder is gone; the run is not in flight

    # 2. a fresh partial, and 3. a complete run
    complete, fresh_partial = _scan_day(ledger_dir, day, fp)
    saw["complete_runs_today"] = complete
    saw["fresh_partials_today"] = fresh_partial
    if not declared_replicate:
        if fresh_partial:
            raise RunRefused(
                f"a checkpoint written {fresh_partial[0]['age_s']} s ago says a run is in flight "
                f"for {day} ({fresh_partial[0]['file']}, {fresh_partial[0]['requested']} units so "
                f"far). A partial file is never a run - and it is a sign of life, which is the "
                f"distinction that cost 3,869 requests on 2026-08-16.")
        if complete:
            raise RunRefused(
                f"{day} has already been measured over this manifest: {complete[0]['file']} "
                f"({complete[0]['requested']} units, started {complete[0]['run_utc_start']}). "
                f"Declare a replicate if a second pass is intended.")

    payload = json.dumps(
        {"pid": os.getpid(), "utc_day": day, "manifest_fingerprint": fp,
         "manifest": manifest_path, "out_path": out_path,
         "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)),
         "declared_replicate": declared_replicate,
         "what_this_is": ("held while a probe is running. If the holding process is gone this "
                          "file is stale and the next run takes it over and says so in its own "
                          "record.")}, indent=1)
    # Session 124's Interlocutor, blocking on the core claim: check-then-write with `open(w)` is
    # not atomic, so two probes that both pass the scan above in the same instant can both write
    # and both proceed — the same-second race the reservation narrows but does not, by itself,
    # close. The write is atomic here: `O_CREAT | O_EXCL` fails if the file already exists, so of
    # two simultaneous starters exactly one creates the lock and the other's create raises. The
    # loser re-reads the now-present lock and refuses unless it is a declared replicate or the
    # lock is its own reservation. This closes the one-filesystem race; two separate checkouts
    # still cannot see each other, as the module docstring states.
    while True:
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
            with os.fdopen(fd, "w") as f:
                f.write(payload)
            break
        except FileExistsError:
            try:
                other = json.load(open(lock_path))
            except (OSError, ValueError):
                other = {}
            mine = (other.get("pid") == os.getpid()
                    and other.get("manifest_fingerprint") == fp)
            stale = (other.get("manifest_fingerprint") == fp
                     and other.get("utc_day") == day and not _alive(other.get("pid")))
            if mine or stale or declared_replicate:
                # our own reservation, a dead holder, or a declared replicate: replace it and go.
                with open(lock_path, "w") as f:
                    f.write(payload)
                break
            saw["blocked_by"] = {"kind": "lost the atomic-create race", "lock": other}
            raise RunRefused(
                f"another probe created the lock for {day} at the same instant (pid "
                f"{other.get('pid')}). The atomic create went to it; this one stands down. "
                f"DOUBLE-PROBE-122.md.")
    saw["lock_path"] = lock_path
    return saw


def reserve(manifest_path, out_path, ledger_dir="ledger", now=None):
    """Take the lock for a day BEFORE sleeping to its hour, naming this process.

    A window probe that holds a long sleep and then measures must reserve the day at the moment
    it is scheduled, not at the moment it wakes — otherwise a second session opening during the
    hold sees nothing and launches its own probe, which is exactly the 2026-08-16 accident. The
    reserving process must be the one that survives the hold (so its pid stays valid): call this,
    sleep in the same process, then `exec`/run the measurement, which takes over its own
    reservation. `acquire()` still runs its full refusal checks — a reservation cannot be taken
    if a run for the day is already in flight or complete.
    """
    return acquire(manifest_path, out_path, ledger_dir=ledger_dir, now=now)


def _lock_files(ledger_dir):
    if not os.path.isdir(ledger_dir):
        return []
    return [os.path.join(ledger_dir, n) for n in sorted(os.listdir(ledger_dir))
            if n.startswith(LOCK_PREFIX) and n.endswith(".json")]


def release(ledger_dir="ledger"):
    """Drop every lock this process holds. Never removes another process's lock."""
    dropped = False
    for p in _lock_files(ledger_dir):
        try:
            held = json.load(open(p))
        except (OSError, ValueError):
            continue
        if held.get("pid") == os.getpid():
            os.remove(p)
            dropped = True
    return dropped


def main(argv):
    ap = argparse.ArgumentParser(description="inspect the run lock without starting a probe")
    ap.add_argument("manifest")
    ap.add_argument("--ledger-dir", default="ledger")
    a = ap.parse_args(argv)
    day, fp = _utc_day(), manifest_fingerprint(a.manifest)
    complete, partial = _scan_day(a.ledger_dir, day, fp)
    lock_path = _lock_path(a.ledger_dir, fp, day)
    held = None
    if os.path.exists(lock_path):
        try:
            held = json.load(open(lock_path))
        except (OSError, ValueError):
            held = {"unreadable": True}
    print(json.dumps({"utc_day": day, "manifest_fingerprint": fp,
                      "lock": held, "lock_holder_alive": _alive((held or {}).get("pid")),
                      "complete_runs_today": complete, "fresh_partials_today": partial,
                      "would_refuse": bool(held and _alive(held.get("pid"))) or bool(partial)
                                      or bool(complete)}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
