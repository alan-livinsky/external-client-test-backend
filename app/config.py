from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent
API_DIR = BASE_DIR.parent
PROJECT_ROOT = API_DIR.parent.parent
DEFAULT_TRYTON_CONFIG = PROJECT_ROOT / "trytond.conf"


@dataclass(frozen=True)
class Settings:
    api_host: str = os.getenv("API_HOST", "127.0.0.1")
    api_port: int = int(os.getenv("API_PORT", "8001"))
    api_session_secret: str = os.getenv("API_SESSION_SECRET", "change-me")
    tryton_config: str = os.getenv("TRYTON_CONFIG", str(DEFAULT_TRYTON_CONFIG))
    tryton_database: str = os.getenv("TRYTON_DATABASE", "health")
    tryton_patient_limit: int = int(os.getenv("TRYTON_PATIENT_LIMIT", "500"))


settings = Settings()
