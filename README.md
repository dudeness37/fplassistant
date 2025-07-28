# FPL-AI (25/26)

Monorepo for our Fantasy Premier League assistant.

## Quick start

```bash
cp infra/.env.example infra/.env
# edit infra/.env with real secrets (Telegram token, DB URL, etc.)
docker compose -f infra/docker-compose.yml up --build
```

Visit:
- Backend API docs: http://localhost:8000/docs
- Frontend: http://localhost:3000

## Structure
(See tree above)

## Dev tips
- Run alembic migrations:
```bash
docker compose exec api alembic revision --autogenerate -m "init"
docker compose exec api alembic upgrade head
```
