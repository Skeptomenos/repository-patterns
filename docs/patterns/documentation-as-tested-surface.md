---
name: documentation-as-tested-surface
description: Examples and docs drift from the product.
category: verification-and-release
---

# Documentation as a tested surface

## Intent

Treat documentation and examples as product surface. Type-check the examples, test the links, ship the documents with the package, and measure whether they help.

## Use when

- examples are the main way users, or agents, learn an API;
- an agent reads the product's own documentation at run time;
- documentation drift has caused support load or wrong answers.

## Small shape

```text
examples -> part of the type check + imported by tests
docs     -> test for broken links, orphaned pages, and slug collisions
package  -> ships docs and examples for agents to read at run time
eval     -> same build with and without docs; compare paired runs
```

## Pi example

**Observed:** The root type check includes `packages/coding-agent/examples/**/*` ([`tsconfig.json` L57](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/tsconfig.json#L57)). Tests import examples directly. [`documentation.test.ts`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/test/documentation.test.ts#L132-L176) fails on broken links and orphaned Markdown pages.

**Observed:** The published coding agent includes `docs` and `examples` in its `files` list. The root README says you can "ask the agent to explain itself".

**Observed:** `pi-evals` measures documentation lift. Its Dockerfile builds a `without-docs-install` stage that deletes the README, changelog, docs, and examples from an otherwise identical install ([`Dockerfile` L14–15](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/evals/docker/Dockerfile#L14-L15)). The runner plans every paired run in advance and alternates their order. When a pair is incomplete, it withholds the headline lift. The README says one repetition cannot establish stability ([`evals README`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/evals/README.md)).

**Observed (drift):** What is not checked drifts. `tsconfig.examples.json` is referenced by no script and maps a file that does not exist. The repository's own `.pi/extensions/` folder is outside the type check, and [`prompt-url-widget.ts` L230](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/.pi/extensions/prompt-url-widget.ts#L230) still subscribes to `session_switch`, an event the changelog records as removed.

**Inferred:** Paired runs turn "the docs help" from an opinion into a measurement.

**Recommended:** Add examples to the type check and add one link test first. Measure lift only when agents depend on the documents.

## Benefits

- Examples keep compiling as the API changes.
- Broken links and orphaned pages fail before release.
- The value of documentation becomes measurable.

## Trade-offs

- Paid model runs and container builds cost time and money.
- Evaluation results are noisy and need repetitions.
- Every checked example becomes code to maintain.

## Poor fit signals

- The documentation is short and has no runnable examples.
- No agent or tool reads the documentation at run time.

## Adoption questions

- Which examples would break silently today?
- Which documents does an agent read to answer users?
- What result would convince you that a document helps?

## Related patterns

- [Consumer-oriented verification](consumer-oriented-verification.md)
- [Progressive disclosure of instructions](progressive-disclosure.md)
- [Hermetic tests, live tests by opt-in](hermetic-tests-live-opt-in.md)
