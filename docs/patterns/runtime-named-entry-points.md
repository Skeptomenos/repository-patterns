---
name: runtime-named-entry-points
description: Server-only imports break browser or edge consumers.
category: structure-and-boundaries
---

# Runtime-named entry points

## Intent

Keep the root entry portable. Put runtime-bound code behind entry points named after the runtime. Then prove the split by bundling for the most constrained target.

## Use when

- a package serves browser, edge, and server consumers;
- one server-only import in a shared entry breaks other consumers downstream;
- adapters bind a specific runtime, such as SQLite on Node or Unix sockets.

## Small shape

```text
pkg                       -> portable contracts and logic
pkg/storage/sqlite        -> portable engine logic over a small facade
pkg/storage/sqlite/node   -> runtime adapter that implements the facade

check: bundle the root for the browser, then assert the adapter is absent
```

## Pi example

**Observed:** `pi-durable` exports `.`, `./storage/memory`, `./storage/sqlite`, and `./storage/sqlite/node` ([`package.json`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/durable/package.json)). A boundary test forbids `node:` imports from the root and from the portable SQLite entry ([`storage-runtime-boundary.test.ts`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/durable/test/storage-runtime-boundary.test.ts)).

**Observed:** [`check-browser-smoke.mjs`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/scripts/check-browser-smoke.mjs) bundles smoke entries for the browser platform. It asserts that the Node adapter is absent (added in [`81274f0e`](https://github.com/earendil-works/pi/commit/81274f0e)). `chord` keeps Node code under `./node` and `./bundler`. The client and server keep Unix transports under `./unix`.

**Observed:** The portable SQLite code depends on a small synchronous facade: `exec`, `prepare`, `transaction`, and `close` ([`database.ts`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/durable/src/storage/sqlite/database.ts)). The durable README names Bun and Cloudflare Durable Objects as valid hosts, and says Cloudflare D1 cannot implement the synchronous facade.

**Observed:** No Pi manifest uses `browser` or `node` export conditions.

**Inferred:** A subpath name makes the runtime choice visible at the import site. Conditional exports would hide it.

**Recommended:** Name adapters after the runtime. Add one bundler check for the most constrained target before you add more.

## Benefits

- Consumers see the runtime cost at the import.
- Portable code stays portable because a check guards it.
- Supporting a new runtime means writing one adapter.

## Trade-offs

- Consumers must choose the correct subpath.
- A bundler check covers only the symbols its smoke entry imports.
- A synchronous facade excludes asynchronous engines.

## Poor fit signals

- The code runs on one runtime, and no other runtime is planned.
- The adapter is so small that a subpath adds more navigation than it removes.

## Adoption questions

- Which runtime is the most constrained consumer?
- What is the smallest facade the portable code needs?
- Which check proves that the runtime adapter is absent from the portable entry?

## Related patterns

- [[contract-and-adapter|Contract and adapter]]
- [[executable-architecture-checks|Executable architecture checks]]
- [[consumer-oriented-verification|Consumer-oriented verification]]
