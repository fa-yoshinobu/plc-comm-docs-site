---
title: "JTEKT TOYOPUC Computerlink communication libraries"
description: "Talk to JTEKT TOYOPUC controllers over Ethernet with the Computerlink protocol, from .NET or Python, with PCwin and PCwin2 PLC setup guides."
---

# Computerlink — JTEKT TOYOPUC over Ethernet

Computerlink is the protocol a JTEKT TOYOPUC controller speaks over Ethernet.
The network settings are common across the supported controllers; what differs
is the engineering tool used to configure them, so the PLC-side guides are split
between PCwin and PCwin2 rather than by PLC model.

| | |
|---|---|
| Product families | TOYOPUC Nano, Plus, PC10G, PC3J |
| Transport | Ethernet, TCP or UDP |
| Default port | `1025` (TCP), `1035` (UDP) |
| Configuration tools | PCwin, PCwin2 |

TCP and UDP need different PLC-side peer settings on this protocol: for UDP the
PLC requires a peer entry in the Other Node Table and the PC must bind that same
local port. The [setup guides](../plc-setup/computerlink/index.md) cover both.

## Pick your language

Both implementations use the same model: pick a connection option set, pick your
PLC profile, then read or write a device by name.

| Language | Install | Start here |
|----------|---------|-----------|
| **Python** | `pip install plc-comm-toyopuc` | [Getting started](python/GETTING_STARTED.md) |
| **.NET** | `dotnet add package PlcComm.Toyopuc` | [Getting started](dotnet/GETTING_STARTED.md) |

There is no Rust, C++, or Node-RED implementation of Computerlink. See
[Choosing a language](../choosing-a-language.md) for how the implementations
compare by runtime environment.

## Configure the PLC first

| Engineering tool | Product families |
|------------------|------------------|
| PCwin2 | TOYOPUC Nano (Nano 10GX, Nano 2ET) |
| PCwin | TOYOPUC Plus, PC10G, PC3J |

→ [TOYOPUC Computerlink PLC setup](../plc-setup/computerlink/index.md) ·
[Troubleshooting & Codes](../plc-setup/computerlink/troubleshooting-codes.md) ·
[Device ranges](../plc-setup/computerlink/device-ranges.md)

## PLC model profiles

Select the canonical profile for the connected controller and the library
applies the correct area layout and addressing behavior. The profile is always
chosen explicitly — neither implementation infers it from the PLC.

→ [TOYOPUC profile reference](profile-reference/index.md) ·
[Profile parameters](profile-reference/parameters.md) ·
[Area ranges](profile-reference/area-ranges.md)

## Before you write anything

A wrong write on a running machine is not undoable. Read
[Bit Write Safety](../bit-write-safety.md) before your first write, and confirm
an address range is safe for the connected equipment.

To check a connection with no code at all,
[PLC Scope](../index.md#try-it-without-writing-code) is a Windows tool built on
these libraries — keep the first session read-only.
