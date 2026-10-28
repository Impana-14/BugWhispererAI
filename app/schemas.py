
from pydantic import BaseModel, Field


class BugAnalysisRequest(BaseModel):
    code: str = Field(
        ...,
        min_length=1,
        description="The source code that contains the suspected bug",
    )
    error_message: str = Field(
        ...,
        min_length=1,
        description="The error message or description of the problem",
    )
    conversation_id: str | None = Field(
        default=None,
        description="Optional ID used to continue a debugging conversation",
    )


class BugReport(BaseModel):
    title: str = Field(description="Short title describing the bug")
    error_type: str = Field(description="Category of the error")
    severity: str = Field(description="Severity: low, medium, high, or critical")
    root_cause: str = Field(description="Likely reason for the bug")
    explanation: str = Field(description="Detailed explanation of the problem")
    suggested_fix: str = Field(description="Recommended steps to fix the bug")
    corrected_code: str | None = Field(
        default=None,
        description="Corrected code, when a suitable fix can be determined",
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence in the diagnosis, from 0 to 1",
    )


class BugAnalysisResponse(BaseModel):
    conversation_id: str
    report: BugReport
