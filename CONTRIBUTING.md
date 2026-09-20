# Contributing to Repository Patterns

Add a useful option, not another universal rule.

## Pattern pages

Use [`docs/templates/pattern.md`](docs/templates/pattern.md). Explain:

- the problem the pattern addresses;
- the conditions in which it helps;
- the smallest useful shape;
- evidence from a named example;
- benefits and trade-offs;
- cases where it is a poor fit;
- questions an adopting team should answer.

Prefer “consider”, “often helps”, and “a useful option” over absolute language. If a stronger constraint is genuinely necessary, explain the safety or correctness reason.

## Case studies

Use [`docs/templates/case-study.md`](docs/templates/case-study.md). Separate:

- `Observed`: directly supported by source, configuration, tests, or documentation;
- `Inferred`: a reasoned interpretation that still deserves verification;
- `Recommended`: a transferable suggestion;
- `Trade-off`: cost, risk, or mismatch.

Pin external examples to a commit where practical. Do not present an example's design documents as proof of runtime behavior without a source or test reference.

## Validation

Run:

```sh
./scripts/check-docs.sh
```
