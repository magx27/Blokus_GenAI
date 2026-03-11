# Team Summary

## Scope

This repository delivers Phase 1 of the assignment: Blokus Classic as the baseline milestone. The implementation focuses on correctness, testability, reproducibility, and documentation instead of UI complexity or advanced AI strength.

Implemented in this phase:

- Classic 4-player game state and turn order.
- Rule enforcement for opening corners, same-color corner contact, and same-color edge exclusion.
- Piece transforms for the 21 Classic polyominoes.
- JSON state serialization and deserialization.
- Minimal CLI commands for state creation, rendering, validation, application, legal-move listing, pass handling, and interactive play.
- A simple deterministic computer player.
- Automated tests and a scenario-based evaluation harness.

Deferred to Phase 2:

- Blokus Duo mode on the same configurable engine.
- Duo-specific board, player, and starting-corner configuration.
- Expanded evaluation coverage across both modes.
- Requirements-evolution write-up covering what broke between Classic and Duo.

## Architecture

The codebase is intentionally split into small plain-Python modules:

- `config.py`: mode configuration and board symbols.
- `pieces.py`: piece definitions and transform generation.
- `models.py`: serializable move and game-state data structures.
- `engine.py`: rule enforcement, state transitions, legal-move generation, pass logic, and scoring.
- `players.py`: simple computer-player policy.
- `render.py`: text rendering for CLI output.
- `cli.py`: command surface for humans and scripts.
- `evaluate.py`: fixture-backed evaluation harness.

This keeps the Phase 1 surface small, but it also leaves a clear insertion point for a Duo `ModeConfig` in Phase 2 without duplicating engine logic.

## AI-assisted engineering disclosure

AI assistance was used during repository setup, code drafting, and documentation drafting. All adopted code paths were validated by direct human review, unit tests, CLI checks, and the evaluation harness before inclusion. The runtime solution itself does not depend on LLMs or network calls.

Detailed disclosure is recorded in `docs/ai_usage.md`.

## Key results

- The repository is stdlib-only at runtime.
- The Phase 1 implementation passes the automated test suite and fixture-backed evaluation harness.
- The CLI exposes the required JSON/state/move operations in a scriptable form.
- The documentation ties requirements to code and tests to reduce reviewer search time.

## Top counterexample candidates for later portfolio work

- Passing when legal moves still exist.
- Opening move that does not cover the assigned corner.
- Same-color side contact that looks visually close to legal corner contact.
- Symmetric transforms that can accidentally be counted twice during move generation.

## Classic to Duo impact

Phase 1 keeps configuration separate from rule execution specifically to prepare for the Classic to Duo change request. The expected low-risk extension points are board size, player order, starting corners, and evaluation fixtures. The highest-risk areas for Phase 2 are likely move-generation assumptions, scenario fixtures, and report-level evidence of what changed and why.

