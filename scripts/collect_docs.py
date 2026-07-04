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


SLMP_PROFILE_REFERENCE_INDEX = """# SLMP Profile Reference

This section is built from the canonical `plc-comm-slmp-profiles` data repository during the documentation build.

Use it when you need to compare MELSEC SLMP profiles across the supported built-in Ethernet profiles.

For normal library usage, select the PLC profile in the library or Node-RED connection settings and follow that library's getting started guide.

For PLC-side Binary data code, port/open settings, and RUN-time write permission, use the [MELSEC SLMP PLC Setup Guide](../../plc-setup/index.md).

## Pages

| Page | Use it for |
| --- | --- |
| [Parameters](parameters.md) | Compare frame defaults, feature decisions, point limits, write policy, and device availability across profiles. |
| [Device ranges](device-ranges.md) | Check SD-derived range rules, fixed ranges, probe markers, and unsupported device families. |
| [Troubleshooting & end codes](troubleshooting-end-codes.md) | Map common SLMP end codes to likely causes and checks. |

## Scope

The profile data targets CPU built-in Ethernet ports. Extension Ethernet modules may support additional commands, but the built-in Ethernet profiles remain the conservative baseline.

Device range rules are not send/receive address guards for communication libraries. They are for applications that need to discover or display the valid device range of a selected PLC profile.
"""


SLMP_TROUBLESHOOTING_END_CODES = """# SLMP Troubleshooting & End Codes

This page summarizes situations observed during this project's live PLC verification and common SLMP setup issues. It is not the official definition of every SLMP end code. Use the Mitsubishi manuals for formal definitions and complete code tables.

## First Checks

Before chasing one code, confirm these basics:

- The application selected the correct canonical PLC profile.
- The PLC Ethernet port uses Binary SLMP data code; see the [MELSEC SLMP PLC Setup Guide](../../plc-setup/index.md).
- PLC-side RUN-time write permission is enabled before write tests where the PLC exposes that setting.
- Strict profile mode is enabled unless you intentionally want to send unsupported commands and let the PLC answer.
- Point counts are within the selected profile limits.
- Routed devices such as `Un\\Gn`, `Jn\\...`, and `U3En\\G` exist in the actual PLC configuration.

## Common End Codes

| End code | Typical symptom | Likely cause | What to check |
| --- | --- | --- | --- |
| `C050` | The TCP connection opens, but every request fails. | PLC-side data-code setting does not match the library request format, often ASCII vs binary. | Check the Ethernet open setting and use binary SLMP settings for these libraries. |
| `C051` | A direct word read/write fails at a large point count. | Word point count is over the selected profile limit. | Split the request or select the correct profile. In normal high-level use this should be caught before send. |
| `C052` | A direct bit read/write fails at a large point count. | Bit point count is over the selected profile limit. On iQ-F, observed `C051` and `C052` point-limit meanings differ from the other verified profiles. | Split the request and check the profile table for the active PLC. |
| `C053` | Random bit write fails when many bit devices are included. | Random bit write point count is over the profile limit. | Reduce the random write batch size. |
| `C054` | Random word read/write or monitor registration fails with many devices. | Random/monitor word count is over the profile limit. Dword devices can consume more than one word slot. | Reduce the batch size and account for word weighting. |
| `C056` | A request fails only for a high device number. | Device number is outside the PLC range. | Use an address that exists for the PLC program and configuration. |
| `C058` | A low-level or raw-frame request fails immediately. | Request length does not match the encoded address section. | Prefer high-level builders, or re-check raw frame length fields and address packing. |
| `C059` | A command fails even though the device address is ordinary. | Command or subcommand is not supported by the selected profile. | Check the profile's feature support. This is common for block/type-name commands on some Q/L profiles. |
| `C05B` | A routed or special device request fails. | The target CPU cannot access that device path or family. | Check PLC model, mounted modules, route notation, and whether the family exists on that profile. |
| `C05C` | A request fails after changing bit/word mode or count. | Request content is invalid for that command, such as a bit-unit mismatch. | Check the command variant, device family type, address unit, and count. |
| `C05F` | The command is syntactically valid but still refused. | The target CPU cannot execute that request in the current state or route. | Check CPU mode, route, command support, and profile setting. |
| `C061` | A raw-frame or low-level request fails with a length/count error. | Request data length and data count disagree. | Recalculate count fields and payload length, or use a high-level helper. |
| `C0B5` | A file-register or special data request is refused by the CPU. | The CPU cannot handle that data specification. | Check whether the selected profile and PLC model support the requested family or data area. |
| `C200`, `C201`, `C204` | Access is refused after the network path is established. | Remote password state prevents the operation. | Release the remote password and check whether another device owns the unlock state. |
| `4030`, `4031` | The PLC reports a CPU-side device name or device number error. | Invalid device family, invalid device number, or nonexistent routed path. | Re-check the device notation and PLC configuration. Treat other 4000-series CPU errors as manual lookup items. |

## Profile Limit Codes

`C051` through `C054` are normally prevented by the library profile checks when using the high-level API. If they appear in normal usage, check for one of these first:

- The profile was not selected correctly.
- The call used a raw or low-level path that bypasses profile checks.
- The bundled profile data is stale.
- The request includes dword devices and the weighted word count is higher than expected.

## Unsupported Operations

For unsupported profile features, the preferred behavior is to reject before sending when strict profile mode is enabled. If strict profile mode is disabled, the request is sent and the PLC end code becomes the diagnostic result.

Use this only for troubleshooting or compatibility investigation. Normal applications should keep strict profile behavior enabled.
"""


REMOVE_AFTER_COPY: tuple[str, ...] = (
    "slmp/profile-reference/device-range-rules.md",
    "slmp/profile-reference/profile-comparison.md",
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

    for source in SOURCE_FILES:
        source_file = resolve_source_file(source_root, source)
        target_file = docs_root / source.target_file
        copy_file(source_file, target_file)
        print(f"collected {source.repo_name}: {source_file} -> {target_file}")

    write_generated_page(docs_root / "slmp/profile-reference/index.md", SLMP_PROFILE_REFERENCE_INDEX)
    write_generated_page(
        docs_root / "slmp/profile-reference/troubleshooting-end-codes.md",
        SLMP_TROUBLESHOOTING_END_CODES,
    )

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
