# Evidence Log

This log is a lightweight starting point for the course requirement that evidence be reproducible and attributable.

## Phase 1 baseline evidence

| Claim | Evidence |
| --- | --- |
| Repository is reproducible with plain Python tooling | `scripts/install.sh`, `scripts/test.sh`, `scripts/evaluate.sh`, `pyproject.toml` |
| Core Classic rules are enforced | `src/blokus/engine.py`, `tests/test_engine.py` |
| Piece transforms are implemented | `src/blokus/pieces.py`, `tests/test_pieces.py` |
| State JSON round-trip works | `src/blokus/models.py`, `tests/test_serialization.py`, `fixtures/states/classic_initial.json` |
| Evaluation harness exists and runs repeatable scenarios | `src/blokus/evaluate.py`, `fixtures/scenarios/classic_corner_sequence.json`, `tests/test_evaluate.py` |
| Simple computer player exists | `src/blokus/players.py`, `tests/test_ai.py` |
| CLI supports the required baseline actions | `src/blokus/cli.py`, `tests/test_cli.py`, `README.md` |

## Team follow-up needed

- Add commit references once work is split across team members.
- Add review records per work package.
- Add portfolio-specific evidence links.
- Add Classic-to-Duo evolution evidence during Phase 2.

