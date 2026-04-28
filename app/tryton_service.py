from __future__ import annotations

from dataclasses import dataclass
from threading import Lock
from typing import Any

from trytond.config import config as tryton_config
from trytond.pool import Pool
from trytond.transaction import Transaction

from .config import settings


@dataclass
class AuthenticatedUser:
    user_id: int
    username: str


class TrytonService:
    def __init__(self) -> None:
        self._pool: Pool | None = None
        self._started = False
        self._lock = Lock()

    def startup(self) -> None:
        with self._lock:
            if self._started:
                return

            tryton_config.update_etc(settings.tryton_config)
            Pool.start()
            pool = Pool(settings.tryton_database)
            pool.init()

            self._pool = pool
            self._started = True

    @property
    def pool(self) -> Pool:
        if not self._pool:
            raise RuntimeError("Tryton pool has not been initialized.")
        return self._pool

    def authenticate(self, username: str, password: str) -> AuthenticatedUser | None:
        self.startup()
        User = self.pool.get("res.user")
        with Transaction().start(settings.tryton_database, 0, readonly=True):
            user_id = User.get_login(username, {"password": password})
        if not user_id:
            return None
        return AuthenticatedUser(user_id=user_id, username=username)

    def fetch_patients(self, user_id: int, limit: int | None = None) -> list[dict[str, Any]]:
        self.startup()
        Patient = self.pool.get("gnuhealth.patient")

        rows: list[dict[str, Any]] = []
        patient_limit = limit or settings.tryton_patient_limit

        with Transaction().start(settings.tryton_database, user_id, readonly=True):
            patients = Patient.search([], limit=patient_limit, order=[("id", "ASC")])
            for patient in patients:
                party = patient.name
                rows.append(
                    {
                        "id": patient.id,
                        "code": getattr(party, "ref", None),
                        "display_name": getattr(party, "rec_name", str(patient)),
                        "gender": getattr(patient, "gender", None),
                        "birth_date": getattr(party, "dob", None),
                        "active": getattr(patient, "active", None),
                    }
                )

        return rows


tryton_service = TrytonService()
