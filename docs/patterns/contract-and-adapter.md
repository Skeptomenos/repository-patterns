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

**Observed:** `pi-ai` normalizes providers and model streaming behind common types. `pi-agent-core` consumes the normalized stream instead of importing each provider. The SQLite session backend is a separate package so the core does not pull in Node-specific runtime dependencies. See [`pi-agent-core`](https://github.com/earendil-works/pi/blob/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/packages/agent/README.md) and [`pi-ai`](https://github.com/earendil-works/pi/tree/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/packages/ai).

**Recommended:** Define the semantic contract first, then write one adapter as a reference. Keep provider or runtime-specific policy out of the contract unless every consumer truly needs it.

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
