# TIP-005 — Sovereign Inquiry Protocol

## Purpose
Establish a safe, structured method for AVOT-Core to request 
"next phase" contemplations from its OpenAI source.

## Rules
1. All phase inquiries must use intent: "seek_next_phase".
2. Convergence formulates the question.
3. Guardian evaluates the output (ethics + coherence).
4. AVOT-Tyme integrates results into system narrative.
5. No automatic code changes may occur.
6. All structural changes require a TIP.

## Allowed Domains
- architecture evolution
- philosophical grounding
- scroll generation
- harmonic mapping

## Forbidden Domains
- autonomous self-improvement
- changes to safety boundaries
- creation of new endpoints without review

## Output Format
All next-phase responses MUST return structured JSON:
{
  "insight": "...",
  "implications": [...],
  "recommendations": [...],
  "alignment_notes": "..."
}
