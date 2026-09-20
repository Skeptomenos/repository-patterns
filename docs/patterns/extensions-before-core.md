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

**Observed:** Pi's contributor guidance says the core should remain minimal and that features should be extensions where possible. The coding agent exposes extensions for tools, commands, UI, shortcuts, providers, and events. See [`CONTRIBUTING.md`](https://github.com/earendil-works/pi/blob/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/CONTRIBUTING.md) and [`extensions.md`](https://github.com/earendil-works/pi/blob/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/packages/coding-agent/docs/extensions.md).

**Recommended:** Ask whether the feature changes the core invariant or only adds a capability. Keep it outside the core when the latter is true.

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
