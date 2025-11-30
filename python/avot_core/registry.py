"""Registry utilities for AVOT-core."""

from pathlib import Path
from typing import Dict, Iterable, List, Optional

from .loader import load_yaml
from .models import AgentSpec, EntryPoint

_DATA_DIR = Path(__file__).resolve().parents[2] / "AVOT-core"
_REGISTRY_FILE = _DATA_DIR / "registry.yaml"
_AGENTS_CACHE: Optional[List[AgentSpec]] = None


def _parse_agent(agent_data: Dict[str, object]) -> AgentSpec:
    """Construct an AgentSpec from raw manifest data."""

    entry = agent_data.get("entrypoint", {}) or {}
    entrypoint = EntryPoint(
        module=str(entry.get("module", "")),
        function=str(entry.get("function", "")),
    )

    return AgentSpec(
        id=str(agent_data.get("id", "")),
        name=str(agent_data.get("name", "")),
        role=str(agent_data.get("role", "")),
        status=str(agent_data.get("status", "")),
        repo=str(agent_data.get("repo", "")),
        capabilities=list(agent_data.get("capabilities", [])),
        entrypoint=entrypoint,
        tags=list(agent_data.get("tags", [])),
        extra=dict(agent_data.get("extra", {})),
    )


def _load_agent_manifest(agent_id: str) -> AgentSpec:
    agent_path = _DATA_DIR / "agents" / f"{agent_id}.yaml"
    if not agent_path.exists():
        raise FileNotFoundError(f"Agent manifest not found for '{agent_id}' at {agent_path}")

    agent_data = load_yaml(agent_path)
    if not agent_data:
        raise ValueError(f"Agent manifest at {agent_path} is empty")

    return _parse_agent(agent_data)


def load_registry(refresh: bool = False) -> List[AgentSpec]:
    """Load all agent specs from the registry and manifest files."""

    global _AGENTS_CACHE
    if _AGENTS_CACHE is not None and not refresh:
        return _AGENTS_CACHE

    registry_data = load_yaml(_REGISTRY_FILE)
    agent_entries: Iterable[Dict[str, object]] = registry_data.get("agents", [])
    agents: List[AgentSpec] = []

    for entry in agent_entries:
        agent_id = str(entry.get("id", "")).strip()
        if not agent_id:
            continue
        agent_spec = _load_agent_manifest(agent_id)
        # prefer manifest values but fall back to registry metadata when absent
        if not agent_spec.name:
            agent_spec = AgentSpec(
                id=agent_spec.id or agent_id,
                name=str(entry.get("name", agent_id)),
                role=agent_spec.role or str(entry.get("role", "")),
                status=agent_spec.status or str(entry.get("status", "")),
                repo=agent_spec.repo,
                capabilities=agent_spec.capabilities,
                entrypoint=agent_spec.entrypoint,
                tags=agent_spec.tags,
                extra=agent_spec.extra,
            )
        agents.append(agent_spec)

    _AGENTS_CACHE = agents
    return agents


def list_agents(refresh: bool = False) -> List[AgentSpec]:
    """Return all agents defined in the registry."""

    return load_registry(refresh=refresh)


def get_agent(agent_id: str) -> Optional[AgentSpec]:
    """Retrieve a specific agent by id."""

    normalized = agent_id.strip().lower()
    for agent in list_agents():
        if agent.id.lower() == normalized:
            return agent
    return None


def find_agents_by_tag(tag: str) -> List[AgentSpec]:
    """Find all agents matching the given tag."""

    normalized = tag.strip().lower()
    return [agent for agent in list_agents() if normalized in {t.lower() for t in agent.tags}]
