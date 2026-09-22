---
name: canonical-record-projected-per-target
description: One history must feed several targets with different formats.
category: core-runtime-design
---

# Canonical record, projected per target

## Intent

Store one rich, target-neutral record. Project it into each target's format at the edge, and downgrade what the target cannot accept.

## Use when

- one history or document must be sent to several targets with different formats;
- the application needs record kinds that no target understands;
- switching targets mid-history must not break.

## Small shape

```text
application record (open union: user, assistant, tool, + application kinds)
  -> transformContext   optional: prune or inject
  -> convertToLlm       required: drop or convert application kinds
  -> transformMessages  per target:
       same target?  keep signatures and opaque blocks
       other target? reasoning -> plain text; drop opaque blocks
       normalize call ids; orphaned call -> synthetic "No result provided"
       images -> placeholder for text-only targets
```

## Pi example

**Observed:** `pi-agent-core` declares `CustomAgentMessages` as an empty interface that applications extend by declaration merging ([`types.ts` L354–361](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/agent/src/types.ts#L354-L361)). `convertToLlm` is required, and `transformContext` is optional ([L204–221](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/agent/src/types.ts#L204-L221)).

**Observed:** `pi-ai` projects per target in [`transform-messages.ts`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/ai/src/api/transform-messages.ts#L95-L175). For the same model, it keeps thinking blocks with signatures. For another model, it drops redacted thinking and converts other thinking to plain text. An orphaned tool call gets a synthetic result, "No result provided".

**Observed (drift):** The `pi-ai` README says foreign thinking becomes text "with `<thinking>` tags" ([`README.md` L1349](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/ai/README.md#L1349)). The code emits plain text without tags.

**Inferred:** The application keeps the richest form. Each target gets the best form it can accept, and downgrades happen in one audited place.

**Recommended:** Make the projection a required, typed step. Test it with pairs of source and target, not only with each target alone.

## Benefits

- Applications add record kinds without forking the core.
- Switching targets mid-history works.
- Lossy conversions are explicit and testable.

## Trade-offs

- A downgrade loses information that some targets could have used.
- Fidelity depends on a test matrix of target pairs.
- A wrong projector silently drops records.

## Poor fit signals

- There is one target, and its format is the domain format.
- The history is never replayed into a different target.

## Adoption questions

- Which record kinds exist only for the application?
- What must be dropped or converted for each target?
- Which pairs of targets must hand off a history to each other?

## Related patterns

- [[contract-and-adapter|Contract and adapter]]
- [[protocol-and-vendor-axes|Protocol and vendor axes]]
- [[core-and-host|Core and host]]
