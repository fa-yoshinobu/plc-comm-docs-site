# plc-comm Package Matrix

This page maps each maintained plc-comm library to its registry package and install command.

Python package names changed in v2.0.0, but import names stay the same: `slmp`, `hostlink`, and `toyopuc`. Rust package names changed in v2.0.0, and the Rust import paths are `plc_comm_slmp` and `plc_comm_kv_hostlink`.

| Protocol | Language | Repository | Registry package | Install command |
| --- | --- | --- | --- | --- |
| Computerlink | .NET | [plc-comm-computerlink-dotnet](https://github.com/fa-yoshinobu/plc-comm-computerlink-dotnet) | NuGet: `PlcComm.Toyopuc` | `dotnet add package PlcComm.Toyopuc` |
| Computerlink | Python | [plc-comm-computerlink-python](https://github.com/fa-yoshinobu/plc-comm-computerlink-python) | PyPI: `plc-comm-toyopuc` | `pip install plc-comm-toyopuc` |
| KV Host Link | .NET | [plc-comm-hostlink-dotnet](https://github.com/fa-yoshinobu/plc-comm-hostlink-dotnet) | NuGet: `PlcComm.KvHostLink` | `dotnet add package PlcComm.KvHostLink` |
| KV Host Link | Python | [plc-comm-hostlink-python](https://github.com/fa-yoshinobu/plc-comm-hostlink-python) | PyPI: `plc-comm-kv-hostlink` | `pip install plc-comm-kv-hostlink` |
| KV Host Link | Rust | [plc-comm-hostlink-rust](https://github.com/fa-yoshinobu/plc-comm-hostlink-rust) | crates.io: `plc-comm-kv-hostlink` | `cargo add plc-comm-kv-hostlink` |
| KV Host Link | Node-RED | [node-red-contrib-plc-comm-kvhostlink](https://github.com/fa-yoshinobu/node-red-contrib-plc-comm-kvhostlink) | npm: `@fa_yoshinobu/node-red-contrib-plc-comm-kvhostlink` | `npm install @fa_yoshinobu/node-red-contrib-plc-comm-kvhostlink` |
| SLMP | .NET | [plc-comm-slmp-dotnet](https://github.com/fa-yoshinobu/plc-comm-slmp-dotnet) | NuGet: `PlcComm.Slmp` | `dotnet add package PlcComm.Slmp` |
| SLMP | Python | [plc-comm-slmp-python](https://github.com/fa-yoshinobu/plc-comm-slmp-python) | PyPI: `plc-comm-slmp` | `pip install plc-comm-slmp` |
| SLMP | Rust | [plc-comm-slmp-rust](https://github.com/fa-yoshinobu/plc-comm-slmp-rust) | crates.io: `plc-comm-slmp` | `cargo add plc-comm-slmp` |
| SLMP | C++ (Arduino/PlatformIO) | [plc-comm-slmp-cpp-minimal](https://github.com/fa-yoshinobu/plc-comm-slmp-cpp-minimal) | PlatformIO: `fa-yoshinobu/slmp-connect-cpp-minimal` | `fa-yoshinobu/slmp-connect-cpp-minimal@^4.0.1` |
| SLMP | Node-RED | [node-red-contrib-plc-comm-slmp](https://github.com/fa-yoshinobu/node-red-contrib-plc-comm-slmp) | npm: `@fa_yoshinobu/node-red-contrib-plc-comm-slmp` | `npm install @fa_yoshinobu/node-red-contrib-plc-comm-slmp` |
| MC Protocol Serial | C++ (Arduino/PlatformIO) | [plc-comm-mcprotocol-serial-cpp](https://github.com/fa-yoshinobu/plc-comm-mcprotocol-serial-cpp) | PlatformIO: `fa-yoshinobu/mcprotocol-serial-cpp` | `fa-yoshinobu/mcprotocol-serial-cpp@^3.2.1` |
