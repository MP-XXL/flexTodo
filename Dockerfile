# # ---------------------------------------------------------------------------
# # Builder stage — install dependencies
# # ---------------------------------------------------------------------------
# FROM python:3.12-slim AS builder

# WORKDIR /app

# # System dependencies required for psycopg2
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     gcc \
#     libpq-dev \
#  && rm -rf /var/lib/apt/lists/*

# COPY requirements.txt .
# RUN pip install --upgrade pip \
#  && pip install --no-cache-dir --prefix=/install -r requirements.txt


# # ---------------------------------------------------------------------------
# # Runtime stage — lean production image
# # ---------------------------------------------------------------------------
# FROM python:3.12-slim AS runtime

# WORKDIR /app

# # Runtime system dependency for psycopg2
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     libpq5 \
#  && rm -rf /var/lib/apt/lists/*

# # Copy installed packages from builder
# COPY --from=builder /install /usr/local

# # Copy application source
# COPY . .

# # Non-root user for security
# RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
# USER appuser

# EXPOSE 8000

# # Gunicorn with Uvicorn workers for production
# CMD ["gunicorn", "app.main:app", \
#      "--worker-class", "uvicorn.workers.UvicornWorker", \
#      "--workers", "2", \
#      "--bind", "0.0.0.0:8000", \
#      "--timeout", "120", \
#      "--access-logfile", "-", \
#      "--error-logfile", "-"]


# ---------------------------------------------------------------------------
# Builder stage
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir --prefix=/install -r requirements.txt


# ---------------------------------------------------------------------------
# Runtime stage
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
 && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local
COPY . .

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser

# Render injects PORT at runtime; default to 8000 for local/Docker use.
ENV PORT=8000

EXPOSE ${PORT}

CMD gunicorn app.main:app \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers 2 \
    --bind 0.0.0.0:${PORT} \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -