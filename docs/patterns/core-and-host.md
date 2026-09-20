# Core and host

## Intent

Keep reusable domain or runtime behavior separate from the product host that supplies UI, configuration, tools, persistence, and policy.

## Use when

- the same engine needs several interfaces;
- a CLI, server, library, and test harness share behavior;
- product-specific features are accumulating in a reusable package;
- the host needs to compose optional capabilities.

## Small shape

```text
host: CLI / UI / RPC / configuration / product policy
  -> core: state / semantics / events / lifecycle
      -> adapters: providers / storage / tools
```

## Pi example

**Observed:** `pi-agent-core` owns agent state, tool execution, and event streaming. `pi-coding-agent` owns CLI modes, sessions, resource loading, UI, and extensions. The same core events can feed interactive, print, JSON, or RPC modes. See [`pi-agent-core`](https://github.com/earendil-works/pi/blob/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/packages/agent/README.md) and [`coding-agent extensions`](https://github.com/earendil-works/pi/blob/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/packages/coding-agent/docs/extensions.md).

**Recommended:** Keep the core unaware of product presentation. Let the host decide how to display, configure, authorize, and package the core.

## Benefits

- More than one consumer can share the same behavior.
- Tests can exercise semantics without starting the full product.
- Product experiments do not necessarily enlarge the core.

## Trade-offs

- The host/core boundary must be designed deliberately.
- Some behavior will need explicit hooks or context.
- A thin host can become an overly complex composition layer.

## Poor fit signals

- The application has one interface and no reuse horizon.
- The proposed core is only a wrapper around the current UI.
- The boundary requires constant back-and-forth calls that obscure ownership.

## Adoption questions

- Which behavior would still matter if the current UI disappeared?
- Which state belongs to the engine and which belongs to the product?
- Can a second presentation consume the core without branching its semantics?
