---
name: conformance-tests
description: Multiple implementations drift from a shared interface.
category: verification-and-release
---

# Conformance tests

## Intent

Define a reusable behavioral contract once and run it against every implementation that claims to satisfy it.

## Use when

- multiple storage or transport adapters should behave alike;
- the interface is more important than the implementation;
- regressions often appear only in one backend.

## Small shape

```text
contract suite(storageFactory)
contract suite(telemetryAdapter)
contract suite(remoteClient)
```

The suite should test observable behavior, failure, rollback, reopening, and lifecycle—not only method signatures.

## Pi example

**Observed:** Pi has reusable conformance cases for session storage and repositories, and telemetry has a reference adapter plus conformance checks. The SQLite backend invokes the session contract suite rather than inventing a second definition of correctness.

**Observed (v0.87.1):** Pi uses two styles.

- `pi-agent-core` publishes its session suite as runner-agnostic cases at the `./harness/session/testing` export, together with fault-injecting storage decorators. Memory, JSONL, and the SQLite backend in `session-backends/sqlite-node` run it, so an external backend can run it too.
- `pi-durable` keeps its storage suite private to its tests, because both of its backends live in one package. Its SQLite run wraps storage in a decorator that closes and reopens the database after every commit ([`sqlite-storage.test.ts`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/durable/test/sqlite-storage.test.ts#L34)). The whole behavioural suite then also proves persistence. The memory backend is the reference semantics and copies values to simulate a serialization boundary, so aliasing bugs appear in the reference too.

**Observed (v0.87.1):** Chord writes its conformance matrix in the plan before the code, and requires race tests to control exact points instead of relying on timing. `pi-ai` providers have no shared conformance suite. They follow a per-provider checklist of test files, gated by API keys.

**Recommended:** Ship the suite with the contract when third parties write adapters. Reuse the suite with a reopening or fault-injecting decorator to test durability without writing new cases.

See the [`agent conformance tests`](https://github.com/earendil-works/pi/tree/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/agent/src/harness/session/testing/conformance) and [`telemetry README`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/telemetry/README.md).

## Benefits

- Prevents backend-specific interpretations from drifting.
- Makes adding an adapter cheaper.
- Documents the real contract through executable behavior.

## Trade-offs

- Contract suites can be slow or difficult to isolate.
- Some implementations legitimately need capability-specific behavior.
- Tests still need explicit coverage for performance and scale.

## Poor fit signals

- Implementations intentionally have different semantics.
- The interface is unstable and still changing daily.
- The suite only checks trivial happy paths.

## Adoption questions

- Which behaviors are contractually observable?
- Which errors, lifecycle transitions, and rollback cases matter?
- Which differences should be separate capabilities instead of exceptions?
- Should the suite ship with the contract, so external adapters can run it?

## Related patterns

- [Contract and adapter](contract-and-adapter.md)
- [Executable architecture checks](executable-architecture-checks.md)
- [Hermetic tests, live tests by opt-in](hermetic-tests-live-opt-in.md)
