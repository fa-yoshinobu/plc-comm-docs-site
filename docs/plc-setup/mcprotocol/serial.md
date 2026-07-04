# MELSEC MC Protocol Serial — PLC-side settings

This setup page is under preparation.

Before using the MC Protocol Serial library, configure the PLC serial module so
that the serial protocol, station number, and physical serial settings match the
application.

## Current minimum checklist

| Item | Setting |
|------|---------|
| Serial protocol | Enable MC Protocol on the PLC serial module |
| Frame / format | Match the library profile and protocol helper |
| Baud rate | Match the host or MCU serial setting |
| Data bits / parity / stop bits | Match the host or MCU serial setting exactly |
| Station number | Match the application route setting |
| Physical layer | Use RS-232C, RS-422, or RS-485 hardware that matches the PLC module |
| After parameter changes | Power cycle the PLC or module if the PLC/tool requires it |

Detailed model-specific screenshots and setting names will be added later.

## Connecting with this library

| Parameter | Example value |
|-----------|---------------|
| Serial port | `COM3` or `/dev/ttyUSB0` |
| Serial setting | `19200 / 8E1` |
| Station number | `0` for a point-to-point station, or the configured multidrop station |
| Canonical profile | `melsec:qcpu`, `melsec:iq-r`, `melsec:iq-f`, etc. |

Pass the canonical profile explicitly. The standard connection helpers do not
infer it from the PLC model or serial settings.

## Troubleshooting

- [MC Protocol Serial error codes](error-codes.md)
