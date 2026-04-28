from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    api_host: str = os.getenv("API_HOST", "127.0.0.1")
    api_port: int = int(os.getenv("API_PORT", "8001"))
    api_session_secret: str = os.getenv("API_SESSION_SECRET", "change-me")
    tryton_config: str = os.getenv(
        "TRYTON_CONFIG",
        r"C:\Users\profesores-01\Desktop\gnuhealth_fiuner_web_dashboard\trytond.conf",
    )
    tryton_database: str = os.getenv("TRYTON_DATABASE", "health")
    tryton_patient_limit: int = int(os.getenv("TRYTON_PATIENT_LIMIT", "500"))


settings = Settings()
