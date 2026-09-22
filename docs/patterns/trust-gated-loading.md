---
name: trust-gated-loading
description: Opening a folder could run its code.
category: extensibility-and-plugins
---

# Trust-gated loading

## Intent

Do not run code from a folder until the user trusts that folder. Let the user's own plugins automate the decision.

## Use when

- opening a repository can load executable plugins or configuration from it;
- users open cloned or unfamiliar folders;
- different hosts (CLI, SDK, server) load the same resources.

## Small shape

```text
pass 1: load user and CLI plugins; treat the project as untrusted
        plugins may answer "trust this folder?" (the first decision wins)
        otherwise: saved decision -> configured default -> prompt (no UI -> decline)
pass 2: load project resources; reuse the plugin instances from pass 1
```

## Pi example

**Observed:** The resource loader forces untrusted project settings for its bootstrap pass ([`resource-loader.ts` L380–400](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/src/core/resource-loader.ts#L380-L400)). User and CLI extensions may decide trust, and the first decision wins. Otherwise Pi uses the closest saved decision, then `defaultProjectTrust`, then a prompt. Without a UI, the default is to decline ([`project-trust.ts`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/src/core/project-trust.ts), [`security.md`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/docs/security.md)). Project package storage refuses access while the project is untrusted.

**Observed:** The documentation states the limits. Trust is not a sandbox. Context files such as `AGENTS.md` load regardless of trust.

**Observed:** The CLI resolves trust. The SDK does not. `SettingsManager.create` defaults `projectTrusted` to `true` ([`settings-manager.ts` L379](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/src/core/settings-manager.ts#L379)).

**Inferred:** A program that embeds the SDK gets a different default from a CLI user. Each host needs a stated policy default.

**Recommended:** Make "untrusted" the default in every host, or document the default of each host next to its API.

## Benefits

- Cloning a repository does not silently run its plugins.
- Users can automate trust decisions with their own trusted code.
- Plugins loaded in pass 1 are not initialized twice.

## Trade-offs

- Trust prompts cause fatigue, and users learn to accept them.
- The gate protects code loading only. Instruction files can still steer an agent.
- Two passes complicate the loader.

## Poor fit signals

- Code runs only from locations the operator controls.
- The product already runs every workspace inside an isolated environment.

## Adoption questions

- Which resources can execute code, and which can only influence behaviour?
- What is the default in each host: CLI, SDK, server, CI?
- Where is a trust decision stored, and how is it revoked?

## Related patterns

- [Declared trust boundary](declared-trust-boundary.md)
- [Layered resource discovery](layered-resource-discovery.md)
- [Core and host](core-and-host.md)
