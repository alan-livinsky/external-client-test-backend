# External Client Test API

Small FastAPI service that authenticates users against Tryton and exposes a protected patients endpoint for the SvelteKit frontend.

## Python version

Use Python 3.10 to stay aligned with the dashboard environment.

## Setup

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
Copy-Item .env.example .env
```

Update `.env` with the correct `TRYTON_CONFIG`, database name, and session secret.

## Run

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

## Endpoints

- `POST /auth/login`
- `POST /auth/logout`
- `GET /patients`
- `GET /health`

## Notes

This prototype uses in-memory API sessions. Restarting the API clears them.
