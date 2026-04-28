from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .dependencies import get_current_session, get_tryton_service, session_store
from .schemas import LoginRequest, LoginResponse, LogoutResponse, PatientRecord
from .tryton_service import TrytonService


app = FastAPI(title="External Client Test API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    service = get_tryton_service()
    service.startup()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/auth/login", response_model=LoginResponse)
def login(
    payload: LoginRequest,
    service: TrytonService = Depends(get_tryton_service),
) -> LoginResponse:
    user = service.authenticate(payload.username, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Tryton credentials.",
        )

    session = session_store.create(user.user_id, user.username)
    return LoginResponse(
        access_token=session.token,
        user_id=user.user_id,
        username=user.username,
        expires_at=session.expires_at,
    )


@app.post("/auth/logout", response_model=LogoutResponse)
def logout(session=Depends(get_current_session)) -> LogoutResponse:
    session_store.delete(session.token)
    return LogoutResponse()


@app.get("/patients", response_model=list[PatientRecord])
def patients(
    session=Depends(get_current_session),
    service: TrytonService = Depends(get_tryton_service),
) -> list[PatientRecord]:
    rows = service.fetch_patients(session.user_id)
    return [PatientRecord(**row) for row in rows]
