#!/usr/bin/env python3
"""Fail the build when two published pages share a browser title.

Every library ships the same five page names, so without a front matter title
twelve pages render as "Getting started" and are indistinguishable in a search
result, in a shared link preview, and in the site's own search. Page metadata is
applied by `scripts/collect_docs.py`; this script checks the built HTML, which
is what readers and crawlers actually receive.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.DOTALL)


def page_titles(site_root: Path) -> dict[str, list[str]]:
    titles: dict[str, list[str]] = defaultdict(list)
    for path in sorted(site_root.rglob("*.html")):
        if path.name == "404.html":
            continue
        match = TITLE_RE.search(path.read_text(encoding="utf-8", errors="replace"))
        if match is None:
            raise RuntimeError(f"page has no title element: {path.relative_to(site_root)}")
        titles[match.group(1).strip()].append(path.relative_to(site_root).as_posix())
    return titles


def check_site(site_root: Path) -> list[str]:
    if not site_root.is_dir():
        raise RuntimeError(f"site directory not found: {site_root}. Run mkdocs build first.")

    problems = []
    for title, pages in sorted(page_titles(site_root).items()):
        if len(pages) > 1:
            problems.append(f'{len(pages)} pages share the title "{title}": ' + ", ".join(pages))
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Check built pages for duplicate titles.")
    parser.add_argument(
        "--site-root",
        default="site",
        help="Directory holding the built site. Default: site.",
    )
    args = parser.parse_args()

    site_root = Path(args.site_root)
    if not site_root.is_absolute():
        site_root = REPO_ROOT / site_root

    try:
        problems = check_site(site_root)
    except Exception as exc:
        print(f"check_page_titles.py: {exc}", file=sys.stderr)
        return 1

    if problems:
        for problem in problems:
            print(f"check_page_titles.py: {problem}", file=sys.stderr)
        return 1

    print("check_page_titles.py: every published page has a unique title")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
