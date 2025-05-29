FROM python:3.11-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

COPY pyproject.toml poetry.lock* /app/
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

COPY src/ /app/src/

EXPOSE 8000

CMD ["uvicorn", "webhook_forwarder.main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "src"]
