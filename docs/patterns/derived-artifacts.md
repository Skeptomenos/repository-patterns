---
name: derived-artifacts
description: Generated files drift or get edited by hand.
category: core-runtime-design
---

# Derived artifacts with a guarded source

## Intent

Generate every derived file from one source with one generator. Mark the file as generated. Add a check that fails when the file and its source disagree.

## Use when

- files are produced from upstream APIs, lockfiles, or schemas;
- contributors or agents are tempted to edit generated output by hand;
- consumers receive derived files, such as a lockfile or a catalog.

## Small shape

```text
source -> generator -> derived file with a "do not edit" header
check mode: regenerate, then compare byte for byte or against a hash manifest
agent rule: edit the generator, never the output
bulk data: uncommitted + hash manifest    small typed shell: committed
fast-changing data: publish out of band, keyed by a minimum client version
```

## Pi example

**Observed (model catalog):**

- `models.generated.ts` starts with "Do not edit manually". `AGENTS.md` tells agents to change `generate-models.ts` instead ([`AGENTS.md`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/AGENTS.md)).
- Bulk provider JSON is ignored by git and validated against a manifest that records a schema version, a structure hash, and per-file SHA-256 hashes (`packages/ai/scripts/model-data.ts`).
- [`diff-model-catalog.mjs`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/scripts/diff-model-catalog.mjs) regenerates the catalog for `HEAD` in a temporary git worktree, so reviewers see the real change.
- [`publish-model-catalog.mjs`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/scripts/publish-model-catalog.mjs#L15-L26) uploads immutable, content-addressed revisions and a `no-store` index keyed by `MINIMUM_PI_VERSION`. It refuses catalogs with fewer than 500 models or without the required providers. Scheduled publishing runs only during Vienna business hours ([workflow](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/.github/workflows/publish-model-catalog.yml)).

**Observed (consumer locks):** The published CLI's `npm-shrinkwrap.json` and its installer lock are generated from the root lockfile. `--check` compares them byte for byte. The lifecycle-script allowlist is checked in both directions: a stale entry fails with "is no longer present; remove it from the allowlist" ([`generate-coding-agent-shrinkwrap.mjs` L275](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/scripts/generate-coding-agent-shrinkwrap.mjs#L275)).

**Observed (docs):** A test compares the generated telemetry schema document with the renderer output.

**Inferred:** Publishing the catalog out of band decouples fast-changing data from code releases. The minimum client version keeps old clients from reading data they cannot interpret.

**Recommended:** Give every generator a `--check` mode first. Add the agent rule to the repository instructions in the same change.

## Benefits

- Generated files never drift silently from their source.
- Reviews see meaningful diffs instead of hand edits.
- Agents know which file to change.

## Trade-offs

- Online generation depends on the network, so builds are not reproducible from git alone. Pi adds `build:offline` for this.
- Generators become critical code that needs tests.
- Helpers and allowlists get duplicated across generators.

## Poor fit signals

- The file is small, stable, and easier to edit than to generate.
- The source is not machine-readable.

## Adoption questions

- Which files in the repository are derived, and from what?
- Does each generator have a check mode that CI runs?
- Which derived data changes faster than the code that reads it?

## Related patterns

- [[capabilities-as-data|Capabilities as data]]
- [[dependencies-as-reviewed-code|Dependencies as reviewed code]]
- [[executable-architecture-checks|Executable architecture checks]]
