#!/usr/bin/env python3
"""Documentation checks for Repository Patterns.

Each rule prevents a failure that breaks discovery for a reader or an agent:
unique file names, resolvable wiki links, reachability from AGENTS.md, the
shape of every pattern page, catalog coverage, and one evidence pin per
external repository. Standard library only; no network.
"""

import argparse
import os
import re
import sys
from collections import defaultdict, deque

REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "index.md",
    "docs/catalog.md",
    "docs/library-architecture.md",
    "docs/using-this-repo.md",
    "docs/patterns/pattern-index.md",
    "docs/examples/pi/pi-case-study.md",
    "docs/templates/pattern-template.md",
    "docs/templates/case-study-template.md",
    "docs/templates/adoption-worksheet.md",
]
ROOT_DOCUMENT = "AGENTS.md"
PATTERN_DIR = "docs/patterns"
PATTERN_INDEX = "docs/patterns/pattern-index.md"
CATALOG = "docs/catalog.md"
INDEX = "index.md"
CATEGORIES = {
    "Structure and boundaries": "structure-and-boundaries",
    "Extensibility and plugins": "extensibility-and-plugins",
    "Core runtime design": "core-runtime-design",
    "Verification and release": "verification-and-release",
    "Repository operations and governance": "repository-operations-and-governance",
}
PATTERN_SECTIONS = [
    r"Intent",
    r"Use when",
    r"Small shape",
    r".+ example",
    r"Benefits",
    r"Trade-offs",
    r"Poor fit signals",
    r"Adoption questions",
    r"Related patterns",
]
CASE_STUDY_TERMS = {"docs/examples/pi/pi-case-study.md": ["Observed", "Recommendation", "Important limit"]}

WIKI_LINK = re.compile(r"\[\[([^\]|#\\]+)(?:#([^\]|\\]+))?(?:\\?\|[^\]]+)?\]\]")
RELATIVE_DOC_LINK = re.compile(r"\]\((?![a-z]+:|#)[^)\s]*\.md(?:#[^)\s]*)?\)")
EXTERNAL_REF = re.compile(r"https://github\.com/([\w.-]+/[\w.-]+)/(?:blob|tree)/([0-9a-f]{7,40})/")
HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*$")
INLINE_CODE = re.compile(r"`[^`]*`")


def markdown_files(root):
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d != ".git")
        for name in sorted(filenames):
            if name.endswith(".md"):
                found.append(os.path.relpath(os.path.join(dirpath, name), root))
    return found


def prose_lines(text):
    """Yield (line number, line) outside fenced code, with inline code removed."""
    fence = False
    for number, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if not fence:
            yield number, INLINE_CODE.sub("", line)


def normalize(heading):
    return " ".join(heading.split()).casefold()


def headings(text):
    return {normalize(m.group(1)) for _, line in prose_lines(text) if (m := HEADING.match(line))}


def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip()
    return fields


def check(root):
    errors = []
    files = markdown_files(root)
    texts = {}
    for rel in files:
        with open(os.path.join(root, rel), encoding="utf-8") as handle:
            texts[rel] = handle.read()

    for rel in REQUIRED_FILES:
        if rel not in texts:
            errors.append(f"missing required file: {rel}")

    by_name = defaultdict(list)
    for rel in files:
        by_name[os.path.splitext(os.path.basename(rel))[0]].append(rel)
    for name, paths in sorted(by_name.items()):
        if len(paths) > 1:
            errors.append(f"duplicate basename '{name}': {', '.join(paths)} (wiki links need unique names)")
    target = {name: paths[0] for name, paths in by_name.items()}

    graph = defaultdict(set)
    heading_cache = {}
    for rel in files:
        for number, line in prose_lines(texts[rel]):
            if RELATIVE_DOC_LINK.search(line):
                errors.append(f"{rel}:{number}: relative Markdown link to a document; use a wiki link")
            for match in WIKI_LINK.finditer(line):
                name, heading = match.group(1).strip(), match.group(2)
                if name not in target:
                    errors.append(f"{rel}:{number}: unresolved wiki link [[{name}]]")
                    continue
                dest = target[name]
                graph[rel].add(dest)
                if heading:
                    known = heading_cache.setdefault(dest, headings(texts[dest]))
                    if normalize(heading) not in known:
                        errors.append(f"{rel}:{number}: unresolved heading [[{name}#{heading}]]")

    if ROOT_DOCUMENT in texts:
        reached = {ROOT_DOCUMENT}
        queue = deque([ROOT_DOCUMENT])
        while queue:
            for dest in graph[queue.popleft()]:
                if dest not in reached:
                    reached.add(dest)
                    queue.append(dest)
        for rel in files:
            if rel not in reached:
                errors.append(f"{rel}: unreachable from {ROOT_DOCUMENT} by wiki links")

    patterns = sorted(
        rel for rel in files if os.path.dirname(rel) == PATTERN_DIR and rel != PATTERN_INDEX
    )
    catalog_category = {}
    if CATALOG in texts:
        category = None
        for _, line in prose_lines(texts[CATALOG]):
            if line.startswith("## "):
                category = CATEGORIES.get(line[3:].strip())
            if line.startswith("|") and category:
                for match in WIKI_LINK.finditer(line.split("|")[2] if line.count("|") > 2 else ""):
                    catalog_category[match.group(1).strip()] = category
    index_links = set()
    if PATTERN_INDEX in texts:
        index_links = {m.group(1).strip() for _, line in prose_lines(texts[PATTERN_INDEX]) for m in WIKI_LINK.finditer(line)}

    for rel in patterns:
        name = os.path.splitext(os.path.basename(rel))[0]
        text = texts[rel]
        fields = frontmatter(text)
        if fields is None:
            errors.append(f"{rel}: missing frontmatter")
            fields = {}
        if fields.get("name") != name:
            errors.append(f"{rel}: frontmatter name must be '{name}'")
        if not fields.get("description"):
            errors.append(f"{rel}: frontmatter description is empty")
        if fields.get("category") not in CATEGORIES.values():
            errors.append(f"{rel}: frontmatter category must be one of {sorted(CATEGORIES.values())}")
        found = [m.group(1) for _, line in prose_lines(text) if (m := re.match(r"^## (.+?)\s*$", line))]
        for section in PATTERN_SECTIONS:
            if not any(re.fullmatch(section, heading) for heading in found):
                errors.append(f"{rel}: missing section '## {section}'")
        if "**Observed" not in text:
            errors.append(f"{rel}: no Observed evidence label")
        related = text.split("## Related patterns", 1)[-1] if "## Related patterns" in text else ""
        if not WIKI_LINK.search(related):
            errors.append(f"{rel}: Related patterns has no wiki link")
        if name not in catalog_category:
            errors.append(f"{rel}: not listed in the pattern column of {CATALOG}")
        elif fields.get("category") and catalog_category[name] != fields.get("category"):
            errors.append(f"{rel}: category '{fields.get('category')}' differs from its catalog group '{catalog_category[name]}'")
        if name not in index_links:
            errors.append(f"{rel}: not listed in {PATTERN_INDEX}")

    refs = defaultdict(set)
    for rel in files:
        for match in EXTERNAL_REF.finditer(texts[rel]):
            refs[match.group(1)].add(match.group(2))
    for repo, shas in sorted(refs.items()):
        if len(shas) > 1:
            errors.append(f"external repository {repo} is cited at more than one ref: {', '.join(sorted(shas))}")
        for sha in shas:
            if INDEX in texts and sha not in texts[INDEX]:
                errors.append(f"external repository {repo} ref {sha} is not recorded in {INDEX}")

    for rel, terms in CASE_STUDY_TERMS.items():
        for term in terms:
            if rel in texts and term not in texts[rel]:
                errors.append(f"{rel}: missing '{term}'")

    return errors, len(files), len(patterns)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    args = parser.parse_args()
    errors, file_count, pattern_count = check(args.root)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"documentation checks failed: {len(errors)} problem(s)", file=sys.stderr)
        return 1
    print(f"documentation checks passed: {file_count} documents, {pattern_count} patterns")
    return 0


if __name__ == "__main__":
    sys.exit(main())
