---
description: "Real-hardware measurements for the PLC communication libraries: every language and protocol run for an hour on 2026-09-03, an SLMP .NET/Rust latency deep-dive, and a five-hour continuous soak, each with its full test conditions."
---

# Performance

This project measures its libraries against real PLC hardware, not only against
simulators. Three sessions are published here:

- **Every implementation, one hour each (2026-09-03).** All five languages and
  all four protocols, writing one word and reading it back every cycle for an
  hour per run.
- **SLMP .NET / Rust deep-dive (2026-06-24).** The .NET and Rust SLMP clients
  over eight workload shapes, TCP versus UDP, with the full per-sample latency
  distribution.
- **Five-hour continuous soak (2026-07-19 to 2026-07-20).** Seven
  implementations held open at one cycle per second for five hours.

They are published so you can judge for yourself whether these libraries are
quick enough — and steady enough — for your application.

Read them as one data point, not as a specification. Response time on a PLC
network is dominated by the PLC itself: CPU model, scan time, communication
settings, cabling, switch load, and how many other clients are attached all move
these numbers. Measure in your own installation before designing a control loop
around any specific value. Each session ran on its own host under its own
conditions, so figures from different sessions are not directly comparable.

## Every implementation, one hour continuous (2026-09-03)

On 2026-09-03 every published implementation was run for one hour against real
PLC hardware. Each run held a single connection open and, every cycle, wrote one
word and read it back to confirm the value. This is the broadest of the three
sessions — all five languages, all four protocols — where the 2026-06-24
deep-dive below covers only the SLMP .NET and Rust clients but in more workload
detail.

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
  9 MB/h) as garbage collection cycled. For a real endurance answer see the
  5-hour soak below.

## SLMP .NET / Rust deep-dive (2026-06-24)

This earlier session profiles only the SLMP .NET and Rust clients, but over more
workload shapes than the all-implementations run above: eight request types,
TCP against UDP, and the full per-sample latency distribution.

### Measurement conditions

| Item | Value |
|------|-------|
| Date measured | 2026-06-24 |
| PLC | MELSEC iQ-R, built-in Ethernet port (`192.168.250.100`) |
| Protocol | SLMP, 4E frame, own station as target |
| Transports | TCP port 1025 (5 minutes) and UDP port 1035 (5 minutes) |
| Libraries measured | `plc-comm-slmp-dotnet` and `plc-comm-slmp-rust` |
| Test suite | 8 cases, repeated in a loop for the full duration |
| Per case | 200 measured iterations after 20 warmup iterations |
| Concurrency | 1 connection per case, requests issued sequentially |
| Timeouts | 2000 ms per operation, 20000 ms per case |

The eight cases in the suite:

| Case | What it does | Requests per iteration |
|------|--------------|-----------------------:|
| `latency-word-d1000-1` | Read 1 word from D1000 | 1 |
| `pair-sm400-d1000` | Read 1 bit from SM400, then 1 word from D1000 | 2 |
| `batch-word-d1000-64` | Read 64 consecutive words from D1000 | 1 |
| `bulk-word-d1000-960` | Read 960 consecutive words from D1000 | 1 |
| `dword-d1000-64` | Read 64 consecutive double words from D1000 | 1 |
| `random-read-dispersed-medium` | Dispersed read of scattered D devices | 1 |
| `write-word-d2000-64` | Write 64 words to D2000 | 1 |
| `write-verify-d2000-16` | Write 16 words to D2000, then read them back | 2 |

### Summary

Average time per iteration across the eight cases, with process-level resource
use recorded during the same run.

| Transport | Library | Avg ms/iter | Ops/sec | Failures | Process memory MB | CPU total % |
|-----------|---------|------------:|--------:|---------:|------------------:|------------:|
| TCP/1025 | .NET | 4.77 | 230.4 | 0 | 57.8 | 0.20 |
| TCP/1025 | Rust | 4.78 | 230.8 | 0 | 6.4 | 0.14 |
| UDP/1035 | .NET | 4.54 | 239.2 | 0 | 57.8 | 0.20 |
| UDP/1035 | Rust | 4.52 | 240.6 | 0 | 6.4 | 0.14 |

`Avg ms/iter` is the mean of the per-case averages; one iteration is one or two
requests depending on the case. Every case completed in both transports, and the
failure count was 0 in all four combinations.

### Sample distribution

Per-sample latency over the whole run, taken from the recorded time series
rather than from the per-case averages above.

| Transport | Library | Samples | Avg ms | P50 ms | P90 ms | P99 ms | Max ms |
|-----------|---------|--------:|-------:|-------:|-------:|-------:|-------:|
| TCP/1025 | .NET | 19,200 | 4.73 | 3.69 | 7.20 | 9.47 | 18.39 |
| TCP/1025 | Rust | 19,200 | 4.78 | 3.71 | 7.22 | 9.69 | 18.65 |
| UDP/1035 | .NET | 20,800 | 4.50 | 3.62 | 7.06 | 7.20 | 16.04 |
| UDP/1035 | Rust | 20,800 | 4.52 | 3.64 | 7.08 | 7.20 | 10.19 |

### How to read these numbers

A median of 3.62 ms to 3.71 ms, for a workload dominated by single-word reads,
says that the PLC's own turnaround sets the floor here — the same request costs
roughly the same regardless of which client sends it. UDP produced the tighter
tail in this session: P99 stayed at 7.20 ms for both clients, with maximums of
16.04 ms (.NET) and 10.19 ms (Rust), while TCP reached 9.47 ms and 9.69 ms at
P99 with maximums of 18.39 ms and 18.65 ms. The .NET and Rust clients landed
close enough — 0.01 ms to 0.02 ms apart on the per-iteration average — that
throughput is not a deciding factor when choosing between them; pick the one
that fits your stack. The process memory column is a reference figure rather
than a like-for-like comparison: the .NET value covers the whole benchmark
runner process, while the Rust value is a separate small client process started
per case. CPU stayed far below 1% in every combination, so it did not separate
the two either.

## Reliability: 5-hour continuous soak on real hardware

Latency answers how quickly one request returns. The other half of the question
is whether a client stays healthy when it is simply left running. On 2026-07-19
and 2026-07-20, every protocol and client language in this project was put
through a five-hour continuous soak against physical PLC hardware at one cycle
per second, and each run's raw summary was kept as the evidence behind the
table below.

This was a separate session on a different host from the benchmark above, so
the latency columns in this section are not comparable with the benchmark
figures earlier on the page. Read each session within its own conditions.

### Soak conditions

| Item | Value |
|------|-------|
| Dates measured | 2026-07-19 to 2026-07-20 |
| Duration per run | 5 hours (18,000 seconds) |
| Cycle rate | 1 cycle per second, requests issued sequentially |
| Per cycle | One typed word read over a single connection held open for the whole run |
| Runs | 7, one per protocol and client language |
| Runner host | A Linux host with 2 logical processors, one runner process per run |
| PLCs | MELSEC iQ-R (SLMP, TCP), KEYENCE KV-X500 (KV Host Link, TCP), JTEKT TOYOPUC (Computerlink, TCP), MELSEC QCPU (MC Protocol, serial) |
| Pass thresholds | Error rate 0.1%, P99 200 ms, mismatches 0, reconnect recovery 30 s, memory slope 1 MB/h, CPU 90% |

### Soak results

| Protocol | Client | Profile | Cycles | Errors | Mismatches | Reconnects | P50 ms | P99 ms | Memory slope MB/h | Status |
|----------|--------|---------|-------:|-------:|-----------:|-----------:|-------:|-------:|------------------:|--------|
| SLMP | .NET | `melsec:iq-r` | 17,999 | 0 | 0 | 0 | 3.24 | 5.21 | 0.312 | completed |
| SLMP | C++ | `melsec:iq-r` | 17,951 | 0 | 0 | 0 | 2.67 | 4.68 | 0.030 | completed |
| SLMP | Rust | `melsec:iq-r` | 17,953 | 0 | 0 | 0 | 3.13 | 5.18 | 0.074 | completed |
| KV Host Link | .NET | `keyence:kv-x500` | 17,996 | 0 | 0 | 0 | 0.81 | 1.88 | 0.362 | completed |
| KV Host Link | Rust | `keyence:kv-x500` | 17,953 | 0 | 0 | 0 | 0.85 | 1.05 | 0.076 | completed |
| Computerlink | .NET | `toyopuc:nano-10gx:compatible` | 18,002 | 0 | 0 | 0 | 7.67 | 10.27 | 0.407 | completed |
| MC Protocol Serial | C++ | `melsec:qcpu` | 17,313 | 0 | 0 | 0 | 32.51 | 33.06 | 0.032 | completed |

Every run ended because its five hours elapsed, not because anything failed:
errors, mismatches, and reconnects were **0 in all seven runs**. The memory
slope — a least-squares regression over sampled process memory, with the
initial warm-up window discarded — stayed **below 1 MB/h in all seven runs**,
the highest being 0.407 MB/h. Cycle counts differ slightly between rows because
each runner drives its own one-second interval; the fixed quantity is the
18,000-second run length, not the cycle total.

### How to read the soak numbers

Seven implementations ran for five hours each without a single communication
error, mismatch, or dropped-and-reopened connection, and none of them showed a
memory growth trend over the run. That is the property this session was after:
long unattended operation with no slow leak and no accumulating failure.

The rows are not comparable with each other as client measurements — each one
talks to a different PLC over a different protocol and transport, so the latency
spread is a property of the link, not of the client. MC Protocol Serial sits
near 32.5 ms at P50 because moving a frame over a serial line at its configured
baud rate takes that long; KV Host Link reads land under 1 ms because
that is how quickly the KV-X500 turns a request around; the Ethernet SLMP and
Computerlink rows fall between the two. As with the benchmark session, treat
these as one data point under one set of conditions and measure your own
installation before designing a control loop around a specific value.

## What is not on this page

- **No comparisons against other vendors' libraries.** Cross-library benchmarks
  age quickly and depend on tuning choices this project cannot make fairly on
  someone else's behalf, so only its own measurements are published here.
- **No ranking of one implementation against another.** The 2026-09-03 tables
  and the soak table each record one run per protocol and client language, every
  one against a different PLC and transport. They document that every
  implementation runs clean, not which one you should prefer — choose the
  language that fits your stack.
- **No estimated or simulated figures.** Everything above was recorded against
  physical hardware in the three sessions described; nothing is extrapolated.
