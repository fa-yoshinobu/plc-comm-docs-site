#!/usr/bin/env python3
"""Collect source repository documentation into the MkDocs site tree.

The docs site keeps only its landing pages, PLC setup guide, and assets in git.
Protocol/library pages are copied from source repositories before building.
This script is the single implementation used by both local preview and CI.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class SourceDocs:
    repo_name: str
    ci_dir: str
    source_dir: str
    target_dir: str


SOURCES: tuple[SourceDocs, ...] = (
    SourceDocs("plc-comm-computerlink-dotnet", "computerlink-dotnet", "docsrc/user", "computerlink/dotnet"),
    SourceDocs("plc-comm-computerlink-python", "computerlink-python", "docsrc/user", "computerlink/python"),
    SourceDocs("plc-comm-hostlink-dotnet", "hostlink-dotnet", "docsrc/user", "hostlink/dotnet"),
    SourceDocs("plc-comm-hostlink-python", "hostlink-python", "docsrc/user", "hostlink/python"),
    SourceDocs("plc-comm-hostlink-rust", "hostlink-rust", "docs", "hostlink/rust"),
    SourceDocs("node-red-contrib-plc-comm-kvhostlink", "hostlink-nodered", "docsrc/user", "hostlink/nodered"),
    SourceDocs("plc-comm-slmp-dotnet", "slmp-dotnet", "docsrc/user", "slmp/dotnet"),
    SourceDocs("plc-comm-slmp-python", "slmp-python", "docsrc/user", "slmp/python"),
    SourceDocs("plc-comm-slmp-rust", "slmp-rust", "docs", "slmp/rust"),
    SourceDocs("plc-comm-slmp-cpp-minimal", "slmp-cpp", "docsrc/user", "slmp/cpp"),
    SourceDocs("node-red-contrib-plc-comm-slmp", "slmp-nodered", "docsrc/user", "slmp/nodered"),
    SourceDocs("plc-comm-mcprotocol-serial-cpp", "mcprotocol-serial-cpp", "docsrc/user", "mcprotocol/cpp"),
)


REMOVE_AFTER_COPY: tuple[str, ...] = (
    "mcprotocol/cpp/README.md",
    "hostlink/rust/DEVELOPMENT_HISTORY.md",
    "hostlink/rust/KV5000_LIVE_VALIDATION_2026-05-03.md",
    "hostlink/rust/KV7000_LIVE_VALIDATION_2026-05-03.md",
    "hostlink/rust/RELEASE_PUBLICATION_2026-06-12.md",
    "slmp/rust/DEVELOPMENT_HISTORY.md",
    "slmp/rust/EXTENDED_DEVICE_COVERAGE_LATEST.md",
    "slmp/rust/IQF_DEVICE_RANGE_SAMPLE_VALIDATION_2026-05-03.md",
    "slmp/rust/IQL_DEVICE_RANGE_SAMPLE_VALIDATION_2026-05-03.md",
    "slmp/rust/IQL_EXTENDED_DEVICE_COVERAGE_2026-05-03.md",
    "slmp/rust/IQL_LIVE_STRESS_VALIDATION_2026-05-03.md",
    "slmp/rust/IQR_DEVICE_RANGE_SAMPLE_VALIDATION_2026-05-03.md",
    "slmp/rust/IQR_EXTENDED_DEVICE_COVERAGE_2026-05-29.md",
    "slmp/rust/LCPU_DEVICE_RANGE_SAMPLE_VALIDATION_2026-05-03.md",
    "slmp/rust/MIXED_BLOCK_WRITE_1406_NOTES_2026-05-03.md",
    "slmp/rust/QCPU_RUNTIME_RANGE_VALIDATION_2026-05-15.md",
    "slmp/rust/QNU_RUNTIME_RANGE_VALIDATION_2026-05-15.md",
    "slmp/rust/QNUDV_DEVICE_RANGE_SAMPLE_VALIDATION_2026-05-03.md",
    "slmp/rust/QNUDV_RUNTIME_RANGE_VALIDATION_2026-05-15.md",
    "slmp/rust/RELEASE_PUBLICATION_2026-06-12.md",
)


LINK_REPLACEMENTS: dict[str, dict[str, str]] = {
    "slmp/rust": {
        "(../src/": "(https://github.com/fa-yoshinobu/plc-comm-slmp-rust/blob/main/src/",
    },
    "mcprotocol/cpp": {
        "(../../examples/": "(https://github.com/fa-yoshinobu/plc-comm-mcprotocol-serial-cpp/blob/main/examples/",
        "(../../include/": "(https://github.com/fa-yoshinobu/plc-comm-mcprotocol-serial-cpp/blob/main/include/",
    },
}


RETAINED_NOTE = "retained in the source repository technical notes"
LOCAL_VALIDATION_LINK_RE = re.compile(r"\[([^\]]+)\]\(\.\./validation/reports/[A-Za-z0-9_./-]+\.md\)")
TECHNICAL_RECORD_LINK_RE = re.compile(
    r"\[([^\]]+)\]\((?:"
    r"KV5000_LIVE_VALIDATION_2026-05-03|"
    r"KV7000_LIVE_VALIDATION_2026-05-03|"
    r"IQF_DEVICE_RANGE_SAMPLE_VALIDATION_2026-05-03|"
    r"IQL_DEVICE_RANGE_SAMPLE_VALIDATION_2026-05-03|"
    r"IQL_LIVE_STRESS_VALIDATION_2026-05-03|"
    r"IQR_DEVICE_RANGE_SAMPLE_VALIDATION_2026-05-03|"
    r"LCPU_DEVICE_RANGE_SAMPLE_VALIDATION_2026-05-03|"
    r"QCPU_RUNTIME_RANGE_VALIDATION_2026-05-15|"
    r"QNU_RUNTIME_RANGE_VALIDATION_2026-05-15|"
    r"QNUDV_DEVICE_RANGE_SAMPLE_VALIDATION_2026-05-03|"
    r"QNUDV_RUNTIME_RANGE_VALIDATION_2026-05-15"
    r")\.md\)"
)


def resolve_path(raw: str, base: Path) -> Path:
    path = Path(raw)
    if not path.is_absolute():
        path = base / path
    return path.resolve()


def resolve_source(source_root: Path, source: SourceDocs) -> Path:
    for directory_name in (source.repo_name, source.ci_dir):
        candidate = source_root / directory_name / source.source_dir
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError(
        f"Could not find docs for {source.repo_name}. Tried "
        f"{source_root / source.repo_name / source.source_dir} and "
        f"{source_root / source.ci_dir / source.source_dir}."
    )


def copy_contents(source_dir: Path, target_dir: Path) -> None:
    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    for child in source_dir.iterdir():
        target = target_dir / child.name
        if child.is_dir():
            shutil.copytree(child, target)
        else:
            shutil.copy2(child, target)


def remove_unpublished_files(docs_root: Path) -> None:
    for relative in REMOVE_AFTER_COPY:
        path = docs_root / relative
        if path.exists():
            path.unlink()


def replace_text(path: Path, replacements: dict[str, str]) -> None:
    text = path.read_text(encoding="utf-8")
    updated = text
    for old, new in replacements.items():
        updated = updated.replace(old, new)
    if updated != text:
        path.write_text(updated, encoding="utf-8")


def postprocess_links(docs_root: Path) -> None:
    for relative_folder, replacements in LINK_REPLACEMENTS.items():
        folder = docs_root / relative_folder
        if not folder.exists():
            continue
        for path in folder.rglob("*.md"):
            replace_text(path, replacements)

    for relative_folder in ("slmp/cpp", "mcprotocol/cpp"):
        folder = docs_root / relative_folder
        if not folder.exists():
            continue
        for path in folder.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            updated = LOCAL_VALIDATION_LINK_RE.sub(lambda match: f"{match.group(1)} ({RETAINED_NOTE})", text)
            if updated != text:
                path.write_text(updated, encoding="utf-8")

    for relative in (
        "hostlink/rust/LATEST_COMMUNICATION_VERIFICATION.md",
        "slmp/rust/LATEST_COMMUNICATION_VERIFICATION.md",
    ):
        path = docs_root / relative
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        updated = TECHNICAL_RECORD_LINK_RE.sub(lambda match: f"{match.group(1)} ({RETAINED_NOTE})", text)
        if updated != text:
            path.write_text(updated, encoding="utf-8")


def collect_docs(source_root: Path, docs_root: Path) -> None:
    for source in SOURCES:
        source_dir = resolve_source(source_root, source)
        target_dir = docs_root / source.target_dir
        copy_contents(source_dir, target_dir)
        print(f"collected {source.repo_name}: {source_dir} -> {target_dir}")

    remove_unpublished_files(docs_root)
    postprocess_links(docs_root)


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect source repository docs for the MkDocs site.")
    parser.add_argument(
        "--source-root",
        default="..",
        help="Directory containing source repos. Use '..' locally or '_src' in CI. Default: '..'.",
    )
    parser.add_argument(
        "--docs-root",
        default="docs",
        help="MkDocs docs directory to populate. Default: docs.",
    )
    args = parser.parse_args()

    source_root = resolve_path(args.source_root, REPO_ROOT)
    docs_root = resolve_path(args.docs_root, REPO_ROOT)

    try:
        collect_docs(source_root, docs_root)
    except Exception as exc:
        print(f"collect_docs.py: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
