---
description: "PLC-side Ethernet settings for the MELSEC MX-R built-in CPU port used with SLMP."
---

# MELSEC MX-R — PLC-side settings

MELSEC MX-R — built-in Ethernet port (CPU module).

## What you need

- **Configuration tool:** GX Works3
- **Network:** Align IP address, subnet mask, and default gateway with your network environment.
- **After configuration:** Power cycle the PLC to apply the new parameters.

## Example values used in this guide

| Parameter | Example value | Notes |
|-----------|--------------|-------|
| IP address | `192.168.250.100` | Adapt to your network |
| TCP port | `1025` | SLMP TCP |
| UDP port | `1035` | SLMP UDP |

## PLC-side settings

MX-R uses its own canonical library profile (`melsec:mx-r`) while keeping iQ-R-compatible SLMP connection settings.

### Screen: Unit parameters

| Parameter | Setting |
|-----------|---------|
| IP Address | `192.168.250.100` (example) |
| Subnet Mask | Match your network |
| Default Gateway | Match your network |
| Open Method | Program does not open |

### Screen: Remote device connection settings

| Parameter | TCP | UDP |
|-----------|-----|-----|
| Communication Method | SLMP | SLMP |
| Protocol | TCP | UDP |
| Port Number | `1025` | `1035` |
| Keep-Alive | Enabled | UDP (alive check) |

## Connecting with this library

| Parameter | Value |
|-----------|-------|
| Canonical profile | `melsec:mx-r` |
| Port (TCP) | `1025` |
| Port (UDP) | `1035` |

Code example:

=== "Python"

    ```python
    import asyncio

    from slmp import SlmpConnectionOptions, open_and_connect, read_typed


    async def main() -> None:
        options = SlmpConnectionOptions(host="192.168.250.100", port=1025, plc_profile="melsec:mx-r")
        async with await open_and_connect(options) as client:
            value = await read_typed(client, "D100", "U")
            print(f"D100={value}")


    asyncio.run(main())
    ```

=== ".NET (C#)"

    ```csharp
    using PlcComm.Slmp;

    var options = new SlmpConnectionOptions("192.168.250.100", SlmpPlcProfile.MxR) { Port = 1025 };
    await using var client = await SlmpClientFactory.OpenAndConnectAsync(options);
    var value = await client.ReadTypedAsync("D100", "U");
    Console.WriteLine($"D100={value}");
    ```

The PLC-side settings on this page apply to every language. For
[Rust](../../slmp/rust/GETTING_STARTED.md),
[C++ (Arduino/PlatformIO)](../../slmp/cpp/GETTING_STARTED.md), and
[Node-RED](../../slmp/nodered/GETTING_STARTED.md), start from each
library's Getting started.

## Related SLMP docs

- [SLMP profile parameters](../../slmp/profile-reference/parameters.md)
- [SLMP Troubleshooting & Codes](troubleshooting-codes.md)

## Screenshots

![MXR300-32 IP address settings for the built-in Ethernet port](../images/slmp/mx-r/screenshot-01.png)
*MXR300-32 IP address settings for the built-in Ethernet port.*

![MXR300-32 basic settings and external device configuration](../images/slmp/mx-r/screenshot-02.png)
*MXR300-32 basic settings and external device configuration.*

![Built-in Ethernet configuration with TCP and UDP SLMP entries](../images/slmp/mx-r/screenshot-03.png)
*Built-in Ethernet configuration with TCP port 1025 and UDP port 1035 SLMP entries.*
