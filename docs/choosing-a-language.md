---
description: "How to choose between the .NET, Python, Rust, C++, and Node-RED plc-comm implementations, based on runtime environment, footprint, and protocol coverage rather than on latency."
---

# Choosing a language

Every implementation in this project follows the same model: pick a connection
option set, pick your PLC profile, read or write a device by name. Which one you
install is therefore a question about your runtime environment — where the code
has to run, what has to be installed alongside it, and which protocol you need —
rather than a question about which one talks to a PLC better.

## Latency is not the deciding factor

In the published benchmark session, the .NET and Rust clients landed 0.01 ms to
0.02 ms apart on the per-iteration average against the same physical MELSEC
iQ-R. Response time on a PLC network is dominated by the PLC itself: CPU model,
scan time, communication settings, cabling, and how many other clients are
attached move these numbers far more than the client language does.

The measured figures, the full test conditions, and a five-hour soak of every
implementation are on the [Performance](performance.md) page. Read them as one
data point and measure your own installation before designing a control loop
around a specific value.

## The five implementations

| Language | Choose it when | Getting started |
|----------|---------------|-----------------|
| **Python** | You want a quick answer today: bring-up scripts, one-off verification, logging and data analysis | [SLMP](slmp/python/GETTING_STARTED.md) · [KV Host Link](hostlink/python/GETTING_STARTED.md) · [Computerlink](computerlink/python/GETTING_STARTED.md) |
| **.NET** | The code ships as a Windows desktop or server application: WPF HMI, Windows service, enterprise stack | [SLMP](slmp/dotnet/GETTING_STARTED.md) · [KV Host Link](hostlink/dotnet/GETTING_STARTED.md) · [Computerlink](computerlink/dotnet/GETTING_STARTED.md) |
| **Rust** | You want the smallest deployed footprint with no runtime to install and no garbage collector: embedded Linux, AGVs, long-running resident processes | [SLMP](slmp/rust/GETTING_STARTED.md) · [KV Host Link](hostlink/rust/GETTING_STARTED.md) |
| **C++ (Arduino/PlatformIO)** | The client is microcontroller firmware — ESP32/RP2040-class boards — or you need MC Protocol Serial | [SLMP](slmp/cpp/GETTING_STARTED.md) · [MC Protocol Serial](mcprotocol/cpp/GETTING_STARTED.md) |
| **Node-RED** | You would rather wire nodes than write code: dashboards, and PLC data added to an existing flow | [SLMP](slmp/nodered/GETTING_STARTED.md) · [KV Host Link](hostlink/nodered/GETTING_STARTED.md) |

### Python

Python 3.10 or newer, with an asyncio client. This is the shortest path from
"can I reach this PLC" to a printed value, and the easiest place to take the
values somewhere else — a CSV, a notebook, pandas, a plotting library. Use it
for commissioning scripts, acceptance checks, and data collection. Together with
.NET it has the widest protocol coverage: SLMP, KV Host Link, and Computerlink.

### .NET

The implementation to pick when the PLC client is part of a shipped Windows
application: a WPF HMI, a background Windows service, or an existing enterprise
codebase. It carries the same three protocols as Python, so a Python bring-up
script and the .NET application that replaces it use the same profile names and
the same typed-read vocabulary.

### Rust

No managed runtime to install on the target and no garbage collector, which
makes it the choice for equipment you deploy once and leave running: embedded
Linux boxes, AGVs, edge gateways, and other long-lived resident processes. In
the benchmark session the Rust client process was recorded at 6.4 MB of process
memory against 57.8 MB for the .NET benchmark runner — read
[how to read these numbers](performance.md#how-to-read-these-numbers) before
quoting that pair, because the two values cover differently shaped processes and
are a reference figure rather than a like-for-like comparison. Rust covers SLMP
and KV Host Link.

### C++ (Arduino/PlatformIO)

For firmware rather than for a PC: ESP32/RP2040-class boards using
Arduino-compatible cores or PlatformIO, where there is no runtime and no
operating system to depend on. C++ is also the only implementation of
MC Protocol Serial over RS-232C/RS-485, and that library builds host-side as
well for bring-up tools.

### Node-RED

Install the package from Manage palette, add a connection config node with your
PLC profile, and drop a read node into a flow. Nothing is compiled and nothing
is deployed separately, which suits dashboards, quick visualizations, and adding
PLC values to automation you already run in Node-RED.

## If you would rather not write code at all

Node-RED is the no-code option when you want a flow you keep and extend. For a
one-off check — is the PLC reachable, is `D100` really what I think it is —
[PLC Scope](index.md#try-it-without-writing-code) is a Windows desktop tool you
download and run, with no project and no install step.

## Protocol coverage differs by language

Not every protocol has every implementation. Check this before you commit to a
language.

| Protocol | .NET | Python | Rust | C++ | Node-RED |
|----------|:----:|:------:|:----:|:---:|:--------:|
| **SLMP** (MELSEC, Ethernet) | ✓ | ✓ | ✓ | ✓ | ✓ |
| **MC Protocol Serial** (MELSEC, serial) | — | — | — | ✓ | — |
| **KV Host Link** (KEYENCE KV) | ✓ | ✓ | ✓ | — | ✓ |
| **Computerlink** (JTEKT TOYOPUC) | ✓ | ✓ | — | — | — |

Registry package names and install commands for each pairing are in the
[Package Matrix](package-matrix.md). If you are not yet sure which protocol your
PLC speaks, start from [Which protocol do I need?](index.md#which-protocol-do-i-need)

## Mixing languages

The implementations are designed to be mixed. Prototype in Node-RED or Python
against the real PLC, then ship the same profile, the same address strings, and
the same typed reads in .NET, Rust, or C++. The knowledge transfers because the
API vocabulary does.
