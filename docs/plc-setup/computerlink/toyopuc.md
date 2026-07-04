# TOYOPUC Computerlink — PLC-side settings

This setup page is under preparation.

Before using the Computerlink libraries, configure the PLC side so that
Computerlink communication is enabled and the Ethernet port matches the library
connection settings.

## Current minimum checklist

| Item | Setting |
|------|---------|
| Computerlink communication | Enabled on the PLC side |
| TCP port | Match the library setting; examples use `1025` |
| UDP port | Match the library setting when UDP is used; examples use `1035` |
| Network settings | Align IP address, subnet mask, and default gateway with your network |
| After parameter changes | Power cycle the PLC if the PLC/tool requires it |

Detailed model-specific screenshots and setting names will be added later.

## Connecting with this library

| Parameter | Example value |
|-----------|---------------|
| Host | `192.168.250.100` |
| TCP port | `1025` |
| UDP port | `1035` |
| Canonical profile | `toyopuc:plus:extended` |

Pass the canonical profile explicitly. The standard connection helpers do not
infer it from the PLC.

## Troubleshooting

- [Computerlink Troubleshooting & Codes](troubleshooting-codes.md)
