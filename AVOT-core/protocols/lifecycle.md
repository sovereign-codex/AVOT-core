# AVOT Lifecycle

1. **Proposal**
   - Draft an intent brief: purpose, beneficiaries, risks, and alignment with the Living Kodex.
   - Present to the AVOT council with Guardian review notes.
2. **Scaffolding**
   - Create an agent manifest in `agents/` describing role, capabilities, entrypoint, and tags.
   - Bootstrap a dedicated repository with minimal runtime hooks and CI guardrails.
   - Connect the repo to SIB-core sandbox endpoints for early integration tests.
3. **Deployment**
   - Graduate from sandbox after Guardian approval and reproducible test runs.
   - Register the agent in `registry.yaml` with status `active` or `beta`.
   - Publish playbooks and operational runbooks for operators.
4. **Operation**
   - Monitor logs, ethics signals, and performance metrics. Route alerts to Guardian when thresholds are crossed.
   - Iterate capabilities with versioned manifests and changelogs.
5. **Retirement or Merge**
   - When an AVOT is superseded or merged, update status to `retired` and archive the repo.
   - Preserve scrolls and data artifacts in Archivist-led cold storage.
   - Announce the transition in constellation playbooks to avoid broken pipelines.
