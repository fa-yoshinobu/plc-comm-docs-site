# PLC Communication Libraries

A set of libraries for communicating with industrial PLCs over TCP/UDP and RS-232C/RS-485 serial.

![PLC Communication Libraries](assets/plc-communication-libraries.png)

Maintained by [fa-yoshinobu](https://github.com/fa-yoshinobu) · [FA Labo](https://fa-yoshinobu.github.io/FA_Labo/index.html)

## Computerlink (JTEKT TOYOPUC)

| Language | Docs | GitHub | Registry |
|----------|------|--------|----------|
| .NET | [Getting started](computerlink/dotnet/GETTING_STARTED.md) | [plc-comm-computerlink-dotnet](https://github.com/fa-yoshinobu/plc-comm-computerlink-dotnet) | [NuGet](https://www.nuget.org/packages/PlcComm.Toyopuc/) |
| Python | [Getting started](computerlink/python/GETTING_STARTED.md) | [plc-comm-computerlink-python](https://github.com/fa-yoshinobu/plc-comm-computerlink-python) | [PyPI](https://pypi.org/project/toyopuc-computerlink/) |

## KV Host Link (KEYENCE KV series)

| Language | Docs | GitHub | Registry |
|----------|------|--------|----------|
| .NET | [Getting started](hostlink/dotnet/GETTING_STARTED.md) | [plc-comm-hostlink-dotnet](https://github.com/fa-yoshinobu/plc-comm-hostlink-dotnet) | [NuGet](https://www.nuget.org/packages/PlcComm.KvHostLink/) |
| Python | [Getting started](hostlink/python/GETTING_STARTED.md) | [plc-comm-hostlink-python](https://github.com/fa-yoshinobu/plc-comm-hostlink-python) | [PyPI](https://pypi.org/project/kv-hostlink/) |
| Rust | [Getting started](hostlink/rust/GETTING_STARTED.md) | [plc-comm-hostlink-rust](https://github.com/fa-yoshinobu/plc-comm-hostlink-rust) | [crates.io](https://crates.io/crates/plc-comm-hostlink-rust) |
| Node-RED | [Getting started](hostlink/nodered/GETTING_STARTED.md) | [node-red-contrib-plc-comm-kvhostlink](https://github.com/fa-yoshinobu/node-red-contrib-plc-comm-kvhostlink) | [npm](https://www.npmjs.com/package/@fa_yoshinobu/node-red-contrib-plc-comm-kvhostlink) |

## SLMP (MELSEC iQ-R/F/L, Q, L)

| Language | Docs | GitHub | Registry |
|----------|------|--------|----------|
| .NET | [Getting started](slmp/dotnet/GETTING_STARTED.md) | [plc-comm-slmp-dotnet](https://github.com/fa-yoshinobu/plc-comm-slmp-dotnet) | [NuGet](https://www.nuget.org/packages/PlcComm.Slmp/) |
| Python | [Getting started](slmp/python/GETTING_STARTED.md) | [plc-comm-slmp-python](https://github.com/fa-yoshinobu/plc-comm-slmp-python) | [PyPI](https://pypi.org/project/slmp-connect-python/) |
| Rust | [Getting started](slmp/rust/GETTING_STARTED.md) | [plc-comm-slmp-rust](https://github.com/fa-yoshinobu/plc-comm-slmp-rust) | [crates.io](https://crates.io/crates/plc-comm-slmp-rust) |
| C++ (Arduino/PlatformIO) | [Getting started](slmp/cpp/GETTING_STARTED.md) | [plc-comm-slmp-cpp-minimal](https://github.com/fa-yoshinobu/plc-comm-slmp-cpp-minimal) | [PlatformIO](https://registry.platformio.org/libraries/fa-yoshinobu/slmp-connect-cpp-minimal) |
| Node-RED | [Getting started](slmp/nodered/GETTING_STARTED.md) | [node-red-contrib-plc-comm-slmp](https://github.com/fa-yoshinobu/node-red-contrib-plc-comm-slmp) | [npm](https://www.npmjs.com/package/@fa_yoshinobu/node-red-contrib-plc-comm-slmp) |

## MC Protocol Serial (MELSEC iQ-R/L, Q, A)

| Language | Docs | GitHub | Registry |
|----------|------|--------|----------|
| C++ (Arduino/PlatformIO) | [Getting started](mcprotocol/cpp/GETTING_STARTED.md) | [plc-comm-mcprotocol-serial-cpp](https://github.com/fa-yoshinobu/plc-comm-mcprotocol-serial-cpp) | [PlatformIO](https://registry.platformio.org/libraries/fa-yoshinobu/mcprotocol-serial-cpp) |

## PLC Setup Guide

Step-by-step PLC-side configuration for each supported hardware model.

| Protocol | Models covered |
|----------|---------------|
| MELSEC SLMP | iQ-R, iQ-F, iQ-L, MX-R, MX-F, QnUDV, QnU, LCPU, RJ71EN71, QJ71E71-100, LJ71E71-100 |
| KV Host Link | KV-X500, KV-8000, KV-7000, KV-5000, KV-XLE02 |
| Computerlink | *(coming soon)* |
| MC Protocol Serial | *(coming soon)* |

→ [Open PLC Setup Guide](plc-setup/index.md)

## Connection settings used in TCP/UDP examples

| Protocol | Host | TCP port | UDP port |
|----------|------|----------|----------|
| SLMP | 192.168.250.100 | 1025 | 1035 |
| Computerlink | 192.168.250.100 | 1025 | 1035 |
| KV Host Link | 192.168.250.100 | 8501 | 8501 |
