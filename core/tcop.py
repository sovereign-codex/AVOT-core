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
from core.openai_bridge import run_chat

PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "tcop_prompt.txt"

def _load_tcop_prompt():
    return PROMPT_PATH.read_text()

def generate_cycle_report():
    """Run a single TCOP cycle and return a structured dict."""
    snapshot = generate_snapshot()
    system_prompt = _load_tcop_prompt()

    payload = {
        "snapshot": snapshot,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": json.dumps(payload)}
    ]

    raw = run_chat(
        model="gpt-5.1",
        messages=messages,
        temperature=0.15,
        max_tokens=1400,
    )

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
