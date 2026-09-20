# Using Repository Patterns

## For a human

Start with the design problem, not with a favorite architecture.

1. Describe the constraint: for example, “provider changes keep leaking into the core” or “a workflow loses state after restart.”
2. Find the closest need in [`catalog.md`](catalog.md).
3. Read the pattern's fit, trade-offs, and “poor fit” section.
4. Read the linked case study.
5. Compare the pattern with the target repository.
6. Record whether to adopt, adapt, defer, or reject it.

## For an LLM

Use this repository as a source of recommendations, not as a policy file.

For each request:

1. Identify the target repository, audience, constraints, and desired outcome.
2. Search [`docs/catalog.md`](catalog.md) by need.
3. Extract the pattern's mechanism rather than copying its directory names.
4. Use the case study only for evidence and concrete illustrations.
5. State what is observed, what is inferred, and what is recommended.
6. Propose the smallest adoption step that could test the idea.
7. State what the source material does not prove.

A useful response shape is:

```text
Target need:
Candidate pattern:
Observed target state:
Relevant example:
Why it might fit:
Trade-offs and mismatch risks:
Smallest adoption step:
Evidence still needed:
```

## Vocabulary

| Label | Meaning |
|---|---|
| Observed | Directly supported by code, configuration, tests, or a cited document. |
| Inferred | A reasoned interpretation that may be useful but is not directly proven. |
| Recommended | A transferable option, subject to target-project judgment. |
| Trade-off | A cost, risk, complexity, or opportunity cost. |
| Example | A concrete implementation used to illuminate an idea. |

## What not to do

- Do not treat Pi's package count as a target architecture.
- Do not infer runtime correctness from documentation alone.
- Do not call a pattern “best practice” without naming its context.
- Do not introduce durable machinery when restartability is not a real requirement.
- Do not hide unresolved evidence gaps behind a polished diagram.
