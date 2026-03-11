# Blocus Focus Pokus

Plain-Python Phase 1 delivery for the course Blokus project. This repository implements the Classic baseline only: a configurable engine shape, 4-player Classic rules, a minimal CLI, JSON state I/O, a simple computer player, automated tests, fixtures, and a fixture-backed evaluation harness.

## Phase 1 scope

- Implement Blokus Classic as the milestone baseline.
- Support 4 players on a 20x20 board with standard starting corners.
- Load and save game states as JSON.
- Validate moves, apply legal moves, list legal moves, and render board state.
- Include at least one simple computer player strategy.
- Cover key rules, transforms, serialization, and scenario execution with automated tests.

Phase 2 support for Blokus Duo is intentionally not implemented yet. The code is structured around a mode configuration layer so Duo can be added in the same engine rather than by creating a second code path.

## Repository layout

- `src/blokus/`: engine, CLI, rendering, evaluation harness, and simple AI.
- `tests/`: `unittest` suite for rules, transforms, serialization, CLI behavior, and evaluation scenarios.
- `fixtures/`: repeatable JSON states and scenario inputs.
- `scripts/`: reproducible install, test, evaluation, and demo-entry scripts.
- `docs/`: architecture, traceability, evidence, AI usage, and rule-source notes.
- `.github/workflows/ci.yml`: CI pipeline for install, tests, and harness execution.

## Quick start

```bash
./scripts/install.sh
./scripts/test.sh
./scripts/evaluate.sh
```

Without a virtual environment, the commands also work with `PYTHONPATH=src`.

## CLI contract

Create a new state:

```bash
python -m blokus new --mode classic --output /tmp/classic.json
```

Render a state:

```bash
python -m blokus show --state /tmp/classic.json
```

Validate a move:

```bash
python -m blokus validate --state /tmp/classic.json --piece I1 --x 0 --y 0
```

Apply a move and write the updated state:

```bash
python -m blokus apply --state /tmp/classic.json --piece I1 --x 0 --y 0 --output /tmp/classic.json
```

List legal moves:

```bash
python -m blokus legal-moves --state /tmp/classic.json --limit 10
```

Ask the simple computer player for a move:

```bash
python -m blokus suggest --state /tmp/classic.json
```

Run the evaluation harness:

```bash
python -m blokus evaluate
```

Play interactively or run mixed human/computer turns:

```bash
python -m blokus play --mode classic --players human,computer,computer,computer
```

## Rule assumptions used in Phase 1

- Authoritative gameplay reference for Classic: official Mattel Blokus instructions and the course specification excerpts supplied in the task.
- Opening move: each player must cover their assigned board corner.
- Subsequent moves: a new piece must touch at least one same-color piece at a corner and may not share a same-color edge.
- End of game: the game finishes when all players are blocked.
- Scoring: negative count of unplayed squares, plus the official perfect-game bonuses (`+15`, plus `+5` if `I1` is the final piece played).

See `docs/rule-sources.md` for cited sources and implementation notes.

## Deliverables created in this setup

- `TEAM_SUMMARY.md`
- `OWNERSHIP.md`
- `docs/requirements_traceability.md`
- `docs/architecture.md`
- `docs/ai_usage.md`
- `docs/evidence_log.md`
- `TOPIC-REVIEWING_guidelines.md`
- `TOPIC-REVIEWING_example-problems.md`
- `TOPIC-REVIEWING_evaluation.md`
- `Portfolio_TEMPLATE.md`

The team-specific attribution fields are intentionally marked `TBD` where member names were not available in the prompt.

