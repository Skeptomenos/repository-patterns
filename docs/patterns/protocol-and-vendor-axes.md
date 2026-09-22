---
name: protocol-and-vendor-axes
description: Many vendors speak a few protocols.
category: core-runtime-design
---

# Protocol and vendor axes

## Intent

Model the wire protocol and the vendor endpoint as two independent axes. Then a new vendor that speaks a known protocol costs configuration, not code.

## Use when

- many vendors speak a few shared protocols;
- vendors differ in authentication, catalog, base URL, and headers more than in wire format;
- one vendor offers several protocols for different products or models.

## Small shape

```text
protocol (wire codec):  anthropic-messages | openai-completions | openai-responses | ...
vendor (endpoint):      identity + auth + catalog + base URL + headers
                        -> binds one protocol, or one protocol per model
model record:           {vendor, protocol, id, capabilities}
```

## Pi example

**Observed:** `pi-ai` lists ten wire APIs as `KnownApi` and about forty providers as `KnownProvider` ([`types.ts` L17–29](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/ai/src/types.ts#L17-L29)). The source tree mirrors the split: `src/api/` holds one module per wire API, and `src/providers/` holds one factory per vendor.

**Observed:** `createProvider` binds either one API or one API per model: `single ?? byApi?.[model.api]` ([`models.ts` L799–801](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/ai/src/models.ts#L799-L801)). The README says providers share API implementations. xAI, Groq, Cerebras, OpenRouter, and most others share `openai-completions`, and mixed providers dispatch per model ([`README.md` L238](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/ai/README.md#L238)).

**Observed:** Cross-cutting policy, such as auth merging and header order, sits in the `Models` collection, not in each adapter.

**Observed (residue):** Protocol quirks return as compatibility flags. When a custom endpoint sets no flags, `detectCompat()` falls back to inspecting its base URL.

**Inferred:** The idea transfers to payment networks and acquirers, SQL dialects and database hosts, and messaging protocols and brokers.

**Recommended:** Name both axes in your types before you write the second adapter.

## Benefits

- Adding a compatible vendor is mostly data.
- Protocol fixes reach every vendor that uses the protocol.
- Tests can target a protocol once and a vendor's quirks separately.

## Trade-offs

- Compatibility flags accumulate and are hard to test in combination.
- A protocol can drift per vendor until the shared codec is mostly exceptions.
- Two axes are more to explain than one "provider" concept.

## Poor fit signals

- Each vendor speaks its own protocol.
- There is one vendor.

## Adoption questions

- Which parts of an integration are wire format, and which are vendor identity?
- How many vendors share each protocol today?
- Where do vendor quirks live, and how are they tested?

## Related patterns

- [Contract and adapter](contract-and-adapter.md)
- [Capabilities as data](capabilities-as-data.md)
- [Derived artifacts with a guarded source](derived-artifacts.md)
