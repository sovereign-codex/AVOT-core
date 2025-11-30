from fabricator.sandbox import sandbox_response


def test_fabricator_sandbox_valid():
    payload = {
        "files": [{"path": "x.py", "content": "print(123)"}],
        "instructions": "Apply changes manually.",
        "tip_required": False,
    }
    assert "error" not in sandbox_response(payload)


def test_fabricator_sandbox_missing_key():
    payload = {
        "files": [{"path": "x.py", "content": "print(123)"}]
    }
    assert "error" in sandbox_response(payload)
