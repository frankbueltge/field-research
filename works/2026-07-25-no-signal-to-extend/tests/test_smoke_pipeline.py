"""
End-to-end smoke test: filter (tokenizer + corpus rules) -> metrics -> envelope, on
SYNTHETIC in-memory data constructed here. None of this data is fabricated as real
measurement -- it exists only to exercise the pipeline's wiring and arithmetic before
any real harvest happens. Real strings are used in exactly one place (a handful of
actual marker "style" words, loaded from the real provenance CSV) purely as filler
tokens, so the marker channel has something non-trivial to count; this does not
constitute a claim about any real corpus.
"""
import random as pyrandom
import unittest

import _pathfix  # noqa: F401
from tokenizer import tokenize
from filter_corpus import half_year_unit, MIN_TOKENS
import metrics as metrics_mod
import envelope as envelope_mod

WINDOW_SIZE = 220   # distinct words per abstract, freq-decaying (see below)
VOCAB_SPAN = 6000    # modulo space words are drawn from; keeps a cell's abstracts
                     # non-overlapping (n_abstracts * WINDOW_SIZE << VOCAB_SPAN)
STRATA = ("cs.CL", "cs.CV", "math.NT")

_LETTERS = "abcdefghijklmnopqrstuvwxyz"


def _letters_word(prefix, n, suffix_len=4):
    """A purely-alphabetic synthetic word: prefix + base-26 digits. The real
    tokenizer's `[a-z]+` pattern stops at the first digit, so fixture vocabulary
    MUST be letters-only or it silently collapses (e.g. "lex00000" and "lex00001"
    both tokenize down to just "lex") -- this generator exists to avoid that trap.
    """
    digits = []
    m = n
    for _ in range(suffix_len):
        digits.append(_LETTERS[m % 26])
        m //= 26
    return prefix + "".join(reversed(digits))


COMMON_VOCAB = [_letters_word("cm", i) for i in range(40)]


def _load_small_marker_sample():
    marker_set = metrics_mod.load_marker_set(metrics_mod.default_marker_csv())
    return sorted(marker_set)[:5]


def _decaying_freq_tokens(base, jitter):
    """WINDOW_SIZE distinct words at frequency ~ 30*jitter / rank**0.7 -- a real
    decaying rank-frequency profile (not flat), so the Zipf-tail slope has actual
    non-degenerate structure past rank 100, and varies with `jitter` (which the
    caller ties to the unit index) instead of being identical across every cell.
    A flat (all-frequency-1) profile was tried first and produced an exact-zero
    slope in every cell, which zeroed the envelope's residual variance and broke
    the prediction-interval division -- this is why the profile needs real decay.
    """
    tokens = []
    for rank in range(1, WINDOW_SIZE + 1):
        word = _letters_word("lx", (base + rank) % VOCAB_SPAN)
        freq = max(1, round(30 * jitter / (rank ** 0.7)))
        tokens.extend([word] * freq)
    return tokens


def _make_corpus_rows(stratum, marker_sample):
    rows = []
    for x, unit in enumerate(envelope_mod.UNITS):
        rng = pyrandom.Random(f"smoke-fixture:{stratum}:{unit}")
        n_abstracts = rng.randint(6, 9)
        for k in range(n_abstracts):
            base = (x * 97 + k) * WINDOW_SIZE
            jitter = rng.uniform(0.8, 1.2)
            decaying_tokens = _decaying_freq_tokens(base, jitter)
            common_tokens = []
            for w in COMMON_VOCAB:
                reps = rng.randint(0, 4)
                common_tokens.extend([w] * reps)
            marker_count = rng.randint(0, 3)
            marker_tokens = rng.choices(marker_sample, k=marker_count) if marker_sample else []
            tokens = decaying_tokens + common_tokens + marker_tokens
            rng.shuffle(tokens)
            abstract = " ".join(tokens) + "."

            # Round-trip through the real tokenizer + the real MIN_TOKENS rule, the
            # way filter_corpus.py would.
            tok_count = len(tokenize(abstract))
            assert tok_count >= MIN_TOKENS, f"fixture abstract too short: {tok_count}"

            created = f"{unit[:4]}-{'03' if unit.endswith('H1') else '09'}-15"
            assert half_year_unit(created) == unit
            rid = f"{stratum}-{unit}-{k:02d}"
            rows.append({"id": rid, "created": created, "unit": unit, "abstract": abstract})
    return rows


class TestSmokeEndToEnd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.marker_set = metrics_mod.load_marker_set(metrics_mod.default_marker_csv())
        cls.marker_sample = sorted(cls.marker_set)[:5]
        cls.stratum_metrics = {}
        for stratum in STRATA:
            rows = _make_corpus_rows(stratum, cls.marker_sample)
            unit_results = metrics_mod.compute_stratum(stratum, rows, cls.marker_set)
            cls.stratum_metrics[stratum] = {
                "stratum": stratum,
                "marker_style_word_count": len(cls.marker_set),
                "units": unit_results,
            }

    def test_metrics_cover_all_23_units_per_stratum(self):
        for stratum in STRATA:
            units = [u["unit"] for u in self.stratum_metrics[stratum]["units"]]
            self.assertEqual(sorted(units), sorted(envelope_mod.UNITS))
            self.assertEqual(len(units), 23)

    def test_zipf_is_computable_in_every_cell(self):
        # By construction every cell has >= 6*220 = 1320 >= 300 distinct tokens.
        for stratum in STRATA:
            for u in self.stratum_metrics[stratum]["units"]:
                self.assertFalse(u["zipf_slope"]["non_computable"], f"{stratum} {u['unit']}")

    def test_envelope_build_results_runs_without_error(self):
        results = envelope_mod.build_results(self.stratum_metrics)
        self.assertIn("verdicts", results)
        self.assertIn("cs.CL", results["verdicts"])
        self.assertIn("cs.CV", results["verdicts"])
        self.assertIn("math_nt_marker_channel_valid", results["control"])

        for stratum in STRATA:
            rep = results["strata"][stratum]
            for metric_key in envelope_mod.MARGIN_METRIC_DIRECTIONS:
                mrep = rep["metrics"][metric_key]
                self.assertEqual(len(mrep["rows"]), 23)
                self.assertIn(
                    mrep["label"],
                    ("NO-ANOMALY", "CONTINUE", "NEW-ONSET", "PLATEAU", "REVERSE", "RESIDUAL", "NON-DECIDABLE"),
                )
            self.assertIn("a_validity_window_2023h1_2026h1", rep["marker"])
            self.assertIn("context_whole_cell_rate", rep["marker"])
            # quadratic sensitivity table present, with its own label per metric
            for metric_key in envelope_mod.MARGIN_METRIC_DIRECTIONS:
                self.assertIn(
                    rep["quadratic_sensitivity"][metric_key]["label"],
                    ("NO-ANOMALY", "CONTINUE", "NEW-ONSET", "PLATEAU", "REVERSE", "RESIDUAL", "NON-DECIDABLE"),
                )

        for stratum in ("cs.CL", "cs.CV"):
            v = results["verdicts"][stratum]
            self.assertIn("verdict", v)
            self.assertIsInstance(v["kill_condition_met"], bool)

    def test_markdown_summary_renders(self):
        results = envelope_mod.build_results(self.stratum_metrics)
        md = envelope_mod.render_markdown(results)
        self.assertIn("# Homogenization Dossier", md)
        self.assertIn("cs.CL", md)
        self.assertIn("math.NT", md)
        self.assertIn("Verdict", md)

    def test_results_are_json_serializable(self):
        import json
        results = envelope_mod.build_results(self.stratum_metrics)
        json.dumps(results)  # must not raise


if __name__ == "__main__":
    unittest.main()
