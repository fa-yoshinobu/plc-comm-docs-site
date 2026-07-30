---
description: "Measured SLMP latency and throughput from a physical MELSEC iQ-R, with the full test conditions for the .NET and Rust clients over TCP and UDP."
---

# Performance

This project measures its libraries against real PLC hardware, not only against
simulators. The figures on this page come from a benchmark session run on
2026-06-24 against a physical MELSEC iQ-R, and they are published so you can
judge for yourself whether these libraries are quick enough for your
application.

Read them as one data point, not as a specification. Response time on a PLC
network is dominated by the PLC itself: CPU model, scan time, communication
settings, cabling, switch load, and how many other clients are attached all move
these numbers. Measure in your own installation before designing a control loop
around any specific value.

## Measurement conditions

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

## Summary

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

## Sample distribution

Per-sample latency over the whole run, taken from the recorded time series
rather than from the per-case averages above.

| Transport | Library | Samples | Avg ms | P50 ms | P90 ms | P99 ms | Max ms |
|-----------|---------|--------:|-------:|-------:|-------:|-------:|-------:|
| TCP/1025 | .NET | 19,200 | 4.73 | 3.69 | 7.20 | 9.47 | 18.39 |
| TCP/1025 | Rust | 19,200 | 4.78 | 3.71 | 7.22 | 9.69 | 18.65 |
| UDP/1035 | .NET | 20,800 | 4.50 | 3.62 | 7.06 | 7.20 | 16.04 |
| UDP/1035 | Rust | 20,800 | 4.52 | 3.64 | 7.08 | 7.20 | 10.19 |

## How to read these numbers

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

## What is not on this page

- **No comparisons against other vendors' libraries.** Cross-library benchmarks
  age quickly and depend on tuning choices this project cannot make fairly on
  someone else's behalf, so only its own measurements are published here.
- **No long-duration soak results yet.** A long-run stability measurement is in
  preparation and will be added once its evidence is complete, in the same
  conditions-first format.
- **No estimated or simulated figures.** Everything above was recorded against
  physical hardware in a single session; nothing is extrapolated.
