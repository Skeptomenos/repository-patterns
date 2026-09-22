# Decision 0003: which patterns this repository applies to itself

**Date:** 2026-09-22

## Context

A library of repository patterns should follow its own advice where the advice fits. It should also say where the advice does not fit, because "recommendations, not rules" ([`docs/decisions/0001-recommendations-not-rules.md`](0001-recommendations-not-rules.md)) applies here too. This record uses the decisions of the [adoption worksheet](../templates/adoption-worksheet.md): adopt, adapt, defer, or reject.

## Decision

| Pattern | Decision | How it applies here |
|---|---|---|
| [Repository as operating system](../patterns/repository-as-operating-system.md) | Adopt | `AGENTS.md` is the entry point for agents. `CONTRIBUTING.md`, `scripts/`, and CI carry the operating model. |
| [Progressive disclosure of instructions](../patterns/progressive-disclosure.md) | Adopt | `AGENTS.md` stays short and routes to [`index.md`](../../index.md), then [`docs/catalog.md`](../catalog.md), then one page. Pattern frontmatter is the always-cheap index. |
| [Executable architecture checks](../patterns/executable-architecture-checks.md) | Adopt | `scripts/check_docs.py` enforces unique names, link resolution, reachability, page structure, frontmatter, catalog coverage, and one evidence pin per source repository. |
| [Documentation as a tested surface](../patterns/documentation-as-tested-surface.md) | Adopt the checks; defer the evals | The link and orphan checks mirror Pi's documentation test. Measuring documentation lift is deferred until agents depend on the library often enough to measure. |
| [Conformance tests](../patterns/conformance-tests.md) | Adapt | Every pattern page must pass the same structure check, so pages stay comparable. |
| [Derived artifacts with a guarded source](../patterns/derived-artifacts.md) | Adapt | Frontmatter descriptions were derived from the catalog once. A check keeps the catalog, frontmatter, and pattern index consistent. A generator is deferred until a drift incident justifies it. |
| [Visible maturity](../patterns/visible-maturity.md) | Adopt | [`index.md`](../../index.md) carries a reconciled stamp, the evidence boundary, and a ledger of candidate patterns not yet written. The case study records superseded pins and corrections. |
| [Hermetic tests, live tests by opt-in](../patterns/hermetic-tests-live-opt-in.md) | Adopt | The checks use only the Python standard library and never touch the network. |
| [Multi-agent-safe working tree](../patterns/multi-agent-safe-worktree.md) | Adopt | `AGENTS.md` lists the git rules for parallel sessions. |
| [Dependencies as reviewed code](../patterns/dependencies-as-reviewed-code.md) | Adopt the small part | The repository has no dependencies. The CI workflow pins its one action to a commit SHA and requests read-only permissions. |
| [Change-axis boundaries](../patterns/change-axis-boundaries.md) | Adopt | Patterns change when ideas change, case studies when a source repository changes, templates when the page shape changes. A new source repository adds a folder, not edits to existing ones. |
| [Consumer-oriented verification](../patterns/consumer-oriented-verification.md) | Adapt | The consumer is an agent that enters at `AGENTS.md`. The reachability check is the consumer test. |
| [Declared trust boundary](../patterns/declared-trust-boundary.md) | Adapt | The README's scope boundary states what the library is not: not a security review, not project architecture, not live acceptance evidence. |
| [Staged, reversible release](../patterns/staged-reversible-release.md) | Reject | The library has no releases. A push publishes it. |
| [Attention-budget contribution gate](../patterns/attention-budget-gate.md) | Reject | One maintainer and no inbound volume. Revisit if outside contributions start. |
| Extensibility and core runtime patterns | Not applicable | The library has no runtime, plugin surface, or transport. |

## Consequences

- The library demonstrates the patterns it recommends, including the decision to reject some.
- The checks add maintenance. They are small, and their tests prove each rule can fail.
- Revisit this record when the library gains a second case study, outside contributors, or a generator.
