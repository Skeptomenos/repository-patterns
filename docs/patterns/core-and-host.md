---
name: core-and-host
description: Reusable runtime logic is tangled with CLI or UI behavior.
category: structure-and-boundaries
---

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

**Observed:** `pi-agent-core` owns agent state, tool execution, and event streaming. `pi-coding-agent` owns CLI modes, sessions, resource loading, UI, and extensions. The same core events can feed interactive, print, JSON, or RPC modes. See [`pi-agent-core`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/agent/README.md) and [`coding-agent extensions`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/docs/extensions.md).

**Observed (v0.87.1):** The split repeats inside `pi-coding-agent`. `AgentSession` acts as the core, and each mode acts as a host. Interactive, print, JSON, RPC, and SDK modes drive the same session. Each injects its own ports when it binds extensions: a UI context, command actions, a shutdown handler, and an error sink. The core returns diagnostics, and the host decides how to show them. See [Host-owned UI port](host-owned-ui-port.md).

**Observed (v0.87.1):** Policy defaults differ by host. The CLI resolves project trust before it loads project resources. The SDK's `SettingsManager.create` defaults `projectTrusted` to `true`. See [Trust-gated loading](trust-gated-loading.md).

**Recommended:** Keep the core unaware of product presentation. Let the host decide how to display, configure, authorize, and package the core. Write down each host's policy defaults next to its entry point.

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
- Which policy defaults does each host set, and where are they written down?

## Related patterns

- [Host-owned UI port](host-owned-ui-port.md)
- [Extensions before core](extensions-before-core.md)
- [Trust-gated loading](trust-gated-loading.md)
- [Canonical record, projected per target](canonical-record-projected-per-target.md)
