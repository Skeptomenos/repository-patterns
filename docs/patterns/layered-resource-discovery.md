---
name: layered-resource-discovery
description: Users cannot tell which of several same-named resources is active.
category: extensibility-and-plugins
---

# Layered resource discovery

## Intent

Discover resources from several scopes with a documented precedence. Record where each resource came from, and report every name collision.

## Use when

- one kind of resource can come from built-ins, user settings, project settings, installed packages, or command-line flags;
- users ask "why is this version active?";
- packages bundle several resource kinds, and consumers need to narrow what loads.

## Small shape

```text
discover -> tag {source, scope, origin} -> sort by rank -> first name wins
         -> collision diagnostic {name, winner path, loser path}

package layer:
  the package manifest declares its resources
  the consumer's filter can only narrow that list
  package identity = registry name | git host + path without ref | absolute local path
  a project entry replaces a user entry with the same identity
```

## Pi example

**Observed:** The package manager ranks resources: 0 project settings entry, 1 project auto-discovered, 2 user settings entry, 3 user auto-discovered, 4 package resource. The rank sorts resources "so that name-collision resolution ('first wins') produces the correct outcome" ([`package-manager.ts` L176–192](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/src/core/package-manager.ts#L176-L192)). Paths passed with `-e` load first. Inline built-ins load last.

**Observed:** Prompt and theme collisions record `winnerPath` and `loserPath` ([`resource-loader.ts` L974–1025](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/src/core/resource-loader.ts#L974-L1025)). Every resource carries source information (`source-info.ts`).

**Observed:** A Pi package declares resources in a manifest or in conventional folders. Consumer settings filter them with globs and can only narrow the declared set. Project scope wins over user scope for the same package identity ([`package-manager.ts` L926](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/src/core/package-manager.ts#L926)). See [`packages.md`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/docs/packages.md).

**Observed:** Conflict rules differ by kind:

- tools: the first extension wins, and extension tools override built-in tools;
- shortcuts: the last extension wins, and reserved core keys block extensions;
- commands: all are kept, and duplicates are renamed `name:1`, `name:2`.

**Inferred:** Different rules per kind cost learnability. A reusable version should document one rule per kind in one table.

**Recommended:** Record provenance first. You can change the precedence later. You cannot recover provenance that was never recorded.

## Benefits

- Users and agents can explain which resource is active and why.
- Project settings can override personal settings in a predictable way.
- Packages can ship many resources while consumers keep control.

## Trade-offs

- Several scopes make debugging harder without good diagnostics.
- Precedence rules become a compatibility surface.
- Filters and identity rules add configuration concepts.

## Poor fit signals

- Resources come from one location only.
- Names never collide, because one owner controls all of them.

## Adoption questions

- Which scopes exist, and which one should win?
- What does a user see when two resources share a name?
- How is a package identified independently of its version or ref?

## Related patterns

- [[trust-gated-loading|Trust-gated loading]]
- [[customization-ladder|Customization ladder]]
- [[extensions-before-core|Extensions before core]]
