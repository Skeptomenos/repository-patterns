---
name: durable-effect-state
description: Work can be interrupted after an external side effect begins.
category: core-runtime-design
---

# Durable effect state

## Intent

Make interruption and recovery understandable by representing external work as explicit state transitions.

## Use when

- a process may restart during a workflow;
- tools, queues, payments, or remote calls create external effects;
- retries must avoid duplicating work;
- a human may resume work later.

## Small shape

```text
decide -> record intent -> perform effect -> record outcome
                    \\-> recover or reconcile after interruption
```

The names differ by system. The important distinction is between “we intend to do this,” “we did this,” and “we do not know what happened.”

## Pi example

**Observed:** Pi has two durable designs.

- The agent harness (`packages/agent/src/harness`) documents lanes, checkpoints, effect-pending states, retries, deferred work, and recovery. Its [specification](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/agent/docs/harness.md#L141-L160) says work packages WP00–WP07 are complete and lists known gaps by stable id. The shipped CLI does not use the harness yet: it builds the plain `Agent`. The harness runs only on experimental paths behind `PI_EXPERIMENTAL=1`.
- `pi-durable` is a second, separate design (Pico5). It publishes record contracts and storage (memory and SQLite) behind a runtime-neutral root. Its [specification](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/durable/docs/pico-v5.md) is labelled normative. Its [handoff](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/durable/docs/pico-v5-handoff.md#L10-L14) says only packages 1–3, the storage layers, are implemented.

**Observed:** The Pico5 specification calls the shape an "effect sandwich": commit intent, perform the effect, commit the outcome. It adds: "Reopening in an intent phase means the effect may have happened" ([`pico-v5.md` §5.2](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/durable/docs/pico-v5.md#L1234-L1242)). It separates caller cancellation from durable abort. Cancelling a context does not abort shared work unless the API commits an abort mark.

**Observed:** The harness adds three refinements.

- A synchronous admission gate: an effect starts only if no abort came first. The check and the call happen in one expression ([`effect-gate.ts`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/agent/src/harness/execution/effect-gate.ts)).
- A per-tool replay policy, `replay: "safe" | "never"`.
- Hooks classified by durability: transition-consumed, request-local, or pass-local, each with a documented repetition rule.

See the [`agent` documentation](https://github.com/earendil-works/pi/tree/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/agent/docs) and [`pi-durable`](https://github.com/earendil-works/pi/tree/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/durable).

**Recommended:** Use this pattern only where restart and side-effect ambiguity are real requirements. Start with one failure-prone operation rather than redesigning the whole application.

## Benefits

- Recovery behavior becomes inspectable.
- Retries can be designed rather than improvised.
- Operators can distinguish pending, failed, and completed work.

## Trade-offs

- More states mean more tests and more user-facing status.
- Exactly-once behavior is usually impossible without cooperation from the external system.
- State machines can become ceremony if the workflow is short-lived.

## Poor fit signals

- The operation is purely local and finishes inside one transaction.
- Restarting simply means starting over safely.
- The team cannot define what recovery should mean.

## Adoption questions

- What must be true after a restart?
- Which effects are idempotent, deduplicated, or reconciled?
- What evidence distinguishes “not started” from “unknown outcome”?
- How does a caller's cancellation differ from a durable abort of shared work?
- Which operations may be replayed after a crash, and which must never be?

## Related patterns

- [[single-writer-mutation|Single-writer mutation]]
- [[extension-state-in-host-log|Extension state in the host log]]
- [[in-band-terminal-streams|In-band terminal streams]]
- [[visible-maturity|Visible maturity]]
