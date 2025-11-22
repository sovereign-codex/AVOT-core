import os
import sys
import types
from pathlib import Path

# Provide a lightweight stub for the OpenAI client so tests do not require
# network access or external dependencies.
if "openai" not in sys.modules:
    mock_openai = types.SimpleNamespace(api_key=None)

    class _ChatCompletion:
        @staticmethod
        def create(**_kwargs):
            # Return a minimal structure compatible with avot_engine expectations.
            return {"choices": [{"message": {"content": "Mock completion"}}]}

    mock_openai.ChatCompletion = _ChatCompletion
    sys.modules["openai"] = mock_openai

# Ensure a dummy API key is present to satisfy client checks.
os.environ.setdefault("OPENAI", "test-key")

# Ensure project root is on sys.path for module imports
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
