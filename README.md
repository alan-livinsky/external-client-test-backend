# External Client Test API

Small FastAPI service that authenticates users against Tryton/GNU Health and exposes a protected patients endpoint for external frontends (SvelteKit or similar).

## Python version

Use Python 3.10+ aligned with the GNU Health venv environment.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Linux
# .venv\Scripts\activate         # Windows
pip install -r requirements.txt
cp .env.example .env
```

## Configuración: Test vs Producción

### Desarrollo / Test local

CORS abierto a cualquier origen (para facilitar pruebas desde cualquier cliente o herramienta como Postman, Bruno, etc).

**`app/main.py`:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,   # debe ser False si origins="*"
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**`.env` mínimo para test:**
```env
API_HOST=127.0.0.1
API_PORT=8001
API_SESSION_SECRET=cualquier-valor-para-test
TRYTON_CONFIG=/etc/gnuhealth/trytond.conf
TRYTON_DATABASE=gnuhealth
TRYTON_PATIENT_LIMIT=500
```

### Producción

CORS restringido a los orígenes del frontend real. `allow_credentials=True` para soportar cookies de sesión si se usan.

**`app/main.py`:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mi-frontend.example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**`.env` para producción:**
```env
API_HOST=127.0.0.1
API_PORT=8001
API_SESSION_SECRET=valor-largo-aleatorio-seguro   # openssl rand -hex 32
TRYTON_CONFIG=/etc/gnuhealth/trytond.conf
TRYTON_DATABASE=gnuhealth                          # verificar con: psql -U gnuhealth -l
TRYTON_PATIENT_LIMIT=500
```

> **Importante:** `TRYTON_CONFIG` debe apuntar a `/etc/gnuhealth/trytond.conf` en el servidor de producción GNU Health. Si esta variable falta o tiene un valor incorrecto, trytond cae a un backend SQLite por defecto y el servidor no levanta.

### Tabla resumen

| Variable | Test | Producción |
|---|---|---|
| `allow_origins` | `["*"]` | `["https://tu-frontend.com"]` |
| `allow_credentials` | `False` | `True` |
| `API_SESSION_SECRET` | cualquier valor | string aleatorio seguro (`openssl rand -hex 32`) |
| `TRYTON_CONFIG` | `/etc/gnuhealth/trytond.conf` | `/etc/gnuhealth/trytond.conf` |
| `TRYTON_DATABASE` | nombre real de la BD | nombre real de la BD |

## Despliegue en producción (GNU Health server)

```bash
# En /opt/gnuhealth/custom_modules/external-client-test-backend/
git pull
# editar .env con valores de producción
source /opt/gnuhealth/venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8001
```

Para correr como servicio systemd ver la documentación del servidor.

## Endpoints

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/health` | No | Health check |
| `POST` | `/auth/login` | No | Login con credenciales Tryton |
| `POST` | `/auth/logout` | Bearer token | Invalida la sesión |
| `GET` | `/patients` | Bearer token | Lista de pacientes (hasta `TRYTON_PATIENT_LIMIT`) |

## Notas

- Sesiones en memoria: se pierden al reiniciar el proceso.
- El token de sesión es HMAC-SHA256 firmado con `API_SESSION_SECRET`, TTL 8 horas.
- Autenticación delegada a `res.user` de Tryton; permisos de pacientes respetan el contexto del usuario autenticado.
