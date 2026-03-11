# Architecture Notes

## Design goals

Phase 1 is optimized for correctness, inspection, and easy extension. The implementation avoids external runtime dependencies and keeps state explicit and serializable.

## Core flow

1. `new_game()` builds a mode-specific empty state.
2. `validate_move()` enforces turn order, remaining-piece ownership, bounds, overlap, opening-corner rules, and same-color touch rules.
3. `apply_move()` mutates a cloned state, updates turn order, consumes the piece, and recomputes finish status.
4. `list_legal_moves()` enumerates placements from candidate anchor cells rather than scanning every board coordinate blindly.
5. `choose_simple_move()` picks a deterministic legal move, preferring larger pieces first.

## Why anchor-based move generation

A brute-force scan of every board coordinate for every transform is simple but wasteful. The anchor strategy narrows candidate placements to:

- the assigned start corner for a player’s first move
- empty cells that are diagonally adjacent to the player’s existing pieces and not already invalidated by same-color edge contact

That keeps the implementation simple enough for plain Python while still supporting legal-move listing and a deterministic computer player.

## Serialization approach

Game states are serialized as readable JSON:

- board rows are strings of `.`, `B`, `Y`, `R`, and `G`
- remaining pieces are listed per player
- history is retained for auditability
- controller types are recorded so an interactive session can be resumed

This format is easy to diff, review, and use in fixtures.

## Planned Duo extension point

Phase 2 should add a new `ModeConfig` plus Duo fixtures and tests. The following modules were intentionally shaped to avoid a mode split:

- `config.py`
- `models.py`
- `engine.py`
- `evaluate.py`

