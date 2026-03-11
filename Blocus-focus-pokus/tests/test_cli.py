import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def test_new_command_writes_valid_json_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "state.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "blokus",
                    "new",
                    "--mode",
                    "classic",
                    "--output",
                    str(output_path),
                ],
                cwd=REPO_ROOT,
                env={"PYTHONPATH": str(REPO_ROOT / "src")},
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            with output_path.open("r", encoding="utf-8") as handle:
                payload = json.load(handle)
            self.assertEqual(payload["mode"], "classic")
            self.assertEqual(payload["current_player"], "blue")

    def test_validate_command_rejects_bad_opening(self) -> None:
        fixture_path = REPO_ROOT / "fixtures" / "states" / "classic_initial.json"
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "blokus",
                "validate",
                "--state",
                str(fixture_path),
                "--piece",
                "I1",
                "--x",
                "1",
                "--y",
                "1",
            ],
            cwd=REPO_ROOT,
            env={"PYTHONPATH": str(REPO_ROOT / "src")},
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 1)
        self.assertIn("must cover start corner", completed.stdout)


if __name__ == "__main__":
    unittest.main()
