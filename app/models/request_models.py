from typing import Dict

from pydantic import BaseModel, Field, ConfigDict


class StartDocumentRequest(BaseModel):
    """
    Starts a new document generation session.
    """

    instruction: str = Field(
        ...,
        min_length=3,
        max_length=10000,
        description="User instruction describing the document."
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "instruction": "Create a professional CV for a software engineer."
            }
        }
    )


class ReplyQuestionsRequest(BaseModel):
    """
    Saves answers to AI clarification questions.
    Questions may be answered partially.
    """

    session_id: str = Field(
        ...,
        description="Session ID returned from /document/start."
    )

    answers: Dict[int, str] = Field(
        default_factory=dict,
        description="Dictionary of question_id -> answer."
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "8db68a2e-44d3-4fcb-b8b3-57d3d760d7dc",
                "answers": {
                    "1": "Hussain Abro",
                    "2": "Software Engineer",
                    "3": "Python, FastAPI, React"
                }
            }
        }
    )


class GenerateDocumentRequest(BaseModel):
    """
    Generates the final document.
    """

    session_id: str = Field(
        ...,
        description="Session ID returned from /document/start."
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "8db68a2e-44d3-4fcb-b8b3-57d3d760d7dc"
            }
        }
    )