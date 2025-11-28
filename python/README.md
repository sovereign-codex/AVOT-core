# avot_core Python package

This package provides a minimal reference implementation for reading the AVOT-core manifests and simulating AVOT execution. It is intended for local tooling, tests, and early SIB-core integrations.

## Features
- Load the AVOT registry and per-agent manifests from the repository.
- Query agents by id or tag.
- Simulate running an AVOT via a simple runtime stub.
- Offer bridge hooks for future SIB-core orchestration.

## Installation
From the repository root:

```bash
pip install -e ./python
```

## Quickstart
```python
from avot_core import registry, runtime

agents = registry.list_agents()
print([a.id for a in agents])

agent = registry.get_agent("avot-convergence")
runtime.run_agent(agent.id, intent="demo")
```
