from __future__ import annotations

from datetime import datetime, timedelta
from threading import Lock
from typing import Dict
from uuid import uuid4

from fastapi import HTTPException

from app.models.session_models import DocumentSession


class SessionService:
    """
    Thread-safe in-memory session manager.

    NOTE:
    Replace this implementation with Redis or a database in production
    without changing the API routes.
    """

    SESSION_TIMEOUT_MINUTES = 30

    def __init__(self):
        self._sessions: Dict[str, DocumentSession] = {}
        self._lock = Lock()

    # ---------------------------------------------------------
    # Internal
    # ---------------------------------------------------------

    def _cleanup(self):
        """
        Remove expired sessions.
        """
        now = datetime.utcnow()

        expired = [
            session_id
            for session_id, session in self._sessions.items()
            if now - session.updated_at
            > timedelta(minutes=self.SESSION_TIMEOUT_MINUTES)
        ]

        for session_id in expired:
            del self._sessions[session_id]

    # ---------------------------------------------------------
    # Create
    # ---------------------------------------------------------

    def create_session(
        self,
        instruction: str,
        title: str,
        questions,
    ) -> DocumentSession:

        with self._lock:

            self._cleanup()

            session = DocumentSession(
                session_id=str(uuid4()),
                instruction=instruction,
                title=title,
                questions=questions,
            )

            self._sessions[session.session_id] = session

            return session

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    def get_session(
        self,
        session_id: str,
    ) -> DocumentSession:

        with self._lock:

            self._cleanup()

            session = self._sessions.get(session_id)

            if session is None:
                raise HTTPException(
                    status_code=404,
                    detail="Session not found or expired."
                )

            return session

    # ---------------------------------------------------------
    # Save Answers
    # ---------------------------------------------------------

    def save_answers(
        self,
        session_id: str,
        answers: dict[int, str],
    ) -> DocumentSession:

        session = self.get_session(session_id)

        if session.generated:
            raise HTTPException(
                status_code=400,
                detail="Document already generated for this session."
            )

        for question_id, answer in answers.items():

            if answer is None:
                continue

            answer = answer.strip()

            if answer:
                session.answers[question_id] = answer

        session.update_timestamp()

        return session

    # ---------------------------------------------------------
    # Complete Session
    # ---------------------------------------------------------

    def mark_generated(
        self,
        session_id: str,
    ):

        session = self.get_session(session_id)

        if session.generated:
            raise HTTPException(
                status_code=400,
                detail="Document already generated."
            )

        session.generated = True
        session.update_timestamp()

    # ---------------------------------------------------------
    # Delete
    # ---------------------------------------------------------

    def delete_session(
        self,
        session_id: str,
    ):

        with self._lock:

            self._sessions.pop(session_id, None)


# Singleton instance
session_service = SessionService()