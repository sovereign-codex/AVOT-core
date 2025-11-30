"""Bridge hooks for SIB-core integrations.

These functions are stubs that document how SIB-core is expected to interact
with AVOT-core. Implementations will be provided as SIB-core surfaces concrete
APIs for scheduling and executing AVOTs.
"""

from typing import Any, Dict, List, Optional

from .models import AgentSpec
from .registry import get_agent, list_agents


def resolve_agent_for_flow(flow_name: str, tags: Optional[List[str]] = None) -> Optional[AgentSpec]:
    """Return an appropriate agent for a given SIB-core flow name.

    For now this is a simple tag-based lookup; SIB-core can extend this to
    consult policies, availability, or dynamic routing.
    """

    tags = tags or []
    for tag in tags:
        matches = [agent for agent in list_agents() if tag.lower() in {t.lower() for t in agent.tags}]
        if matches:
            return matches[0]
    return get_agent(flow_name)


def format_invocation(agent: AgentSpec, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Prepare an invocation envelope for SIB-core schedulers."""

    return {
        "agent_id": agent.id,
        "entrypoint": {
            "module": agent.entrypoint.module,
            "function": agent.entrypoint.function,
        },
        "payload": payload,
    }


def acknowledge_result(agent: AgentSpec, result: Any) -> None:
    """Placeholder for pushing execution results back into SIB-core."""

    # In a future integration this would persist to SIB-core storage or emit an
    # event to the lattice message bus.
    print(f"[SIB bridge] Result from {agent.id}: {result}")
