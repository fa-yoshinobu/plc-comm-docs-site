---
description: "Applications built on the plc-comm libraries: PLC Scope (Windows monitor), FA Labo PLC Console (Android/iOS), and the Factory I/O SLMP / Host Link Gateway."
---

# Applications built with these libraries

These are complete applications that use the plc-comm libraries for all of their
PLC communication. They are worth knowing about for two reasons: they show what
the libraries can carry in a real product, and the first one doubles as a way to
check a PLC connection before you write any code of your own.

Each application selects a connection option set, picks a PLC profile, and reads
or writes devices by name — the same model described throughout this
documentation. When a connection works in one of these tools, the protocol,
host, port, profile, and address strings carry straight over into your own code.

## PLC Scope

A Windows desktop tool for live PLC I/O checks: connect to a PLC, monitor device
ranges, keep important devices in a watch list, edit values inline, import
comments, issue CPU RUN / STOP, and save the layout as a project file.

PLC Scope implements no protocol itself — every connection, read, and write goes
through the same .NET packages you would reference in your own application, so a
working session proves the library, the connection settings, and the PLC-side
configuration before a line of code is written.

| | |
|---|---|
| Platform | Windows desktop (.NET 10) |
| Protocols | MELSEC SLMP, KEYENCE KV Host Link, JTEKT TOYOPUC Computer Link |
| Built on | [`PlcComm.Slmp`](slmp/dotnet/GETTING_STARTED.md), [`PlcComm.KvHostLink`](hostlink/dotnet/GETTING_STARTED.md), [`PlcComm.Toyopuc`](computerlink/dotnet/GETTING_STARTED.md) |
| Source | [github.com/fa-yoshinobu/plc-scope-dotnet](https://github.com/fa-yoshinobu/plc-scope-dotnet) |
| License | MIT |

## FA Labo PLC Console

An Android / iOS app for monitoring and controlling MELSEC and KEYENCE KV PLCs
from a phone or tablet: block, list, and panel monitor views, device writes and
CPU mode control, time-chart recording with CSV export, and trap (alarm)
conditions with an event log. Projects are prepared on a PC with the companion
ProjectBuilder tool and transferred to the device by QR code or JSON file.

| | |
|---|---|
| Platform | Android, iOS |
| Protocols | MELSEC SLMP, KEYENCE KV Host Link |
| Built on | [`plc-comm-slmp`](slmp/rust/GETTING_STARTED.md) and [`plc-comm-kv-hostlink`](hostlink/rust/GETTING_STARTED.md) (Rust) |
| Product site | [plc-console.fa-labo.com](https://plc-console.fa-labo.com/) |
| Distribution | Mobile app stores — see the product site |

## Factory I/O SLMP / Host Link Gateway

A Windows desktop application that bridges the [Factory I/O](https://factoryio.com/)
`Modbus TCP/IP Client` driver to a real PLC. Factory I/O connects to the gateway
as a Modbus TCP client; the gateway talks to the PLC over SLMP or KEYENCE Host
Link. Coil and holding-register values flow from Factory I/O to the PLC, and
discrete-input and input-register values are read back from the PLC. It imports
the Factory I/O tag CSV, maps each tag to a PLC device address (with bulk
assignment), selects a PLC profile, and reconnects automatically with backoff if
the PLC link drops while Factory I/O stays connected.

| | |
|---|---|
| Platform | Windows desktop (.NET 9) |
| Protocols | MELSEC SLMP, KEYENCE Host Link |
| Built on | The .NET plc-comm libraries ([`PlcComm.Slmp`](slmp/dotnet/GETTING_STARTED.md), [`PlcComm.KvHostLink`](hostlink/dotnet/GETTING_STARTED.md)) |
| Source | [github.com/fa-yoshinobu/factoryio-slmp-hostlink-gateway](https://github.com/fa-yoshinobu/factoryio-slmp-hostlink-gateway) |
| License | MIT |
