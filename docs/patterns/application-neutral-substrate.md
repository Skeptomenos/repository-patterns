---
name: application-neutral-substrate
description: Generic machinery keeps absorbing product concepts.
category: structure-and-boundaries
---

# Application-neutral substrate

## Intent

Keep generic machinery reusable. Give it its own package, its own vocabulary, and a test that rejects product concepts.

## Use when

- several packages or products need the same runtime machinery, such as composition, RPC, replicated state, or context;
- generic code keeps absorbing product words;
- the machinery should be replaceable or publishable on its own.

## Small shape

```text
substrate package
  - zero product dependencies
  - a written list of forbidden product terms
  - a boundary test that fails on product imports
products -> depend on the substrate (never the reverse)
```

## Pi example

**Observed:** `chord` is a standalone application-composition runtime. Its README says it does not depend on any other Pi workspace package. Its [PLANNING.md](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/chord/PLANNING.md#L30-L37) requires application-neutral vocabulary in source, errors, tests, and examples. It lists terms that must not become Chord concepts: Session, Harness, AgentLane, server, client, attachment, TUI, model, tool, hook, provider credential, and workspace.

**Observed:** [`test/boundary.test.ts`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/chord/test/boundary.test.ts) fails on any `@earendil-works/pi-*` dependency or import, and on relative imports that leave `src`. The package name drops the `pi-` prefix that every other package carries. Six packages depend on it: protocol, client, server, agent, durable, and coding-agent.

**Observed:** The plan migrates rewrite-first. Consumers move to the substrate, then the duplicates are deleted.

**Inferred:** The unprefixed name is a social signal. The boundary test is the enforcement.

**Recommended:** Start with the forbidden-term list and one boundary test. Both cost little and stop drift early.

## Benefits

- The machinery stays reusable by products that do not exist yet.
- Products change without edits to the substrate.
- The substrate can be replaced or published separately.

## Trade-offs

- Two vocabularies need adapter code between them.
- A substrate can grow ahead of real need.
- Substrate packages can get less process attention. Pi's `chord` has no `CHANGELOG.md`, although Pi's `AGENTS.md` asks for one per package.

## Poor fit signals

- Only one application uses the machinery.
- The generic API is not yet known. Extract it later.
- The "substrate" is a thin wrapper around one product's needs.

## Adoption questions

- Which words must never appear in the substrate?
- Which test fails when they do?
- Which consumer moves first, and when are the duplicates deleted?

## Related patterns

- [Change-axis boundaries](change-axis-boundaries.md)
- [Executable architecture checks](executable-architecture-checks.md)
- [Explicit context](explicit-context.md)
