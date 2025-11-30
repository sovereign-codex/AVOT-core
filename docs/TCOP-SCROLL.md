# 🧠 Tyme-Core Operating Protocol (TCOP)

TCOP is the operating rhythm of Sovereign Intelligence.

## Purpose
- Define how AVOT-Core orchestrates agents over time
- Provide a safe, non-self-modifying "heartbeat" cycle
- Coordinate Archivist, Convergence, Guardian, Quill, and Tyme
- Make system operation inspectable and repeatable

## TCOP Cycle (high level)
1. Take a system snapshot.
2. Ensure Archivist index is fresh (optional lightweight refresh).
3. Ask Convergence for a brief "state-of-understanding".
4. Have Guardian check coherence/ethics of that state.
5. Have Quill and/or Tyme narrate a short log entry.
6. Write log output to console or log file (future: CodexNet).

## TCOP Does NOT
- Modify code or workflows.
- Change AVOT registry or routing.
- Alter safety boundaries.
- Apply architectural changes without TIP governance.

TCOP is rhythm, not mutation.
