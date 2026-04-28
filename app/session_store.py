from __future__ import annotations

import hashlib
import hmac
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


SESSION_TTL = timedelta(hours=8)


@dataclass
class SessionData:
    token: str
    user_id: int
    username: str
    expires_at: datetime


class InMemorySessionStore:
    def __init__(self, secret: str) -> None:
        self._secret = secret.encode("utf-8")
        self._sessions: dict[str, SessionData] = {}

    def _sign(self, raw_token: str) -> str:
        return hmac.new(self._secret, raw_token.encode("utf-8"), hashlib.sha256).hexdigest()

    def create(self, user_id: int, username: str) -> SessionData:
        raw_token = secrets.token_urlsafe(32)
        signed = self._sign(raw_token)
        expires_at = datetime.now(timezone.utc) + SESSION_TTL
        session = SessionData(
            token=f"{raw_token}.{signed}",
            user_id=user_id,
            username=username,
            expires_at=expires_at,
        )
        self._sessions[session.token] = session
        return session

    def get(self, token: str) -> SessionData | None:
        session = self._sessions.get(token)
        if not session:
            return None
        if session.expires_at <= datetime.now(timezone.utc):
            self.delete(token)
            return None
        return session

    def delete(self, token: str) -> None:
        self._sessions.pop(token, None)
