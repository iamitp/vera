#!/usr/bin/env bash
# Vera one-line installer.
# curl -sSf https://raw.githubusercontent.com/iamitp/vera/main/install.sh | bash
set -euo pipefail

if ! command -v pipx >/dev/null 2>&1; then
  echo "pipx not found. Install with: brew install pipx (or pip install --user pipx)"
  exit 1
fi

pipx install vera-ai

echo ""
echo "✓ Vera installed."
echo ""
echo "Next:"
echo "  export ANTHROPIC_API_KEY=sk-ant-...   # or OPENAI_API_KEY"
echo "  vera init"
echo "  vera chat"
