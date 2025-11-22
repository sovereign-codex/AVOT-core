# AVOT Agent Spec (Template)

name: AVOT-Example
role: "Short description of what this agent does"
input_scope:
  - "types of tasks / domains"
output_scope:
  - "expected output formats"
forbidden_zones:
  - "things this agent must never do"
coherence_hooks:
  - "must read docs/SIOS-CORE.md"
  - "must defer ethics to AVOT-Guardian when unsure"
