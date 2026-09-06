---
description: "Device families supported by the MC Protocol Serial libraries on MELSEC serial targets."
---

# MC Protocol Serial Supported Registers

This page lists the current device-family support surface for MELSEC serial MC Protocol targets.

Profile-specific device-number ranges still depend on the PLC model, serial module parameters, route, and user program. The example addresses below show parser syntax; they are not range limits.

## Common Rules

| Rule | Behavior |
| --- | --- |
| Plain device strings | The high-level parser accepts plain device strings such as `D100`, `M100`, `X10`, `W100`, and `LZ0`. |
| Standalone `G` / `HG` | Not plain devices for any profile. Use qualified forms such as `Un\G` or `Un\HG` only when the selected profile supports that route. |
| `S` device | Not supported by this serial MC library. |
| Link-direct devices | Use dedicated `Jn\...` link-direct APIs when the selected profile supports them. |
| Qualified unit access | Use native-qualified `Un\G` / `Un\HG` APIs when the selected profile supports that route. The `0601/1601` helper route is profile/target-specific and must not be used as a fallback. |

## Profile Support Summary

### `melsec:iq-r`

| Support class | Device families |
| --- | --- |
| Plain bit read/write | `X`, `Y`, `M`, `L`, `SM`, `F`, `V`, `B`, `TS`, `TC`, `STS`, `STC`, `CS`, `CC`, `SB`, `DX`, `DY` |
| Plain word read/write | `D`, `SD`, `W`, `TN`, `STN`, `CN`, `SW`, `Z`, `R`, `RD`, `ZR` |
| Long-state helper | `LTS`, `LTC`, `LSTS`, `LSTC`, `LCS`, `LCC` |
| Native random double-word read/write | `LTN`, `LSTN`, `LCN`, `LZ` |
| Link-direct read/write | `Jn\X`, `Jn\Y`, `Jn\B`, `Jn\W`, `Jn\SB`, `Jn\SW` |
| Native-qualified read/write | `Un\G`, `Un\HG` |
| Not supported | `S` |

### `melsec:iq-l`

| Support class | Device families |
| --- | --- |
| Plain bit read/write | `X`, `Y`, `M`, `L`, `SM`, `F`, `V`, `B`, `TS`, `TC`, `STS`, `STC`, `CS`, `CC`, `SB`, `DX`, `DY` |
| Plain word read/write | `D`, `SD`, `W`, `TN`, `STN`, `CN`, `SW`, `Z`, `R`, `ZR` |
| Native-qualified read/write | `Un\G` |
| Not supported | `S`, `LTS`, `LTC`, `LSTS`, `LSTC`, `LCS`, `LCC`, `LTN`, `LSTN`, `LCN`, `LZ`, `RD`, `Un\HG` |
| Not confirmed | `Jn\X`, `Jn\Y`, `Jn\B`, `Jn\W`, `Jn\SB`, `Jn\SW` |

### `melsec:iq-f`

| Support class | Device families |
| --- | --- |
| Plain bit read/write | `X`, `Y`, `M`, `L`, `SM`, `F`, `B`, `TS`, `TC`, `STS`, `STC`, `CS`, `CC`, `SB` |
| Plain word read/write | `D`, `SD`, `W`, `TN`, `STN`, `CN`, `SW`, `Z`, `R` |
| Long counter state read/write | `LCS`, `LCC`; reads use the long-state helper |
| Native random double-word read/write | `LCN`, `LZ` |
| Native-qualified read/write | `Un\G` |
| Not supported | `S`, `V`, `ZR`, `DX`, `DY`, `LTS`, `LTC`, `LTN`, `LSTS`, `LSTC`, `LSTN`, `Un\HG`, `Jn\...`, monitor, host-buffer, and module-buffer helper routes |

### `melsec:qcpu`

| Support class | Device families |
| --- | --- |
| Plain bit read/write | `X`, `Y`, `M`, `L`, `SM`, `F`, `V`, `B`, `TS`, `TC`, `STS`, `STC`, `CS`, `CC`, `SB`, `DX`, `DY` |
| Plain word read/write | `D`, `SD`, `W`, `TN`, `STN`, `CN`, `SW`, `Z`, `R`, `ZR` |
| Link-direct read/write | `Jn\X`, `Jn\Y`, `Jn\B`, `Jn\W` |
| Link-direct read-only | `Jn\SB`, `Jn\SW` |
| Native-qualified read/write | `Un\G` |
| Not supported | `S`, `LTS`, `LTC`, `LSTS`, `LSTC`, `LCS`, `LCC`, `LTN`, `LSTN`, `LCN`, `LZ`, `RD`, `Un\HG` |

Native random read on tested Q targets can be narrower than batch access for some timer/counter status families. Treat random-read rejection as a command route limitation, not as a batch-read exclusion.

### `melsec:lcpu`

| Support class | Device families |
| --- | --- |
| Plain bit read/write | `X`, `Y`, `M`, `L`, `SM`, `F`, `V`, `B`, `TS`, `TC`, `STS`, `STC`, `CS`, `CC`, `SB`, `DX`, `DY` |
| Plain word read/write | `D`, `SD`, `W`, `TN`, `STN`, `CN`, `SW`, `Z`, `R`, `ZR` |
| Native-qualified read/write | `Un\G` |
| Expected but not locally confirmed | `Jn\X`, `Jn\Y`, `Jn\B`, `Jn\W`, `Jn\SB`, `Jn\SW` |
| Not supported | `S`, `LTS`, `LTC`, `LSTS`, `LSTC`, `LCS`, `LCC`, `LTN`, `LSTN`, `LCN`, `LZ`, `RD`, `Un\HG` |

Native random read on tested L targets can be narrower than batch access for some timer/counter status families. Treat random-read rejection as a command route limitation, not as a batch-read exclusion.

### `melsec:qna`, `melsec:ana-anu`, and `melsec:a`

These profiles select older command families and are maintained by manual-derived inference and codec-level tests until matching hardware is available. Do not promote a device inventory for these profiles without target evidence.

`melsec:a` is required for A-series extended file-register `ER/EW` paths. `melsec:qna` or `melsec:ana-anu` is required for QnA/AnA/AnU command-family paths such as direct extended file-register access.

## Bit Device Families

| Family | Kind | Example address | Notes |
| --- | --- | --- | --- |
| `X` | Input relay | `X10` | Hexadecimal address. |
| `Y` | Output relay | `Y10` | Hexadecimal address. |
| `M` | Internal relay | `M100` | Decimal address. |
| `L` | Latch relay | `L100` | Decimal address. |
| `SM` | Special relay | `SM100` | Decimal address. |
| `F` | Annunciator | `F100` | Decimal address. |
| `V` | Edge relay | `V100` | Decimal address. |
| `B` | Link relay | `B100` | Hexadecimal address. |
| `TS`, `TC` | Timer contact / coil | `TS0` | Decimal address. |
| `STS`, `STC` | Retentive timer contact / coil | `STS0` | Decimal address. |
| `CS`, `CC` | Counter contact / coil | `CS0` | Decimal address. |
| `SB` | Link special relay | `SB100` | Hexadecimal address. |
| `S` | Step relay | `S100` | Not supported by this serial MC library. |
| `DX`, `DY` | Direct access input/output | `DX10` | Hexadecimal address. |
| `LTS`, `LTC` | Long timer contact / coil | `LTS0` | Decimal address; profile-specific helper route. |
| `LSTS`, `LSTC` | Long retentive timer contact / coil | `LSTS0` | Decimal address; profile-specific helper route. |
| `LCS`, `LCC` | Long counter contact / coil | `LCS0` | Decimal address; profile-specific helper route. |

## Word Device Families

| Family | Kind | Example address | Notes |
| --- | --- | --- | --- |
| `D` | Data register | `D100` | Decimal address. |
| `SD` | Special register | `SD100` | Decimal address. |
| `W` | Link register | `W100` | Hexadecimal address. |
| `TN` | Timer current value | `TN0` | Decimal address. |
| `STN` | Retentive timer current value | `STN0` | Decimal address. |
| `CN` | Counter current value | `CN0` | Decimal address. |
| `SW` | Link special register | `SW100` | Hexadecimal address. |
| `LTN` | Long timer current value | `LTN0` | Decimal address; double-word in native random helpers. |
| `LSTN` | Long retentive timer current value | `LSTN0` | Decimal address; double-word in native random helpers. |
| `LCN` | Long counter current value | `LCN0` | Decimal address; double-word in native random helpers. |
| `LZ` | Long index register | `LZ0` | Decimal address; double-word in native random helpers. |
| `Z` | Index register | `Z0` | Decimal address. |
| `R` | File register | `R0` | Decimal address. |
| `RD` | Module access register | `RD0` | Decimal address. |
| `ZR` | File register | `ZR0` | Decimal address. |

## Addressing Notes

| Topic | Current behavior |
| --- | --- |
| Plain device string | Supported for profile-allowed plain devices. |
| Hexadecimal address families | `X`, `Y`, `B`, `W`, `SB`, `SW`, `DX`, and `DY` parse their numeric part as hexadecimal. |
| `:D` / `:F` suffix | Not supported by the current high-level parser. Use typed C++ fields such as `double_word` where available. |
| `.n` bit-in-word suffix | Not supported by the current high-level parser. |
| Long timer/counter state reads | Use `read_long_state_bits()` for supported long-state families. |
| Link-direct access | Use `read_link_direct_*()` / `write_link_direct_*()` helpers for supported `Jn\...` families. |
| Qualified unit access | Use `read_native_qualified_words()` / `write_native_qualified_words()` for supported `Un\G` / `Un\HG` families. |
| Trace logging | Set `MCPROTOCOL_SERIAL_TRACE=1` with the synchronous host client to log MC TX/RX frame bytes. |
