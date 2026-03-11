import json
from pathlib import Path
import unittest

from blokus.engine import apply_move, new_game
from blokus.models import GameState, Move


REPO_ROOT = Path(__file__).resolve().parents[1]


class SerializationTests(unittest.TestCase):
    def test_initial_fixture_round_trips(self) -> None:
        fixture_path = REPO_ROOT / "fixtures" / "states" / "classic_initial.json"
        with fixture_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        state = GameState.from_dict(payload)
        self.assertEqual(state.to_dict(), payload)

    def test_state_round_trip_after_moves(self) -> None:
        state = new_game()
        for move in (
            Move("blue", "I1", 0, 0),
            Move("yellow", "I1", 19, 0),
            Move("red", "I1", 19, 19),
            Move("green", "I1", 0, 19),
            Move("blue", "I2", 1, 1),
        ):
            state = apply_move(state, move)
        reloaded = GameState.from_dict(state.to_dict())
        self.assertEqual(reloaded.to_dict(), state.to_dict())


if __name__ == "__main__":
    unittest.main()

