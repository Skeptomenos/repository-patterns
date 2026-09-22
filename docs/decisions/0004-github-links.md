# Decision 0004: relative Markdown links that GitHub renders

**Date:** 2026-09-23
**Supersedes:** the link syntax in [`0002-wiki-links-and-discovery.md`](0002-wiki-links-and-discovery.md)

## Context

Decision 0002 introduced wiki links (`[[name]]`). The repository is published on GitHub, and GitHub does not render wiki links in repository files. On github.com every cross-reference appeared as plain text, so human readers lost navigation.

## Decision

- Documents reference each other with relative Markdown links, for example `[Core and host](core-and-host.md)` or `[corrections](../examples/pi/pi-case-study.md#corrections-since-the-first-analysis)`.
- A pattern link shows the pattern's title. Other document links show the repository path in backticks.
- Wiki links are rejected by the check.
- These rules from 0002 stay: `AGENTS.md` is the root of discovery, every document is reachable from it, file names are unique, and pattern pages carry frontmatter.

## Consequences

- Links work on GitHub, in editors, and for agents. An agent resolves a path from the folder of the linking file.
- `scripts/check_docs.py` resolves every relative link and heading anchor, and still rejects unreachable pages.
- **Trade-off:** A relative path depends on the folder layout. Moving a file means updating the links to it. The check lists each broken one.
- **Trade-off:** Unique file names are no longer required for link resolution. They are kept because a search by name then finds exactly one file, and case-study files stay prefixed with their example's name.

## Alternatives considered

- Keep wiki links and accept plain text on GitHub: rejected because GitHub is the main place humans read the library.
- Write both forms side by side: rejected because two link forms per reference would drift.
