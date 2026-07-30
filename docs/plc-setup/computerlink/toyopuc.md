---
description: "PLC-side setup checklist for JTEKT TOYOPUC controllers communicating over Computerlink."
---

# TOYOPUC Computerlink — PLC-side settings

This page provides the vendor-neutral minimum PLC-side checklist used by the
Computerlink libraries. Exact menu labels vary by TOYOPUC model and engineering
tool version; use the matching manufacturer manual for model-specific screens.

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

Model-specific screenshots are intentionally outside this minimum guide. Add
them only when a verified model/tool-version contribution is available.

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
