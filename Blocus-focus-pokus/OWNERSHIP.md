# Ownership Table

The assignment requires primary ownership, review accountability, and traceable evidence. Team-member names were not included in the prompt, so the owner fields below are initialized as `TBD`. Replace those placeholders with actual names before submission.

| Work package | Primary owner | Responsibilities | Acceptance evidence |
| --- | --- | --- | --- |
| Requirements and traceability | TBD | Freeze Phase 1 scope, maintain requirement-to-code/test mapping, track phase boundaries | `docs/requirements_traceability.md`, `TEAM_SUMMARY.md` |
| Core engine | TBD | Board rules, turn order, move validation, application, pass logic, scoring | `src/blokus/engine.py`, `tests/test_engine.py` |
| Piece modeling and transforms | TBD | Maintain 21-piece catalog and transform correctness | `src/blokus/pieces.py`, `tests/test_pieces.py` |
| CLI and state I/O | TBD | JSON contract, CLI commands, rendering behavior | `src/blokus/cli.py`, `src/blokus/models.py`, `tests/test_cli.py` |
| Evaluation and test harness | TBD | Fixtures, automated tests, scenario execution, reproducible scripts | `tests/`, `fixtures/`, `src/blokus/evaluate.py`, `scripts/test.sh`, `scripts/evaluate.sh` |
| Documentation and evidence | TBD | Summary docs, AI disclosure, evidence log, reviewing package | `README.md`, `docs/`, `TOPIC-REVIEWING_*.md` |

## Review responsibility

Primary owners are expected to ensure correctness for their package, but no package should merge without review by at least one non-owner. Suggested review checkpoints:

- Requirement review before structural code changes.
- Rule review for each new legality constraint.
- Test review for each new fixture or scenario.
- AI-output review before any generated content is adopted.

## Evidence expectations per owner

- Link commits to the owned package.
- Link authored tests or fixtures to the requirement being supported.
- Record at least one review artifact or review note for each package.
- Record counterexamples and refinements in the individual portfolio.

