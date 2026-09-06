---
description: "Common TOYOPUC Computerlink response errors, their likely causes, and how to resolve them."
---

# Computerlink Troubleshooting & Codes

This page summarizes TOYOPUC Computerlink response errors that users commonly see. It is not a complete manufacturer code table; use the JTEKT TOYOPUC manuals for formal definitions.

## First Checks

- Confirm that Computerlink communication is enabled on the PLC side.
- Confirm the TCP/UDP port and network settings in the [TOYOPUC setup page](toyopuc.md).
- For UDP, confirm that the PC local UDP port matches the port in the PLC Other Node Table.
- Confirm that the application selected the exact canonical TOYOPUC profile.
- For write errors, check PLC run/write permission and protection settings before retrying.
- For relay access, configure the relay hops explicitly; relay topology is not auto-discovered.

## Connection Checks

| Symptom | First check |
| --- | --- |
| Connection timeout | Confirm the PLC host address and the configured Computerlink port. TCP examples use `1025`. |
| TCP connection refused | Confirm Computerlink is enabled on the target PLC and the TCP port is open. |
| UDP requests do not return | Confirm the PLC UDP port and bind the PC local UDP port to the value configured in the PLC Other Node Table. |
| Intermittent timeouts | Increase timeout/retry settings, reuse a connection, and avoid reconnecting for every small request. |

## Addressing Checks

| Symptom | First check |
| --- | --- |
| Profile rejected before communication | Use one exact canonical profile from the library's PLC Profiles page. |
| Unknown device area | Confirm that the selected profile supports that family. |
| Address out of range | Compare the selected profile with the shared [Computerlink Device Ranges](device-ranges.md) page. |
| Basic address rejected | Use `P1-`, `P2-`, or `P3-` for basic families such as `D`, `M`, `X`, `Y`, `T`, `C`, `L`, `N`, `R`, and `S`. |
| Dword read returns a bit | Use `:D` for dword access and `.D` only for bit 13 inside a word. |

## Write Checks

| Symptom | First check |
| --- | --- |
| A write appears to change the wrong value | Stop and confirm that you are using a test address you control. |
| FR value does not survive power cycle | Stage the FR write and then commit it when persistence is intended. |
| Relay write or read does not reach the target PLC | Set the relay hop string explicitly. |

## Common PLC Codes

| Code | Typical cause | First check |
| --- | --- | --- |
| `0x40` | Address or address plus count is outside the CPU range. This is also the common result when FR is not exposed on the tested unit. | Check the selected profile, address range, and count. |
| `0x24` | Subcommand is not supported by the CPU or routed target. | Check whether the feature exists on that CPU; for example some targets reject `A0`. |
| `0x23` | Command code is not supported. | Check the selected helper and profile. |
| `0x31` | Write or function call is prohibited while the sequence is running. | Check PLC run/write settings before retrying. |
| `0x34` | Access is prohibited by configuration. | Check PLC communication and protection settings. |
| `0x41` | Word or byte count is outside the permitted range. | Split the request or reduce the count. |
| `0x52` | Timer/counter set-value and current-value command type do not match. | Check whether the helper targets a preset or current value. |
| `0x66`, `0x70`, `0x72` | Relay link module did not answer or could not execute the request. | Check relay hops and the target PLC path. |
| `0x73` | Relay command collision on the same link module; retry is appropriate. | Retry after a short delay or reduce concurrent relay access. |
| `0x11` | CPU module hardware failure. | Check the PLC CPU status before continuing. |
