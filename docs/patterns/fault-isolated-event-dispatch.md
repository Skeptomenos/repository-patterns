---
name: fault-isolated-event-dispatch
description: Many plugins handle the same event, and one crash stops the host.
category: extensibility-and-plugins
---

# Fault-isolated event dispatch

## Intent

Let many plugins handle the same event. Declare one combination rule per event kind, and contain each plugin's failure.

## Use when

- several plugins observe or change the same lifecycle events;
- one plugin's crash must not stop the host;
- some events guard dangerous actions and must fail closed.

## Small shape

```text
event kind      -> combination rule
notification    -> call every handler; continue after errors
before-X        -> the first "cancel" stops the chain
transform       -> chain handlers; each sees the previous result
guard           -> a throw blocks the action (fail closed)

every call is wrapped -> errors carry the plugin path and stack
fatal crash -> match stack frames to plugin paths -> name the plugin
```

## Pi example

**Observed:** The extension runner's `emit` continues after handler errors. The first `cancel` result stops "before" events ([`runner.ts` L988–1017](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/src/core/extensions/runner.ts#L988-L1017)). `tool_result` handlers chain, and each sees the previous changes ([L1082](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/src/core/extensions/runner.ts#L1082)). A `message_end` handler must keep the message's role.

**Observed:** A throw inside a `tool_call` handler blocks the tool: "Extension failed, blocking execution" ([`agent-session.ts` L547](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/src/core/agent-session.ts#L547)).

**Observed:** On a fatal crash, Pi matches stack frames to the paths of loaded extensions and writes a crash record ([`crash-log.ts`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/src/core/crash-log.ts#L69)). Commit [`63787ee6`](https://github.com/earendil-works/pi/commit/63787ee6) introduced this ("identify extensions in crash stacks").

**Inferred:** Observation fails open. Guards fail closed. The rule depends on what a failure would cost.

**Recommended:** Write the combination rule and the failure rule for each event kind in one table.

## Benefits

- A broken plugin degrades one feature instead of the host.
- Plugin authors can predict how their results combine with others.
- Crash reports point at the responsible plugin.

## Trade-offs

- Per-event rules are easy to misread when they live only in type declarations.
- Continuation events can create loops between plugins.
- A slow handler delays every handler after it.

## Poor fit signals

- Only one handler per event is allowed.
- Every event has the same rule, so a table adds nothing.

## Adoption questions

- Which events guard actions that must fail closed?
- Which events transform data, and in which order do handlers run?
- How does a user learn which plugin caused a failure?

## Related patterns

- [[two-phase-extension-registration|Two-phase extension registration]]
- [[extensions-before-core|Extensions before core]]
- [[in-band-terminal-streams|In-band terminal streams]]
