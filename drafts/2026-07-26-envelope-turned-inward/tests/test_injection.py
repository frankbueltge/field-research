import unittest

import _pathfix  # noqa: F401
import sensitivity_units as su
import envelope_units as eu
from pools import load_pool


class TestInjectionDeterminism(unittest.TestCase):
    """PREREGISTRATION.md §9.2: same seed -> identical output. The seed string is
    `20260726:inject:{unit}:{p}:{recipe}`, so repeated calls with identical
    (unit, p, recipe, donor_list) must be byte-for-byte identical."""

    def test_inject_prefix_is_deterministic(self):
        pool = load_pool()
        donors = su.donor_list_for_recipe(pool, "A")
        prefix = [f"tok{i:04d}" for i in range(600)]
        injected1, positions1 = su.inject_prefix(prefix, unit_index=65, p=0.2, recipe="A", donor_list=donors)
        injected2, positions2 = su.inject_prefix(prefix, unit_index=65, p=0.2, recipe="A", donor_list=donors)
        self.assertEqual(injected1, injected2)
        self.assertEqual(positions1, positions2)

    def test_different_unit_gives_different_positions_in_general(self):
        pool = load_pool()
        donors = su.donor_list_for_recipe(pool, "A")
        prefix = [f"tok{i:04d}" for i in range(600)]
        _inj1, positions_unit65 = su.inject_prefix(prefix, unit_index=65, p=0.2, recipe="A", donor_list=donors)
        _inj2, positions_unit66 = su.inject_prefix(prefix, unit_index=66, p=0.2, recipe="A", donor_list=donors)
        self.assertNotEqual(positions_unit65, positions_unit66)

    def test_donor_list_construction_is_deterministic(self):
        pool = load_pool()
        d1 = su.donor_list_for_recipe(pool, "B")
        d2 = su.donor_list_for_recipe(pool, "B")
        self.assertEqual(d1, d2)
        self.assertEqual(len(d1), 100)  # ranks 51-150

    def test_recipe_a_donor_count(self):
        pool = load_pool()
        donors = su.donor_list_for_recipe(pool, "A")
        self.assertEqual(len(donors), 50)

    def test_replaced_position_count_matches_p_exactly(self):
        pool = load_pool()
        donors = su.donor_list_for_recipe(pool, "A")
        prefix = [f"tok{i:04d}" for i in range(600)]
        for p in su.P_GRID:
            _injected, positions = su.inject_prefix(prefix, unit_index=61, p=p, recipe="A", donor_list=donors)
            self.assertEqual(len(positions), round(p * 600))


class TestFullPipelineDeterminism(unittest.TestCase):
    def test_build_injected_docs_is_deterministic(self):
        import json
        with open(su.METRICS_PATH, "r", encoding="utf-8") as f:
            metrics = json.load(f)
        units_metrics = metrics["units"]
        units_jsonl = su.load_units_jsonl()
        pool = load_pool()
        donors = su.donor_list_for_recipe(pool, "B")
        docs1 = su.build_injected_docs(units_metrics, units_jsonl, 0.1, "B", donors)
        docs2 = su.build_injected_docs(units_metrics, units_jsonl, 0.1, "B", donors)
        self.assertEqual(docs1, docs2)


class TestEnvelopeFitUnaffectedByInjection(unittest.TestCase):
    """PREREGISTRATION.md §9.2: 'the envelope fit itself stays fitted on the REAL
    envelope-era data -- only the decision units are injected.' The fit only ever
    reads units 1-47's real prefix600 series; injection only ever touches units
    61-73's token lists, which the fit computation never looks at."""

    def test_real_decisional_state_fit_identical_regardless_of_injection_activity(self):
        import json
        with open(su.METRICS_PATH, "r", encoding="utf-8") as f:
            metrics = json.load(f)
        units_metrics = metrics["units"]
        units_jsonl = su.load_units_jsonl()
        pool = load_pool()

        state_before = su.real_decisional_state(units_metrics)

        # Run a full injected pass (smallest grid p, both recipes) -- this must not
        # mutate units_metrics/units_jsonl or otherwise perturb the envelope fit.
        for recipe in su.RECIPES:
            donors = su.donor_list_for_recipe(pool, recipe)
            su.build_injected_docs(units_metrics, units_jsonl, su.P_GRID[0], recipe, donors)

        state_after = su.real_decisional_state(units_metrics)

        for name in eu.MARGIN_METRIC_DIRECTIONS:
            fit_before = state_before[name]["fit"]
            fit_after = state_after[name]["fit"]
            self.assertEqual(fit_before["n"], fit_after["n"])
            self.assertEqual(fit_before["df"], fit_after["df"])
            self.assertAlmostEqual(fit_before["t_crit"], fit_after["t_crit"], places=12)
            self.assertAlmostEqual(fit_before["s"], fit_after["s"], places=12)
            key_a = "a" if "a" in fit_before else "coeffs"
            self.assertEqual(fit_before[key_a], fit_after[key_a])
            self.assertEqual(state_before[name]["delta_ref"], state_after[name]["delta_ref"])
            self.assertEqual(state_before[name]["a_ref"], state_after[name]["a_ref"])

    def test_envelope_window_tokens_never_read_by_injection_code(self):
        # build_injected_docs only ever indexes units 61-73 in the returned mapping.
        import json
        with open(su.METRICS_PATH, "r", encoding="utf-8") as f:
            metrics = json.load(f)
        units_metrics = metrics["units"]
        units_jsonl = su.load_units_jsonl()
        pool = load_pool()
        donors = su.donor_list_for_recipe(pool, "A")
        docs = su.build_injected_docs(units_metrics, units_jsonl, su.P_GRID[0], "A", donors)
        self.assertEqual(set(docs.keys()), set(range(61, 74)))


if __name__ == "__main__":
    unittest.main()
