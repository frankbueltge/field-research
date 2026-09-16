"""Fixtures — every rung run against cases whose answer is fixed by hand, before any data.

Session 162, 2026-09-16. Carried from session 161, which shipped this apparatus and then
showed its limit: a fixture checks that a rule computes what its author says it computes.
It cannot check that the author wrote the right sentence. So each case below names, in
words, the sentence it is holding the rule to.

Every case is a hand-written file list (and where a rung reads text, hand-written blobs).
No case is taken from a real repository. Run:  python3 tools/behind-the-door/fixtures.py
"""

import json
import sys

import rungs

# (rung, expected, label, files, blobs)
CASES = [
    # ---- R1: something beyond boilerplate ----
    ("R1_content", True, "a source file beside a README", ["README.md", "main.py"], {}),
    ("R1_content", False, "an empty tree", [], {}),
    ("R1_content", False, "README and LICENSE only", ["README.md", "LICENSE"], {}),
    ("R1_content", False, "the full GitHub boilerplate set and nothing else",
     ["README.md", "LICENSE.txt", ".gitignore", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md",
      "SECURITY.md", "CITATION.cff", "CHANGELOG.md"], {}),
    ("R1_content", True, "a boilerplate name inside a directory is not root boilerplate",
     ["README.md", "docs/README.md", "src/x.py"], {}),

    # ---- R2: a source-code extension ----
    ("R2_code", True, "one python file", ["a/b/train.py"], {}),
    ("R2_code", True, "a notebook counts as code", ["demo.ipynb"], {}),
    ("R2_code", False, "documentation and data only", ["README.md", "data/x.csv", "fig.png"], {}),
    ("R2_code", False, "a Dockerfile alone is not source code", ["Dockerfile"], {}),
    ("R2_code", False, "a YAML config alone is not source code", ["config.yaml"], {}),
    ("R2_code", True, "an extension is matched case-insensitively", ["MODEL.PY"], {}),

    # ---- R3: a licence file ----
    ("R3_licence", True, "LICENSE at the root", ["LICENSE", "x.py"], {}),
    ("R3_licence", True, "British spelling", ["LICENCE.md"], {}),
    ("R3_licence", True, "COPYING", ["COPYING"], {}),
    ("R3_licence", True, "a licence nested in a subdirectory still grants",
     ["src/x.py", "third_party/LICENSE-MIT"], {}),
    ("R3_licence", False, "a word starting with the same letters is not a licence",
     ["licensing_notes.md", "LICENSEE_LIST.csv"], {}),
    ("R3_licence", False, "a licence mentioned only in the README",
     ["README.md"], {"README.md": "This project is MIT licensed."}),

    # ---- R3b: declared, no file ----
    ("R3b_licence_declared_only", True, "pyproject names a licence",
     ["pyproject.toml"], {"pyproject.toml": '[project]\nname = "x"\nlicense = "MIT"\n'}),
    ("R3b_licence_declared_only", True, "package.json names a licence",
     ["package.json"], {"package.json": '{"name":"x","license":"Apache-2.0"}'}),
    ("R3b_licence_declared_only", False, "package.json without a licence key",
     ["package.json"], {"package.json": '{"name":"x","version":"1.0.0"}'}),
    ("R3b_licence_declared_only", False, "pyproject mentioning a licence classifier only",
     ["pyproject.toml"],
     {"pyproject.toml": '[project]\nclassifiers = ["License :: OSI Approved :: MIT License"]\n'}),

    # ---- R4: a dependency manifest ----
    ("R4_manifest", True, "requirements.txt", ["requirements.txt"], {}),
    ("R4_manifest", True, "a split requirements file", ["requirements-dev.txt"], {}),
    ("R4_manifest", True, "an R package description", ["DESCRIPTION"], {}),
    ("R4_manifest", True, "a conda environment", ["environment.yml"], {}),
    ("R4_manifest", False, "a Dockerfile is a container recipe, not a manifest", ["Dockerfile"], {}),
    ("R4_manifest", False, "a text file that merely mentions requirements",
     ["docs/requirements_discussion.md"], {}),
    ("R4_manifest", False, "code alone", ["train.py", "README.md"], {}),

    # ---- R4b: a container recipe ----
    ("R4b_container", True, "a Dockerfile", ["Dockerfile"], {}),
    ("R4b_container", True, "a suffixed Dockerfile", ["docker/Dockerfile.gpu"], {}),
    ("R4b_container", False, "a compose file is not a recipe for an image",
     ["docker-compose.yml"], {}),

    # ---- R6: an entry point ----
    ("R6_entry", True, "a Makefile", ["Makefile", "x.py"], {}),
    ("R6_entry", True, "a root runner script", ["run_experiment.py"], {}),
    ("R6_entry", False, "a runner buried in a subdirectory is not a root runner",
     ["scripts/run_all.py"], {}),
    ("R6_entry", True, "a fenced command in the README",
     ["README.md", "t.py"],
     {"README.md": "# X\n\nInstall then:\n\n```bash\npython train.py --seed 0\n```\n"}),
    ("R6_entry", True, "an indented command in the README",
     ["README.md", "t.py"],
     {"README.md": "# X\n\nRun it:\n\n    python train.py\n\nDone.\n"}),
    ("R6_entry", False, "prose naming python is not a command",
     ["README.md", "t.py"],
     {"README.md": "# X\n\nOur code is written in python and uses make extensively.\n"}),
    # Added 2026-09-16 after the mutation test: the "whole README is scanned" mutant
    # survived because no must-not-fire case had a prose line *beginning* with a command
    # word. This is that case, and it is a real README sentence.
    ("R6_entry", False, "a requirements sentence outside any code block",
     ["README.md", "t.py"],
     {"README.md": "# X\n\nPython 3.10 is required.\nconda is recommended.\n"}),
    ("R6_entry", False, "a fenced block that is output, not a command",
     ["README.md", "t.py"],
     {"README.md": "# X\n\nResults:\n\n```\naccuracy: 0.91\nmake sure to cite us\n```\n"}),
    ("R6_entry", False, "a command in the README of a repo we did not read",
     ["README.md", "t.py"], {}),
    ("R6_entry", True, "a dollar-prompted command",
     ["README.md"], {"README.md": "```\n$ pip install -e .\n```\n"}),
    ("R6_entry", False, "DECLARED: make in a README without a Makefile does not count",
     ["README.md", "t.py"], {"README.md": "```\nmake train\n```\n"}),
    ("R6_entry", True, "a shell invocation",
     ["README.md", "t.py"], {"README.md": "```\nsh scripts/go.sh\n```\n"}),

    # ---- R7: tests ----
    ("R7_tests", True, "a tests directory", ["tests/test_a.py", "x.py"], {}),
    ("R7_tests", True, "a suffix-named test file", ["pkg/model_test.go"], {}),
    ("R7_tests", True, "conftest at the root", ["conftest.py"], {}),
    ("R7_tests", False, "a word containing test is not a test directory",
     ["testbed/x.py", "latest/y.py", "contest.py"], {}),
    ("R7_tests", False, "data used for testing is not a test",
     ["data/test.csv", "data/test/images.tar"], {}),
    ("R7_tests", False, "an evaluation split holding code is still a split, not a suite",
     ["data/test/loader.py", "train.py"], {}),
    ("R7_tests", False, "DECLARED BOUNDARY: a tests directory with no code undercounts",
     ["tests/fixtures/golden.json", "train.py"], {}),
    ("R7_tests", True, "a test suite one level down from the root",
     ["src/tests/test_model.py"], {}),

    # ---- R8: CI ----
    ("R8_ci", True, "a GitHub Actions workflow", [".github/workflows/ci.yml"], {}),
    ("R8_ci", True, "a Travis file", [".travis.yml"], {}),
    ("R8_ci", False, "an issue template is not CI", [".github/ISSUE_TEMPLATE/bug.md"], {}),
    ("R8_ci", False, "a workflow-shaped path outside .github",
     ["workflows/ci.yml"], {}),
]

# R5 returns a pair, so it gets its own table: (expected_applicable, expected_pinned)
PIN_CASES = [
    ((True, True), "a lockfile is a pin by construction", ["poetry.lock"], {}),
    ((True, True), "every requirement pinned exactly", ["requirements.txt"],
     {"requirements.txt": "numpy==1.26.0\ntorch==2.3.1\n"}),
    ((True, False), "no requirement pinned", ["requirements.txt"],
     {"requirements.txt": "numpy\ntorch>=2.0\nscipy\n"}),
    ((True, True), "exactly half pinned counts as pinned (the boundary, stated)",
     ["requirements.txt"], {"requirements.txt": "numpy==1.26.0\ntorch>=2.0\n"}),
    ((True, False), "just under half pinned", ["requirements.txt"],
     {"requirements.txt": "numpy==1.26.0\ntorch>=2.0\nscipy\n"}),
    ((True, True), "a commit-pinned VCS requirement counts", ["requirements.txt"],
     {"requirements.txt": "git+https://example.org/x@3f9a1c2d4b5e6f7a8b9c0d1e2f3a4b5c6d7e8f90\n"}),
    ((False, False), "comments and options only, nothing to pin", ["requirements.txt"],
     {"requirements.txt": "# deps\n--index-url https://example.org/simple\n"}),
    ((False, False), "no manifest text read at all", ["pyproject.toml"], {}),
    ((True, True), "a pin with a trailing comment", ["requirements.txt"],
     {"requirements.txt": "numpy==1.26.0  # tested\n"}),
]

FLOOR_CASES = [
    (True, "code, licence, manifest and a Makefile",
     ["train.py", "LICENSE", "requirements.txt", "Makefile"], {}),
    (False, "everything but the licence",
     ["train.py", "requirements.txt", "Makefile"], {}),
    (False, "everything but the manifest",
     ["train.py", "LICENSE", "Makefile"], {}),
    (False, "everything but a way in",
     ["src/train.py", "LICENSE", "requirements.txt"], {}),
    (False, "a licence, a manifest and a Makefile but no code",
     ["LICENSE", "requirements.txt", "Makefile"], {}),
]


def run():
    results = []
    failures = []
    for rung, expected, label, files, blobs in CASES:
        fn = dict((n, f) for n, _d, f in rungs.RUNGS + rungs.EXTRAS)[rung]
        got = bool(fn(files, blobs))
        if rung == "R3b_licence_declared_only" and rungs.r3_licence_file(files, blobs):
            got = False
        ok = got == expected
        results.append({"rung": rung, "sentence": label, "expected": expected,
                        "got": got, "ok": ok})
        if not ok:
            failures.append(results[-1])
    for expected, label, files, blobs in PIN_CASES:
        got = rungs.r5_pinning(files, blobs)
        ok = got == expected
        results.append({"rung": "R5_pinning", "sentence": label,
                        "expected": list(expected), "got": list(got), "ok": ok})
        if not ok:
            failures.append(results[-1])
    for expected, label, files, blobs in FLOOR_CASES:
        got = rungs.code_repo(files, blobs)["FLOOR"]
        ok = got == expected
        results.append({"rung": "FLOOR", "sentence": label, "expected": expected,
                        "got": got, "ok": ok})
        if not ok:
            failures.append(results[-1])
    return results, failures


if __name__ == "__main__":
    results, failures = run()
    out = {
        "note": "Fixtures for the rungs of session 162. Hand-made cases, no real repository.",
        "written": "2026-09-16, before any repository was cloned",
        "limit": ("A fixture checks that a rule computes what its author says. It cannot "
                  "check that the author wrote the right sentence — session 161's finding, "
                  "carried here unresolved."),
        "cases": len(results),
        "failed": len(failures),
        "results": results,
    }
    path = ("artifacts/2026-09-16-an-address-is-not-an-artifact/data/fixture-check.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print(f"{len(results)} fixtures, {len(failures)} failed -> {path}")
    for f in failures:
        print("  FAIL", f["rung"], "|", f["sentence"], "| expected", f["expected"], "got", f["got"])
    sys.exit(1 if failures else 0)
