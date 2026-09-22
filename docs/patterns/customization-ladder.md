---
name: customization-ladder
description: Users reach for code where instructions would do.
category: extensibility-and-plugins
---

# Customization ladder

## Intent

Offer customization mechanisms in order of power. Tell users to start with the least powerful one that meets the need.

## Use when

- a product has several customization mechanisms, from plain text to executable code;
- users reach for code where configuration or instructions would do;
- each mechanism has a different trust and maintenance cost.

## Small shape

```text
need                                   -> start with
persistent instructions for a folder   -> context file
a reusable prompt                      -> prompt template
task instructions plus files           -> skill
executable tools, commands, handlers   -> extension
a custom UI component                  -> UI component
an unsupported backend                 -> custom provider
several resources together             -> package
```

## Pi example

**Observed:** Pi's quickstart says "Start with the least powerful mechanism that meets your need" and gives the table above ([`quickstart.md` L94–106](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/docs/quickstart.md#L94-L106)). The custom provider guide has a matching table for choosing the smallest integration ([`custom-provider.md`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/docs/custom-provider.md)).

**Observed:** Pi's [`CONTRIBUTING.md`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/CONTRIBUTING.md) says the core is minimal, features that do not belong in the core should be extensions, and hook points "should be well considered and discussed".

**Inferred:** The ladder is the user-facing twin of "extensions before core". Each rung costs more trust and more maintenance than the one below it.

**Recommended:** Publish the ladder as one table on the page users read first. Open each mechanism's page with when to use it and when not to.

## Benefits

- Users pick cheaper, safer mechanisms first.
- Fewer executable plugins means less code to trust and maintain.
- Maintainers get fewer requests for core changes.

## Trade-offs

- Each rung is a compatibility surface that must be documented and kept.
- Users can misjudge which rung fits and climb too high.
- A long ladder is itself a learning cost.

## Poor fit signals

- There is one customization mechanism.
- Every customization needs code anyway.

## Adoption questions

- Which customization mechanisms exist today, and how powerful is each?
- Which one do users reach for first, and is it the right one?
- Where does a user see the ladder before they choose?

## Related patterns

- [Extensions before core](extensions-before-core.md)
- [Progressive disclosure of instructions](progressive-disclosure.md)
- [Layered resource discovery](layered-resource-discovery.md)
- [Built-ins through public seams](built-ins-through-public-seams.md)
