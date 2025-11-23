#!/usr/bin/env bash
set -euo pipefail

GREEN="\033[0;32m"
RED="\033[0;31m"
RESET="\033[0m"

pass() { echo -e "${GREEN}✅ $1${RESET}"; }
fail() { echo -e "${RED}❌ $1${RESET}"; }
info() { echo "🔍 $1"; }

info "Checking GitHub-style environment secrets…"

if [[ -z "${GH_PAT:-}" ]]; then
  fail "GH_PAT missing in environment"
  exit 1
else
  pass "GH_PAT detected in environment"
fi

if [[ -z "${OPENAI:-${OPENAI_API_KEY:-}}" ]]; then
  fail "OPENAI or OPENAI_API_KEY missing in environment"
  exit 1
else
  pass "OpenAI key detected in environment"
fi

info "Verifying Codex runtime availability…"
python3 - <<'PY'
import os
import sys

gh = os.getenv("GH_PAT")
oa = os.getenv("OPENAI") or os.getenv("OPENAI_API_KEY")

if not gh:
    print("❌ GH_PAT not available in runtime")
    sys.exit(1)
print("✅ GH_PAT available in runtime")

if not oa:
    print("❌ OpenAI key missing in runtime")
    sys.exit(1)
print("✅ OpenAI key available in runtime")

print("⚡ Secrets passed runtime environment validation")
PY

info "Testing GH_PAT authentication against GitHub API…"
if curl -H "Authorization: token ${GH_PAT}" https://api.github.com/user >/dev/null 2>&1; then
  pass "GH_PAT authentication successful"
else
  fail "GH_PAT authentication failed"
  exit 1
fi

info "Testing OpenAI API communication…"
python3 - <<'PY'
import os
import sys

try:
    from openai import OpenAI
except ImportError:
    print("❌ openai package not installed; install with 'pip install openai'")
    sys.exit(1)

key = os.getenv("OPENAI") or os.getenv("OPENAI_API_KEY")
if not key:
    print("❌ OpenAI key missing during API test")
    sys.exit(1)

client = OpenAI(api_key=key)
try:
    client.responses.create(model="gpt-4.1-mini", input="ping")
    print("✅ OpenAI key authenticated successfully")
except Exception as exc:
    print(f"❌ OpenAI authentication failed: {exc}")
    sys.exit(1)
PY

info "CMS.verify-secrets complete"
pass "GitHub secrets validated"
pass "Codex secrets validated"
pass "GitHub PAT authenticated"
pass "OpenAI key authenticated"
info "AVOT-core is ready for next-phase API operations"
