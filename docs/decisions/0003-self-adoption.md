# Decision 0003: which patterns this repository applies to itself

**Date:** 2026-09-22

## Context

A library of repository patterns should follow its own advice where the advice fits. It should also say where the advice does not fit, because "recommendations, not rules" ([[0001-recommendations-not-rules]]) applies here too. This record uses the decisions of the [[adoption-worksheet]]: adopt, adapt, defer, or reject.

## Decision

| Pattern | Decision | How it applies here |
|---|---|---|
| [[repository-as-operating-system]] | Adopt | `AGENTS.md` is the entry point for agents. `CONTRIBUTING.md`, `scripts/`, and CI carry the operating model. |
| [[progressive-disclosure]] | Adopt | `AGENTS.md` stays short and routes to [[index]], then [[catalog]], then one page. Pattern frontmatter is the always-cheap index. |
| [[executable-architecture-checks]] | Adopt | `scripts/check_docs.py` enforces unique names, link resolution, reachability, page structure, frontmatter, catalog coverage, and one evidence pin per source repository. |
| [[documentation-as-tested-surface]] | Adopt the checks; defer the evals | The link and orphan checks mirror Pi's documentation test. Measuring documentation lift is deferred until agents depend on the library often enough to measure. |
| [[conformance-tests]] | Adapt | Every pattern page must pass the same structure check, so pages stay comparable. |
| [[derived-artifacts]] | Adapt | Frontmatter descriptions were derived from the catalog once. A check keeps the catalog, frontmatter, and pattern index consistent. A generator is deferred until a drift incident justifies it. |
| [[visible-maturity]] | Adopt | [[index]] carries a reconciled stamp, the evidence boundary, and a ledger of candidate patterns not yet written. The case study records superseded pins and corrections. |
| [[hermetic-tests-live-opt-in]] | Adopt | The checks use only the Python standard library and never touch the network. |
| [[multi-agent-safe-worktree]] | Adopt | `AGENTS.md` lists the git rules for parallel sessions. |
| [[dependencies-as-reviewed-code]] | Adopt the small part | The repository has no dependencies. The CI workflow pins its one action to a commit SHA and requests read-only permissions. |
| [[change-axis-boundaries]] | Adopt | Patterns change when ideas change, case studies when a source repository changes, templates when the page shape changes. A new source repository adds a folder, not edits to existing ones. |
| [[consumer-oriented-verification]] | Adapt | The consumer is an agent that enters at `AGENTS.md`. The reachability check is the consumer test. |
| [[declared-trust-boundary]] | Adapt | The README's scope boundary states what the library is not: not a security review, not project architecture, not live acceptance evidence. |
| [[staged-reversible-release]] | Reject | The library has no releases. A push publishes it. |
| [[attention-budget-gate]] | Reject | One maintainer and no inbound volume. Revisit if outside contributions start. |
| Extensibility and core runtime patterns | Not applicable | The library has no runtime, plugin surface, or transport. |

## Consequences

- The library demonstrates the patterns it recommends, including the decision to reject some.
- The checks add maintenance. They are small, and their tests prove each rule can fail.
- Revisit this record when the library gains a second case study, outside contributors, or a generator.
