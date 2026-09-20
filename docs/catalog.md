# Pattern catalog

Choose by need. The catalog is a routing layer, not a ranking.

| Need | Pattern | Start with | Pi example |
|---|---|---|---|
| Vendor or infrastructure changes keep spreading through the core | [Contract and adapter](patterns/contract-and-adapter.md) | Define the stable semantic contract first | `pi-ai`, `pi-agent-core`, SQLite backend |
| Reusable runtime logic is tangled with CLI or UI behavior | [Core and host](patterns/core-and-host.md) | Move product composition to a host layer | `pi-agent-core` and `pi-coding-agent` |
| Work can be interrupted after an external side effect begins | [Durable effect state](patterns/durable-effect-state.md) | Persist intent and outcome separately | Agent harness runtime and sessions |
| Concurrent state updates are difficult to reason about | [Single-writer mutation](patterns/single-writer-mutation.md) | Plan separately, commit once | Harness session mutation line |
| Multiple implementations drift from a shared interface | [Conformance tests](patterns/conformance-tests.md) | Reuse one contract suite across adapters | Telemetry and session conformance |
| Hidden globals make cancellation, telemetry, or testing fragile | [Explicit context](patterns/explicit-context.md) | Pass capabilities and lifecycle explicitly | Telemetry context and agent options |
| Every feature wants another core flag or special case | [Extensions before core](patterns/extensions-before-core.md) | Test whether a stable extension seam is enough | Pi extensions and minimal-core guidance |
| Transport code is accumulating business semantics | [Opaque transport](patterns/opaque-transport.md) | Keep wire mechanics below domain contracts | `pi-protocol`, `pi-client`, `pi-server` |
| Source tests pass but published artifacts fail for consumers | [Consumer-oriented verification](patterns/consumer-oriented-verification.md) | Test packaging and clean installs | Pi release smoke tests and browser checks |
| Repository process is tribal knowledge | [Repository as operating system](patterns/repository-as-operating-system.md) | Put local operating context near the code | `AGENTS.md`, `.pi/`, scripts, workflows |

If two patterns appear relevant, start with the one that reduces the largest current source of change or failure. Do not adopt both automatically.
