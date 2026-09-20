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

See the [`agent conformance tests`](https://github.com/earendil-works/pi/tree/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/packages/agent/src/harness/session/testing/conformance) and [`telemetry README`](https://github.com/earendil-works/pi/blob/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/packages/telemetry/README.md).

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
