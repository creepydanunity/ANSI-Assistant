# ANSI-Assistant

- `git clone https://github.com/creepydanunity/ANSI-Assistant.git`
- `cd backend`
- `touch .env` # Fill .env file. Example below.
- `docker compose up --build -d`
- Check API Docs on http://localhost:80/docs

## backend/.env
SECRET_KEY="SomeSecret"
ACCESS_TOKEN_EXPIRE_MINUTES=3600
OPENAI_API_KEY="API_KEY"
POSTGRES_DATABASE_URL="postgresql+asyncpg://user:password@db:5432/ansi"
