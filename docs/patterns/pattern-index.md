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

The pages are recommendations. They are intentionally not written as mandatory repository rules. Choose a page by need in the [[catalog]].

## Available patterns

### Structure and boundaries

- [[change-axis-boundaries|Change-axis boundaries]]
- [[contract-and-adapter|Contract and adapter]]
- [[core-and-host|Core and host]]
- [[application-neutral-substrate|Application-neutral substrate]]
- [[runtime-named-entry-points|Runtime-named entry points]]
- [[executable-architecture-checks|Executable architecture checks]]
- [[opaque-transport|Opaque transport]]
- [[visible-maturity|Visible maturity]]

### Extensibility and plugins

- [[extensions-before-core|Extensions before core]]
- [[customization-ladder|Customization ladder]]
- [[two-phase-extension-registration|Two-phase extension registration]]
- [[fault-isolated-event-dispatch|Fault-isolated event dispatch]]
- [[host-owned-ui-port|Host-owned UI port]]
- [[layered-resource-discovery|Layered resource discovery]]
- [[trust-gated-loading|Trust-gated loading]]
- [[built-ins-through-public-seams|Built-ins through public seams]]
- [[extension-state-in-host-log|Extension state in the host log]]
- [[progressive-disclosure|Progressive disclosure of instructions]]

### Core runtime design

- [[protocol-and-vendor-axes|Protocol and vendor axes]]
- [[capabilities-as-data|Capabilities as data]]
- [[derived-artifacts|Derived artifacts with a guarded source]]
- [[in-band-terminal-streams|In-band terminal streams]]
- [[canonical-record-projected-per-target|Canonical record, projected per target]]
- [[explicit-context|Explicit context]]
- [[durable-effect-state|Durable effect state]]
- [[single-writer-mutation|Single-writer mutation]]

### Verification and release

- [[conformance-tests|Conformance tests]]
- [[hermetic-tests-live-opt-in|Hermetic tests, live tests by opt-in]]
- [[consumer-oriented-verification|Consumer-oriented verification]]
- [[documentation-as-tested-surface|Documentation as a tested surface]]
- [[dependencies-as-reviewed-code|Dependencies as reviewed code]]
- [[staged-reversible-release|Staged, reversible release]]

### Repository operations and governance

- [[repository-as-operating-system|Repository as operating system]]
- [[multi-agent-safe-worktree|Multi-agent-safe working tree]]
- [[attention-budget-gate|Attention-budget contribution gate]]
- [[declared-trust-boundary|Declared trust boundary]]
