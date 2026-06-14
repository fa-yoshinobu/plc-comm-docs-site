# PLC Communication Libraries

A set of libraries for communicating with industrial PLCs over TCP/UDP.

| Protocol | Hardware | Languages |
|----------|----------|-----------|
| [Computerlink](computerlink/dotnet/GETTING_STARTED.md) | JTEKT TOYOPUC | .NET, Python |
| [Host Link (KV)](hostlink/dotnet/GETTING_STARTED.md) | KEYENCE KV series | .NET, Python, Rust, Node-RED |
| [SLMP](slmp/dotnet/GETTING_STARTED.md) | Mitsubishi iQ-R/F/L, Q, L | .NET, Python, Rust, C++, Node-RED |

## Connection settings used in all examples

| Protocol | Host | TCP port | UDP port |
|----------|------|----------|----------|
| SLMP / Computerlink | 192.168.250.100 | 1025 | 1035 |
| KV Host Link | 192.168.250.100 | 8501 | 8501 |
