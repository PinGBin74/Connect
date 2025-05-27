FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry
RUN poetry lock
RUN poetry install --no-root

COPY . .

# Install wait-for-it script
RUN apt-get update && apt-get install -y wait-for-it

# Wait for database using correct host extraction and run migrations
CMD ["sh", "-c", "echo 'Waiting for database...'; wait-for-it $(echo $DATABASE_URL | sed 's/.*@\\([^:]*\\).*/\\1/'):5432 --timeout=30 -- poetry run alembic upgrade head && echo 'Migrations applied' || echo 'Migration failed: $?' && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]