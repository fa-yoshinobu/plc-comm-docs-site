# SLMP Troubleshooting & Codes

This page summarizes situations observed during this project's live PLC verification and common SLMP setup issues. It is not the official definition of every SLMP end code. Use the Mitsubishi manuals for formal definitions and complete code tables.

## First Checks

Before chasing one code, confirm these basics:

- The application selected the correct canonical PLC profile.
- The PLC Ethernet port uses Binary SLMP data code; see the [MELSEC SLMP PLC Setup Guide](../index.md).
- PLC-side RUN-time write permission is enabled before write tests where the PLC exposes that setting.
- Strict profile mode is enabled unless you intentionally want to send unsupported commands and let the PLC answer.
- Point counts are within the selected profile limits.
- Routed devices such as `Un\Gn`, `Jn\...`, and `U3En\G` exist in the actual PLC configuration.

## Common Symptoms

| Symptom | Likely cause | First check |
| --- | --- | --- |
| The connection opens, but every request returns an end code. | The selected PLC profile does not match the PLC, or the PLC Ethernet port data-code setting does not match the library request format. | Select the canonical profile for the connected PLC and confirm Binary SLMP is configured on the PLC-side port. |
| Reads work, but writes fail. | PLC-side RUN-time write permission, remote password state, or profile write policy blocks the write. | Check RUN-time write permission, remote password state, and the selected profile's write policy. |
| A large read, write, random request, or monitor request fails with `C051`, `C052`, `C053`, or `C054`. | The request exceeds the selected profile's per-request point limit. | Split the request and check the shared profile parameter table for the active PLC. |
| One write request mixes word devices and bit devices and fails. | Some PLC paths reject mixed word and bit block writes. | Send word writes and bit writes as separate requests. |
| `X`/`Y` points look shifted, or `DX`/`DY` is rejected on iQ-F. | iQ-F uses octal text for `X`/`Y`, and the iQ-F profile does not support `DX`/`DY`. | Use the iQ-F profile and use `X` / `Y` rather than `DX` / `DY` on iQ-F. |
| `D50.D` reads bit 13 instead of a 32-bit value. | Dot notation means bit-in-word access; `D` after the dot is hexadecimal bit index 13. | Use the library's typed form such as `D50:D` for unsigned 32-bit data. |
| `D50.3,8` or a similar bit-in-word count is rejected. | Dot notation selects one bit inside one word and is scalar-only. | Use `D50.3` for one bit, or use a direct bit family such as `M1000:BIT,8` for consecutive bit devices. |
| `LTN`, `LSTN`, `LCN`, or `LZ` looks truncated or shifted. | These current-value families are 32-bit values. | Use the library's 32-bit form, such as `:D` or `:L` in named addresses. |
| `LCS` or `LCC` behaves unlike a word value. | Long counter state devices are bit devices. | Read or write them as bit values. |
| Block commands fail on Q/L built-in profiles. | Some Q/L built-in Ethernet profiles do not use block commands for normal high-level access. | Use normal direct/random read and write helpers. Disable strict profile only for deliberate compatibility investigation. |

## Common End Codes

| End code | Typical symptom | Likely cause | What to check |
| --- | --- | --- | --- |
| `C050` | The TCP connection opens, but every request fails. | PLC-side data-code setting does not match the library request format, often ASCII vs binary. | Check the Ethernet open setting and use binary SLMP settings for these libraries. |
| `C051` | A direct word read/write fails at a large point count. | Word point count is over the selected profile limit. | Split the request or select the correct profile. In normal high-level use this should be caught before send. |
| `C052` | A direct bit read/write fails at a large point count. | Bit point count is over the selected profile limit. On iQ-F, observed `C051` and `C052` point-limit meanings differ from the other verified profiles. | Split the request and check the profile table for the active PLC. |
| `C053` | Random bit write fails when many bit devices are included. | Random bit write point count is over the profile limit. | Reduce the random write batch size. |
| `C054` | Random word read/write or monitor registration fails with many devices. | Random/monitor word count is over the profile limit. Dword devices can consume more than one word slot. | Reduce the batch size and account for word weighting. |
| `C056` | A request fails only for a high device number. | Device number is outside the PLC range. | Use an address that exists for the PLC program and configuration. |
| `C058` | A low-level or raw-frame request fails immediately. | Request length does not match the encoded address section. | Prefer high-level builders, or re-check raw frame length fields and address packing. |
| `C059` | A command fails even though the device address is ordinary. | Command or subcommand is not supported by the selected profile. | Check the profile's feature support. This is common for block/type-name commands on some Q/L profiles. |
| `C05B` | A routed or special device request fails. | The target CPU cannot access that device path or family. | Check PLC model, mounted modules, route notation, and whether the family exists on that profile. |
| `C05C` | A request fails after changing bit/word mode or count. | Request content is invalid for that command, such as a bit-unit mismatch. | Check the command variant, device family type, address unit, and count. |
| `C05F` | The command is syntactically valid but still refused. | The target CPU cannot execute that request in the current state or route. | Check CPU mode, route, command support, and profile setting. |
| `C061` | A raw-frame or low-level request fails with a length/count error. | Request data length and data count disagree. | Recalculate count fields and payload length, or use a high-level helper. |
| `C200`, `C201`, `C204` | Access is refused after the network path is established. | Remote password state prevents the operation. | Release the remote password and check whether another device owns the unlock state. |
| `4030`, `4031` | The PLC reports a CPU-side device name or device number error. | Invalid device family, invalid device number, or nonexistent routed path. | Re-check the device notation and PLC configuration. Treat other 4000-series CPU errors as manual lookup items. |

## Node-Function End Codes

The codes below are SLMP node-function responses from the Mitsubishi manuals.
They are included here so operators can recognize them, but the maintained
libraries do not implement the `0x0E3x` node-function command family. For that
scope decision, see [SLMP API Parity](../../slmp/api-parity.md#out-of-scope-node-functions).

| End code | Meaning | Practical check |
| --- | --- | --- |
| `CEE0` | Node-function command is already executing. | Wait for the current node-function operation to finish before retrying from a tool that supports that command family. |
| `CEE1` | Node-function request data size is invalid. | Check the command's required request length in the Mitsubishi manual. |
| `CEE2` | Node-function response data size is invalid. | Check whether the requester expected the correct response length for that command. |
| `CF10` | Server number does not exist. | Check the target server number before using node-function tooling. |
| `CF20` | Communication settings cannot be changed. | Do not attempt communication-setting changes from these libraries; use supported engineering tools and controlled setup procedures. |
| `CF30` | Parameter ID does not exist. | Check the parameter ID against the Mitsubishi manual for the target. |
| `CF31` | Parameter cannot be set. | Check whether the parameter is read-only, target-dependent, or restricted by the current configuration. |

## Profile Limit Codes

`C051` through `C054` are normally prevented by the library profile checks when using the high-level API. If they appear in normal usage, check for one of these first:

- The profile was not selected correctly.
- The call used a raw or low-level path that bypasses profile checks.
- The bundled profile data is stale.
- The request includes dword devices and the weighted word count is higher than expected.

## Unsupported Operations

For unsupported profile features, the preferred behavior is to reject before sending when strict profile mode is enabled. If strict profile mode is disabled, the request is sent and the PLC end code becomes the diagnostic result.

Use this only for troubleshooting or compatibility investigation. Normal applications should keep strict profile behavior enabled.
