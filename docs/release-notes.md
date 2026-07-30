---
description: "Where to follow releases and changelogs for every plc-comm PLC communication library across .NET, Python, Rust, C++, and Node-RED."
---

# Release notes

This project is developed continuously and re-verified against physical PLCs as
device profiles, protocol behavior, and vendor firmware evolve. Each library is
released from its own repository, so the authoritative record of what changed
and when lives there.

Version numbers are deliberately not reproduced on this site. Follow the
**Releases** feed of a repository to be notified of new versions, and read its
**Changelog** for the detailed history.

!!! tip "Watch a repository"

    On GitHub, open a repository and choose **Watch → Custom → Releases** to get
    a notification whenever that library publishes a new version.

## MELSEC SLMP (Ethernet)

| Library | What it is | Follow |
|---------|-----------|--------|
| **plc-comm-slmp-dotnet** | SLMP client for .NET, with async API, PLC model profiles, and typed device access. | [Releases](https://github.com/fa-yoshinobu/plc-comm-slmp-dotnet/releases) · [Changelog](https://github.com/fa-yoshinobu/plc-comm-slmp-dotnet/blob/main/CHANGELOG.md) |
| **plc-comm-slmp-python** | SLMP client for Python, with sync and asyncio clients sharing one profile model. | [Releases](https://github.com/fa-yoshinobu/plc-comm-slmp-python/releases) · [Changelog](https://github.com/fa-yoshinobu/plc-comm-slmp-python/blob/main/CHANGELOG.md) |
| **plc-comm-slmp-rust** | SLMP client crate for Rust, built on Tokio with the same options and profile vocabulary. | [Releases](https://github.com/fa-yoshinobu/plc-comm-slmp-rust/releases) · [Changelog](https://github.com/fa-yoshinobu/plc-comm-slmp-rust/blob/main/CHANGELOG.md) |
| **plc-comm-slmp-cpp-minimal** | Minimal SLMP client for Arduino and PlatformIO targets on constrained microcontrollers. | [Releases](https://github.com/fa-yoshinobu/plc-comm-slmp-cpp-minimal/releases) · [Changelog](https://github.com/fa-yoshinobu/plc-comm-slmp-cpp-minimal/blob/main/CHANGELOG.md) |
| **node-red-contrib-plc-comm-slmp** | Node-RED nodes for SLMP, for wiring PLC reads and writes into flows without code. | [Releases](https://github.com/fa-yoshinobu/node-red-contrib-plc-comm-slmp/releases) · [Changelog](https://github.com/fa-yoshinobu/node-red-contrib-plc-comm-slmp/blob/main/CHANGELOG.md) |

## MC Protocol Serial (MELSEC, RS-232C/RS-485)

| Library | What it is | Follow |
|---------|-----------|--------|
| **plc-comm-mcprotocol-serial-cpp** | MC Protocol serial client for Arduino and PlatformIO, for MELSEC serial communication modules. | [Releases](https://github.com/fa-yoshinobu/plc-comm-mcprotocol-serial-cpp/releases) · [Changelog](https://github.com/fa-yoshinobu/plc-comm-mcprotocol-serial-cpp/blob/main/CHANGELOG.md) |

## KEYENCE KV Host Link (Ethernet)

| Library | What it is | Follow |
|---------|-----------|--------|
| **plc-comm-hostlink-dotnet** | KV Host Link client for .NET, with KV model profiles and device-range validation. | [Releases](https://github.com/fa-yoshinobu/plc-comm-hostlink-dotnet/releases) · [Changelog](https://github.com/fa-yoshinobu/plc-comm-hostlink-dotnet/blob/main/CHANGELOG.md) |
| **plc-comm-hostlink-python** | KV Host Link client for Python, with sync and asyncio clients over one profile model. | [Releases](https://github.com/fa-yoshinobu/plc-comm-hostlink-python/releases) · [Changelog](https://github.com/fa-yoshinobu/plc-comm-hostlink-python/blob/main/CHANGELOG.md) |
| **plc-comm-hostlink-rust** | KV Host Link client crate for Rust, built on Tokio with the shared API vocabulary. | [Releases](https://github.com/fa-yoshinobu/plc-comm-hostlink-rust/releases) · [Changelog](https://github.com/fa-yoshinobu/plc-comm-hostlink-rust/blob/main/CHANGELOG.md) |
| **node-red-contrib-plc-comm-kvhostlink** | Node-RED nodes for KV Host Link, for reading and writing KV devices from flows. | [Releases](https://github.com/fa-yoshinobu/node-red-contrib-plc-comm-kvhostlink/releases) · [Changelog](https://github.com/fa-yoshinobu/node-red-contrib-plc-comm-kvhostlink/blob/main/CHANGELOG.md) |

## JTEKT TOYOPUC Computerlink (Ethernet)

| Library | What it is | Follow |
|---------|-----------|--------|
| **plc-comm-computerlink-dotnet** | Computerlink client for .NET, covering TOYOPUC program areas and relay/register access. | [Releases](https://github.com/fa-yoshinobu/plc-comm-computerlink-dotnet/releases) · [Changelog](https://github.com/fa-yoshinobu/plc-comm-computerlink-dotnet/blob/main/CHANGELOG.md) |
| **plc-comm-computerlink-python** | Computerlink client for Python, with sync and asyncio clients and TOYOPUC profiles. | [Releases](https://github.com/fa-yoshinobu/plc-comm-computerlink-python/releases) · [Changelog](https://github.com/fa-yoshinobu/plc-comm-computerlink-python/blob/main/CHANGELOG.md) |

## Installing a specific version

Install commands and registry pages for every package are collected in the
[Package Matrix](package-matrix.md). Each registry page lists the published
version history for that package.
