#!/usr/bin/env bash
# Publish only the built static site, without installing build dependencies.
set -euo pipefail

site_dir="$(cd -- "$1" && pwd -P)"
git_dir="$(git rev-parse --absolute-git-dir)"
readonly site_dir git_dir
readonly pages_ref=refs/heads/gh-pages

test -s "$site_dir/index.html"
# Keep the configured custom domain from the trusted source checkout.
cmp -- docs/CNAME "$site_dir/CNAME"
# Treat the downloaded artifact only as data, never as a Git checkout.
unsafe_path="$(find "$site_dir" \
  \( -iname .git -o -iname .gitmodules -o -iname .gitattributes -o -type l \) \
  -print -quit)"
if [[ -n "$unsafe_path" ]]; then
  echo "Unexpected Git metadata or symlink in site artifact." >&2
  exit 1
fi
: > "$site_dir/.nojekyll"

# Start with an empty index to remove obsolete pages and assets.
index_dir="$(mktemp -d)"
trap 'rm -rf -- "$index_dir"' EXIT
(
  cd -- "$site_dir"
  export GIT_INDEX_FILE="$index_dir/index"
  git --git-dir="$git_dir" --work-tree="$site_dir" add --all --force -- .
  git --git-dir="$git_dir" write-tree
) > "$index_dir/tree"
tree="$(cat "$index_dir/tree")"

parent=()
if git ls-remote --exit-code --heads origin "$pages_ref" > /dev/null; then
  git fetch --no-tags origin "$pages_ref"
  parent=(-p "$(git rev-parse FETCH_HEAD)")
else
  status=$?
  # Git returns 2 when the repository is accessible but the branch is absent.
  if [[ "$status" != 2 ]]; then
    exit "$status"
  fi
fi

source="$(git rev-parse HEAD)"
commit="$(git commit-tree "$tree" "${parent[@]}" -m "Deploy docs from $source")"
# The new commit inherits the current branch history. If another deployment
# wins a race, reject the non-fast-forward push instead of overwriting it.
git push origin "$commit:$pages_ref"
