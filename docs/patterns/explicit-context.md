---
name: explicit-context
description: Hidden globals make cancellation, telemetry, or testing fragile.
category: core-runtime-design
---

# Explicit context

## Intent

Pass lifecycle, cancellation, telemetry, capability, and configuration context explicitly instead of relying on hidden global state.

## Use when

- operations need cancellation or deadlines;
- tests need isolated dependencies;
- nested work should inherit telemetry or permissions;
- multiple sessions can run in one process.

## Small shape

```text
operation(input, context)
context = { abort, telemetry, capabilities, configuration }
```

The context should remain small and typed. It should not become a bag containing every service in the application.

## Pi example

**Observed:** Pi's telemetry package uses explicit contexts and callbacks rather than a global current span. The agent and tool APIs expose abort and lifecycle hooks through options and events.

**Observed (v0.87.1):** The harness takes a Chord `Context` as the trailing parameter of its asynchronous public methods. The context carries the abort signal and keyed values, and the telemetry parent sits under a key ([`harness/context.ts`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/agent/src/harness/context.ts)). The harness specification keeps invocation cancellation separate from durable cancellation, and says a context is never durable data. Chord marks call sites where context is not threaded yet with a named placeholder, `TODO_CONTEXT` ([`chord/src/context/index.ts` L56](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/chord/src/context/index.ts#L56)).

**Observed (counter-evidence):** Adoption is partial. The plain `Agent` takes `AbortSignal` options instead of a context, and `pi-agent-core` keeps a process-global default stream function.

**Recommended:** Mark missing context propagation with a named placeholder, so the gaps can be found by search.

See [`pi-telemetry`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/telemetry/README.md) and [`pi-agent-core`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/agent/README.md).

## Benefits

- Dependencies are visible at the call boundary.
- Tests can supply fakes and isolated lifecycles.
- Nested operations can preserve cancellation and observability.

## Trade-offs

- Context objects can become unwieldy.
- Passing context through many layers adds ceremony.
- A context may conceal too much if its fields are not carefully scoped.

## Poor fit signals

- The value is immutable configuration with a clear owner.
- Passing the context would add more indirection than it removes.
- The proposed context has no coherent lifecycle or capability boundary.

## Adoption questions

- Which values must follow an operation across async boundaries?
- Which dependencies should remain explicit parameters instead?
- Can the context be divided into smaller contexts by concern?

## Related patterns

- [Application-neutral substrate](application-neutral-substrate.md)
- [Two-phase extension registration](two-phase-extension-registration.md)
- [Durable effect state](durable-effect-state.md)
