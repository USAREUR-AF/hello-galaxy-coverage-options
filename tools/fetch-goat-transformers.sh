#!/usr/bin/env bash
# Fetch goat-transformers at the commit in GOAT_TRANSFORMERS_REF into
# .cache/goat-transformers. Every stage runs goat-options and the Python engine
# from there. CI runs this same script.
#
#   GOAT_TRANSFORMERS_URL   where to fetch from (default: the public repository)
#   GOAT_TRANSFORMERS_REF   a commit to use in place of the file's
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
URL="${GOAT_TRANSFORMERS_URL:-https://github.com/USAREUR-AF/goat-transformers.git}"
REF="${GOAT_TRANSFORMERS_REF:-$(tr -d '[:space:]' < "$ROOT/GOAT_TRANSFORMERS_REF")}"
DEST="$ROOT/.cache/goat-transformers"
case "$REF" in
  *[!0-9a-f]*|"") echo "not a commit: '$REF'" >&2; exit 2 ;;
esac
[ "${#REF}" -eq 40 ] || { echo "not a full 40-character commit: '$REF'" >&2; exit 2; }
if [ -d "$DEST/.git" ] && [ "$(git -C "$DEST" rev-parse HEAD 2>/dev/null)" = "$REF" ]; then
  echo "goat-transformers $REF is already at .cache/goat-transformers"
  exit 0
fi
rm -rf "$DEST"
mkdir -p "$DEST"
git -C "$DEST" init -q
git -C "$DEST" fetch -q --depth 1 "$URL" "$REF"
git -C "$DEST" -c advice.detachedHead=false checkout -q FETCH_HEAD
echo "goat-transformers $(git -C "$DEST" rev-parse HEAD) from $URL at .cache/goat-transformers"
