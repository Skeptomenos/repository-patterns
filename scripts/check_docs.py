#!/usr/bin/env python3
"""Documentation checks for Repository Patterns.

Each rule prevents a failure that breaks discovery for a reader or an agent:
unique file names, resolvable relative links and heading anchors, no wiki
links (GitHub does not render them), reachability from AGENTS.md, the shape of
every pattern page, catalog coverage, and one evidence pin per external
repository. Standard library only; no network.
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

LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
WIKI_LINK = re.compile(r"\[\[[^\]]+\]\]")
EXTERNAL = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)
EXTERNAL_REF = re.compile(r"https://github\.com/([\w.-]+/[\w.-]+)/(?:blob|tree)/([0-9a-f]{7,40})/")
HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$")
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


def anchors(text):
    """GitHub heading anchors: lower case, punctuation removed, spaces to hyphens, duplicates numbered."""
    seen = defaultdict(int)
    result = set()
    fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        match = None if fence else HEADING.match(line)
        if match:
            slug = re.sub(r"[^\w\- ]", "", match.group(1).lower()).replace(" ", "-")
            result.add(slug if seen[slug] == 0 else f"{slug}-{seen[slug]}")
            seen[slug] += 1
    return result


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


def document_links(rel, line):
    """Yield (target document or None, anchor) for each relative link on a line."""
    for match in LINK.finditer(line):
        target = match.group(1)
        if EXTERNAL.match(target):
            continue
        path, _, anchor = target.partition("#")
        if not path:
            yield rel, anchor
            continue
        yield os.path.normpath(os.path.join(os.path.dirname(rel), path)), anchor


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
        by_name[os.path.basename(rel)].append(rel)
    for name, paths in sorted(by_name.items()):
        if len(paths) > 1:
            errors.append(f"duplicate basename '{name}': {', '.join(paths)} (a search by name must find one file)")

    graph = defaultdict(set)
    anchor_cache = {}
    for rel in files:
        for number, line in prose_lines(texts[rel]):
            if WIKI_LINK.search(line):
                errors.append(f"{rel}:{number}: wiki link; use a relative Markdown link, because GitHub does not render wiki links")
            for dest, anchor in document_links(rel, line):
                if dest in texts:
                    if dest != rel:
                        graph[rel].add(dest)
                    if anchor and anchor not in anchor_cache.setdefault(dest, anchors(texts[dest])):
                        errors.append(f"{rel}:{number}: unresolved heading anchor {dest}#{anchor}")
                elif not os.path.exists(os.path.join(root, dest)):
                    errors.append(f"{rel}:{number}: unresolved link {dest}")

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
                errors.append(f"{rel}: unreachable from {ROOT_DOCUMENT} by relative links")

    patterns = sorted(rel for rel in files if os.path.dirname(rel) == PATTERN_DIR and rel != PATTERN_INDEX)
    catalog_category = {}
    if CATALOG in texts:
        category = None
        for _, line in prose_lines(texts[CATALOG]):
            if line.startswith("## "):
                category = CATEGORIES.get(line[3:].strip())
            cells = line.split("|")
            if line.startswith("|") and category and len(cells) > 2:
                for dest, _ in document_links(CATALOG, cells[2]):
                    catalog_category[dest] = category
    index_links = set()
    if PATTERN_INDEX in texts:
        index_links = {dest for _, line in prose_lines(texts[PATTERN_INDEX]) for dest, _ in document_links(PATTERN_INDEX, line)}

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
        if not any(dest.endswith(".md") for line in related.splitlines() for dest, _ in document_links(rel, line)):
            errors.append(f"{rel}: Related patterns has no link to another document")
        if rel not in catalog_category:
            errors.append(f"{rel}: not listed in the pattern column of {CATALOG}")
        elif fields.get("category") and catalog_category[rel] != fields.get("category"):
            errors.append(f"{rel}: category '{fields.get('category')}' differs from its catalog group '{catalog_category[rel]}'")
        if rel not in index_links:
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
