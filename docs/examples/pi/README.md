# Case study: Pi Agent Harness

## Scope

This case study uses Pi at commit [`3390bd93630965a12a0a1a5c36ce890ec22f7e1d`](https://github.com/earendil-works/pi/tree/3390bd93630965a12a0a1a5c36ce890ec22f7e1d). It is a source, manifest, test, documentation, and workflow analysis.

The case study explains why selected structures are useful. It does not claim that every Pi design is appropriate elsewhere, or that an experimental design is fully runtime-accepted.

For a deeper package-level reading, see the [layered architecture notes](architecture.md).

## Why Pi is a useful example

Pi makes several change axes visible in one repository:

- model providers;
- reusable agent semantics;
- product host and UI modes;
- extensions;
- durable sessions and recovery;
- transport and remote boundaries;
- package and release verification.

## Layered map

| Layer | Pi location | Responsibility | Transferable idea |
|---|---|---|---|
| Repository operating system | `AGENTS.md`, `.pi/`, scripts, workflows | Local operating model and checks | Make repository context discoverable |
| Primitive substrate | `packages/chord`, `packages/telemetry`, `packages/tui` | Composition, observability, rendering | Keep independent contracts small |
| Provider boundary | `packages/ai` | Normalize model providers and streaming | Put vendor variation at the edge |
| Agent semantics | `packages/agent` | State, turns, tools, events | Separate semantic messages from provider messages |
| Durable execution | `packages/agent` harness and `packages/durable` | Recovery, lanes, effects, sessions | Model interruption explicitly when needed |
| Product host | `packages/coding-agent` | CLI, UI, resources, extensions | Keep product composition above reusable runtime |
| Remote path | `packages/protocol`, `client`, `server` | Framing, routing, attachments | Keep transport payloads domain-owned |
| Verification | `test.sh`, CI, release scripts, evals | Consumer and artifact evidence | Test what users actually consume |

## Pattern matrix

| Pattern | Observed in Pi | Recommendation | Important limit |
|---|---|---|---|
| Contract and adapter | `pi-ai`, telemetry, SQLite backend | Stabilize semantics before infrastructure | Avoid abstractions that erase real capability differences |
| Core and host | `pi-agent-core` plus `pi-coding-agent` | Keep UI and product policy out of the engine | A small product may not need the split |
| Durable effect state | Agent harness and session design | Persist intent and outcome around risky effects | Do not add it to short-lived local work |
| Single-writer mutation | Harness/session mutation line | Plan separately, commit once | Watch for throughput bottlenecks |
| Conformance tests | Storage and telemetry tests | Reuse behavior contracts across adapters | Account for intentional capability differences |
| Explicit context | Telemetry and agent lifecycle APIs | Pass lifecycle and capabilities visibly | Avoid a giant service bag |
| Extensions before core | Coding-agent extension API | Keep optional features outside core | Extension APIs become compatibility surfaces |
| Opaque transport | Protocol/client/server | Keep wire mechanics below domain meaning | Generic transport may be unnecessary locally |
| Consumer verification | Offline builds, clean installs, smoke tests | Test packaged artifacts | A smoke test cannot prove all live behavior |
| Repository as operating system | `AGENTS.md`, `.pi`, CI | Encode local workflow and source-of-truth rules | Keep instructions short and non-contradictory |

## Representative flow

```text
CLI mode
  -> coding-agent host
  -> agent session
  -> agent core
  -> normalized provider API
  -> model stream and tool execution
  -> events
  -> TUI, print, JSON, or RPC presentation
```

For durable work, the session/harness adds checkpoints and recovery state around the operations that can be interrupted.

## What to borrow

- The explicit separation between provider, agent, host, and presentation.
- Adapter contracts with reusable conformance tests.
- Extensions as a pressure valve for product-specific behavior.
- Consumer-level packaging and isolated test paths.
- Documentation that distinguishes current behavior from experimental design.

## What not to copy automatically

- Pi's number of packages.
- Its durable runtime for simple applications.
- Its contributor gate for a low-volume repository.
- Its external-sandbox trust model for security-sensitive automation.
- Its exact build scripts or directory names.

## Source map

- [Root README](https://github.com/earendil-works/pi/blob/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/README.md)
- [`package.json`](https://github.com/earendil-works/pi/blob/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/package.json)
- [`AGENTS.md`](https://github.com/earendil-works/pi/blob/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/AGENTS.md)
- [`CONTRIBUTING.md`](https://github.com/earendil-works/pi/blob/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/CONTRIBUTING.md)
- [`pi-agent-core` README](https://github.com/earendil-works/pi/blob/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/packages/agent/README.md)
- [`chord` README](https://github.com/earendil-works/pi/blob/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/packages/chord/README.md)
- [`pi-telemetry` README](https://github.com/earendil-works/pi/blob/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/packages/telemetry/README.md)
- [`protocol` README](https://github.com/earendil-works/pi/blob/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/packages/protocol/README.md)
- [`test.sh`](https://github.com/earendil-works/pi/blob/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/test.sh)
- [CI workflow](https://github.com/earendil-works/pi/blob/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/.github/workflows/ci.yml)
