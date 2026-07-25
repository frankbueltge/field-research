"""Adds scripts/ to sys.path so tests can `import tokenizer`, `import metrics`, etc.
without installing a package. Imported for its side effect only."""
import os
import sys

_SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)
