# Computerlink Device Ranges

This page is the shared device-family, address-notation, and practical range reference for the TOYOPUC Computerlink libraries.

These tables are for profile selection, UI address pickers, model-specific display, and pre-checks in applications that need a range catalog. They are not a guarantee that every address can be read or written on every connected PLC. The actual PLC model, link route, project settings, and run/write permission can still reject a request.

## Device Families

### Bit device families

| Family | Access | Example | Notes |
| --- | --- | --- | --- |
| `P` | Prefixed | `P1-P0000` | Shared relay family; profile ranges may include upper split ranges. |
| `K` | Prefixed | `P1-K0000` | Keep relay family. |
| `V` | Prefixed | `P1-V0000` | Profile-dependent split ranges. |
| `T` | Prefixed | `P1-T0000` | Timer bit family. |
| `C` | Prefixed | `P1-C0000` | Counter bit family. |
| `L` | Prefixed | `P1-L0000` | Link relay family; profile ranges may include upper split ranges. |
| `X` | Prefixed | `P1-X0000` | Input relay family. |
| `Y` | Prefixed | `P1-Y0000` | Output relay family. |
| `M` | Prefixed | `P1-M0000` | Internal relay family; profile ranges may include upper split ranges. |
| `EP` | Direct extension | `EP0000` | Extended P bit family. |
| `EK` | Direct extension | `EK0000` | Extended K bit family. |
| `EV` | Direct extension | `EV0000` | Extended V bit family. |
| `ET` | Direct extension | `ET0000` | Extended T bit family. |
| `EC` | Direct extension | `EC0000` | Extended C bit family. |
| `EL` | Direct extension | `EL0000` | Extended L bit family. |
| `EX` | Direct extension | `EX0000` | Extended X bit family. |
| `EY` | Direct extension | `EY0000` | Extended Y bit family. |
| `EM` | Direct extension | `EM0000` | Extended M bit family. |
| `GM` | Direct extension | `GM0000` | Global M bit family where the selected profile enables it. |
| `GX` | Direct extension | `GX0000` | Global X bit family where the selected profile enables it. |
| `GY` | Direct extension | `GY0000` | Global Y bit family where the selected profile enables it. |

### Word device families

| Family | Access | Example | Notes |
| --- | --- | --- | --- |
| `S` | Prefixed | `P1-S0000` | Special register family. |
| `N` | Prefixed | `P1-N0000` | File register word family. |
| `R` | Prefixed | `P1-R0000` | Register word family. |
| `D` | Prefixed | `P1-D0000` | Data register family. |
| `B` | Direct | `B0000` | Direct word area where the selected profile enables it. |
| `ES` | Direct extension | `ES0000` | Extended special register family. |
| `EN` | Direct extension | `EN0000` | Extended file register family. |
| `H` | Direct extension | `H0000` | Extended H word family. |
| `U` | Direct extension | `U00000` | Profile and addressing options select standard or PC10 routing. |
| `EB` | Direct extension | `EB00000` | Extended block word family where the selected profile enables it. |
| `FR` | Direct FR | `FR000000` | File-register flash area with two-phase write semantics. |

## Type Suffixes

| Form | Example | Meaning |
| --- | --- | --- |
| No suffix or `:U` | `P1-D0100` | Unsigned 16-bit word. |
| `:S` | `P1-D0100:S` | Signed 16-bit word. |
| `:D` | `P1-D0100:D` | Unsigned 32-bit dword from two words. |
| `:L` | `P1-D0100:L` | Signed 32-bit long from two words. |
| `:F` | `P1-D0100:F` | IEEE 754 32-bit floating point value from two words. |
| `.n` | `P1-D0100.3` | Bit `n` inside a word, where `n` is hexadecimal `0` through `F`. |
| `W` | `P1-M0010W` | 16-bit packed view of a bit family. |
| `L` / `H` | `P1-M0010L` | Low or high byte view of a bit family. |

## Addressing Rules

| Rule | Correct form |
| --- | --- |
| Basic families require a program prefix. | `P1-D0000`, `P2-M0000`, `P3-S0000` |
| Extension families are direct. | `ES0000`, `EP0000`, `U00000`, `FR000000` |
| Data type views use a colon. | `P1-D0100:D` |
| Bit-in-word views use a dot. | `P1-D0100.D` means bit 13. |
| Packed bit-area views append the packed unit. | `P1-M0010W`, `P1-M0010L`, `P1-M0010H` |
| FR writes are explicit. | Stage an FR write, then commit when persistence is intended. |

## Practical Writable Ranges

These are writable-range summaries from project evidence, not a complete hardware manual.

### TOYOPUC-Plus CPU with Plus EX2

| Area | Writable range summary |
| --- | --- |
| Basic bit | `P0000-P17FF`, `K0000-K02FF`, `V/T/C/M0000-17FF`, `L0000-L2FFF`, `X/Y0000-07FF` |
| Basic word | `S0000-S13FF`, `N0000-N17FF`, `R0000-R07FF`, `D0000-D0FFF`; `B` is not writable |
| Prefixed bit | `P1/P2/P3-P000-P1FF`, `K000-K2FF`, `V/T/C000-C1FF`, `L000-L7FF`, `X/Y000-X7FF`, `M000-M7FF` |
| Prefixed word | `P1/P2/P3-S0000-S03FF`, `N0000-N01FF`, `R0000-R07FF`, `D0000-D0FFF`; `B` is not writable |
| Extension bit | `EP/EK/EV0000-0FFF`, `ET/EC/EX/EY0000-07FF`, `EL0000-1FFF`, `EM0000-1FFF`, `GX/GY/GM0000-FFFF` |
| Extension word | `ES/EN/H0000-07FF`, `U00000-U07FFF`; `EB` is not present |
| FR | Not exposed on this CPU |

### Nano 10GX

| Area | Writable range summary |
| --- | --- |
| Basic bit | `P/K/V/T/C/L/X/Y/M` standard ranges |
| Basic word | `S0000-S13FF`, `N0000-N17FF`, `R0000-R07FF`, `D0000-D2FFF`; `B` is not present |
| Prefixed bit | `P1/P2/P3` standard ranges |
| Prefixed word | `S0000-S13FF`, `N0000-N17FF`, `R0000-R07FF`, `D0000-D2FFF`; upper prefixed `1000` series are not implemented |
| Extension | Standard `EP/EK/EV/ET/EC/EL/EX/EY/EM`, `GX/GY/GM`, `ES/EN/H`; `U00000-U1FFFF` in PC10 mode |
| FR | `FR000000-FR1FFFFF` when the CPU/configuration exposes FR |

### PC10G-CPU

| Area | Writable range summary |
| --- | --- |
| Basic bit | `P0000-P17FF`, `K0000-K02FF`, `V/T/C/M0000-17FF`, `L0000-L2FFF`, `X/Y0000-07FF` |
| Basic word | `S0000-S13FF`, `N0000-N17FF`, `R0000-R07FF`, `D0000-D2FFF` |
| Prefixed bit | `P1/P2/P3` standard ranges, including the upper `1000` series on this CPU |
| Prefixed word | `S0000-S13FF`, `N0000-N17FF`, `R0000-R07FF`, `D0000-D2FFF` |
| Extension bit | `EP/EK/EV0000-0FFF`, `ET/EC/EX/EY0000-07FF`, `EL0000-1FFF`, `EM0000-1FFF`, `GX/GY/GM0000-FFFF` |
| Extension word | `ES/EN/H0000-07FF`, `U00000-U1FFFF`, `EB00000-EB3FFFF` |
| FR | Not exposed on the tested PC10G unit |

## Range Notes

- A profile can make an address syntactically valid while the connected PLC still rejects it because of hardware, mode, project configuration, or route.
- FR writes are persistent operations. Use dedicated FR helpers only on test addresses you control.
