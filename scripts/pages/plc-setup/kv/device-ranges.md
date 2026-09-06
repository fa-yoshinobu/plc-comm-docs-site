---
description: "Device families, address notation, and range reference for KEYENCE KV Host Link communication."
---

# KV Host Link Device Ranges

This page is the shared device-family, address-notation, and range reference for the KV Host Link libraries.

These tables are for profile selection, UI address pickers, model-specific display, and pre-checks in applications that need a range catalog. They are not a guarantee that every address can be read or written on every connected PLC. The actual PLC model, project settings, mounted units, protection settings, and Host Link command support can still reject a request.

## Device Families

### Word device families

| Family | Notation | Example | Notes |
| --- | --- | --- | --- |
| `DM` | Decimal | `DM0:U` | General data memory. Start here for first reads. |
| `EM` | Decimal | `EM0:U` | Extended data memory on profiles that provide EM ranges. |
| `FM` | Decimal | `FM0:U` | File memory on profiles that provide FM ranges. |
| `ZF` | Decimal | `ZF0:U` | File register area on profiles that provide ZF ranges. |
| `W` | Hexadecimal | `W0:U` | Link register word area. |
| `CM` | Decimal | `CM0:U` | Control memory word area. |
| `TM` | Decimal | `TM0:U` | Timer-related word area. |
| `VM` | Decimal | `VM0:U` | Variable memory word area; not available on KV-X500 profiles. |
| `D` | Decimal | `D0:U` | XYM-style alias for `DM`. |
| `E` | Decimal | `E0:U` | XYM-style alias for `EM`. |
| `F` | Decimal | `F0:U` | XYM-style alias for `FM`. |
| `Z` | Decimal | `Z1:D` | Index registers. KV-X500 profiles expose `Z1` through `Z10`; other profiles expose `Z1` through `Z12`. |

### Bit device families

| Family | Notation | Example | Notes |
| --- | --- | --- | --- |
| `R` | Decimal bank plus two decimal bit digits | `R200:BIT` | Relay bits. Low two digits are bit `00` through `15`. |
| `B` | Hexadecimal | `B0000:BIT` | Link relay bits. |
| `MR` | Decimal bank plus two decimal bit digits | `MR100:BIT` | Internal relay bits. |
| `LR` | Decimal bank plus two decimal bit digits | `LR100:BIT` | Latch relay bits. |
| `CR` | Decimal bank plus two decimal bit digits | `CR100:BIT` | Control relay bits. |
| `VB` | Hexadecimal | `VB0:BIT` | Variable memory bits; not available on KV-X500 profiles. |
| `X` | Decimal bank plus hex bit | `X10F:BIT` | Input alias in XYM profiles. |
| `Y` | Decimal bank plus hex bit | `Y10F:BIT` | Output alias in XYM profiles. |
| `M` | Decimal | `M0:BIT` | Internal relay alias in XYM profiles. |
| `L` | Decimal | `L0:BIT` | Latch relay alias in XYM profiles. |

### Timer, counter, and catalog rows

| Family | Category | Example | Notes |
| --- | --- | --- | --- |
| `T` | Timer | `T0:D` | Timer preset/current composite in high-level helpers. |
| `TC` | Timer | `TC0:D` | Timer current/contact family where exposed by the library. |
| `TS` | Timer | `TS0:BIT` | Timer contact/status family where exposed by the library. |
| `C` | Counter | `C0:D` | Counter preset/current composite in high-level helpers. |
| `CC` | Counter | `CC0:D` | Counter current/contact family where exposed by the library. |
| `CS` | Counter | `CS0:BIT` | Counter contact/status family where exposed by the library. |
| `AT` | Timer/counter catalog category | `AT0:D` | Digital trimmer. Not available on KV-NANO or KV-X500 profiles. |
| `CTH` | Catalog metadata | `CTH0` | High-speed counter row on some profiles. Catalog entry only; not accepted by high-level address parsers. |
| `CTC` | Catalog metadata | `CTC0` | High-speed counter row on some profiles. Catalog entry only; not accepted by high-level address parsers. |

## Type Suffixes

| Form | Example | Meaning |
| --- | --- | --- |
| `:U` | `DM100:U` | Unsigned 16-bit word. |
| `:S` | `DM100:S` | Signed 16-bit word. |
| `:D` | `DM100:D` | Unsigned 32-bit double word. |
| `:L` | `DM100:L` | Signed 32-bit double word. |
| `:F` | `DM100:F` | IEEE 754 32-bit floating-point value. |
| `:H` | `DM100:H` | Hexadecimal 16-bit word text. |
| `:BIT` | `R200:BIT` | Direct bit device value. |
| `:COMMENT` | `DM100:COMMENT` | PLC device comment text. |
| `.n` | `DM100.A` | Bit `n` inside a word, where `n` is hexadecimal `0` through `F`. |

High-level address text should include the intended type. Use `DM100:U`, not plain `DM100`, when reading an unsigned word.

## Addressing Notes

| Topic | Rule |
| --- | --- |
| `X` and `Y` notation | Use decimal bank digits followed by one hexadecimal bit digit, such as `X10F`. Do not treat the whole value as one decimal number. |
| `R`, `MR`, `LR`, and `CR` notation | Use two decimal bit digits for the low bit position, such as `R200:BIT`, `MR115:BIT`, or `CR7915:BIT`. The low two digits must be `00` through `15`. |
| `AT` restriction | `AT` exists only on KV-3000, KV-5000, KV-7000, and KV-8000 catalog profiles. High-level write helpers can reject it before sending. |
| Catalog-only rows | `CTH` and `CTC` appear in some range catalogs but are not accepted as high-level address input. |
| Default port | KV Host Link commonly uses port `8501` unless the PLC configuration says otherwise. |

## Standard Catalog

| DeviceType | Base | KV-NANO | KV-3000 | KV-5000 | KV-7000 | KV-8000 | KV-X500 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R | 10 | R00000-R59915 | R00000-R99915 | R00000-R99915 | R00000-R199915 | R00000-R199915 | R00000-R199915 |
| B | 16 | B0000-B1FFF | B0000-B3FFF | B0000-B3FFF | B0000-B7FFF | B0000-B7FFF | B0000-B7FFF |
| MR | 10 | MR00000-MR59915 | MR00000-MR99915 | MR00000-MR99915 | MR000000-MR399915 | MR000000-MR399915 | MR000000-MR399915 |
| LR | 10 | LR00000-LR19915 | LR00000-LR99915 | LR00000-LR99915 | LR00000-LR99915 | LR00000-LR99915 | LR00000-LR99915 |
| CR | 10 | CR0000-CR8915 | CR0000-CR3915 | CR0000-CR3915 | CR0000-CR7915 | CR0000-CR7915 | CR0000-CR7915 |
| CM | 10 | CM0000-CM8999 | CM0000-CM5999 | CM0000-CM5999 | CM0000-CM5999 | CM0000-CM7599 | CM0000-CM7599 |
| T | 10 | T0000-T0511 | T0000-T3999 | T0000-T3999 | T0000-T3999 | T0000-T3999 | T0000-T3999 |
| C | 10 | C0000-C0255 | C0000-C3999 | C0000-C3999 | C0000-C3999 | C0000-C3999 | C0000-C3999 |
| DM | 10 | DM00000-DM32767 | DM00000-DM65534 | DM00000-DM65534 | DM00000-DM65534 | DM00000-DM65534 | DM00000-DM65534 |
| EM | 10 | - | EM00000-EM65534 | EM00000-EM65534 | EM00000-EM65534 | EM00000-EM65534 | EM00000-EM65534 |
| FM | 10 | - | FM00000-FM32767 | FM00000-FM32767 | FM00000-FM32767 | FM00000-FM32767 | FM00000-FM32767 |
| ZF | 10 | - | ZF000000-ZF131071 | ZF000000-ZF131071 | ZF000000-ZF524287 | ZF000000-ZF524287 | ZF000000-ZF524287 |
| W | 16 | W0000-W3FFF | W0000-W3FFF | W0000-W3FFF | W0000-W7FFF | W0000-W7FFF | W0000-W7FFF |
| TM | 10 | TM000-TM511 | TM000-TM511 | TM000-TM511 | TM000-TM511 | TM000-TM511 | TM000-TM511 |
| VM | 10 | VM0-9999 | VM0-59999 | VM0-59999 | VM0-63999 | VM0-589823 | - |
| VB | 16 | VB0-1FFF | VB0-3FFF | VB0-3FFF | VB0-F9FF | VB0-F9FF | - |
| Z | 10 | Z1-12 | Z1-12 | Z1-12 | Z1-12 | Z1-23 | Z1-10 |
| CTH | 10 | CTH0-3 | CTH0-1 | CTH0-1 | - | - | - |
| CTC | 10 | CTC0-7 | CTC0-3 | CTC0-3 | - | - | - |
| AT | 10 | - | AT0-7 | AT0-7 | AT0-7 | AT0-7 | - |

## XYM Catalog

| DeviceType | Base | KV-NANO(XYM) | KV-3000(XYM) | KV-5000(XYM) | KV-7000(XYM) | KV-8000(XYM) | KV-X500(XYM) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R | 10 | X0-599F,Y0-599F | X0-999F,Y0-999F | X0-999F,Y0-999F | X0-1999F,Y0-1999F | X0-1999F,Y0-1999F | X0-1999F,Y0-1999F |
| B | 16 | B0000-B1FFF | B0000-B3FFF | B0000-B3FFF | B0000-B7FFF | B0000-B7FFF | B0000-B7FFF |
| MR | 10 | M0-9599 | M0-15999 | M0-15999 | M000000-M63999 | M000000-M63999 | M000000-M63999 |
| LR | 10 | L0-3199 | L0-15999 | L0-15999 | L00000-L15999 | L00000-L15999 | L00000-L15999 |
| CR | 10 | CR0000-CR8915 | CR0000-CR3915 | CR0000-CR3915 | CR0000-CR7915 | CR0000-CR7915 | CR0000-CR7915 |
| CM | 10 | CM0000-CM8999 | CM0000-CM5999 | CM0000-CM5999 | CM0000-CM5999 | CM0000-CM7599 | CM0000-CM7599 |
| T | 10 | T0000-T0511 | T0000-T3999 | T0000-T3999 | T0000-T3999 | T0000-T3999 | T0000-T3999 |
| C | 10 | C0000-C0255 | C0000-C3999 | C0000-C3999 | C0000-C3999 | C0000-C3999 | C0000-C3999 |
| DM | 10 | D0-32767 | D0-65534 | D0-65534 | D00000-D65534 | D00000-D65534 | D00000-D65534 |
| EM | 10 | - | E0-65534 | E0-65534 | E00000-E65534 | E00000-E65534 | E00000-E65534 |
| FM | 10 | - | F0-32767 | F0-32767 | F00000-F32767 | F00000-F32767 | F00000-F32767 |
| ZF | 10 | - | ZF000000-ZF131071 | ZF000000-ZF131071 | ZF000000-ZF524287 | ZF000000-ZF524287 | ZF000000-ZF524287 |
| W | 16 | W0000-W3FFF | W0000-W3FFF | W0000-W3FFF | W0000-W7FFF | W0000-W7FFF | W0000-W7FFF |
| TM | 10 | TM000-TM511 | TM000-TM511 | TM000-TM511 | TM000-TM511 | TM000-TM511 | TM000-TM511 |
| VM | 10 | VM0-9999 | VM0-59999 | VM0-59999 | VM0-63999 | VM0-589823 | - |
| VB | 16 | VB0-1FFF | VB0-3FFF | VB0-3FFF | VB0-F9FF | VB0-F9FF | - |
| Z | 10 | Z1-12 | Z1-12 | Z1-12 | Z1-12 | Z1-23 | Z1-10 |
| CTH | 10 | CTH0-3 | CTH0-1 | CTH0-1 | - | - | - |
| CTC | 10 | CTC0-7 | CTC0-3 | CTC0-3 | - | - | - |
| AT | 10 | - | AT0-7 | AT0-7 | AT0-7 | AT0-7 | - |
