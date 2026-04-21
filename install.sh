#!/usr/bin/env bash
# Vera — one-line install.
# curl -sSf https://raw.githubusercontent.com/iamitp/vera/main/install.sh | bash
set -euo pipefail

echo "→ Installing Vera..."

# 1. pipx
if ! command -v pipx >/dev/null 2>&1; then
  echo "  pipx not found. Installing..."
  if command -v brew >/dev/null 2>&1; then
    brew install pipx >/dev/null
    pipx ensurepath >/dev/null
  elif command -v python3 >/dev/null 2>&1; then
    python3 -m pip install --user --quiet pipx
    python3 -m pipx ensurepath >/dev/null
    export PATH="$HOME/.local/bin:$PATH"
  else
    echo "  Need either Homebrew or Python 3 to install pipx. Install one and re-run."
    exit 1
  fi
fi

# 2. install vera
pipx install --force vera-clerk >/dev/null
echo "✓ Vera installed."
echo ""

# 3. Guide API key + next step
if [[ -z "${ANTHROPIC_API_KEY:-}" && -z "${OPENAI_API_KEY:-}" ]]; then
  cat <<MSG
One step left: an API key. Vera works with either:

  Anthropic (recommended): https://console.anthropic.com/keys
    Requires a small credit (\$5 is plenty). 90 seconds to set up.

  OpenAI: https://platform.openai.com/api-keys

Then in your shell:

  export ANTHROPIC_API_KEY=sk-ant-...     # add to ~/.zshrc to persist
  vera init                               # 3-question wizard, 30 seconds
  vera chat                               # start
MSG
else
  cat <<MSG
Next:

  vera init     # 3-question wizard (30 seconds)
  vera chat     # start
MSG
fi
