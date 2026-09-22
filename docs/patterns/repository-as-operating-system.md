---
name: repository-as-operating-system
description: Repository process is tribal knowledge.
category: repository-operations-and-governance
---

# Repository as operating system

## Intent

Make the repository's local way of working discoverable to humans and agents through concise instructions, scripts, examples, and checks.

## Use when

- contributors repeatedly miss local conventions;
- agents need safe commands and acceptance criteria;
- generated files have a source-of-truth rule;
- testing and release paths are easy to misuse.

## Small shape

```text
README: purpose and entry point
AGENTS: portable local context
scripts: repeatable operations
tests/CI: executable expectations
examples: consumer guidance
```

Keep each document responsible for one kind of meaning. Put mutable status in an index or plan rather than turning the README into a diary.

## Pi example

**Observed:** Pi combines a concise README, `AGENTS.md`, contributor guidance, `.pi` prompts and skills, safe test scripts, package-local documentation, and CI/release checks. Its own agent tooling is used to maintain the repository.

See [`AGENTS.md`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/AGENTS.md), [`CONTRIBUTING.md`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/CONTRIBUTING.md), and the [root README](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/README.md).

**Observed (v0.87.1):** Pi layers its guidance:

- a short `AGENTS.md` with standing rules;
- skills loaded on demand, for releasing and interactive testing;
- prompt templates as maintainer macros: `/is`, `/pr`, `/cl`, `/wr`;
- a project extension that imports CI agent sessions for local replay.

`CONTRIBUTING.md` tells contributors to run agents from the repository root, so they pick up `AGENTS.md`. See [Progressive disclosure of instructions](progressive-disclosure.md) and [Multi-agent-safe working tree](multi-agent-safe-worktree.md).

**Observed (v0.87.1):** Some rules have a mechanism behind them: erasable-only syntax (a compiler option), exact pins, the lockfile gate, and generated-file checks. Others are instructions only. The linter turns `noExplicitAny` off, although `AGENTS.md` forbids `any`. Two inline `await import(` calls remain in package sources, although `AGENTS.md` forbids them. Changelog placement is audited by the `/cl` prompt, not by a check.

**Observed (drift):** Configuration drifts like instructions do. `CONTRIBUTING.md` sends provider-test guidance to `AGENTS.md`, but it lives in `.pi/skills/add-llm-provider.md`. Removed packages are still referenced in `biome.json`, the pre-commit hook, and `tsconfig.json`.

**Recommended:** Start with a small local context file and one reliable check. Add more structure only when repeated failures justify it. Back each rule that matters with a check, and derive lists from manifests instead of copying them.

## Benefits

- Reduces tribal knowledge.
- Gives agents a safe navigation path.
- Makes generated artifacts and acceptance commands clearer.

## Trade-offs

- Instruction sprawl can create contradictions.
- A repository can optimize for agents at the expense of human readers.
- Local instructions still need maintenance and review.
- A rule without a mechanism drifts silently.

## Poor fit signals

- The proposed instruction repeats universal guidance available elsewhere.
- The rule has no observed failure or local exception behind it.
- The document has become a second project-management system.

## Adoption questions

- What does a new contributor need to know in the first five minutes?
- Which command is the narrowest trustworthy validation path?
- Which files are generated, and where is their source of truth?
- Which rules have a mechanism behind them, and which rely on memory?

## Related patterns

- [Progressive disclosure of instructions](progressive-disclosure.md)
- [Multi-agent-safe working tree](multi-agent-safe-worktree.md)
- [Executable architecture checks](executable-architecture-checks.md)
- [Attention-budget contribution gate](attention-budget-gate.md)
