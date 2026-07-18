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
| `1C` NAK codes | Legacy `1C` A-compatible / QnA-compatible frames. | Representative project-observed codes are listed below. Record the raw response and exact target settings before applying a meaning to another setup. |
| No response | The module ignores the request or cannot answer in the selected mode. | Treat as a transport/configuration problem first, not as an error code. |

## Observed Codes

Only project-observed cases are listed here. If you see a code not listed here, record the raw response, frame kind, ASCII/binary mode, station, sum-check setting, PLC model, serial module, and selected PLC profile.

| Code | Observed situation | Practical check |
| --- | --- | --- |
| `0x4031` | CPU-side device or route rejection observed on serial paths, for example unsupported link-direct access on a target setup. | Check the selected profile, route notation, mounted module, and whether the requested device family exists on that PLC. |
| `0x7F22` | Serial-module rejection observed for unsupported serial-MC device/command shapes, such as `S` device probes on a C24 path before CPU forwarding. | Do not treat unsupported device families as valid access paths. Recheck the profile support table and the serial-module MC protocol format. |
| `1C` NAK `0x02` | Intentionally bad sum-check on a transmitted `WR0` read. | Verify that sum-check is enabled consistently and recalculate the transmitted sum. |
| `1C` NAK `0x03` | Nonexistent `1C` command. | Check the command mnemonic and selected `1C` format. |
| `1C` NAK `0x06` | `WR0` read with a zero point count. | Send a valid nonzero point count within the command limit. |
| `1C` NAK `0x07` | `WR0` read with an invalid device code. | Check the device family and its encoding for the selected profile. |
| `1C` NAK `0x10` | Format 4 `WR0` read with a mismatched PC field on the tested iQ-F / FX5 bench. | Check the station and PC header fields against the serial-module settings. |
| `0x7E40` | Invalid `C4` command/subcommand and an unregistered monitor-read shape on the tested bench. | Check the command, subcommand, and whether a required registration step exists for the selected route. |
| `0x7F21` | `C4` read/write using `DX0`, which was unavailable on the tested setup. | Recheck the selected profile, device family, and route; do not generalize one setup to every PLC. |
| `0x7F24` | Intentionally bad sum-check on a transmitted `C4` read. | Verify the sum-check setting and recalculate the transmitted sum. |

## Evidence Scope

The decoder preserves error codes such as two-digit `1C` NAK codes and four-digit QnA serial responses, but this page does not assign meanings to unmeasured codes.

Representative `1C` NAK and `C4`/serial `7Fxx` measurements are complete; there is no active generic error-code collection TODO. Future measurements should start only from a specific diagnostic need and must record the exact frame, target, module settings, and observed response. Add only observed codes to this page.
