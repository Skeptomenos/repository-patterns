---
name: declared-trust-boundary
description: Users assume protections the software does not provide.
category: repository-operations-and-governance
---

# Declared trust boundary

## Intent

State in one place what the software trusts and what it does not protect against. Point to external isolation instead of shipping a partial sandbox.

## Use when

- the software runs code or commands with the user's permissions;
- a partial sandbox would create a false sense of safety;
- security reports need a clear scope for triage.

## Small shape

```text
SECURITY.md : inside the boundary  -> the user account, its files, config, repositories, extensions
              out of scope         -> prompt injection, untrusted repositories or extensions,
                                      attacks that need prior local write access
README      : "no built-in permission system" + isolation recipes (micro-VM, container, policy sandbox)
product     : trust prompts are user experience, not a sandbox
```

## Pi example

**Observed:** Pi's root README has a "Permissions & Containerization" section. It says Pi has no built-in permission system and points to three isolation patterns ([`README.md`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/README.md), [`containerization.md`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/docs/containerization.md)).

**Observed:** [`SECURITY.md`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/SECURITY.md#L10-L22) puts the local user account and its writable files inside the same trust boundary as the Pi process. It says files like `AGENTS.md` can prompt-inject the agent "and this cannot be protected against". Its out-of-scope list includes sandboxing behaviour ("the Pi coding agent intentionally does not have a sandbox") and prompt injection ([L50–56](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/SECURITY.md#L50-L56)).

**Inferred:** A partial sandbox would create an endless class of bypass reports and a false sense of safety. A declared boundary makes reports triageable and puts isolation where it can be strong.

**Recommended:** Write the boundary before users ask. Pair every "out of scope" item with a way to get stronger isolation.

## Benefits

- Users know what they must isolate themselves.
- Security reports can be triaged against a written scope.
- Engineering effort goes to real boundaries instead of partial ones.

## Trade-offs

- Users must do the isolation work.
- Some organisations will reject software without a built-in sandbox.
- A declared boundary can be misread as negligence.

## Poor fit signals

- The software is a multi-tenant service.
- The product is sold as safe for untrusted input.

## Adoption questions

- What does the software trust today, stated in one paragraph?
- Which attacks are out of scope, and what isolation covers them?
- Where does a user read this before they install?

## Related patterns

- [[trust-gated-loading|Trust-gated loading]]
- [[attention-budget-gate|Attention-budget contribution gate]]
- [[dependencies-as-reviewed-code|Dependencies as reviewed code]]
