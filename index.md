# Repository Patterns index

**Reconciled:** 2026-09-20
**Authority:** The repository owns stable guidance. This index owns the reading path and current coverage.

## Current scope

The first release documents patterns visible in the Pi repository and translates them into recommendations for unrelated repositories. The writing deliberately separates evidence from advice.

## Reading paths

| If you want to... | Start here |
|---|---|
| Choose a pattern for a current design problem | [`docs/catalog.md`](docs/catalog.md) |
| Understand the repository's own information architecture | [`docs/architecture.md`](docs/architecture.md) |
| Learn how to use the material as an LLM | [`docs/using-this-repo.md`](docs/using-this-repo.md) |
| See the ideas in one substantial codebase | [`docs/examples/pi/README.md`](docs/examples/pi/README.md) |
| Add a pattern | [`docs/templates/pattern.md`](docs/templates/pattern.md) |
| Add a case study | [`docs/templates/case-study.md`](docs/templates/case-study.md) |

## Coverage map

| Area | Current documents | Next useful expansion |
|---|---|---|
| Boundaries | Contract and adapter; core and host; opaque transport | A small web application and a data pipeline |
| Runtime reliability | Durable effects; single-writer mutation | Recovery after external callbacks and queues |
| Extensibility | Extensions before core | Plugin versioning and lifecycle isolation |
| Verification | Conformance tests; consumer-oriented verification | Security and performance evidence |
| Repository operations | Repository as operating system | Multi-repository and monorepo trade-offs |

## Current evidence boundary

- The Pi example is a source and documentation analysis at commit `3390bd93630965a12a0a1a5c36ce890ec22f7e1d`.
- The Pi case study does not claim that every documented experimental design is fully shipped or production-accepted.
- No target repository is assumed to need Pi's number of packages, durable runtime, or contributor gate.

## Repository state

- Local repository path: `/Users/david.helmus/workspace/personal/repository-patterns`
- Remote publication: not configured
- Linear binding: none yet
