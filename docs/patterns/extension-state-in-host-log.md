---
name: extension-state-in-host-log
description: Plugin state is lost on restart or ignores branches.
category: extensibility-and-plugins
---

# Extension state in the host log

## Intent

Store plugin state as typed entries in the host's own durable log. Then the state follows restarts, branches, and forks without a separate store.

## Use when

- plugins keep state that must survive a restart;
- the host log branches or forks, and plugin state must follow the active branch;
- a separate plugin database would duplicate the host's persistence.

## Small shape

```text
kind of state                          -> where it lives
follows the branch, owned by a tool    -> tool result details
durable, hidden from the model         -> custom entry {customType, data}
visible to the model                   -> custom message
spans sessions                         -> external store

on start or branch change: rebuild state from the active branch
rendering: renderer keyed by customType
```

## Pi example

**Observed:** Pi's extension documentation gives this decision table ([`extensions.md` L163–176](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/docs/extensions.md#L163-L176)). It tells authors to rebuild branch-sensitive state from the active branch during `session_start`, and not from every file entry, "because abandoned branches represent alternative histories".

**Observed:** The session manager exposes `appendCustomEntry` and `appendCustomMessageEntry` ([`session-manager.ts` L1288 and L1337](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/src/core/session-manager.ts#L1288)). [`session-format.md`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/docs/session-format.md) documents the entry formats. The [todo example](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/examples/extensions/todo.ts) rebuilds its list from the branch.

**Inferred:** The host's log becomes the single source of truth. Forking a session forks the plugin state with it.

**Recommended:** Give plugins a typed append operation and a rebuild event before you give them a database.

## Benefits

- Plugin state survives restarts and follows branches for free.
- Export, sharing, and replay include plugin state.
- There is one persistence mechanism to secure and back up.

## Trade-offs

- Each plugin replays the branch at start. This stays cheap only while entries are small.
- Plugins must version the schema of their own custom data.
- The log grows with plugin data that the model never sees.

## Poor fit signals

- The state is large, queried often, or shared across sessions.
- The host log is not durable or not ordered.

## Adoption questions

- Which plugin state must follow a branch or a fork?
- Which state should the model see, and which must it never see?
- How does a plugin migrate its custom entry format?

## Related patterns

- [Durable effect state](durable-effect-state.md)
- [Single-writer mutation](single-writer-mutation.md)
- [Two-phase extension registration](two-phase-extension-registration.md)
