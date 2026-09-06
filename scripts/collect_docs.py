#!/usr/bin/env python3
"""Collect source repository documentation into the MkDocs site tree.

The docs site keeps only its landing pages, PLC setup guide, and assets in git.
Protocol/library pages are copied from source repositories before building.
This script is the single implementation used by both local preview and CI.
"""

from __future__ import annotations

import argparse
import os
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


@dataclass(frozen=True)
class SourceFile:
    repo_name: str
    ci_dir: str
    source_file: str
    target_file: str


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


SOURCE_FILES: tuple[SourceFile, ...] = (
    SourceFile(
        "plc-comm-computerlink-profiles",
        "computerlink-profiles",
        "tables/toyopuc_profile_parameters.md",
        "computerlink/profile-reference/parameters.md",
    ),
    SourceFile(
        "plc-comm-computerlink-profiles",
        "computerlink-profiles",
        "tables/toyopuc_area_ranges.md",
        "computerlink/profile-reference/area-ranges.md",
    ),
    SourceFile(
        "plc-comm-hostlink-profiles",
        "hostlink-profiles",
        "tables/kv_profile_parameters.md",
        "hostlink/profile-reference/parameters.md",
    ),
    SourceFile(
        "plc-comm-hostlink-profiles",
        "hostlink-profiles",
        "tables/kv_device_ranges.md",
        "hostlink/profile-reference/device-ranges.md",
    ),
    SourceFile(
        "plc-comm-slmp-profiles",
        "slmp-profiles",
        "tables/slmp_profile_parameters.md",
        "slmp/profile-reference/parameters.md",
    ),
    SourceFile(
        "plc-comm-slmp-profiles",
        "slmp-profiles",
        "tables/slmp_device_ranges.md",
        "slmp/profile-reference/device-ranges.md",
    ),
)


PAGES_ROOT = Path(__file__).resolve().parent / "pages"


def read_page_source(relative: str) -> str:
    """Read one page body from scripts/pages/."""
    path = PAGES_ROOT / relative
    if not path.is_file():
        raise RuntimeError(f"page source is missing: scripts/pages/{relative}")
    return path.read_text(encoding="utf-8")


# Pages this repository owns rather than collects. The body of each one lives in
# scripts/pages/ under the same relative path it is published at, so editing a
# troubleshooting table is a Markdown change and not a build-script change.
GENERATED_PAGES: tuple[str, ...] = (
    "computerlink/profile-reference/index.md",
    "hostlink/profile-reference/index.md",
    "slmp/profile-reference/index.md",
    "slmp/api-parity.md",
    "plc-setup/slmp/troubleshooting-codes.md",
    "plc-setup/kv/troubleshooting-codes.md",
    "plc-setup/kv/device-ranges.md",
    "plc-setup/computerlink/troubleshooting-codes.md",
    "plc-setup/computerlink/device-ranges.md",
    "plc-setup/mcprotocol/troubleshooting-codes.md",
    "plc-setup/mcprotocol/supported-registers.md",
)


# Included in the generated SLMP Python API reference page.
SLMP_PYTHON_API_OPERATION_INDEX = read_page_source("partials/slmp-python-api-operation-index.md")


PYTHON_API_REFERENCE_PAGES: tuple[tuple[str, str, str, str], ...] = (
    (
        "computerlink/python/API_REFERENCE.md",
        "TOYOPUC Computerlink Python API Reference",
        "toyopuc",
        "plc-comm-toyopuc",
    ),
    (
        "hostlink/python/API_REFERENCE.md",
        "KV Host Link Python API Reference",
        "hostlink",
        "plc-comm-kv-hostlink",
    ),
    (
        "slmp/python/API_REFERENCE.md",
        "SLMP Python API Reference",
        "slmp",
        "plc-comm-slmp",
    ),
)


SLMP_PARITY_SURFACE_MARKERS: tuple[tuple[str, str, str, tuple[str, ...]], ...] = (
    ("plc-comm-slmp-python", "slmp-python", "docsrc/user/API_REFERENCE.md", ("register_monitor_devices", "self_test_loopback", "clear_error", r"U3E0\HG")),
    ("plc-comm-slmp-dotnet", "slmp-dotnet", "docsrc/user/API_REFERENCE.md", ("RegisterMonitorDevicesAsync", "SelfTestLoopbackAsync", "ClearErrorAsync", "ReadWordsExtendedAsync")),
    ("plc-comm-slmp-cpp-minimal", "slmp-cpp", "docsrc/user/API_REFERENCE.md", ("registerMonitorDevices", "selfTestLoopback", "clearError", "U3En&#92;HG")),
    ("plc-comm-slmp-rust", "slmp-rust", "docs/API_REFERENCE.md", ("register_monitor_devices", "self_test_loopback", "clear_error", "parse_qualified_device")),
    ("node-red-contrib-plc-comm-slmp", "slmp-nodered", "docsrc/user/API_REFERENCE.md", ("registerMonitorDevices", "selfTestLoopback", "clearError", r"U3E0\HG")),
)


REMOVE_AFTER_COPY: tuple[str, ...] = (
    "slmp/profile-reference/device-range-rules.md",
    "slmp/profile-reference/profile-comparison.md",
    "slmp/profile-reference/troubleshooting-end-codes.md",
    "plc-setup/slmp/troubleshooting-end-codes.md",
    "plc-setup/kv/error-codes.md",
    "plc-setup/computerlink/error-codes.md",
    "plc-setup/mcprotocol/error-codes.md",
    "mcprotocol/cpp/README.md",
    "hostlink/rust/KV5000_LIVE_VALIDATION_2026-05-03.md",
    "hostlink/rust/KV7000_LIVE_VALIDATION_2026-05-03.md",
    "hostlink/rust/RELEASE_PUBLICATION_2026-06-12.md",
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


# Every library ships the same five page names, so the nav label alone ("Getting
# started") is identical on 12 pages. The nav label is what a reader wants in the
# sidebar, but it becomes the <title>, the search-result heading, and the social
# card heading too. Material resolves all three from `page.meta.title` when it is
# present and falls back to the nav label otherwise, so collected pages get a
# front matter title that names the protocol and language, and the sidebar stays
# short.
PAGE_TITLES: dict[str, str] = {
    "GETTING_STARTED.md": "Getting started",
    "USAGE_GUIDE.md": "Usage guide",
    "API_REFERENCE.md": "API reference",
    "PROFILES.md": "Profiles",
    "GOTCHAS.md": "Gotchas",
}


PAGE_DESCRIPTIONS: dict[str, str] = {
    "GETTING_STARTED.md": (
        "Install the {language} {protocol} library and make a first read from a "
        "{vendor} PLC: connection options, PLC profile, and a typed device read."
    ),
    "USAGE_GUIDE.md": (
        "Task-oriented {protocol} guide for {language}: reading and writing devices "
        "by name, typed values, and connection handling against a {vendor} PLC."
    ),
    "API_REFERENCE.md": (
        "Complete public API of the {language} {protocol} library: client, connection "
        "options, address parsing, and the supported device operations."
    ),
    "PROFILES.md": (
        "{vendor} PLC model profiles in the {language} {protocol} library, and how "
        "selecting a profile sets the address grammar and device ranges."
    ),
    "GOTCHAS.md": (
        "Sharp edges before shipping {protocol} in {language}: device quirks, request "
        "limits, and failure modes found during real-hardware verification."
    ),
}


PROTOCOL_LABELS: dict[str, tuple[str, str]] = {
    "slmp": ("SLMP", "MELSEC"),
    "hostlink": ("KV Host Link", "KEYENCE KV"),
    "computerlink": ("Computerlink", "JTEKT TOYOPUC"),
    "mcprotocol": ("MC Protocol Serial", "MELSEC"),
}


LANGUAGE_LABELS: dict[str, str] = {
    "dotnet": ".NET",
    "python": "Python",
    "rust": "Rust",
    "cpp": "C++",
    "nodered": "Node-RED",
}


# Pages that are not part of a library's five-page set. An empty description
# means the generated page already carries one.
GENERATED_PAGE_METADATA: tuple[tuple[str, str, str], ...] = (
    (
        "slmp/api-parity.md",
        "SLMP API parity across implementations",
        "Which SLMP operations are implemented in each maintained library — Python, "
        ".NET, C++ minimal, Rust, and Node-RED — with the current scope boundaries.",
    ),
    (
        "slmp/profile-reference/index.md",
        "MELSEC SLMP profile reference",
        "Compare MELSEC SLMP PLC profiles: frame defaults, feature support, point "
        "limits, and device availability across built-in Ethernet ports and units.",
    ),
    (
        "slmp/profile-reference/parameters.md",
        "SLMP profile parameters",
        "Frame defaults, feature decisions, point limits, write policy, and device "
        "availability for every MELSEC SLMP PLC profile.",
    ),
    (
        "slmp/profile-reference/device-ranges.md",
        "SLMP device ranges by profile",
        "SD-derived range rules, fixed ranges, probe markers, and unsupported device "
        "families for every MELSEC SLMP PLC profile.",
    ),
    (
        "hostlink/profile-reference/index.md",
        "KEYENCE KV Host Link profile reference",
        "Compare KEYENCE KV Host Link PLC profiles: canonical IDs, display names, "
        "XYM notation variants, and device range rows.",
    ),
    (
        "hostlink/profile-reference/parameters.md",
        "KV Host Link profile parameters",
        "Canonical IDs, display names, native and XYM device relationships, and "
        "verified-model status for every KEYENCE KV Host Link profile.",
    ),
    (
        "hostlink/profile-reference/device-ranges.md",
        "KV Host Link device ranges by profile",
        "Device definitions and ranges compared across the supported KEYENCE KV Host "
        "Link PLC profiles.",
    ),
    (
        "computerlink/profile-reference/index.md",
        "TOYOPUC Computerlink profile reference",
        "Compare JTEKT TOYOPUC Computer Link profiles: display names, profile IDs, "
        "area counts, addressing options, and area range attributes.",
    ),
    (
        "computerlink/profile-reference/parameters.md",
        "TOYOPUC Computerlink profile parameters",
        "Display names, profile IDs, area counts, addressing options, and "
        "verified-model status for every JTEKT TOYOPUC Computer Link profile.",
    ),
    (
        "computerlink/profile-reference/area-ranges.md",
        "TOYOPUC Computerlink area ranges by profile",
        "Direct, prefixed, packed, width, and step attributes compared across the "
        "supported JTEKT TOYOPUC Computer Link profiles.",
    ),
    ("plc-setup/slmp/troubleshooting-codes.md", "SLMP troubleshooting and end codes", ""),
    ("plc-setup/kv/troubleshooting-codes.md", "KV Host Link troubleshooting and error codes", ""),
    ("plc-setup/kv/device-ranges.md", "KV Host Link device ranges", ""),
    ("plc-setup/computerlink/troubleshooting-codes.md", "Computerlink troubleshooting and error codes", ""),
    ("plc-setup/computerlink/device-ranges.md", "Computerlink device ranges", ""),
    ("plc-setup/mcprotocol/troubleshooting-codes.md", "MC Protocol Serial troubleshooting and error codes", ""),
    ("plc-setup/mcprotocol/supported-registers.md", "MC Protocol Serial supported registers", ""),
)


# A reader who finishes a library page has no way back to that library's
# repository, registry entry, or changelog: the header repository link points at
# this docs site, not at the library. Each collected page gets a footer naming
# its own library.
REGISTRY_LINKS: dict[str, tuple[str, str]] = {
    "computerlink/dotnet": ("NuGet: PlcComm.Toyopuc", "https://www.nuget.org/packages/PlcComm.Toyopuc"),
    "computerlink/python": ("PyPI: plc-comm-toyopuc", "https://pypi.org/project/plc-comm-toyopuc/"),
    "hostlink/dotnet": ("NuGet: PlcComm.KvHostLink", "https://www.nuget.org/packages/PlcComm.KvHostLink"),
    "hostlink/python": ("PyPI: plc-comm-kv-hostlink", "https://pypi.org/project/plc-comm-kv-hostlink/"),
    "hostlink/rust": ("crates.io: plc-comm-kv-hostlink", "https://crates.io/crates/plc-comm-kv-hostlink"),
    "hostlink/nodered": (
        "npm: @fa_yoshinobu/node-red-contrib-plc-comm-kvhostlink",
        "https://www.npmjs.com/package/@fa_yoshinobu/node-red-contrib-plc-comm-kvhostlink",
    ),
    "slmp/dotnet": ("NuGet: PlcComm.Slmp", "https://www.nuget.org/packages/PlcComm.Slmp"),
    "slmp/python": ("PyPI: plc-comm-slmp", "https://pypi.org/project/plc-comm-slmp/"),
    "slmp/rust": ("crates.io: plc-comm-slmp", "https://crates.io/crates/plc-comm-slmp"),
    "slmp/cpp": (
        "PlatformIO: fa-yoshinobu/slmp-connect-cpp-minimal",
        "https://registry.platformio.org/libraries/fa-yoshinobu/slmp-connect-cpp-minimal",
    ),
    "slmp/nodered": (
        "npm: @fa_yoshinobu/node-red-contrib-plc-comm-slmp",
        "https://www.npmjs.com/package/@fa_yoshinobu/node-red-contrib-plc-comm-slmp",
    ),
    "mcprotocol/cpp": (
        "PlatformIO: fa-yoshinobu/mcprotocol-serial-cpp",
        "https://registry.platformio.org/libraries/fa-yoshinobu/mcprotocol-serial-cpp",
    ),
}


LIBRARY_FOOTER_HEADING = "## This library"


FRONT_MATTER_DELIMITER = "---"
RETAINED_NOTE = "retained in the source repository technical notes"

# Source repositories link to shared site pages with absolute URLs so the links
# also work when the same Markdown is read on GitHub. Collected copies are
# rewritten to site-relative Markdown links so MkDocs validates them; an
# absolute URL is invisible to the link and anchor checks and can rot silently.
SITE_ABSOLUTE_URL_RE = re.compile(
    r"https://(?:fa-yoshinobu\.github\.io/plc-comm-docs-site|plc-comm-docs-site\.fa-labo\.com)"
    r"(?P<path>/[A-Za-z0-9_./-]*)?"
    r"(?P<anchor>#[A-Za-z0-9_-]+)?"
)
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


def resolve_source_file(source_root: Path, source: SourceFile) -> Path:
    for directory_name in (source.repo_name, source.ci_dir):
        candidate = source_root / directory_name / source.source_file
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(
        f"Could not find source file for {source.repo_name}. Tried "
        f"{source_root / source.repo_name / source.source_file} and "
        f"{source_root / source.ci_dir / source.source_file}."
    )


def resolve_repo_file(source_root: Path, repo_name: str, ci_dir: str, relative_path: str) -> Path:
    for directory_name in (repo_name, ci_dir):
        candidate = source_root / directory_name / relative_path
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(
        f"Could not find {relative_path} for {repo_name} below {source_root}."
    )


def public_api_table_symbols(markdown: str) -> set[str]:
    """Return every code-formatted symbol in a Markdown Public API table cell."""
    symbols: set[str] = set()
    for line in markdown.splitlines():
        if not line.startswith("|") or re.match(r"^\|\s*-", line):
            continue
        columns = line.split("|")
        if len(columns) < 4 or columns[1].strip() == "Operation":
            continue
        symbols.update(re.findall(r"`([^`]+)`", columns[2]))
    return symbols


def validate_operation_index(operation_index: str, source_reference: str) -> None:
    indexed = public_api_table_symbols(operation_index)
    public = public_api_table_symbols(source_reference)
    stale = sorted(indexed - public)
    if stale:
        raise RuntimeError(
            "SLMP Python operation index names symbols absent from source Public API tables: "
            + ", ".join(stale)
        )


def validate_slmp_api_indexes(source_root: Path) -> None:
    python_reference = resolve_repo_file(
        source_root,
        "plc-comm-slmp-python",
        "slmp-python",
        "docsrc/user/API_REFERENCE.md",
    ).read_text(encoding="utf-8")
    validate_operation_index(SLMP_PYTHON_API_OPERATION_INDEX, python_reference)

    for repo_name, ci_dir, relative_path, markers in SLMP_PARITY_SURFACE_MARKERS:
        reference = resolve_repo_file(source_root, repo_name, ci_dir, relative_path).read_text(encoding="utf-8")
        missing = [marker for marker in markers if marker not in reference]
        if missing:
            raise RuntimeError(
                f"SLMP API parity markers missing from {repo_name}/{relative_path}: " + ", ".join(missing)
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


def copy_file(source_file: Path, target_file: Path) -> None:
    target_file.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_file, target_file)


def write_generated_page(target_file: Path, text: str) -> None:
    target_file.parent.mkdir(parents=True, exist_ok=True)
    target_file.write_text(text, encoding="utf-8")


def python_api_reference_page(title: str, module_name: str, package_name: str) -> str:
    operation_index = ""
    if module_name == "slmp":
        operation_index = f"\n{SLMP_PYTHON_API_OPERATION_INDEX}\n"

    return f"""# {title}

This page is generated during the docs-site build from the installed `{package_name}` PyPI package.

It follows the latest package release installed by the site build. Use the handwritten Getting started and Usage guide pages for task-oriented examples, and this page for the complete public Python API surface.
{operation_index}
## Generated API Details

::: {module_name}
    options:
      members: true
"""


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


def library_page_metadata(target_dir: str, file_name: str) -> tuple[str, str] | None:
    """Build the title and description for one page of a library's five-page set."""
    protocol_key, _, language_key = target_dir.partition("/")
    protocol = PROTOCOL_LABELS.get(protocol_key)
    language = LANGUAGE_LABELS.get(language_key)
    page = PAGE_TITLES.get(file_name)
    if protocol is None or language is None or page is None:
        return None

    protocol_label, vendor = protocol
    description = PAGE_DESCRIPTIONS[file_name].format(
        protocol=protocol_label, language=language, vendor=vendor
    )
    return f"{protocol_label} for {language} — {page}", description


def insert_front_matter_fields(text: str, fields: dict[str, str]) -> str:
    """Add front matter fields, leaving any field the document already sets."""
    for name, value in fields.items():
        if '"' in value:
            raise RuntimeError(f"front matter value for {name} must not contain a double quote: {value}")

    lines = text.splitlines(keepends=True)
    if lines and lines[0].strip() == FRONT_MATTER_DELIMITER:
        end = next(
            (index for index in range(1, len(lines)) if lines[index].strip() == FRONT_MATTER_DELIMITER),
            None,
        )
        if end is None:
            raise RuntimeError("front matter block is not terminated")
        present = {line.split(":", 1)[0].strip() for line in lines[1:end] if ":" in line}
        added = [f'{name}: "{value}"\n' for name, value in fields.items() if name not in present]
        return "".join(lines[:end] + added + lines[end:])

    added = [f'{name}: "{value}"\n' for name, value in fields.items()]
    return "".join([f"{FRONT_MATTER_DELIMITER}\n", *added, f"{FRONT_MATTER_DELIMITER}\n", "\n", *lines])


def apply_page_metadata(docs_root: Path) -> int:
    """Give every collected and generated page a unique title and a description."""
    applied = 0

    def apply(relative: str, title: str, description: str) -> None:
        nonlocal applied
        path = docs_root / relative
        if not path.is_file():
            raise RuntimeError(f"page metadata target is missing: {relative}")

        fields = {"title": title}
        if description:
            fields["description"] = description

        text = path.read_text(encoding="utf-8")
        updated = insert_front_matter_fields(text, fields)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            applied += 1

    for source in SOURCES:
        for file_name in PAGE_TITLES:
            metadata = library_page_metadata(source.target_dir, file_name)
            if metadata is None:
                raise RuntimeError(f"no metadata rule for {source.target_dir}/{file_name}")
            title, description = metadata
            apply(f"{source.target_dir}/{file_name}", title, description)

    for relative, title, description in GENERATED_PAGE_METADATA:
        apply(relative, title, description)

    return applied


def library_footer(target_dir: str, repo_name: str) -> str:
    """Build the source and package footer for one library's pages."""
    registry = REGISTRY_LINKS.get(target_dir)
    if registry is None:
        raise RuntimeError(f"no registry link for {target_dir}")

    registry_label, registry_url = registry
    repo_url = f"https://github.com/fa-yoshinobu/{repo_name}"
    return "\n".join(
        [
            "",
            LIBRARY_FOOTER_HEADING,
            "",
            "| | |",
            "|---|---|",
            f"| Source | [{repo_name}]({repo_url}) |",
            f"| Package | [{registry_label}]({registry_url}) |",
            f"| Changelog | [CHANGELOG.md]({repo_url}/blob/main/CHANGELOG.md) |",
            f"| Report a problem | [Issues]({repo_url}/issues) |",
            "",
        ]
    )


def append_library_footers(docs_root: Path) -> int:
    """Append the source and package footer to every collected library page."""
    appended = 0
    for source in SOURCES:
        footer = library_footer(source.target_dir, source.repo_name)
        for file_name in PAGE_TITLES:
            path = docs_root / source.target_dir / file_name
            if not path.is_file():
                raise RuntimeError(f"library page is missing: {source.target_dir}/{file_name}")

            text = path.read_text(encoding="utf-8")
            if LIBRARY_FOOTER_HEADING in text:
                continue
            if not text.endswith("\n"):
                text += "\n"
            path.write_text(text + footer, encoding="utf-8")
            appended += 1

    return appended


def verify_page_descriptions(docs_root: Path) -> None:
    """Fail the build if any published page would fall back to the site description."""
    missing = [
        path.relative_to(docs_root).as_posix()
        for path in sorted(docs_root.rglob("*.md"))
        if not re.search(r"(?m)^description:", path.read_text(encoding="utf-8"))
    ]
    if missing:
        raise RuntimeError(
            "pages without a description, which would share the site description: "
            + ", ".join(missing)
        )


def resolve_site_url_target(docs_root: Path, url_path: str) -> Path | None:
    """Return the Markdown source for a published site URL path, if it exists."""
    trimmed = (url_path or "/").strip("/")
    if not trimmed:
        candidate = docs_root / "index.md"
        return candidate if candidate.is_file() else None

    for relative in (f"{trimmed}.md", f"{trimmed}/index.md"):
        candidate = docs_root / relative
        if candidate.is_file():
            return candidate
    return None


def rewrite_site_absolute_links(docs_root: Path) -> int:
    """Rewrite absolute links to this site into relative Markdown links.

    A URL that does not resolve to a collected page is left untouched so the
    build does not invent a link target; the CI link check reports it instead.
    """
    rewritten = 0

    for path in sorted(docs_root.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        replacements = 0

        def replace(match: re.Match[str]) -> str:
            nonlocal replacements
            target = resolve_site_url_target(docs_root, match.group("path") or "/")
            if target is None:
                return match.group(0)
            relative = os.path.relpath(target, path.parent).replace(os.sep, "/")
            replacements += 1
            return f"{relative}{match.group('anchor') or ''}"

        updated = SITE_ABSOLUTE_URL_RE.sub(replace, text)
        if replacements:
            path.write_text(updated, encoding="utf-8")
            rewritten += replacements

    return rewritten


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

    rewritten = rewrite_site_absolute_links(docs_root)
    print(f"rewrote {rewritten} absolute site links to relative Markdown links")


def collect_docs(source_root: Path, docs_root: Path) -> None:
    validate_slmp_api_indexes(source_root)
    for source in SOURCES:
        source_dir = resolve_source(source_root, source)
        target_dir = docs_root / source.target_dir
        copy_contents(source_dir, target_dir)
        print(f"collected {source.repo_name}: {source_dir} -> {target_dir}")

    for source in SOURCE_FILES:
        source_file = resolve_source_file(source_root, source)
        target_file = docs_root / source.target_file
        copy_file(source_file, target_file)
        print(f"collected {source.repo_name}: {source_file} -> {target_file}")

    for relative in GENERATED_PAGES:
        write_generated_page(docs_root / relative, read_page_source(relative))
        print(f"generated {relative}")

    for relative_path, title, module_name, package_name in PYTHON_API_REFERENCE_PAGES:
        write_generated_page(docs_root / relative_path, python_api_reference_page(title, module_name, package_name))

    remove_unpublished_files(docs_root)

    applied = apply_page_metadata(docs_root)
    print(f"applied front matter title and description to {applied} pages")
    verify_page_descriptions(docs_root)

    appended = append_library_footers(docs_root)
    print(f"appended the source and package footer to {appended} pages")

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
