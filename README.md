# ANSI-Assistant

- `git clone https://github.com/creepydanunity/ANSI-Assistant.git`
- `cd backend`
- `touch .env` # Fill .env file. Example below.
- `cd ..` # Return to root
- `docker compose up --build -d`
- Check API Docs on http://localhost:80/docs #( Current API documentation available at http://64.225.65.211/redoc )

## backend/.env
```text
SECRET_KEY="SomeSecret"
ACCESS_TOKEN_EXPIRE_MINUTES=3600
OPENAI_API_KEY="API_KEY"
POSTGRES_DATABASE_URL="postgresql+asyncpg://user:password@db:5432/ansi"
```
