# What makes Pi work

## Purpose

This page distils the design principles behind Pi's patterns. Read it to see why the patterns fit together. Read a pattern page before you adopt one.

**Evidence boundary:** Pi at [v0.87.1](https://github.com/earendil-works/pi/tree/f07218c4d4bbc12bef056a7058c3dd49dfe41abe) (`f07218c`). Each principle is **Inferred** from the **Observed** evidence on the linked pattern pages.

## The principles at a glance

| # | Principle | What goes wrong without it | Patterns |
|---|---|---|---|
| 1 | Cut along sources of change | One vendor or runtime change touches every package | [[change-axis-boundaries]], [[contract-and-adapter]], [[core-and-host]], [[protocol-and-vendor-axes]], [[application-neutral-substrate]] |
| 2 | Keep the core small and make the seams first-class | The core becomes a pile of flags, or plugins become a second core | [[extensions-before-core]], [[customization-ladder]], [[two-phase-extension-registration]], [[fault-isolated-event-dispatch]], [[host-owned-ui-port]], [[built-ins-through-public-seams]], [[extension-state-in-host-log]], [[layered-resource-discovery]] |
| 3 | Put variation in data | Behaviour hides in name checks that nobody can review or override | [[capabilities-as-data]], [[derived-artifacts]] |
| 4 | Make failure a value and recovery explicit | Partial work is lost, and restarts repeat side effects | [[in-band-terminal-streams]], [[canonical-record-projected-per-target]], [[durable-effect-state]], [[single-writer-mutation]], [[explicit-context]] |
| 5 | Enforce architecture with checks, not diagrams | Boundaries erode one reasonable commit at a time | [[executable-architecture-checks]], [[runtime-named-entry-points]], [[conformance-tests]] |
| 6 | Verify what the consumer receives | Source tests pass while installs, docs, or releases fail | [[hermetic-tests-live-opt-in]], [[consumer-oriented-verification]], [[documentation-as-tested-surface]], [[dependencies-as-reviewed-code]], [[staged-reversible-release]] |
| 7 | Say what is true now | Readers and agents treat plans as products and assume protections that do not exist | [[visible-maturity]], [[declared-trust-boundary]], [[trust-gated-loading]] |
| 8 | Design the repository for agents as well as humans | Agents stomp on each other, flood the tracker, or load every instruction every time | [[repository-as-operating-system]], [[progressive-disclosure]], [[multi-agent-safe-worktree]], [[attention-budget-gate]] |

## The principles in more detail

### 1. Cut along sources of change

Pi's folders are a map of what changes independently: vendors, the agent loop, the product, the runtime target, transport, storage, and telemetry. They are not a map of technical layers. Boundaries also move with evidence. Telemetry was extracted once two packages shared it. Products that left the mission moved to their own repositories with a pointer.

### 2. Keep the core small and make the seams first-class

"Pi's core is minimal" is the first rule in its contributor guide. The seams get the same care as features. Plugins declare before they act. Each event has a combination rule. Each host implements the same UI port. Built-ins use the plugin registry. A ladder sends users to the weakest mechanism that meets their need.

### 3. Put variation in data

Model capabilities, catalogs, resource precedence, and consumer locks are records. Generators produce them, and checks compare them with their source. Code reads the records through pure helpers instead of branching on names.

### 4. Make failure a value and recovery explicit

Streams end with a terminal event instead of throwing. Plugin failures are contained according to what they guard: observation fails open, guards fail closed. The durable designs separate intent from outcome, and caller cancellation from durable abort.

### 5. Enforce architecture with checks, not diagrams

Import audits, entry-point budgets, runtime-boundary bundles, and vocabulary tests fail at commit time. Each check has its own test, and the test names the incident it prevents.

### 6. Verify what the consumer receives

The default test run is hermetic. The release path installs the packed artifact the way a consumer would. Examples are type-checked, doc links are tested, and documentation lift is measured. Dependencies are reviewed like code. Releases are staged so the public step comes last.

### 7. Say what is true now

Experimental code is fenced off from the shipped surface. Plans open with a status line and list their gaps by id. The security boundary is declared, not simulated with a partial sandbox.

### 8. Design the repository for agents as well as humans

Pi's product maintains Pi's repository. `.pi/` holds prompts, skills, and extensions, and a CI workflow runs the agent on issues. Instructions are layered and loaded on demand. Git rules assume parallel sessions. A gate protects maintainer attention from agent-generated volume.

## Where Pi itself drifts

**Observed:** Even a disciplined repository drifts where no mechanism guards it.

- Hand-kept lists still name removed packages: `tsconfig.json` maps `packages/agent-old`, and the pre-commit hook matches `packages/web-ui/*`.
- The `pi-ai` README says foreign thinking becomes text "with `<thinking>` tags". The code emits plain text.
- A repository extension subscribes to an event the changelog records as removed. `.pi/` is outside the type check.
- Plans cite paths that do not exist, and two status lines disagree about the current slice.
- `CONTRIBUTING.md` mentions two issue templates. There are three.
- `chord` has no changelog, although `AGENTS.md` asks for one per package.

**Recommended:** Treat each drift as a missing mechanism. Derive lists from manifests. Put instruction and plan files under a check that at least verifies the paths they cite.

## How to use this page

- **For an existing repository:** find the row in the table whose "what goes wrong" column matches your pain today. Read its patterns, then fill in the [[adoption-worksheet|adoption worksheet]].
- **For a new repository:** principles 1, 5, and 7 are cheap early and expensive late. This is a **Recommended** starting point, not an observation about Pi.
- **Do not copy by default:** Pi's package count, its durable runtime, or its contributor gate. See [[pi-case-study#What not to copy automatically|what not to copy]].
