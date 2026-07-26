import subprocess
import sys
import unittest

import _pathfix  # noqa: F401
import metrics_units as mu


class TestMetricsRunIsDeterministic(unittest.TestCase):
    def test_running_the_script_twice_gives_byte_identical_output(self):
        script = mu.__file__
        for _ in range(2):
            result = subprocess.run(
                [sys.executable, script], capture_output=True, check=True
            )
            self.assertEqual(result.returncode, 0)

        with open(mu.OUT_PATH, "rb") as f:
            first = f.read()

        result = subprocess.run([sys.executable, script], capture_output=True, check=True)
        self.assertEqual(result.returncode, 0)
        with open(mu.OUT_PATH, "rb") as f:
            second = f.read()

        self.assertEqual(first, second)

    def test_in_process_recompute_is_identical(self):
        # Faster, in-process corroboration of the same property, on the same
        # already-loaded inputs.
        from pools import load_pool
        from metrics import load_marker_set

        units = mu.load_units()
        marker_set = load_marker_set(mu.MARKER_CSV_PATH)
        pool = load_pool()

        result1 = mu.compute_all(units, marker_set, pool)
        result2 = mu.compute_all(units, marker_set, pool)
        self.assertEqual(result1, result2)


if __name__ == "__main__":
    unittest.main()
