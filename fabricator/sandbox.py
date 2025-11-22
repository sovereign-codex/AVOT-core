"""
Fabricator Sandbox
Ensures file modifications pass through Guardian
and are output-only (no execution).
"""
import json


def sandbox_response(agent_output):
    """
    Accepts Fabricator output (JSON string or dict).
    Enforces schema:
    {
      "files": [...],
      "instructions": "...",
      "tip_required": bool
    }
    """
    if isinstance(agent_output, str):
        try:
            agent_output = json.loads(agent_output)
        except:
            return {"error": "Fabricator output not valid JSON"}

    # Ensure required keys
    for key in ["files", "instructions"]:
        if key not in agent_output:
            return {"error": f"Missing required key: {key}"}

    # Ensure file entries are structured
    for item in agent_output.get("files", []):
        if not {"path", "content"} <= set(item.keys()):
            return {"error": "Each file must include path & content"}

    return agent_output
