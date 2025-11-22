"""Minimal bridge module connecting AVOT and TCOP to the LocalOpenAIClient."""
import json
from typing import Any

from clients.local_openai_client import get_client


def run_chat(model: str, messages, **kwargs) -> Any:
    """Call the local OpenAI client and return the response content.

    Falls back to returning the raw response if the expected message format is
    unavailable (e.g., error responses or unexpected payloads).
    """
    client = get_client()
    response: Any = client.chat(
        model=model,
        messages=messages,
        temperature=kwargs.get("temperature", 0.2),
        max_tokens=kwargs.get("max_tokens"),
    )

    if isinstance(response, dict) and response.get("error"):
        # Bubble up serialized error information for diagnostics
        return json.dumps(response)

    try:
        return response["choices"][0]["message"]["content"]
    except Exception:
        return response
