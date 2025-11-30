from avot_engine import handle_task


def test_quill_write_scroll():
    task = {"intent": "write_scroll", "payload": "Explain what AVOT-Quill does."}
    result = handle_task(task)
    assert "content" in result


def test_tyme_describe_system():
    task = {"intent": "describe_system", "payload": "Summarize the Tyme architecture."}
    result = handle_task(task)
    assert "content" in result


def test_harmonia_reflective():
    task = {"intent": "reflective_guidance", "payload": "Talk about inner coherence in a gentle way."}
    result = handle_task(task)
    assert "content" in result


def test_initiate_onboard():
    task = {"intent": "onboard_user", "payload": "I am new. Where do I start?"}
    result = handle_task(task)
    assert "content" in result
