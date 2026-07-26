"""Adds this draft's scripts/ and the parent instrument's scripts/ to sys.path so tests
can `import extract_units`, `import pools`, `import metrics_units`, and — for agreement
tests — the parent's own `tokenizer` / `metrics` modules, without installing a package.
Imported for its side effect only."""
import os
import sys

_TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
_DRAFT_DIR = os.path.dirname(_TESTS_DIR)
_REPO_ROOT = os.path.dirname(os.path.dirname(_DRAFT_DIR))

_OWN_SCRIPTS_DIR = os.path.join(_DRAFT_DIR, "scripts")
_PARENT_SCRIPTS_DIR = os.path.join(
    _REPO_ROOT, "works", "2026-07-25-no-signal-to-extend", "scripts"
)

for _p in (_OWN_SCRIPTS_DIR, _PARENT_SCRIPTS_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)
