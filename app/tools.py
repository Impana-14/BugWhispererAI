
import ast
import re


def inspect_python_syntax(code: str) -> dict:
    """Check Python code for syntax errors."""
    try:
        ast.parse(code)
        return {
            "valid": True,
            "message": "No Python syntax errors detected.",
        }
    except SyntaxError as exc:
        return {
            "valid": False,
            "message": exc.msg,
            "line": exc.lineno,
            "column": exc.offset,
        }


def find_debugging_hints(code: str, error_message: str) -> dict:
    """Collect simple clues that may help diagnose a bug."""
    hints = []
    combined_text = f"{code}\n{error_message}".lower()

    if "nameerror" in combined_text or "is not defined" in combined_text:
        hints.append(
            "Check for misspelled variable or function names and missing definitions."
        )

    if "indexerror" in combined_text or "index out of range" in combined_text:
        hints.append(
            "Check list or sequence indexes and confirm they are within valid bounds."
        )

    if "keyerror" in combined_text:
        hints.append(
            "Check whether the requested dictionary key exists before accessing it."
        )

    if "typeerror" in combined_text:
        hints.append(
            "Check whether the values and types used in the operation are compatible."
        )

    if re.search(r"\bexcept\s*:", code):
        hints.append(
            "A broad exception handler was found; consider catching specific exceptions."
        )

    if not hints:
        hints.append(
            "Review the traceback, input values, variable types, and relevant execution path."
        )

    return {
        "hints": hints,
        "code_length": len(code),
        "line_count": len(code.splitlines()),
    }
