# syntax=docker/dockerfile:1

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy files
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --no-root

# Copy the source code
COPY src/ /app/src/
COPY .env /app/.env

# Expose port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "webhook_forwarder.main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "src"]
