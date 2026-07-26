"""Blocking agreement tests (PREREGISTRATION.md §3): MTLD, hapax share, the Zipf-tail
diagnostic and the cosine primitive must return EXACTLY what the parent instrument's
functions return, on at least three fixtures, one of which is a real unit's 600-token
prefix. `metrics_units.py` imports these functions from the parent unchanged (does not
reimplement them), so agreement is structural; these tests exercise that import path
directly rather than merely asserting it exists."""
import json
import os
import unittest

import _pathfix  # noqa: F401
import metrics_units as mu
from metrics import (  # the parent's own functions, imported independently here
    mtld_bidirectional as parent_mtld,
    hapax_share as parent_hapax,
    zipf_tail_slope as parent_zipf,
    _cosine as parent_cosine,
)

_UNITS_PATH = mu.UNITS_PATH


def _fixture_tokens():
    fixtures = []
    # Fixture 1: short synthetic vocabulary, repeated with variation.
    fixtures.append(
        (["the", "quick", "brown", "fox"] * 20 + ["jumps", "over", "lazy", "dog"] * 5)
    )
    # Fixture 2: larger synthetic vocabulary, skewed frequency (zipfian-ish).
    toks = []
    for i in range(1, 60):
        toks.extend([f"type{i}"] * (60 - i))
    fixtures.append(toks)
    # Fixture 3: a REAL unit's 600-token prefix, loaded from the frozen extraction.
    with open(_UNITS_PATH, "r", encoding="utf-8") as f:
        units = [json.loads(line) for line in f if line.strip()]
    real_unit = next(u for u in units if u["n_tokens"] >= 600)
    fixtures.append(real_unit["tokens"][:600])
    return fixtures


class TestMTLDAgreement(unittest.TestCase):
    def test_agrees_on_three_fixtures(self):
        for tokens in _fixture_tokens():
            self.assertEqual(
                mu.mtld_bidirectional(tokens, threshold=mu.MTLD_THRESHOLD),
                parent_mtld(tokens, threshold=0.72),
            )


class TestHapaxShareAgreement(unittest.TestCase):
    def test_agrees_on_three_fixtures(self):
        for tokens in _fixture_tokens():
            self.assertEqual(mu.parent_hapax_share(tokens), parent_hapax(tokens))


class TestZipfSlopeAgreement(unittest.TestCase):
    def test_agrees_on_three_fixtures(self):
        for tokens in _fixture_tokens():
            got = mu.zipf_tail_slope(tokens)
            want = parent_zipf(tokens)
            self.assertEqual(got, want)


class TestCosineAgreement(unittest.TestCase):
    def test_agrees_on_normalized_fixtures(self):
        fixtures = [
            ({"x": 0.6, "y": 0.8}, {"x": 0.6, "y": 0.8}),
            ({"x": 1.0}, {"y": 1.0}),
            ({"a": 0.5, "b": 0.5, "c": 0.7071067811865476}, {"a": 0.5, "b": -0.5, "c": 0.7071067811865476}),
        ]
        for va, vb in fixtures:
            self.assertEqual(mu._cosine(va, vb), parent_cosine(va, vb))


if __name__ == "__main__":
    unittest.main()
