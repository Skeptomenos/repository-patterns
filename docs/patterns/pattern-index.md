# Patterns

Each pattern page follows the same shape:

1. the problem it addresses;
2. when it is useful;
3. a small conceptual shape;
4. the Pi example, labelled Observed, Inferred, or Recommended;
5. benefits and trade-offs;
6. signals that it may be a poor fit;
7. questions for adoption;
8. related patterns.

The pages are recommendations. They are intentionally not written as mandatory repository rules. Choose a page by need in the [catalog](../catalog.md).

## Available patterns

### Structure and boundaries

- [Change-axis boundaries](change-axis-boundaries.md)
- [Contract and adapter](contract-and-adapter.md)
- [Core and host](core-and-host.md)
- [Application-neutral substrate](application-neutral-substrate.md)
- [Runtime-named entry points](runtime-named-entry-points.md)
- [Executable architecture checks](executable-architecture-checks.md)
- [Opaque transport](opaque-transport.md)
- [Visible maturity](visible-maturity.md)

### Extensibility and plugins

- [Extensions before core](extensions-before-core.md)
- [Customization ladder](customization-ladder.md)
- [Two-phase extension registration](two-phase-extension-registration.md)
- [Fault-isolated event dispatch](fault-isolated-event-dispatch.md)
- [Host-owned UI port](host-owned-ui-port.md)
- [Layered resource discovery](layered-resource-discovery.md)
- [Trust-gated loading](trust-gated-loading.md)
- [Built-ins through public seams](built-ins-through-public-seams.md)
- [Extension state in the host log](extension-state-in-host-log.md)
- [Progressive disclosure of instructions](progressive-disclosure.md)

### Core runtime design

- [Protocol and vendor axes](protocol-and-vendor-axes.md)
- [Capabilities as data](capabilities-as-data.md)
- [Derived artifacts with a guarded source](derived-artifacts.md)
- [In-band terminal streams](in-band-terminal-streams.md)
- [Canonical record, projected per target](canonical-record-projected-per-target.md)
- [Explicit context](explicit-context.md)
- [Durable effect state](durable-effect-state.md)
- [Single-writer mutation](single-writer-mutation.md)

### Verification and release

- [Conformance tests](conformance-tests.md)
- [Hermetic tests, live tests by opt-in](hermetic-tests-live-opt-in.md)
- [Consumer-oriented verification](consumer-oriented-verification.md)
- [Documentation as a tested surface](documentation-as-tested-surface.md)
- [Dependencies as reviewed code](dependencies-as-reviewed-code.md)
- [Staged, reversible release](staged-reversible-release.md)

### Repository operations and governance

- [Repository as operating system](repository-as-operating-system.md)
- [Multi-agent-safe working tree](multi-agent-safe-worktree.md)
- [Attention-budget contribution gate](attention-budget-gate.md)
- [Declared trust boundary](declared-trust-boundary.md)
