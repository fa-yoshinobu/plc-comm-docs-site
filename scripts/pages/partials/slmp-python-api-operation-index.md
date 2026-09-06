## Operation Index

The sync `SlmpClient` and async `AsyncSlmpClient` expose the same low-level
operation names unless noted otherwise.

### Direct And Random Device Operations

| Operation | Public API |
| --- | --- |
| Direct `DeviceAddress` parsing | `DeviceRef(code, number, plc_profile)`, `parse_device(value, plc_profile=...)`, `str(ref)` |
| Typed `AddressSpec` parsing | `SlmpAddress`, `parse_address`, `try_parse_address`, `format_address`, `normalize_address` |
| Direct device read/write | `read_devices`, `write_devices` |
| 32-bit values | `read_dword`, `write_dword`, `read_dwords`, `write_dwords` |
| Float32 values | `read_float32`, `write_float32`, `read_float32s`, `write_float32s` |
| Extended direct device read/write | `read_devices_extended`, `write_devices_extended` |
| Random read | `read_random` |
| Extended random read | `read_random_extended` |
| Random word/dword write | `write_random_words` |
| Extended random word/dword write | `write_random_words_extended` |
| Random bit write | `write_random_bits` |
| Extended random bit write | `write_random_bits_extended` |
| Block read/write | `read_block`, `write_block` |
| Type name | `read_type_name` |

Extended random APIs use the 008x subcommands. Use qualified device notation
such as `U1\G0`, `U3E0\HG0`, or `J2\SW10` where the route requires it.

### Specialized Operations

| Operation | Public API |
| --- | --- |
| Monitor registration/cycle | `register_monitor_devices`, `register_monitor_devices_extended`, `run_monitor_cycle` |
| Label array access | `read_array_labels`, `write_array_labels` |
| Label random access | `read_random_labels`, `write_random_labels` |
| Remote CPU control | `remote_run`, `remote_stop`, `remote_pause`, `remote_latch_clear`, `remote_reset` |
| Remote password | `remote_password_unlock`, `remote_password_lock` |
| Self-test loopback | `self_test_loopback` |
| Clear Error | `clear_error` |
| Latest self-diagnosis error code | `read_latest_self_diagnosis_error_code` |

### High-Level Helpers

| Operation | Public API |
| --- | --- |
| Connection helper | `open_and_connect`, `open_and_connect_sync` |
| Typed values | `read_typed`, `write_typed` |
| Named mixed snapshots | `read_named`, `write_named`, `poll` |
| Single-request word/dword reads | `read_words_single_request`, `read_dwords_single_request` |
| Address handling | `normalize_address`, `parse_address`, `try_parse_address`, `format_address` |
| Bit-in-word write | `write_bit_in_word` |
