---
name: contract-and-adapter
description: Vendor or infrastructure changes keep spreading through the core.
category: structure-and-boundaries
---

# Contract and adapter

## Intent

Keep a stable semantic contract in the center while allowing providers, databases, vendors, and platforms to vary at the edge.

## Use when

- several implementations should satisfy the same behavior;
- external APIs change faster than your domain model;
- consumers need to replace infrastructure without rewriting core logic;
- the core should remain usable in more than one runtime.

## Small shape

```text
consumer -> stable contract -> adapter -> external system
```

The contract should describe what the application needs, not mirror every detail of an external SDK.

## Pi example

**Observed:** `pi-ai` normalizes providers and model streaming behind common types. `pi-agent-core` consumes the normalized stream instead of importing each provider. The SQLite session backend is a separate package so the core does not pull in Node-specific runtime dependencies. See [`pi-agent-core`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/agent/README.md) and [`pi-ai`](https://github.com/earendil-works/pi/tree/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/ai).

**Observed (v0.87.1):** `pi-agent-core` still depends on the `pi-ai` package for shared types and normalization, but on no provider SDK. The provider boundary has two axes, wire API and vendor; see [Protocol and vendor axes](protocol-and-vendor-axes.md). Only `normalizeContext()` can produce the branded `TranscriptContext` type, so raw input cannot reach an adapter. Cross-cutting policy, such as auth merging and header order, sits in the `Models` collection, not in each adapter.

**Observed (v0.87.1):** `pi-durable` repeats the idea for storage. Portable SQLite logic depends on a small synchronous facade, and the Node adapter sits behind `./storage/sqlite/node`. See [Runtime-named entry points](runtime-named-entry-points.md).

**Recommended:** Define the semantic contract first, then write one adapter as a reference. Keep provider or runtime-specific policy out of the contract unless every consumer truly needs it. Put cross-cutting policy in the layer that owns the collection of adapters.

## Benefits

- Limits dependency spread.
- Makes substitutions and fakes easier.
- Clarifies package ownership.
- Supports different deployment environments.

## Trade-offs

- A bad abstraction can erase important provider differences.
- Adapters add translation code and another place for bugs.
- Too many tiny interfaces can make the system harder to navigate.

## Poor fit signals

- There is only one implementation and no realistic variation.
- The “contract” is just a copy of the vendor API.
- The abstraction cannot express important failure or capability differences.

## Adoption questions

- What behavior must remain stable if the provider changes?
- Which differences should be visible capabilities rather than hidden translation?
- Can the contract be tested without the external system?

## Related patterns

- [Protocol and vendor axes](protocol-and-vendor-axes.md)
- [Capabilities as data](capabilities-as-data.md)
- [Conformance tests](conformance-tests.md)
- [Runtime-named entry points](runtime-named-entry-points.md)
