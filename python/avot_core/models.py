"""Data models for AVOT-core registries."""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class EntryPoint:
    """Entrypoint descriptor for an AVOT runtime function."""

    module: str
    function: str


@dataclass(frozen=True)
class AgentSpec:
    """Specification for an AVOT as described in the registry manifests."""

    id: str
    name: str
    role: str
    status: str
    repo: str
    capabilities: List[str]
    entrypoint: EntryPoint
    tags: List[str] = field(default_factory=list)
    extra: Dict[str, object] = field(default_factory=dict)
