from __future__ import annotations

from datetime import date
import json
import os
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest

from page_dates import MANIFEST_NAME, on_page_markdown, on_pre_build, write_page_dates


class SitemapDateTests(unittest.TestCase):
    def setUp(self):
        cache = Path(__file__).resolve().parents[1] / ".cache"
        cache.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=cache)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source.md"
        self.source.write_text("# Guide\n", encoding="utf-8")
        self.run_git("init", "-q")
        self.commit("2026-01-02T12:00:00+09:00")
        self.docs = self.root / "docs"
        self.docs.mkdir()
        self.page = self.docs / "index.md"
        self.page.write_text("# Guide\n", encoding="utf-8")

    def run_git(self, *args, env=None):
        return subprocess.check_output(
            ["git", "-C", str(self.root), *args], env=env, stderr=subprocess.PIPE
        )

    def commit(self, timestamp):
        self.run_git("add", "source.md")
        env = dict(os.environ, GIT_AUTHOR_DATE=timestamp, GIT_COMMITTER_DATE=timestamp)
        self.run_git("-c", "user.name=Date Test", "-c", "user.email=date-test@example.invalid",
                     "commit", "-qm", "source update", env=env)

    def manifest(self):
        write_page_dates(self.docs, {"index.md": [self.source]})
        return json.loads((self.docs / MANIFEST_NAME).read_text(encoding="utf-8"))["pages"]

    def test_rebuild_and_checkout_mtime_do_not_advance_lastmod(self):
        first = self.manifest()
        os.utime(self.source, (2000000000, 2000000000))
        os.utime(self.page, (2000000000, 2000000000))
        self.assertEqual(first, self.manifest())
        self.assertEqual(first["index.md"]["date"], "2026-01-02")

    def test_new_source_commit_advances_date(self):
        self.source.write_text("# Updated guide\n", encoding="utf-8")
        self.commit("2026-02-03T12:00:00+09:00")
        self.assertEqual(self.manifest()["index.md"]["date"], "2026-02-03")

    def test_explicit_edit_date_stays_fixed_until_newer_commit(self):
        self.page.write_text("---\nlastmod: 2026-01-15\n---\n# Guide\n", encoding="utf-8")
        self.assertEqual(self.manifest()["index.md"]["date"], "2026-01-15")
        self.source.write_text("# Updated guide\n", encoding="utf-8")
        self.commit("2026-02-03T12:00:00+09:00")
        self.assertEqual(self.manifest()["index.md"]["date"], "2026-02-03")

    def test_hook_overrides_build_date_and_rejects_stale_manifest(self):
        self.manifest()
        on_pre_build(SimpleNamespace(docs_dir=str(self.docs)))
        page = SimpleNamespace(file=SimpleNamespace(src_uri="index.md", abs_src_path=str(self.page)),
                               update_date=date.today().isoformat())
        on_page_markdown("# Guide", page, None, None)
        self.assertEqual(page.update_date, "2026-01-02")
        self.page.write_text("# Changed since collection\n", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "stale"):
            on_page_markdown("# Changed since collection", page, None, None)

    def test_new_uncommitted_page_accepts_an_explicit_date(self):
        new = self.docs / "new.md"
        new.write_text("---\nlastmod: 2026-01-15\n---\n# New guide\n", encoding="utf-8")
        self.assertEqual(self.manifest()["new.md"]["date"], "2026-01-15")

    def test_shallow_source_history_is_rejected(self):
        clone = self.root / "shallow"
        subprocess.check_call(["git", "clone", "-q", "--depth", "1", self.root.as_uri(), str(clone)])
        with self.assertRaisesRegex(RuntimeError, "Complete Git history"):
            write_page_dates(self.docs, {"index.md": [clone / "source.md"]})


if __name__ == "__main__":
    unittest.main()
