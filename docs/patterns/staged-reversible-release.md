---
name: staged-reversible-release
description: A failed release leaves users with a half-published version.
category: verification-and-release
---

# Staged, reversible release

## Intent

Release in stages. Each stage verifies the previous one, public visibility comes last, and a re-run is safe.

## Use when

- a release publishes to several places, such as a registry, binaries, and an announcement;
- a partial release would leave users with a broken or inconsistent version;
- releases are re-run after failures.

## Small shape

```text
local: check versions -> rotate changelogs -> tag
CI:    source archive -> binaries built from the archive -> cross-platform smoke
       -> draft release -> publish packages (skip versions already published)
       -> verify on the registry -> advance the "latest" marker (never backwards)
       -> un-draft last
       failure at any stage -> delete the draft
```

## Pi example

**Observed:** All public packages share one version. [`sync-versions.js`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/scripts/sync-versions.js#L4-L32) fails when versions diverge. The release skill defines the policy: patch means fixes and additions, minor means breaking changes, and there are no major releases ([`release.md`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/.pi/skills/release.md)). `release.mjs` renames each `## [Unreleased]` section to the new version and then adds a fresh one.

**Observed:** The tag workflow creates a draft release first. It removes the draft when a later stage fails, and it un-drafts only at the end ([`build-binaries.yml` L26, L248–282, L418–435](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/.github/workflows/build-binaries.yml#L26)). Binaries are built from the extracted source archive, and the README documents that build for users. [`publish.mjs`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/scripts/publish.mjs#L88-L104) skips versions that are already published. The announcement script refuses to move the latest-release marker to an older or equal version ([`publish-release-announcement.mjs` L242–257](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/scripts/publish-release-announcement.mjs#L242-L257)).

**Observed (limits):** The cross-platform smoke runs only `--help` and `--version`. The release skill keeps interactive checks manual.

**Inferred:** Each stage is idempotent, so the pipeline can resume after a failure instead of starting a new version.

**Recommended:** Make "public" the last step and "re-run" a safe operation before you add more targets.

## Benefits

- Users never see a half-published release.
- A failed release can be retried without a new version number.
- Binaries are reproducible from the published source.

## Trade-offs

- The pipeline is long, and a late failure costs time.
- Workflow files repeat lists, such as the asset list in three places.
- Lockstep versions produce empty changelog sections for unchanged packages.

## Poor fit signals

- The project publishes to one place, and a failed publish is harmless.
- Releases are continuous deployments with automatic rollback.

## Adoption questions

- What does a user see if the release fails half-way?
- Which stages are safe to re-run?
- Which marker or pointer must never move backwards?

## Related patterns

- [Consumer-oriented verification](consumer-oriented-verification.md)
- [Dependencies as reviewed code](dependencies-as-reviewed-code.md)
- [Derived artifacts with a guarded source](derived-artifacts.md)
