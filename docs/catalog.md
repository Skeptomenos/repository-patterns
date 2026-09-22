# Pattern catalog

Choose by need. The catalog is a routing layer, not a ranking. The groups follow the questions a design review asks: where boundaries go, how the system grows, how the core behaves, how it is verified, and how the repository is operated.

## Structure and boundaries

| Need | Pattern | Start with | Pi example |
|---|---|---|---|
| One kind of change keeps touching many packages | [[change-axis-boundaries]] | List the sources of change, then give each one owner | Package per change source; telemetry extracted, `mom` and `web-ui` evicted |
| Vendor or infrastructure changes keep spreading through the core | [[contract-and-adapter]] | Define the stable semantic contract first | `pi-ai`, `pi-agent-core`, SQLite backend |
| Reusable runtime logic is tangled with CLI or UI behavior | [[core-and-host]] | Move product composition to a host layer | `pi-agent-core` and `pi-coding-agent`; `AgentSession` and its modes |
| Generic machinery keeps absorbing product concepts | [[application-neutral-substrate]] | Write a forbidden-term list and one boundary test | `chord` |
| Server-only imports break browser or edge consumers | [[runtime-named-entry-points]] | Name adapters after the runtime; bundle to prove it | `pi-durable` storage subpaths, browser smoke |
| Architecture rules live only in diagrams and reviews | [[executable-architecture-checks]] | Encode the rule that broke last | Runtime-deps audit, entry-point budgets |
| Transport code is accumulating business semantics | [[opaque-transport]] | Keep wire mechanics below domain contracts | `pi-protocol`, `pi-client`, `pi-server` |
| Readers cannot tell shipped behavior from plans | [[visible-maturity]] | Put a status line at the top of every plan | Source-only experimental exports; gap ledgers |

## Extensibility and plugins

| Need | Pattern | Start with | Pi example |
|---|---|---|---|
| Every feature wants another core flag or special case | [[extensions-before-core]] | Test whether a stable extension seam is enough | Pi extensions and minimal-core guidance |
| Users reach for code where instructions would do | [[customization-ladder]] | Publish the mechanisms in order of power | Quickstart "least powerful mechanism" table |
| Plugins load before the host is ready, or fail half-way | [[two-phase-extension-registration]] | Separate "declare" from "act" in the API | Extension loader commit and discard |
| Many plugins handle the same event, and one crash stops the host | [[fault-isolated-event-dispatch]] | Write one combination rule per event kind | Extension runner; crash attribution |
| The same plugin must run in a UI, over RPC, and headless | [[host-owned-ui-port]] | Publish a degradation table with the port | Extension UI context in TUI, RPC, print |
| Users cannot tell which of several same-named resources is active | [[layered-resource-discovery]] | Record provenance for every resource | Precedence ranks, collision diagnostics, packages |
| Opening a folder could run its code | [[trust-gated-loading]] | Load user plugins first; project plugins after trust | Two-pass resource loading |
| Built-in features cannot be replaced without a fork | [[built-ins-through-public-seams]] | Ship built-ins through the plugin registry | Tool override by name; operations interfaces |
| Plugin state is lost on restart or ignores branches | [[extension-state-in-host-log]] | Give plugins a typed append and a rebuild event | Custom session entries |
| Many instructions compete for a small context window | [[progressive-disclosure]] | Keep an index; load bodies on demand | Agent Skills index; `AGENTS.md` to `.pi/skills` |

## Core runtime design

| Need | Pattern | Start with | Pi example |
|---|---|---|---|
| Many vendors speak a few protocols | [[protocol-and-vendor-axes]] | Name both axes in the types | `src/api/` and `src/providers/` in `pi-ai` |
| Code branches on an implementation's name | [[capabilities-as-data]] | Move one branch into a capability field | Model records and pure helpers |
| Generated files drift or get edited by hand | [[derived-artifacts]] | Give every generator a check mode | Model catalog, shrinkwrap, telemetry docs |
| Callers need both exception and event handling for streams | [[in-band-terminal-streams]] | Never throw after returning the stream | `StreamFn` contract; lazy providers |
| One history must feed several targets with different formats | [[canonical-record-projected-per-target]] | Make the projection a required, typed step | `convertToLlm`, cross-provider transform |
| Hidden globals make cancellation, telemetry, or testing fragile | [[explicit-context]] | Pass capabilities and lifecycle explicitly | Telemetry context; Chord `Context` |
| Work can be interrupted after an external side effect begins | [[durable-effect-state]] | Persist intent and outcome separately | Harness design; Pico5 "effect sandwich" |
| Concurrent state updates are difficult to reason about | [[single-writer-mutation]] | Plan separately, commit once | Session mutation line; `CredentialStore.modify` |

## Verification and release

| Need | Pattern | Start with | Pi example |
|---|---|---|---|
| Multiple implementations drift from a shared interface | [[conformance-tests]] | Reuse one contract suite across adapters | Session, telemetry, and durable storage suites |
| Tests can spend money, leak keys, or depend on the developer's machine | [[hermetic-tests-live-opt-in]] | Start the runner from an empty environment | `test.sh`, faux provider, key-gated suites |
| Source tests pass but published artifacts fail for consumers | [[consumer-oriented-verification]] | Test packaging and clean installs | Packed-consumer smoke; binaries from source archive |
| Examples and docs drift from the product | [[documentation-as-tested-surface]] | Type-check examples; test links | Docs link test; documentation-lift evals |
| Dependency changes reach users without review | [[dependencies-as-reviewed-code]] | Pin direct deps; ignore install scripts | Supply-chain hardening section |
| A failed release leaves users with a half-published version | [[staged-reversible-release]] | Make "public" the last step | Draft first, un-draft last |

## Repository operations and governance

| Need | Pattern | Start with | Pi example |
|---|---|---|---|
| Repository process is tribal knowledge | [[repository-as-operating-system]] | Put local operating context near the code | `AGENTS.md`, `.pi/`, scripts, workflows |
| Several agent sessions share one checkout | [[multi-agent-safe-worktree]] | Write the "never run" list | `AGENTS.md` git rules |
| The tracker receives more than maintainers can review | [[attention-budget-gate]] | Auto-close unknown authors; record approvals | `lgtm` and `lgtmi` workflows |
| Users assume protections the software does not provide | [[declared-trust-boundary]] | Write the boundary and the isolation options | `SECURITY.md`, containerization guide |

If two patterns appear relevant, start with the one that reduces the largest current source of change or failure. Do not adopt both automatically.

For the design principles that connect these patterns, read [[pi-essence|what makes Pi work]].
