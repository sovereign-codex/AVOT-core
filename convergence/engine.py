"""
Convergence Engine
Synthesizes multi-agent outputs, archival data,
and Guardian constraints to produce unified insights.
"""
import json
from pathlib import Path
from clients.openai_client import run_chat_completion

PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "convergence_prompt.txt"

def load_prompt():
    return PROMPT_PATH.read_text()

def converge(inputs):
    """
    inputs: {
      "task": {...},
      "agent_outputs": [...],
      "archival_context": [...],
      "guardian_context": {...}
    }
    """
    system_prompt = load_prompt()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": json.dumps(inputs)}
    ]

    raw = run_chat_completion(
        model="gpt-5.1",
        messages=messages,
        temperature=0.1,
        max_tokens=2600
    )

    try:
        return json.loads(raw)
    except:
        return {"synthesis": raw}
