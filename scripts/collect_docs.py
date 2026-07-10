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


COMPUTERLINK_PROFILE_REFERENCE_INDEX = """# TOYOPUC Computer Link Profile Reference

This section is built from the canonical `plc-comm-computerlink-profiles` data repository during the documentation build.

Use it when you need to compare TOYOPUC Computer Link profile options and area ranges across supported profiles.

For normal library usage, select the PLC profile in the .NET or Python library settings and follow that library's getting started guide.

## Pages

| Page | Use it for |
| --- | --- |
| [Parameters](parameters.md) | Compare display names, profile IDs, area counts, addressing options, and verified-model status. |
| [Area ranges](area-ranges.md) | Compare direct, prefixed, packed, width, and step attributes across TOYOPUC profiles. |

## Scope

Ranges are catalog data for profile selection, UI address pickers, and application-layer checks. The actual PLC model, link route, project settings, and run/write permission can still reject a request.
"""


HOSTLINK_PROFILE_REFERENCE_INDEX = """# KEYENCE KV Host Link Profile Reference

This section is built from the canonical `plc-comm-hostlink-profiles` data repository during the documentation build.

Use it when you need to compare KEYENCE KV Host Link profile IDs, display names, XYM notation variants, and device range rows.

For normal library usage, select the PLC profile in the library or Node-RED connection settings and follow that library's getting started guide.

## Pages

| Page | Use it for |
| --- | --- |
| [Parameters](parameters.md) | Compare canonical IDs, display names, native/XYM relationships, and verified-model status. |
| [Device ranges](device-ranges.md) | Compare device definitions and ranges across the supported KEYENCE KV profiles. |

## Scope

Ranges are catalog data for profile selection, UI address pickers, and application-layer checks. They are not a production guarantee that every address can be read or written on a connected PLC.
"""


SLMP_PROFILE_REFERENCE_INDEX = """# SLMP Profile Reference

This section is built from the canonical `plc-comm-slmp-profiles` data repository during the documentation build.

Use it when you need to compare MELSEC SLMP profiles across the supported built-in Ethernet and Ethernet unit profiles.

For normal library usage, select the PLC profile in the library or Node-RED connection settings and follow that library's getting started guide.

For PLC-side Binary data code, port/open settings, and RUN-time write permission, use the [MELSEC SLMP PLC Setup Guide](../../plc-setup/index.md).

## Pages

| Page | Use it for |
| --- | --- |
| [Parameters](parameters.md) | Compare frame defaults, feature decisions, point limits, write policy, and device availability across profiles. |
| [Device ranges](device-ranges.md) | Check SD-derived range rules, fixed ranges, probe markers, and unsupported device families. |

## Scope

The profile data covers CPU built-in Ethernet ports and verified Ethernet unit routes. Base profiles can be used internally for inherited address and device-range behavior even when they are not selectable connection profiles.

Device range rules are not send/receive address guards for communication libraries. They are for applications that need to discover or display the valid device range of a selected PLC profile.
"""


SLMP_API_PARITY = """# SLMP API Parity

This page summarizes the user-facing SLMP operation surface across the maintained implementations. It is a navigation aid, not a live verification record.

Legend:

- `yes`: implemented in the public low-level/client library surface.
- `gap`: intentionally not implemented in that library today; the note explains the current boundary.
- `n/a`: not a normal target for that implementation's scope.

## Five-Implementation Snapshot

Snapshot date: 2026-07-06.

| Operation family | Python | .NET | C++ minimal | Rust | Node-RED |
| --- | --- | --- | --- | --- | --- |
| Direct word/bit read/write | yes: `read_devices` / `write_devices` | yes: `ReadWordsRawAsync` / `WriteWordsAsync` / bit variants | yes: `readWords` / `writeWords` / bit variants | yes: `read_words_raw` / `write_words` / bit variants | yes: `readDevices` / `writeDevices` |
| Dword / float32 helpers | yes | yes | yes | yes | gap: use word/dword random and typed high-level helpers |
| Extended direct word/bit read/write | yes: `read_devices_ext` / `write_devices_ext` | yes: `ReadWordsExtendedAsync` / `WriteWordsExtendedAsync` / bit variants | yes: module-buffer and link-direct helpers | yes: `read_words_extended` / `write_words_extended` / bit variants | gap: low-level surface currently exposes extended random only |
| Random read | yes: `read_random` | yes: `ReadRandomAsync` | yes: `readRandom` | yes: `read_random` | yes: `readRandom` |
| Extended random read | yes: `read_random_ext` | yes: `ReadRandomExtAsync` | yes: `readRandomExt` | yes: `read_random_ext` | yes: `readRandomExt` |
| Random word/dword write | yes: `write_random_words` | yes: `WriteRandomWordsAsync` | yes: `writeRandomWords` | yes: `write_random_words` | yes: `writeRandomWords` |
| Extended random word/dword write | yes: `write_random_words_ext` | yes: `WriteRandomWordsExtAsync` | yes: `writeRandomWordsExt` | yes: `write_random_words_ext` | yes: `writeRandomWordsExt` |
| Random bit write | yes: `write_random_bits` | yes: `WriteRandomBitsAsync` | yes: `writeRandomBits` | yes: `write_random_bits` | yes: `writeRandomBits` |
| Extended random bit write | yes: `write_random_bits_ext` | yes: `WriteRandomBitsExtAsync` | yes: `writeRandomBitsExt` | yes: `write_random_bits_ext` | yes: `writeRandomBitsExt` |
| Block read/write | yes: `read_block` / `write_block` | yes: `ReadBlockAsync` / `WriteBlockAsync` | yes: `readBlock` / `writeBlock` | yes: `read_block` / `write_block` | yes: `readBlock` / `writeBlock` |
| Type name | yes: `read_type_name` | yes: `ReadTypeNameAsync` | yes: `readTypeName` | yes: `read_type_name` | yes: `readTypeName` |
| Monitor register/cycle | yes | yes | yes | gap: typed monitor API is backlog | gap: low-level client has no monitor-register API yet |
| Memory read/write words | yes | yes | gap: minimal client does not expose memory commands | yes | yes |
| Extend-unit read/write words | yes | yes | gap: minimal client uses extended-device helpers instead | yes | yes |
| CPU-buffer convenience helpers | yes | yes | gap: use module-buffer helpers | gap: use extended-device `HG` access where supported | gap: use lower-level primitives where available |
| Label array read/write | yes | yes | yes | yes | yes |
| Label random read/write | yes | yes | yes | yes | yes |
| Remote CPU control | yes | yes | yes | yes | yes |
| Remote password lock/unlock | yes | yes | yes | yes | yes |

Rust and Node-RED both expose the extended random APIs added in the 2026-07-06 parity pass. Node-RED editor nodes do not need to surface every low-level JavaScript API; this table tracks the JavaScript client surface used by the nodes.

## Out-of-Scope Node Functions

SLMP node-function commands in the `0x0E3x` family, including NodeSearch,
IPAddressSet, ParameterGet/Set, StatusRead, and CommunicationSettingGet, are
outside the maintained library surfaces. These libraries target MELSEC CPU
SLMP server communication for PLC data access and setup-compatible operation;
they do not implement a node-function server-management surface. NodeSearch
and IPAddressSet are also send-prohibited by project policy because they can
discover or alter network identity outside normal PLC data access workflows.

See the [SLMP Troubleshooting & Codes guide](../plc-setup/slmp/troubleshooting-codes.md#node-function-end-codes)
for the related node-function end-code category.
"""


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


SLMP_PYTHON_API_OPERATION_INDEX = """## Operation Index

The sync `SlmpClient` and async `AsyncSlmpClient` expose the same low-level
operation names unless noted otherwise.

### Direct And Random Device Operations

| Operation | Public API |
| --- | --- |
| Direct device read/write | `read_devices`, `write_devices` |
| 32-bit values | `read_dword`, `write_dword`, `read_dwords`, `write_dwords` |
| Float32 values | `read_float32`, `write_float32`, `read_float32s`, `write_float32s` |
| Extended direct device read/write | `read_devices_ext`, `write_devices_ext` |
| Random read | `read_random` |
| Extended random read | `read_random_ext` |
| Random word/dword write | `write_random_words` |
| Extended random word/dword write | `write_random_words_ext` |
| Random bit write | `write_random_bits` |
| Extended random bit write | `write_random_bits_ext` |
| Block read/write | `read_block`, `write_block` |
| Type name | `read_type_name` |

Extended random APIs use the 008x subcommands. Use qualified device notation
such as `U1\\G0`, `U3E0\\HG0`, or `J2\\SW10` where the route requires it.

### Specialized Operations

| Operation | Public API |
| --- | --- |
| Monitor registration/cycle | `register_monitor_devices`, `register_monitor_devices_ext`, `run_monitor_cycle` |
| Memory command words | `memory_read_words`, `memory_write_words` |
| Extend-unit command words | `extend_unit_read_words`, `extend_unit_write_words` |
| CPU-buffer convenience words | `cpu_buffer_read_words`, `cpu_buffer_write_words` |
| Label array access | `read_array_labels`, `write_array_labels` |
| Label random access | `read_random_labels`, `write_random_labels` |
| Remote CPU control | `remote_run`, `remote_stop`, `remote_pause`, `remote_latch_clear`, `remote_reset` |
| Remote password | `remote_password_unlock`, `remote_password_lock` |

### High-Level Helpers

| Operation | Public API |
| --- | --- |
| Connection helper | `open_and_connect`, `open_and_connect_sync`, `QueuedAsyncSlmpClient` |
| Typed values | `read_typed`, `write_typed` |
| Named mixed snapshots | `read_named`, `write_named`, `poll` |
| Chunked word/dword reads | `read_words_single_request`, `read_words_chunked`, `read_dwords_single_request`, `read_dwords_chunked` |
| Address handling | `normalize_address`, `parse_address`, `try_parse_address`, `format_address` |
| Bit-in-word write | `write_bit_in_word` |
"""


SLMP_TROUBLESHOOTING_END_CODES = """# SLMP Troubleshooting & Codes

This page summarizes situations observed during this project's live PLC verification and common SLMP setup issues. It is not the official definition of every SLMP end code. Use the Mitsubishi manuals for formal definitions and complete code tables.

## First Checks

Before chasing one code, confirm these basics:

- The application selected the correct canonical PLC profile.
- The PLC Ethernet port uses Binary SLMP data code; see the [MELSEC SLMP PLC Setup Guide](../index.md).
- PLC-side RUN-time write permission is enabled before write tests where the PLC exposes that setting.
- Strict profile mode is enabled unless you intentionally want to send unsupported commands and let the PLC answer.
- Point counts are within the selected profile limits.
- Routed devices such as `Un\\Gn`, `Jn\\...`, and `U3En\\G` exist in the actual PLC configuration.

## Common Symptoms

| Symptom | Likely cause | First check |
| --- | --- | --- |
| The connection opens, but every request returns an end code. | The selected PLC profile does not match the PLC, or the PLC Ethernet port data-code setting does not match the library request format. | Select the canonical profile for the connected PLC and confirm Binary SLMP is configured on the PLC-side port. |
| Reads work, but writes fail. | PLC-side RUN-time write permission, remote password state, or profile write policy blocks the write. | Check RUN-time write permission, remote password state, and the selected profile's write policy. |
| A large read, write, random request, or monitor request fails with `C051`, `C052`, `C053`, or `C054`. | The request exceeds the selected profile's per-request point limit. | Split the request and check the shared profile parameter table for the active PLC. |
| One write request mixes word devices and bit devices and fails. | Some PLC paths reject mixed word and bit block writes. | Send word writes and bit writes as separate requests. |
| `X`/`Y` points look shifted, or `DX`/`DY` is rejected on iQ-F. | iQ-F uses octal text for `X`/`Y`, and the iQ-F profile does not support `DX`/`DY`. | Use the iQ-F profile and use `X` / `Y` rather than `DX` / `DY` on iQ-F. |
| `D50.D` reads bit 13 instead of a 32-bit value. | Dot notation means bit-in-word access; `D` after the dot is hexadecimal bit index 13. | Use the library's typed form such as `D50:D` for unsigned 32-bit data. |
| `D50.3,8` or a similar bit-in-word count is rejected. | Dot notation selects one bit inside one word and is scalar-only. | Use `D50.3` for one bit, or use a direct bit family such as `M1000:BIT,8` for consecutive bit devices. |
| `LTN`, `LSTN`, `LCN`, or `LZ` looks truncated or shifted. | These current-value families are 32-bit values. | Use the library's 32-bit form, such as `:D` or `:L` in named addresses. |
| `LCS` or `LCC` behaves unlike a word value. | Long counter state devices are bit devices. | Read or write them as bit values. |
| Block commands fail on Q/L built-in profiles. | Some Q/L built-in Ethernet profiles do not use block commands for normal high-level access. | Use normal direct/random read and write helpers. Disable strict profile only for deliberate compatibility investigation. |

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
| `C200`, `C201`, `C204` | Access is refused after the network path is established. | Remote password state prevents the operation. | Release the remote password and check whether another device owns the unlock state. |
| `4030`, `4031` | The PLC reports a CPU-side device name or device number error. | Invalid device family, invalid device number, or nonexistent routed path. | Re-check the device notation and PLC configuration. Treat other 4000-series CPU errors as manual lookup items. |

## Node-Function End Codes

The codes below are SLMP node-function responses from the Mitsubishi manuals.
They are included here so operators can recognize them, but the maintained
libraries do not implement the `0x0E3x` node-function command family. For that
scope decision, see [SLMP API Parity](../../slmp/api-parity.md#out-of-scope-node-functions).

| End code | Meaning | Practical check |
| --- | --- | --- |
| `CEE0` | Node-function command is already executing. | Wait for the current node-function operation to finish before retrying from a tool that supports that command family. |
| `CEE1` | Node-function request data size is invalid. | Check the command's required request length in the Mitsubishi manual. |
| `CEE2` | Node-function response data size is invalid. | Check whether the requester expected the correct response length for that command. |
| `CF10` | Server number does not exist. | Check the target server number before using node-function tooling. |
| `CF20` | Communication settings cannot be changed. | Do not attempt communication-setting changes from these libraries; use supported engineering tools and controlled setup procedures. |
| `CF30` | Parameter ID does not exist. | Check the parameter ID against the Mitsubishi manual for the target. |
| `CF31` | Parameter cannot be set. | Check whether the parameter is read-only, target-dependent, or restricted by the current configuration. |

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


KV_HOSTLINK_ERROR_CODES = """# KV Host Link Troubleshooting & Codes

This page summarizes common KEYENCE KV Host Link PLC errors for the PLC setup guide. It is not a complete manufacturer code table; use the KEYENCE manuals for formal definitions.

## PLC Codes

| Code | Typical cause | First check |
| --- | --- | --- |
| `E0` | Device number is invalid, outside range, or not available on the selected PLC model. | Check the address and selected canonical profile. |
| `E1` | Command is not supported by the selected PLC/model. Timer/counter preset writes are a common case on unsupported models. | Check the model profile and avoid unsupported write helpers. |
| `E2` | Program is not registered. | Check the PLC project/program state. |
| `E4` | Write is disabled by CPU protection, lock state, or project settings. | Check KV Studio and CPU write-protection settings. |
| `E5` | Unit error. | Check the PLC/unit error state. |
| `E6` | Comment data is not registered. | Check comment registration before using comment reads. |

## Common Symptoms

| Symptom | Likely cause | First check |
| --- | --- | --- |
| The connection times out immediately. | KV Host Link normally uses port `8501`, not the SLMP/Computerlink example port `1025`. | Confirm the port in the library options or Node-RED connection node. |
| A timer or counter preset write returns `E1`. | Host Link preset writes through `WS` / `WSS` are supported on KV-8000/7000-series, not on every KV model. | Do not write timer/counter presets on unsupported models; use timer/counter read helpers for monitoring. |
| `AT` is rejected or missing on KV-X500. | `AT` is not available in `keyence:kv-x500` or `keyence:kv-x500-xym`. | Check the selected profile before using `AT`. |
| `X` or `Y` is rejected or points look shifted. | `X` and `Y` use decimal-bank plus hexadecimal-bit notation, for example `X10F`. | Use the correct bank/bit notation and select an `-xym` profile when using XYM aliases. |
| `R`, `MR`, `LR`, or `CR` is rejected. | These bit-bank families use two-digit bit notation rather than one plain hexadecimal number. | Use forms such as `R200:BIT` or `MR100:BIT`. |
| `DM100.D` reads a bit instead of a 32-bit value. | Dot notation means bit-in-word access; `D` after the dot is bit 13. | Use the library's typed form such as `DM100:D` for unsigned 32-bit data. |
| `DM100.3,4` or a similar bit-in-word count is rejected. | Dot notation selects one bit inside one word and is scalar-only. | Use `DM100.3` for one bit, or use a direct bit family such as `R200:BIT,4` for bit arrays. |
| A write to `DM100:COMMENT` is rejected. | Device comments are read-only through the high-level Host Link helpers. | Use `:COMMENT` only with read helpers. |
| Expansion unit buffer access fails. | The selected unit number, buffer address, data format, or mounted module may not match the connected PLC hardware. | Verify the expansion unit number and buffer address before using expansion buffer helpers. |
| `CTH` or `CTC` appears in a catalog but fails as an input address. | `CTH` and `CTC` are catalog metadata rows for supported profiles. | Treat them as catalog metadata only. |
| A non-canonical profile string is rejected. | The profile catalog accepts exact canonical profile strings only. | Copy the exact profile string from the profile list or setup guide. |

## First Checks

- Confirm that Host Link / Upper Link communication is enabled on the PLC.
- Confirm the port number, protocol, and IP settings in the [KV PLC setup pages](../index.md).
- Confirm that the application selected the canonical profile for the actual PLC model.
- For write errors, check CPU protection, lock state, project settings, and RUN-time write permission where applicable.
"""


KV_HOSTLINK_DEVICE_RANGES = """# KV Host Link Device Ranges

This page is the shared device-family, address-notation, and range reference for the KV Host Link libraries.

These tables are for profile selection, UI address pickers, model-specific display, and pre-checks in applications that need a range catalog. They are not a guarantee that every address can be read or written on every connected PLC. The actual PLC model, project settings, mounted units, protection settings, and Host Link command support can still reject a request.

## Device Families

### Word device families

| Family | Notation | Example | Notes |
| --- | --- | --- | --- |
| `DM` | Decimal | `DM0:U` | General data memory. Start here for first reads. |
| `EM` | Decimal | `EM0:U` | Extended data memory on profiles that provide EM ranges. |
| `FM` | Decimal | `FM0:U` | File memory on profiles that provide FM ranges. |
| `ZF` | Decimal | `ZF0:U` | File register area on profiles that provide ZF ranges. |
| `W` | Hexadecimal | `W0:U` | Link register word area. |
| `CM` | Decimal | `CM0:U` | Control memory word area. |
| `TM` | Decimal | `TM0:U` | Timer-related word area. |
| `VM` | Decimal | `VM0:U` | Variable memory word area; not available on KV-X500 profiles. |
| `D` | Decimal | `D0:U` | XYM-style alias for `DM`. |
| `E` | Decimal | `E0:U` | XYM-style alias for `EM`. |
| `F` | Decimal | `F0:U` | XYM-style alias for `FM`. |
| `Z` | Decimal | `Z1:D` | Index registers. KV-X500 profiles expose `Z1` through `Z10`; other profiles expose `Z1` through `Z12`. |

### Bit device families

| Family | Notation | Example | Notes |
| --- | --- | --- | --- |
| `R` | Decimal bank plus two decimal bit digits | `R200:BIT` | Relay bits. Low two digits are bit `00` through `15`. |
| `B` | Hexadecimal | `B0000:BIT` | Link relay bits. |
| `MR` | Decimal bank plus two decimal bit digits | `MR100:BIT` | Internal relay bits. |
| `LR` | Decimal bank plus two decimal bit digits | `LR100:BIT` | Latch relay bits. |
| `CR` | Decimal bank plus two decimal bit digits | `CR100:BIT` | Control relay bits. |
| `VB` | Hexadecimal | `VB0:BIT` | Variable memory bits; not available on KV-X500 profiles. |
| `X` | Decimal bank plus hex bit | `X10F:BIT` | Input alias in XYM profiles. |
| `Y` | Decimal bank plus hex bit | `Y10F:BIT` | Output alias in XYM profiles. |
| `M` | Decimal | `M0:BIT` | Internal relay alias in XYM profiles. |
| `L` | Decimal | `L0:BIT` | Latch relay alias in XYM profiles. |

### Timer, counter, and catalog rows

| Family | Category | Example | Notes |
| --- | --- | --- | --- |
| `T` | Timer | `T0:D` | Timer preset/current composite in high-level helpers. |
| `TC` | Timer | `TC0:D` | Timer current/contact family where exposed by the library. |
| `TS` | Timer | `TS0:BIT` | Timer contact/status family where exposed by the library. |
| `C` | Counter | `C0:D` | Counter preset/current composite in high-level helpers. |
| `CC` | Counter | `CC0:D` | Counter current/contact family where exposed by the library. |
| `CS` | Counter | `CS0:BIT` | Counter contact/status family where exposed by the library. |
| `AT` | Timer/counter catalog category | `AT0:D` | Digital trimmer. Not available on KV-NANO or KV-X500 profiles. |
| `CTH` | Catalog metadata | `CTH0` | High-speed counter row on some profiles. Catalog entry only; not accepted by high-level address parsers. |
| `CTC` | Catalog metadata | `CTC0` | High-speed counter row on some profiles. Catalog entry only; not accepted by high-level address parsers. |

## Type Suffixes

| Form | Example | Meaning |
| --- | --- | --- |
| `:U` | `DM100:U` | Unsigned 16-bit word. |
| `:S` | `DM100:S` | Signed 16-bit word. |
| `:D` | `DM100:D` | Unsigned 32-bit double word. |
| `:L` | `DM100:L` | Signed 32-bit double word. |
| `:F` | `DM100:F` | IEEE 754 32-bit floating-point value. |
| `:H` | `DM100:H` | Hexadecimal 16-bit word text. |
| `:BIT` | `R200:BIT` | Direct bit device value. |
| `:COMMENT` | `DM100:COMMENT` | PLC device comment text. |
| `.n` | `DM100.A` | Bit `n` inside a word, where `n` is hexadecimal `0` through `F`. |

High-level address text should include the intended type. Use `DM100:U`, not plain `DM100`, when reading an unsigned word.

## Addressing Notes

| Topic | Rule |
| --- | --- |
| `X` and `Y` notation | Use decimal bank digits followed by one hexadecimal bit digit, such as `X10F`. Do not treat the whole value as one decimal number. |
| `R`, `MR`, `LR`, and `CR` notation | Use two decimal bit digits for the low bit position, such as `R200:BIT`, `MR115:BIT`, or `CR7915:BIT`. The low two digits must be `00` through `15`. |
| `AT` restriction | `AT` exists only on KV-3000, KV-5000, KV-7000, and KV-8000 catalog profiles. High-level write helpers can reject it before sending. |
| Catalog-only rows | `CTH` and `CTC` appear in some range catalogs but are not accepted as high-level address input. |
| Default port | KV Host Link commonly uses port `8501` unless the PLC configuration says otherwise. |

## Standard Catalog

| DeviceType | Base | KV-NANO | KV-3000 | KV-5000 | KV-7000 | KV-8000 | KV-X500 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R | 10 | R00000-R59915 | R00000-R99915 | R00000-R99915 | R00000-R199915 | R00000-R199915 | R00000-R199915 |
| B | 16 | B0000-B1FFF | B0000-B3FFF | B0000-B3FFF | B0000-B7FFF | B0000-B7FFF | B0000-B7FFF |
| MR | 10 | MR00000-MR59915 | MR00000-MR99915 | MR00000-MR99915 | MR000000-MR399915 | MR000000-MR399915 | MR000000-MR399915 |
| LR | 10 | LR00000-LR19915 | LR00000-LR99915 | LR00000-LR99915 | LR00000-LR99915 | LR00000-LR99915 | LR00000-LR99915 |
| CR | 10 | CR0000-CR8915 | CR0000-CR3915 | CR0000-CR3915 | CR0000-CR7915 | CR0000-CR7915 | CR0000-CR7915 |
| CM | 10 | CM0000-CM8999 | CM0000-CM5999 | CM0000-CM5999 | CM0000-CM5999 | CM0000-CM7599 | CM0000-CM7599 |
| T | 10 | T0000-T0511 | T0000-T3999 | T0000-T3999 | T0000-T3999 | T0000-T3999 | T0000-T3999 |
| C | 10 | C0000-C0255 | C0000-C3999 | C0000-C3999 | C0000-C3999 | C0000-C3999 | C0000-C3999 |
| DM | 10 | DM00000-DM32767 | DM00000-DM65534 | DM00000-DM65534 | DM00000-DM65534 | DM00000-DM65534 | DM00000-DM65534 |
| EM | 10 | - | EM00000-EM65534 | EM00000-EM65534 | EM00000-EM65534 | EM00000-EM65534 | EM00000-EM65534 |
| FM | 10 | - | FM00000-FM32767 | FM00000-FM32767 | FM00000-FM32767 | FM00000-FM32767 | FM00000-FM32767 |
| ZF | 10 | - | ZF000000-ZF131071 | ZF000000-ZF131071 | ZF000000-ZF524287 | ZF000000-ZF524287 | ZF000000-ZF524287 |
| W | 16 | W0000-W3FFF | W0000-W3FFF | W0000-W3FFF | W0000-W7FFF | W0000-W7FFF | W0000-W7FFF |
| TM | 10 | TM000-TM511 | TM000-TM511 | TM000-TM511 | TM000-TM511 | TM000-TM511 | TM000-TM511 |
| VM | 10 | VM0-9999 | VM0-59999 | VM0-59999 | VM0-63999 | VM0-589823 | - |
| VB | 16 | VB0-1FFF | VB0-3FFF | VB0-3FFF | VB0-F9FF | VB0-F9FF | - |
| Z | 10 | Z1-12 | Z1-12 | Z1-12 | Z1-12 | Z1-23 | Z1-10 |
| CTH | 10 | CTH0-3 | CTH0-1 | CTH0-1 | - | - | - |
| CTC | 10 | CTC0-7 | CTC0-3 | CTC0-3 | - | - | - |
| AT | 10 | - | AT0-7 | AT0-7 | AT0-7 | AT0-7 | - |

## XYM Catalog

| DeviceType | Base | KV-NANO(XYM) | KV-3000(XYM) | KV-5000(XYM) | KV-7000(XYM) | KV-8000(XYM) | KV-X500(XYM) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R | 10 | X0-599F,Y0-599F | X0-999F,Y0-999F | X0-999F,Y0-999F | X0-1999F,Y0-1999F | X0-1999F,Y0-1999F | X0-1999F,Y0-1999F |
| B | 16 | B0000-B1FFF | B0000-B3FFF | B0000-B3FFF | B0000-B7FFF | B0000-B7FFF | B0000-B7FFF |
| MR | 10 | M0-9599 | M0-15999 | M0-15999 | M000000-M63999 | M000000-M63999 | M000000-M63999 |
| LR | 10 | L0-3199 | L0-15999 | L0-15999 | L00000-L15999 | L00000-L15999 | L00000-L15999 |
| CR | 10 | CR0000-CR8915 | CR0000-CR3915 | CR0000-CR3915 | CR0000-CR7915 | CR0000-CR7915 | CR0000-CR7915 |
| CM | 10 | CM0000-CM8999 | CM0000-CM5999 | CM0000-CM5999 | CM0000-CM5999 | CM0000-CM7599 | CM0000-CM7599 |
| T | 10 | T0000-T0511 | T0000-T3999 | T0000-T3999 | T0000-T3999 | T0000-T3999 | T0000-T3999 |
| C | 10 | C0000-C0255 | C0000-C3999 | C0000-C3999 | C0000-C3999 | C0000-C3999 | C0000-C3999 |
| DM | 10 | D0-32767 | D0-65534 | D0-65534 | D00000-D65534 | D00000-D65534 | D00000-D65534 |
| EM | 10 | - | E0-65534 | E0-65534 | E00000-E65534 | E00000-E65534 | E00000-E65534 |
| FM | 10 | - | F0-32767 | F0-32767 | F00000-F32767 | F00000-F32767 | F00000-F32767 |
| ZF | 10 | - | ZF000000-ZF131071 | ZF000000-ZF131071 | ZF000000-ZF524287 | ZF000000-ZF524287 | ZF000000-ZF524287 |
| W | 16 | W0000-W3FFF | W0000-W3FFF | W0000-W3FFF | W0000-W7FFF | W0000-W7FFF | W0000-W7FFF |
| TM | 10 | TM000-TM511 | TM000-TM511 | TM000-TM511 | TM000-TM511 | TM000-TM511 | TM000-TM511 |
| VM | 10 | VM0-9999 | VM0-59999 | VM0-59999 | VM0-63999 | VM0-589823 | - |
| VB | 16 | VB0-1FFF | VB0-3FFF | VB0-3FFF | VB0-F9FF | VB0-F9FF | - |
| Z | 10 | Z1-12 | Z1-12 | Z1-12 | Z1-12 | Z1-23 | Z1-10 |
| CTH | 10 | CTH0-3 | CTH0-1 | CTH0-1 | - | - | - |
| CTC | 10 | CTC0-7 | CTC0-3 | CTC0-3 | - | - | - |
| AT | 10 | - | AT0-7 | AT0-7 | AT0-7 | AT0-7 | - |
"""


COMPUTERLINK_ERROR_CODES = """# Computerlink Troubleshooting & Codes

This page summarizes TOYOPUC Computerlink response errors that users commonly see. It is not a complete manufacturer code table; use the JTEKT TOYOPUC manuals for formal definitions.

## First Checks

- Confirm that Computerlink communication is enabled on the PLC side.
- Confirm the TCP/UDP port and network settings in the [TOYOPUC setup page](toyopuc.md).
- Confirm that the application selected the exact canonical TOYOPUC profile.
- For write errors, check PLC run/write permission and protection settings before retrying.
- For relay access, configure the relay hops explicitly; relay topology is not auto-discovered.

## Connection Checks

| Symptom | First check |
| --- | --- |
| Connection timeout | Confirm the PLC host address and the configured Computerlink port. TCP examples use `1025`. |
| TCP connection refused | Confirm Computerlink is enabled on the target PLC and the TCP port is open. |
| UDP requests do not return | Confirm the UDP port configured for the target PLC. |
| Intermittent timeouts | Increase timeout/retry settings, reuse a connection, and avoid reconnecting for every small request. |

## Addressing Checks

| Symptom | First check |
| --- | --- |
| Profile rejected before communication | Use one exact canonical profile from the library's PLC Profiles page. |
| Unknown device area | Confirm that the selected profile supports that family. |
| Address out of range | Compare the selected profile with the shared [Computerlink Device Ranges](device-ranges.md) page. |
| Basic address rejected | Use `P1-`, `P2-`, or `P3-` for basic families such as `D`, `M`, `X`, `Y`, `T`, `C`, `L`, `N`, `R`, and `S`. |
| Dword read returns a bit | Use `:D` for dword access and `.D` only for bit 13 inside a word. |

## Write Checks

| Symptom | First check |
| --- | --- |
| A write appears to change the wrong value | Stop and confirm that you are using a test address you control. |
| FR value does not survive power cycle | Stage the FR write and then commit it when persistence is intended. |
| Relay write or read does not reach the target PLC | Set the relay hop string explicitly. |

## Common PLC Codes

| Code | Typical cause | First check |
| --- | --- | --- |
| `0x40` | Address or address plus count is outside the CPU range. This is also the common result when FR is not exposed on the tested unit. | Check the selected profile, address range, and count. |
| `0x24` | Subcommand is not supported by the CPU or routed target. | Check whether the feature exists on that CPU; for example some targets reject `A0`. |
| `0x23` | Command code is not supported. | Check the selected helper and profile. |
| `0x31` | Write or function call is prohibited while the sequence is running. | Check PLC run/write settings before retrying. |
| `0x34` | Access is prohibited by configuration. | Check PLC communication and protection settings. |
| `0x41` | Word or byte count is outside the permitted range. | Split the request or reduce the count. |
| `0x52` | Timer/counter set-value and current-value command type do not match. | Check whether the helper targets a preset or current value. |
| `0x66`, `0x70`, `0x72` | Relay link module did not answer or could not execute the request. | Check relay hops and the target PLC path. |
| `0x73` | Relay command collision on the same link module; retry is appropriate. | Retry after a short delay or reduce concurrent relay access. |
| `0x11` | CPU module hardware failure. | Check the PLC CPU status before continuing. |
"""


COMPUTERLINK_DEVICE_RANGES = """# Computerlink Device Ranges

This page is the shared device-family, address-notation, and practical range reference for the TOYOPUC Computerlink libraries.

These tables are for profile selection, UI address pickers, model-specific display, and pre-checks in applications that need a range catalog. They are not a guarantee that every address can be read or written on every connected PLC. The actual PLC model, link route, project settings, and run/write permission can still reject a request.

## Device Families

### Bit device families

| Family | Access | Example | Notes |
| --- | --- | --- | --- |
| `P` | Prefixed | `P1-P0000` | Shared relay family; profile ranges may include upper split ranges. |
| `K` | Prefixed | `P1-K0000` | Keep relay family. |
| `V` | Prefixed | `P1-V0000` | Profile-dependent split ranges. |
| `T` | Prefixed | `P1-T0000` | Timer bit family. |
| `C` | Prefixed | `P1-C0000` | Counter bit family. |
| `L` | Prefixed | `P1-L0000` | Link relay family; profile ranges may include upper split ranges. |
| `X` | Prefixed | `P1-X0000` | Input relay family. |
| `Y` | Prefixed | `P1-Y0000` | Output relay family. |
| `M` | Prefixed | `P1-M0000` | Internal relay family; profile ranges may include upper split ranges. |
| `EP` | Direct extension | `EP0000` | Extended P bit family. |
| `EK` | Direct extension | `EK0000` | Extended K bit family. |
| `EV` | Direct extension | `EV0000` | Extended V bit family. |
| `ET` | Direct extension | `ET0000` | Extended T bit family. |
| `EC` | Direct extension | `EC0000` | Extended C bit family. |
| `EL` | Direct extension | `EL0000` | Extended L bit family. |
| `EX` | Direct extension | `EX0000` | Extended X bit family. |
| `EY` | Direct extension | `EY0000` | Extended Y bit family. |
| `EM` | Direct extension | `EM0000` | Extended M bit family. |
| `GM` | Direct extension | `GM0000` | Global M bit family where the selected profile enables it. |
| `GX` | Direct extension | `GX0000` | Global X bit family where the selected profile enables it. |
| `GY` | Direct extension | `GY0000` | Global Y bit family where the selected profile enables it. |

### Word device families

| Family | Access | Example | Notes |
| --- | --- | --- | --- |
| `S` | Prefixed | `P1-S0000` | Special register family. |
| `N` | Prefixed | `P1-N0000` | File register word family. |
| `R` | Prefixed | `P1-R0000` | Register word family. |
| `D` | Prefixed | `P1-D0000` | Data register family. |
| `B` | Direct | `B0000` | Direct word area where the selected profile enables it. |
| `ES` | Direct extension | `ES0000` | Extended special register family. |
| `EN` | Direct extension | `EN0000` | Extended file register family. |
| `H` | Direct extension | `H0000` | Extended H word family. |
| `U` | Direct extension | `U00000` | Profile and addressing options select standard or PC10 routing. |
| `EB` | Direct extension | `EB00000` | Extended block word family where the selected profile enables it. |
| `FR` | Direct FR | `FR000000` | File-register flash area with two-phase write semantics. |

## Type Suffixes

| Form | Example | Meaning |
| --- | --- | --- |
| No suffix or `:U` | `P1-D0100` | Unsigned 16-bit word. |
| `:S` | `P1-D0100:S` | Signed 16-bit word. |
| `:D` | `P1-D0100:D` | Unsigned 32-bit dword from two words. |
| `:L` | `P1-D0100:L` | Signed 32-bit long from two words. |
| `:F` | `P1-D0100:F` | IEEE 754 32-bit floating point value from two words. |
| `.n` | `P1-D0100.3` | Bit `n` inside a word, where `n` is hexadecimal `0` through `F`. |
| `W` | `P1-M0010W` | 16-bit packed view of a bit family. |
| `L` / `H` | `P1-M0010L` | Low or high byte view of a bit family. |

## Addressing Rules

| Rule | Correct form |
| --- | --- |
| Basic families require a program prefix. | `P1-D0000`, `P2-M0000`, `P3-S0000` |
| Extension families are direct. | `ES0000`, `EP0000`, `U00000`, `FR000000` |
| Data type views use a colon. | `P1-D0100:D` |
| Bit-in-word views use a dot. | `P1-D0100.D` means bit 13. |
| Packed bit-area views append the packed unit. | `P1-M0010W`, `P1-M0010L`, `P1-M0010H` |
| FR writes are explicit. | Stage an FR write, then commit when persistence is intended. |

## Practical Writable Ranges

These are writable-range summaries from project evidence, not a complete hardware manual.

### TOYOPUC-Plus CPU with Plus EX2

| Area | Writable range summary |
| --- | --- |
| Basic bit | `P0000-P17FF`, `K0000-K02FF`, `V/T/C/M0000-17FF`, `L0000-L2FFF`, `X/Y0000-07FF` |
| Basic word | `S0000-S13FF`, `N0000-N17FF`, `R0000-R07FF`, `D0000-D0FFF`; `B` is not writable |
| Prefixed bit | `P1/P2/P3-P000-P1FF`, `K000-K2FF`, `V/T/C000-C1FF`, `L000-L7FF`, `X/Y000-X7FF`, `M000-M7FF` |
| Prefixed word | `P1/P2/P3-S0000-S03FF`, `N0000-N01FF`, `R0000-R07FF`, `D0000-D0FFF`; `B` is not writable |
| Extension bit | `EP/EK/EV0000-0FFF`, `ET/EC/EX/EY0000-07FF`, `EL0000-1FFF`, `EM0000-1FFF`, `GX/GY/GM0000-FFFF` |
| Extension word | `ES/EN/H0000-07FF`, `U00000-U07FFF`; `EB` is not present |
| FR | Not exposed on this CPU |

### Nano 10GX

| Area | Writable range summary |
| --- | --- |
| Basic bit | `P/K/V/T/C/L/X/Y/M` standard ranges |
| Basic word | `S0000-S13FF`, `N0000-N17FF`, `R0000-R07FF`, `D0000-D2FFF`; `B` is not present |
| Prefixed bit | `P1/P2/P3` standard ranges |
| Prefixed word | `S0000-S13FF`, `N0000-N17FF`, `R0000-R07FF`, `D0000-D2FFF`; upper prefixed `1000` series are not implemented |
| Extension | Standard `EP/EK/EV/ET/EC/EL/EX/EY/EM`, `GX/GY/GM`, `ES/EN/H`; `U00000-U1FFFF` in PC10 mode |
| FR | `FR000000-FR1FFFFF` when the CPU/configuration exposes FR |

### PC10G-CPU

| Area | Writable range summary |
| --- | --- |
| Basic bit | `P0000-P17FF`, `K0000-K02FF`, `V/T/C/M0000-17FF`, `L0000-L2FFF`, `X/Y0000-07FF` |
| Basic word | `S0000-S13FF`, `N0000-N17FF`, `R0000-R07FF`, `D0000-D2FFF` |
| Prefixed bit | `P1/P2/P3` standard ranges, including the upper `1000` series on this CPU |
| Prefixed word | `S0000-S13FF`, `N0000-N17FF`, `R0000-R07FF`, `D0000-D2FFF` |
| Extension bit | `EP/EK/EV0000-0FFF`, `ET/EC/EX/EY0000-07FF`, `EL0000-1FFF`, `EM0000-1FFF`, `GX/GY/GM0000-FFFF` |
| Extension word | `ES/EN/H0000-07FF`, `U00000-U1FFFF`, `EB00000-EB3FFFF` |
| FR | Not exposed on the tested PC10G unit |

## Range Notes

- A profile can make an address syntactically valid while the connected PLC still rejects it because of hardware, mode, project configuration, or route.
- FR writes are persistent operations. Use dedicated FR helpers only on test addresses you control.
"""


MCPROTOCOL_SERIAL_ERROR_CODES = """# MC Protocol Serial Troubleshooting & Codes

This page is a practical guide for errors returned by MELSEC serial MC Protocol targets. It is not a complete Mitsubishi error-code table. Use the PLC and serial-module manuals for formal definitions.

## Library Status Categories

The C++ library reports transport and parser failures separately from PLC/module error responses.

| Status category | Typical meaning | First checks |
| --- | --- | --- |
| Timeout | No complete response arrived before the response timeout. | Check wiring, baud rate, parity, stop bits, station number, and whether the PLC module is configured for the same frame type. |
| Framing | Bytes arrived, but they did not match the selected response frame. | Check 1C/2C/3C/4C/1E selection, ASCII format, binary vs ASCII mode, and CR/LF settings. |
| Sum-check mismatch | A response arrived, but its sum-check did not match. | Check whether sum-check is enabled on both sides. If it is, check serial noise and wiring. |
| Parse | The response frame shape was recognized, but a numeric field or payload length could not be decoded. | Capture the raw frame and check whether the selected frame/profile matches the PLC setting. |
| Unsupported configuration | The request cannot be encoded for the selected profile, frame, or build options. | Select an explicit PLC profile, choose a supported frame helper, and check disabled feature macros. |
| PLC/module error | The PLC or serial module returned an error response. | Read the preserved PLC/module error code and use the sections below. |

## PLC and Serial-Module Error Families

Serial MC Protocol uses more than one error-code family. Do not interpret every code as an SLMP Ethernet end code.

| Code family | Where it appears | How to handle it |
| --- | --- | --- |
| CPU-side `4000`-series and related PLC end codes | QnA extended `3C` / `4C` routes when the request reaches the CPU. | Use the [SLMP Troubleshooting & Codes guide](../slmp/troubleshooting-codes.md) for practical checks. |
| `7Fxx` serial-module responses | Serial-module rejection before or around CPU forwarding. | Treat as target/module dependent. Check frame mode, profile, device family, route, and module settings. |
| `1C` NAK codes | Legacy `1C` A-compatible / QnA-compatible frames. | Not yet published as a user table. Record the raw response and target settings; deliberately malformed-request measurements are still a TODO. |
| No response | The module ignores the request or cannot answer in the selected mode. | Treat as a transport/configuration problem first, not as an error code. |

## Observed Codes

Only project-observed cases are listed here. If you see a code not listed here, record the raw response, frame kind, ASCII/binary mode, station, sum-check setting, PLC model, serial module, and selected PLC profile.

| Code | Observed situation | Practical check |
| --- | --- | --- |
| `0x4031` | CPU-side device or route rejection observed on serial paths, for example unsupported link-direct access on a target setup. | Check the selected profile, route notation, mounted module, and whether the requested device family exists on that PLC. |
| `0x7F22` | Serial-module rejection observed for unsupported serial-MC device/command shapes, such as `S` device probes on a C24 path before CPU forwarding. | Do not treat unsupported device families as valid access paths. Recheck the profile support table and the serial-module MC protocol format. |

## Codes Intentionally Not Expanded Yet

The decoder preserves error codes such as two-digit `1C` NAK codes and four-digit QnA serial responses, but this page does not assign meanings to unmeasured codes.

The active TODO is to collect live-device evidence for:

- `1C` NAK codes from deliberately malformed but transmitted requests.
- `3C` / `4C` serial-link `7Fxx` codes from deliberately malformed serial requests.

After those measurements exist, add only observed codes to this page.
"""


MCPROTOCOL_SERIAL_SUPPORTED_REGISTERS = """# MC Protocol Serial Supported Registers

This page lists the current device-family support surface for MELSEC serial MC Protocol targets.

Profile-specific device-number ranges still depend on the PLC model, serial module parameters, route, and user program. The example addresses below show parser syntax; they are not range limits.

## Common Rules

| Rule | Behavior |
| --- | --- |
| Plain device strings | The high-level parser accepts plain device strings such as `D100`, `M100`, `X10`, `W100`, and `LZ0`. |
| Standalone `G` / `HG` | Not plain devices for any profile. Use qualified forms such as `Un\\G` or `Un\\HG` only when the selected profile supports that route. |
| `S` device | Not supported by this serial MC library. |
| Link-direct devices | Use dedicated `Jn\\...` link-direct APIs when the selected profile supports them. |
| Qualified unit access | Use native-qualified `Un\\G` / `Un\\HG` APIs when the selected profile supports that route. The `0601/1601` helper route is profile/target-specific and must not be used as a fallback. |

## Profile Support Summary

### `melsec:iq-r`

| Support class | Device families |
| --- | --- |
| Plain bit read/write | `X`, `Y`, `M`, `L`, `SM`, `F`, `V`, `B`, `TS`, `TC`, `STS`, `STC`, `CS`, `CC`, `SB`, `DX`, `DY` |
| Plain word read/write | `D`, `SD`, `W`, `TN`, `STN`, `CN`, `SW`, `Z`, `R`, `RD`, `ZR` |
| Long-state helper | `LTS`, `LTC`, `LSTS`, `LSTC`, `LCS`, `LCC` |
| Native random double-word read/write | `LTN`, `LSTN`, `LCN`, `LZ` |
| Link-direct read/write | `Jn\\X`, `Jn\\Y`, `Jn\\B`, `Jn\\W`, `Jn\\SB`, `Jn\\SW` |
| Native-qualified read/write | `Un\\G`, `Un\\HG` |
| Not supported | `S` |

### `melsec:iq-l`

| Support class | Device families |
| --- | --- |
| Plain bit read/write | `X`, `Y`, `M`, `L`, `SM`, `F`, `V`, `B`, `TS`, `TC`, `STS`, `STC`, `CS`, `CC`, `SB`, `DX`, `DY` |
| Plain word read/write | `D`, `SD`, `W`, `TN`, `STN`, `CN`, `SW`, `Z`, `R`, `ZR` |
| Native-qualified read/write | `Un\\G` |
| Not supported | `S`, `LTS`, `LTC`, `LSTS`, `LSTC`, `LCS`, `LCC`, `LTN`, `LSTN`, `LCN`, `LZ`, `RD`, `Un\\HG` |
| Not confirmed | `Jn\\X`, `Jn\\Y`, `Jn\\B`, `Jn\\W`, `Jn\\SB`, `Jn\\SW` |

### `melsec:iq-f`

| Support class | Device families |
| --- | --- |
| Plain bit read/write | `X`, `Y`, `M`, `L`, `SM`, `F`, `B`, `TS`, `TC`, `STS`, `STC`, `CS`, `CC`, `SB` |
| Plain word read/write | `D`, `SD`, `W`, `TN`, `STN`, `CN`, `SW`, `Z`, `R` |
| Long counter state read/write | `LCS`, `LCC`; reads use the long-state helper |
| Native random double-word read/write | `LCN`, `LZ` |
| Native-qualified read/write | `Un\\G` |
| Not supported | `S`, `V`, `ZR`, `DX`, `DY`, `LTS`, `LTC`, `LTN`, `LSTS`, `LSTC`, `LSTN`, `Un\\HG`, `Jn\\...`, monitor, host-buffer, and module-buffer helper routes |

### `melsec:qcpu`

| Support class | Device families |
| --- | --- |
| Plain bit read/write | `X`, `Y`, `M`, `L`, `SM`, `F`, `V`, `B`, `TS`, `TC`, `STS`, `STC`, `CS`, `CC`, `SB`, `DX`, `DY` |
| Plain word read/write | `D`, `SD`, `W`, `TN`, `STN`, `CN`, `SW`, `Z`, `R`, `ZR` |
| Link-direct read/write | `Jn\\X`, `Jn\\Y`, `Jn\\B`, `Jn\\W` |
| Link-direct read-only | `Jn\\SB`, `Jn\\SW` |
| Native-qualified read/write | `Un\\G` |
| Not supported | `S`, `LTS`, `LTC`, `LSTS`, `LSTC`, `LCS`, `LCC`, `LTN`, `LSTN`, `LCN`, `LZ`, `RD`, `Un\\HG` |

Native random read on tested Q targets can be narrower than batch access for some timer/counter status families. Treat random-read rejection as a command route limitation, not as a batch-read exclusion.

### `melsec:lcpu`

| Support class | Device families |
| --- | --- |
| Plain bit read/write | `X`, `Y`, `M`, `L`, `SM`, `F`, `V`, `B`, `TS`, `TC`, `STS`, `STC`, `CS`, `CC`, `SB`, `DX`, `DY` |
| Plain word read/write | `D`, `SD`, `W`, `TN`, `STN`, `CN`, `SW`, `Z`, `R`, `ZR` |
| Native-qualified read/write | `Un\\G` |
| Expected but not locally confirmed | `Jn\\X`, `Jn\\Y`, `Jn\\B`, `Jn\\W`, `Jn\\SB`, `Jn\\SW` |
| Not supported | `S`, `LTS`, `LTC`, `LSTS`, `LSTC`, `LCS`, `LCC`, `LTN`, `LSTN`, `LCN`, `LZ`, `RD`, `Un\\HG` |

Native random read on tested L targets can be narrower than batch access for some timer/counter status families. Treat random-read rejection as a command route limitation, not as a batch-read exclusion.

### `melsec:qna`, `melsec:ana-anu`, and `melsec:a`

These profiles select older command families and are maintained by manual-derived inference and codec-level tests until matching hardware is available. Do not promote a device inventory for these profiles without target evidence.

`melsec:a` is required for A-series extended file-register `ER/EW` paths. `melsec:qna` or `melsec:ana-anu` is required for QnA/AnA/AnU command-family paths such as direct extended file-register access.

## Bit Device Families

| Family | Kind | Example address | Notes |
| --- | --- | --- | --- |
| `X` | Input relay | `X10` | Hexadecimal address. |
| `Y` | Output relay | `Y10` | Hexadecimal address. |
| `M` | Internal relay | `M100` | Decimal address. |
| `L` | Latch relay | `L100` | Decimal address. |
| `SM` | Special relay | `SM100` | Decimal address. |
| `F` | Annunciator | `F100` | Decimal address. |
| `V` | Edge relay | `V100` | Decimal address. |
| `B` | Link relay | `B100` | Hexadecimal address. |
| `TS`, `TC` | Timer contact / coil | `TS0` | Decimal address. |
| `STS`, `STC` | Retentive timer contact / coil | `STS0` | Decimal address. |
| `CS`, `CC` | Counter contact / coil | `CS0` | Decimal address. |
| `SB` | Link special relay | `SB100` | Hexadecimal address. |
| `S` | Step relay | `S100` | Not supported by this serial MC library. |
| `DX`, `DY` | Direct access input/output | `DX10` | Hexadecimal address. |
| `LTS`, `LTC` | Long timer contact / coil | `LTS0` | Decimal address; profile-specific helper route. |
| `LSTS`, `LSTC` | Long retentive timer contact / coil | `LSTS0` | Decimal address; profile-specific helper route. |
| `LCS`, `LCC` | Long counter contact / coil | `LCS0` | Decimal address; profile-specific helper route. |

## Word Device Families

| Family | Kind | Example address | Notes |
| --- | --- | --- | --- |
| `D` | Data register | `D100` | Decimal address. |
| `SD` | Special register | `SD100` | Decimal address. |
| `W` | Link register | `W100` | Hexadecimal address. |
| `TN` | Timer current value | `TN0` | Decimal address. |
| `STN` | Retentive timer current value | `STN0` | Decimal address. |
| `CN` | Counter current value | `CN0` | Decimal address. |
| `SW` | Link special register | `SW100` | Hexadecimal address. |
| `LTN` | Long timer current value | `LTN0` | Decimal address; double-word in native random helpers. |
| `LSTN` | Long retentive timer current value | `LSTN0` | Decimal address; double-word in native random helpers. |
| `LCN` | Long counter current value | `LCN0` | Decimal address; double-word in native random helpers. |
| `LZ` | Long index register | `LZ0` | Decimal address; double-word in native random helpers. |
| `Z` | Index register | `Z0` | Decimal address. |
| `R` | File register | `R0` | Decimal address. |
| `RD` | Module access register | `RD0` | Decimal address. |
| `ZR` | File register | `ZR0` | Decimal address. |

## Addressing Notes

| Topic | Current behavior |
| --- | --- |
| Plain device string | Supported for profile-allowed plain devices. |
| Hexadecimal address families | `X`, `Y`, `B`, `W`, `SB`, `SW`, `DX`, and `DY` parse their numeric part as hexadecimal. |
| `:D` / `:F` suffix | Not supported by the current high-level parser. Use typed C++ fields such as `double_word` where available. |
| `.n` bit-in-word suffix | Not supported by the current high-level parser. |
| Long timer/counter state reads | Use `read_long_state_bits()` for supported long-state families. |
| Link-direct access | Use `read_link_direct_*()` / `write_link_direct_*()` helpers for supported `Jn\\...` families. |
| Qualified unit access | Use `read_native_qualified_words()` / `write_native_qualified_words()` for supported `Un\\G` / `Un\\HG` families. |
| Trace logging | Set `MCPROTOCOL_SERIAL_TRACE=1` with the synchronous host client to log MC TX/RX frame bytes. |
"""


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

    write_generated_page(docs_root / "computerlink/profile-reference/index.md", COMPUTERLINK_PROFILE_REFERENCE_INDEX)
    write_generated_page(docs_root / "hostlink/profile-reference/index.md", HOSTLINK_PROFILE_REFERENCE_INDEX)
    write_generated_page(docs_root / "slmp/profile-reference/index.md", SLMP_PROFILE_REFERENCE_INDEX)
    write_generated_page(docs_root / "slmp/api-parity.md", SLMP_API_PARITY)
    write_generated_page(docs_root / "plc-setup/slmp/troubleshooting-codes.md", SLMP_TROUBLESHOOTING_END_CODES)
    write_generated_page(docs_root / "plc-setup/kv/troubleshooting-codes.md", KV_HOSTLINK_ERROR_CODES)
    write_generated_page(docs_root / "plc-setup/kv/device-ranges.md", KV_HOSTLINK_DEVICE_RANGES)
    write_generated_page(docs_root / "plc-setup/computerlink/troubleshooting-codes.md", COMPUTERLINK_ERROR_CODES)
    write_generated_page(docs_root / "plc-setup/computerlink/device-ranges.md", COMPUTERLINK_DEVICE_RANGES)
    write_generated_page(docs_root / "plc-setup/mcprotocol/troubleshooting-codes.md", MCPROTOCOL_SERIAL_ERROR_CODES)
    write_generated_page(docs_root / "plc-setup/mcprotocol/supported-registers.md", MCPROTOCOL_SERIAL_SUPPORTED_REGISTERS)
    for relative_path, title, module_name, package_name in PYTHON_API_REFERENCE_PAGES:
        write_generated_page(docs_root / relative_path, python_api_reference_page(title, module_name, package_name))

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
