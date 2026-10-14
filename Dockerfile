ARG BASE_IMAGE=python:3.12-slim

FROM ${BASE_IMAGE}

# Avoid Python writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install only the runtime requirements first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app/ ./app/

# Create the data directory for SQLite, owned by the non-root user
RUN mkdir -p /data && chown 10001:10001 /data

# Run as a non-root user
USER 10001:10001

# Default SQLite database path inside the container
ENV CARS_DB_PATH=/data/cars.db

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
