---
name: built-ins-through-public-seams
description: Built-in features cannot be replaced without a fork.
category: extensibility-and-plugins
---

# Built-ins through public seams

## Intent

Ship built-in features through the same types and registries that plugins use. Then a plugin can replace or wrap a built-in by name.

## Use when

- users want to change a built-in feature without forking;
- the extension API risks becoming weaker than the internal API;
- built-in I/O, such as file or shell access, should be reroutable.

## Small shape

```text
built-in tool = same definition type + same wrapper + same registry as a plugin tool
plugin registers the same name -> the built-in is replaced
tool I/O behind an operations interface -> reroute it (for example over SSH) without a rewrite
optional built-in feature -> ships as a hidden inline extension
```

## Pi example

**Observed:** Built-in tools and extension tools pass through the same wrapper and registry. An extension tool with a built-in name overrides the built-in ([`agent-session.ts`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/src/core/agent-session.ts)). When an override supplies no renderer, the built-in renderer is used.

**Observed:** Tools expose operations interfaces, for example `ReadOperations` ([`read.ts` L35](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/src/core/tools/read.ts#L35)). The [SSH example](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/examples/extensions/ssh.ts) reroutes file and shell I/O through them.

**Observed:** The llama.cpp provider and its `/llama` command ship as a hidden inline extension ([`extensions/index.ts` L4](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/src/extensions/index.ts#L4)).

**Observed (limit):** Built-in slash commands are a static list. An extension command with a built-in name is renamed or dropped from autocomplete.

**Inferred:** Pi dogfoods its tool and provider seams. The session record, the agent loop, trust, and the UI shell stay in the core.

**Recommended:** When you add a built-in, ask whether a plugin could have written it with the public API. If not, the API is missing a seam.

## Benefits

- The public API is exercised by real features every day.
- Users can replace a built-in without a fork.
- Reroutable I/O enables remote and sandboxed execution by plugins.

## Trade-offs

- Built-ins become compatibility surfaces, so their names and shapes are harder to change.
- Overriding by name can surprise users when two plugins claim one name.
- Some core features cannot use the public seam, and the exceptions need a list.

## Poor fit signals

- Built-ins need privileged internals that plugins must never see.
- There is no plugin API, and none is planned.

## Adoption questions

- Which built-ins could be expressed with the public API today?
- Which built-in I/O should be reroutable?
- Which core features must stay out of reach, and why?

## Related patterns

- [[extensions-before-core|Extensions before core]]
- [[contract-and-adapter|Contract and adapter]]
- [[customization-ladder|Customization ladder]]
