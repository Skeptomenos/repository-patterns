---
name: consumer-oriented-verification
description: Source tests pass but published artifacts fail for consumers.
category: verification-and-release
---

# Consumer-oriented verification

## Intent

Verify the artifacts and environments that users consume, not only the source tree and unit tests.

## Use when

- the repository publishes packages, binaries, plugins, or browser bundles;
- packaging can change dependency resolution;
- generated files or optional dependencies affect consumers;
- local tests do not exercise a clean installation.

## Small shape

```text
source tests -> build -> package -> clean install -> representative consumer smoke
```

The verification should state what it proves and what it cannot prove.

## Pi example

**Observed:** Pi splits the checks by cost. Pull request CI runs build, check, and tests ([`ci.yml` L32–42](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/.github/workflows/ci.yml#L32-L42)). The check step already covers dependency pinning, generated shrinkwraps, entry graphs, and a browser bundle smoke. The heavier consumer checks run on the release path. `npm run release:local` builds, packs, and creates isolated npm and Bun installs outside the repository. The tag workflow builds binaries from the source archive, smoke-tests them on three platforms, and installs the packed CLI before publishing. A scheduled workflow checks dependency signatures. `test.sh` isolates home and configuration state. See the [root README](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/README.md), [`test.sh`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/test.sh), and [CI](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/.github/workflows/ci.yml).

**Observed (v0.87.1):** The consumer smoke installs only what a consumer installs. The top package is the single direct dependency, and the other local tarballs enter only through overrides ([`coding-agent-consumer.mjs` L44–54](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/scripts/coding-agent-consumer.mjs#L44-L54)). Its test records why: installing every tarball directly hid an undeclared runtime import (#9132). The smoke also asserts negatives: dev-only packages are absent and dev-only subpaths are not exported. It imports the public SDK, not only the bundled CLI.

**Recommended:** Add one clean consumer smoke test before building an elaborate release system. Install only the package a consumer installs, and assert what must be absent. Expand only when a real packaging failure justifies it.

## Benefits

- Catches packaging-only failures.
- Protects users from dependency and entry-point surprises.
- Makes release claims more evidence-based.

## Trade-offs

- Consumer tests cost more time and setup.
- Cross-platform environments multiply the matrix.
- A green smoke test is still not proof of every production behavior.

## Poor fit signals

- The project is private and never produces a distributable artifact.
- The proposed check duplicates a reliable lower-level test without a consumer risk.

## Adoption questions

- What exact artifact does a user install or execute?
- Which environment differences have caused failures before?
- Which claims require live acceptance rather than automation?
- Which checks are cheap enough for every change, and which belong on the release path?

## Related patterns

- [[dependencies-as-reviewed-code|Dependencies as reviewed code]]
- [[staged-reversible-release|Staged, reversible release]]
- [[hermetic-tests-live-opt-in|Hermetic tests, live tests by opt-in]]
- [[documentation-as-tested-surface|Documentation as a tested surface]]
