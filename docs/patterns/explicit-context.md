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

See [`pi-telemetry`](https://github.com/earendil-works/pi/blob/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/packages/telemetry/README.md) and [`pi-agent-core`](https://github.com/earendil-works/pi/blob/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/packages/agent/README.md).

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
