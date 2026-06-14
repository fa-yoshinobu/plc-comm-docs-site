# Site management

## Architecture

This repo does not permanently store source documentation content.
It collects Markdown files from 12 source repos at build time and publishes HTML to GitHub Pages.

```text
Source repo (docsrc/user/*.md or docs/*.md)
  -> push to main
  -> triggers repository_dispatch to plc-comm-docs-site
  -> deploy.yml runs
  -> collects all current Markdown files from all 12 repos
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
| plc-comm-mcprotocol-serial-cpp | docsrc/user/ | docs/mcprotocol/cpp/ |

## How to trigger a rebuild manually

Go to Actions -> Deploy docs -> Run workflow.

## How to add a new page to the site

1. Add the Markdown file to the source repo under `docsrc/user/` or `docs/` for Rust repos.
2. Add the page to `nav:` in `mkdocs.yml` in this repo.
3. Push both changes. The CI will rebuild the site after the source repo dispatches the event.

## README maintenance policy

Keep each source repository README as a stable entrance page. When README points
to another page, that linked page becomes the maintained detail page and must
carry the actual table, cautions, and evidence.

README should usually contain only:

- badges
- title and one-sentence purpose
- short links to the maintained `PROFILES.md`, `SUPPORTED_REGISTERS.md`, and verification pages
- installation command
- one minimal quick example
- documentation links
- license and registry table

Do not delete detail from README unless the same detail is already present in a
linked docs page or is moved there in the same change. Large PLC profile tables,
device-range tables, and live-device verification matrices should live in the
linked docs pages so README stays stable without becoming an empty signpost.

## How to add a new source repo

1. Add a `git clone` line for the new repo in `deploy.yml`.
2. Add a `copy_docs` line for the new repo's docs folder.
3. Add the new repo's pages to `nav:` in `mkdocs.yml`.
4. Add the `repository_dispatch` trigger job to the new repo's CI.
5. Register `DOCS_REPO_TOKEN` as a secret in the new repo.

## Required secrets

| Secret | Where to set | Purpose |
|--------|-------------|---------|
| `DOCS_REPO_TOKEN` | Each of the 12 source repos | Allows source repos to trigger this repo's CI |

Token type: GitHub fine-grained personal access token.
Required permission: `Contents: write` on `plc-comm-docs-site`.

The source workflows skip the dispatch step when `DOCS_REPO_TOKEN` is not set, so normal CI can stay green before the manual secret setup is complete.

## Registering `DOCS_REPO_TOKEN`

Use a fine-grained personal access token that is limited to `plc-comm-docs-site`
with `Contents: write`. Avoid reusing a broad `repo` token unless you accept that
larger blast radius.

After creating the token, set it in every source repo:

```powershell
$repos = @(
  "plc-comm-computerlink-dotnet",
  "plc-comm-computerlink-python",
  "plc-comm-hostlink-dotnet",
  "plc-comm-hostlink-python",
  "plc-comm-hostlink-rust",
  "node-red-contrib-plc-comm-kvhostlink",
  "plc-comm-slmp-dotnet",
  "plc-comm-slmp-python",
  "plc-comm-slmp-rust",
  "plc-comm-slmp-cpp-minimal",
  "node-red-contrib-plc-comm-slmp",
  "plc-comm-mcprotocol-serial-cpp"
)

foreach ($repo in $repos) {
  gh secret set DOCS_REPO_TOKEN --repo "fa-yoshinobu/$repo"
}
```

When prompted by `gh`, paste the token value. The token is stored as an Actions
secret in each source repo and is not committed to git.

To verify registration:

```powershell
foreach ($repo in $repos) {
  gh secret list --repo "fa-yoshinobu/$repo" | Select-String "^DOCS_REPO_TOKEN\s"
}
```

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
| `README.md` | Short repository overview |
| `SITE_MANAGEMENT.md` | Maintainer guide for this repo |
| `TODO.md` | Pending manual setup tasks |
