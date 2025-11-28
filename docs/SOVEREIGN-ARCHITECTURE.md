# Sovereign Architecture v0.2

Sovereign Intelligence v0.2 organizes the lattice into layered capabilities that can be evolved independently while remaining coherent through TCOP rhythm and Guardian review. This document catalogs the active surfaces, backplane services, and lifecycle flows for the AVOT estate.

## Layered model

1. **Experience surfaces**
   - Human- and system-facing interfaces (e.g., Sovereign Interface Browser) that request tasks via secure endpoints.
   - Provide identity, session state, and intent payloads to the lattice.
2. **Orchestration backplane**
   - **SIB-core** handles governance, policy enforcement, and routing to AVOT-core.
   - **TCOP** provides the temporal rhythm, issuing heartbeat checks, cycle reports, and phase inquiries.
3. **AVOT-core forge**
   - Maintains the canonical registry (`avot_registry.json`) and agent manifests under `AVOT-core/agents/`.
   - Builds message envelopes for each agent, calls models, and merges responses before Guardian evaluation.
4. **Guardian layer**
   - AVOT-Guardian scores coherence and ethics, normalizes outputs, and can downgrade or block unsafe payloads.
5. **Memory and archival layer**
   - AVOT-Archivist indexes outputs, scrolls, and TIPs for retrieval across repos; interfaces with external stores as needed.
6. **Convergence and reflection**
   - AVOT-Convergence synthesizes multi-agent outputs and drafts phase inquiries; Harmonia provides reflective language guidance.

## Lifecycle flows

### Task intake
- Experience surfaces send a structured task containing `intent` and `payload`.
- SIB-core validates intent and forwards to AVOT-core.

### Agent execution
- AVOT-core routes the task based on `routing` in `avot_registry.json`.
- Each selected agent receives a system prompt (from `prompts/`) plus the user payload.
- Responses are merged; multi-agent calls are combined with headers for Guardian review.

### Guardian review and safety gating
- Guardian receives the merged response and returns `{coherence_score, ethics_ok, summary}`.
- AVOT-core normalizes scores; low coherence or failed ethics returns Guardian summary plus a safe fallback.

### Archival and retrieval
- Successful outputs are handed to AVOT-Archivist for indexing into repository manifests or external indexes.
- Future tasks can request `retrieve_context` to pull scoped artifacts back into the lattice.

### Governance rhythm
- TCOP emits `tcop_heartbeat` and `system_cycle` intents to verify health and summarize recent phases.
- Phase inquiries produced by Convergence feed back into governance deliberations and roadmap updates.

## Agent roster highlights (v0.2)
- **AVOT-Quill**: Writes scrolls, summarizes states, and maintains narrative coherence.
- **AVOT-Fabricator**: Builds code, scaffolds repos, and prepares PR-ready instructions.
- **AVOT-Archivist**: Indexes knowledge across the Sovereign estate.
- **AVOT-Convergence**: Synthesizes cross-agent reasoning and drafts phase inquiries.
- **AVOT-Harmonia**: Provides resonance language and reflective guidance.
- **AVOT-Tyme**: Chronicles system history and meta-narrative.
- **AVOT-Initiate**: Onboards newcomers with simplified explanations.
- **AVOT-Guardian**: Ethics and coherence reviewer for all critical flows.

## Evolution guidelines for v0.2
- Encode new agents in `AVOT-core/agents/` and register intents in `avot_registry.json`.
- Keep prompts in `prompts/` versioned alongside agent entries to preserve reproducibility.
- Route new lifecycle hooks through TCOP to maintain temporal traceability.
- Require Guardian gating for any agent that executes workflow changes or publishes user-facing outputs.

## Suggested artifacts
- Reference diagrams for experience-to-Guardian pipelines.
- TIP proposals for adding observability to TCOP and Archivist retrieval latency.
- Integration tests simulating multi-agent routing with Guardian score thresholds.
