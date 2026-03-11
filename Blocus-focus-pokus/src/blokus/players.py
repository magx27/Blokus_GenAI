"""Simple computer-player helpers."""

from blokus.engine import list_legal_moves
from blokus.models import GameState, Move
from blokus.pieces import PIECES


def choose_simple_move(state: GameState, player: str | None = None) -> Move | None:
    active_player = player or state.current_player
    legal_moves = list_legal_moves(state, player=active_player)
    if not legal_moves:
        return None
    return min(
        legal_moves,
        key=lambda move: (
            -PIECES[move.piece].size,
            move.y,
            move.x,
            move.piece,
            move.rotation,
            move.flipped,
        ),
    )

