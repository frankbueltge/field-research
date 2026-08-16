#!/usr/bin/env python3
"""selftest_run_lock - the lock is shown refusing, on the shape of the accident it exists for.

Session 124, 2026-08-16. A guard nobody has watched fail is a guard nobody should trust, and this
arc has already published one assertion that "passes identically whether the constant was computed
or typed" (ERRATA-122.md, E9). So every case below constructs the state on disk and calls the real
`acquire()`; nothing here asserts a constant against a literal.

Run: python3 selftest_run_lock.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

import run_lock

PASS, FAIL = [], []


def check(name, ok, detail=""):
    (PASS if ok else FAIL).append(name)
    print(("  ok   " if ok else "  FAIL ") + name + (f"  [{detail}]" if detail else ""))


def refuses(fn):
    try:
        fn()
    except run_lock.RunRefused as e:
        return str(e)
    return None


def main():
    root = tempfile.mkdtemp(prefix="runlock-")
    led = os.path.join(root, "ledger")
    os.makedirs(led)
    man = os.path.join(root, "manifest.json")
    json.dump({"units": [{"vid": "1", "handle": "h", "arm": "A"}], "arms": {}}, open(man, "w"))
    other = os.path.join(root, "manifest-other.json")
    json.dump({"units": [{"vid": "2", "handle": "h", "arm": "A"}], "arms": {}}, open(other, "w"))
    out = os.path.join(led, "run-today.json")
    day = time.strftime("%Y-%m-%d", time.gmtime())
    # The lock file is named for the manifest and day it guards, so the selftest writes and reads
    # locks at the same per-manifest path acquire() uses.
    lp = run_lock._lock_path(led, run_lock.manifest_fingerprint(man), day)

    print("a clean day")
    st = run_lock.acquire(man, out, ledger_dir=led)
    check("a first run on a clean day is allowed", st["utc_day"] == day)
    check("it leaves a lock naming this process",
          json.load(open(lp))["pid"] == os.getpid())

    print("\nthe accident of 2026-08-16: a second probe while the first is in flight")
    # A lock held by a process that really exists and is not this one.
    helper = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
    try:
        json.dump({"pid": helper.pid, "utc_day": day,
                   "manifest_fingerprint": run_lock.manifest_fingerprint(man),
                   "manifest": man, "out_path": out, "started_utc": "x"},
                  open(lp, "w"))
        why = refuses(lambda: run_lock.acquire(man, out, ledger_dir=led))
        check("a live lock over the same manifest and day REFUSES the start", bool(why))
        check("the refusal names the holding process", bool(why) and str(helper.pid) in why)
        check("the refusal points at the record of why this exists",
              bool(why) and "DOUBLE-PROBE-122" in why)

        # A different manifest is a different measurement and must not be blocked.
        st2 = run_lock.acquire(other, os.path.join(led, "run-other.json"), ledger_dir=led)
        check("a DIFFERENT manifest is not blocked by that lock", st2["utc_day"] == day)
    finally:
        helper.terminate()
        helper.wait()

    print("\na dead holder is a stale lock, not a run in flight")
    json.dump({"pid": helper.pid, "utc_day": day,
               "manifest_fingerprint": run_lock.manifest_fingerprint(man),
               "manifest": man, "out_path": out, "started_utc": "x"},
              open(lp, "w"))
    st3 = run_lock.acquire(man, out, ledger_dir=led)
    check("a lock whose holder is gone is taken over", "stale_lock_taken_over" in st3)
    check("and the takeover is recorded, not silent",
          st3["stale_lock_taken_over"]["pid"] == helper.pid)

    print("\nthe signal the handover teaches sessions to ignore")
    os.remove(lp)
    part = out + ".partial"
    json.dump({"partial": True, "requested": 700}, open(part, "w"))
    why = refuses(lambda: run_lock.acquire(man, out, ledger_dir=led))
    check("a FRESH .partial refuses the start", bool(why), "a partial is a sign of life")
    check("the refusal states how far the run in flight has got",
          bool(why) and "700" in why)
    old = time.time() - run_lock.PARTIAL_FRESH_S - 60
    os.utime(part, (old, old))
    st4 = run_lock.acquire(man, out, ledger_dir=led)
    check("a STALE .partial does not refuse", st4["fresh_partials_today"] == [])
    os.remove(part)

    print("\na day already measured is not measured again by accident")
    os.remove(lp)
    json.dump({"schema": "x", "run_utc_start": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "requested": 3869, "observations": []}, open(out, "w"))
    why = refuses(lambda: run_lock.acquire(man, out, ledger_dir=led))
    check("a complete run for the same day REFUSES the start", bool(why))
    check("the refusal names the run that already exists", bool(why) and "3869" in why)

    print("\na deliberate replicate is possible, and must be declared twice")
    why = refuses(lambda: run_lock.acquire(man, out, ledger_dir=led, replicate=True))
    check("--replicate alone is refused when the path does not declare it", bool(why))
    check("the refusal says what the path must carry",
          bool(why) and run_lock.REPLICATE_MARK in why)
    rep = os.path.join(led, "run-today-second-probe.json")
    st5 = run_lock.acquire(man, rep, ledger_dir=led, replicate=True)
    check("--replicate plus a declaring path is allowed", st5["declared_replicate"] is True)
    check("and the run it allows still records what it stepped over",
          bool(st5["complete_runs_today"]))

    print("\nthe reservation that would have stopped the real accident")
    # The 2026-08-16 accident: a run scheduled and held, a second session opening DURING the hold,
    # seeing nothing, and launching. A reservation taken before the hold is a live lock during it.
    for f in (lp, out, out + ".partial"):
        if os.path.exists(f):
            os.remove(f)
    reserving = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
    try:
        # The reserving process writes the lock naming itself, then (in reality) sleeps.
        json.dump({"pid": reserving.pid, "utc_day": day,
                   "manifest_fingerprint": run_lock.manifest_fingerprint(man),
                   "manifest": man, "out_path": out, "started_utc": "reserved"},
                  open(lp, "w"))
        why = refuses(lambda: run_lock.acquire(man, out, ledger_dir=led))
        check("a second session opening DURING a held reservation is refused", bool(why),
              "the case the accident needed")
    finally:
        reserving.terminate()
        reserving.wait()
    # And the reserving process itself, on wake, takes over its OWN reservation rather than
    # refusing it. Simulated by writing a lock naming THIS process, then acquiring.
    json.dump({"pid": os.getpid(), "utc_day": day,
               "manifest_fingerprint": run_lock.manifest_fingerprint(man),
               "manifest": man, "out_path": out, "started_utc": "reserved"},
              open(lp, "w"))
    st6 = run_lock.acquire(man, out, ledger_dir=led)
    check("the reserver takes over its own reservation on wake", "took_over_own_reservation" in st6)

    print("\ntwo probes starting in the same instant — only one may win")
    # The Interlocutor's blocking objection: two sessions firing at the identical scheduled second,
    # both passing the pre-scan before either writes. The lock is created with O_CREAT|O_EXCL, so of
    # N real processes racing to acquire the SAME manifest+day with no prior lock, exactly one
    # proceeds and the rest raise RunRefused. Run it for real with a barrier, not asserted.
    for f in (lp, out, out + ".partial"):
        if os.path.exists(f):
            os.remove(f)
    racer = (
        "import sys, json, time, os\n"
        "sys.path.insert(0, %r)\n"
        "import run_lock\n"
        "man, out, led, barrier = sys.argv[1:5]\n"
        "while not os.path.exists(barrier):\n"
        "    time.sleep(0.005)\n"                       # all racers block on the barrier file
        "try:\n"
        "    run_lock.acquire(man, out, ledger_dir=led)\n"
        "    print('WON'); time.sleep(2)\n"             # winner holds the lock briefly
        "except run_lock.RunRefused:\n"
        "    print('REFUSED')\n"
        % os.path.dirname(os.path.abspath(run_lock.__file__))
    )
    barrier = os.path.join(root, "go")
    procs = [subprocess.Popen([sys.executable, "-c", racer, man,
                               os.path.join(led, "run-%d.json" % i), led, barrier],
                              stdout=subprocess.PIPE, text=True) for i in range(6)]
    open(barrier, "w").close()                          # release all six at once
    outs = [p.communicate()[0].strip() for p in procs]
    wins = outs.count("WON")
    check("exactly one of six simultaneous starters wins the atomic lock", wins == 1,
          f"{wins} won, {outs.count('REFUSED')} refused")
    # clean every run file and lock the racers left, so the release test starts from nothing
    for n in os.listdir(led):
        os.remove(os.path.join(led, n))

    print("\nthe lock is released by its holder and only by its holder")
    st_rel = run_lock.acquire(man, os.path.join(led, "run-rel.json"), ledger_dir=led)
    check("the holder releases it", bool(st_rel) and run_lock.release(led) is True)
    json.dump({"pid": 1, "utc_day": day, "manifest_fingerprint": "x"},
              open(lp, "w"))
    check("a non-holder does not remove someone else's lock", run_lock.release(led) is False)

    print("\nthe builder's half of the same accident")
    # The bundle ships this selftest beside run_lock.py but NOT the builder (build_deliverable.py
    # is a working-tree script, not a receiver artifact). So this cross-check runs where the
    # builder is importable and is skipped, out loud, where it is not — a skip stated is not a
    # pass claimed.
    try:
        import build_deliverable
        check("the builder names the replicate mark it recognises",
              build_deliverable.REPLICATE_MARK == run_lock.REPLICATE_MARK,
              f"{build_deliverable.REPLICATE_MARK!r}")
    except ImportError:
        print("  skip build_deliverable not importable here (the bundle ships the lock, not the "
              "builder)")

    shutil.rmtree(root)
    print(f"\n{len(PASS)} passed, {len(FAIL)} failed")
    if FAIL:
        for f in FAIL:
            print("  FAILED:", f)
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
