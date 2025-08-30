# SafiriSchola - MVP

End-to-end scaffold matching the PRD: FastAPI backend (MySQL + MongoDB), USSD stub, rides + incidents, and React/Vite frontend.

## Prerequisites
- Python 3.13 with `python3.13-venv` (installed)
- Node.js 20+
- MySQL 8 & MongoDB 6 (run locally or via Docker)

## Backend (FastAPI)

```bash
# Create venv and install deps
python3 -m venv backend/.venv
source backend/.venv/bin/activate
pip install -r backend/requirements.txt

# Configure env
cp backend/.env.example backend/.env
# Edit backend/.env if needed

# Run API
PYTHONPATH=backend uvicorn app.main:app --reload --port 8000
```

By default, DB connects to `mysql:3306`. For local without Docker, set in `.env`:
```
MYSQL_HOST=localhost
```

## Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

Frontend proxies `/api` to `http://localhost:8000` during dev.

## Docker (optional)

```bash
# Requires Docker & docker-compose installed on host
cp backend/.env.example backend/.env
JWT_SECRET_KEY=change-me # update in env

docker compose up --build
```
- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- MySQL: localhost:3306 (user/pass: safiri/safiri)
- Mongo: localhost:27017

## API Highlights
- Auth: `POST /api/v1/auth/register`, `POST /api/v1/auth/login`
- Parents: `GET/POST /api/v1/parents/children`
- Rides: `POST /api/v1/rides`, `GET /api/v1/rides`
- Incidents: `POST /api/v1/rides/incidents`
- USSD: `POST /api/v1/ussd` (Africa's Talking-compatible form body)

## Notes
- Table creation runs on startup; use Alembic in production.
- Camera/IoT integrations are stubbed for MVP and can be extended.