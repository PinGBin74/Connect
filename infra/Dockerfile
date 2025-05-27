FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry
RUN poetry lock
RUN poetry install --no-root

COPY . .

# Install wait-for-it script
RUN apt-get update && apt-get install -y wait-for-it

# Wait for database to be ready and then run migrations
CMD ["sh", "-c", "wait-for-it db:5432 -- poetry run alembic upgrade head && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]