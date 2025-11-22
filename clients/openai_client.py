import os
import openai

OPENAI_KEY = os.getenv("OPENAI") or os.getenv("OPENAI_API_KEY")


def run_chat_completion(model, messages, **kwargs):
    if not OPENAI_KEY:
        raise RuntimeError("OPENAI/OPENAI_API_KEY env var not set")
    openai.api_key = OPENAI_KEY
    resp = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        **kwargs,
    )
    return resp["choices"][0]["message"]["content"]
