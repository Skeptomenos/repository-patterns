#!/usr/bin/env python3
"""Regression tests for check_docs.py: each rule must pass on the real tree and fail when broken."""

import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_docs  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATTERN = "docs/patterns/change-axis-boundaries.md"


class CheckDocsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="check-docs-")
        self.root = os.path.join(self.tmp, "repo")
        shutil.copytree(REPO, self.root, ignore=shutil.ignore_patterns(".git"))

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def path(self, rel):
        return os.path.join(self.root, rel)

    def read(self, rel):
        with open(self.path(rel), encoding="utf-8") as handle:
            return handle.read()

    def write(self, rel, text):
        os.makedirs(os.path.dirname(self.path(rel)), exist_ok=True)
        with open(self.path(rel), "w", encoding="utf-8") as handle:
            handle.write(text)

    def append(self, rel, text):
        self.write(rel, self.read(rel) + text)

    def assert_fails_with(self, fragment):
        errors, _, _ = check_docs.check(self.root)
        self.assertTrue(any(fragment in error for error in errors), f"expected '{fragment}' in {errors}")

    def test_real_tree_passes(self):
        errors, _, _ = check_docs.check(self.root)
        self.assertEqual(errors, [])

    def test_unresolved_link(self):
        self.append("docs/catalog.md", "\nSee [missing](no-such-page.md).\n")
        self.assert_fails_with("unresolved link docs/no-such-page.md")

    def test_unresolved_heading_anchor(self):
        self.append("docs/catalog.md", "\nSee [index](../index.md#no-such-heading).\n")
        self.assert_fails_with("unresolved heading anchor index.md#no-such-heading")

    def test_unresolved_local_anchor(self):
        self.append("docs/catalog.md", "\nSee [below](#no-such-heading).\n")
        self.assert_fails_with("unresolved heading anchor docs/catalog.md#no-such-heading")

    def test_link_in_code_is_ignored(self):
        self.append("docs/catalog.md", "\nWrite `[x](no-such-page.md)` or `[[name]]` in prose.\n")
        errors, _, _ = check_docs.check(self.root)
        self.assertEqual(errors, [])

    def test_wiki_link_rejected(self):
        self.append("docs/catalog.md", "\nSee [[index]].\n")
        self.assert_fails_with("wiki link; use a relative Markdown link")

    def test_orphaned_page(self):
        self.write("docs/orphan-page.md", "# Orphan\n\nLinks to [the index](../index.md) but nothing links here.\n")
        self.assert_fails_with("docs/orphan-page.md: unreachable from AGENTS.md")

    def test_duplicate_basename(self):
        self.write("docs/examples/catalog.md", "# Another catalog\n")
        self.assert_fails_with("duplicate basename 'catalog.md'")

    def test_missing_pattern_section(self):
        self.write(PATTERN, self.read(PATTERN).replace("## Poor fit signals", "## Misfits"))
        self.assert_fails_with("missing section '## Poor fit signals'")

    def test_frontmatter_name_mismatch(self):
        self.write(PATTERN, self.read(PATTERN).replace("name: change-axis-boundaries", "name: other"))
        self.assert_fails_with("frontmatter name must be 'change-axis-boundaries'")

    def test_category_differs_from_catalog(self):
        text = self.read(PATTERN).replace("category: structure-and-boundaries", "category: core-runtime-design")
        self.write(PATTERN, text)
        self.assert_fails_with("differs from its catalog group")

    def test_pattern_missing_from_catalog(self):
        text = self.read(PATTERN).replace("name: change-axis-boundaries", "name: new-pattern")
        self.write("docs/patterns/new-pattern.md", text)
        self.append("docs/patterns/pattern-index.md", "\n- [New pattern](new-pattern.md)\n")
        self.assert_fails_with("new-pattern.md: not listed in the pattern column")

    def test_second_evidence_pin(self):
        self.append(PATTERN, "\n[x](https://github.com/earendil-works/pi/blob/0000000000000000000000000000000000000000/README.md)\n")
        self.assert_fails_with("cited at more than one ref")


if __name__ == "__main__":
    unittest.main(verbosity=2)
