# Repository Patterns index

**Reconciled:** 2026-09-22
**Authority:** The repository owns stable guidance. This index owns the reading path and current coverage.

## Current scope

The library documents 36 patterns visible in the Pi repository and translates them into recommendations for unrelated repositories. The writing deliberately separates evidence from advice.

## Reading paths

| If you want to... | Start here |
|---|---|
| Choose a pattern for a current design problem | [`docs/catalog.md`](docs/catalog.md) |
| Understand why Pi's patterns fit together | [`docs/examples/pi/pi-essence.md`](docs/examples/pi/pi-essence.md) |
| See how Pi arranges folders, packages, and documents | [`docs/examples/pi/pi-repository-layout.md`](docs/examples/pi/pi-repository-layout.md) |
| Understand the repository's own information architecture | [`docs/library-architecture.md`](docs/library-architecture.md) |
| Learn how to use the material as an LLM | [`docs/using-this-repo.md`](docs/using-this-repo.md) |
| See the ideas in one substantial codebase | [`docs/examples/pi/pi-case-study.md`](docs/examples/pi/pi-case-study.md) |
| Add a pattern | [`docs/templates/pattern-template.md`](docs/templates/pattern-template.md) |
| Add a case study | [`docs/templates/case-study-template.md`](docs/templates/case-study-template.md) |
| See which patterns this repository applies to itself | [`docs/decisions/0003-self-adoption.md`](docs/decisions/0003-self-adoption.md) |
| Understand the link and discovery rules | [`docs/decisions/0004-github-links.md`](docs/decisions/0004-github-links.md) |

## Coverage map

| Area | Current patterns | Next useful expansion |
|---|---|---|
| Structure and boundaries | Change-axis boundaries; contract and adapter; core and host; application-neutral substrate; runtime-named entry points; executable architecture checks; opaque transport; visible maturity | A small web application and a data pipeline |
| Extensibility and plugins | Extensions before core; customization ladder; two-phase registration; fault-isolated dispatch; host-owned UI port; layered discovery; trust-gated loading; built-ins through public seams; extension state in the host log; progressive disclosure | Plugin versioning and compatibility over time |
| Core runtime design | Protocol and vendor axes; capabilities as data; derived artifacts; in-band terminal streams; canonical record projected per target; explicit context; durable effect state; single-writer mutation | Recovery after external callbacks and queues |
| Verification and release | Conformance tests; hermetic tests; consumer-oriented verification; documentation as a tested surface; dependencies as reviewed code; staged, reversible release | Security and performance evidence |
| Repository operations and governance | Repository as operating system; multi-agent-safe working tree; attention-budget gate; declared trust boundary | Multi-repository and monorepo trade-offs |

## Current evidence boundary

- The Pi example is a source, documentation, workflow, and git-history analysis at release v0.87.1, commit `f07218c4d4bbc12bef056a7058c3dd49dfe41abe`.
- The first analysis used commit `3390bd93630965a12a0a1a5c36ce890ec22f7e1d`. Since 2026-09-22, v0.87.1 owns every claim and link. The case study lists the [corrections](docs/examples/pi/pi-case-study.md#corrections-since-the-first-analysis).
- The Pi case study does not claim that every documented experimental design is fully shipped or production-accepted. At v0.87.1 the durable harness runs only on an experimental path.
- No target repository is assumed to need Pi's number of packages, durable runtime, or contributor gate.

## Candidate patterns not yet written

These appeared in the v0.87.1 analysis. They have evidence but were judged too narrow or too language-specific for a page today.

- Source-ordered concurrent tool batches (`pi-agent-core` `agent-loop.ts`).
- Line-array UI components with swappable differential renderers (`pi-tui`).
- Optional native capability with graceful absence (`pi-tui` native helpers).
- Host-injected modules for build-free TypeScript plugins (`pi-coding-agent` extension loader).
- Out-of-band data channel with a minimum client version (partly covered in derived artifacts).

## Repository state

- Local checkout: `$HOME/workspace/personal/repository-patterns`
- Remote publication: [github.com/Skeptomenos/repository-patterns](https://github.com/Skeptomenos/repository-patterns), branch `main`
- Validation: `./scripts/check-docs.sh` and `python3 scripts/test_check_docs.py`, run locally and in CI
- Linear binding: none yet
