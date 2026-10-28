
import pytest
from pydantic import ValidationError

from app.schemas import BugReport


def test_valid_bug_report():
    report = BugReport(
        title="Undefined variable",
        error_type="NameError",
        severity="high",
        root_cause="Variable 'x' is not defined.",
        explanation="The code references an undefined variable.",
        suggested_fix="Define the variable before using it.",
        corrected_code="x = 10",
        confidence=0.95,
    )

    assert report.severity == "high"
    assert report.confidence == 0.95


def test_confidence_must_be_between_zero_and_one():
    with pytest.raises(ValidationError):
        BugReport(
            title="Test bug",
            error_type="NameError",
            severity="low",
            root_cause="Missing variable.",
            explanation="A variable is missing.",
            suggested_fix="Define the variable.",
            confidence=1.5,
        )
