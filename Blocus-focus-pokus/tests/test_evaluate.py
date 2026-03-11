import unittest

from blokus.evaluate import run_all_scenarios


class EvaluationHarnessTests(unittest.TestCase):
    def test_all_scenarios_pass(self) -> None:
        results = run_all_scenarios()
        self.assertTrue(results)
        self.assertTrue(all(result.passed for result in results), results)


if __name__ == "__main__":
    unittest.main()

