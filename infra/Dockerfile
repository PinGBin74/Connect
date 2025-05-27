FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry
RUN poetry lock
RUN poetry install --no-root

COPY . .

RUN apt-get update && apt-get install -y wait-for-it

CMD ["sh", "-c", "wait-for-it $(echo $DATABASE_URL | sed 's/.*@\\(.*\\)\\//\\1/'):5432 --timeout=30 -- poetry run alembic upgrade head && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]