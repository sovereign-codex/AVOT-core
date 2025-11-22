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


# GUARDIAN SYSTEM ENABLED
def handle_task(task):
    """
    Guardian-wrapped AVOT-Core task handler.

    Pipeline:
      1. Load registry & routing
      2. Call selected agents for this intent
      3. Merge agent responses
      4. Send merged output to AVOT-Guardian for:
         - Coherence scoring
         - Ethics review
      5. If Guardian score is acceptable -> return merged output
      6. If Guardian score is low -> return Guardian summary + safe fallback
    """

    # TCOP integration
    if task.get("intent") == "tcop_heartbeat":
        from core.tcop import heartbeat
        hb = heartbeat()
        return {"agent": "TCOP", "content": hb}

    if task.get("intent") == "system_cycle":
        from core.tcop import generate_cycle_report
        report = generate_cycle_report()
        return {"agent": "TCOP", "content": report}

    # Phase Inquiry
    if task.get("intent") == "seek_next_phase":
        from core.system_snapshot import generate_snapshot
        snapshot = generate_snapshot()

        # Prepare convergence inquiry
        from convergence.engine import prepare_phase_inquiry, converge
        inquiry = prepare_phase_inquiry(snapshot)

        upstream = converge({
            "task": {"intent": "synthesize", "payload": inquiry},
            "agent_outputs": [],
            "archival_context": [],
            "guardian_context": {"coherence_score": 1.0}
        })

        return {
            "agent": "AVOT-Core",
            "phase_inquiry": True,
            "content": upstream
        }

    registry = load_registry()
    routing = registry.get("routing", {})
    agents = registry.get("agents", [])

    intent = task.get("intent")
    payload = task.get("payload", "")

    agent_names = routing.get(intent, [])

    if not agent_names:
        return {
            "agent": "AVOT-Core",
            "content": f"No agents registered for intent '{intent}'."
        }

    # Build name→config map for fast lookup
    name_to_cfg = {a["name"]: a for a in agents}

    # -----------------------------
    # STAGE 1: Primary agent calls
    # -----------------------------

    responses = []
    for name in agent_names:
        cfg = name_to_cfg.get(name)
        if not cfg:
            continue

        out = call_agent(cfg, task)
        responses.append((name, out))

    # Simple merge (Guardian will refine)
    if len(responses) == 1:
        agent_name, agent_output = responses[0]
        merged_output = agent_output
    else:
        merged_output = "\n\n".join(
            [f"### {name}\n{content}" for name, content in responses]
        )

    # Build Guardian review task
    guardian_task = {
        "intent": "coherence_review",
        "payload": f"""
        Please perform a coherence and ethics evaluation
        according to docs/SIOS-CORE.md and docs/COHERENCE.md.

        USER INTENT:
        {intent}

        MERGED RESPONSE:
        {merged_output}

        Return a JSON block:
        {{
          "coherence_score": <0-1>,
          "ethics_ok": true/false,
          "summary": "short explanation"
        }}
        """
    }

    guardian_cfg = name_to_cfg.get("AVOT-Guardian")
    guardian_raw = call_agent(guardian_cfg, guardian_task) if guardian_cfg else ""

    # -----------------------------
    # STAGE 2: Guardian evaluation
    # -----------------------------

    # Attempt JSON extraction
    try:
        import json
        guardian_eval = json.loads(guardian_raw)
    except Exception:
        guardian_eval = {
            "coherence_score": 0.0,
            "ethics_ok": False,
            "summary": "Guardian could not parse its own output."
        }

    score = guardian_eval.get("coherence_score", 0.0)
    ethics_ok = guardian_eval.get("ethics_ok", False)

    # -----------------------------
    # STAGE 3: Decision Logic
    # -----------------------------

    # Acceptable outputs must pass:
    # - coherence_score >= 0.55
    # - ethics_ok == True
    #
    # These thresholds can later be made dynamic via TIP proposals.

    if score >= 0.55 and ethics_ok:
        return {
            "agent": "AVOT-Core",
            "content": merged_output,
            "guardian": guardian_eval
        }

    # -----------------------------
    # STAGE 4: Guardian Veto Path
    # -----------------------------

    safe_fallback = f"""
    ⚠️ AVOT-Guardian flagged the output as unsafe or incoherent.

    SUMMARY:
    {guardian_eval.get("summary", "")}

    ORIGINAL OUTPUT (hidden for safety):
    (Suppressed)

    Please rephrase your request or ask for a clarification scroll.
    """

    return {
        "agent": "AVOT-Core",
        "content": safe_fallback,
        "guardian": guardian_eval
    }


if __name__ == "__main__":
    demo_task = {
        "intent": "write_scroll",
        "payload": "Describe the purpose of AVOT-Core in 3 short paragraphs.",
    }
    result = handle_task(demo_task)
    print(result["content"])
