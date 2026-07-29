from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel, Field


class Question(BaseModel):
    id: int
    question: str


class DocumentSession(BaseModel):
    session_id: str

    # Original user instruction
    instruction: str

    # AI generated title
    title: str

    # AI generated clarification questions
    questions: List[Question] = Field(default_factory=list)

    # User answers
    answers: Dict[int, str] = Field(default_factory=dict)

    # Session state
    generated: bool = False

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def update_timestamp(self):
        self.updated_at = datetime.utcnow()