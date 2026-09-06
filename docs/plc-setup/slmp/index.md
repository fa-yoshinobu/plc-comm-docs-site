---
description: "PLC-side Ethernet settings for MELSEC SLMP: pick the setup guide for your iQ-R, iQ-F, iQ-L, MX-R, MX-F, QnUDV, QnU, LCPU, or Ethernet communication unit."
---

# MELSEC SLMP — PLC setup

Configure the MELSEC PLC before connecting with any SLMP library. Each guide
below covers one CPU or communication unit down to the parameter screens of the
engineering tool, and ends with a first read using the libraries.

A **power cycle is required** after every parameter change. Pass the canonical
PLC profile explicitly when opening a connection — the libraries do not infer it
from the PLC.

## Choose your model

These guides use TCP port `1025`.

### Built-in Ethernet (CPU module)

| Model | Configuration tool | Canonical profile | Setup guide |
|-------|-------------------|-------------------|-------------|
| iQ-R | GX Works3 | `melsec:iq-r` | [iQ-R settings](iq-r.md) |
| iQ-F | GX Works3 | `melsec:iq-f` | [iQ-F settings](iq-f.md) |
| iQ-L | GX Works3 | `melsec:iq-l` | [iQ-L settings](iq-l.md) |
| MX-R | GX Works3 | `melsec:mx-r` | [MX-R settings](mx-r.md) |
| MX-F | GX Works3 | `melsec:mx-f` | [MX-F settings](mx-f.md) |
| QnUDV | GX Works2 | `melsec:qnudv` | [QnUDV settings](qnudv.md) |
| QnU | GX Works2 | `melsec:qnu` | [QnU settings](qnu.md) |
| LCPU | GX Works2 | `melsec:lcpu` | [LCPU settings](lcpu.md) |

### Ethernet communication unit

| Model | Configuration tool | Canonical profile | Setup guide |
|-------|-------------------|-------------------|-------------|
| RJ71EN71 | GX Works3 | `melsec:iq-r:rj71en71` | [RJ71EN71 settings](rj71en71.md) |
| QJ71E71-100 | GX Works2 | `melsec:qcpu:qj71e71-100`, `melsec:qnu:qj71e71-100`, or `melsec:qnudv:qj71e71-100`, matching the connected CPU generation | [QJ71E71-100 settings](qj71e71-100.md) |
| LJ71E71-100 | GX Works2 | `melsec:lcpu:lj71e71-100` | [LJ71E71-100 settings](lj71e71-100.md) |

## Shared reference pages

These pages apply to every language implementation of SLMP.

| Page | Use it for |
|------|-----------|
| [SLMP Troubleshooting & Codes](troubleshooting-codes.md) | Symptoms, end codes, and profile limit codes seen during live verification. |
| [SLMP profile parameters](../../slmp/profile-reference/parameters.md) | Frame defaults, point limits, write policy, and device availability per profile. |
| [SLMP device ranges](../../slmp/profile-reference/device-ranges.md) | Range rules, fixed ranges, and unsupported device families per profile. |

Simulator connection notes for GX Simulator 3 are on the
[PLC setup guide overview](../index.md#simulator-connection-notes).

## After the PLC is configured

Start from the Getting started page for your language:
[.NET](../../slmp/dotnet/GETTING_STARTED.md) ·
[Python](../../slmp/python/GETTING_STARTED.md) ·
[Rust](../../slmp/rust/GETTING_STARTED.md) ·
[C++ (Arduino/PlatformIO)](../../slmp/cpp/GETTING_STARTED.md) ·
[Node-RED](../../slmp/nodered/GETTING_STARTED.md)

To confirm the settings before writing any code, use
[PLC Scope](../../index.md#try-it-without-writing-code) and keep the first check
read-only.
