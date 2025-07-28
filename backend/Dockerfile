FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

# Poetry
RUN pip install --no-cache-dir poetry==1.8.3
# 👇 Add this line so Poetry does NOT create a virtualenv
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-interaction --no-ansi

COPY . /app
ENV PYTHONPATH=/app
