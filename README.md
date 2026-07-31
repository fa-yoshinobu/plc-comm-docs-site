# PLC Communication Libraries

Documentation hub for the PLC communication libraries.

[Open the documentation site](https://fa-yoshinobu.github.io/plc-comm-docs-site/)

![PLC Communication Libraries](docs/assets/plc-communication-libraries.png)

This site collects setup guides, supported PLC profiles, device/register notes,
sample workflows, and release-oriented documentation for the PLC communication
libraries maintained under the `fa-yoshinobu` GitHub account.

The documentation is organized by protocol and implementation language, so each
library can stay focused while users still have one entry point for comparing
protocols and finding the right package.

## What You Can Find

| Area | Contents |
|------|----------|
| PLC setup | Practical connection settings for supported PLC families and modules |
| Library docs | Getting started guides, usage notes, API references, supported profiles, and samples |
| Communication verification | Current live-device verification summaries and limitations |
| Reliability validation | Generated results for exact library artifacts tested on real PLC hardware |
| Release navigation | Links to package registries, source repositories, and published docs |

## Source Libraries

| Protocol | Hardware | Languages |
|----------|----------|-----------|
| Computerlink | JTEKT TOYOPUC | .NET, Python |
| KV Host Link | KEYENCE KV series | .NET, Python, Rust, Node-RED |
| SLMP | MELSEC iQ-R/F/L, Q, L | .NET, Python, Rust, C++, Node-RED |
| MC Protocol Serial | MELSEC iQ-R/L, Q, A (RS-232C/RS-485) | C++ |

## How This Repo Works

This repository builds the public site with
[MkDocs Material](https://squidfunk.github.io/mkdocs-material/). Most page
content is collected from the source library repositories during deployment.
Python API reference pages are generated with mkdocstrings from the installed
PyPI release packages during the site build.
Real-hardware reliability results are generated from the hashed public evidence
under `evidence/validation-results`; current package versions are not copied into
the page by hand.

## Deployment Flow

Publishing is manual: after source-repo docs change, a maintainer runs
Actions -> Deploy docs -> Run workflow in this repo.

1. A maintainer runs the `Deploy docs` workflow (or pushes a change to this repo)
2. `deploy.yml` collects `.md` files from all 12 source repos
3. MkDocs builds the site
4. HTML is published to the `gh-pages` branch

## For maintainers

See [SITE_MANAGEMENT.md](SITE_MANAGEMENT.md) for architecture details,
how to add pages, and how to add new source repos.

See [TODO.md](TODO.md) for pending manual setup steps.
