# Repository Patterns — agent entry point

Ownership-ID: Personal

This file is the root of discovery. Every document in this repository is reachable from here by following relative Markdown links. A check enforces this.

## What this repository is

- A recommendation library of repository and agent-system design patterns, distilled from real repositories. It is not a policy or compliance rulebook. [`README.md`](README.md) is the human entry point.
- The evidence comes from named source repositories, pinned to one commit each. [`index.md`](index.md) owns the pins and the current coverage.

## How to follow a link

- Internal links are relative Markdown links, such as `[Core and host](core-and-host.md)`. Resolve the path from the folder of the file that contains the link. An anchor such as `#what-not-to-copy-automatically` names a heading in the target.
- Every Markdown file name is unique. If you only know a name, find the file with `find . -name 'name.md' -not -path './.git/*'`.
- Each pattern page starts with YAML frontmatter: `name`, `description` (the need it answers), and `category`. To scan every pattern without reading the bodies, run `grep -H '^description:' docs/patterns/*.md`.
- Links to `github.com` are external evidence, pinned to a commit.

## If you are applying the library to another repository

1. Read [`index.md`](index.md) for the map and the evidence boundary. Then read [`docs/catalog.md`](docs/catalog.md) to route from a need to a pattern.
2. Choose at most two candidate patterns. Read their pages. Follow a page's "Related patterns" only when its fit is unclear.
3. Read the evidence in one case study: [`docs/examples/pi/pi-case-study.md`](docs/examples/pi/pi-case-study.md). For the principles that connect the patterns, read [`docs/examples/pi/pi-essence.md`](docs/examples/pi/pi-essence.md).
4. Compare the pattern with the target repository with [`docs/templates/adoption-worksheet.md`](docs/templates/adoption-worksheet.md). Use the response shape in [`docs/using-this-repo.md`](docs/using-this-repo.md).
5. Stop when you can state the fit, the trade-offs, the smallest adoption step, and the evidence still needed. Do not load the whole library.

Keep these labels distinct: `Observed`, `Inferred`, `Recommended`, `Trade-off`, and `Example`. Prefer the smallest useful adoption. Do not copy a repository's structure just because the example is impressive.

## If you are changing this repository

- Read [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`docs/library-architecture.md`](docs/library-architecture.md) first. Start new pages from [`docs/templates/pattern-template.md`](docs/templates/pattern-template.md) or [`docs/templates/case-study-template.md`](docs/templates/case-study-template.md).
- Every pattern states when it helps, when it does not, what it costs, and where the example came from.
- Reference other documents with relative Markdown links that GitHub renders. Keep every Markdown file name unique.
- Link each new document from an existing page in the same change. The check rejects pages that cannot be reached from this file.
- Run `./scripts/check-docs.sh` after every change. Run `python3 scripts/test_check_docs.py` when you change the checks.
- Record durable decisions in `docs/decisions/`: [`docs/decisions/0001-recommendations-not-rules.md`](docs/decisions/0001-recommendations-not-rules.md), [`docs/decisions/0002-wiki-links-and-discovery.md`](docs/decisions/0002-wiki-links-and-discovery.md), [`docs/decisions/0003-self-adoption.md`](docs/decisions/0003-self-adoption.md), [`docs/decisions/0004-github-links.md`](docs/decisions/0004-github-links.md).

## Git rules

Several sessions may work in this checkout at the same time.

- Commit only the files you changed. Stage explicit paths, and run `git status` before you commit.
- Never run `git reset --hard`, `git checkout .`, `git clean -fd`, `git stash`, `git add -A`, `git add .`, or `git commit --no-verify`. Never force push.
- If a conflict appears in a file you did not change, stop and ask.
