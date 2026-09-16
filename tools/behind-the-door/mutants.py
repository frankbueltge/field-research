"""Mutation test — break each rung on purpose and check that something notices.

Session 162, 2026-09-16. A passing fixture suite proves nothing on its own: a suite that
would pass no matter what the rules did is decoration. So every rule is deliberately
broken, one breakage at a time, and the suite must fail. A mutant that survives means the
suite does not exercise that rule, and the gap is closed before any repository is cloned.

Run:  python3 tools/behind-the-door/mutants.py
"""

import importlib
import json
import re
import sys

import fixtures
import rungs


def _rebuild(name, fn):
    """Replace a rung function and rebuild the tables the fixture runner reads."""
    setattr(rungs, name, fn)
    rungs.RUNGS = [(n, d, getattr(rungs, f.__name__)) for n, d, f in rungs.RUNGS]
    rungs.EXTRAS = [(n, d, getattr(rungs, f.__name__)) for n, d, f in rungs.EXTRAS]


# Each mutant: (rung it attacks, what was broken, patch function)
MUTANTS = [
    ("R1_content", "dotfiles no longer count as boilerplate",
     lambda: setattr(rungs, "BOILERPLATE_RE", re.compile(
         r"^(readme|licen[cs]e|copying|unlicense|contributing|code_of_conduct|security"
         r"|citation|authors|changelog|codeowners|notice|acknowledgements?)([.\-_].*)?$",
         re.I))),
    ("R1_content", "an empty tree counts as content",
     lambda: _rebuild("r1_content", lambda files, blobs=None: True)),
    ("R2_code", "a YAML config counts as source code",
     lambda: rungs.SOURCE_EXT.add("yaml")),
    ("R2_code", "extensions matched case-sensitively",
     lambda: _rebuild("r2_code", lambda files, blobs=None: any(
         (rungs.basename(p).rsplit(".", 1)[-1] if "." in rungs.basename(p) else "")
         in rungs.SOURCE_EXT for p in files))),
    ("R3_licence", "any name beginning with 'licen' is a licence",
     lambda: setattr(rungs, "LICENCE_BASENAME_RE", re.compile(r"^licen", re.I))),
    ("R3_licence", "only a root-level licence grants",
     lambda: _rebuild("r3_licence_file", lambda files, blobs=None: any(
         "/" not in p and rungs.LICENCE_BASENAME_RE.match(p) for p in files))),
    ("R3b_licence_declared_only", "a licence classifier counts as a declaration",
     lambda: _rebuild("r3b_licence_declared", lambda files, blobs: any(
         "license" in (t or "").lower() for t in (blobs or {}).values()))),
    ("R4_manifest", "a container recipe counts as a dependency manifest",
     lambda: rungs.MANIFEST_BASENAMES.add("dockerfile")),
    ("R4_manifest", "'requirements' anywhere in the path counts",
     lambda: _rebuild("r4_manifest", lambda files, blobs=None: any(
         "requirements" in p.lower() or rungs._is_manifest(p) for p in files))),
    ("R4b_container", "a compose file counts as a container recipe",
     lambda: setattr(rungs, "CONTAINER_BASENAMES_RE", re.compile(r"^docker", re.I))),
    ("R5_pinning", "the threshold becomes strictly more than half",
     lambda: _rebuild("r5_pinning", _strict_majority_pinning)),
    ("R5_pinning", "options and comments count as requirement lines",
     lambda: _rebuild("r5_pinning", _counts_options_pinning)),
    ("R6_entry", "the whole README is scanned, not only its code blocks",
     lambda: setattr(rungs, "code_block_lines", lambda text: text.splitlines())),
    ("R6_entry", "'make' is a command again",
     lambda: setattr(rungs, "COMMAND_RE", re.compile(
         r"^\s*(?:\$|>|#\s*)?\s*(?:sudo\s+)?(python3?|bash|sh|make|docker|pip3?)(\s|$)"))),
    ("R6_entry", "a runner anywhere in the tree counts as a root runner",
     lambda: _rebuild("r6_entry_point", lambda files, blobs: any(
         rungs.ROOT_RUNNER_RE.match(rungs.basename(p)) for p in files))),
    ("R7_tests", "a test path need not hold code",
     lambda: _rebuild("r7_tests", lambda files, blobs=None: any(
         any(part.lower() in rungs.TEST_DIR_NAMES for part in p.split("/")[:-1])
         or rungs.TEST_FILE_RE.match(rungs.basename(p)) for p in files))),
    ("R7_tests", "evaluation splits are no longer excluded",
     lambda: setattr(rungs, "SPLIT_PARENTS", set())),
    ("R8_ci", "a workflow-shaped path anywhere counts as CI",
     lambda: setattr(rungs, "CI_PATH_RE", re.compile(r"workflows/.*\.ya?ml$", re.I))),
    ("FLOOR", "the floor becomes a disjunction",
     lambda: _rebuild("code_repo", _floor_any)),
]


def _strict_majority_pinning(files, blobs):
    if any(rungs.basename(p).lower() in rungs.LOCKFILES for p in files):
        return True, True
    texts = rungs._requirements_texts(blobs)
    if not texts:
        return False, False
    total = pinned = 0
    for text in texts:
        for raw in text.splitlines():
            line = raw.split("#", 1)[0].strip()
            if not line or line.startswith("-"):
                continue
            total += 1
            if "==" in line or re.search(r"@\s*[0-9a-f]{7,40}\b", line):
                pinned += 1
    if total == 0:
        return False, False
    return True, pinned * 2 > total


def _counts_options_pinning(files, blobs):
    if any(rungs.basename(p).lower() in rungs.LOCKFILES for p in files):
        return True, True
    texts = rungs._requirements_texts(blobs)
    if not texts:
        return False, False
    total = pinned = 0
    for text in texts:
        for raw in text.splitlines():
            if not raw.strip():
                continue
            total += 1
            if "==" in raw:
                pinned += 1
    if total == 0:
        return False, False
    return True, pinned * 2 >= total


def _floor_any(files, blobs):
    out = {}
    for name, _d, fn in rungs.RUNGS:
        out[name] = bool(fn(files, blobs))
    for name, _d, fn in rungs.EXTRAS:
        out[name] = bool(fn(files, blobs))
    if out["R3_licence"]:
        out["R3b_licence_declared_only"] = False
    applicable, pinned = rungs.r5_pinning(files, blobs)
    out["R5_pinning_applicable"] = applicable
    out["R5_pinned"] = pinned if applicable else None
    out["FLOOR"] = any(out[r] for r in rungs.FLOOR_RUNGS)
    return out


def main():
    baseline_results, baseline_failures = fixtures.run()
    if baseline_failures:
        print("baseline suite already fails; refusing to mutation-test")
        return 1

    records = []
    survivors = []
    for rung, broken, patch in MUTANTS:
        importlib.reload(rungs)
        importlib.reload(fixtures)
        # the reloaded fixtures module must see the reloaded rungs module
        fixtures.rungs = rungs
        globals()["rungs"] = rungs
        patch()
        _results, failures = fixtures.run()
        caught = len(failures) > 0
        records.append({
            "rung": rung,
            "breakage": broken,
            "fixtures_failed": len(failures),
            "caught": caught,
            "first_catch": (failures[0]["sentence"] if failures else None),
        })
        if not caught:
            survivors.append(records[-1])

    importlib.reload(rungs)
    importlib.reload(fixtures)

    out = {
        "note": ("Mutation test of the rungs of session 162. Each rule broken on purpose; "
                 "the fixture suite must fail. A survivor is an unexercised rule."),
        "written": "2026-09-16, before any repository was cloned",
        "baseline_fixtures": len(baseline_results),
        "mutants": len(records),
        "survivors": len(survivors),
        "results": records,
    }
    path = "artifacts/2026-09-16-an-address-is-not-an-artifact/data/mutation-check.json"
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print(f"{len(records)} mutants, {len(survivors)} survived -> {path}")
    for s in survivors:
        print("  SURVIVED", s["rung"], "|", s["breakage"])
    return 1 if survivors else 0


if __name__ == "__main__":
    sys.exit(main())
