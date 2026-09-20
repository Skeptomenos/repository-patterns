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

**Observed:** Pi's agent harness documents lanes, checkpoints, effect-pending states, retries, deferred work, and recovery paths. Session and runtime designs live beside the implementation. The separate `pi-durable` package exposes a smaller public surface while the broader durable design remains experimental.

See the [`agent` documentation](https://github.com/earendil-works/pi/tree/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/packages/agent/docs) and [`pi-durable`](https://github.com/earendil-works/pi/tree/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/packages/durable).

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
