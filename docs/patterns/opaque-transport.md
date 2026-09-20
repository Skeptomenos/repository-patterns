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

**Observed:** `pi-protocol` owns framing, CBOR, routing, correlation, cancellation, and subscriptions. Its payloads remain application-owned. `pi-client` and `pi-server` expose transport-neutral boundaries instead of embedding agent semantics into the wire format.

See [`pi-protocol`](https://github.com/earendil-works/pi/blob/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/packages/protocol/README.md) and [`pi-client`](https://github.com/earendil-works/pi/blob/3390bd93630965a12a0a1a5c36ce890ec22f7e1d/packages/client/README.md).

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
