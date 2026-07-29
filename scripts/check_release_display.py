#!/usr/bin/env python3
"""Verify that version-pinned package-matrix commands match source manifests."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class DisplayCheck:
    repo_name: str
    ci_dir: str
    package: str


CHECKS: tuple[DisplayCheck, ...] = (
    DisplayCheck(
        "plc-comm-slmp-cpp-minimal",
        "slmp-cpp",
        "fa-yoshinobu/slmp-connect-cpp-minimal",
    ),
    DisplayCheck(
        "plc-comm-mcprotocol-serial-cpp",
        "mcprotocol-serial-cpp",
        "fa-yoshinobu/mcprotocol-serial-cpp",
    ),
)


def resolve_source(source_root: Path, check: DisplayCheck) -> Path:
    for directory in (check.repo_name, check.ci_dir):
        candidate = source_root / directory
        if (candidate / "library.json").is_file():
            return candidate
    raise FileNotFoundError(f"Could not find {check.repo_name} below {source_root}")


def manifest_version(source: Path) -> str:
    data = json.loads((source / "library.json").read_text(encoding="utf-8"))
    version = str(data.get("version", ""))
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:[-.][0-9A-Za-z.-]+)?", version):
        raise ValueError(f"Invalid library.json version in {source}: {version!r}")
    return version


def check_display(source_root: Path, matrix: str, check: DisplayCheck) -> None:
    source = resolve_source(source_root, check)
    expected = manifest_version(source)
    pattern = re.compile(rf"{re.escape(check.package)}@\^([^`\s|]+)")
    displayed = pattern.findall(matrix)
    if displayed != [expected]:
        raise RuntimeError(
            f"{check.package} display mismatch: expected one @^{expected}, found {displayed or 'none'}"
        )
    print(f"[OK] {check.package}@^{expected}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", default="..", help="Directory containing the source repositories")
    args = parser.parse_args()
    source_root = Path(args.source_root)
    if not source_root.is_absolute():
        source_root = (REPO_ROOT / source_root).resolve()

    try:
        matrix = (REPO_ROOT / "docs" / "package-matrix.md").read_text(encoding="utf-8")
        for check in CHECKS:
            check_display(source_root, matrix, check)
    except Exception as exc:
        print(f"check_release_display.py: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
