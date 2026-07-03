#!/usr/bin/env bash
# Apply SHA-25 Build Transparency panel into a local resume-website checkout.
# Run from the resume-website repo root:
#   bash /path/to/integrate-build-transparency.sh /path/to/AI-Workspace/resume-website
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <AI-Workspace/resume-website source> <resume-website repo root>"
  exit 1
fi

SRC="$1"
DEST="$2"

copy_tree() {
  local rel="$1"
  mkdir -p "$DEST/$(dirname "$rel")"
  cp -R "$SRC/$rel" "$DEST/$rel"
}

for rel in \
  src/components/build-transparency \
  src/lib/build-stats.ts \
  openspec/specs/build-transparency \
  openspec/changes/sha-25-build-transparency; do
  copy_tree "$rel"
done

echo ""
echo "Copied component, stats, and OpenSpec files."
echo ""
echo "Manual step — add to your production page (after Contact section):"
echo ""
cat <<'EOF'
import { BuildTransparency } from "@/components/build-transparency/BuildTransparency";
// ...
<BuildTransparency />
EOF
echo ""
echo "Update openspec/project.md capability index with build-transparency."
echo "Ensure voice-agent FAB z-index stays above the sheet (150+)."
