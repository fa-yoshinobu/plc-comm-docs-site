# plc-comm-docs-site

Unified documentation site for the PLC communication libraries.
Published at: https://fa-yoshinobu.github.io/plc-comm-docs-site/

## What this repo is

This repo does not contain documentation content.
It collects `.md` files from 11 source repos at build time,
builds a [MkDocs](https://squidfunk.github.io/mkdocs-material/) site,
and publishes the HTML to GitHub Pages.

## Source libraries

| Protocol | Hardware | Languages |
|----------|----------|-----------|
| Computerlink | JTEKT TOYOPUC | .NET, Python |
| Host Link (KV) | KEYENCE KV series | .NET, Python, Rust, Node-RED |
| SLMP | MELSEC iQ-R/F/L, Q, L | .NET, Python, Rust, C++, Node-RED |

## How it works

1. A source repo pushes to `main`
2. Its CI sends a `repository_dispatch` event to this repo
3. `deploy.yml` collects `.md` files from all 11 source repos
4. MkDocs builds the site
5. HTML is published to the `gh-pages` branch

## For maintainers

See [SITE_MANAGEMENT.md](SITE_MANAGEMENT.md) for architecture details,
how to add pages, and how to add new source repos.

See [TODO.md](TODO.md) for pending manual setup steps.
