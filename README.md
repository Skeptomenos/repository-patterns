# Repository Patterns

Repository Patterns is a small, recommendation-oriented library for designing and improving software repositories, agent harnesses, and developer workflows.

It answers questions such as:

- Where should a boundary live?
- When should a core become an adapter or an extension?
- How can a workflow survive retries and restarts?
- What evidence should a repository collect before calling a change complete?

The examples are deliberately concrete. The first case study is [Pi Agent Harness](https://github.com/earendil-works/pi), because Pi makes package boundaries, extension points, durable execution, and consumer-level verification unusually visible.

This is not a rulebook. A pattern is a useful option when its context, benefits, and costs match the problem. Each page should make that judgment easier.

## Fast path for an LLM

An agent enters at [`AGENTS.md`](AGENTS.md). Every document is reachable from there by following relative links, and every file name is unique, so a search by name finds exactly one file.

1. Read [`index.md`](index.md) for the current map.
2. Select a need in [`docs/catalog.md`](docs/catalog.md). The catalog groups 36 patterns under five questions: structure, extensibility, core runtime design, verification, and repository operations.
3. Read the matching pattern page.
4. Read the relevant [Pi case study](docs/examples/pi/pi-case-study.md), or another example as the library grows. [What makes Pi work](docs/examples/pi/pi-essence.md) connects the patterns to eight design principles.
5. Use the [adoption worksheet](docs/templates/adoption-worksheet.md) to compare the pattern with the target repository.

Ask the LLM to return: the observed target state, the candidate pattern, fit, trade-offs, the smallest adoption step, and what remains unverified.

## Architecture of this repository

```mermaid
flowchart LR
    Need[Need or design question] --> Catalog[Pattern catalog]
    Catalog --> Pattern[Pattern recommendation]
    Pattern --> Example[Repository case study]
    Example --> Worksheet[Adoption worksheet]
    Worksheet --> Decision[Context-specific decision]
```

The repository separates reusable ideas from evidence and from decisions made in a particular project.

## Start here

| Document | Question it answers |
|---|---|
| [`docs/catalog.md`](docs/catalog.md) | Which pattern might help? |
| [`docs/library-architecture.md`](docs/library-architecture.md) | How is this meta repository organized? |
| [`docs/patterns/pattern-index.md`](docs/patterns/pattern-index.md) | What does each pattern mean? |
| [`docs/examples/pi/pi-case-study.md`](docs/examples/pi/pi-case-study.md) | How do the ideas appear in a real repository? |
| [`docs/examples/pi/pi-essence.md`](docs/examples/pi/pi-essence.md) | Which design principles make Pi work, and where does it drift? |
| [`docs/examples/pi/pi-repository-layout.md`](docs/examples/pi/pi-repository-layout.md) | How does Pi arrange folders, packages, and documents? |
| [`docs/using-this-repo.md`](docs/using-this-repo.md) | How should a human or LLM use the material? |
| [`docs/templates/pattern-template.md`](docs/templates/pattern-template.md), [`docs/templates/case-study-template.md`](docs/templates/case-study-template.md), [`docs/templates/adoption-worksheet.md`](docs/templates/adoption-worksheet.md) | How can a new pattern or case study be added, or a pattern adopted? |
| [`docs/decisions/0001-recommendations-not-rules.md`](docs/decisions/0001-recommendations-not-rules.md) | Why is this a recommendation library rather than a rulebook? |

## Scope boundary

This repository is about reusable repository and agent-system design patterns. It is not a replacement for project-specific architecture, security review, product decisions, or live acceptance evidence.
