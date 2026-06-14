# TODO

## Manual steps required after setup

- [x] Create a GitHub fine-grained personal access token with `Contents: write`
      permission on `plc-comm-docs-site`
- [x] Add the token as `DOCS_REPO_TOKEN` secret in each of the 11 source repos (existing):
- [x] Add `DOCS_REPO_TOKEN` secret to repo 12: `plc-comm-mcprotocol-serial-cpp`
  - [x] plc-comm-computerlink-dotnet
  - [x] plc-comm-computerlink-python
  - [x] plc-comm-hostlink-dotnet
  - [x] plc-comm-hostlink-python
  - [x] plc-comm-hostlink-rust
  - [x] node-red-contrib-plc-comm-kvhostlink
  - [x] plc-comm-slmp-dotnet
  - [x] plc-comm-slmp-python
  - [x] plc-comm-slmp-rust
  - [x] plc-comm-slmp-cpp-minimal
  - [x] node-red-contrib-plc-comm-slmp
- [x] Enable GitHub Pages on `plc-comm-docs-site` (Settings -> Pages -> Source: gh-pages branch)
- [x] Disable GitHub Pages on each source repo that was publishing its own site:
  - [x] plc-comm-computerlink-dotnet
  - [x] plc-comm-computerlink-python
  - [x] plc-comm-hostlink-dotnet
  - [x] plc-comm-hostlink-python
  - [x] plc-comm-slmp-dotnet
  - [x] plc-comm-slmp-python
  - [x] plc-comm-slmp-rust
  - [x] plc-comm-slmp-cpp-minimal

## After token setup

- [x] Trigger a manual deploy (Actions -> Deploy docs -> Run workflow)
- [x] Verify all 11 repos' pages appear on the site
- [ ] Verify `plc-comm-mcprotocol-serial-cpp` pages appear on the site after adding it
- [x] Disable GitHub Pages on `plc-comm-mcprotocol-serial-cpp`
- [x] Verify `repository_dispatch` deploy path in `plc-comm-docs-site`
- [x] Verify a source repo `docsrc/user` push triggers `plc-comm-docs-site`
- [x] Run GOAL_CLEANUP_DOCFX.md to remove DocFX artifacts from source repos

## Fully automatic rebuilds

- [x] `DOCS_REPO_TOKEN` is configured in the 11 source repos.
- [x] `plc-comm-computerlink-python` doc push triggered source CI.
- [x] Source CI `trigger-docs-rebuild` called `repository_dispatch`.
- [x] `plc-comm-docs-site` built and deployed from that dispatch.
