# KV Host Link Troubleshooting & Codes

This page summarizes common KEYENCE KV Host Link PLC errors for the PLC setup guide. It is not a complete manufacturer code table; use the KEYENCE manuals for formal definitions.

## PLC Codes

| Code | Typical cause | First check |
| --- | --- | --- |
| `E0` | Device number is invalid, outside range, or not available on the selected PLC model. | Check the address and selected canonical profile. |
| `E1` | Command is not supported by the selected PLC/model. Timer/counter preset writes are a common case on unsupported models. | Check the model profile and avoid unsupported write helpers. |
| `E2` | Program is not registered. | Check the PLC project/program state. |
| `E4` | Write is disabled by CPU protection, lock state, or project settings. | Check KV Studio and CPU write-protection settings. |
| `E5` | Unit error. | Check the PLC/unit error state. |
| `E6` | Comment data is not registered. | Check comment registration before using comment reads. |

## Common Symptoms

| Symptom | Likely cause | First check |
| --- | --- | --- |
| The connection times out immediately. | KV Host Link normally uses port `8501`, not the SLMP/Computerlink example port `1025`. | Confirm the port in the library options or Node-RED connection node. |
| A timer or counter preset write returns `E1`. | Host Link preset writes through `WS` / `WSS` are supported on KV-8000/7000-series, not on every KV model. | Do not write timer/counter presets on unsupported models; use timer/counter read helpers for monitoring. |
| `AT` is rejected or missing on KV-X500. | `AT` is not available in `keyence:kv-x500` or `keyence:kv-x500-xym`. | Check the selected profile before using `AT`. |
| `X` or `Y` is rejected or points look shifted. | `X` and `Y` use decimal-bank plus hexadecimal-bit notation, for example `X10F`. | Use the correct bank/bit notation and select an `-xym` profile when using XYM aliases. |
| `R`, `MR`, `LR`, or `CR` is rejected. | These bit-bank families use two-digit bit notation rather than one plain hexadecimal number. | Use forms such as `R200:BIT` or `MR100:BIT`. |
| `DM100.D` reads a bit instead of a 32-bit value. | Dot notation means bit-in-word access; `D` after the dot is bit 13. | Use the library's typed form such as `DM100:D` for unsigned 32-bit data. |
| `DM100.3,4` or a similar bit-in-word count is rejected. | Dot notation selects one bit inside one word and is scalar-only. | Use `DM100.3` for one bit, or use a direct bit family such as `R200:BIT,4` for bit arrays. |
| A write to `DM100:COMMENT` is rejected. | Device comments are read-only through the high-level Host Link helpers. | Use `:COMMENT` only with read helpers. |
| Expansion unit buffer access fails. | The selected unit number, buffer address, data format, or mounted module may not match the connected PLC hardware. | Verify the expansion unit number and buffer address before using expansion buffer helpers. |
| `CTH` or `CTC` appears in a catalog but fails as an input address. | `CTH` and `CTC` are catalog metadata rows for supported profiles. | Treat them as catalog metadata only. |
| A non-canonical profile string is rejected. | The profile catalog accepts exact canonical profile strings only. | Copy the exact profile string from the profile list or setup guide. |

## First Checks

- Confirm that Host Link / Upper Link communication is enabled on the PLC.
- Confirm the port number, protocol, and IP settings in the [KV PLC setup pages](../index.md).
- Confirm that the application selected the canonical profile for the actual PLC model.
- For write errors, check CPU protection, lock state, project settings, and RUN-time write permission where applicable.
