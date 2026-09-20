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

See [`AGENTS.md`](https://github.com/earendil-works/pi/blob/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/AGENTS.md), [`CONTRIBUTING.md`](https://github.com/earendil-works/pi/blob/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/CONTRIBUTING.md), and the [root README](https://github.com/earendil-works/pi/blob/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/README.md).

**Recommended:** Start with a small local context file and one reliable check. Add more structure only when repeated failures justify it.

## Benefits

- Reduces tribal knowledge.
- Gives agents a safe navigation path.
- Makes generated artifacts and acceptance commands clearer.

## Trade-offs

- Instruction sprawl can create contradictions.
- A repository can optimize for agents at the expense of human readers.
- Local instructions still need maintenance and review.

## Poor fit signals

- The proposed instruction repeats universal guidance available elsewhere.
- The rule has no observed failure or local exception behind it.
- The document has become a second project-management system.

## Adoption questions

- What does a new contributor need to know in the first five minutes?
- Which command is the narrowest trustworthy validation path?
- Which files are generated, and where is their source of truth?
