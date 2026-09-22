# Case study: Pi Agent Harness

## Scope

This case study uses Pi at release [v0.87.1](https://github.com/earendil-works/pi/tree/f07218c4d4bbc12bef056a7058c3dd49dfe41abe), commit `f07218c4d4bbc12bef056a7058c3dd49dfe41abe` (2026-09-22). It is a source, manifest, test, documentation, workflow, and git-history analysis.

**Superseded pin:** The first analysis (2026-09-20) used commit `3390bd93630965a12a0a1a5c36ce890ec22f7e1d`. Since 2026-09-22, every claim and link in this library uses v0.87.1. The re-reading corrected three earlier claims. See [corrections](#corrections-since-the-first-analysis).

The case study explains why selected structures are useful. It does not claim that every Pi design is appropriate elsewhere, or that an experimental design is fully runtime-accepted.

Read next:

- [What makes Pi work](pi-essence.md): the eight design principles behind the patterns.
- [Repository layout](pi-repository-layout.md): an annotated map of folders, packages, and documents.
- [Layered architecture notes](pi-architecture.md): the dependency shape and each boundary.

## Why Pi is a useful example

Pi makes several change axes visible in one repository:

- model providers and wire protocols;
- reusable agent semantics;
- product host and UI modes;
- extensions, skills, prompt templates, themes, and packages;
- durable sessions and recovery;
- transport and remote boundaries;
- package, release, and supply-chain verification;
- a repository operated by its own agent.

## Layered map

| Layer | Pi location | Responsibility | Transferable idea |
|---|---|---|---|
| Repository operating system | `AGENTS.md`, `.pi/`, scripts, workflows | Local operating model, agent procedures, and checks | Make repository context discoverable, and back rules with checks |
| Substrate | `packages/chord` | Application-neutral composition, services, replicated state, context | Keep generic machinery free of product words |
| Primitives | `packages/telemetry`, `packages/tui` | Observability contracts, terminal rendering | Keep independent contracts small |
| Provider boundary | `packages/ai` | Wire protocols, vendors, catalogs, streaming | Separate protocol from vendor; put variation in data |
| Agent semantics | `packages/agent` | State, turns, tools, events | Separate application messages from provider messages |
| Durable execution | `packages/agent` harness (experimental path), `packages/durable` (Pico5 storage) | Recovery, lanes, effects, sessions | Model interruption explicitly when needed |
| Storage backends | `packages/session-backends/*` | Session storage per engine and runtime | Group implementations of one contract in a family folder |
| Product host | `packages/coding-agent` | CLI, modes, resources, extensions, packages, trust | Keep product composition above reusable runtime |
| Remote path | `packages/protocol`, `client`, `server` | Framing, routing, attachments | Keep transport payloads domain-owned |
| Verification | `test.sh`, CI, release scripts, `packages/evals` | Hermetic tests, consumer and artifact evidence, documentation lift | Test what users actually consume |

## Pattern matrix

| Pattern | Observed in Pi | Recommendation | Important limit |
|---|---|---|---|
| [Change-axis boundaries](../../patterns/change-axis-boundaries.md) | Package per change source; extraction and eviction in history | Draw boundaries around what changes | Every package costs release work |
| [Contract and adapter](../../patterns/contract-and-adapter.md) | `pi-ai`, telemetry, SQLite backends | Stabilize semantics before infrastructure | Avoid abstractions that erase real capability differences |
| [Core and host](../../patterns/core-and-host.md) | `pi-agent-core` plus `pi-coding-agent`; `AgentSession` and its modes | Keep UI and product policy out of the engine | A small product may not need the split |
| [Application-neutral substrate](../../patterns/application-neutral-substrate.md) | `chord` forbidden terms and boundary test | Enforce the vocabulary with a test | Two vocabularies need adapters |
| [Runtime-named entry points](../../patterns/runtime-named-entry-points.md) | `pi-durable` storage subpaths, browser smoke | Name runtime adapters; prove portability by bundling | The smoke covers only what it imports |
| [Executable architecture checks](../../patterns/executable-architecture-checks.md) | Runtime-deps audit, entry-point budgets | Encode the rule that broke last | Hand-kept lists still drift |
| [Opaque transport](../../patterns/opaque-transport.md) | Protocol, client, server; grammar owned by Chord | Keep wire mechanics below domain meaning | Generic transport may be unnecessary locally |
| [Visible maturity](../../patterns/visible-maturity.md) | Source-only experimental exports; status lines; gap ledgers | Put status on line one | Status labels rot without checks |
| [Extensions before core](../../patterns/extensions-before-core.md) | Coding-agent extension API | Keep optional features outside core | Extension APIs become compatibility surfaces |
| [Customization ladder](../../patterns/customization-ladder.md) | Quickstart "least powerful mechanism" table | Point users to the weakest mechanism that works | Each rung is a surface to keep |
| [Two-phase extension registration](../../patterns/two-phase-extension-registration.md) | Loader commit and discard; stale contexts | Declare before act; load all-or-nothing | Authors learn two phases |
| [Fault-isolated event dispatch](../../patterns/fault-isolated-event-dispatch.md) | Per-event rules; guards fail closed; crash attribution | One combination rule per event kind | Rules are easy to misread |
| [Host-owned UI port](../../patterns/host-owned-ui-port.md) | UI context in TUI, RPC, and print modes | Publish a degradation table | Rich components do not cross processes |
| [Layered resource discovery](../../patterns/layered-resource-discovery.md) | Precedence ranks; winner and loser diagnostics | Record provenance first | Different rules per kind confuse |
| [Trust-gated loading](../../patterns/trust-gated-loading.md) | Two-pass loading; SDK defaults to trusted | Default to untrusted in every host | Trust is not a sandbox |
| [Built-ins through public seams](../../patterns/built-ins-through-public-seams.md) | Tool override by name; operations interfaces | Ship built-ins through the plugin registry | Built-in commands stay static |
| [Extension state in the host log](../../patterns/extension-state-in-host-log.md) | Custom session entries | Typed append plus rebuild event | Replay cost grows with entries |
| [Progressive disclosure of instructions](../../patterns/progressive-disclosure.md) | Agent Skills index; `AGENTS.md` to `.pi/skills` | Index always; bodies on demand | The agent can miss a skill |
| [Protocol and vendor axes](../../patterns/protocol-and-vendor-axes.md) | `src/api/` and `src/providers/` | Name both axes in the types | Compatibility flags accumulate |
| [Capabilities as data](../../patterns/capabilities-as-data.md) | Model records and pure helpers | Move name branches into fields | Some behaviour resists fields |
| [Derived artifacts with a guarded source](../../patterns/derived-artifacts.md) | Model catalog, shrinkwrap, telemetry docs | Every generator gets a check mode | Online builds depend on the network |
| [In-band terminal streams](../../patterns/in-band-terminal-streams.md) | `StreamFn` contract; lazy providers | Never throw after returning a stream | The partial result is live |
| [Canonical record, projected per target](../../patterns/canonical-record-projected-per-target.md) | `convertToLlm`; cross-provider transform | Make the projection a typed step | Downgrades lose information |
| [Explicit context](../../patterns/explicit-context.md) | Telemetry context; Chord `Context` in the harness | Pass lifecycle and capabilities visibly | Avoid a giant service bag |
| [Durable effect state](../../patterns/durable-effect-state.md) | Harness design (experimental); Pico5 effect sandwich | Persist intent and outcome around risky effects | The shipped CLI does not use it yet |
| [Single-writer mutation](../../patterns/single-writer-mutation.md) | Session mutation line; `CredentialStore.modify` | Plan separately, commit once | Ownership is enforced by the host only |
| [Conformance tests](../../patterns/conformance-tests.md) | Session, telemetry, and durable storage suites | Reuse behavior contracts across adapters | Account for intentional capability differences |
| [Hermetic tests, live tests by opt-in](../../patterns/hermetic-tests-live-opt-in.md) | `test.sh`; faux provider; key-gated suites | Start tests from an empty environment | Wire regressions need live runs |
| [Consumer-oriented verification](../../patterns/consumer-oriented-verification.md) | Packed-consumer smoke on the release path | Install only what the consumer installs | A smoke test cannot prove all live behavior |
| [Documentation as a tested surface](../../patterns/documentation-as-tested-surface.md) | Examples type-checked; docs link test; lift evals | Check examples and links first | Evals are paid and noisy |
| [Dependencies as reviewed code](../../patterns/dependencies-as-reviewed-code.md) | Pins, age gate, lockfile gate, derived shrinkwrap | Pin and ignore install scripts first | Routine overrides stop being controls |
| [Staged, reversible release](../../patterns/staged-reversible-release.md) | Draft first, un-draft last, idempotent publish | Make "public" the last step | Long pipelines |
| [Repository as operating system](../../patterns/repository-as-operating-system.md) | `AGENTS.md`, `.pi`, CI | Encode local workflow and source-of-truth rules | Keep instructions short and non-contradictory |
| [Multi-agent-safe working tree](../../patterns/multi-agent-safe-worktree.md) | `AGENTS.md` git rules for parallel sessions | Write the "never run" list | Instructions only; no mechanism |
| [Attention-budget contribution gate](../../patterns/attention-budget-gate.md) | Auto-close; `lgtm` registry | Protect maintainer attention | Can deter new contributors |
| [Declared trust boundary](../../patterns/declared-trust-boundary.md) | `SECURITY.md`; containerization guide | Declare the boundary; point to isolation | Users must isolate themselves |

## Representative flow

```text
CLI mode
  -> coding-agent host (modes/: interactive, print, JSON, RPC, SDK)
  -> AgentSession (core/: resources, extensions, tools, trust)
  -> Agent (pi-agent-core: loop, queues, events)
  -> normalized provider API (pi-ai: protocol + vendor)
  -> model stream and tool execution
  -> events
  -> TUI, print, JSON, or RPC presentation
```

**Observed:** The shipped CLI builds the plain `Agent`. The durable harness adds checkpoints and recovery state around operations that can be interrupted, but at v0.87.1 it runs only on the experimental server and worker path behind `PI_EXPERIMENTAL=1`.

## What to borrow

- The explicit separation between provider, agent, host, and presentation.
- Adapter contracts with reusable conformance tests.
- Extensions as a pressure valve for product-specific behavior, with a ladder that keeps users on the weakest mechanism that works.
- Architecture rules encoded as fast checks.
- Consumer-level packaging and isolated test paths.
- Documentation that distinguishes current behavior from experimental design.

## What not to copy automatically

- Pi's number of packages.
- Its durable runtime for simple applications.
- Its contributor gate for a low-volume repository.
- Its external-sandbox trust model for security-sensitive automation.
- Its exact build scripts or directory names.

## Corrections since the first analysis

- **Durable runtime status:** The earlier text said `pi-durable` "exposes a smaller public surface while the broader durable design remains experimental". At v0.87.1, `pi-durable` is a second, separate design (Pico5) with a normative specification; only its storage layers are implemented. The harness is experimental and not used by the shipped CLI. See [Durable effect state](../../patterns/durable-effect-state.md).
- **Where consumer checks run:** The earlier text listed isolated installs and binaries among Pi's checks without saying when they run. Pull request CI runs build, check, and tests. Packed-consumer installs, Bun installs, and binaries run on the release path. See [Consumer-oriented verification](../../patterns/consumer-oriented-verification.md).
- **Subscriptions:** The earlier text said `pi-protocol` owns subscriptions. Subscribe and unsubscribe are ordinary requests that carry Chord control calls. Only update delivery is a protocol envelope. See [Opaque transport](../../patterns/opaque-transport.md).

## Source map

- [Root README](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/README.md)
- [`package.json`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/package.json)
- [`AGENTS.md`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/AGENTS.md)
- [`CONTRIBUTING.md`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/CONTRIBUTING.md)
- [`SECURITY.md`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/SECURITY.md)
- [`pi-agent-core` README](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/agent/README.md)
- [`pi-ai` README](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/ai/README.md)
- [`chord` README](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/chord/README.md) and [`PLANNING.md`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/chord/PLANNING.md)
- [`pi-telemetry` README](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/telemetry/README.md)
- [`protocol` README](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/protocol/README.md)
- [Coding-agent documentation](https://github.com/earendil-works/pi/tree/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/docs)
- [Agent harness specification](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/agent/docs/harness.md)
- [`test.sh`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/test.sh)
- [`scripts/`](https://github.com/earendil-works/pi/tree/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/scripts)
- [CI workflow](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/.github/workflows/ci.yml)
