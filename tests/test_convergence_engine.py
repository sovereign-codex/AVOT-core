from convergence.engine import converge

def test_convergence_basic():
    out = converge({
        "task": {"intent": "synthesize", "payload": "Test."},
        "agent_outputs": ["A", "B"],
        "archival_context": [],
        "guardian_context": {"coherence_score": 1.0}
    })
    assert "synthesis" in out
