# Reviewing Guidelines

## Purpose

This guideline package is tailored to the course topic `Reviewing` and anchored in this Blokus project. It focuses on review tasks that materially affect correctness, evidence quality, and reproducibility.

## Guidelines

1. Review every rule change against both the rule source and at least one executable test.
2. Review every new fixture for reproducibility: the file must be loadable without hidden setup.
3. Review move-generation changes for duplicate-placement risk caused by symmetric transforms.
4. Review CLI changes against the stable command contract in `README.md`.
5. Review AI-assisted outputs before adoption using at least one concrete validator: code execution, test coverage, fixture replay, or line-by-line human comparison.
6. Review documentation claims for direct evidence links so evaluators do not need to search the repository.
7. Review ownership-sensitive files (`OWNERSHIP.md`, portfolios, evidence logs) for attribution completeness.

## Review checklist

- Does the change alter game rules or assumptions?
- Is there at least one positive and one negative test for the changed behavior?
- Are JSON fixtures still valid after the change?
- Does the change preserve determinism in the simple AI and evaluation harness?
- Are documentation updates aligned with the actual behavior in code and tests?

