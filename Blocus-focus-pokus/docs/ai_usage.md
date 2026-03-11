# AI Usage Disclosure

## Scope of AI use

AI assistance was used during:

- repository scaffolding
- initial code drafting
- documentation drafting
- requirements consolidation from the supplied specification text

## Validation policy used here

No AI-generated output was accepted without at least one of the following:

- direct human source review
- unit-test execution
- scenario harness execution
- CLI smoke testing

## Adopted outputs in this repository

| Area | Validation used before adoption |
| --- | --- |
| Engine structure | Human review plus unit tests |
| Piece catalog and transform handling | Human review plus `tests/test_pieces.py` |
| CLI command surface | Human review plus `tests/test_cli.py` |
| Documentation drafts | Human review plus consistency check against repository files |

## Runtime boundary

The delivered game engine, CLI, and tests do not call LLMs or depend on networked AI services at runtime.

