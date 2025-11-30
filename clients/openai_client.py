import os
from typing import Any, Dict, List

try:  # New-style OpenAI client
    from openai import OpenAI
except ImportError:  # pragma: no cover - optional dependency
    OpenAI = None  # type: ignore

try:  # Legacy OpenAI client
    import openai
except ImportError:  # pragma: no cover - optional dependency
    openai = None

OPENAI_KEY = os.getenv("OPENAI") or os.getenv("OPENAI_API_KEY")


def _ensure_api_key() -> str:
    if not OPENAI_KEY:
        raise RuntimeError("OPENAI/OPENAI_API_KEY env var not set")
    return OPENAI_KEY


def _new_client_completion(model: str, messages: List[Dict[str, Any]], **kwargs: Any) -> str:
    if OpenAI is None:  # pragma: no cover - defensive guard
        raise RuntimeError("openai package not installed; cannot call model")
    client = OpenAI(api_key=_ensure_api_key())
    resp = client.chat.completions.create(model=model, messages=messages, **kwargs)
    return resp.choices[0].message.content


def _legacy_completion(model: str, messages: List[Dict[str, Any]], **kwargs: Any) -> str:
    if openai is None:
        raise RuntimeError("openai package not installed; cannot call model")
    openai.api_key = _ensure_api_key()
    resp = openai.ChatCompletion.create(model=model, messages=messages, **kwargs)
    return resp["choices"][0]["message"]["content"]


def run_chat_completion(model: str, messages: List[Dict[str, Any]], **kwargs: Any) -> str:
    """Call the OpenAI chat completion API.

    The function prefers the new-style `OpenAI` client when available but
    gracefully falls back to the legacy `openai.ChatCompletion` interface.
    """

    if OpenAI is not None:
        return _new_client_completion(model, messages, **kwargs)
    return _legacy_completion(model, messages, **kwargs)
