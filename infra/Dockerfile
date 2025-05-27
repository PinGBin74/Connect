FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry
RUN poetry lock
RUN poetry install --no-root

COPY . .

# Install wait-for-it script
RUN apt-get update && apt-get install -y wait-for-it

# Wait for database with more debugging
CMD ["sh", "-c", "echo 'DATABASE_URL: $DATABASE_URL'; echo 'Waiting for database...'; wait-for-it $(echo $DATABASE_URL | sed 's/.*@\\([^:]*\\).*/\\1/'):5432 --timeout=30 -- echo 'Database available'; echo 'Applying migrations...'; poetry run alembic upgrade head; echo 'Migration command exit code: $?'; poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]