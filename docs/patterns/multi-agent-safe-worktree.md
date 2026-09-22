---
name: multi-agent-safe-worktree
description: Several agent sessions share one checkout.
category: repository-operations-and-governance
---

# Multi-agent-safe working tree

## Intent

Write version-control rules that stay safe when several agent sessions edit the same checkout at the same time.

## Use when

- more than one agent session, or an agent and a human, work in one directory;
- a single destructive command could erase another session's uncommitted work;
- agents review pull requests in the same checkout.

## Small shape

```text
assume : other sessions have unstaged work in this tree
commit : only files you changed; stage explicit paths; check status first
never  : reset --hard, checkout ., clean -fd, stash, add -A, add ., commit --no-verify, force push
conflict in a file you did not change -> abort and ask
review : read pull requests without switching the tree (diff, show ref:path)
```

## Pi example

**Observed:** Pi's [`AGENTS.md` L54–66](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/AGENTS.md#L54-L66) says: "Multiple pi sessions may be running in this cwd at the same time". It then lists the commit rules and the forbidden commands. For pull request reviews, it forbids `gh pr checkout` and `git switch` unless the user asks, and it points to `gh pr diff` and `git show <ref>:<path>`.

**Observed:** The same file asks agents to post comments from a file with `--body-file`, to end AI-posted comments with a disclaimer, and never to commit unless the user asks.

**Observed:** A CI workflow runs Pi's `/is` prompt on an issue, but only for staff. It exports the session, and a project extension imports it locally for replay ([`issue-analysis.yml`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/.github/workflows/issue-analysis.yml), [`import-repro.ts`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/.pi/extensions/import-repro.ts)).

**Inferred:** These rules are instructions only. Nothing blocks a destructive command mechanically. One worktree per session would be a stronger control.

**Recommended:** Write the "never" list first. Prefer separate worktrees when the tooling allows it.

## Benefits

- Parallel sessions do not destroy each other's work.
- Commits contain only the changes a session made.
- Reviews do not disturb work in progress.

## Trade-offs

- Explicit staging is slower than staging everything.
- Two sessions can still conflict on the same file.
- Compliance depends on the agent following the rules.

## Poor fit signals

- Each session already has its own worktree or sandbox.
- Only one person or agent ever works in the checkout.

## Adoption questions

- Can two sessions run in this checkout at the same time?
- Which commands would destroy another session's work?
- Is a separate worktree per session possible here?

## Related patterns

- [Repository as operating system](repository-as-operating-system.md)
- [Progressive disclosure of instructions](progressive-disclosure.md)
- [Single-writer mutation](single-writer-mutation.md)
