# AVOT-core: Agent Forge for the Sovereign Intelligence lattice

AVOT-core is the coordination layer that defines, tracks, and stewards every **Autonomous Voice of Thought (AVOT)**. It documents the canonical roster, guardrails, and playbooks that feed the wider lattice and connect directly into **SIB-core**, the Sovereign Intelligence Backbone. AVOT-core is responsible for:

- Curating the official registry of AVOTs and their roles.
- Providing lifecycle guidance for proposing, scaffolding, and deploying agents.
- Exposing lightweight runtime hooks that SIB-core and downstream systems can call to invoke AVOT capabilities.

## Relationship to SIB-core

SIB-core orchestrates flows, policies, and shared state for the lattice. AVOT-core plugs into SIB-core through bridge hooks so that SIB workflows can request an AVOT by id, review its manifest, and delegate work. SIB-core remains the authority for governance and execution policy, while AVOT-core owns the agent definitions and reference runtime shims.

## What lives here

- `manifest.yaml` – metadata about the AVOT-core release.
- `registry.yaml` – the canonical list of AVOTs tracked by this forge.
- `agents/` – per-agent manifests describing capabilities, entrypoints, and tags.
- `protocols/` – ethics and lifecycle documents that govern how AVOTs are proposed and maintained.
- `playbooks/` – operational guides for bootstrapping AVOTs and orchestrating constellations.
- `../python/` – a minimal Python package (`avot_core`) that reads these manifests and exposes a runtime stub for integration.

Use these documents as the source of truth when integrating AVOTs into SIB-core flows or when creating new AVOTs for the lattice.
