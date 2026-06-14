# Site management

## Architecture

This repo does not permanently store source documentation content.
It collects Markdown files from 11 source repos at build time and publishes HTML to GitHub Pages.

```text
Source repo (docsrc/user/*.md or docs/*.md)
  -> push to main
  -> triggers repository_dispatch to plc-comm-docs-site
  -> deploy.yml runs
  -> collects all current Markdown files from all 11 repos
  -> mkdocs build
  -> publishes to GitHub Pages (gh-pages branch)
```

## Source repos and their doc locations

| Repo | Docs location | Collected to |
|------|--------------|--------------|
| plc-comm-computerlink-dotnet | docsrc/user/ | docs/computerlink/dotnet/ |
| plc-comm-computerlink-python | docsrc/user/ | docs/computerlink/python/ |
| plc-comm-hostlink-dotnet | docsrc/user/ | docs/hostlink/dotnet/ |
| plc-comm-hostlink-python | docsrc/user/ | docs/hostlink/python/ |
| plc-comm-hostlink-rust | docs/ | docs/hostlink/rust/ |
| node-red-contrib-plc-comm-kvhostlink | docsrc/user/ | docs/hostlink/nodered/ |
| plc-comm-slmp-dotnet | docsrc/user/ | docs/slmp/dotnet/ |
| plc-comm-slmp-python | docsrc/user/ | docs/slmp/python/ |
| plc-comm-slmp-rust | docs/ | docs/slmp/rust/ |
| plc-comm-slmp-cpp-minimal | docsrc/user/ | docs/slmp/cpp/ |
| node-red-contrib-plc-comm-slmp | docsrc/user/ | docs/slmp/nodered/ |

## How to trigger a rebuild manually

Go to Actions -> Deploy docs -> Run workflow.

## How to add a new page to the site

1. Add the Markdown file to the source repo under `docsrc/user/` or `docs/` for Rust repos.
2. Add the page to `nav:` in `mkdocs.yml` in this repo.
3. Push both changes. The CI will rebuild the site after the source repo dispatches the event.

## How to add a new source repo

1. Add a `git clone` line for the new repo in `deploy.yml`.
2. Add a `copy_docs` line for the new repo's docs folder.
3. Add the new repo's pages to `nav:` in `mkdocs.yml`.
4. Add the `repository_dispatch` trigger job to the new repo's CI.
5. Register `DOCS_REPO_TOKEN` as a secret in the new repo.

## Required secrets

| Secret | Where to set | Purpose |
|--------|-------------|---------|
| `DOCS_REPO_TOKEN` | Each of the 11 source repos | Allows source repos to trigger this repo's CI |

Token type: GitHub fine-grained personal access token.
Required permission: `Contents: write` on `plc-comm-docs-site`.

The source workflows skip the dispatch step when `DOCS_REPO_TOKEN` is not set, so normal CI can stay green before the manual secret setup is complete.

## Local preview

```bash
pip install mkdocs-material
# Collect docs manually from source repos first, then:
mkdocs serve
```

## Files in this repo

| File | Purpose |
|------|---------|
| `mkdocs.yml` | Site structure and theme config |
| `docs/index.md` | Top-level landing page |
| `.github/workflows/deploy.yml` | Collects docs and deploys to GitHub Pages |
| `SITE_MANAGEMENT.md` | Maintainer guide for this repo |
| `TODO.md` | Pending manual setup tasks |
