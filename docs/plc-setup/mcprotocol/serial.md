# MELSEC MC Protocol Serial Setup

This page covers PLC-side serial-module setup and physical wiring checks for MELSEC MC Protocol Serial libraries.

## Minimum Setup Checklist

| Item | Setting |
|------|---------|
| Serial protocol | Enable MC Protocol on the PLC serial module |
| Frame / format | Match the library profile and protocol helper |
| Baud rate | Match the host or MCU serial setting |
| Data bits / parity / stop bits | Match the host or MCU serial setting exactly |
| Station number | Match the application route setting |
| Physical layer | Use RS-232C, RS-422, or RS-485 hardware that matches the PLC module |
| After parameter changes | Power cycle the PLC or module if the PLC/tool requires it |

## Known Host-side Shape

The project has used this shape for real-hardware validation:

```text
Linux host
  -> USB to RS-232C adapter
  -> RS-232C cable
  -> MELSEC serial module RS-232C port
```

Important points:

- Use an actual RS-232C adapter, not a bare 3.3V TTL UART.
- RS-232C and MCU UART logic levels are different.
- Match the client frame mode to the serial module setting. A module configured for one MC Protocol format will not treat another format as equivalent.
- Do not copy protocol settings from an old sample or old log without checking the current PLC/module configuration.

## MCU-side Shape

For ESP32-C3, RP2040, Arduino Mega, or similar boards, do not wire TX/RX directly to the PLC RS-232C connector.

Use this shape instead:

```text
MCU UART (3.3V or 5V TTL)
  -> TTL / RS-232C level shifter such as MAX3232
  -> RS-232C cable
  -> MELSEC serial module RS-232C port
```

Important points:

- The MCU side is TTL UART.
- The PLC side is RS-232C.
- A level shifter is required between them.
- RS-485 DE/RE control is not needed for the validated RS-232C setup.
- Sample UART pins are board defaults, not wiring rules. Change them to match the board, level shifter, and cable.

## Connecting with a Library

| Parameter | Example value |
|-----------|---------------|
| Serial port | `COM3` or `/dev/ttyUSB0` |
| Serial setting | `19200 / 8E1` |
| Station number | `0` for a point-to-point station, or the configured multidrop station |
| Canonical profile | `melsec:qcpu`, `melsec:iq-r`, `melsec:iq-f`, etc. |

Pass the canonical profile explicitly. Standard connection helpers do not infer it from the PLC model or serial settings.

## Bring-up Order

1. Confirm the PLC serial-module parameters.
2. Confirm the physical interface and TX/RX/GND mapping.
3. Prove the line with a read-only identification check.
4. Prove a small read-only device range.
5. Add write traffic only against a safe test area.

## Related Pages

- [MC Protocol Serial supported registers](supported-registers.md)
- [MC Protocol Serial Troubleshooting & Codes](troubleshooting-codes.md)
