#!/usr/bin/env sh
set -e

echo "⏳ waiting for database to be ready…"
sleep 5

alembic stamp head

alembic revision --autogenerate -m "revisioned models"

alembic upgrade head

exec uvicorn main:app --host 0.0.0.0 --port 8000
