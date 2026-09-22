# Pi — repository layout

## Purpose

This page is an annotated map of how Pi arranges folders, packages, and documents. It ends with the layout ideas that transfer. Evidence is from Pi at [v0.87.1](https://github.com/earendil-works/pi/tree/f07218c4d4bbc12bef056a7058c3dd49dfe41abe) (`f07218c`), and everything here is **Observed** unless marked otherwise.

## Root

| Entry | Responsibility |
|---|---|
| `packages/` | Eleven public packages, plus the private `evals` package and example packages |
| `scripts/` | Checks, generators, release and publish tools, statistics tools |
| `.github/workflows/` | CI, daily audit, tag release, model-catalog publishing, contribution gates, AI issue analysis |
| `.github/APPROVED_CONTRIBUTORS` | Contributor registry that the gate workflows read and update |
| `.husky/pre-commit` | Lockfile gate, then `npm run check` |
| `.pi/` | Pi's own agent assets for this repository: `prompts/`, `skills/`, `extensions/` |
| `AGENTS.md` | Rules for agents and humans: style, commands, dependency security, git safety, changelog |
| `CONTRIBUTING.md` | Human policy: minimal core, contribution gate, quality bar, FAQ |
| `SECURITY.md` | Trust boundary and out-of-scope list |
| `README.md` | Package table, development commands, supply-chain hardening, building from source |
| `package.json` | Workspaces, build order, the `check` chain, `test`, release scripts |
| `tsconfig.base.json`, `tsconfig.json` | Shared compiler options; root no-emit type check against source |
| `biome.json` | Lint and format |
| `.npmrc` | `save-exact=true`, `min-release-age=2` |
| `test.sh` | Hermetic test run without API keys |
| `pi-test.sh` (and `.ps1`, `.bat`) | Run Pi from source |
| `tui-plan.md` | A cross-package implementation handoff |

## Packages and their dependencies

The table lists internal runtime dependencies from each `package.json`.

| Package | Folder | Depends on |
|---|---|---|
| `@earendil-works/chord` | `packages/chord` | none |
| `pi-telemetry` | `packages/telemetry` | none |
| `pi-tui` | `packages/tui` | none |
| `pi-ai` | `packages/ai` | telemetry |
| `pi-protocol` | `packages/protocol` | chord |
| `pi-client` | `packages/client` | chord, protocol |
| `pi-durable` | `packages/durable` | chord, ai |
| `pi-agent-core` | `packages/agent` | chord, ai, telemetry |
| `pi-server` | `packages/server` | chord, agent, protocol |
| `pi-session-backend-sqlite-node` | `packages/session-backends/sqlite-node` | ai, agent |
| `pi-coding-agent` | `packages/coding-agent` | chord, agent, ai, tui (client, protocol, server as dev dependencies only) |
| `pi-evals` (private) | `packages/evals` | ai, coding-agent (dev) |

## Package anatomy

Most packages share one shape:

```text
packages/<name>/
  package.json          exports map with narrow and runtime-named subpaths
  README.md             purpose, API, examples
  CHANGELOG.md          "## [Unreleased]" on top; released sections immutable
  src/                  source; index.ts is the barrel
  test/                 tests; separate configs for harness coverage and benchmarks where needed
  docs/                 design documents, when the package has a design worth specifying
  scripts/              package-local generators
  tsconfig.build.json   build against sibling declarations
```

**Observed exceptions:** `chord` has a `PLANNING.md` and no changelog. `tui` has no exports map. `evals` is private.

## Inside the largest packages

| Package | Folder | Responsibility |
|---|---|---|
| `pi-coding-agent` | `src/core/` | The mode-independent engine: session, runtime, settings, resources, packages, trust |
| | `src/core/extensions/` | Extension types, loader, runner, virtual modules |
| | `src/core/tools/` | Built-in tools as ordinary tool definitions |
| | `src/extensions/` | Built-in extensions that ship through the public API |
| | `src/modes/` | Hosts: `interactive/`, `print-mode.ts`, `json-event.ts`, `rpc/` |
| | `src/experimental/` | Server, worker, and client split behind `PI_EXPERIMENTAL=1` |
| | `src/config.ts` | Asset paths for source checkouts, npm installs, and standalone binaries |
| `pi-ai` | `src/api/` | One module per wire protocol, each with a lazy wrapper |
| | `src/providers/` | One factory per vendor, generated catalogs, and a faux provider for tests |
| | `src/auth/` | Credential contracts, resolution, per-vendor OAuth |
| | `src/types.ts`, `src/models.ts` | All contracts; the model collection and capability helpers |
| `pi-agent-core` | `src/agent-loop.ts`, `src/agent.ts` | The event-producing loop and the stateful agent shell |
| | `src/harness/` | The durable runtime: `session/`, `runtime/`, `execution/`, `compaction/`, `tools/`, `env/` |
| | `src/harness/pico3/` | An experimental prototype, exported as `./experimental/pico3` |

## Naming conventions

- Product packages are named `@earendil-works/pi-*`. The substrate is `@earendil-works/chord`, without the prefix.
- Subpaths name their runtime or role: `/node`, `/unix`, `/testing`, `/experimental/*`, `/storage/sqlite/node`.
- A family folder holds implementations of one contract: `session-backends/<engine>-<runtime>`.
- Generated files carry a header and a recognisable name: `models.generated.ts`, `<provider>.models.ts`.

## Where documents live

| Kind of document | Location |
|---|---|
| Human entry point | Root `README.md` and each package `README.md` |
| Standing agent rules | Root `AGENTS.md` |
| Human policy | `CONTRIBUTING.md`, `SECURITY.md` |
| On-demand procedures | `.pi/skills/*.md` (release, interactive testing, adding a provider) |
| Maintainer macros | `.pi/prompts/*.md` (`/is`, `/pr`, `/cl`, `/wr`, `/sa`, `/deslop`) |
| Product documentation shipped with the package | `packages/coding-agent/docs/`, `packages/coding-agent/examples/` |
| Normative specifications and work packages | `packages/agent/docs/harness.md`, `packages/agent/docs/work-packages/` |
| Living plan beside code | `packages/chord/PLANNING.md` |
| Cross-package handoff | Root `tui-plan.md` |
| Negative results | `packages/durable/docs/chord-delta-findings.md` |
| Larger decisions | External RFCs at rfc.earendil.com |
| Scratch plans | `plans/` and `todo.md`, ignored by git |

## Transferable layout ideas

**Recommended:**

- Mirror the architecture's axes in folder names, as `api/` and `providers/` do.
- Keep the mode-independent engine in `core/` and each host in `modes/`.
- Name runtime-bound code after the runtime.
- Put experimental code under `experimental/` and exclude it from published files.
- Put a design document beside the code it governs. Use the root only for plans that span packages.
- Keep the repository's own agent assets in one dot-folder beside `AGENTS.md`.

## Limits

- **Observed:** Pi has no single convention for plans. Placement follows scope.
- **Observed:** Package lists are kept by hand in several places (type-check paths, test aliases, build paths, the entry-graph map, and build order), and some have drifted.
- **Inferred:** The layout works because checks enforce parts of it. Copying the folders without the checks copies the least valuable part.
