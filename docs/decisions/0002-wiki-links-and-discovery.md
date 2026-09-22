# Decision 0002: wiki links and discovery from AGENTS.md

**Date:** 2026-09-22

**Status:** Superseded in part on 2026-09-23 by [`0004-github-links.md`](0004-github-links.md). Documents now use relative Markdown links, because GitHub does not render wiki links. Discovery from `AGENTS.md`, unique file names, and pattern frontmatter still apply.

## Context

Agents in other sessions use this library while they work on unrelated repositories. They enter at the root `AGENTS.md` and must find the right pattern without loading every page. Relative Markdown links depend on each file's folder, break when files move, and do not say which document they mean when a folder has several `README.md` files.

## Decision

- Documents reference each other with wiki links: `[[name]]`, `[[name#Heading]]`, or `[[name|text]]`.
- `[[name]]` resolves to the only file named `name.md` in the repository. File names are unique, so case-study files carry their example's name (`pi-case-study.md`, `pi-architecture.md`).
- `AGENTS.md` is the root of discovery. Every document must be reachable from it by following wiki links.
- Pattern pages carry frontmatter (`name`, `description`, `category`), so an agent can scan all needs before it reads a body.
- `scripts/check_docs.py` enforces all four rules, and `scripts/test_check_docs.py` proves that each rule can fail.

## Consequences

- An agent can walk the whole library from one entry point, and can find any referenced file by name alone.
- Obsidian and similar tools render the links and the backlinks.
- **Trade-off:** GitHub does not render wiki links in repository files. On github.com they appear as plain text, such as `[[catalog]]`. A reader then finds the file by name.
- **Trade-off:** File names must stay unique across folders, which makes some names longer.
- Renaming a file means updating every wiki link to it. The check lists each broken link.

## Alternatives considered

- Relative Markdown links: rejected because they tie a reference to the folder layout and are ambiguous for agents.
- Wiki links with full paths (`[[docs/patterns/catalog]]`): rejected because they are verbose in prose and tables, and still break when folders move.
