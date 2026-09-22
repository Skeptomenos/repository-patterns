# Contributing to Repository Patterns

Add a useful option, not another universal rule.

## Pattern pages

Start from [`docs/templates/pattern-template.md`](docs/templates/pattern-template.md). Explain:

- the problem the pattern addresses;
- the conditions in which it helps;
- the smallest useful shape;
- evidence from a named example;
- benefits and trade-offs;
- cases where it is a poor fit;
- questions an adopting team should answer;
- related patterns, as relative links.

Start each page with frontmatter. `name` equals the file name. `description` is the need the pattern answers, in one sentence. `category` is one of the five catalog groups. Add the pattern to [`docs/catalog.md`](docs/catalog.md) under its category and to [`docs/patterns/pattern-index.md`](docs/patterns/pattern-index.md) in the same change.

Prefer “consider”, “often helps”, and “a useful option” over absolute language. If a stronger constraint is genuinely necessary, explain the safety or correctness reason.

## Case studies

Start from [`docs/templates/case-study-template.md`](docs/templates/case-study-template.md). Name case-study files after the example, for example `pi-case-study.md`, so that file names stay unique as the library grows. Separate:

- `Observed`: directly supported by source, configuration, tests, or documentation;
- `Inferred`: a reasoned interpretation that still deserves verification;
- `Recommended`: a transferable suggestion;
- `Trade-off`: cost, risk, or mismatch.

Pin each external example to one commit, and record the pin in [`index.md`](index.md). Do not present an example's design documents as proof of runtime behavior without a source or test reference. When you re-pin, keep a note of the superseded pin and list the claims that changed.

## Links

- Reference documents in this repository with relative Markdown links, for example `[Core and host](core-and-host.md)` or `[corrections](../examples/pi/pi-case-study.md#corrections-since-the-first-analysis)`. GitHub renders them, and the check resolves every path and heading anchor.
- Link a pattern with its title. Link other documents with their path in backticks, for example ``[`docs/catalog.md`](docs/catalog.md)``.
- Do not use wiki links (`[[name]]`). GitHub does not render them in repository files.
- Keep every Markdown file name unique, so that a search by name finds exactly one file.
- Link each new document from an existing page. Every page must be reachable from `AGENTS.md`.

See [`docs/decisions/0004-github-links.md`](docs/decisions/0004-github-links.md) for the reasons and the trade-offs.

## Validation

Run:

```sh
./scripts/check-docs.sh
```

When you change the checks, also run:

```sh
python3 scripts/test_check_docs.py
```

CI runs both on every push and pull request. The checks use only the Python standard library and need no network.
