---
title: "MELSEC MC Protocol Serial communication library"
description: "Talk to MELSEC PLCs over an RS-232C, RS-422, or RS-485 serial communication module with MC Protocol, from C++ on Arduino, PlatformIO, or a Linux host."
---

# MC Protocol Serial — MELSEC over RS-232C/RS-485

MC Protocol Serial is the protocol a MELSEC serial communication module speaks
over RS-232C, RS-422, or RS-485. Use it when the MELSEC PLC has no Ethernet port
and only a serial module — typically a legacy Q or A series installation. When
an Ethernet port or communication unit is available, prefer
[SLMP](../slmp/index.md): it is faster and easier to wire.

| | |
|---|---|
| PLC families | MELSEC iQ-R, iQ-L, Q series, A series, via a serial communication module |
| Transport | RS-232C, RS-422, RS-485 |
| Typical link | 19,200 baud, 8-E-1 |
| Physical layer | Part of the setup — an MCU UART needs a level shifter |

The link, not the library, sets the pace here. In the published
[benchmark](../performance.md) a single round-trip took about 67 ms at 19,200
baud, against roughly 9 ms for SLMP over TCP. Size your polling loop for the
wire, not for the client.

## The implementation

| Language | Install | Start here |
|----------|---------|-----------|
| **C++ (Arduino/PlatformIO)** | `fa-yoshinobu/mcprotocol-serial-cpp` | [Getting started](cpp/GETTING_STARTED.md) |

This is the only implementation. It targets ESP32/RP2040-class boards and
Arduino-compatible cores, and the same library builds host-side on Linux for
bring-up tools.

## Configure the PLC and the wiring first

The frame format, baud rate, and character format on the PLC module must match
the client exactly, and RS-232C levels must be converted before an MCU UART is
connected. Wiring an MCU's TX/RX straight to the module is the common mistake.

→ [MC Protocol Serial PLC setup](../plc-setup/mcprotocol/index.md) ·
[Serial modules](../plc-setup/mcprotocol/serial.md) ·
[Supported registers](../plc-setup/mcprotocol/supported-registers.md) ·
[Troubleshooting & Codes](../plc-setup/mcprotocol/troubleshooting-codes.md)

## Before you write anything

A wrong write on a running machine is not undoable. Read
[Bit Write Safety](../bit-write-safety.md) before your first write, and confirm
an address range is safe for the connected equipment.

PLC Scope does not cover MC Protocol Serial. For a first read-only check, use
the bring-up scripts in
[`examples/linux_cli`](https://github.com/fa-yoshinobu/plc-comm-mcprotocol-serial-cpp/tree/main/examples/linux_cli)
of the C++ library.
