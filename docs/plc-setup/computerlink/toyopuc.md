---
description: "Choose the correct PCwin or PCwin2 PLC-side setup guide for JTEKT TOYOPUC Computerlink."
---

# TOYOPUC Computerlink — PLC-side setup

The Computerlink network settings are common across the supported TOYOPUC
controllers. The engineering-tool screens differ between PCwin and PCwin2, so
choose the guide by tool generation rather than by PLC model.

## Choose the setup guide

| Product family | Hardware | Engineering tool | Setup guide |
| --- | --- | --- | --- |
| TOYOPUC Nano | Nano 10GX, Nano 2ET | PCwin2 | [Configure Computerlink in PCwin2](pcwin2.md) |
| TOYOPUC Plus | Plus CPU, Plus EX2 | PCwin | [Configure Computerlink in PCwin](pcwin.md) |
| TOYOPUC PC10G | PC10G-1SP, PC10G, EF10, 2PORT-EFR | PCwin | [Configure Computerlink in PCwin](pcwin.md) |
| TOYOPUC PC3J | PC3JX-D, PC3JG | PCwin | [Configure Computerlink in PCwin](pcwin.md) |

## Example network settings

The screenshots in both guides use the same example network. Replace the IP
addresses and ports with values for your own isolated PLC network.

| Parameter | Example value |
| --- | --- |
| PLC IP address | `192.168.250.100` |
| Computerlink TCP port | `1025` |
| Computerlink UDP port | `1035` |
| UDP peer PC IP address | `192.168.250.120` |
| UDP peer PC port | `12000` |

## TCP and UDP use different peer settings

For TCP, the guides select `TCP Destination Non-Specified Passive Open`. The
PLC waits for a connection from the PC, and no peer entry is selected for that
connection. If you intentionally select a destination-specified TCP mode
instead, the connecting PC must match the peer parameters.

For UDP, the PLC requires a peer IP address and port in the Other Node Table.
The PC application must bind its UDP local port to the same port. With the
example above, use `LocalPort = 12000` in .NET or `local_port=12000` in Python;
do not use `0` for this PLC configuration.

## Connecting with the libraries

| Library setting | TCP | UDP |
| --- | --- | --- |
| PLC host | `192.168.250.100` | `192.168.250.100` |
| PLC destination port | `1025` | `1035` |
| PC local port | Not configured | `12000` |
| Transport | TCP | UDP |

Select the exact canonical profile for the connected PLC. The standard
connection helpers do not infer it from the PLC.

## Related pages

- [Computerlink Device Ranges](device-ranges.md)
- [Computerlink Troubleshooting & Codes](troubleshooting-codes.md)
- [.NET Getting started](../../computerlink/dotnet/GETTING_STARTED.md)
- [Python Getting started](../../computerlink/python/GETTING_STARTED.md)
