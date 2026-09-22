# Repository Patterns — agent entry point

Ownership-ID: Personal

This file is the root of discovery. Every document in this repository is reachable from here by following wiki links. A check enforces this.

## What this repository is

- A recommendation library of repository and agent-system design patterns, distilled from real repositories. It is not a policy or compliance rulebook. [[README]] is the human entry point.
- The evidence comes from named source repositories, pinned to one commit each. [[index]] owns the pins and the current coverage.

## How to resolve a link

- `[[name]]` means the only file named `name.md` in this repository. Find it with `find . -name 'name.md' -not -path './.git/*'`.
- `[[name#Heading]]` means that heading inside the file. `[[name|text]]` displays `text`.
- Each pattern page starts with YAML frontmatter: `name`, `description` (the need it answers), and `category`. To scan every pattern without reading the bodies, run `grep -H '^description:' docs/patterns/*.md`.
- Links to `github.com` are external evidence, pinned to a commit.

## If you are applying the library to another repository

1. Read [[index]] for the map and the evidence boundary. Then read [[catalog]] to route from a need to a pattern.
2. Choose at most two candidate patterns. Read their pages. Follow a page's "Related patterns" only when its fit is unclear.
3. Read the evidence in one case study: [[pi-case-study]]. For the principles that connect the patterns, read [[pi-essence]].
4. Compare the pattern with the target repository with [[adoption-worksheet]]. Use the response shape in [[using-this-repo]].
5. Stop when you can state the fit, the trade-offs, the smallest adoption step, and the evidence still needed. Do not load the whole library.

Keep these labels distinct: `Observed`, `Inferred`, `Recommended`, `Trade-off`, and `Example`. Prefer the smallest useful adoption. Do not copy a repository's structure just because the example is impressive.

## If you are changing this repository

- Read [[CONTRIBUTING]] and [[library-architecture]] first. Start new pages from [[pattern-template]] or [[case-study-template]].
- Every pattern states when it helps, when it does not, what it costs, and where the example came from.
- Reference other documents with wiki links only. Keep every Markdown file name unique.
- Link each new document from an existing page in the same change. The check rejects pages that cannot be reached from this file.
- Run `./scripts/check-docs.sh` after every change. Run `python3 scripts/test_check_docs.py` when you change the checks.
- Record durable decisions in `docs/decisions/`: [[0001-recommendations-not-rules]], [[0002-wiki-links-and-discovery]], [[0003-self-adoption]].

## Git rules

Several sessions may work in this checkout at the same time.

- Commit only the files you changed. Stage explicit paths, and run `git status` before you commit.
- Never run `git reset --hard`, `git checkout .`, `git clean -fd`, `git stash`, `git add -A`, `git add .`, or `git commit --no-verify`. Never force push.
- If a conflict appears in a file you did not change, stop and ask.
