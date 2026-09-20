# Decision 0001: recommendations, not rules

## Context

The repository is intended to help an LLM generate ideas for unrelated projects. A universal rulebook would encourage cargo-cult architecture and would not know the target project's constraints.

## Decision

Pattern pages will describe recommendations with explicit fit conditions, benefits, trade-offs, poor-fit signals, and adoption questions. Case studies will separate observed facts from inference and advice.

## Consequences

- Readers must exercise judgment.
- The catalog can serve different languages, runtimes, and repository sizes.
- The repository is less suitable as an automated compliance checker.
- Evidence quality and source links become important.

## Alternatives considered

- A normative repository standard: rejected because the target projects are intentionally unrelated.
- A collection of unstructured essays: rejected because LLMs need predictable routing and metadata.
