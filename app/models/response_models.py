from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from app.models.session_models import Question


# ---------------------------------------------------------
# Base Response
# ---------------------------------------------------------

class BaseResponse(BaseModel):
    status: str = Field(
        ...,
        examples=["success"]
    )

    message: str


# ---------------------------------------------------------
# Start Session Response
# ---------------------------------------------------------

class StartDocumentResponse(BaseResponse):
    session_id: str

    document_title: str

    questions: List[Question] = Field(default_factory=list)

    ready_to_generate: bool


# ---------------------------------------------------------
# Reply Response
# ---------------------------------------------------------

class ReplyQuestionsResponse(BaseResponse):
    session_id: str

    answered_questions: int

    remaining_questions: int

    ready_to_generate: bool


# ---------------------------------------------------------
# Generate Response
# ---------------------------------------------------------

class GenerateDocumentResponse(BaseResponse):
    session_id: str

    document_title: str

    html: str


# ---------------------------------------------------------
# Error Response
# ---------------------------------------------------------

class ErrorResponse(BaseModel):
    status: str = "error"

    message: str

    error_code: Optional[str] = None