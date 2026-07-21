#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="$ROOT/../previews/SHA-25-build"
BASE_PATH="/previews/SHA-25-build"

cd "$ROOT"
rm -rf out "$OUT_DIR"

PREVIEW_BASE_PATH="$BASE_PATH" npm run build

mkdir -p "$(dirname "$OUT_DIR")"
cp -r out/. "$OUT_DIR/"

echo "Preview static export written to previews/SHA-25-build/"
echo "Local path: file://$OUT_DIR/index.html"
