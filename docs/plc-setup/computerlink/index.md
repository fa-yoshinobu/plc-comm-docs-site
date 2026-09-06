---
description: "PLC-side Ethernet settings for JTEKT TOYOPUC Computerlink: pick the PCwin or PCwin2 setup guide for your TOYOPUC Nano, Plus, PC10G, or PC3J controller."
---

# TOYOPUC Computerlink — PLC setup

Configure the JTEKT TOYOPUC controller before connecting with any Computerlink
library. The Computerlink network settings are common across the supported
controllers; only the engineering-tool screens differ, so the guides are split
by tool generation rather than by PLC model.

A **power cycle is required** after every parameter change. Pass the canonical
PLC profile explicitly when opening a connection — the libraries do not infer it
from the PLC.

## Choose your setup guide

These guides use TCP port `1025` and UDP port `1035`.

| Product family | Hardware | Engineering tool | Setup guide |
|----------------|----------|------------------|-------------|
| TOYOPUC Nano | Nano 10GX, Nano 2ET | PCwin2 | [PCwin2 settings](pcwin2.md) |
| TOYOPUC Plus | Plus CPU, Plus EX2 | PCwin | [PCwin settings](pcwin.md) |
| TOYOPUC PC10G | PC10G-1SP, PC10G, EF10, 2PORT-EFR | PCwin | [PCwin settings](pcwin.md) |
| TOYOPUC PC3J | PC3JX-D, PC3JG | PCwin | [PCwin settings](pcwin.md) |

[Choose a setup guide](toyopuc.md) also lists the example network used by the
screenshots, and explains why TCP and UDP need different peer settings on this
protocol.

## Shared reference pages

These pages apply to both language implementations of Computerlink.

| Page | Use it for |
|------|-----------|
| [Computerlink Troubleshooting & Codes](troubleshooting-codes.md) | PLC error codes and the first check for each. |
| [Computerlink Device Ranges](device-ranges.md) | Device families and ranges shared by the setup guides. |
| [TOYOPUC profile parameters](../../computerlink/profile-reference/parameters.md) | Canonical profile IDs, area counts, addressing options, and verified-model status. |
| [TOYOPUC area ranges](../../computerlink/profile-reference/area-ranges.md) | Direct, prefixed, packed, width, and step attributes per profile. |

## After the PLC is configured

Start from the Getting started page for your language:
[.NET](../../computerlink/dotnet/GETTING_STARTED.md) ·
[Python](../../computerlink/python/GETTING_STARTED.md)

To confirm the settings before writing any code, use
[PLC Scope](../../index.md#try-it-without-writing-code) and keep the first check
read-only.
