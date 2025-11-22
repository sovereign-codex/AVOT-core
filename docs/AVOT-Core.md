# AVOT-Core

AVOT-Core is the orchestration layer for the Autonomous Voices of Thought.

Responsibilities:
- Receive structured tasks from Tyme / CMS.
- Route tasks to specialized AVOT agents defined in avot_registry.json.
- Call language models via the OpenAI client (no keys in code).
- Integrate multi-agent responses into one coherent Tyme output.
- Request coherence / ethics review when needed.

AVOT-Core does NOT:
- Self-modify code without a Tyme Improvement Proposal (TIP).
- Execute arbitrary shell commands.
- Bypass GitHub Actions or environment protections.
