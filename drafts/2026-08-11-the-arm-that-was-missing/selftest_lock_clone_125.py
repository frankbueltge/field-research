#!/usr/bin/env python3
"""selftest_lock_clone_125 - the false refusal of 2026-08-17, and the control that must still fire.

Session 125. `selftest_run_lock.py` raced six real processes against each other and asserted that
exactly one wins. It never asked what the lock sees in a FRESH CLONE, which is how every session
of this practice begins. On 2026-08-17 the lock refused day 7 ninety seconds before it was due,
reporting day 6's finished checkpoint as "a run in flight, written 36.8 s ago". The checkpoint was
36.8 seconds old because `git checkout` had just written it.

Four cases. Three are the defect and must NOT refuse. The fourth is the control: the case the lock
exists for, which must STILL refuse - because a guard repaired into never refusing is worse than
the bug it replaced.

    L1  a checkpoint whose own run_id names an earlier day, mtime now
    L3  a checkpoint for today whose COMPLETED run file sits beside it
    L2  a checkpoint for today, fresh, byte-identical to its committed state (a checkout)
    C   a checkpoint for today, fresh, genuinely written by a process (untracked)

Run: python3 selftest_lock_clone_125.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_lock


def _git(repo, *args):
    return subprocess.run(("git",) + args, cwd=repo, capture_output=True, text=True)


def _write_partial(path, run_id, requested=3800):
    json.dump({"schema": "field-research/retrievability-ledger/1/partial", "partial": True,
               "run_id": run_id, "requested": requested, "planned": 3869, "observations": []},
              open(path, "w"))


def _write_complete(path, start):
    json.dump({"schema": "field-research/retrievability-ledger/1", "partial": False,
               "run_utc_start": start, "requested": 3869, "observations": []}, open(path, "w"))


def _case(repo, name, setup, expect_refusal, forbidden_reason=None):
    """Build a ledger dir inside a real git repo, then ask the lock whether it would refuse.

    `forbidden_reason` is for the case where a refusal is CORRECT but must come from the right
    signal. L3 is that case, and the first version of this test got it wrong: it asserted that a
    checkpoint with a completed run beside it must not refuse at all. It must — signal 3, "a day
    already measured is not measured again by accident" — and what must not happen is a refusal
    blaming the phantom checkpoint. The lock was right and the test was wrong; the test is
    corrected here rather than the lock, and this note is the record of which way that went.
    """
    ledger = os.path.join(repo, name)
    os.makedirs(ledger, exist_ok=True)
    manifest = os.path.join(ledger, "manifest.json")
    json.dump({"units": ["a", "b"]}, open(manifest, "w"))
    setup(ledger)
    # Commit whatever the setup marked as committed, so `_is_committed_state` has real bytes to
    # compare against. Files the setup leaves untracked stay untracked on purpose.
    _git(repo, "add", "--", ledger + "/committed") if os.path.isdir(ledger + "/committed") else None

    refused, reason = False, ""
    try:
        run_lock.acquire(manifest, os.path.join(ledger, "run-out.json"), ledger_dir=ledger)
    except run_lock.RunRefused as e:
        refused, reason = True, str(e)
    ok = refused == expect_refusal
    if ok and refused and forbidden_reason and forbidden_reason in reason:
        ok = False
        reason = "REFUSED FOR THE WRONG SIGNAL (" + forbidden_reason + "): " + reason
    print(("  PASS  " if ok else "  FAIL  ") + name
          + (" - refused: " + reason[:130] if refused else " - allowed the run"))
    return ok


def main():
    today = time.strftime("%Y-%m-%d", time.gmtime())
    yesterday = time.strftime("%Y-%m-%d", time.gmtime(time.time() - 86400))
    repo = tempfile.mkdtemp(prefix="lock-clone-125-")
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "selftest@field-research.local")
    _git(repo, "config", "user.name", "selftest")
    results = []

    # L1 - the exact 2026-08-17 case: yesterday's checkpoint, freshly stamped by a checkout.
    def l1(d):
        p = os.path.join(d, "run-%sT0337Z.json.partial" % yesterday)
        _write_partial(p, "%sT03:37:40Z" % yesterday)
        os.utime(p, None)                                  # as a checkout leaves it: now
    results.append(_case(repo, "L1-checkpoint-names-an-earlier-day", l1, expect_refusal=False))

    # L3 - today's checkpoint, but the run it checkpoints has finished and its file is beside it.
    # The checkpoint must stop counting as a sign of life; the COMPLETED run must still refuse.
    def l3(d):
        _write_partial(os.path.join(d, "run-%sT0337Z.json.partial" % today), "%sT03:37:40Z" % today)
        _write_complete(os.path.join(d, "run-%sT0337Z.json" % today), "%sT03:37:40Z" % today)
    # It MUST refuse - signal 3, the day is already measured - but never by blaming the checkpoint.
    results.append(_case(repo, "L3-completed-run-sits-beside-it", l3, expect_refusal=True,
                         forbidden_reason="is in flight"))

    # L2 - today's checkpoint, no completed file, fresh - but byte-identical to its committed
    # state, i.e. written by a checkout and by no process.
    def l2(d):
        p = os.path.join(d, "run-%sT0337Z.json.partial" % today)
        _write_partial(p, "%sT03:37:40Z" % today)
        _git(repo, "add", "-A")
        _git(repo, "commit", "-q", "-m", "committed checkpoint, as this repository really stores them")
        os.utime(p, None)                                  # the checkout's timestamp
    results.append(_case(repo, "L2-byte-identical-to-committed-state", l2, expect_refusal=False))

    # C - THE CONTROL. Today's checkpoint, fresh, and NOT the committed bytes: a real process is
    # writing it. This is the 2026-08-16 double probe, and the lock must still refuse it.
    def c(d):
        p = os.path.join(d, "run-%sT0337Z.json.partial" % today)
        _write_partial(p, "%sT03:37:40Z" % today, requested=1200)
    results.append(_case(repo, "C-CONTROL-live-run-must-still-be-refused", c, expect_refusal=True))

    shutil.rmtree(repo, ignore_errors=True)
    print("\n%d of %d cases as specified" % (sum(results), len(results)))
    if not all(results):
        return 1
    print("The three legs of the false refusal are closed and the double-probe case still refuses.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
