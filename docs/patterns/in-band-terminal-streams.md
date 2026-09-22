---
name: in-band-terminal-streams
description: Callers need both exception and event handling for streams.
category: core-runtime-design
---

# In-band terminal streams

## Intent

After a stream is returned, report every failure as the final event on that stream. Make the final event carry the stop reason and the partial result.

## Use when

- operations stream results over time, such as model output, jobs, or uploads;
- callers otherwise need both exception handling and event handling;
- partial output has value after a failure or an abort.

## Small shape

```text
grammar : start -> update* -> (done | error)
rule    : never throw after the stream is returned
final   : {stopReason: stop | length | toolUse | error | aborted, content: partial, errorMessage?}
setup failure (auth, lazy import) -> a single error event
```

## Pi example

**Observed:** `pi-agent-core` states the contract for its stream function: it "Must not throw or return a rejected promise" for request, model, or runtime failures. Failures "must be encoded in the returned stream" with a final message whose `stopReason` is `error` or `aborted` ([`types.ts` L26–33](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/agent/src/types.ts#L26-L33)).

**Observed:** `pi-ai` returns lazy provider streams synchronously. Setup work, such as authentication and loading the SDK, runs behind the stream, and a setup failure becomes an in-band error ([`api/lazy.ts`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/ai/src/api/lazy.ts#L46-L73)). The README documents compact assistant-message frames with an encoder and a pure reducer, so a stream can be persisted and rebuilt.

**Observed (caveat):** The partial message is a live shared object, not a snapshot.

**Inferred:** Callers write one code path. Partial output survives failures, and a persisted stream can be replayed.

**Recommended:** Write the grammar and the never-throw rule on the stream type itself.

## Benefits

- One consumer code path handles success, failure, and abort.
- Partial results are not lost.
- Streams can be persisted, replayed, and forwarded over a transport.

## Trade-offs

- Every producer must obey the rule, including third-party adapters.
- Consumers that keep a live partial object see it change later.
- The pattern is unusual where exceptions are idiomatic and streams are short.

## Poor fit signals

- Operations are short, and partial results have no value.
- The language or framework already models failures as values everywhere.

## Adoption questions

- Which failures can happen after a stream starts?
- What does a consumer need from the final event to decide what to do next?
- Is the partial result a snapshot or a live object, and is that documented?

## Related patterns

- [[fault-isolated-event-dispatch|Fault-isolated event dispatch]]
- [[durable-effect-state|Durable effect state]]
- [[protocol-and-vendor-axes|Protocol and vendor axes]]
