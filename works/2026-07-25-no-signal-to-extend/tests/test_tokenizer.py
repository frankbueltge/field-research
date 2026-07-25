import unittest

import _pathfix  # noqa: F401
from tokenizer import tokenize


class TestTokenizer(unittest.TestCase):
    def test_nfkc_and_lowercase(self):
        # U+FF41 FULLWIDTH LATIN SMALL LETTER A + uppercase ASCII; NFKC folds the
        # fullwidth form to ASCII 'a', then lowercasing handles 'BC'.
        text = "ａBC"
        self.assertEqual(tokenize(text), ["abc"])

    def test_url_removal(self):
        text = "see https://example.com/path?q=1 for details"
        self.assertEqual(tokenize(text), ["see", "for", "details"])

    def test_url_removal_no_trailing_leak(self):
        text = "prefix http://x.io/a-b more"
        self.assertEqual(tokenize(text), ["prefix", "more"])

    def test_inline_math_removal(self):
        text = "the value $x^2 + y^2$ is bounded"
        self.assertEqual(tokenize(text), ["the", "value", "is", "bounded"])

    def test_inline_math_non_greedy(self):
        # Two separate math spans must not be merged into one greedy match.
        text = "$a$ and $b$ remain separate"
        self.assertEqual(tokenize(text), ["and", "remain", "separate"])

    def test_texcmd_removal(self):
        text = r"we use \alpha and \textbf{bold} notation"
        # \textbf is stripped; the brace-delimited argument has no letters removed
        # from it by the texcmd rule (braces aren't backslash-letters), so "bold"
        # survives as its own token.
        self.assertEqual(tokenize(text), ["we", "use", "and", "bold", "notation"])

    def test_hyphenated_token(self):
        text = "a state-of-the-art model"
        self.assertEqual(tokenize(text), ["a", "state-of-the-art", "model"])

    def test_apostrophe_token(self):
        text = "it isn't obvious"
        self.assertEqual(tokenize(text), ["it", "isn't", "obvious"])

    def test_digits_and_punctuation_are_not_tokens(self):
        text = "model achieves 95.3% accuracy, (see Table 2)."
        self.assertEqual(tokenize(text), ["model", "achieves", "accuracy", "see", "table"])

    def test_combined_pipeline(self):
        text = r"See https://arxiv.org/abs/1234.5678 for $\mathcal{L}$ and \emph{proof}."
        self.assertEqual(tokenize(text), ["see", "for", "and", "proof"])

    def test_empty_string(self):
        self.assertEqual(tokenize(""), [])


if __name__ == "__main__":
    unittest.main()
