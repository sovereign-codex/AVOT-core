"""
TCOP: Tyme-Core Operating Protocol

Provides:
- generate_cycle_report(): one TCOP cycle
- heartbeat(): lightweight "I'm alive" ping

This module coordinates existing components. It does NOT
modify code, registry, or safety boundaries.
"""
import json
from datetime import datetime
from pathlib import Path

from core.system_snapshot import generate_snapshot
from clients.openai_client import run_chat_completion

PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "tcop_prompt.txt"

def _load_tcop_prompt():
    return PROMPT_PATH.read_text()

def generate_cycle_report(user_payload: str | None = None):
    """Run a single TCOP cycle and return a structured dict.

    When an OpenAI key is unavailable, return a local fallback report so
    the TCOP flow still produces a usable first-cycle artifact.
    """
    snapshot = generate_snapshot()
    system_prompt = _load_tcop_prompt()

    payload = {
        "snapshot": snapshot,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    if user_payload:
        payload["user_payload"] = user_payload

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": json.dumps(payload)}
    ]

    try:
        raw = run_chat_completion(
            model="gpt-5.1",
            messages=messages,
            temperature=0.15,
            max_tokens=1400,
        )
    except Exception as exc:  # pragma: no cover - network/env dependent
        return {
            "cycle_id": payload["timestamp"],
            "summary": "TCOP fallback: OpenAI client unavailable; generated local snapshot summary.",
            "highlights": [
                f"Agents registered: {len(snapshot.get('registry_avots', []))}",
                f"Routing intents: {', '.join(sorted(snapshot.get('routing', {})))}",
            ],
            "warnings": [str(exc)],
            "next_suggestions": [
                "Provision OPENAI/OPENAI_API_KEY to enable full TCOP cycles.",
                "Review TIP-006 for governance expectations.",
            ],
        }

    try:
        data = json.loads(raw)
    except Exception:
        data = {
            "cycle_id": payload["timestamp"],
            "summary": raw,
            "highlights": [],
            "warnings": [],
            "next_suggestions": []
        }

    return data

def heartbeat():
    """A very lightweight 'alive' indicator."""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "component": "TCOP"
    }

if __name__ == "__main__":
    report = generate_cycle_report()
    print(json.dumps(report, indent=2))
