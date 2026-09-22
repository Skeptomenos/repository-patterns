# Pattern catalog

Choose by need. The catalog is a routing layer, not a ranking. The groups follow the questions a design review asks: where boundaries go, how the system grows, how the core behaves, how it is verified, and how the repository is operated.

## Structure and boundaries

| Need | Pattern | Start with | Pi example |
|---|---|---|---|
| One kind of change keeps touching many packages | [Change-axis boundaries](patterns/change-axis-boundaries.md) | List the sources of change, then give each one owner | Package per change source; telemetry extracted, `mom` and `web-ui` evicted |
| Vendor or infrastructure changes keep spreading through the core | [Contract and adapter](patterns/contract-and-adapter.md) | Define the stable semantic contract first | `pi-ai`, `pi-agent-core`, SQLite backend |
| Reusable runtime logic is tangled with CLI or UI behavior | [Core and host](patterns/core-and-host.md) | Move product composition to a host layer | `pi-agent-core` and `pi-coding-agent`; `AgentSession` and its modes |
| Generic machinery keeps absorbing product concepts | [Application-neutral substrate](patterns/application-neutral-substrate.md) | Write a forbidden-term list and one boundary test | `chord` |
| Server-only imports break browser or edge consumers | [Runtime-named entry points](patterns/runtime-named-entry-points.md) | Name adapters after the runtime; bundle to prove it | `pi-durable` storage subpaths, browser smoke |
| Architecture rules live only in diagrams and reviews | [Executable architecture checks](patterns/executable-architecture-checks.md) | Encode the rule that broke last | Runtime-deps audit, entry-point budgets |
| Transport code is accumulating business semantics | [Opaque transport](patterns/opaque-transport.md) | Keep wire mechanics below domain contracts | `pi-protocol`, `pi-client`, `pi-server` |
| Readers cannot tell shipped behavior from plans | [Visible maturity](patterns/visible-maturity.md) | Put a status line at the top of every plan | Source-only experimental exports; gap ledgers |

## Extensibility and plugins

| Need | Pattern | Start with | Pi example |
|---|---|---|---|
| Every feature wants another core flag or special case | [Extensions before core](patterns/extensions-before-core.md) | Test whether a stable extension seam is enough | Pi extensions and minimal-core guidance |
| Users reach for code where instructions would do | [Customization ladder](patterns/customization-ladder.md) | Publish the mechanisms in order of power | Quickstart "least powerful mechanism" table |
| Plugins load before the host is ready, or fail half-way | [Two-phase extension registration](patterns/two-phase-extension-registration.md) | Separate "declare" from "act" in the API | Extension loader commit and discard |
| Many plugins handle the same event, and one crash stops the host | [Fault-isolated event dispatch](patterns/fault-isolated-event-dispatch.md) | Write one combination rule per event kind | Extension runner; crash attribution |
| The same plugin must run in a UI, over RPC, and headless | [Host-owned UI port](patterns/host-owned-ui-port.md) | Publish a degradation table with the port | Extension UI context in TUI, RPC, print |
| Users cannot tell which of several same-named resources is active | [Layered resource discovery](patterns/layered-resource-discovery.md) | Record provenance for every resource | Precedence ranks, collision diagnostics, packages |
| Opening a folder could run its code | [Trust-gated loading](patterns/trust-gated-loading.md) | Load user plugins first; project plugins after trust | Two-pass resource loading |
| Built-in features cannot be replaced without a fork | [Built-ins through public seams](patterns/built-ins-through-public-seams.md) | Ship built-ins through the plugin registry | Tool override by name; operations interfaces |
| Plugin state is lost on restart or ignores branches | [Extension state in the host log](patterns/extension-state-in-host-log.md) | Give plugins a typed append and a rebuild event | Custom session entries |
| Many instructions compete for a small context window | [Progressive disclosure of instructions](patterns/progressive-disclosure.md) | Keep an index; load bodies on demand | Agent Skills index; `AGENTS.md` to `.pi/skills` |

## Core runtime design

| Need | Pattern | Start with | Pi example |
|---|---|---|---|
| Many vendors speak a few protocols | [Protocol and vendor axes](patterns/protocol-and-vendor-axes.md) | Name both axes in the types | `src/api/` and `src/providers/` in `pi-ai` |
| Code branches on an implementation's name | [Capabilities as data](patterns/capabilities-as-data.md) | Move one branch into a capability field | Model records and pure helpers |
| Generated files drift or get edited by hand | [Derived artifacts with a guarded source](patterns/derived-artifacts.md) | Give every generator a check mode | Model catalog, shrinkwrap, telemetry docs |
| Callers need both exception and event handling for streams | [In-band terminal streams](patterns/in-band-terminal-streams.md) | Never throw after returning the stream | `StreamFn` contract; lazy providers |
| One history must feed several targets with different formats | [Canonical record, projected per target](patterns/canonical-record-projected-per-target.md) | Make the projection a required, typed step | `convertToLlm`, cross-provider transform |
| Hidden globals make cancellation, telemetry, or testing fragile | [Explicit context](patterns/explicit-context.md) | Pass capabilities and lifecycle explicitly | Telemetry context; Chord `Context` |
| Work can be interrupted after an external side effect begins | [Durable effect state](patterns/durable-effect-state.md) | Persist intent and outcome separately | Harness design; Pico5 "effect sandwich" |
| Concurrent state updates are difficult to reason about | [Single-writer mutation](patterns/single-writer-mutation.md) | Plan separately, commit once | Session mutation line; `CredentialStore.modify` |

## Verification and release

| Need | Pattern | Start with | Pi example |
|---|---|---|---|
| Multiple implementations drift from a shared interface | [Conformance tests](patterns/conformance-tests.md) | Reuse one contract suite across adapters | Session, telemetry, and durable storage suites |
| Tests can spend money, leak keys, or depend on the developer's machine | [Hermetic tests, live tests by opt-in](patterns/hermetic-tests-live-opt-in.md) | Start the runner from an empty environment | `test.sh`, faux provider, key-gated suites |
| Source tests pass but published artifacts fail for consumers | [Consumer-oriented verification](patterns/consumer-oriented-verification.md) | Test packaging and clean installs | Packed-consumer smoke; binaries from source archive |
| Examples and docs drift from the product | [Documentation as a tested surface](patterns/documentation-as-tested-surface.md) | Type-check examples; test links | Docs link test; documentation-lift evals |
| Dependency changes reach users without review | [Dependencies as reviewed code](patterns/dependencies-as-reviewed-code.md) | Pin direct deps; ignore install scripts | Supply-chain hardening section |
| A failed release leaves users with a half-published version | [Staged, reversible release](patterns/staged-reversible-release.md) | Make "public" the last step | Draft first, un-draft last |

## Repository operations and governance

| Need | Pattern | Start with | Pi example |
|---|---|---|---|
| Repository process is tribal knowledge | [Repository as operating system](patterns/repository-as-operating-system.md) | Put local operating context near the code | `AGENTS.md`, `.pi/`, scripts, workflows |
| Several agent sessions share one checkout | [Multi-agent-safe working tree](patterns/multi-agent-safe-worktree.md) | Write the "never run" list | `AGENTS.md` git rules |
| The tracker receives more than maintainers can review | [Attention-budget contribution gate](patterns/attention-budget-gate.md) | Auto-close unknown authors; record approvals | `lgtm` and `lgtmi` workflows |
| Users assume protections the software does not provide | [Declared trust boundary](patterns/declared-trust-boundary.md) | Write the boundary and the isolation options | `SECURITY.md`, containerization guide |

If two patterns appear relevant, start with the one that reduces the largest current source of change or failure. Do not adopt both automatically.

For the design principles that connect these patterns, read [what makes Pi work](examples/pi/pi-essence.md).
