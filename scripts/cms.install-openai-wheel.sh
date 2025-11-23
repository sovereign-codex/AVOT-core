#!/usr/bin/env bash
# CMS: Install OpenAI SDK via wheel (AVOT-core)
# Repository: sovereign-codex/AVOT-core
# Purpose: Ensure the 'openai' Python package is available for TCOP and AVOT clients
# Notes:
#  - Tries pip install normally first.
#  - If that fails due to network/proxy, reports a clear status but does not break the run.
#  - Meant to be invoked from Codex / CI, not from end-user machines.

set -euo pipefail

python3 --version || python --version
python3 -m pip --version || python -m pip --version

PYTHON_BIN="${PYTHON_BIN:-python3}"

echo "🔧 Upgrading pip (best effort)..."
if ! "$PYTHON_BIN" -m pip install --upgrade pip; then
  echo "⚠️ pip upgrade failed, continuing."
fi

echo "📦 Attempting to install 'openai' package..."
if "$PYTHON_BIN" -m pip install --upgrade openai; then
  echo "✅ OpenAI SDK installed successfully."
else
  echo "⚠️ OpenAI SDK install failed (likely network/proxy issue)."
  echo "   TCOP and AVOT OpenAI calls will remain in fallback mode."
fi

echo "🔍 Verifying 'openai' import (non-fatal)..."
"$PYTHON_BIN" - <<'PY'
import importlib, sys
mod = importlib.util.find_spec("openai")
if mod is None:
    print("⚠️ 'openai' module not found. System will operate in fallback / no-API mode.")
    sys.exit(0)
print("✅ 'openai' module is importable; AVOT-core can use OpenAI SDK.")
PY
