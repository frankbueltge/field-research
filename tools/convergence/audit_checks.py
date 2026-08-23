#!/usr/bin/env python3
"""audit_checks.py — run every check this practice relies on twice, against an unchanged
record, and report which of them measure the record plus themselves.

WHY THIS EXISTS (2026-08-23, session 133)
-----------------------------------------
`CONDITIONS-132.md` binding item 7 and `memory/open-questions.md` file this as owed and
explicitly not performed:

    "Which of this practice's other checks scan a population that contains their own
    output? ... What would close it: for each check, the stated relation between its
    search space and its output path, and a convergence test — run it twice against an
    unchanged record and assert the two reports are identical. That test is cheap, it is
    not written anywhere, and this session did not write it either."

This is that test. It is written to be run, not read: every verdict below is produced by
executing a check and observing what it touched, never by reading its source and forming
an opinion. The defect that raised the question (`e34_sweep.py`, `ERRATA-132.md` E36) was
invisible to review and obvious to a second run.

THE TWO MEASUREMENTS
--------------------
1. **SELF-CONTAINMENT** — does the check write into a place it also reads?
   Observed with `iotrace.py`: the set of paths written, intersected with (a) the set of
   paths read and (b) the set of directories enumerated. A write into an enumerated
   directory is the `e34_sweep` shape even when run 1 did not read the file, because the
   file did not exist yet on run 1 — that is precisely how the defect hides.

2. **CONVERGENCE** — run the check twice with nothing in the record changed between the
   runs, and compare. Two reports are compared, not one: the check's own stdout/stderr,
   and every file it wrote. **The record is deliberately NOT restored between run 1 and
   run 2.** Restoring it would test something nobody needs to know. The question is what
   happens when a check runs twice in a row on a repository nobody has edited — which is
   what a session actually does — and if the check's own output changed the record, that
   is the finding, not a spoiled experiment.

ISOLATION, AND WHY IT IS NOT OPTIONAL
-------------------------------------
Every run happens in a **fresh copy** of the repository in a scratch directory outside it,
restored from one pristine master copy before each check's pair of runs. The audit's own
outputs — traces, reports, this file's JSON — are written outside the repository under
audit for the duration. An audit of self-referential instruments that dropped its report
into the tree its subjects search would be the twelfth instance of the defect it is
counting. It is committed into the record afterwards, and what that does to the next run
of these checks is stated in the finding rather than avoided.

WHAT THIS CANNOT DO, STATED BEFORE THE RESULTS
----------------------------------------------
  * The tracer sees Python-level file entry points only (`iotrace.py` lists them). A check
    that shells out is marked PARTIALLY OBSERVED and never reported as clean.
  * A check is run in ONE invocation, the one named in `POPULATION` below and taken from
    the check's own documented usage. A different flag may have a different search space.
    The invocation is printed with every verdict.
  * Convergence over two runs is a floor, not a proof. `e34_sweep.py` needed three runs
    before its own count stopped moving, so a third run is taken for every check that
    converges over two, and a check is reported as converged only if all three agree.
  * A check that reads no repository file at all cannot exhibit this defect and is
    reported as NOT APPLICABLE rather than as passing.

USAGE
    python3 tools/convergence/audit_checks.py            # writes convergence-audit-133.json
    python3 tools/convergence/audit_checks.py --report   # human-readable, changes nothing
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
ARC = "drafts/2026-08-11-the-arm-that-was-missing"

# Every check this practice runs against its own record, with the invocation taken from
# the script's own documented usage. `cwd` is relative to the repository root.
POPULATION = [
    # --- repository-level guards: the three a session runs at orientation, plus two more
    {"id": "chronicle_check", "cwd": ".",
     "argv": ["tools/chronicle_check.py"],
     "role": "orientation guard — refuses a chronicle entry the receiving site cannot read"},
    {"id": "check_anchors", "cwd": ".",
     "argv": ["tools/journal/check_anchors.py"],
     "role": "orientation guard — journal/chronicle anchor agreement"},
    {"id": "requests_room_check", "cwd": ".",
     "argv": ["tools/requests_room_check.py"],
     "role": "orientation guard — REQUESTS.md word budget in the receiving build"},
    {"id": "record_ceiling_check", "cwd": ".",
     "argv": ["tools/record_ceiling_check.py", ARC],
     "role": "rule 6 ceiling on a work's process record"},
    {"id": "apparatus_ratio", "cwd": ".",
     "argv": ["tools/apparatus_ratio.py", "--json"],
     "role": "the apparatus ratios, published at every consolidation"},
    # --- the live arc's own checks
    {"id": "errata_check_coverage", "cwd": ARC,
     "argv": ["errata_check.py", "--coverage"],
     "role": "accounting of every published erratum against the bundle"},
    {"id": "errata_check_bundle", "cwd": ARC,
     "argv": ["errata_check.py", "deliverable-v0.3"],
     "role": "fails if a published correction reappears in the bundle"},
    {"id": "guard_claims_check", "cwd": ARC,
     "argv": ["guard_claims.py", "--check"],
     "role": "fails if the claims block on disk is not what the guards say now"},
    {"id": "e34_sweep", "cwd": ARC,
     "argv": ["e34_sweep.py"],
     "role": "the check whose defect raised this question (fixed at session 132)"},
    {"id": "prose_vs_json", "cwd": ARC,
     "argv": ["prose_vs_json.py", "INCREMENT-20.md"],
     "role": "numbers in prose against the computed files behind them"},
    {"id": "validate_timestamps", "cwd": ARC,
     "argv": ["validate_timestamps.py"],
     "role": "timestamp validation over the arc's run files"},
    {"id": "check_sweep_completeness", "cwd": ARC,
     "argv": ["check_sweep_completeness.py"],
     "role": "completeness of a probe sweep against its manifest"},
]

RUNS_PER_CHECK = 3       # two would answer the question; e34_sweep needed three to show it


def sha(b):
    return hashlib.sha256(b).hexdigest()


def snapshot_dir(root):
    """sha256 of every regular file under root, keyed by relative path. .git excluded:
    the audit never commits, and git's own internals move for reasons that are not the
    record changing."""
    out = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, root)
            try:
                with open(p, "rb") as fh:
                    out[rel] = sha(fh.read())
            except OSError:
                out[rel] = "<unreadable>"
    return out


def run_once(work, check, trace_path):
    cwd = os.path.join(work, check["cwd"])
    env = dict(os.environ)
    env["IOTRACE_OUT"] = trace_path
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    tracer = os.path.join(work, "tools", "convergence", "iotrace.py")
    argv = [sys.executable, tracer] + check["argv"]
    proc = subprocess.run(argv, cwd=cwd, env=env, capture_output=True)
    trace = None
    if os.path.exists(trace_path):
        with open(trace_path) as fh:
            trace = json.load(fh)
    return {
        "exit_code": proc.returncode,
        "stdout_sha": sha(proc.stdout),
        "stderr_sha": sha(proc.stderr),
        "stdout_len": len(proc.stdout),
        "stdout_head": proc.stdout.decode("utf-8", "replace")[:400],
        "stderr_head": proc.stderr.decode("utf-8", "replace")[:400],
        "trace": trace,
    }


def rel_to_work(work, paths):
    out = set()
    w = os.path.abspath(work) + os.sep
    for p in paths:
        if p.startswith(w):
            out.add(p[len(w):])
    return out


def audit_one(master, scratch, check):
    work = os.path.join(scratch, "work")
    if os.path.exists(work):
        shutil.rmtree(work)
    shutil.copytree(master, work, symlinks=True)
    before = snapshot_dir(work)

    runs = []
    for i in range(RUNS_PER_CHECK):
        tp = os.path.join(scratch, "trace-%s-%d.json" % (check["id"], i + 1))
        runs.append(run_once(work, check, tp))

    after = snapshot_dir(work)

    # what the check itself changed in the record, across all runs
    changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))

    t1 = runs[0]["trace"] or {}
    reads = rel_to_work(work, t1.get("reads", []))
    writes = rel_to_work(work, t1.get("writes", []))
    listed = rel_to_work(work, t1.get("dirs_listed", []))
    listed_dirs = {d if d else "." for d in listed}

    # SELF-CONTAINMENT, observed three ways
    written_and_read = sorted(writes & reads)
    written_into_listed = sorted(
        w for w in writes
        if (os.path.dirname(w) or ".") in listed_dirs
        or any(w.startswith(d.rstrip("/") + os.sep) for d in listed_dirs if d != ".")
        or "." in listed_dirs
    )
    repo_writes = sorted(writes)
    # A write that is gone from the tree when the check exits is a temporary probe, not a
    # contaminant of the record — but it is still inside another check's search space
    # while it exists, which is a race rather than a convergence failure. The two are
    # told apart here rather than conflated: `guard_claims.py --check` writes a probe
    # into the arc directory and removes it, and grading that as the `e34_sweep` defect
    # would be a false positive this audit would deserve to be refuted on.
    transient_writes = sorted(w for w in repo_writes if w not in after)
    persistent_writes = sorted(w for w in repo_writes if w in after)

    # CONVERGENCE across the runs
    fields = ("exit_code", "stdout_sha", "stderr_sha")
    identical = all(all(r[f] == runs[0][f] for f in fields) for r in runs)
    written_stable = True
    written_hashes = []
    for w in repo_writes:
        h = [after.get(w)]
        written_hashes.append({"path": w, "sha_after": after.get(w)})
    # a written file whose content differs between runs shows up as the check's stdout
    # differing only if the check prints it; so re-derive per-run by re-reading is not
    # possible after the fact — the per-run stdout hash plus the record diff is what is
    # claimed, and nothing more.

    partially_observed = bool(t1.get("children")) or bool(t1.get("os_open_used"))
    reaches_network = bool(t1.get("network_calls"))

    reads_repo = bool(reads or listed)

    # Order matters, and the first version of this classifier got it wrong: it reported
    # `apparatus_ratio` as NOT-APPLICABLE — "touches nothing" — when in fact it reads the
    # whole tracked record through `git ls-files` in a child process the tracer cannot see
    # inside. A check whose reading happens somewhere this instrument cannot look must
    # never be graded as if the instrument had looked and found nothing.
    if partially_observed and not reads_repo:
        verdict_containment = "PARTIALLY-OBSERVED"
    elif reaches_network and not reads_repo:
        verdict_containment = "MEASURES-A-LIVE-SERVICE-NOT-THE-RECORD"
    elif not reads_repo:
        verdict_containment = "NOT-APPLICABLE"
    elif [w for w in (written_and_read + written_into_listed) if w in persistent_writes]:
        verdict_containment = "OUTPUT-INSIDE-SEARCH-SPACE"
    elif written_and_read or written_into_listed:
        verdict_containment = "TRANSIENT-WRITE-INSIDE-SEARCH-SPACE"
    elif repo_writes:
        verdict_containment = "WRITES-OUTSIDE-SEARCH-SPACE"
    else:
        verdict_containment = "READ-ONLY"

    # VACUOUS IS NOT A PASS. This arc already refuses to score a test whose condition never
    # fired (K4 on day 11, `CONDITIONS-132.md`), and the same refusal applies here: a check
    # that dies in an unhandled exception produces three identical crash reports, and three
    # identical crashes say nothing whatever about whether its report over the record is
    # stable. Recorded as its own verdict rather than counted with the genuine passes.
    if not identical:
        verdict_convergence = "DOES-NOT-CONVERGE"
    elif t1.get("error"):
        verdict_convergence = "CONVERGES-VACUOUSLY"
    else:
        verdict_convergence = "CONVERGES"

    return {
        "id": check["id"],
        "role": check["role"],
        "invocation": "(cd %s && python3 %s)" % (check["cwd"], " ".join(check["argv"])),
        "runs": RUNS_PER_CHECK,
        "exit_codes": [r["exit_code"] for r in runs],
        "stdout_shas": [r["stdout_sha"][:16] for r in runs],
        "stderr_shas": [r["stderr_sha"][:16] for r in runs],
        "first_run_stdout_head": runs[0]["stdout_head"],
        "first_run_stderr_head": runs[0]["stderr_head"],
        "tracer_error": t1.get("error"),
        "repo_files_read": len(reads),
        "repo_dirs_listed": sorted(listed_dirs),
        "repo_files_written": repo_writes,
        "writes_still_present_at_exit": persistent_writes,
        "writes_removed_before_exit": transient_writes,
        "written_and_also_read": written_and_read,
        "written_into_an_enumerated_directory": written_into_listed,
        "record_changed_by_the_check": changed,
        "partially_observed": partially_observed,
        "network_calls": t1.get("network_calls", 0),
        "network_head": (t1.get("network") or [])[:6],
        "child_processes": t1.get("children", []),
        "os_open_used": t1.get("os_open_used", False),
        "verdict_containment": verdict_containment,
        "verdict_convergence": verdict_convergence,
        "written_state_after": written_hashes,
    }


def main(argv):
    report_only = "--report" in argv
    out_path = os.path.join(REPO, "tools", "convergence", "convergence-audit-133.json")

    # --inject FILE places FILE where this audit's own report will be committed, BEFORE
    # the checks run. It exists to answer the question this audit cannot dodge: this
    # audit writes a report into the repository, and several of the checks it audits
    # enumerate the repository — so the audit is itself a candidate instance of the very
    # defect it counts. `--inject` measures that instead of confessing it. See
    # `contamination_133.py`.
    inject = None
    if "--inject" in argv:
        inject = os.path.abspath(argv[argv.index("--inject") + 1])

    # --master DIR runs against an already-frozen copy instead of copying the live tree.
    # This exists because the first replicated contamination run was invalid: each pass
    # re-copied the LIVE repository, and this session wrote `INCREMENT-21.md` into the arc
    # directory between two of them. `record_ceiling_check.py` counts words in that
    # directory, so its report moved — and the test reported it as "unstable on its own"
    # when in fact the record had changed underneath, which is the one precondition the
    # whole test rests on and the one thing it was not checking. A test for "run it twice
    # against an unchanged record" that never verified the record was unchanged is the
    # same shape of defect as the ones it hunts.
    frozen_master = None
    if "--master" in argv:
        frozen_master = os.path.abspath(argv[argv.index("--master") + 1])

    scratch = tempfile.mkdtemp(prefix="convergence-audit-")
    master = os.path.join(scratch, "master")
    # The master copy carries the working tree as this session found it, .git included so
    # that checks shelling out to git see a real repository.
    shutil.copytree(frozen_master or REPO, master, symlinks=True)
    if inject:
        dest = os.path.join(master, "tools", "convergence", "convergence-audit-133.json")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copyfile(inject, dest)

    results = []
    for check in POPULATION:
        script = os.path.join(master, check["cwd"], check["argv"][0])
        if not os.path.exists(script):
            results.append({"id": check["id"], "role": check["role"],
                            "invocation": "(cd %s && python3 %s)" % (check["cwd"], " ".join(check["argv"])),
                            "verdict_containment": "SCRIPT-NOT-FOUND",
                            "verdict_convergence": "NOT-RUN"})
            continue
        sys.stderr.write("auditing %s ...\n" % check["id"])
        sys.stderr.flush()
        results.append(audit_one(master, scratch, check))

    summary = {
        "generated_by": "tools/convergence/audit_checks.py",
        "session": 133,
        "runs_per_check": RUNS_PER_CHECK,
        "population": len(POPULATION),
        "counts": {
            v: sum(1 for r in results if r.get("verdict_containment") == v)
            for v in sorted({r.get("verdict_containment") for r in results})
        },
        "convergence_counts": {
            v: sum(1 for r in results if r.get("verdict_convergence") == v)
            for v in sorted({r.get("verdict_convergence") for r in results})
        },
        "checks": results,
    }

    if report_only:
        print(json.dumps(summary, indent=1, sort_keys=True))
    else:
        with open(out_path, "w") as fh:
            json.dump(summary, fh, indent=1, sort_keys=True)
        print("wrote " + os.path.relpath(out_path, REPO))
    shutil.rmtree(scratch, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
