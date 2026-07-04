# MELSEC MX-F — PLC-side settings

MELSEC MX-F — built-in Ethernet port (CPU module).

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

MX-F uses its own canonical library profile (`melsec:mx-f`) while keeping iQ-F-compatible SLMP connection settings.

!!! note "Connection reports wanted"
    This project has not yet received live connection reports for the `melsec:mx-f` profile. If you use this profile, please report both successful and failed connection examples, including the PLC model, port setting, selected profile, and first SLMP end code when a connection fails.

### Screen: Unit parameters

| Parameter | Setting |
|-----------|---------|
| IP Address | `192.168.250.100` (example) |
| Subnet Mask | Match your network |
| Default Gateway | Match your network |
| Communication Data Code | Binary |

### Screen: Connection settings

| Parameter | TCP | UDP |
|-----------|-----|-----|
| Communication Method | SLMP | SLMP |
| Protocol | TCP | UDP |
| Port Number | `1025` | `1035` |
| Remote Device IP Address | - | Enter the IP of the connecting PC |
| Keep-Alive | Enabled | Disabled |

!!! warning "DX/DY not valid for MX-F"
    Use X and Y instead of DX and DY with the MX-F profile.

## Connecting with this library

| Parameter | Value |
|-----------|-------|
| Canonical profile | `melsec:mx-f` |
| Port (TCP) | `1025` |
| Port (UDP) | `1035` |

Code example:

=== "Python"

    ```python
    import asyncio

    from slmp import SlmpConnectionOptions, open_and_connect, read_typed


    async def main() -> None:
        options = SlmpConnectionOptions(host="192.168.250.100", port=1025, plc_profile="melsec:mx-f")
        async with await open_and_connect(options) as client:
            value = await read_typed(client, "D100", "U")
            print(f"D100={value}")


    asyncio.run(main())
    ```

=== ".NET (C#)"

    ```csharp
    using PlcComm.Slmp;

    var options = new SlmpConnectionOptions("192.168.250.100", SlmpPlcProfile.MxF) { Port = 1025 };
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

![Unit parameters screen for the built-in Ethernet port](../images/slmp/mx-f/screenshot-01.png)
*Unit parameters screen for the built-in Ethernet port.*

![Connection settings screen for the first SLMP entry](../images/slmp/mx-f/screenshot-02.png)
*Connection settings screen for the first SLMP entry.*

![Connection settings screen for the second SLMP entry](../images/slmp/mx-f/screenshot-03.png)
*Connection settings screen for the second SLMP entry.*
