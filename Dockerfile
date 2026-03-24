FROM python:3.12-slim AS base

WORKDIR /app

# System deps for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
RUN pip install --no-cache-dir .

COPY oneplanet_backend/ ./oneplanet_backend/
COPY docs/ ./docs/

ENV PYTHONPATH=/app
ENV ENVIRONMENT=production

EXPOSE 8000

CMD ["uvicorn", "oneplanet_backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
