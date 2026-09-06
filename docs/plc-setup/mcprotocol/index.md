---
description: "PLC-side serial module setup for MELSEC MC Protocol Serial: module settings, host and MCU wiring shapes, supported registers, and observed error codes."
---

# MC Protocol Serial — PLC setup

Configure the MELSEC serial communication module before connecting with the
MC Protocol Serial library. Unlike the three Ethernet protocols, the physical
layer is part of the setup: the frame format, baud rate, and character format on
the PLC module must match the client exactly, and RS-232C levels must be
converted before an MCU UART is connected.

Power cycle the PLC or module after parameter changes if the PLC or engineering
tool requires it.

## Setup pages

| Page | Use it for |
|------|-----------|
| [Serial modules](serial.md) | Minimum module checklist, the verified host-side wiring shape, and the MCU-side shape using a level shifter. |
| [Supported registers](supported-registers.md) | Device families the serial library addresses, and how they are encoded. |
| [MC Protocol Serial Troubleshooting & Codes](troubleshooting-codes.md) | NAK and error responses observed during live verification, with the first check for each. |

## After the PLC is configured

MC Protocol Serial is implemented in C++ for Arduino and PlatformIO targets, and
the same library builds host-side for bring-up tools.

[C++ (Arduino/PlatformIO) Getting started](../../mcprotocol/cpp/GETTING_STARTED.md)

PLC Scope does not cover MC Protocol Serial. For a first read-only check on a
serial PLC, use the bring-up scripts in
[`examples/linux_cli`](https://github.com/fa-yoshinobu/plc-comm-mcprotocol-serial-cpp/tree/main/examples/linux_cli)
of the MC Protocol Serial C++ library.
