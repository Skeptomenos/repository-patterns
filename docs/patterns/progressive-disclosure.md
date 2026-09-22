---
name: progressive-disclosure
description: Many instructions compete for a small context window.
category: extensibility-and-plugins
---

# Progressive disclosure of instructions

## Intent

Give an agent a short index of the available instructions. Load each full body only when the task needs it.

## Use when

- there are many skills, procedures, or playbooks;
- the context window is a budget;
- long procedures, such as releasing or interactive testing, are needed rarely.

## Small shape

```text
always loaded : name + one-line description + location   (the index)
on a match    : the agent reads the body with its file tool
forced        : a command inlines the body with its base directory
repository    : short AGENTS.md -> "for releases, load .pi/skills/release.md"
```

## Pi example

**Observed:** Pi implements the [Agent Skills specification](https://agentskills.io/specification) ([`skills.md` L7](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/docs/skills.md#L7)). It formats an XML index "per Agent Skills standard" ([`skills.ts` L349](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/packages/coding-agent/src/core/skills.ts#L349)) and validates name and description lengths. A `/skill:` command expands a body on demand. Project `.agents/skills/` folders are discovered from the working directory up to the repository root.

**Observed:** Pi's own [`AGENTS.md`](https://github.com/earendil-works/pi/blob/f07218c4d4bbc12bef056a7058c3dd49dfe41abe/AGENTS.md) stays short. It delegates releasing and interactive testing to `.pi/skills/release.md` and `.pi/skills/interactive-testing.md`. Maintainer workflows are prompt templates in `.pi/prompts/`: `/is` (issue analysis), `/pr` (review), `/cl` (changelog audit), and `/wr` (wrap-up).

**Observed (limits):** The skills documentation warns that the model may not load a relevant skill. Pi's own repository skills are single Markdown files, while its documentation calls folders with `SKILL.md` the portable form. `.pi/skills/add-llm-provider.md` cites a path that no longer exists.

**Inferred:** The index is a routing table. A skill's description is its trigger, so a vague description hides the skill.

**Recommended:** Keep the always-loaded layer to rules that apply to every task. Move each procedure behind a description that names when to use it.

## Benefits

- The context window stays small while many procedures remain available.
- Procedures can be long and precise without taxing every task.
- One standard format makes skills portable across agent tools.

## Trade-offs

- The agent can miss a skill whose description does not match the task.
- Skills drift like any other document unless something checks them.
- Two layers (index and body) must stay consistent.

## Poor fit signals

- There are only a few short instructions. Put them all in one file.
- A procedure applies to every task. It belongs in the always-loaded layer.

## Adoption questions

- Which instructions apply to every task, and which only to some?
- Does each skill's description name its trigger?
- Which check tells you that a skill cites a path that no longer exists?

## Related patterns

- [[repository-as-operating-system|Repository as operating system]]
- [[customization-ladder|Customization ladder]]
- [[documentation-as-tested-surface|Documentation as a tested surface]]
