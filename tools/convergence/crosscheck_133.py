#!/usr/bin/env python3
"""crosscheck_133.py — run the checks in ONE tree, in sequence, the way a session does.

WHY THIS EXISTS (2026-08-23, session 133)
-----------------------------------------
`audit_checks.py` audits each check in a fresh copy of the record, in isolation. That
answers the question as `memory/open-questions.md` filed it and it is not the condition
that actually obtains. A session runs several of these checks in one tree, one after
another, and each one's output is still lying there when the next one starts.
`INCREMENT-21.md` §8 names this as owed and not done. This closes it.

`guard_claims.py --check` is the reason it is worth doing: it writes
`guard-claims-wordnumber-probe.md` into the arc directory and removes it before it exits.
While it exists, that file sits inside the search space of `record_ceiling_check.py`,
`e34_sweep.py` and `prose_vs_json.py`, all of which enumerate that directory. The isolated
audit could not fire that and said so rather than implying otherwise.

METHOD
------
0. **Freeze the record once**, and take BOTH passes from that one frozen copy. The first
   version of this script read the ISOLATED side from the committed audit artifact, which
   was produced from a copy of the live tree taken minutes earlier — and reported
   `record_ceiling_check` and `apparatus_ratio` as moved. They had not moved: **the record
   had.** The arc's own daily probe writes its progress log into the very directory
   `record_ceiling_check` counts words in, so that directory grows every few minutes while
   a run is in flight, and `apparatus_ratio` measures the byte size of every tracked file.
   **This is the third false attribution this session produced from comparing two runs
   taken against two different states of a moving record**, and all three had the same
   cause. Freezing once is the only fix that works.
1. Run every check in the population, in order, in ONE copy of the frozen tree, without
   restoring anything between them. (SEQUENTIAL)
2. Run the same population against the same frozen tree with a fresh copy per check, via
   `audit_checks.py --master`. (ISOLATED)
3. A check whose report differs between the two was affected by another check having run
   before it. Which one, this does not say; that it happened, it does say.

The order is the population order, which is the order these appear in `audit_checks.py`
and has no other significance. **A different order is a different experiment**, and one
run of one order is what is claimed here.

WHAT THIS STILL DOES NOT DO
---------------------------
It runs each check ONCE in the sequential pass. A difference could therefore be a check
that is unstable on its own rather than one affected by a neighbour — so any check the
isolated pass did not record as plainly CONVERGES is excluded from the attribution by
name, exactly as `contamination_133.py` excludes checks unstable between two baselines.
It also does not run the branch-forced invocation `audit_checks.py` carries beside the
population, so the persistent file that invocation leaves behind is not in this sequence.

USAGE
    python3 tools/convergence/crosscheck_133.py      # writes crosscheck-133.json
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "crosscheck-133.json")
AUDIT = os.path.join(HERE, "audit_checks.py")

sys.path.insert(0, HERE)
from audit_checks import POPULATION            # noqa: E402  the one population, not a copy


def sha(b):
    return hashlib.sha256(b).hexdigest()


def tree_hash(root):
    h = hashlib.sha256()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d != ".git")
        for fn in sorted(filenames):
            p = os.path.join(dirpath, fn)
            h.update(os.path.relpath(p, root).encode())
            try:
                with open(p, "rb") as fh:
                    h.update(hashlib.sha256(fh.read()).digest())
            except OSError:
                h.update(b"<unreadable>")
    return h.hexdigest()


def main():
    scratch = tempfile.mkdtemp(prefix="crosscheck-133-")
    frozen = os.path.join(scratch, "frozen")
    sys.stderr.write("freezing the record ...\n")
    shutil.copytree(REPO, frozen, symlinks=True)
    h_before = tree_hash(frozen)

    sys.stderr.write("isolated pass: a fresh copy of the frozen tree per check ...\n")
    proc = subprocess.run([sys.executable, AUDIT, "--report", "--master", frozen],
                          cwd=REPO, capture_output=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr.decode("utf-8", "replace")[-2000:])
        raise SystemExit("isolated pass failed")
    isolated = {c["id"]: c for c in json.loads(proc.stdout.decode("utf-8"))["checks"]}

    work = os.path.join(scratch, "work")
    shutil.copytree(frozen, work, symlinks=True)

    tracer = os.path.join(work, "tools", "convergence", "iotrace.py")
    rows = []
    order = []
    for check in POPULATION:
        cwd = os.path.join(work, check["cwd"])
        script = os.path.join(cwd, check["argv"][0])
        if not os.path.exists(script):
            continue
        order.append(check["id"])
        env = dict(os.environ)
        env["IOTRACE_OUT"] = os.path.join(scratch, "trace-" + check["id"] + ".json")
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        sys.stderr.write("sequential: %s ...\n" % check["id"])
        sys.stderr.flush()
        proc = subprocess.run([sys.executable, tracer] + check["argv"],
                              cwd=cwd, env=env, capture_output=True)

        iso = isolated.get(check["id"], {})
        iso_stdout = (iso.get("stdout_shas") or [None])[0]
        iso_stderr = (iso.get("stderr_shas") or [None])[0]
        iso_exit = (iso.get("exit_codes") or [None])[0]
        seq_stdout = sha(proc.stdout)[:16]
        seq_stderr = sha(proc.stderr)[:16]
        converged = iso.get("verdict_convergence") == "CONVERGES"

        differs = (seq_stdout != iso_stdout or seq_stderr != iso_stderr
                   or proc.returncode != iso_exit)
        rows.append({
            "id": check["id"],
            "ran_after": list(order[:-1]),
            "isolated_converged": converged,
            "isolated_stdout_sha": iso_stdout,
            "sequential_stdout_sha": seq_stdout,
            "isolated_stderr_sha": iso_stderr,
            "sequential_stderr_sha": seq_stderr,
            "isolated_exit_code": iso_exit,
            "sequential_exit_code": proc.returncode,
            "differs_from_isolated": differs,
            "attributable": bool(differs and converged),
            "excluded_reason": (None if converged else
                                "did not converge cleanly in isolation "
                                "(" + str(iso.get("verdict_convergence")) + ") — "
                                "a difference here cannot be attributed to a neighbour"),
        })

    h_after = tree_hash(frozen)
    shutil.rmtree(scratch, ignore_errors=True)

    attributable = [r["id"] for r in rows if r["attributable"]]
    excluded = [r["id"] for r in rows if not r["isolated_converged"]]
    summary = {
        "generated_by": "tools/convergence/crosscheck_133.py",
        "session": 133,
        "question": "does running these checks one after another in a single tree, the way a "
                    "session does, change any of their reports against running each alone in a "
                    "fresh copy?",
        "order_run": order,
        "order_note": "one run of one order; a different order is a different experiment",
        "population": len(rows),
        "frozen_record_sha256_before": h_before,
        "frozen_record_sha256_after": h_after,
        "both_passes_ran_against_the_same_frozen_record": h_before == h_after,
        "excluded_as_not_cleanly_convergent_in_isolation": excluded,
        "checks_whose_report_moved": attributable,
        "count_moved": len(attributable),
        "verdict": ("RUNNING THE CHECKS IN SEQUENCE MOVES AT LEAST ONE REPORT" if attributable
                    else "NO CHECK'S REPORT MOVED WHEN THE CHECKS WERE RUN IN SEQUENCE IN ONE TREE"),
        "rows": rows,
    }
    with open(OUT, "w") as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)
    print(json.dumps({k: summary[k] for k in
                      ("count_moved", "checks_whose_report_moved",
                       "excluded_as_not_cleanly_convergent_in_isolation", "verdict")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
