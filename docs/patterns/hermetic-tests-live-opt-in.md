---
name: hermetic-tests-live-opt-in
description: Tests can spend money, leak keys, or depend on the developer's machine.
category: verification-and-release
---

# Hermetic tests, live tests by opt-in

## Intent

Make the default test run hermetic: no keys, no network, an isolated home directory. Let live tests run only when their credentials are present.

## Use when

- tests can reach paid, rate-limited, or flaky external services;
- developer machines carry credentials and configuration that leak into tests;
- agents run tests and must never spend money or touch real accounts by accident.

## Small shape

```text
default runner : empty environment + explicit allowlist
                 HOME, XDG, TMP, git config -> a fresh temporary root; offline flag on
live suites    : skip unless their credential is set
expensive dependency -> deterministic fake implementation
SDK clients    -> injected fetch
measurements   -> separate configs; never CI gates
```

## Pi example

**Observed:** [`test.sh`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/test.sh#L39-L79) builds an allowlisted environment, prints "Running tests without API keys in isolated home", and runs `env -i … npm test`. Its cleanup deletes the temporary root only if the root carries the expected marker and is not a symlink.

**Observed:** Provider suites skip without keys, for example `describe.skipIf(!process.env.GEMINI_API_KEY)` ([`stream.test.ts` L351](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/ai/test/stream.test.ts#L351)). A faux provider replaces the network ([`faux.ts`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/ai/src/providers/faux.ts)). `AGENTS.md` tells agents to use the test harness and the faux provider: "No real provider APIs, keys, or paid tokens". It forbids running the full test runner directly, because end-to-end tests activate when credentials are present.

**Observed:** `pi-agent-core` keeps three test configurations: the default suite, a harness suite with coverage, and a benchmark suite. The benchmark README says its timings are not CI performance gates.

**Observed (contrast):** `pi-test.sh`, which runs Pi from source, removes provider variables with a hand-kept denylist.

**Inferred:** An allowlist stays safe when new providers are added. A denylist silently goes stale.

**Recommended:** Start from an empty environment and add what tests need. Give agents one command that is always safe to run.

## Benefits

- Tests are reproducible on any machine.
- Agents and contributors cannot spend money or leak credentials by running tests.
- Live coverage is still available to whoever holds the keys.

## Trade-offs

- Wire-format regressions can slip through when nobody runs the live suites.
- Live coverage depends on which secrets exist where.
- A fake implementation can drift from the real service.

## Poor fit signals

- The system has no external services.
- The external service offers a free, stable sandbox that is cheaper to use than a fake.

## Adoption questions

- Which environment variables can change test behaviour today?
- Which command is always safe for an agent to run?
- Who runs the live suites, and how often?

## Related patterns

- [Conformance tests](conformance-tests.md)
- [Consumer-oriented verification](consumer-oriented-verification.md)
- [Documentation as a tested surface](documentation-as-tested-surface.md)
