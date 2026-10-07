"""Preserve source modification dates in MkDocs' generated sitemap.

The collector records Git provenance before MkDocs substitutes its build date.
This module is also registered as a MkDocs hook, without adding a dependency.
"""

from __future__ import annotations

from datetime import date
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit


MANIFEST_NAME = ".sitemap-dates.json"
_page_dates: dict = {}


class MissingSourceHistory(RuntimeError):
    pass


def git(directory: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(directory), *args], encoding="utf-8", stderr=subprocess.PIPE
    ).strip()


@lru_cache(maxsize=None)
def repository(directory: Path) -> Path:
    root = Path(git(directory, "rev-parse", "--show-toplevel"))
    if git(root, "rev-parse", "--is-shallow-repository") == "true":
        raise RuntimeError(f"Complete Git history is required for sitemap dates: {root}")
    return root


@lru_cache(maxsize=None)
def source_revision(path: Path) -> dict[str, str]:
    root = repository(path if path.is_dir() else path.parent)
    relative = path.relative_to(root).as_posix()
    revision = git(root, "log", "-1", "--format=%cs%x09%H", "--", relative)
    if not revision:
        raise MissingSourceHistory(f"No committed source history for sitemap date: {path}")
    modified, commit = revision.split("\t")
    date.fromisoformat(modified)
    return {"repository": root.name, "path": relative, "commit": commit, "date": modified}


def page_hash(path: Path) -> str:
    # Normalize checkout line endings so Windows and Linux produce the same hash.
    return hashlib.sha256(path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()


def explicit_date(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    front_matter = text.split("---\n", 2)[1]
    match = re.search(r"(?m)^lastmod:\s*[\"']?(\d{4}-\d{2}-\d{2})[\"']?\s*$", front_matter)
    if not match:
        return None
    date.fromisoformat(match[1])
    return match[1]


def write_page_dates(docs_root: Path, origins: dict[str, list[Path]]) -> None:
    """Write one dated provenance record per published Markdown page."""
    source_revision.cache_clear()
    repository.cache_clear()
    pages = {}
    for page in sorted(docs_root.rglob("*.md")):
        relative = page.relative_to(docs_root).as_posix()
        override = explicit_date(page)
        sources = list(origins.get(relative, [page]))
        # Screenshots and illustrations are part of a page's actual content.
        for source in sources.copy():
            if source.is_file() and source.suffix == ".md":
                for image in re.findall(r"!\[[^\]]*\]\(([^\s)]+)", source.read_text(encoding="utf-8")):
                    url = urlsplit(image)
                    if not url.scheme and not url.netloc:
                        asset = (source.parent / unquote(url.path)).resolve()
                        if asset.is_file():
                            sources.append(asset)
        evidence = []
        for path in dict.fromkeys(sources):
            path = path.resolve()
            try:
                evidence.append(source_revision(path))
            except MissingSourceHistory:
                if not override:
                    raise
                root = repository(path if path.is_dir() else path.parent)
                evidence.append({"repository": root.name, "path": path.relative_to(root).as_posix(),
                                 "date": override, "uncommitted": True})
        dates = [item["date"] for item in evidence]
        if override:
            dates.append(override)
        pages[relative] = {"date": max(dates), "sources": evidence, "sha256": page_hash(page)}
        if override:
            pages[relative]["explicit_lastmod"] = override
    (docs_root / MANIFEST_NAME).write_text(
        json.dumps({"pages": pages}, indent=2) + "\n", encoding="utf-8"
    )
    print(f"recorded source modification dates for {len(pages)} pages")


def on_pre_build(config, **kwargs):
    global _page_dates
    manifest = Path(config.docs_dir) / MANIFEST_NAME
    if not manifest.is_file():
        raise RuntimeError("Run scripts/collect_docs.py before building: sitemap date manifest is missing")
    _page_dates = json.loads(manifest.read_text(encoding="utf-8"))["pages"]


def on_page_markdown(markdown, page, config, files, **kwargs):
    relative = page.file.src_uri
    record = _page_dates.get(relative)
    if not record or record["sha256"] != page_hash(Path(page.file.abs_src_path)):
        raise RuntimeError(f"Run scripts/collect_docs.py again: sitemap date record is missing or stale: {relative}")
    date.fromisoformat(record["date"])
    page.update_date = record["date"]
    return markdown
