# PLC Communication Libraries

A set of libraries for communicating with industrial PLCs over TCP/UDP and RS-232C/RS-485 serial.

![PLC Communication Libraries](assets/plc-communication-libraries.png)

Maintained by [fa-yoshinobu](https://github.com/fa-yoshinobu) · [FA Labo](https://fa-yoshinobu.github.io/FA_Labo/index.html)

For license terms, commercial support, sponsorship, and donations, see
[License & Support](support.md).

For package names and install commands across the plc-comm family, see the
[Package Matrix](package-matrix.md).

## Which protocol do I need?

| Your PLC | Connection | Use |
|----------|-----------|-----|
| MELSEC (iQ-R/F/L, MX-R/F, Q, L) | Ethernet (TCP/UDP) | **SLMP** |
| MELSEC (iQ-R/L, Q, A) | RS-232C/RS-485 serial module | **MC Protocol Serial** |
| KEYENCE KV series | Ethernet (TCP/UDP) | **KV Host Link** |
| JTEKT TOYOPUC | Ethernet (TCP/UDP) | **Computerlink** |

For MELSEC PLCs, prefer **SLMP over Ethernet** whenever an Ethernet port or
communication unit is available — it is faster and easier to wire. Choose
**MC Protocol Serial** when only a serial communication module (RS-232C/RS-485)
is available, such as on legacy Q/A installations.

## Computerlink (JTEKT TOYOPUC)

| Language | Docs | Samples | GitHub | Registry |
|----------|------|---------|--------|----------|
| .NET | [Getting started](computerlink/dotnet/GETTING_STARTED.md) | [Examples](https://github.com/fa-yoshinobu/plc-comm-computerlink-dotnet/tree/main/examples) | [plc-comm-computerlink-dotnet](https://github.com/fa-yoshinobu/plc-comm-computerlink-dotnet) | [NuGet](https://www.nuget.org/packages/PlcComm.Toyopuc/) |
| Python | [Getting started](computerlink/python/GETTING_STARTED.md) | [Samples](https://github.com/fa-yoshinobu/plc-comm-computerlink-python/tree/main/samples) | [plc-comm-computerlink-python](https://github.com/fa-yoshinobu/plc-comm-computerlink-python) | [PyPI](https://pypi.org/project/plc-comm-toyopuc/) |

## KV Host Link (KEYENCE KV series)

| Language | Docs | Samples | GitHub | Registry |
|----------|------|---------|--------|----------|
| .NET | [Getting started](hostlink/dotnet/GETTING_STARTED.md) | [Samples](https://github.com/fa-yoshinobu/plc-comm-hostlink-dotnet/tree/main/samples) | [plc-comm-hostlink-dotnet](https://github.com/fa-yoshinobu/plc-comm-hostlink-dotnet) | [NuGet](https://www.nuget.org/packages/PlcComm.KvHostLink/) |
| Python | [Getting started](hostlink/python/GETTING_STARTED.md) | [Samples](https://github.com/fa-yoshinobu/plc-comm-hostlink-python/tree/main/samples) | [plc-comm-hostlink-python](https://github.com/fa-yoshinobu/plc-comm-hostlink-python) | [PyPI](https://pypi.org/project/plc-comm-kv-hostlink/) |
| Rust | [Getting started](hostlink/rust/GETTING_STARTED.md) | [Examples](https://github.com/fa-yoshinobu/plc-comm-hostlink-rust/tree/main/examples) | [plc-comm-hostlink-rust](https://github.com/fa-yoshinobu/plc-comm-hostlink-rust) | [crates.io](https://crates.io/crates/plc-comm-kv-hostlink) / [docs.rs](https://docs.rs/plc-comm-kv-hostlink/) |
| Node-RED | [Getting started](hostlink/nodered/GETTING_STARTED.md) | [Flows](https://github.com/fa-yoshinobu/node-red-contrib-plc-comm-kvhostlink/tree/main/examples/flows) | [node-red-contrib-plc-comm-kvhostlink](https://github.com/fa-yoshinobu/node-red-contrib-plc-comm-kvhostlink) | [npm](https://www.npmjs.com/package/@fa_yoshinobu/node-red-contrib-plc-comm-kvhostlink) |

## SLMP (MELSEC iQ-R/F/L, MX-R/F, Q, L)

| Language | Docs | Samples | GitHub | Registry |
|----------|------|---------|--------|----------|
| .NET | [Getting started](slmp/dotnet/GETTING_STARTED.md) | [Samples](https://github.com/fa-yoshinobu/plc-comm-slmp-dotnet/tree/main/samples) | [plc-comm-slmp-dotnet](https://github.com/fa-yoshinobu/plc-comm-slmp-dotnet) | [NuGet](https://www.nuget.org/packages/PlcComm.Slmp/) |
| Python | [Getting started](slmp/python/GETTING_STARTED.md) | [Samples](https://github.com/fa-yoshinobu/plc-comm-slmp-python/tree/main/samples) | [plc-comm-slmp-python](https://github.com/fa-yoshinobu/plc-comm-slmp-python) | [PyPI](https://pypi.org/project/plc-comm-slmp/) |
| Rust | [Getting started](slmp/rust/GETTING_STARTED.md) | [Examples](https://github.com/fa-yoshinobu/plc-comm-slmp-rust/tree/main/examples) | [plc-comm-slmp-rust](https://github.com/fa-yoshinobu/plc-comm-slmp-rust) | [crates.io](https://crates.io/crates/plc-comm-slmp) / [docs.rs](https://docs.rs/plc-comm-slmp/) |
| C++ (Arduino/PlatformIO) | [Getting started](slmp/cpp/GETTING_STARTED.md) | [Examples](https://github.com/fa-yoshinobu/plc-comm-slmp-cpp-minimal/tree/main/examples) | [plc-comm-slmp-cpp-minimal](https://github.com/fa-yoshinobu/plc-comm-slmp-cpp-minimal) | [PlatformIO](https://registry.platformio.org/libraries/fa-yoshinobu/slmp-connect-cpp-minimal) |
| Node-RED | [Getting started](slmp/nodered/GETTING_STARTED.md) | [Flows](https://github.com/fa-yoshinobu/node-red-contrib-plc-comm-slmp/tree/main/examples/flows) | [node-red-contrib-plc-comm-slmp](https://github.com/fa-yoshinobu/node-red-contrib-plc-comm-slmp) | [npm](https://www.npmjs.com/package/@fa_yoshinobu/node-red-contrib-plc-comm-slmp) |

## MC Protocol Serial (MELSEC iQ-R/L, Q, A)

| Language | Docs | Samples | GitHub | Registry |
|----------|------|---------|--------|----------|
| C++ (Arduino/PlatformIO) | [Getting started](mcprotocol/cpp/GETTING_STARTED.md) | [Examples](https://github.com/fa-yoshinobu/plc-comm-mcprotocol-serial-cpp/tree/main/examples) | [plc-comm-mcprotocol-serial-cpp](https://github.com/fa-yoshinobu/plc-comm-mcprotocol-serial-cpp) | [PlatformIO](https://registry.platformio.org/libraries/fa-yoshinobu/mcprotocol-serial-cpp) |

## PLC Setup Guide

Step-by-step PLC-side configuration for each supported hardware model.

| Protocol | Models covered |
|----------|---------------|
| MELSEC SLMP | iQ-R, iQ-F, iQ-L, MX-R, MX-F, QnUDV, QnU, LCPU, RJ71EN71, QJ71E71-100, LJ71E71-100 |
| KV Host Link | KV-X500, KV-8000, KV-7000, KV-5000, KV-XLE02 |
| Computerlink | TOYOPUC (minimum checklist; full guide in preparation) |
| MC Protocol Serial | MELSEC serial modules (iQ-R/L, Q, A) |

→ [Open PLC Setup Guide](plc-setup/index.md)

## Connection settings used in TCP/UDP examples

| Protocol | Host | TCP port | UDP port |
|----------|------|----------|----------|
| SLMP | 192.168.250.100 | 1025 | 1035 |
| Computerlink | 192.168.250.100 | 1025 | 1035 |
| KV Host Link | 192.168.250.100 | 8501 | 8501 |
