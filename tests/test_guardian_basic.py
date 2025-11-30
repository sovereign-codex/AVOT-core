import json
from avot_engine import handle_task

def test_basic_guardian_logic():
  task = {
    "intent": "write_scroll",
    "payload": "Describe the role of harmony in intelligence."
  }
  result = handle_task(task)
  assert "guardian" in result
  eval = result["guardian"]
  assert isinstance(eval.get("coherence_score"), float)
