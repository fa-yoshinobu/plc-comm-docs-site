---
title: "KEYENCE KV Host Link communication libraries"
description: "Talk to KEYENCE KV series PLCs over Ethernet with the KV Host Link protocol, from .NET, Python, Rust, or Node-RED, with per-model PLC setup guides."
---

# KV Host Link — KEYENCE KV over Ethernet

KV Host Link is the upper-level link protocol a KEYENCE KV series PLC speaks on
its built-in Ethernet port or on a KV-XLE02 communication unit. It is an ASCII
command protocol, which keeps round-trip times short: in the published
[benchmark](../performance.md) it was the fastest of the four protocols
measured, at roughly 1.3–2.6 ms median round-trip.

| | |
|---|---|
| PLC families | KEYENCE KV-X500, KV-8000, KV-7000, KV-5000 |
| Transport | Ethernet, TCP or UDP |
| Default port | `8501` |
| Configuration tool | KV Studio |

## Pick your language

All four implementations use the same model: pick a connection option set, pick
your PLC profile, then read or write a device by name.

| Language | Install | Start here |
|----------|---------|-----------|
| **Python** | `pip install plc-comm-kv-hostlink` | [Getting started](python/GETTING_STARTED.md) |
| **.NET** | `dotnet add package PlcComm.KvHostLink` | [Getting started](dotnet/GETTING_STARTED.md) |
| **Rust** | `cargo add plc-comm-kv-hostlink` | [Getting started](rust/GETTING_STARTED.md) |
| **Node-RED** | `@fa_yoshinobu/node-red-contrib-plc-comm-kvhostlink` | [Getting started](nodered/GETTING_STARTED.md) |

There is no C++ (Arduino/PlatformIO) implementation of KV Host Link. See
[Choosing a language](../choosing-a-language.md) for how the four compare by
runtime environment and footprint.

## Configure the PLC first

The setup guides cover the KV Studio parameter screens for each model.

| Connection | Models with a setup guide |
|-----------|---------------------------|
| Built-in Ethernet (CPU) | KV-X500, KV-8000, KV-7000, KV-5000 |
| Communication unit | KV-XLE02, for a CPU with no built-in Ethernet port |

→ [KEYENCE KV Host Link PLC setup](../plc-setup/kv/index.md) ·
[Troubleshooting & Codes](../plc-setup/kv/troubleshooting-codes.md) ·
[Device ranges](../plc-setup/kv/device-ranges.md)

## PLC model profiles

Select a profile such as `keyence:kv-x500` and the library applies the correct
address grammar and per-model device ranges. With a KV-XLE02, pass the profile
of the CPU behind the unit. The profile is always chosen explicitly — no
implementation infers it from the PLC.

→ [KV Host Link profile reference](profile-reference/index.md) ·
[Profile parameters](profile-reference/parameters.md) ·
[Device ranges by profile](profile-reference/device-ranges.md)

## Before you write anything

A wrong write on a running machine is not undoable. Read
[Bit Write Safety](../bit-write-safety.md) before your first write, and confirm
an address range is safe for the connected equipment.

To check a connection with no code at all,
[PLC Scope](../index.md#try-it-without-writing-code) is a Windows tool built on
these libraries — keep the first session read-only.
