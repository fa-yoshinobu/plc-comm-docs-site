---
description: "PLC-side Ethernet settings for KEYENCE KV Host Link: pick the setup guide for your KV-X500, KV-8000, KV-7000, KV-5000, or KV-XLE02 communication unit."
---

# KEYENCE KV Host Link — PLC setup

Configure the KEYENCE KV PLC before connecting with any KV Host Link library.
Each guide below covers one CPU or communication unit down to the KV Studio
parameter screens, and ends with a first read using the libraries.

A **power cycle is required** after every parameter change. Pass the canonical
PLC profile explicitly when opening a connection — the libraries do not infer it
from the PLC.

## Choose your model

These guides use TCP port `8501`, and KV Studio is the configuration tool for
every model.

| Model | Connection | Canonical profile | Setup guide |
|-------|-----------|-------------------|-------------|
| KV-X500 | Built-in Ethernet | `keyence:kv-x500` | [KV-X500 settings](kv-x500.md) |
| KV-8000 | Built-in Ethernet | `keyence:kv-8000` | [KV-8000 settings](kv-8000.md) |
| KV-7000 | Built-in Ethernet | `keyence:kv-7000` | [KV-7000 settings](kv-7000.md) |
| KV-5000 | Built-in Ethernet | `keyence:kv-5000` | [KV-5000 settings](kv-5000.md) |
| KV-XLE02 | Communication unit | Connected CPU profile, for example `keyence:kv-x500` | [KV-XLE02 settings](kv-xle02.md) |

Use the KV-XLE02 when the KV series CPU has no built-in Ethernet port.

## Shared reference pages

These pages apply to every language implementation of KV Host Link.

| Page | Use it for |
|------|-----------|
| [KV Host Link Troubleshooting & Codes](troubleshooting-codes.md) | PLC error codes and the first check for each. |
| [KV Host Link Device Ranges](device-ranges.md) | Device families and ranges shared by the setup guides. |
| [KV profile parameters](../../hostlink/profile-reference/parameters.md) | Canonical IDs, display names, and XYM notation per profile. |
| [KV device ranges by profile](../../hostlink/profile-reference/device-ranges.md) | Device definitions and ranges compared across profiles. |

Simulator connection notes for the KV STUDIO Simulator are on the
[PLC setup guide overview](../index.md#simulator-connection-notes).

## After the PLC is configured

Start from the Getting started page for your language:
[.NET](../../hostlink/dotnet/GETTING_STARTED.md) ·
[Python](../../hostlink/python/GETTING_STARTED.md) ·
[Rust](../../hostlink/rust/GETTING_STARTED.md) ·
[Node-RED](../../hostlink/nodered/GETTING_STARTED.md)

To confirm the settings before writing any code, use
[PLC Scope](../../index.md#try-it-without-writing-code) and keep the first check
read-only.
