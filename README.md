# 🌀 AVOT-core Engine

AVOT-core is the Agent Forge for the Sovereign Intelligence lattice. It tracks the canonical AVOT roster, documents guardrails, and ships a lightweight Python package for loading manifests and simulating agents. The forge connects directly to **SIB-core** so governance and orchestration flows can request and route AVOTs by id.

## What’s inside
- `AVOT-core/` — manifests, registry, and playbooks for every AVOT tracked by the forge.
- `python/` — the `avot_core` Python package for reading manifests, querying agents, and stubbing runtime execution.
- `scripts/avot_cli.py` — a convenience CLI to list, inspect, and simulate AVOTs locally.
- `docs/SOVEREIGN-ARCHITECTURE.md` — the v0.2 reference for how Sovereign Intelligence layers connect through AVOT-core.

## Install the Python package
From the repository root:

```bash
pip install -e ./python
```

This installs the `avot_core` module and its dependencies (Python 3.11+).

## Example usage
```python
from avot_core import registry, runtime

# List all registered AVOT ids
for agent in registry.list_agents():
    print(agent.id, agent.role)

# Fetch a single agent
agent = registry.get_agent("avot-convergence")
print(agent.capabilities)

# Simulate running an agent
runtime.run_agent(agent.id, intent="demo-task")
```

You can perform the same actions via CLI:

```bash
python scripts/avot_cli.py list
python scripts/avot_cli.py show avot-convergence
python scripts/avot_cli.py run avot-convergence --intent "demo"
```

## Connecting to SIB-core
The `avot_core` package includes `sib_bridge.py`, a placeholder module that outlines how SIB-core flows will resolve agents, format invocation envelopes, and capture results. As SIB-core APIs solidify, these hooks will be implemented to provide authenticated, policy-aware execution.

## Governance
All AVOT work must align with the Living Kodex and Garden Flame Codex. Guardrails, lifecycle steps, and constellation playbooks live under `AVOT-core/` and should be treated as the source of truth for new or evolving agents.
