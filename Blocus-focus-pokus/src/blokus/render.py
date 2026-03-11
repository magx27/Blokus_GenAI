"""Text rendering helpers for CLI output."""

from blokus.config import symbol_for_player
from blokus.engine import compute_scores, occupied_square_counts
from blokus.models import GameState


def render_board(state: GameState) -> str:
    header = "   " + " ".join(f"{column:02d}" for column in range(state.board_size))
    lines = [header]
    for row_index, row in enumerate(state.board):
        line = " ".join(symbol_for_player(cell) if cell else "." for cell in row)
        lines.append(f"{row_index:02d} {line}")
    return "\n".join(lines)


def render_state(state: GameState) -> str:
    counts = occupied_square_counts(state)
    scores = compute_scores(state)
    summary_lines = [
        f"Mode: {state.mode}",
        f"Current player: {state.current_player}",
        f"Finished: {state.finished}",
        f"Moves played: {len(state.history)}",
        "Occupied squares: " + ", ".join(f"{player}={counts[player]}" for player in state.players),
        "Scores: " + ", ".join(f"{player}={scores[player]}" for player in state.players),
    ]
    return "\n".join(summary_lines + ["", render_board(state)])

