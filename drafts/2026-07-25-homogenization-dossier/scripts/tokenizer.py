"""
scripts/tokenizer.py — the §2 tokenizer (PREREGISTRATION.md), fixed and unit-tested.

Pipeline, in order:
  1. Unicode NFKC normalization.
  2. Lowercase.
  3. Remove URLs (`https?://\\S+`).
  4. Remove inline TeX math (`$...$`, non-greedy).
  5. Remove TeX commands (a backslash followed by one or more letters).
  6. Tokenize with `[a-z]+(?:[-'][a-z]+)*`.

No parameters, no knobs: this is a pre-registered, fixed procedure. Any change to this
function after the pre-registration lock invalidates runs that depend on it.
"""
import re
import unicodedata

_URL_RE = re.compile(r"https?://\S+")
_MATH_RE = re.compile(r"\$.*?\$")
_TEXCMD_RE = re.compile(r"\\[a-zA-Z]+")
_TOKEN_RE = re.compile(r"[a-z]+(?:[-'][a-z]+)*")


def tokenize(text):
    """Tokenize `text` per PREREGISTRATION.md §2. Returns a list of token strings."""
    normalized = unicodedata.normalize("NFKC", text)
    lowered = normalized.lower()
    no_urls = _URL_RE.sub(" ", lowered)
    no_math = _MATH_RE.sub(" ", no_urls)
    no_texcmd = _TEXCMD_RE.sub(" ", no_math)
    return _TOKEN_RE.findall(no_texcmd)
