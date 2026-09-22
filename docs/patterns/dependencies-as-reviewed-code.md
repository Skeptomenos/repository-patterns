---
name: dependencies-as-reviewed-code
description: Dependency changes reach users without review.
category: verification-and-release
---

# Dependencies as reviewed code

## Intent

Treat every dependency change as a code change. Pin versions, delay new releases, block install scripts, gate lockfile commits, and ship consumers a derived lock.

## Use when

- the project publishes packages or binaries to users;
- the dependency tree is large, and transitive changes arrive silently;
- install-time scripts would run on user or CI machines.

## Small shape

```text
direct deps  : exact pins, checked mechanically
resolution   : minimum release age for new versions
install      : --ignore-scripts everywhere
lockfile     : commit gate with an explicit override
consumers    : derived lock + lifecycle-script allowlist, checked both ways
schedule     : audit + registry signature check
CI           : actions pinned to commit SHAs; publishing through OIDC with provenance
```

## Pi example

**Observed:** Pi's root README has a "Supply-chain hardening" section ([`README.md`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/README.md)). `.npmrc` sets `save-exact=true` and `min-release-age=2`. `check-pinned-deps.mjs` fails on floating external versions. The pre-commit hook runs `check-lockfile-commit.mjs`, which blocks lockfile commits unless `PI_ALLOW_LOCKFILE_CHANGE=1` is set.

**Observed:** The published CLI ships a shrinkwrap generated from the root lockfile. A new dependency with lifecycle scripts fails the check until someone adds an allowlist entry with a reason. CI installs with `npm ci --ignore-scripts`, and a daily workflow runs `npm audit` and `npm audit signatures`. Workflows pin actions to commit SHAs. `publish.mjs` publishes with `--provenance --ignore-scripts` ([L108](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/scripts/publish.mjs#L108)).

**Observed:** `AGENTS.md` asks agents to read the release notes of `undici` before updating it, and never to add a lifecycle-script dependency silently.

**Inferred:** The lockfile hook slows people down more than it controls them. The release procedure sets the override routinely. `peerDependencies` are not pin-checked. The user-facing `pi install` command did not appear to pass `--ignore-scripts` to npm, although the repository's own installs do.

**Recommended:** Pin direct dependencies and ignore install scripts first. Add the consumer lock when you publish something users install.

## Benefits

- A compromised or broken release does not reach users on the same day.
- Install scripts cannot run without review.
- Users get the dependency tree that was tested.

## Trade-offs

- Updates are slower, including security fixes delayed by the age gate.
- Allowlists and generators need maintenance.
- An override variable that is used routinely stops being a control.

## Poor fit signals

- The project is an application that is never distributed.
- The dependency tree is tiny and vendored.

## Adoption questions

- Which dependency changes reached users without review last year?
- Which installs run lifecycle scripts today?
- What exact dependency tree does a user receive?

## Related patterns

- [[derived-artifacts|Derived artifacts with a guarded source]]
- [[consumer-oriented-verification|Consumer-oriented verification]]
- [[staged-reversible-release|Staged, reversible release]]
- [[declared-trust-boundary|Declared trust boundary]]
