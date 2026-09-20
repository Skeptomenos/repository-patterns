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

**Observed:** Pi checks dependency pinning, generated shrinkwraps, entry graphs, browser bundles, offline builds, isolated npm/Bun installs, binaries, and dependency signatures. Its test harness isolates home/configuration state. See the [root README](https://github.com/earendil-works/pi/blob/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/README.md), [`test.sh`](https://github.com/earendil-works/pi/blob/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/test.sh), and [CI](https://github.com/earendil-works/pi/blob/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/.github/workflows/ci.yml).

**Recommended:** Add one clean consumer smoke test before building an elaborate release system. Expand only when a real packaging failure justifies it.

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
