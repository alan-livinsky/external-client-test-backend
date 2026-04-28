from __future__ import annotations

from fastapi import Header, HTTPException, status

from .config import settings
from .session_store import InMemorySessionStore, SessionData
from .tryton_service import TrytonService, tryton_service


session_store = InMemorySessionStore(settings.api_session_secret)


def get_tryton_service() -> TrytonService:
    return tryton_service


def get_current_session(authorization: str | None = Header(default=None)) -> SessionData:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token.",
        )

    token = authorization.removeprefix("Bearer ").strip()
    session = session_store.get(token)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session.",
        )
    return session
