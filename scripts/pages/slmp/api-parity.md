# SLMP API Parity

This page summarizes the user-facing SLMP operation surface across the maintained implementations. It is a navigation aid, not a live verification record.

Legend:

- `yes`: implemented in the public low-level/client library surface.
- `gap`: intentionally not implemented in that library today; the note explains the current boundary.
- `n/a`: not a normal target for that implementation's scope.

## Five-Implementation Snapshot

Snapshot date: 2026-09-03.

| Operation family | Python | .NET | C++ minimal | Rust | Node-RED |
| --- | --- | --- | --- | --- | --- |
| Address concepts | `DeviceRef` / `parse_device`; `SlmpAddress` / `parse_address` | `SlmpAddress`; `SlmpAddressSpec` | `DeviceAddress` helpers; `AddressSpec` helpers | `SlmpAddress` / `parse_device`; `NamedAddressParts` / `parse_named_address` | `parseDevice` / `deviceToString`; `parseAddress` / `formatParsedAddress` |
| Direct word/bit read/write | yes: `read_devices` / `write_devices` | yes: `ReadWordsAsync` / `WriteWordsAsync` / bit variants | yes: `readWords` / `writeWords` / bit variants | yes: `read_words` / `write_words` / bit variants | yes: `readDevices` / `writeDevices` |
| Dword / float32 helpers | yes | yes | yes | yes | yes: `readDWordsSingleRequest` / `readFloat32s` and existing write helpers |
| Extended direct word/bit read/write | yes: `read_devices_extended` / `write_devices_extended` | yes: `ReadWordsExtendedAsync` / `WriteWordsExtendedAsync` / bit variants | yes: `readWordsExtended` / `writeWordsExtended` / bit variants | yes: `read_words_extended` / `write_words_extended` / bit variants | yes: `readWordsExtended` / `writeWordsExtended` / bit variants |
| Random read | yes: `read_random` | yes: `ReadRandomAsync` | yes: `readRandom` | yes: `read_random` | yes: `readRandom` |
| Extended random read | yes: `read_random_extended` | yes: `ReadRandomExtendedAsync` | yes: `readRandomExtended` | yes: `read_random_extended` | yes: `readRandomExtended` |
| Random word/dword write | yes: `write_random_words` | yes: `WriteRandomWordsAsync` | yes: `writeRandomWords` | yes: `write_random_words` | yes: `writeRandomWords` |
| Extended random word/dword write | yes: `write_random_words_extended` | yes: `WriteRandomWordsExtendedAsync` | yes: `writeRandomWordsExtended` | yes: `write_random_words_extended` | yes: `writeRandomWordsExtended` |
| Random bit write | yes: `write_random_bits` | yes: `WriteRandomBitsAsync` | yes: `writeRandomBits` | yes: `write_random_bits` | yes: `writeRandomBits` |
| Extended random bit write | yes: `write_random_bits_extended` | yes: `WriteRandomBitsExtendedAsync` | yes: `writeRandomBitsExtended` | yes: `write_random_bits_extended` | yes: `writeRandomBitsExtended` |
| Block read/write | yes: `read_block` / `write_block` | yes: `ReadBlockAsync` / `WriteBlockAsync` | yes: `readBlock` / `writeBlock` | yes: `read_block` / `write_block` | yes: `readBlock` / `writeBlock` |
| Type name | yes: `read_type_name` | yes: `ReadTypeNameAsync` | yes: `readTypeName` | yes: `read_type_name` | yes: `readTypeName` |
| Monitor register/cycle | yes | yes | yes | yes | yes |
| Qualified iQ-R CPU-buffer `U3En\HG` access | yes: extended-device API with explicit request target | yes: extended-device API with explicit request target | yes: extended-device API with explicit request target | yes: extended-device API with explicit request target | yes: extended-device API with explicit request target |
| Multiple long timer reads | yes | yes | yes | yes | yes: `readLongTimer` / `readLongRetentiveTimer` |
| Latest self-diagnosis error code (`SD0`) | yes | yes | yes | yes | yes |
| Label array read/write | yes | yes | yes | yes | yes |
| Label random read/write | yes | yes | yes | yes | yes |
| Remote CPU control | yes | yes | yes | yes | yes |
| Remote password lock/unlock | yes | yes | yes | yes | yes |
| Self-test loopback | yes | yes | yes | yes | yes |
| Clear Error | yes | yes | yes | yes | yes |

The command-specific Memory and Extend Unit APIs are not public. Use the semantic qualified extended-device APIs for supported module-buffer, CPU-buffer, and link-direct access. Node-RED editor nodes do not need to surface every JavaScript client API; this table tracks the JavaScript client surface used by the nodes.

## Out-of-Scope Node Functions

SLMP node-function commands in the `0x0E3x` family, including NodeSearch,
IPAddressSet, ParameterGet/Set, StatusRead, and CommunicationSettingGet, are
outside the maintained library surfaces. These libraries target MELSEC CPU
SLMP server communication for PLC data access and setup-compatible operation;
they do not implement a node-function server-management surface. NodeSearch
and IPAddressSet are also send-prohibited by project policy because they can
discover or alter network identity outside normal PLC data access workflows.

See the [SLMP Troubleshooting & Codes guide](../plc-setup/slmp/troubleshooting-codes.md#node-function-end-codes)
for the related node-function end-code category.
