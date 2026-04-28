from __future__ import annotations

from datetime import datetime, date

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str
    expires_at: datetime


class PatientRecord(BaseModel):
    id: int
    code: str | None = None
    display_name: str
    gender: str | None = None
    birth_date: date | None = None
    active: bool | None = None


class LogoutResponse(BaseModel):
    ok: bool = True
