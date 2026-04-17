#!/usr/bin/env bash
# Build the Claude Desktop Extension (.mcpb) bundle for Outlook.
#
# Prerequisites:
#   - Node.js + npx (for @anthropic-ai/mcpb)
#   - uv (for on-demand Pillow to convert the icon)
#
# Output: outlook-<version>.mcpb in the repo root.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

VERSION=$(grep -E '"version"\s*:' dxt/manifest.json | head -1 | sed -E 's/.*"version"\s*:\s*"([^"]+)".*/\1/')
OUTPUT="outlook-${VERSION}.mcpb"

echo "==> Cleaning bundle"
rm -rf dxt/server dxt/icon.*
mkdir -p dxt/server/src

echo "==> Staging server code into dxt/server/"
cp outlook/pyproject.toml dxt/server/pyproject.toml
cp -r outlook/src/outlook_mcp dxt/server/src/outlook_mcp
# Remove __pycache__ copied from live dev tree
find dxt/server -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

echo "==> Preparing icon (must be PNG for .mcpb)"
if [[ -f icon.png ]]; then
  cp icon.png dxt/icon.png
elif [[ -f icon.jpg ]]; then
  echo "    converting icon.jpg -> dxt/icon.png via uv + pillow"
  uv run --with pillow python -c "from PIL import Image; Image.open('icon.jpg').convert('RGBA').save('dxt/icon.png')"
else
  echo "    no icon found; bundle will have no icon"
fi

echo "==> Packing bundle as ${OUTPUT}"
npx --yes @anthropic-ai/mcpb pack dxt "${OUTPUT}"

echo ""
echo "Built: ${OUTPUT}"
ls -la "${OUTPUT}"
