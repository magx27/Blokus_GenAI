# Requirements Traceability

This table maps the strongest Phase 1 requirements from the supplied project specification to implementation and verification evidence in the repository.

| Requirement | Repository implementation | Verification |
| --- | --- | --- |
| Configurable engine for supported mode(s) | `src/blokus/config.py`, `src/blokus/engine.py` | `tests/test_serialization.py`, `tests/test_engine.py` |
| Minimal CLI for load, validate, apply, list, and serialize | `src/blokus/cli.py`, `src/blokus/models.py`, `src/blokus/render.py` | `tests/test_cli.py` |
| Load state from JSON | `GameState.from_dict()` in `src/blokus/models.py` | `tests/test_serialization.py`, `fixtures/states/classic_initial.json` |
| Validate proposed moves | `validate_move()` in `src/blokus/engine.py` | `tests/test_engine.py` |
| Apply valid moves | `apply_move()` in `src/blokus/engine.py` | `tests/test_engine.py`, `tests/test_evaluate.py` |
| List legal moves | `list_legal_moves()` in `src/blokus/engine.py` | `tests/test_ai.py`, manual CLI usage in `README.md` |
| Serialize resulting state | `GameState.to_dict()` in `src/blokus/models.py` | `tests/test_serialization.py` |
| Support human players | `play` command in `src/blokus/cli.py` | manual run path in `README.md`, `scripts/run_demo.sh` |
| Support simple computer player | `choose_simple_move()` in `src/blokus/players.py` | `tests/test_ai.py` |
| Classic 4-player baseline | `CLASSIC_CONFIG` in `src/blokus/config.py` | `tests/test_engine.py`, `fixtures/scenarios/classic_corner_sequence.json` |
| Key rules and transforms | `src/blokus/pieces.py`, `src/blokus/engine.py` | `tests/test_pieces.py`, `tests/test_engine.py` |
| Reproducible scripts and evaluation harness | `scripts/`, `src/blokus/evaluate.py` | `scripts/test.sh`, `scripts/evaluate.sh`, `.github/workflows/ci.yml`, `tests/test_evaluate.py` |

## Not yet complete

- Duo mode support is deferred to Phase 2.
- Team-specific ownership names and individual portfolio evidence still need to be filled in.
- The Classic to Duo requirements-evolution case study belongs to Phase 2 reporting.

