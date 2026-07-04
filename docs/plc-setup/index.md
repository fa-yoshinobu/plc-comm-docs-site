# PLC setup guide

Configure the PLC before using any communication library.
A **power cycle is required** after every parameter change.

For every protocol, choose and pass the canonical PLC profile explicitly when
opening a standard connection — the libraries do not infer it from the PLC.
The setup pages below list the profile to use for each model.

For MELSEC SLMP profile limits and end-code troubleshooting after the PLC-side
settings are correct, use the [SLMP profile reference](../slmp/profile-reference/index.md)
and [SLMP Troubleshooting & Codes](slmp/troubleshooting-codes.md).

## Supported models

| Protocol | Model | Connection type | Port |
|----------|-------|----------------|------|
| MELSEC SLMP | iQ-R | Built-in Ethernet | 1025 |
| MELSEC SLMP | iQ-F | Built-in Ethernet | 1025 |
| MELSEC SLMP | iQ-L | Built-in Ethernet | 1025 |
| MELSEC SLMP | MX-R | Built-in Ethernet | 1025 |
| MELSEC SLMP | MX-F | Built-in Ethernet | 1025 |
| MELSEC SLMP | QnUDV | Built-in Ethernet | 1025 |
| MELSEC SLMP | QnU | Built-in Ethernet | 1025 |
| MELSEC SLMP | LCPU | Built-in Ethernet | 1025 |
| MELSEC SLMP | RJ71EN71 | Communication unit | 1025 |
| MELSEC SLMP | QJ71E71-100 | Communication unit | 1025 |
| MELSEC SLMP | LJ71E71-100 | Communication unit | 1025 |
| KV Host Link | KV-X500 | Built-in Ethernet | 8501 |
| KV Host Link | KV-8000 | Built-in Ethernet | 8501 |
| KV Host Link | KV-7000 | Built-in Ethernet | 8501 |
| KV Host Link | KV-5000 | Built-in Ethernet | 8501 |
| KV Host Link | KV-XLE02 | Communication unit | 8501 |
| Computerlink | [TOYOPUC](computerlink/toyopuc.md) | Ethernet | 1025 |
| MC Protocol Serial | [MELSEC serial modules](mcprotocol/serial.md) | Serial module | *(serial)* |

## Protocol troubleshooting pages

These pages are shared by all language implementations for the same protocol.

| Protocol | Page |
|----------|------|
| MELSEC SLMP | [Troubleshooting & Codes](slmp/troubleshooting-codes.md) |
| KV Host Link | [Troubleshooting & Codes](kv/troubleshooting-codes.md) |
| Computerlink | [Troubleshooting & Codes](computerlink/troubleshooting-codes.md) |
| MC Protocol Serial | [Troubleshooting & Codes](mcprotocol/troubleshooting-codes.md) |

## Configuration tools

| Tool | Applies to |
|------|-----------|
| GX Works3 | MELSEC iQ-R, iQ-F, iQ-L, MX-R, MX-F, RJ71EN71 |
| GX Works2 | MELSEC Q series (QnUDV, QnU, QJ71E71-100), L series (LCPU, LJ71E71-100) |
| KV Studio | KEYENCE KV-X500, KV-8000, KV-7000, KV-5000, KV-XLE02 |

## Simulator connection notes

### GX Simulator 3

GX Simulator 3 uses IP `127.0.0.1` and port `5511` for SLMP over TCP.

The following parameter must be enabled:

- `Enable/Disable Online Change: Enable All (SLMP)`

Simulator model support:

- Model: iQ-R/iQ-L only

Verified with GX Works3 Version 1.125F.

### KV STUDIO Simulator

KV STUDIO Simulator uses IP `127.0.0.1` and port `8501` for Host Link over TCP.

Simulator model support:

- Model: KV-X500/KV-8000 only

Verified with KV STUDIO Ver.12.41.
