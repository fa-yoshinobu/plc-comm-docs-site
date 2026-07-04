# KV Host Link Error Codes

This page summarizes common KEYENCE KV Host Link PLC errors for the PLC setup guide. It is not a complete manufacturer code table; use the KEYENCE manuals for formal definitions.

## PLC Error Codes

| Code | Typical cause | First check |
| --- | --- | --- |
| `E0` | Device number is invalid, outside range, or not available on the selected PLC model. | Check the address and selected canonical profile. |
| `E1` | Command is not supported by the selected PLC/model. Timer/counter preset writes are a common case on unsupported models. | Check the model profile and avoid unsupported write helpers. |
| `E2` | Program is not registered. | Check the PLC project/program state. |
| `E4` | Write is disabled by CPU protection, lock state, or project settings. | Check KV Studio and CPU write-protection settings. |
| `E5` | Unit error. | Check the PLC/unit error state. |
| `E6` | Comment data is not registered. | Check comment registration before using comment reads. |

## First Checks

- Confirm that Host Link / Upper Link communication is enabled on the PLC.
- Confirm the port number, protocol, and IP settings in the [KV PLC setup pages](../index.md).
- Confirm that the application selected the canonical profile for the actual PLC model.
- For write errors, check CPU protection, lock state, project settings, and RUN-time write permission where applicable.
