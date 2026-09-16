"""The rungs — mechanical coding rules for what is behind a declared address.

Session 162, 2026-09-16. Every rule here is a pure function of (a) the list of paths in a
repository's default-branch tree and (b) the text of a small, fixed set of selected files.
No rule calls a model, and no rule looks at anything outside those two inputs.

Frozen at the pre-registration. Once the first repository has been cloned, a rule is not
edited; a rule found defective afterwards is filed as a defect beside its number, and the
number stands (record floor, protocol v4 §7).
"""

import json
import re

# ---------------------------------------------------------------- helpers

SOURCE_EXT = {
    "py", "ipynb", "js", "ts", "tsx", "jsx", "c", "cc", "cpp", "cxx", "h", "hpp",
    "java", "go", "rs", "jl", "r", "m", "mm", "sh", "bash", "zsh", "scala", "rb",
    "swift", "kt", "kts", "lua", "f90", "f95", "f03", "for", "cu", "cuh", "pl",
    "php", "cs", "hs", "ml", "clj", "erl", "ex", "exs", "dart", "sql", "vue",
    "svelte", "mat", "sas", "do", "stan", "nb", "wl",
}

BOILERPLATE_RE = re.compile(
    r"^(readme|licen[cs]e|copying|unlicense|contributing|code_of_conduct|security"
    r"|citation|authors|changelog|codeowners|notice|acknowledgements?"
    r"|\.gitignore|\.gitattributes|\.gitmodules|\.gitkeep)"
    r"([.\-_].*)?$",
    re.I,
)

LICENCE_BASENAME_RE = re.compile(
    r"^(licen[cs]e|copying|unlicense|copyright)([.\-_].*)?$", re.I
)

MANIFEST_BASENAMES = {
    "requirements.txt", "pyproject.toml", "setup.py", "setup.cfg", "pipfile",
    "poetry.lock", "uv.lock", "pipfile.lock", "environment.yml", "environment.yaml",
    "conda.yml", "conda.yaml", "package.json", "cargo.toml", "go.mod", "gemfile",
    "description", "renv.lock", "pom.xml", "build.gradle", "build.gradle.kts",
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "conda-lock.yml",
}
MANIFEST_PATTERNS = [
    re.compile(r"^requirements[.\-_][\w.\-]*\.txt$", re.I),
    re.compile(r"^requirements\.txt$", re.I),
]

LOCKFILES = {
    "poetry.lock", "uv.lock", "pipfile.lock", "package-lock.json", "yarn.lock",
    "pnpm-lock.yaml", "renv.lock", "conda-lock.yml", "cargo.lock",
}

CONTAINER_BASENAMES_RE = re.compile(r"^(dockerfile|containerfile)([.\-_].*)?$", re.I)

CI_PATH_RE = re.compile(
    r"(^\.github/workflows/[^/]+\.ya?ml$)|(^\.travis\.yml$)|(^\.gitlab-ci\.yml$)"
    r"|(^azure-pipelines\.ya?ml$)|(^Jenkinsfile$)|(^\.circleci/config\.ya?ml$)"
    r"|(^\.drone\.yml$)|(^appveyor\.yml$)",
    re.I,
)

TEST_DIR_NAMES = {"test", "tests", "testing", "unittest", "unittests"}
# A directory named ``test`` directly under one of these is an evaluation split, not a
# test suite. This is the known confounder of the domain: machine-learning repositories
# ship ``data/test/`` constantly, and counting it as a test suite would be a lie.
SPLIT_PARENTS = {
    "data", "dataset", "datasets", "split", "splits", "images", "image", "img",
    "assets", "resources", "corpus", "corpora", "benchmark", "benchmarks", "input",
    "inputs", "raw",
}
TEST_FILE_RE = re.compile(
    r"^(test_[\w.\-]+\.(py|js|ts|rb)|[\w.\-]+_test\.(py|go|js|ts|rb)|conftest\.py"
    r"|[\w.\-]+Test\.java|test[\w.\-]*\.m)$"
)

ROOT_RUNNER_RE = re.compile(
    r"^(run|main|train|demo|start|launch|experiment|reproduce|eval|evaluate)"
    r"[\w.\-]*\.(py|sh|ipynb)$",
    re.I,
)

# A command an entry-point line may invoke. Anchored at the start of a code-block line.
# ``make`` and ``go`` are deliberately absent: they are ordinary English verbs, and a
# fenced block of program output saying "make sure to cite us" would otherwise count as
# a command a reader can copy. A repository whose way in really is ``make`` is caught by
# the Makefile clause of R6 instead.
COMMAND_RE = re.compile(
    r"^\s*(?:\$|>|#\s*)?\s*(?:sudo\s+)?"
    r"(python3?|bash|sh|zsh|docker|docker-compose|pip3?|uv|pipx|conda|mamba"
    r"|poetry|npm|yarn|pnpm|node|cargo|julia|Rscript|sbatch|srun|accelerate"
    r"|torchrun|deepspeed|streamlit|uvicorn|jupyter|pytest|tox|gradle|mvn|dotnet)"
    r"(\s|$)"
)

FENCE_RE = re.compile(r"^\s*(```|~~~)")


def basename(path):
    return path.rsplit("/", 1)[-1]


def ext(path):
    b = basename(path)
    return b.rsplit(".", 1)[-1].lower() if "." in b else ""


def code_block_lines(text):
    """Lines inside fenced code blocks, plus four-space-indented blocks.

    A README that shows its command in a fenced block is the common case; some show it
    indented instead. Both count, and nothing outside a block does: prose saying the word
    "python" is not a command a reader can copy.
    """
    out = []
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            out.append(line)
        elif line.startswith("    ") and line.strip():
            out.append(line[4:])
    return out


# ---------------------------------------------------------------- the rungs

def r1_content(files, blobs=None):
    """Something beyond boilerplate is in the tree."""
    return any(not BOILERPLATE_RE.match(basename(p)) for p in files)


def r2_code(files, blobs=None):
    """At least one file with a source-code extension."""
    return any(ext(p) in SOURCE_EXT for p in files)


def r3_licence_file(files, blobs=None):
    """A licence file exists somewhere in the tree."""
    return any(LICENCE_BASENAME_RE.match(basename(p)) for p in files)


def r3b_licence_declared(files, blobs):
    """A licence is named in pyproject.toml or package.json, with no licence file.

    Reported beside R3, never folded into it: a declaration in a manifest is a weaker
    grant than a licence text, and a reader who wants to reuse the code has to take the
    author's word for which version of which licence is meant.
    """
    blobs = blobs or {}
    for path, text in blobs.items():
        b = basename(path).lower()
        if b == "pyproject.toml" and re.search(r"(?m)^\s*license\s*=", text):
            return True
        if b == "package.json":
            try:
                if json.loads(text).get("license"):
                    return True
            except Exception:
                if re.search(r'"license"\s*:', text):
                    return True
    return False


def _is_manifest(path):
    b = basename(path).lower()
    if b in MANIFEST_BASENAMES:
        return True
    return any(p.match(b) for p in MANIFEST_PATTERNS)


def r4_manifest(files, blobs=None):
    """A dependency or environment manifest exists. Container recipes are NOT counted here."""
    return any(_is_manifest(p) for p in files)


def r4b_container(files, blobs=None):
    """A container recipe exists (Dockerfile / Containerfile)."""
    return any(CONTAINER_BASENAMES_RE.match(basename(p)) for p in files)


def _requirements_texts(blobs):
    out = []
    for path, text in (blobs or {}).items():
        b = basename(path).lower()
        if b == "requirements.txt" or MANIFEST_PATTERNS[0].match(b):
            out.append(text)
    return out


def r5_pinning(files, blobs):
    """Pinned dependencies. Returns (applicable, pinned).

    Applicable when a lockfile is present or a requirements.txt was read. A lockfile is
    a pin by construction. Otherwise at least half of the direct requirement lines must
    carry an exact version (``==``, ``===``) or a commit-pinned VCS reference.
    """
    if any(basename(p).lower() in LOCKFILES for p in files):
        return True, True
    texts = _requirements_texts(blobs)
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
    return True, pinned * 2 >= total


def r6_entry_point(files, blobs):
    """A command a stranger can copy, or an obvious root runner, or a Makefile."""
    if any(basename(p).lower() in ("makefile", "gnumakefile", "justfile") for p in files):
        return True
    if any("/" not in p and ROOT_RUNNER_RE.match(p) for p in files):
        return True
    for path, text in (blobs or {}).items():
        if basename(path).lower().startswith("readme"):
            if any(COMMAND_RE.match(line) for line in code_block_lines(text)):
                return True
    return False


def r7_tests(files, blobs=None):
    """Tests exist in the tree.

    Either a file named like a test, or a *code* file under a directory named like a test
    suite. The code requirement and the split-parent exclusion are both deliberate, and
    both undercount: a ``tests/`` directory holding only fixtures does not fire. Declared
    in the pre-registration as a boundary, not discovered afterwards.
    """
    for p in files:
        if TEST_FILE_RE.match(basename(p)):
            return True
        parts = p.split("/")
        for i, part in enumerate(parts[:-1]):
            if part.lower() not in TEST_DIR_NAMES:
                continue
            if i > 0 and parts[i - 1].lower() in SPLIT_PARENTS:
                continue
            if ext(p) in SOURCE_EXT:
                return True
    return False


def r8_ci(files, blobs=None):
    """A continuous-integration configuration exists."""
    return any(CI_PATH_RE.match(p) for p in files)


RUNGS = [
    ("R1_content", "something beyond boilerplate", r1_content),
    ("R2_code", "a file with a source-code extension", r2_code),
    ("R3_licence", "a licence file", r3_licence_file),
    ("R4_manifest", "a dependency or environment manifest", r4_manifest),
    ("R6_entry", "a command a stranger can copy", r6_entry_point),
    ("R7_tests", "tests", r7_tests),
    ("R8_ci", "a CI configuration", r8_ci),
]

EXTRAS = [
    ("R3b_licence_declared_only", "a licence named in a manifest, no licence file", r3b_licence_declared),
    ("R4b_container", "a container recipe", r4b_container),
]

FLOOR_RUNGS = ["R2_code", "R3_licence", "R4_manifest", "R6_entry"]


def code_repo(files, blobs):
    """Apply every rung to one repository. Returns a dict of rung name -> bool/None."""
    out = {}
    for name, _desc, fn in RUNGS:
        out[name] = bool(fn(files, blobs))
    for name, _desc, fn in EXTRAS:
        out[name] = bool(fn(files, blobs))
    if out["R3_licence"]:
        out["R3b_licence_declared_only"] = False
    applicable, pinned = r5_pinning(files, blobs)
    out["R5_pinning_applicable"] = applicable
    out["R5_pinned"] = pinned if applicable else None
    out["FLOOR"] = all(out[r] for r in FLOOR_RUNGS)
    return out
