from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from collect_docs import (
    SLMP_PYTHON_API_OPERATION_INDEX,
    insert_front_matter_fields,
    library_footer,
    library_page_metadata,
    public_api_table_symbols,
    resolve_site_url_target,
    rewrite_site_absolute_links,
    validate_operation_index,
    verify_page_descriptions,
)


class SlmpOperationIndexTests(unittest.TestCase):
    def test_current_index_has_no_deleted_queued_client(self) -> None:
        symbols = public_api_table_symbols(SLMP_PYTHON_API_OPERATION_INDEX)

        self.assertNotIn("QueuedAsyncSlmpClient", symbols)
        self.assertIn("open_and_connect", symbols)
        self.assertIn("open_and_connect_sync", symbols)

    def test_synthetic_stale_class_is_rejected(self) -> None:
        index = "| Operation | Public API |\n| --- | --- |\n| Connect | `DeletedClient` |"
        reference = "| Operation | Public API |\n| --- | --- |\n| Connect | `CurrentClient` |"

        with self.assertRaisesRegex(RuntimeError, "DeletedClient"):
            validate_operation_index(index, reference)

    def test_synthetic_stale_method_is_rejected(self) -> None:
        index = "| Operation | Public API |\n| --- | --- |\n| Read | `removed_read` |"
        reference = "| Operation | Public API |\n| --- | --- |\n| Read | `read_devices` |"

        with self.assertRaisesRegex(RuntimeError, "removed_read"):
            validate_operation_index(index, reference)


class SiteAbsoluteLinkRewriteTests(unittest.TestCase):
    def build_docs_tree(self, root: Path) -> Path:
        (root / "slmp/python").mkdir(parents=True)
        (root / "plc-setup/slmp").mkdir(parents=True)
        (root / "index.md").write_text("# Home\n", encoding="utf-8")
        (root / "plc-setup/slmp/index.md").write_text("# SLMP setup\n", encoding="utf-8")
        (root / "plc-setup/slmp/iq-r.md").write_text("# iQ-R\n", encoding="utf-8")
        return root / "slmp/python/GETTING_STARTED.md"

    def test_both_hosts_are_rewritten_to_relative_links(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            page = self.build_docs_tree(root)
            page.write_text(
                "[setup](https://fa-yoshinobu.github.io/plc-comm-docs-site/plc-setup/slmp/)\n"
                "[iq-r](https://plc-comm-docs-site.fa-labo.com/plc-setup/slmp/iq-r/#multi-cpu)\n"
                "[home](https://plc-comm-docs-site.fa-labo.com/)\n",
                encoding="utf-8",
            )

            self.assertEqual(3, rewrite_site_absolute_links(root))

            text = page.read_text(encoding="utf-8")
            self.assertIn("[setup](../../plc-setup/slmp/index.md)", text)
            self.assertIn("[iq-r](../../plc-setup/slmp/iq-r.md#multi-cpu)", text)
            self.assertIn("[home](../../index.md)", text)

    def test_unknown_target_is_left_untouched(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            page = self.build_docs_tree(root)
            original = "[gone](https://plc-comm-docs-site.fa-labo.com/plc-setup/does-not-exist/)\n"
            page.write_text(original, encoding="utf-8")

            self.assertEqual(0, rewrite_site_absolute_links(root))
            self.assertEqual(original, page.read_text(encoding="utf-8"))

    def test_other_hosts_on_the_same_domain_are_not_matched(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            page = self.build_docs_tree(root)
            original = "[FA Labo](https://fa-yoshinobu.github.io/FA_Labo/index.html)\n"
            page.write_text(original, encoding="utf-8")

            self.assertEqual(0, rewrite_site_absolute_links(root))
            self.assertEqual(original, page.read_text(encoding="utf-8"))

    def test_section_index_is_preferred_over_missing_page(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            self.build_docs_tree(root)

            target = resolve_site_url_target(root, "/plc-setup/slmp/")

            self.assertIsNotNone(target)
            self.assertEqual("index.md", target.name)


class PageMetadataTests(unittest.TestCase):
    def test_title_names_protocol_and_language(self) -> None:
        title, description = library_page_metadata("slmp/python", "GETTING_STARTED.md")

        self.assertEqual("SLMP for Python — Getting started", title)
        self.assertIn("Python", description)
        self.assertIn("MELSEC", description)

    def test_every_library_page_pair_is_unique(self) -> None:
        from collect_docs import PAGE_TITLES, SOURCES

        titles = [
            library_page_metadata(source.target_dir, file_name)[0]
            for source in SOURCES
            for file_name in PAGE_TITLES
        ]

        self.assertEqual(len(titles), len(set(titles)))
        self.assertEqual(60, len(titles))

    def test_front_matter_is_added_to_a_bare_document(self) -> None:
        result = insert_front_matter_fields("# Getting started\n", {"title": "A", "description": "B"})

        self.assertEqual('---\ntitle: "A"\ndescription: "B"\n---\n\n# Getting started\n', result)

    def test_existing_fields_are_not_replaced(self) -> None:
        original = '---\ndescription: "Kept"\n---\n\n# Page\n'

        result = insert_front_matter_fields(original, {"title": "New", "description": "Ignored"})

        self.assertIn('description: "Kept"', result)
        self.assertIn('title: "New"', result)
        self.assertNotIn("Ignored", result)

    def test_double_quote_in_a_value_is_rejected(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "double quote"):
            insert_front_matter_fields("# Page\n", {"title": 'a "quoted" title'})

    def test_missing_description_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            (root / "good.md").write_text('---\ndescription: "d"\n---\n\n# Good\n', encoding="utf-8")
            (root / "bad.md").write_text("# Bad\n", encoding="utf-8")

            with self.assertRaisesRegex(RuntimeError, "bad.md"):
                verify_page_descriptions(root)


class GeneratedPageSourceTests(unittest.TestCase):
    def test_every_generated_page_has_a_source_file(self) -> None:
        from collect_docs import GENERATED_PAGES, read_page_source

        for relative in GENERATED_PAGES:
            with self.subTest(relative):
                self.assertTrue(read_page_source(relative).strip())

    def test_missing_source_file_is_reported(self) -> None:
        from collect_docs import read_page_source

        with self.assertRaisesRegex(RuntimeError, "page source is missing"):
            read_page_source("slmp/does-not-exist.md")

    def test_operation_index_partial_is_loaded(self) -> None:
        self.assertIn("Operation Index", SLMP_PYTHON_API_OPERATION_INDEX)


class LibraryFooterTests(unittest.TestCase):
    def test_footer_names_the_repository_and_its_registry(self) -> None:
        footer = library_footer("slmp/rust", "plc-comm-slmp-rust")

        self.assertIn("https://github.com/fa-yoshinobu/plc-comm-slmp-rust", footer)
        self.assertIn("https://crates.io/crates/plc-comm-slmp", footer)
        self.assertIn("/blob/main/CHANGELOG.md", footer)
        self.assertIn("/issues", footer)

    def test_every_collected_library_has_a_registry_link(self) -> None:
        from collect_docs import SOURCES

        for source in SOURCES:
            with self.subTest(source.target_dir):
                self.assertIn("github.com", library_footer(source.target_dir, source.repo_name))

    def test_unknown_library_is_rejected(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "no registry link"):
            library_footer("slmp/fortran", "plc-comm-slmp-fortran")


if __name__ == "__main__":
    unittest.main()
