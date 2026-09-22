---
name: change-axis-boundaries
description: One kind of change keeps touching many packages.
category: structure-and-boundaries
---

# Change-axis boundaries

## Intent

Draw package and module boundaries around the reasons code changes. Then one kind of change lands in one place.

## Use when

- one kind of change, such as a vendor, a runtime, or a UI mode, regularly touches many packages;
- a reusable part has grown inside a product package;
- a package serves a product that no longer matches the repository's mission.

## Small shape

```text
list the sources of change -> give each source one owner -> point dependencies from volatile to stable

provider change  -> provider package
runtime change   -> runtime-named adapter
product change   -> host or extension

lifecycle: incubate inside the first consumer -> extract at the second consumer -> evict when off-mission
```

## Pi example

**Observed:** Pi's packages match its sources of change: providers (`pi-ai`), the agent loop (`pi-agent-core`), product and UI (`pi-coding-agent`), the composition substrate (`chord`), transport (`pi-protocol`, `pi-client`, `pi-server`), storage backends (`session-backends/*`), and observability (`pi-telemetry`). See the [root README](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/README.md) and the [layered architecture notes](../examples/pi/pi-architecture.md).

**Observed:** Boundaries move when evidence arrives.

- Telemetry code lived in `pi-ai` and `pi-agent-core` until commit [`6b461b75`](https://github.com/earendil-works/pi/commit/6b461b75) ("feat: extract telemetry package", 2026-08-05) moved it into its own package.
- Off-mission products leave the repository. `browser-extension` was "migrated to separate sitegeist repo" ([`aa005d06`](https://github.com/earendil-works/pi/commit/aa005d06), 2025-10-06). `mom` and `pods` were removed with a pointer to `pi-chat` ([`0ed0d434`](https://github.com/earendil-works/pi/commit/0ed0d434), 2026-04-30). `web-ui` was removed in [`b141e1fa`](https://github.com/earendil-works/pi/commit/b141e1fa) (2026-05-20).
- Storage backends live in a family folder, `packages/session-backends/*`, registered as a workspace glob. The folder was renamed from `packages/storage` in [`a80008b9`](https://github.com/earendil-works/pi/commit/a80008b9). The package name encodes contract, engine, and runtime: `pi-session-backend-sqlite-node`.

**Inferred:** The package list is a map of what changes independently. It is not a list of technical layers.

**Recommended:** Write the sources of change down before you add a package. Extract a module at the second real consumer, not the first. When a product leaves the mission, move it out and leave a pointer.

## Benefits

- A change has one expected home, so reviews stay small.
- Packages can be removed without surgery on their neighbours.
- New contributors can predict where code lives.

## Trade-offs

- Every package adds a manifest, a build step, and release work.
- A wrong guess about a change axis creates churn when it is corrected.
- Evicting a package breaks users who relied on it staying in the repository.

## Poor fit signals

- One team ships one deployable, and it has one source of change.
- The proposed boundary is speculative: no second consumer or variation exists yet.
- The split creates chatty calls across the new boundary.

## Adoption questions

- Which three kinds of change happened most often last quarter, and how many packages did each touch?
- Which module has a second consumer today?
- Which package no longer serves the mission, and where should it go?

## Related patterns

- [Contract and adapter](contract-and-adapter.md)
- [Core and host](core-and-host.md)
- [Application-neutral substrate](application-neutral-substrate.md)
- [Runtime-named entry points](runtime-named-entry-points.md)
