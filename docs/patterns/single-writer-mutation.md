---
name: single-writer-mutation
description: Concurrent state updates are difficult to reason about.
category: core-runtime-design
---

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

**Observed:** Pi's harness and session designs distinguish planning from committing and protect a serialized mutation line. The design avoids running providers, tools, hooks, or timers while holding the storage mutation capability. See the [`agent harness documentation`](https://github.com/earendil-works/pi/tree/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/agent/docs).

**Observed (v0.87.1):** There are two serializers. The session mutation line orders reads, publication, and recipient binding. Storage keeps its own commit queue for atomicity and sequence numbers.

**Observed (v0.87.1):** Single ownership is a host responsibility, not a storage guarantee. The harness specification says "Session ownership is host-authoritative" and "SQLite has no lease, fence, heartbeat, or replacement ownership primitive" ([`harness.md` L403](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/agent/docs/harness.md#L403)). The `pi-durable` README says one SQLite storage owner must serialize writes to a database file.

**Observed (v0.87.1):** A second instance lives in `pi-ai`. `CredentialStore.modify` is the only write path for credentials, and OAuth refresh runs inside it, so concurrent requests cannot refresh a rotated token twice ([`auth/types.ts`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/ai/src/auth/types.ts#L52-L54)).

**Recommended:** Treat the serialized mutation path as a small, auditable kernel. Keep orchestration and external work outside it. State who guarantees single ownership when two processes can open the same store.

## Benefits

- Easier ordering and replay reasoning.
- Fewer partial-state races.
- Clearer event publication semantics.

## Trade-offs

- A single writer can become a throughput bottleneck.
- Long planning work must be moved outside the commit path.
- The boundary requires careful handling of stale snapshots.
- Single ownership enforced by convention fails silently when a second process opens the same store.

## Poor fit signals

- State is immutable or naturally partitioned.
- Updates do not share ordering or invariants.
- A database already provides the required transaction boundary and no in-process coordination is needed.

## Adoption questions

- Which invariants must hold across every write?
- What is allowed to happen while the state lock is held?
- How are stale plans rejected or retried?
- What stops a second process from writing to the same state?

## Related patterns

- [Durable effect state](durable-effect-state.md)
- [Extension state in the host log](extension-state-in-host-log.md)
- [Multi-agent-safe working tree](multi-agent-safe-worktree.md)
