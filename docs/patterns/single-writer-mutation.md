# Single-writer mutation

## Intent

Reduce concurrency ambiguity by giving one serialized mutation path responsibility for changing durable state.

## Use when

- many asynchronous actors can update the same state;
- ordering and event publication matter;
- storage callbacks and external effects are easy to interleave accidentally.

## Small shape

```text
read snapshot -> plan next state -> commit once -> publish event
```

External I/O should usually happen outside the mutation line, with its result brought back as an explicit input or effect outcome.

## Pi example

**Observed:** Pi's harness and session designs distinguish planning from committing and protect a serialized mutation line. The design avoids running providers, tools, hooks, or timers while holding the storage mutation capability. See the [`agent harness documentation`](https://github.com/earendil-works/pi/tree/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/packages/agent/docs).

**Recommended:** Treat the serialized mutation path as a small, auditable kernel. Keep orchestration and external work outside it.

## Benefits

- Easier ordering and replay reasoning.
- Fewer partial-state races.
- Clearer event publication semantics.

## Trade-offs

- A single writer can become a throughput bottleneck.
- Long planning work must be moved outside the commit path.
- The boundary requires careful handling of stale snapshots.

## Poor fit signals

- State is immutable or naturally partitioned.
- Updates do not share ordering or invariants.
- A database already provides the required transaction boundary and no in-process coordination is needed.

## Adoption questions

- Which invariants must hold across every write?
- What is allowed to happen while the state lock is held?
- How are stale plans rejected or retried?
