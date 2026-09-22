---
name: opaque-transport
description: Transport code is accumulating business semantics.
category: structure-and-boundaries
---

# Opaque transport

## Intent

Keep wire-level mechanics separate from domain meaning so the protocol can evolve without absorbing application semantics.

## Use when

- a system may support multiple transports;
- remote calls, sessions, or attachments need explicit lifecycle;
- different applications share a transport substrate;
- protocol compatibility matters.

## Small shape

```text
domain contract -> opaque payload -> transport framing/routing -> opaque payload -> domain contract
```

The transport can validate envelopes, identity, correlation, limits, and lifecycle without interpreting every application payload.

## Pi example

**Observed:** `pi-protocol` owns routed envelopes, a version handshake (`PROTOCOL_VERSION = 8`), a CBOR codec with limits, and length-prefixed framing. It checks only that payloads are strict JSON. `pi-client` and `pi-server` expose transport-neutral boundaries instead of embedding agent semantics into the wire format.

**Observed (v0.87.1):** Opacity is layered, not binary. Chord owns the service call and control grammar. Commit [`1a7bc80e`](https://github.com/earendil-works/pi/commit/1a7bc80e) ("move service wire semantics into Chord") took that grammar out of the protocol package. Subscriptions are not a protocol primitive: subscribe and unsubscribe are ordinary requests that carry Chord control calls, and only update delivery has its own envelope. The server parses the service grammar, but not business arguments.

**Observed (v0.87.1):** Every call carries a composite target: server id, session id, and a server-generated attachment id. A server conformance test "rejects a stale attachment route after switching Sessions" ([`conformance.test.ts` L246](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/server/test/conformance.test.ts#L246)). The client "never reconnects or replays requests automatically" ([`client README` L34](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/client/README.md#L34)). In-process consumers use the same service binding over a loopback transport, so local and remote paths share semantics.

**Observed:** The protocol is experimental and has no compatibility guarantees.

See [`pi-protocol`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/protocol/README.md) and [`pi-client`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/client/README.md).

## Benefits

- Domain and transport can evolve independently.
- The same transport can serve multiple applications.
- Ownership of compatibility decisions stays clearer.

## Trade-offs

- Debugging requires inspecting both envelope and domain payload.
- The application must define its own payload contracts.
- Generic transport APIs can feel less convenient than bespoke endpoints.

## Poor fit signals

- The system has one stable local boundary and no transport variation.
- The generic protocol would be less clear than a small domain API.
- Domain validation cannot be separated from routing safely.

## Adoption questions

- Which identity, routing, and lifecycle facts belong to transport?
- Which payload semantics belong to the application?
- How are disconnects, retries, and accepted remote work represented?
- Which identity must each call carry, so that a stale route fails instead of reaching the wrong target?
- Does the local path use the same semantics as the remote path?

## Related patterns

- [Host-owned UI port](host-owned-ui-port.md)
- [Application-neutral substrate](application-neutral-substrate.md)
- [In-band terminal streams](in-band-terminal-streams.md)
