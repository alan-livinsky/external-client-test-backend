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

This API now follows the dashboard pattern by default:

- it uses the repo's existing `trytond.conf`
- it defaults to the `health` database

So for a quick test on the same server, you usually only need to edit `.env` to set a real `API_SESSION_SECRET`.

Only add `TRYTON_CONFIG` or `TRYTON_DATABASE` to `.env` if your server uses different values than the dashboard.

Example minimal `.env`:

```env
API_HOST=127.0.0.1
API_PORT=8001
API_SESSION_SECRET=replace-this-with-a-long-random-value
TRYTON_PATIENT_LIMIT=500
```

Optional overrides:

```env
TRYTON_CONFIG=/path/to/your/real/trytond.conf
TRYTON_DATABASE=health
```

## Run

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

If you keep the default layout from this repository, the API will automatically look for:

```text
<repo-root>/trytond.conf
```

## Endpoints

- `POST /auth/login`
- `POST /auth/logout`
- `GET /patients`
- `GET /health`

## Notes

This prototype uses in-memory API sessions. Restarting the API clears them.
