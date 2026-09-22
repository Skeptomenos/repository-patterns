---
name: visible-maturity
description: Readers cannot tell shipped behavior from plans.
category: structure-and-boundaries
---

# Visible maturity

## Intent

Make the maturity of every surface visible in paths, exports, and documents. Then readers and agents do not mistake a plan for a product.

## Use when

- experimental and shipped code share one repository;
- design documents describe behaviour that is only partly built;
- agents read documents as contracts and act on them.

## Small shape

```text
code:  experimental/ path + source-only export + excluded from published files + opt-in flag
docs:  status line at the top + "normative" or "proposal" label
       + a gap ledger with stable ids, repeated at each section
       + an ordered handoff with review gates
       + negative-result records that say exactly what was rejected
```

## Pi example

**Observed (code):** `pi-coding-agent` exports `./client` and `./experimental/plugin` with only a `source` condition. Its `files` list excludes `dist/client` and `dist/experimental`, and client, protocol, and server are dev dependencies only ([`package.json`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/package.json)). `check-runtime-deps.mjs` fails when built files import excluded ones. The shipped CLI builds the plain `Agent` ([`sdk.ts`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/src/core/sdk.ts#L366)). The durable `AgentHarness` runs only under `src/experimental/`, behind `PI_EXPERIMENTAL`. `pi-agent-core` exports an older prototype as `./experimental/pico3`.

**Observed (docs):**

- [`chord/PLANNING.md`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/chord/PLANNING.md#L3) opens with a status line. It names what exists and what remains planned, and it says the plan "is not a stable public API contract yet".
- [`harness.md` §0.9](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/agent/docs/harness.md#L141-L160) lists known gaps with stable ids (J1, C1, and others). Each id appears again at its section.
- The durable [handoff](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/durable/docs/pico-v5-handoff.md#L10-L14) says "Packages 1–3 are implemented" and asks the implementer to stop for user review after each package.
- [`chord-delta-findings.md`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/durable/docs/chord-delta-findings.md) opens with "Decision and scope". It says the finding "rejects the measured implementation, not every possible graph representation".

**Observed (drift):** Status labels rot. `harness.md` §0.9 and work package 08 disagree about the current slice. Work packages 00–04 cite a `runtime2/` path that does not exist. `pico-v5.md` says its conformance suite covers JSONL, but `pi-durable` has no JSONL backend.

**Inferred:** Agents follow a status line literally. A wrong status line misleads more than a missing one.

**Recommended:** Put the status on the first line of every plan or specification. Give each known gap a stable id. Check that paths cited in plans exist.

## Benefits

- Readers can tell shipped behaviour from planned design.
- Experimental code can live in the repository without reaching consumers.
- Rejected ideas keep their evidence, so nobody retries them blindly.

## Trade-offs

- Status lines and gap ledgers need upkeep, or they mislead.
- Two resolution modes (source and published) are harder to reason about.
- Handoff documents can become a second project tracker.

## Poor fit signals

- The package is small and stable, and nothing is planned.
- The status already lives in an issue tracker that everyone reads.

## Adoption questions

- Can a reader tell, from line one, whether a document describes current behaviour?
- Which experimental exports would reach a consumer today?
- Which rejected experiment is most likely to be retried, and where is its evidence?

## Related patterns

- [[consumer-oriented-verification|Consumer-oriented verification]]
- [[executable-architecture-checks|Executable architecture checks]]
- [[repository-as-operating-system|Repository as operating system]]
- [[progressive-disclosure|Progressive disclosure of instructions]]
