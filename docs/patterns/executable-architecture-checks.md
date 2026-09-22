---
name: executable-architecture-checks
description: Architecture rules live only in diagrams and reviews.
category: structure-and-boundaries
---

# Executable architecture checks

## Intent

Turn architectural rules into fast checks that fail at commit time. Then a rule survives the next contributor and the next agent.

## Use when

- rules exist only in diagrams, reviews, or instructions;
- workspace tooling hides mistakes, for example by hoisting dependencies;
- import cost or runtime portability matters to consumers;
- the same boundary was broken twice.

## Small shape

```text
rule                                         -> check
a package imports only what it declares      -> manifest-truth import audit
a narrow entry point stays narrow            -> entry-point budget (max files, forbidden paths)
a portable entry stays portable              -> bundle for the constrained target, assert absences
a substrate stays neutral                    -> vocabulary and import boundary test
a migration stays done                       -> one-time codemod, then a permanent check
every check                                  -> its own regression test that names the incident
```

## Pi example

**Observed:** [`check-runtime-deps.mjs`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/scripts/check-runtime-deps.mjs) parses each public package with the TypeScript compiler. Every runtime import must be declared in that package's own manifest. Its test names the incident: workspace resolution "masked a missing runtime dependency" ([`check-runtime-deps.test.mjs`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/scripts/check-runtime-deps.test.mjs#L27), #9132).

**Observed:** [`check-entry-graphs.mjs`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/scripts/check-entry-graphs.mjs#L1-L44) opens with "Entry points are cost contracts." It walks the value-import graph of each declared export and enforces a budget. For example, `pi-ai`'s `./utils/*` may load at most three files and must not reach `providers/` or `api/`. The budgets followed commit [`5507d76e`](https://github.com/earendil-works/pi/commit/5507d76e): importing one 6 KB function through the barrel had evaluated 106 files.

**Observed:** `check-ts-relative-imports.mjs` guards the result of a one-time codemod (`update-source-imports-to-ts.sh`). `npm run check` runs lint, format, pinned dependencies, runtime dependencies, import style, entry graphs, generated locks, type check, and the browser smoke. The pre-commit hook runs `npm run check`. `npm test` runs the scripts' own tests first ([root `package.json`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/package.json)).

**Inferred:** Pi does not check a layer diagram. Layering holds because each manifest declares only the dependencies the layer allows. Nothing blocks a contributor from declaring an upward dependency.

**Observed:** Hand-kept lists drift. The root `tsconfig.json` still maps `packages/agent-old`, removed on 2025-11-10. The pre-commit hook still matches `packages/web-ui/*`, removed on 2026-05-20.

**Recommended:** Encode the rule that failed last, not the whole diagram. Derive package lists from manifests instead of copying them into each tool.

## Benefits

- Boundaries survive contributors who never read the architecture document.
- Regressions fail at commit time instead of in a consumer's process.
- Each check documents a rule and the incident behind it.

## Trade-offs

- Checks cost maintenance and slow the commit loop.
- Budgets need re-tuning when growth is legitimate.
- A check that parses code can break when the language or tooling changes.

## Poor fit signals

- The rule has never been broken, and breaking it costs little.
- The check would need a full build or network access to run.
- The repository has no published entry points or consumers.

## Adoption questions

- Which boundary broke most recently, and what would have caught it?
- Which lists are copied by hand into more than one tool?
- Does each check have a test that proves it can fail?

## Related patterns

- [Application-neutral substrate](application-neutral-substrate.md)
- [Runtime-named entry points](runtime-named-entry-points.md)
- [Conformance tests](conformance-tests.md)
- [Repository as operating system](repository-as-operating-system.md)
