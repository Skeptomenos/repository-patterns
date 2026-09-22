---
name: host-owned-ui-port
description: The same plugin must run in a UI, over RPC, and headless.
category: extensibility-and-plugins
---

# Host-owned UI port

## Intent

Let plugins ask for user interaction through an abstract port. Each host implements the port fully, degrades it, or makes it a no-op. Plugins never own the UI.

## Use when

- the same plugin must run in an interactive UI, over RPC, and headless;
- several plugins want space in the same UI areas;
- UI code must not leak into the core or into plugins.

## Small shape

```text
plugin -> ctx.ui.select / confirm / input / notify / setStatus(key) / setWidget(key)

interactive host -> full implementation
RPC host         -> dialogs become request/response records with ids and timeouts;
                    terminal-only calls become no-ops
headless host    -> no-op port; ctx.hasUI = false
```

## Pi example

**Observed:** Pi's print mode injects a no-op UI context. `hasUI()` is true only when the context is not that no-op object ([`runner.ts` L320 and L578](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/src/core/extensions/runner.ts#L578-L579)). RPC mode turns dialogs into request and response records. If a dialog carries a `timeout`, the agent side resolves it with a default value when the timeout expires ([`rpc-extension-ui.md`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/docs/rpc-extension-ui.md)).

**Observed:** The same document lists each degradation: `custom()` returns `undefined`, footer and header setters are no-ops, and theme switching reports an error. It tells authors to check `ctx.mode === "tui"` before they use terminal-only features.

**Observed:** Status and widgets take a key, so several plugins share areas that the host owns.

**Inferred:** The port keeps plugins portable across hosts. The degradation table is the contract.

**Recommended:** Publish the degradation table with the port. A plugin author needs it more than the full API list.

## Benefits

- One plugin works in every host.
- The host keeps control of layout, focus, and theming.
- Headless and remote hosts need no plugin changes.

## Trade-offs

- Rich custom components do not cross a process boundary.
- Two capability probes (`hasUI` and `mode`) confuse authors.
- The lowest common denominator limits what plugins can do.

## Poor fit signals

- There is only one host, and it will stay that way.
- Plugins need full control of rendering.

## Adoption questions

- Which interactions must work in every host?
- What does each host do with an interaction it cannot show?
- How do plugins share screen areas without conflicts?

## Related patterns

- [[core-and-host|Core and host]]
- [[two-phase-extension-registration|Two-phase extension registration]]
- [[opaque-transport|Opaque transport]]
