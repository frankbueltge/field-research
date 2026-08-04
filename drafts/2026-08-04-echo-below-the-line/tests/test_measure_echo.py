#!/usr/bin/env python3
"""
Self-test for scripts/measure_echo.py.

Standard library unittest only. Builds a tiny synthetic pool by hand and
checks Rule A / Rule B against answers worked out manually, including:
  - a title caught by Rule B (near-duplicate cluster, >=3 domains) but NOT
    by Rule A (no shared verbatim 6-gram across >=3 domains);
  - a 2-domain cluster that must NOT count under either rule's >=3-domain
    bar.

Run with: python3 tests/test_measure_echo.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "scripts"))

import measure_echo as me  # noqa: E402


def make_recs(titles_domains):
    """titles_domains: list of (title, domain, url) -> normalised records."""
    recs = []
    for title, domain, url in titles_domains:
        norm = me.normalise_title(title)
        toks = me.tokenise(norm)
        recs.append({
            "url": url,
            "domain": domain,
            "title": title,
            "norm": norm,
            "tokens": toks,
            "token_set": frozenset(toks),
        })
    return recs


class TestNormalisation(unittest.TestCase):
    def test_lowercase_and_punctuation_collapse(self):
        self.assertEqual(
            me.normalise_title("Senate Panel Advances Blanche Nomination!"),
            "senate panel advances blanche nomination",
        )

    def test_non_alnum_run_collapses_to_single_space(self):
        self.assertEqual(
            me.normalise_title("A---B,,,C   D"),
            "a b c d",
        )

    def test_empty_and_none(self):
        self.assertEqual(me.normalise_title(""), "")
        self.assertEqual(me.normalise_title(None), "")


class TestShingles(unittest.TestCase):
    def test_exact_six_tokens_one_shingle(self):
        toks = "one two three four five six".split()
        self.assertEqual(me.shingles(toks), [tuple(toks)])

    def test_seven_tokens_two_shingles(self):
        toks = "one two three four five six seven".split()
        out = me.shingles(toks)
        self.assertEqual(len(out), 2)
        self.assertEqual(out[0], tuple(toks[0:6]))
        self.assertEqual(out[1], tuple(toks[1:7]))

    def test_fewer_than_six_tokens_no_shingle(self):
        toks = "one two three".split()
        self.assertEqual(me.shingles(toks), [])


class TestJaccard(unittest.TestCase):
    def test_identical_sets(self):
        s = frozenset({"a", "b", "c"})
        self.assertEqual(me.jaccard(s, s), 1.0)

    def test_disjoint_sets(self):
        self.assertEqual(
            me.jaccard(frozenset({"a"}), frozenset({"b"})), 0.0
        )

    def test_partial_overlap(self):
        a = frozenset({"a", "b", "c"})
        b = frozenset({"b", "c", "d"})
        # intersection = {b,c} = 2, union = {a,b,c,d} = 4
        self.assertAlmostEqual(me.jaccard(a, b), 0.5)

    def test_both_empty(self):
        self.assertEqual(me.jaccard(frozenset(), frozenset()), 0.0)


class TestRuleAAndB(unittest.TestCase):
    """
    Synthetic pool, worked out by hand:

    Group 1 (verbatim echo, 3 domains) -- same 6-gram title on 3 domains:
      d1: "senators reach deal on border security funding today"
      d2: "senators reach deal on border security funding today"
      d3: "senators reach deal on border security funding today"
      These share a 6-token shingle e.g. "senators reach deal on border
      security" across 3 distinct domains -> Rule A SHOULD catch all three.
      Their token sets are identical -> Jaccard 1.0 -> Rule B clusters them
      too, at every threshold, and the cluster has 3 domains -> counts.

    Group 2 (paraphrase, 3 domains, NOT verbatim) -- same 10-word bag,
    reordered per domain, so token-set Jaccard is 1.0 (identical bag of
    words) but no contiguous 6-token window is shared by any pair (order
    was chosen by search specifically to break every 6-gram overlap; see
    test_group2_paraphrases_share_no_common_6gram_across_all_three):
      d4: "mayor announces new budget plan for city schools this year"
      d5: "new budget plan for schools city mayor announces this year"
      d6: "city schools mayor announces this year new budget plan for"
      Rule A must miss this group entirely (zero shared 6-gram => no echo
      phrase, regardless of domain count). Rule B, at a loose-enough
      threshold, clusters them (Jaccard token-set similarity is 1.0) and
      the cluster spans 3 domains -> counts. This is the canonical
      "paraphrase escapes Rule A but not Rule B" case.

    Group 3 (2-domain near-duplicate, must NOT count):
      d7: "wildfire forces evacuation of coastal town overnight"
      d8: "wildfire forces evacuation of coastal town overnight"
      Identical title, but only 2 distinct domains -> below the >=3-domain
      bar -> must NOT count under Rule A or Rule B at any threshold.

    Group 4 (unrelated singletons, short title):
      d9: "stocks rise" (2 tokens, < 6, no shingle possible)
    """

    @classmethod
    def setUpClass(cls):
        cls.pool_defs = [
            ("Senators reach deal on border security funding today.",
             "site-a.example", "http://site-a.example/1"),
            ("Senators reach deal on border security funding today.",
             "site-b.example", "http://site-b.example/1"),
            ("Senators reach deal on border security funding today.",
             "site-c.example", "http://site-c.example/1"),

            ("Mayor announces new budget plan for city schools this year",
             "site-d.example", "http://site-d.example/1"),
            ("New budget plan for schools city mayor announces this year",
             "site-e.example", "http://site-e.example/1"),
            ("City schools mayor announces this year new budget plan for",
             "site-f.example", "http://site-f.example/1"),

            ("Wildfire forces evacuation of coastal town overnight.",
             "site-g.example", "http://site-g.example/1"),
            ("Wildfire forces evacuation of coastal town overnight.",
             "site-h.example", "http://site-h.example/1"),

            ("Stocks rise.",
             "site-i.example", "http://site-i.example/1"),
        ]
        cls.recs = make_recs(cls.pool_defs)
        cls.n = len(cls.recs)
        cls.token_sets = [r["token_set"] for r in cls.recs]
        cls.sims = me.build_similarity_pairs(cls.token_sets)

    def test_group1_shares_a_verbatim_6gram_across_3_domains(self):
        # sanity: indices 0,1,2 must share at least one 6-gram
        sh0 = set(me.shingles(self.recs[0]["tokens"]))
        sh1 = set(me.shingles(self.recs[1]["tokens"]))
        sh2 = set(me.shingles(self.recs[2]["tokens"]))
        common = sh0 & sh1 & sh2
        self.assertTrue(len(common) > 0)

    def test_group2_paraphrases_share_no_common_6gram_across_all_three(self):
        # constructed so groups 3-5 (paraphrase group) have no single
        # 6-gram shingle common to all three domains (word order/tense
        # differs enough to break at least one pairwise match)
        sh3 = set(me.shingles(self.recs[3]["tokens"]))
        sh4 = set(me.shingles(self.recs[4]["tokens"]))
        sh5 = set(me.shingles(self.recs[5]["tokens"]))
        common_all_three = sh3 & sh4 & sh5
        self.assertEqual(len(common_all_three), 0)

    def test_rule_a_catches_group1_not_group2(self):
        result = me.rule_a(self.recs)
        covered = me.rule_a_covered_titles(self.recs)
        # group 1 (indices 0,1,2) caught by Rule A
        self.assertIn(0, covered)
        self.assertIn(1, covered)
        self.assertIn(2, covered)
        # group 2 (indices 3,4,5) NOT caught by Rule A (no common 6-gram
        # across 3 domains)
        self.assertNotIn(3, covered)
        self.assertNotIn(4, covered)
        self.assertNotIn(5, covered)
        # group 3 (indices 6,7) verbatim duplicate but only 2 domains ->
        # NOT caught (fails the >=3-domain bar even though the shingle
        # exists)
        self.assertNotIn(6, covered)
        self.assertNotIn(7, covered)
        # short title (index 8) has no shingle at all -> not covered
        self.assertNotIn(8, covered)
        # echo index A = 3 titles / 9 total
        self.assertAlmostEqual(result["echo_index"], 3 / 9)
        self.assertEqual(result["titles_in_echo"], 3)
        self.assertEqual(result["short_titles_lt_6_tokens"], 1)

    def test_rule_b_catches_group2_at_threshold_0_7(self):
        t = 0.7
        res = me.rule_b_for_threshold(self.recs, self.sims, t, self.n)
        dsu = me.DSU(self.n)
        for (i, j), s in self.sims.items():
            if s >= t:
                dsu.union(i, j)
        # group 2 (indices 3,4,5) must all land in the same cluster at 0.7
        r3, r4, r5 = dsu.find(3), dsu.find(4), dsu.find(5)
        self.assertEqual(r3, r4)
        self.assertEqual(r4, r5)
        # that cluster spans 3 distinct domains -> counts
        doms = {self.recs[i]["domain"] for i in (3, 4, 5)}
        self.assertEqual(len(doms), 3)
        # echo index B at 0.7 must be strictly greater than echo index A,
        # because group 2 is now included and group 1 still is
        a_index = me.rule_a(self.recs)["echo_index"]
        self.assertGreater(res["echo_index"], a_index)

    def test_group3_two_domain_duplicate_never_counts(self):
        # even at the loosest swept threshold, a 2-domain cluster must not
        # count
        for t in me.THRESHOLDS:
            res = me.rule_b_for_threshold(self.recs, self.sims, t, self.n)
            dsu = me.DSU(self.n)
            for (i, j), s in self.sims.items():
                if s >= t:
                    dsu.union(i, j)
            root6 = dsu.find(6)
            members = [i for i in range(self.n) if dsu.find(i) == root6]
            doms = {self.recs[i]["domain"] for i in members}
            if 7 in members:
                # group 3 clustered together but only 2 domains -> must
                # not be a counting cluster
                self.assertLess(len(doms), me.MIN_ECHO_DOMAINS)

    def test_short_title_excluded_from_rule_a_but_eligible_for_rule_b(self):
        # index 8 "stocks rise" has < 6 tokens: cannot appear in Rule A's
        # covered set (structurally impossible), but IS a normal member of
        # the Rule B similarity computation (it just has no strong link to
        # anything else in this synthetic pool, so it stays a singleton).
        covered = me.rule_a_covered_titles(self.recs)
        self.assertNotIn(8, covered)
        self.assertEqual(len(self.recs[8]["tokens"]), 2)

    def test_find_examples_gap_pairs_are_cross_domain_and_counting(self):
        a_covered = me.rule_a_covered_titles(self.recs)
        examples = me.find_examples(self.recs, self.sims, 0.7, a_covered,
                                     self.n, max_examples=12)
        self.assertTrue(len(examples) > 0)
        for ex in examples:
            self.assertNotEqual(ex["domain_1"], ex["domain_2"])
            # at least one side not individually caught by Rule A
            self.assertTrue(
                not ex["caught_by_rule_a_1"] or not ex["caught_by_rule_a_2"]
            )

    def test_deterministic_repeat_run(self):
        # running rule_a and rule_b twice on the same input must give
        # identical results (no randomness, no reliance on dict/set
        # iteration order affecting the numeric outcome)
        r1 = me.rule_a(self.recs)
        r2 = me.rule_a(self.recs)
        self.assertEqual(r1, r2)
        b1 = me.rule_b_for_threshold(self.recs, self.sims, 0.7, self.n)
        b2 = me.rule_b_for_threshold(self.recs, self.sims, 0.7, self.n)
        self.assertEqual(b1, b2)


class TestUrlPath(unittest.TestCase):
    def test_strips_scheme_host_query_fragment(self):
        self.assertEqual(
            me.url_path("https://example.com/a/b/c?x=1&y=2#frag"),
            "/a/b/c",
        )

    def test_no_query_no_fragment(self):
        self.assertEqual(me.url_path("http://example.com/only/path"),
                          "/only/path")

    def test_empty_and_none(self):
        self.assertEqual(me.url_path(""), "")
        self.assertEqual(me.url_path(None), "")

    def test_root_path(self):
        self.assertEqual(me.url_path("https://example.com/"), "/")

    def test_same_path_different_hosts_are_equal_strings(self):
        p1 = me.url_path("https://siteone.example/story/same-item?ref=a")
        p2 = me.url_path("https://sitetwo.example/story/same-item?ref=b")
        self.assertEqual(p1, p2)
        self.assertEqual(p1, "/story/same-item")


class TestRuleC(unittest.TestCase):
    """
    Synthetic pool for Rule C, worked out by hand.

    Group X -- 3 domains, ALL three serve the exact same URL path (a
    single shared-path group of size 3), and all three carry the same
    6-token+ title so Rule A (domain-based) counts them as a 3-domain
    echo. Under Rule C's publisher collapse, these 3 domains merge into
    ONE publisher group (they all share one path), so the collapsed rule
    must NOT count this title as an echo (only 1 distinct publisher, not
    >=3):
      x1.example  /wire/shared-story-id   "storm brings heavy rain and
                                            flooding across the region"
      x2.example  /wire/shared-story-id   (same title)
      x3.example  /wire/shared-story-id   (same title)

    Group Y -- 3 domains that also share one common 6-gram title (so
    Rule A counts them too), but each serves its OWN distinct URL path
    (no path is shared by more than 1 domain), so all three remain
    separate, singleton publisher groups after collapse -- 3 distinct
    publishers survives the >=3 bar, so the collapsed rule must STILL
    count this title as an echo:
      y1.example  /local/y1-report        "council approves new transit
                                            budget for downtown corridor"
      y2.example  /local/y2-report        (same title)
      y3.example  /local/y3-report        (same title)

    Group Z -- a 2-domain shared-path pair, used only to check path-level
    diagnostics (paths_with_ge2_domains / paths_with_ge3_domains), not
    tied to any echo title:
      z1.example  /shared/two-only
      z2.example  /shared/two-only
    """

    @classmethod
    def setUpClass(cls):
        title_x = "Storm brings heavy rain and flooding across the region"
        title_y = "Council approves new transit budget for downtown corridor"
        pool_defs = [
            (title_x, "x1.example", "https://x1.example/wire/shared-story-id"),
            (title_x, "x2.example", "https://x2.example/wire/shared-story-id"),
            (title_x, "x3.example", "https://x3.example/wire/shared-story-id"),

            (title_y, "y1.example", "https://y1.example/local/y1-report"),
            (title_y, "y2.example", "https://y2.example/local/y2-report"),
            (title_y, "y3.example", "https://y3.example/local/y3-report"),

            ("Unrelated filler title about nothing in particular at all",
             "z1.example", "https://z1.example/shared/two-only"),
            ("A second unrelated filler title about something else again",
             "z2.example", "https://z2.example/shared/two-only"),
        ]
        cls.recs = make_recs(pool_defs)
        cls.path_to_domains = me.build_path_domain_groups(cls.recs)

    def test_group1_shares_a_verbatim_6gram_across_3_domains_sanity(self):
        # sanity: group X titles are identical and >=6 tokens
        toks = self.recs[0]["tokens"]
        self.assertGreaterEqual(len(toks), me.SHINGLE_N)
        self.assertEqual(self.recs[0]["norm"], self.recs[1]["norm"])
        self.assertEqual(self.recs[1]["norm"], self.recs[2]["norm"])

    def test_path_stats_counts_shared_paths_correctly(self):
        stats = me.rule_c_path_stats(self.path_to_domains)
        # exactly 2 paths are shared by >=2 domains: the group-X path
        # (3 domains) and the group-Z path (2 domains)
        self.assertEqual(stats["paths_with_ge2_domains"], 2)
        # exactly 1 path is shared by >=3 domains: the group-X path
        self.assertEqual(stats["paths_with_ge3_domains"], 1)
        self.assertEqual(
            stats["domain_group_size_distribution_for_ge2_paths"],
            {2: 1, 3: 1},
        )
        self.assertEqual(stats["path_with_most_domains"]["domain_count"], 3)

    def test_publisher_groups_collapse_group_x_not_group_y(self):
        domain_to_publisher, n_domains, n_publishers, size_counts = (
            me.build_publisher_groups(self.recs, self.path_to_domains)
        )
        self.assertEqual(n_domains, 8)
        # group X (3 domains) -> 1 publisher; group Y (3 domains) -> 3
        # separate publishers (no shared path); group Z (2 domains) -> 1
        # publisher. Total publishers = 1 (X) + 3 (Y) + 1 (Z) = 5.
        self.assertEqual(n_publishers, 5)
        self.assertEqual(
            domain_to_publisher["x1.example"],
            domain_to_publisher["x2.example"],
        )
        self.assertEqual(
            domain_to_publisher["x2.example"],
            domain_to_publisher["x3.example"],
        )
        self.assertNotEqual(
            domain_to_publisher["y1.example"],
            domain_to_publisher["y2.example"],
        )
        self.assertNotEqual(
            domain_to_publisher["y2.example"],
            domain_to_publisher["y3.example"],
        )
        self.assertEqual(
            domain_to_publisher["z1.example"],
            domain_to_publisher["z2.example"],
        )
        # size_counts: one group of size 3 (X), three groups of size 1 (Y),
        # one group of size 2 (Z)
        self.assertEqual(size_counts, {1: 3, 2: 1, 3: 1})

    def test_collapsed_rule_a_drops_group_x_but_keeps_group_y(self):
        domain_to_publisher, _, _, _ = me.build_publisher_groups(
            self.recs, self.path_to_domains
        )
        original = me.rule_a(self.recs)
        collapsed = me.rule_a_with_unit_map(self.recs, domain_to_publisher)

        # Original (domain-based) Rule A counts BOTH group X and group Y
        # as echoes: 3 domains each, 3 titles each = 6 titles total.
        self.assertEqual(original["titles_in_echo"], 6)

        # Collapsed (publisher-based) Rule A must drop group X (now only
        # 1 distinct publisher) but keep group Y (still 3 distinct
        # publishers) -> exactly the 3 group-Y titles remain.
        self.assertEqual(collapsed["titles_in_echo"], 3)
        self.assertLess(collapsed["echo_index"], original["echo_index"])

        # confirm which indices survive: group Y is indices 3,4,5
        covered_before = me.rule_a_covered_titles(self.recs)
        self.assertEqual(covered_before, {0, 1, 2, 3, 4, 5})


if __name__ == "__main__":
    unittest.main(verbosity=2)
