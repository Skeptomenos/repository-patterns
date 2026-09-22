---
name: extensions-before-core
description: Every feature wants another core flag or special case.
category: extensibility-and-plugins
---

# Extensions before core

## Intent

Preserve a small stable core by placing optional, product-specific, or experimental behavior behind extension points.

## Use when

- users need different workflows or tools;
- features vary by deployment or team;
- experimentation is expected;
- the core is becoming a collection of flags.

## Small shape

```text
stable core + narrow extension API + independently testable extensions
```

An extension boundary is useful only if its lifecycle, capabilities, errors, and versioning are understandable.

## Pi example

**Observed:** Pi's contributor guidance says the core should remain minimal and that features should be extensions where possible. The coding agent exposes extensions for tools, commands, UI, shortcuts, providers, and events. See [`CONTRIBUTING.md`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/CONTRIBUTING.md) and [`extensions.md`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/docs/extensions.md).

**Observed (history):** Pi 0.35.0 merged hooks and custom tools into one extension system ([`CHANGELOG.md`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/CHANGELOG.md#L4263-L4265)). At v0.87.1, one extension API covers tools, commands, shortcuts, flags, renderers, providers, events, and an inter-extension bus.

**Observed:** `CONTRIBUTING.md` also limits the seams themselves: hook points "should be well considered and discussed to avoid adding unmaintainable bloat and complex interactions".

**Inferred:** Each seam is core surface with a budget. Pi makes the principle workable with a set of supporting patterns: a [[customization-ladder|customization ladder]], [[two-phase-extension-registration|two-phase registration]], [[fault-isolated-event-dispatch|fault-isolated dispatch]], [[layered-resource-discovery|layered discovery]], and [[built-ins-through-public-seams|built-ins that ship through the same seams]].

**Recommended:** Ask whether the feature changes the core invariant or only adds a capability. Keep it outside the core when the latter is true. Discuss a new seam as carefully as a new core feature.

## Benefits

- Reduces core coupling.
- Lets users customize without maintaining forks.
- Makes optional features easier to remove or replace.

## Trade-offs

- Extension APIs become compatibility surfaces.
- Poor lifecycle isolation can create surprising interactions.
- Extensions can become an ungoverned second core.

## Poor fit signals

- The feature changes a core invariant.
- The extension API would expose internal implementation details.
- There is only one consumer and no plausible variation.

## Adoption questions

- What is the smallest stable hook?
- What happens when an extension fails or is reloaded?
- Which permissions and capabilities does the extension receive?

## Related patterns

- [[customization-ladder|Customization ladder]]
- [[two-phase-extension-registration|Two-phase extension registration]]
- [[built-ins-through-public-seams|Built-ins through public seams]]
- [[core-and-host|Core and host]]
