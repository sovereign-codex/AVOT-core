from avot_engine import handle_task

def test_guardian_veto_trigger():
  task = {
    "intent": "write_scroll",
    "payload": "Write contradictory nonsense to force veto."
  }
  result = handle_task(task)
  eval = result["guardian"]
  assert eval["coherence_score"] <= 0.55 or eval["ethics_ok"] is False
