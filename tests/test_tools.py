
from app.tools import inspect_python_syntax, find_debugging_hints


def test_valid_python_syntax():
    result = inspect_python_syntax("x = 10")
    assert result["valid"] is True


def test_invalid_python_syntax():
    result = inspect_python_syntax("def add(:")
    assert result["valid"] is False
    assert "message" in result


def test_name_error_hint():
    result = find_debugging_hints(
        "print(username)",
        "NameError: name 'username' is not defined",
    )
    assert any("variable" in hint.lower() for hint in result["hints"])


def test_code_statistics():
    result = find_debugging_hints("x = 1\ny = 2", "Unknown error")
    assert result["code_length"] == len("x = 1\ny = 2")
    assert result["line_count"] == 2
