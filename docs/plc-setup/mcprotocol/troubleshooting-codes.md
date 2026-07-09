# MC Protocol Serial Troubleshooting & Codes

This page is a practical guide for errors returned by MELSEC serial MC Protocol targets. It is not a complete Mitsubishi error-code table. Use the PLC and serial-module manuals for formal definitions.

## Library Status Categories

The C++ library reports transport and parser failures separately from PLC/module error responses.

| Status category | Typical meaning | First checks |
| --- | --- | --- |
| Timeout | No complete response arrived before the response timeout. | Check wiring, baud rate, parity, stop bits, station number, and whether the PLC module is configured for the same frame type. |
| Framing | Bytes arrived, but they did not match the selected response frame. | Check 1C/2C/3C/4C/1E selection, ASCII format, binary vs ASCII mode, and CR/LF settings. |
| Sum-check mismatch | A response arrived, but its sum-check did not match. | Check whether sum-check is enabled on both sides. If it is, check serial noise and wiring. |
| Parse | The response frame shape was recognized, but a numeric field or payload length could not be decoded. | Capture the raw frame and check whether the selected frame/profile matches the PLC setting. |
| Unsupported configuration | The request cannot be encoded for the selected profile, frame, or build options. | Select an explicit PLC profile, choose a supported frame helper, and check disabled feature macros. |
| PLC/module error | The PLC or serial module returned an error response. | Read the preserved PLC/module error code and use the sections below. |

## PLC and Serial-Module Error Families

Serial MC Protocol uses more than one error-code family. Do not interpret every code as an SLMP Ethernet end code.

| Code family | Where it appears | How to handle it |
| --- | --- | --- |
| CPU-side `4000`-series and related PLC end codes | QnA extended `3C` / `4C` routes when the request reaches the CPU. | Use the [SLMP Troubleshooting & Codes guide](../slmp/troubleshooting-codes.md) for practical checks. |
| `7Fxx` serial-module responses | Serial-module rejection before or around CPU forwarding. | Treat as target/module dependent. Check frame mode, profile, device family, route, and module settings. |
| `1C` NAK codes | Legacy `1C` A-compatible / QnA-compatible frames. | Not expanded as a user table here. Use the PLC and serial-module manuals for formal meanings when diagnosing a specific NAK. |
| No response | The module ignores the request or cannot answer in the selected mode. | Treat as a transport/configuration problem first, not as an error code. |

## Observed Codes

Only project-observed cases are listed here.

| Code | Observed situation | Practical check |
| --- | --- | --- |
| `0x4031` | CPU-side device or route rejection observed on serial paths, for example unsupported link-direct access on a target setup. | Check the selected profile, route notation, mounted module, and whether the requested device family exists on that PLC. |
| `0x7F22` | Serial-module rejection observed for unsupported serial-MC device/command shapes, such as `S` device probes on a C24 path before CPU forwarding. | Do not treat unsupported device families as valid access paths. Recheck the profile support table and the serial-module MC protocol format. |

## Codes Intentionally Not Expanded Yet

The decoder preserves error codes such as two-digit `1C` NAK codes and four-digit QnA serial responses, but this page does not assign meanings to unmeasured codes. Use the PLC and serial-module manuals for formal definitions.
