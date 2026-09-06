# SLMP Profile Reference

This section is built from the canonical `plc-comm-slmp-profiles` data repository during the documentation build.

Use it when you need to compare MELSEC SLMP profiles across the supported built-in Ethernet and Ethernet unit profiles.

For normal library usage, select the PLC profile in the library or Node-RED connection settings and follow that library's getting started guide.

For PLC-side Binary data code, port/open settings, and RUN-time write permission, use the [MELSEC SLMP PLC Setup Guide](../../plc-setup/index.md).

## Pages

| Page | Use it for |
| --- | --- |
| [Parameters](parameters.md) | Compare frame defaults, feature decisions, point limits, write policy, and device availability across profiles. |
| [Device ranges](device-ranges.md) | Check SD-derived range rules, fixed ranges, probe markers, and unsupported device families. |

## Scope

The profile data covers CPU built-in Ethernet ports and verified Ethernet unit routes. Base profiles can be used internally for inherited address and device-range behavior even when they are not selectable connection profiles.

Device range rules are not send/receive address guards for communication libraries. They are for applications that need to discover or display the valid device range of a selected PLC profile.
