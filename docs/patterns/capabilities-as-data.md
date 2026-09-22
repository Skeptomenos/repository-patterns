---
name: capabilities-as-data
description: Code branches on an implementation's name.
category: core-runtime-design
---

# Capabilities as data

## Intent

Describe what each implementation supports as data in one record. Derive behaviour from the record with pure helpers, instead of branching on the implementation's name.

## Use when

- implementations differ in limits, modalities, cost, or feature levels;
- code contains branches such as "if vendor is X";
- users need to add or override implementations without code changes.

## Small shape

```text
record  : {reasoning, input: [text, image], contextWindow, maxTokens, cost,
           inputLimits, thinkingLevelMap, compat}
null    = explicitly unsupported; absent = default
helpers : supportedLevels(model), clampLevel(model, level), cost(model, usage)
```

## Pi example

**Observed:** `pi-ai`'s `Model` interface is a plain, serializable record of capabilities ([`types.ts` L982](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/ai/src/types.ts#L982)). Pure helpers derive behaviour from it: `calculateCost`, `getSupportedThinkingLevels`, and `clampThinkingLevel` ([`models.ts` L900–935](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/ai/src/models.ts#L900-L935)). In a thinking-level map, `null` marks a level as unsupported.

**Observed:** Recent capability fixes landed as data and defaults. Examples are "default unknown providers to non-strict tools" ([`890f9208`](https://github.com/earendil-works/pi/commit/890f9208), closes #9816) and "add image input limits" ([`f5c94648`](https://github.com/earendil-works/pi/commit/f5c94648), closes #9631).

**Observed (residue):** When a custom OpenAI-compatible endpoint sets no compatibility flags, `detectCompat()` still inspects its base URL.

**Inferred:** Data can be reviewed in a diff, overridden by users, and generated from upstream sources. Code branches cannot.

**Recommended:** Move one branch on an implementation name into a capability field. Test the helper, not every implementation.

## Benefits

- Behaviour differences are visible and reviewable in one place.
- Users can add custom implementations with a record.
- Records can be generated and diffed when upstream changes.

## Trade-offs

- The flag surface grows, and some combinations stay untested.
- Data must stay in sync with the real implementations.
- A capability record can hide an important behavioural difference behind a boolean.

## Poor fit signals

- Implementations differ in behaviour that no field can describe.
- There are two implementations and no sign of more.

## Adoption questions

- Which branches on an implementation name exist today?
- Which differences are limits, and which are behaviours?
- Who updates the records when an upstream implementation changes?

## Related patterns

- [Protocol and vendor axes](protocol-and-vendor-axes.md)
- [Derived artifacts with a guarded source](derived-artifacts.md)
- [Contract and adapter](contract-and-adapter.md)
