#!/usr/bin/env python3
"""Verify that mkdocstrings imports the canonical released Python packages."""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class PackageCheck:
    repo_name: str
    ci_dir: str
    distribution: str
    module: str
    required_symbols: tuple[str, ...]


CHECKS: tuple[PackageCheck, ...] = (
    PackageCheck(
        "plc-comm-computerlink-python",
        "computerlink-python",
        "plc-comm-toyopuc",
        "toyopuc",
        ("ToyopucConnectionOptions", "open_and_connect", "write_bit_in_word"),
    ),
    PackageCheck(
        "plc-comm-hostlink-python",
        "hostlink-python",
        "plc-comm-kv-hostlink",
        "hostlink",
        (
            "KvHostLinkPlcProfile",
            "available_plc_profiles",
            "write_bit_in_word",
            "write_bit_in_expansion_unit_buffer",
        ),
    ),
    PackageCheck(
        "plc-comm-slmp-python",
        "slmp-python",
        "plc-comm-slmp",
        "slmp",
        ("plc_profile_canonical_name", "device_range_model_label", "write_bit_in_word"),
    ),
)


def resolve_source(source_root: Path, check: PackageCheck) -> Path:
    for directory in (check.repo_name, check.ci_dir):
        candidate = source_root / directory
        if (candidate / "pyproject.toml").is_file():
            return candidate
    raise FileNotFoundError(f"Could not find {check.repo_name} below {source_root}")


def project_version(source: Path) -> str:
    data = tomllib.loads((source / "pyproject.toml").read_text(encoding="utf-8"))
    return str(data["project"]["version"])


def check_package(source_root: Path, check: PackageCheck) -> None:
    source = resolve_source(source_root, check)
    expected = project_version(source)
    installed = importlib.metadata.version(check.distribution)
    if installed != expected:
        raise RuntimeError(
            f"{check.distribution} version mismatch: source docs are {expected}, installed release is {installed}"
        )

    module = importlib.import_module(check.module)
    module_version = str(getattr(module, "__version__", ""))
    if module_version != expected:
        raise RuntimeError(f"{check.module}.__version__ mismatch: expected {expected}, got {module_version!r}")

    missing = [symbol for symbol in check.required_symbols if not hasattr(module, symbol)]
    if missing:
        raise RuntimeError(f"{check.distribution} {installed} is missing required API symbols: {', '.join(missing)}")
    print(f"[OK] {check.distribution} {installed}: {', '.join(check.required_symbols)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", default="..", help="Directory containing the source repositories")
    args = parser.parse_args()
    source_root = Path(args.source_root)
    if not source_root.is_absolute():
        source_root = (REPO_ROOT / source_root).resolve()

    try:
        for check in CHECKS:
            check_package(source_root, check)
    except Exception as exc:
        print(f"check_python_api_packages.py: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
