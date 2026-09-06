---
title: "MELSEC SLMP communication libraries"
description: "Talk to MELSEC iQ-R, iQ-F, iQ-L, MX, Q, and L series PLCs over Ethernet with SLMP, from .NET, Python, Rust, C++, or Node-RED, with per-model PLC setup guides."
---

# SLMP — MELSEC over Ethernet

SLMP (Seamless Message Protocol) is the protocol a MELSEC CPU speaks on its
built-in Ethernet port or on an Ethernet communication unit. It is the
protocol to use for a MELSEC PLC whenever an Ethernet port is available: it is
faster and easier to wire than a serial module, and every implementation in
this project supports it.

If your MELSEC PLC has no Ethernet port and only a serial communication module,
use [MC Protocol Serial](../mcprotocol/index.md) instead.

| | |
|---|---|
| PLC families | MELSEC iQ-R, iQ-F, iQ-L, MX-R, MX-F, Q series, L series |
| Transport | Ethernet, TCP or UDP |
| Default port | `1025` (TCP), `1035` (UDP) |
| Data code | Binary — set this on the PLC before connecting |

## Pick your language

All five implementations use the same model: pick a connection option set, pick
your PLC profile, then read or write a device by name.

| Language | Install | Start here |
|----------|---------|-----------|
| **Python** | `pip install plc-comm-slmp` | [Getting started](python/GETTING_STARTED.md) |
| **.NET** | `dotnet add package PlcComm.Slmp` | [Getting started](dotnet/GETTING_STARTED.md) |
| **Rust** | `cargo add plc-comm-slmp` | [Getting started](rust/GETTING_STARTED.md) |
| **C++ (Arduino/PlatformIO)** | `fa-yoshinobu/slmp-connect-cpp-minimal` | [Getting started](cpp/GETTING_STARTED.md) |
| **Node-RED** | `@fa_yoshinobu/node-red-contrib-plc-comm-slmp` | [Getting started](nodered/GETTING_STARTED.md) |

Not sure which fits? [Choosing a language](../choosing-a-language.md) compares
them by runtime environment and footprint rather than by speed.
[SLMP API parity](api-parity.md) shows which SLMP operations each implementation
exposes.

## Configure the PLC first

The library is only half of a working connection. The setup guides cover the
PLC-side parameter screens for each model, down to the data code and open
settings.

| Connection | Models with a setup guide |
|-----------|---------------------------|
| Built-in Ethernet (CPU) | iQ-R, iQ-F, iQ-L, MX-R, MX-F, QnUDV, QnU, LCPU |
| Ethernet communication unit | RJ71EN71, QJ71E71-100, LJ71E71-100 |

→ [MELSEC SLMP PLC setup](../plc-setup/slmp/index.md) ·
[Troubleshooting & Codes](../plc-setup/slmp/troubleshooting-codes.md)

## PLC model profiles

Select a profile such as `melsec:iq-r` and the library applies the correct frame
type, address grammar, and per-model device ranges for you. The profile is
always chosen explicitly — no implementation infers it from the PLC.

→ [SLMP profile reference](profile-reference/index.md) ·
[Profile parameters](profile-reference/parameters.md) ·
[Device ranges](profile-reference/device-ranges.md)

## Before you write anything

A wrong write on a running machine is not undoable. Read
[Bit Write Safety](../bit-write-safety.md) before your first write, and confirm
an address range is safe for the connected equipment.

To check a connection with no code at all,
[PLC Scope](../index.md#try-it-without-writing-code) is a Windows tool built on
these libraries — keep the first session read-only.
