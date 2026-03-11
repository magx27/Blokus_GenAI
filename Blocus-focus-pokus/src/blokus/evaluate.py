"""Fixture-backed evaluation harness."""

from dataclasses import dataclass
import json
from pathlib import Path

from blokus.engine import apply_move, new_game, occupied_square_counts
from blokus.models import Move


SCENARIO_DIR = Path(__file__).resolve().parents[2] / "fixtures" / "scenarios"


@dataclass(frozen=True)
class ScenarioResult:
    name: str
    passed: bool
    detail: str


def _load_scenario(path: Path) -> dict[str, object]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def run_scenario(path: Path) -> ScenarioResult:
    scenario = _load_scenario(path)
    state = new_game(mode=str(scenario.get("mode", "classic")))
    name = str(scenario.get("name", path.stem))

    try:
        for raw_move in scenario.get("moves", []):
            state = apply_move(state, Move.from_dict(raw_move))
    except Exception as exc:  # pragma: no cover - surfaced in tests and CLI output
        return ScenarioResult(name=name, passed=False, detail=f"Scenario failed during move execution: {exc}")

    expected = scenario.get("expect", {})
    expected_current_player = expected.get("current_player")
    if expected_current_player and state.current_player != expected_current_player:
        return ScenarioResult(
            name=name,
            passed=False,
            detail=(
                f"Expected current player {expected_current_player}, "
                f"got {state.current_player}."
            ),
        )

    expected_finished = expected.get("finished")
    if expected_finished is not None and state.finished != bool(expected_finished):
        return ScenarioResult(
            name=name,
            passed=False,
            detail=f"Expected finished={expected_finished}, got {state.finished}.",
        )

    expected_history_length = expected.get("history_length")
    if expected_history_length is not None and len(state.history) != int(expected_history_length):
        return ScenarioResult(
            name=name,
            passed=False,
            detail=f"Expected history length {expected_history_length}, got {len(state.history)}.",
        )

    expected_counts = expected.get("occupied_counts")
    if isinstance(expected_counts, dict):
        actual_counts = occupied_square_counts(state)
        for player, expected_count in expected_counts.items():
            if actual_counts[str(player)] != int(expected_count):
                return ScenarioResult(
                    name=name,
                    passed=False,
                    detail=(
                        f"Expected {player} to occupy {expected_count} squares, "
                        f"got {actual_counts[str(player)]}."
                    ),
                )

    return ScenarioResult(name=name, passed=True, detail="Passed.")


def run_all_scenarios(directory: Path = SCENARIO_DIR) -> list[ScenarioResult]:
    return [run_scenario(path) for path in sorted(directory.glob("*.json"))]


def main() -> int:
    results = run_all_scenarios()
    passed = sum(1 for result in results if result.passed)
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"{status}: {result.name} - {result.detail}")
    print(f"\nSummary: {passed}/{len(results)} scenarios passed.")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())

