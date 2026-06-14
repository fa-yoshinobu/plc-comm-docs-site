# TODO

## Manual steps required after setup

- [ ] Create a GitHub fine-grained personal access token with `Contents: write`
      permission on `plc-comm-docs-site`
- [ ] Add the token as `DOCS_REPO_TOKEN` secret in each of the 11 source repos:
  - [ ] plc-comm-computerlink-dotnet
  - [ ] plc-comm-computerlink-python
  - [ ] plc-comm-hostlink-dotnet
  - [ ] plc-comm-hostlink-python
  - [ ] plc-comm-hostlink-rust
  - [ ] node-red-contrib-plc-comm-kvhostlink
  - [ ] plc-comm-slmp-dotnet
  - [ ] plc-comm-slmp-python
  - [ ] plc-comm-slmp-rust
  - [ ] plc-comm-slmp-cpp-minimal
  - [ ] node-red-contrib-plc-comm-slmp
- [x] Enable GitHub Pages on `plc-comm-docs-site` (Settings -> Pages -> Source: gh-pages branch)
- [ ] Disable GitHub Pages on each source repo that currently publishes its own site:
  - [ ] plc-comm-computerlink-dotnet
  - [ ] plc-comm-hostlink-dotnet
  - [ ] plc-comm-slmp-dotnet
  - [ ] plc-comm-slmp-rust

## After token setup

- [x] Trigger a manual deploy (Actions -> Deploy docs -> Run workflow)
- [x] Verify all 11 repos' pages appear on the site
- [x] Verify `repository_dispatch` deploy path in `plc-comm-docs-site`
- [ ] Run GOAL_CLEANUP_DOCFX.md to remove DocFX artifacts from source repos

## Current blockers for fully automatic rebuilds

- [ ] `DOCS_REPO_TOKEN` is not configured in the 11 source repos yet.
      Until it is configured, the trigger job logs a notice and skips the
      `repository_dispatch` call so normal CI remains green.
      See `SITE_MANAGEMENT.md` for the exact `gh secret set` loop.
