# 00 – Bootstrap a new AVOT

Use this playbook to add a fresh AVOT to the lattice via AVOT-core.

1. **Define intent**: clarify the problem, success signals, and safety constraints.
2. **Create agent manifest**:
   - Copy an existing file in `../agents/` and update `id`, `name`, `role`, `capabilities`, `entrypoint`, and `tags`.
   - Keep `extra` free-form for notes such as stewards, risk class, or integration links.
3. **Update registry**:
   - Append the new agent to `../registry.yaml` with `status: beta` or `active`.
   - Ensure `id` matches the manifest filename.
4. **Scaffold repository**:
   - Create a dedicated repo (or folder) for the AVOT runtime code.
   - Add guardrails from `../protocols/guardrails.md` and CI checks for linting and safe operations.
5. **Connect to SIB-core**:
   - Wire the new AVOT repo to SIB-core sandbox endpoints.
   - Register the entrypoint (module/function) that SIB-core should call.
6. **Smoke test**:
   - Use `python/scripts/avot_cli.py run <id>` to simulate the AVOT.
   - Iterate until Guardian approvals are satisfied.
7. **Announce**:
   - Add the AVOT to constellation playbooks if it participates in known pipelines.
   - Publish the manifest and initial scrolls.
