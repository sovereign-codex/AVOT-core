"""
AVOT-Core Orchestrator Skeleton.

This module is the entrypoint for Tyme's multi-agent routing.
It loads avot_registry.json, selects agents by intent, calls the
OpenAI client, and merges responses. Coherence/ethics will be
enriched over time.
"""
import json
from pathlib import Path
from clients.openai_client import run_chat_completion

REGISTRY_PATH = Path(__file__).parent / "avot_registry.json"


def load_registry():
    with REGISTRY_PATH.open() as f:
        return json.load(f)


def build_messages(agent_config, task):
    system_msg = {"role": "system", "content": agent_config["system_prompt"]}
    user_msg = {
        "role": "user",
        "content": task.get("payload", ""),
    }
    return [system_msg, user_msg]


def call_agent(agent_config, task):
    messages = build_messages(agent_config, task)
    return run_chat_completion(
        model=agent_config["model"],
        messages=messages,
        temperature=agent_config.get("temperature", 0.2),
        max_tokens=agent_config.get("max_tokens", 1024),
    )


def handle_task(task):
    """
    task = {
      "intent": "write_scroll" | "generate_code" | ...,
      "payload": "natural language description",
    }
    """
    registry = load_registry()
    routing = registry.get("routing", {})
    agents = registry.get("agents", [])
    intent = task.get("intent")

    agent_names = routing.get(intent, [])
    if not agent_names:
        return {"content": f"No agents registered for intent '{intent}'."}

    name_to_cfg = {a["name"]: a for a in agents}
    responses = []
    for name in agent_names:
        cfg = name_to_cfg.get(name)
        if not cfg:
            continue
        out = call_agent(cfg, task)
        responses.append((name, out))

    # naive merge for now; Guardian/Coherence will refine later
    if len(responses) == 1:
        name, content = responses[0]
        return {"agent": name, "content": content}

    merged = "\n\n".join([f"### {name}\n{content}" for name, content in responses])
    return {"agent": "AVOT-Core", "content": merged}


if __name__ == "__main__":
    demo_task = {
        "intent": "write_scroll",
        "payload": "Describe the purpose of AVOT-Core in 3 short paragraphs.",
    }
    result = handle_task(demo_task)
    print(result["content"])
