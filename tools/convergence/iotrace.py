#!/usr/bin/env python3
"""iotrace.py — run a script and record every file it reads and every file it writes.

WHY THIS EXISTS (2026-08-23, session 133)
-----------------------------------------
`CONDITIONS-132.md` binding item 7, and `memory/open-questions.md`:

    "Which of this practice's other checks scan a population that contains their own
    output? ... What would close it: for each check, the stated relation between its
    search space and its output path, and a convergence test — run it twice against an
    unchanged record and assert the two reports are identical."

The defect that raised the question is `e34_sweep.py` (`ERRATA-132.md` E36): it searched
the repository for a withdrawn wording and wrote its report into the repository, quoting
every site it found. The report was therefore a site. Its count rose 11 → 12 → 13 across
three runs with nothing in the record having changed. **The instrument was not measuring
the record; it was measuring the record plus itself.**

That defect was found by running the thing, not by reading it. So this module does not
read code and does not classify by naming convention. It observes: it patches the file
and directory entry points a Python script actually uses, runs the script, and writes down
the paths that crossed them.

WHAT IS OBSERVED
----------------
  * `builtins.open` — mode decides read or write
  * `os.listdir`, `os.scandir`, `os.walk` — directory enumeration (a search space)
  * `glob.glob`, `glob.iglob` — the same, by pattern
  * `pathlib.Path.open` / `.read_text` / `.read_bytes` / `.write_text` / `.write_bytes`
  * `pathlib.Path.glob` / `.rglob`
  * `subprocess.run` / `.check_output` / `.Popen` — recorded as an opaque child process,
    because this tracer cannot see inside one. A check that shells out is reported as
    PARTIALLY OBSERVED and never as clean.

WHAT IS NOT OBSERVED, STATED SO NOBODY HAS TO INFER IT
------------------------------------------------------
  * C-level reads that bypass the Python entry points above.
  * Anything a child process does (see `subprocess` above).
  * Reads through `os.open` with an integer fd. No check in this practice's population
    uses it, which is checked rather than assumed — the audit records whether `os.open`
    was reached at all.

NETWORK
-------
`urllib.request.urlopen` and `socket.socket.connect` are also patched, and every host a
check reaches is recorded. This is not scope creep: the question is which checks scan
*this practice's record*, and a script that fetches a live service is not measuring the
record at all. Observing it is the only way to say so without asserting it from the
script's name.

DEFECTS OF THIS TRACER, FOUND BY RUNNING IT (session 133, before any result was used)
-------------------------------------------------------------------------------------
Three, and each one made a check look CLEANER or emptier than it is. They are recorded
rather than quietly corrected, because an audit of self-measuring instruments that hid its
own measurement defects would be worthless — and because all three were invisible to
reading the tracer and obvious the moment its output was compared against running the
same check by hand.

1. **`runpy.run_path` does not put the script's own directory on `sys.path`**, which the
   ordinary `python3 script.py` invocation does. The first run of the audit therefore
   reported `guard_claims.py --check` as reading nothing at all, with a
   `ModuleNotFoundError` for a module sitting beside it. Fixed by inserting the script's
   directory at `sys.path[0]`, exactly as the interpreter would. Run untraced, that check
   reads 13 files and writes one.
2. **The classifier graded a check that reads the record through a child process as
   touching nothing.** `apparatus_ratio.py` reads the entire tracked record through
   `git ls-files`, which this tracer cannot see inside. Fixed in `audit_checks.py`, not
   here: such a check is PARTIALLY-OBSERVED and is never reported as clean.
3. **A patched `glob.iglob` that routed back through a patched `glob.glob` recursed.**
   `glob.glob` is `list(iglob(...))` against the module global. The second run of the
   audit reported `prose_vs_json.py` as touching no files, with a `RecursionError`; run
   untraced it reads 156 JSON files and exits 0. Fixed below.

The trace is written OUTSIDE the repository under audit, to a path given in the
environment. This is not tidiness: a tracer that wrote its log into the tree would put
itself into the search space of every check it traces, which is the exact defect the
whole exercise exists to measure.

USAGE
    IOTRACE_OUT=/somewhere/outside/trace.json \\
        python3 tools/convergence/iotrace.py <script.py> [args...]
"""
import builtins
import glob as glob_mod
import json
import os
import pathlib
import runpy
import socket
import subprocess
import sys
import time
import urllib.request

READS = []
WRITES = []
LISTS = []
CHILDREN = []
NETWORK = []
OS_OPEN_USED = [False]

_real_open = builtins.open
_real_listdir = os.listdir
_real_scandir = os.scandir
_real_walk = os.walk
_real_glob = glob_mod.glob
_real_iglob = glob_mod.iglob
_real_os_open = os.open
_real_path_open = pathlib.Path.open
_real_path_read_text = pathlib.Path.read_text
_real_path_read_bytes = pathlib.Path.read_bytes
_real_path_write_text = pathlib.Path.write_text
_real_path_write_bytes = pathlib.Path.write_bytes
_real_path_glob = pathlib.Path.glob
_real_path_rglob = pathlib.Path.rglob
_real_run = subprocess.run
_real_check_output = subprocess.check_output
_real_popen = subprocess.Popen
_real_urlopen = urllib.request.urlopen
_real_connect = socket.socket.connect


def _abs(p):
    try:
        return os.path.abspath(os.fspath(p))
    except TypeError:
        return "<non-path:" + repr(p)[:60] + ">"


def _note(bucket, path):
    bucket.append(_abs(path))


def _traced_open(file, mode="r", *a, **kw):
    if any(c in mode for c in "wax+"):
        _note(WRITES, file)
    else:
        _note(READS, file)
    return _real_open(file, mode, *a, **kw)


def _traced_listdir(path="."):
    _note(LISTS, path)
    return _real_listdir(path)


def _traced_scandir(path="."):
    _note(LISTS, path)
    return _real_scandir(path)


def _traced_walk(top, *a, **kw):
    _note(LISTS, top)
    return _real_walk(top, *a, **kw)


def _traced_glob(pathname, *a, **kw):
    res = _real_glob(pathname, *a, **kw)
    _note(LISTS, os.path.dirname(pathname) or ".")
    for r in res:
        _note(READS, r)
    return res


def _traced_iglob(pathname, *a, **kw):
    # MUST call the real iglob, not _traced_glob. `glob.glob` is implemented as
    # `list(iglob(...))` against the module global, so a patched iglob that routed back
    # through a patched glob recursed until the interpreter gave up — which is how the
    # second run of the audit reported `prose_vs_json.py` as touching no files at all,
    # with a RecursionError, when run untraced it reads 156 JSON files and exits 0.
    # Third defect of this tracer found by running it; see DEFECTS above.
    _note(LISTS, os.path.dirname(pathname) or ".")
    for r in _real_iglob(pathname, *a, **kw):
        _note(READS, r)
        yield r


def _traced_os_open(path, flags, *a, **kw):
    OS_OPEN_USED[0] = True
    if flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND):
        _note(WRITES, path)
    else:
        _note(READS, path)
    return _real_os_open(path, flags, *a, **kw)


def _traced_path_open(self, mode="r", *a, **kw):
    if any(c in mode for c in "wax+"):
        _note(WRITES, self)
    else:
        _note(READS, self)
    return _real_path_open(self, mode, *a, **kw)


def _traced_path_read_text(self, *a, **kw):
    _note(READS, self)
    return _real_path_read_text(self, *a, **kw)


def _traced_path_read_bytes(self, *a, **kw):
    _note(READS, self)
    return _real_path_read_bytes(self, *a, **kw)


def _traced_path_write_text(self, *a, **kw):
    _note(WRITES, self)
    return _real_path_write_text(self, *a, **kw)


def _traced_path_write_bytes(self, *a, **kw):
    _note(WRITES, self)
    return _real_path_write_bytes(self, *a, **kw)


def _traced_path_glob(self, pattern, *a, **kw):
    _note(LISTS, self)
    out = list(_real_path_glob(self, pattern, *a, **kw))
    for r in out:
        _note(READS, r)
    return iter(out)


def _traced_path_rglob(self, pattern, *a, **kw):
    _note(LISTS, self)
    out = list(_real_path_rglob(self, pattern, *a, **kw))
    for r in out:
        _note(READS, r)
    return iter(out)


def _child(args):
    try:
        CHILDREN.append(" ".join(str(x) for x in args) if isinstance(args, (list, tuple))
                        else str(args))
    except Exception:
        CHILDREN.append("<unrenderable child argv>")


def _traced_run(args, *a, **kw):
    _child(args)
    return _real_run(args, *a, **kw)


def _traced_check_output(args, *a, **kw):
    _child(args)
    return _real_check_output(args, *a, **kw)


class _TracedPopen(_real_popen):
    def __init__(self, args, *a, **kw):
        _child(args)
        super().__init__(args, *a, **kw)


def _traced_urlopen(url, *a, **kw):
    try:
        target = url.full_url if hasattr(url, "full_url") else str(url)
    except Exception:
        target = "<unrenderable url>"
    NETWORK.append("urlopen " + target[:200])
    return _real_urlopen(url, *a, **kw)


def _traced_connect(self, address):
    try:
        NETWORK.append("connect " + str(address[0]) + ":" + str(address[1]))
    except Exception:
        NETWORK.append("connect <unrenderable address>")
    return _real_connect(self, address)


def install():
    urllib.request.urlopen = _traced_urlopen
    socket.socket.connect = _traced_connect
    builtins.open = _traced_open
    os.listdir = _traced_listdir
    os.scandir = _traced_scandir
    os.walk = _traced_walk
    os.open = _traced_os_open
    glob_mod.glob = _traced_glob
    glob_mod.iglob = _traced_iglob
    pathlib.Path.open = _traced_path_open
    pathlib.Path.read_text = _traced_path_read_text
    pathlib.Path.read_bytes = _traced_path_read_bytes
    pathlib.Path.write_text = _traced_path_write_text
    pathlib.Path.write_bytes = _traced_path_write_bytes
    pathlib.Path.glob = _traced_path_glob
    pathlib.Path.rglob = _traced_path_rglob
    subprocess.run = _traced_run
    subprocess.check_output = _traced_check_output
    subprocess.Popen = _TracedPopen


def main(argv):
    out = os.environ.get("IOTRACE_OUT")
    if not out:
        print("IOTRACE_OUT is not set; refusing to run", file=sys.stderr)
        return 2
    if not argv:
        print("usage: iotrace.py <script.py> [args...]", file=sys.stderr)
        return 2
    script = argv[0]
    # `python3 script.py` puts the script's own directory at sys.path[0]; runpy.run_path
    # does not. Without this a check that imports a sibling module dies with an import
    # error and the audit reads it as a check that touches nothing. See DEFECTS above.
    sys.path.insert(0, os.path.dirname(os.path.abspath(script)) or ".")
    install()
    sys.argv = list(argv)
    started = time.time()
    status = 0
    error = None
    try:
        runpy.run_path(script, run_name="__main__")
    except SystemExit as e:
        status = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
    except BaseException as e:                      # a check that crashes is a finding
        status = 1
        error = type(e).__name__ + ": " + str(e)[:400]
    finally:
        # Restore before writing, so the trace file itself is never traced.
        urllib.request.urlopen = _real_urlopen
        socket.socket.connect = _real_connect
        builtins.open = _real_open
        os.listdir = _real_listdir
        os.scandir = _real_scandir
        os.walk = _real_walk
        os.open = _real_os_open
        glob_mod.glob = _real_glob
        glob_mod.iglob = _real_iglob
        pathlib.Path.open = _real_path_open
        pathlib.Path.read_text = _real_path_read_text
        pathlib.Path.read_bytes = _real_path_read_bytes
        pathlib.Path.write_text = _real_path_write_text
        pathlib.Path.write_bytes = _real_path_write_bytes
        pathlib.Path.glob = _real_path_glob
        pathlib.Path.rglob = _real_path_rglob
        subprocess.run = _real_run
        subprocess.check_output = _real_check_output
        subprocess.Popen = _real_popen
        with _real_open(out, "w") as fh:
            json.dump({
                "script": script,
                "argv": list(argv),
                "cwd": os.getcwd(),
                "exit_status": status,
                "error": error,
                "elapsed_s": round(time.time() - started, 3),
                "reads": sorted(set(READS)),
                "writes": sorted(set(WRITES)),
                "dirs_listed": sorted(set(LISTS)),
                "children": CHILDREN,
                "network": NETWORK[:200],
                "network_calls": len(NETWORK),
                "os_open_used": OS_OPEN_USED[0],
            }, fh, indent=1, sort_keys=True)
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
