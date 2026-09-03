---
description: "Real-hardware measurements for the PLC communication libraries: every language and protocol run for one hour against a physical PLC on 2026-09-03, with the full test conditions."
---

# Performance

This project measures its libraries against real PLC hardware, not only against
simulators. On 2026-09-03 every published implementation was run for one hour
against a real PLC, writing one word and reading it back every cycle — all five
languages and all four protocols. The results are published so you can judge for
yourself whether these libraries are quick enough, and steady enough, for your
application.

Read them as one data point, not as a specification. Response time on a PLC
network is dominated by the PLC itself: CPU model, scan time, communication
settings, cabling, switch load, and how many other clients are attached all move
these numbers. Measure in your own installation before designing a control loop
around any specific value.

## Every implementation, one hour continuous (2026-09-03)

Each run held a single connection open and, every cycle, wrote one word and read
it back to confirm the value.

Conditions:

- One hour per run, one connection held open for the whole run, requests issued
  sequentially.
- One cycle = write one word, then read it back and compare. Send interval
  50 ms over TCP, 100 ms over serial.
- PLCs: MELSEC iQ-R (SLMP, TCP), KEYENCE KV-X500 (KV Host Link, TCP),
  JTEKT TOYOPUC Nano 10GX (Computerlink, TCP), and MELSEC over an RS serial
  module (MC Protocol Serial, 19,200 baud 8-E-1).
- Every run finished on elapsed time with **0 communication errors,
  0 value mismatches, and 0 reconnects**.

### SLMP — MELSEC iQ-R, TCP

| Language | Package | Cycles | Avg ms | p50 ms | p95 ms | p99 ms | Max ms † | Cycles/s | Process memory MB | Memory trend MB/h | CPU avg % |
|----------|---------|-------:|-------:|-------:|-------:|-------:|---------:|---------:|------------------:|------------------:|----------:|
| .NET | `PlcComm.Slmp` | 72,010 | 8.48 | 8.79 | 9.94 | 10.50 | 13.87 | 20.0 | 40.6 → 63.0 | 2.37 | 6.0 |
| Python | `plc-comm-slmp` | 71,596 | 9.72 | 9.73 | 10.45 | 10.59 | 24.87 | 19.9 | 30.3 → 33.9 | 3.62 \* | 2.8 |
| Rust | `plc-comm-slmp` | 70,077 | 8.82 | 8.88 | 9.33 | 9.44 | 13.25 | 19.5 | 4.3 → 5.5 | 0.68 | 1.2 |
| C++ | `fa-yoshinobu/slmp-connect-cpp-minimal` | 72,314 | 8.57 | 8.65 | 9.90 | 10.06 | 11.28 | 20.1 | 4.5 → 5.4 | 0.55 | 0.9 |
| Node-RED | `@fa_yoshinobu/node-red-contrib-plc-comm-slmp` | 71,834 | 9.34 | 9.69 | 10.16 | 10.72 | 12.53 | 20.0 | 69.7 → 103.2 | 3.55 | 2.5 |

### KV Host Link — KEYENCE KV-X500, TCP

| Language | Package | Cycles | Avg ms | p50 ms | p95 ms | p99 ms | Max ms † | Cycles/s | Process memory MB | Memory trend MB/h | CPU avg % |
|----------|---------|-------:|-------:|-------:|-------:|-------:|---------:|---------:|------------------:|------------------:|----------:|
| .NET | `PlcComm.KvHostLink` | 72,234 | 1.40 | 1.35 | 1.69 | 2.75 | 9.24 | 20.1 | 45.4 → 63.6 | 0.37 | 4.2 |
| Python | `plc-comm-kv-hostlink` | 71,592 | 2.57 | 2.59 | 2.90 | 3.04 | 7.10 | 19.9 | 29.1 → 32.7 | 3.63 \* | 1.9 |
| Rust | `plc-comm-kv-hostlink` | 70,068 | 1.62 | 1.62 | 1.83 | 2.32 | 5.44 | 19.5 | 4.1 → 5.4 | 0.66 | 1.1 |
| Node-RED | `@fa_yoshinobu/node-red-contrib-plc-comm-kvhostlink` | 71,929 | 2.55 | 2.50 | 3.05 | 3.42 | 5.26 | 20.0 | 66.9 → 100.4 | 9.01 | 2.4 |

### Computerlink — JTEKT TOYOPUC Nano 10GX, TCP

| Language | Package | Cycles | Avg ms | p50 ms | p95 ms | p99 ms | Max ms † | Cycles/s | Process memory MB | Memory trend MB/h | CPU avg % |
|----------|---------|-------:|-------:|-------:|-------:|-------:|---------:|---------:|------------------:|------------------:|----------:|
| .NET | `PlcComm.Toyopuc` | 72,035 | 16.07 | 16.15 | 17.16 | 19.66 | 25.47 | 20.0 | 43.0 → 62.7 | 0.58 | 7.1 |
| Python | `plc-comm-toyopuc` | 71,611 | 15.89 | 16.53 | 17.93 | 21.17 | 23.21 | 19.9 | 30.5 → 34.1 | 3.68 \* | 3.0 |

### MC Protocol Serial — MELSEC, RS serial 19,200 8-E-1

| Language | Package | Cycles | Avg ms | p50 ms | p95 ms | p99 ms | Max ms † | Cycles/s | Process memory MB | Memory trend MB/h | CPU avg % |
|----------|---------|-------:|-------:|-------:|-------:|-------:|---------:|---------:|------------------:|------------------:|----------:|
| C++ | `fa-yoshinobu/mcprotocol-serial-cpp` | 35,928 | 66.94 | 66.74 | 69.42 | 70.80 | 75.30 | 10.0 | 4.3 → 5.1 | 0.28 | 1.2 |

† **Max** is the worst single round-trip over minutes 5–60 of the run; the first
5-minute window is excluded from this column because every runtime shows a
larger startup outlier there. Averages and percentiles are over the full hour.

\* The Python runs recorded only 12–14 process-memory / CPU samples over the
hour, against roughly 130 for the other runtimes, so their **Memory trend** and
**CPU avg** figures are indicative only. Latency columns are sampled every cycle
and are unaffected.

### How to read this session

- **Protocol and link set the response time, not the language.** Median
  round-trip was about 1.3–2.6 ms for KV Host Link, 8.7–9.7 ms for SLMP, 16 ms
  for Computerlink, and 67 ms for MC Protocol Serial — at 19,200 baud a single
  serial frame simply takes that long on the wire. Rows in different tables talk
  to different PLCs over different links and are not comparable with each other.
- **Within one protocol the languages land close together.** SLMP medians span
  about 1 ms across all five clients; KV Host Link about 1.2 ms across four.
  Throughput tracked the send interval — roughly 20 cycles/s on TCP, 10 on
  serial — in every run. Choose the language that fits your runtime and your
  team, not the one that looks a hair quicker here.
- **Footprint follows the runtime.** End-of-run process memory was about
  4–5 MB for Rust and C++, 30–34 MB for Python, ~63 MB for .NET, and
  100–103 MB for Node-RED.
- **One hour is a leak check, not a soak.** Rust, C++ and most .NET runs stayed
  under 1 MB/h of memory growth; the Node-RED runs grew faster (up to about
  9 MB/h) as garbage collection cycled. An hour catches a fast leak; it does not
  prove long-term stability.

## What is not on this page

- **No comparisons against other vendors' libraries.** Cross-library benchmarks
  age quickly and depend on tuning choices this project cannot make fairly on
  someone else's behalf, so only its own measurements are published here.
- **No ranking of one implementation against another.** The tables record one
  run per protocol and client language, every one against a different PLC and
  transport. They document that every implementation runs clean, not which one
  you should prefer — choose the language that fits your stack.
- **No estimated or simulated figures.** Everything above was recorded against
  physical hardware on 2026-09-03; nothing is extrapolated.
