---
name: two-phase-extension-registration
description: Plugins load before the host is ready, or fail half-way.
category: extensibility-and-plugins
---

# Two-phase extension registration

## Intent

Let a plugin declare its capabilities before the host is ready, and bind them to live services later. Make each load all-or-nothing.

## Use when

- plugins load before the session, registry, or UI exists;
- a plugin that fails half-way must not leave partial registrations;
- plugins reload, or the host replaces its session while plugins stay loaded.

## Small shape

```text
load:   factory(api)
          api.register*()  -> writes only to this plugin's own tables
          api.action*()    -> throws "runtime not initialized"
        success -> commit tables      throw -> discard tables
bind:   host creates the runtime -> stubs are replaced by live actions
reload: old contexts are marked stale -> callbacks receive a fresh context
```

## Pi example

**Observed:** The extension loader builds one API object per extension, with separate `commit` and `discard` functions ([`loader.ts` L228–469](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/src/core/extensions/loader.ts#L228-L469)). Before binding, action methods throw "Action methods cannot be called during extension loading" ([L155](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/src/core/extensions/loader.ts#L155)). The loader awaits the factory, then commits or discards ([L536–555](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/src/core/extensions/loader.ts#L536-L555)).

**Observed:** One API covers events, tools, commands, shortcuts, flags, renderers, providers, session actions, process execution, and an inter-extension bus ([`types.ts`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/src/core/extensions/types.ts)). A flag value is readable only by the extension that registered the flag.

**Observed:** Runtime contexts guard their getters with an "is still active" assertion ([`runner.ts` L688](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/src/core/extensions/runner.ts#L688)). Session replacement emits `session_shutdown`, then passes a fresh context to a `withSession` callback ([`agent-session-runtime.ts`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/src/core/agent-session-runtime.ts#L167-L192)). Only command handlers receive session-replacement operations, because calling them from lifecycle handlers can deadlock ([`extensions.md`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/docs/extensions.md)).

**Observed:** The documentation forbids starting processes inside the factory, because some commands load extensions without a session.

**Inferred:** An all-or-nothing load keeps a plugin failure local. No half-registered provider or bus subscription survives it.

**Recommended:** Separate "declare" from "act" in the API types, not only in the documentation.

## Benefits

- Loading is predictable and testable without a running host.
- One failing plugin does not corrupt the registry.
- Hot reload and session switching become safe operations.

## Trade-offs

- Plugin authors must learn two phases and a stale-context rule.
- Stale-context errors surprise authors who cache a context.
- A plugin cannot use live services during initialization.

## Poor fit signals

- Plugins need real services while they initialize.
- There are few plugins, and they never reload.
- The host is always fully constructed before any plugin loads.

## Adoption questions

- What may a plugin do before the host binds its runtime?
- What happens to its registrations when the factory throws?
- How does a captured context behave after a reload or a session switch?

## Related patterns

- [Extensions before core](extensions-before-core.md)
- [Fault-isolated event dispatch](fault-isolated-event-dispatch.md)
- [Host-owned UI port](host-owned-ui-port.md)
- [Explicit context](explicit-context.md)
